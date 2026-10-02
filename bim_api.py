"""
bim_api.py — BIM Viewer API Router
====================================
Tüm /api/bim/* endpoint'leri bu dosyada tanımlanır.
app.py'de `app.include_router(bim_router)` ile dahil edilir.

Tablolar ORM üzerinden models.py'de tanımlıdır:
  - models.BimModel              (IFC/FRAG dosya meta verisi)
  - models.BimElementEslestirme  (IFC GlobalId ↔ iş kalemi eşleştirme)

Auth: Mevcut JWT tabanlı kullanici_dogrula() helper'ı kullanılır.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime as dt
from difflib import SequenceMatcher
from pathlib import Path
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Request,
    UploadFile,
)
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

import auth
import database
import models
from access_control import require_site, require_hierarchy

# ai_client lazy import — app.py başlatıldıktan sonra erişilebilir
def _get_ai_client():
    try:
        from app import ai_client  # noqa: PLC0415
        return ai_client
    except Exception:
        return None

logger = logging.getLogger("buildingai.bim")


# ── Yetki yardımcısı ──────────────────────────────────────────────────────────

def _bim_santiye_yetkisi_kontrol(user, santiye_id, db):
    require_site(user, santiye_id, db)

# ── Depolama ayarları ───────────────────────────────────────────────────────
BIM_UPLOAD_ROOT = Path("uploads/bim")
BIM_UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB

# ── Router ──────────────────────────────────────────────────────────────────
bim_router = APIRouter(prefix="/api/bim", tags=["BIM Viewer"])


# ── Auth yardımcısı ─────────────────────────────────────────────────────────

def _bim_kullanici_dogrula(request: Request, db: Session) -> models.User:
    from app import kullanici_dogrula, _request_token
    return kullanici_dogrula(_request_token(request), db)


# ── Pydantic şemaları ────────────────────────────────────────────────────────

class MappingItem(BaseModel):
    ifc_global_id: str
    is_kalemi_id: int
    ifc_tip: Optional[str] = None
    ifc_kat: Optional[str] = None
    metraj: Optional[float] = None
    metraj_birimi: Optional[str] = None
    metraj_kaynagi: Optional[str] = None  # "ifc_quantity" | "manuel"


class BulkMappingBody(BaseModel):
    mappings: List[MappingItem]


class SingleMappingBody(BaseModel):
    ifc_global_id: str
    is_kalemi_id: int
    ifc_tip: Optional[str] = None
    ifc_kat: Optional[str] = None
    metraj: Optional[float] = None
    metraj_birimi: Optional[str] = None
    metraj_kaynagi: Optional[str] = None  # "ifc_quantity" | "manuel"


class SuggestBody(BaseModel):
    ifc_element_adi: str


class ElementIlerlemeBody(BaseModel):
    yuzde: float
    notlar: Optional[str] = None


# ── Yardımcı fonksiyonlar ────────────────────────────────────────────────────

def _model_dir(santiye_id: int) -> Path:
    """Şantiyeye özel yükleme dizinini döner (yoksa oluşturur)."""
    d = BIM_UPLOAD_ROOT / str(santiye_id)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _parse_metadata(json_str: Optional[str]) -> dict:
    try:
        return json.loads(json_str or "{}")
    except Exception:
        return {}


def _bim_model_to_dict(m: models.BimModel) -> dict:
    return {
        "id": m.id,
        "santiye_id": m.santiye_id,
        "blok_id": m.blok_id,
        "dosya_adi": m.dosya_adi,
        "orijinal_dosya_adi": m.orijinal_dosya_adi,
        "fragment_dosya_yolu": m.fragment_dosya_yolu,
        "ifc_dosya_yolu": m.ifc_dosya_yolu,
        "dosya_boyutu": m.dosya_boyutu,
        "yukleme_tarihi": m.yukleme_tarihi.isoformat() if m.yukleme_tarihi else None,
        "yukleyen_kullanici_id": m.yukleyen_kullanici_id,
        "durum": m.durum,
        "metadata": _parse_metadata(m.metadata_json),
        "fragment_hazir": bool(m.fragment_dosya_yolu),
    }


def _row_to_dict(row) -> dict:
    """SQLAlchemy Row / RowMapping → plain dict (text() sorguları için)."""
    return dict(row._mapping) if hasattr(row, "_mapping") else dict(row)


# ════════════════════════════════════════════════════════════════════════════
# ENDPOINT'LER
# ════════════════════════════════════════════════════════════════════════════

# ── POST /api/bim/upload ─────────────────────────────────────────────────────

@bim_router.post("/upload", summary="IFC dosyası yükle")
async def bim_upload(
    request: Request,
    santiye_id: int = Form(...),
    blok_id: Optional[int] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):
    """
    IFC dosyasını alır, uploads/bim/<santiye_id>/ altına kaydeder
    ve bim_modeller tablosuna kayıt ekler.
    """
    user = _bim_kullanici_dogrula(request, db)
    require_site(user, santiye_id, db, "write")
    if blok_id:
        block = db.query(models.Bina).filter_by(id=blok_id, santiye_id=santiye_id).first()
        if not block:
            raise HTTPException(422, "Blok modelin şantiyesine ait olmalıdır.")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Dosya çok büyük. Maksimum izin verilen boyut: 500 MB.",
        )

    orijinal_ad = file.filename or "model.ifc"
    ext = Path(orijinal_ad).suffix.lower() or ".ifc"
    yeni_ad = f"{uuid.uuid4().hex}{ext}"

    santiye_dir = _model_dir(santiye_id)
    ifc_yolu = santiye_dir / yeni_ad
    ifc_yolu.write_bytes(contents)

    logger.info(
        "BIM upload: user=%s santiye=%s dosya=%s boyut=%d",
        user.email, santiye_id, yeni_ad, len(contents),
    )

    bim_model = models.BimModel(
        santiye_id=santiye_id,
        blok_id=blok_id,
        dosya_adi=yeni_ad,
        orijinal_dosya_adi=orijinal_ad,
        ifc_dosya_yolu=str(ifc_yolu),
        dosya_boyutu=len(contents),
        yukleyen_kullanici_id=user.id,
        durum="aktif",
    )
    db.add(bim_model)
    db.commit()
    db.refresh(bim_model)

    return {
        "model_id": bim_model.id,
        "dosya_adi": yeni_ad,
        "orijinal_dosya_adi": orijinal_ad,
        "dosya_boyutu": len(contents),
    }


# ── GET /api/bim/models ───────────────────────────────────────────────────────

@bim_router.get("/models", summary="Şantiyeye ait BIM modellerini listele")
async def bim_models_listele(
    request: Request,
    santiye_id: int = Query(..., description="Şantiye ID"),
    db: Session = Depends(database.get_db),
):
    user = _bim_kullanici_dogrula(request, db)
    _bim_santiye_yetkisi_kontrol(user, santiye_id, db)

    modeller_rows = (
        db.query(models.BimModel)
        .filter(
            models.BimModel.santiye_id == santiye_id,
            models.BimModel.durum != "silindi",
        )
        .order_by(models.BimModel.yukleme_tarihi.desc())
        .all()
    )

    return {"modeller": [_bim_model_to_dict(m) for m in modeller_rows], "toplam": len(modeller_rows)}


# ── GET /api/bim/model/{model_id}/download ───────────────────────────────────

@bim_router.get(
    "/model/{model_id}/download",
    summary="BIM model dosyasını indir (.frag varsa .frag, yoksa .ifc)",
)
async def bim_model_indir(
    request: Request,
    model_id: int,
    db: Session = Depends(database.get_db),
):
    user = _bim_kullanici_dogrula(request, db)

    bim_model = db.query(models.BimModel).filter(models.BimModel.id == model_id).first()
    if not bim_model:
        raise HTTPException(status_code=404, detail="BIM modeli bulunamadı.")
    if bim_model.durum == "silindi":
        raise HTTPException(status_code=410, detail="Bu model silinmiş.")
    _bim_santiye_yetkisi_kontrol(user, bim_model.santiye_id, db)

    dosya_yolu: Optional[str] = bim_model.fragment_dosya_yolu or bim_model.ifc_dosya_yolu
    if not dosya_yolu or not Path(dosya_yolu).exists():
        raise HTTPException(status_code=404, detail="Model dosyası sunucuda bulunamadı.")

    return FileResponse(
        path=dosya_yolu,
        media_type="application/octet-stream",
        filename=Path(dosya_yolu).name,
    )


# ── POST /api/bim/model/{model_id}/fragment ──────────────────────────────────

@bim_router.post(
    "/model/{model_id}/fragment",
    summary="Dönüştürülmüş .frag dosyasını yükle ve kaydet",
)
async def bim_fragment_yukle(
    request: Request,
    model_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):
    """
    Frontend IFC → .frag dönüşümünü tamamladığında bu endpoint'i çağırır.
    Sonraki açılışlarda IFC yerine .frag yüklenir (≈10× hızlı).
    """
    user = _bim_kullanici_dogrula(request, db)

    bim_model = db.query(models.BimModel).filter(models.BimModel.id == model_id).first()
    if not bim_model:
        raise HTTPException(status_code=404, detail="BIM modeli bulunamadı.")
    require_site(user, bim_model.santiye_id, db, "write")
    if bim_model.durum == "silindi":
        raise HTTPException(status_code=410, detail="Bu model silinmiş.")
    _bim_santiye_yetkisi_kontrol(user, bim_model.santiye_id, db)

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Fragment dosyası çok büyük (maks 500 MB).")

    # Eski fragment dosyasını diskten temizle
    if bim_model.fragment_dosya_yolu:
        eski_frag = Path(bim_model.fragment_dosya_yolu)
        try:
            if eski_frag.exists():
                eski_frag.unlink()
        except OSError as exc:
            logger.warning("Eski fragment silinemedi: %s — %s", eski_frag, exc)

    santiye_dir = _model_dir(bim_model.santiye_id)
    frag_yolu = santiye_dir / f"{model_id}_{uuid.uuid4().hex[:8]}.frag"
    frag_yolu.write_bytes(contents)

    # dosya_boyutu orijinal IFC boyutunu korur; fragment boyutunu ayrı logla
    bim_model.fragment_dosya_yolu = str(frag_yolu)
    db.commit()

    logger.info("BIM fragment kaydedildi: model_id=%d frag=%s", model_id, frag_yolu)
    return {
        "model_id": model_id,
        "fragment_dosya_yolu": str(frag_yolu),
        "dosya_boyutu": len(contents),
    }


# ── DELETE /api/bim/model/{model_id} ─────────────────────────────────────────

@bim_router.delete("/model/{model_id}", summary="BIM modelini sil (soft delete)")
async def bim_model_sil(
    request: Request,
    model_id: int,
    db: Session = Depends(database.get_db),
):
    user = _bim_kullanici_dogrula(request, db)

    bim_model = db.query(models.BimModel).filter(models.BimModel.id == model_id).first()
    if not bim_model:
        raise HTTPException(status_code=404, detail="BIM modeli bulunamadı.")
    require_site(user, bim_model.santiye_id, db, "write")
    if bim_model.durum == "silindi":
        raise HTTPException(status_code=410, detail="Bu model zaten silinmiş.")
    _bim_santiye_yetkisi_kontrol(user, bim_model.santiye_id, db)

    bim_model.durum = "silindi"
    db.commit()

    # Disk'teki IFC ve fragment dosyalarını temizle
    for dosya_yolu_str in filter(None, [bim_model.ifc_dosya_yolu, bim_model.fragment_dosya_yolu]):
        try:
            p = Path(dosya_yolu_str)
            if p.exists():
                p.unlink()
                logger.info("BIM dosya silindi: %s", p)
        except OSError as exc:
            logger.warning("BIM dosya silinemedi: %s — %s", dosya_yolu_str, exc)

    logger.info("BIM model soft-delete: model_id=%d user=%s", model_id, user.email)
    return {"status": "ok", "model_id": model_id, "durum": "silindi"}


# ── GET /api/bim/model/{model_id}/progress ───────────────────────────────────

@bim_router.get(
    "/model/{model_id}/progress",
    summary="Element–iş kalemi eşleştirmeleri ve ilerleme verisi",
)
async def bim_model_progress(request: Request, model_id: int, db: Session = Depends(database.get_db)):
    user = _bim_kullanici_dogrula(request, db)
    model = db.query(models.BimModel).filter_by(id=model_id).first()
    if not model or model.durum == "silindi":
        raise HTTPException(404, "BIM modeli bulunamadı.")
    require_site(user, model.santiye_id, db)
    mappings = []
    rows = db.query(models.BimElementEslestirme).filter_by(bim_model_id=model_id).order_by(models.BimElementEslestirme.ifc_global_id).all()
    for row in rows:
        ik = row.is_kalemi
        if ik:
            _validate_mapping(user, model, ik.id, db, "read")
        progress = db.query(models.IlerlemeKaydi).filter_by(is_kalemi_id=row.is_kalemi_id).order_by(models.IlerlemeKaydi.created_at.desc(), models.IlerlemeKaydi.id.desc()).first() if ik else None
        pct = progress.yuzde if progress else None
        durum = _normalize_durum(ik.durum) if ik else None
        mappings.append({"eslestirme_id": row.id, "ifc_global_id": row.ifc_global_id,
            "ifc_tip": row.ifc_tip, "ifc_kat": row.ifc_kat, "is_kalemi_id": row.is_kalemi_id,
            "is_kalemi_tanim": ik.tanim if ik else None, "is_kalemi_birim": ik.birim if ik else None,
            "is_kalemi_durum": durum, "is_kalemi_metraj": ik.metraj if ik else None,
            "tamamlanma_yuzdesi": pct, "renk_kodu": _progress_renk(pct, durum)})
    return {"model_id": model_id, "eslestirmeler": mappings, "toplam": len(mappings)}


_DURUM_MAP = {"devam_eden": "devam_ediyor"}


def _normalize_durum(durum: Optional[str]) -> Optional[str]:
    """DB'deki eski durum değerlerini progressColoring.ts'in beklediği forma çevirir."""
    if durum is None:
        return None
    return _DURUM_MAP.get(durum, durum)


def _progress_renk(pct, durum: Optional[str]) -> str:
    """İlerleme yüzdesine ve duruma göre renk kodu döner."""
    if durum == "iptal":
        return "#9E9E9E"        # gri — iptal
    if pct is None:
        return "#607D8B"        # mavi-gri — eşleşmiş ama ilerleme kaydı yok
    if pct >= 100 or durum == "tamamlandi":
        return "#4CAF50"        # yeşil — tamamlandı
    if pct >= 75:
        return "#8BC34A"        # açık yeşil
    if pct >= 50:
        return "#FFC107"        # sarı
    if pct >= 25:
        return "#FF9800"        # turuncu
    if pct > 0:
        return "#FF5722"        # koyu turuncu
    return "#F44336"            # kırmızı — başlanmadı


# ── POST /api/bim/model/{model_id}/mapping ───────────────────────────────────

@bim_router.post(
    "/model/{model_id}/mapping",
    summary="Tek element–iş kalemi eşleştirmesi kaydet/güncelle",
)
async def bim_mapping_kaydet(
    request: Request,
    model_id: int,
    body: SingleMappingBody,
    db: Session = Depends(database.get_db),
):
    user = _bim_kullanici_dogrula(request, db)

    bim_model = db.query(models.BimModel).filter(
        models.BimModel.id == model_id,
        models.BimModel.durum != "silindi",
    ).first()
    if not bim_model:
        raise HTTPException(status_code=404, detail="BIM modeli bulunamadı.")
    require_site(user, bim_model.santiye_id, db, "write")

    _validate_mapping(user, bim_model, body.is_kalemi_id, db)
    eslestirme = db.query(models.BimElementEslestirme).filter_by(
        bim_model_id=model_id,
        ifc_global_id=body.ifc_global_id,
    ).first()

    if eslestirme:
        eslestirme.is_kalemi_id             = body.is_kalemi_id
        eslestirme.eslestiren_kullanici_id  = user.id
        eslestirme.eslestirme_tarihi        = dt.utcnow()
        if body.ifc_tip       is not None: eslestirme.ifc_tip       = body.ifc_tip
        if body.ifc_kat       is not None: eslestirme.ifc_kat       = body.ifc_kat
        if body.metraj        is not None: eslestirme.metraj        = body.metraj
        if body.metraj_birimi is not None: eslestirme.metraj_birimi = body.metraj_birimi
        if body.metraj_kaynagi is not None: eslestirme.metraj_kaynagi = body.metraj_kaynagi
    else:
        eslestirme = models.BimElementEslestirme(
            bim_model_id            = model_id,
            ifc_global_id           = body.ifc_global_id,
            is_kalemi_id            = body.is_kalemi_id,
            eslestiren_kullanici_id = user.id,
            ifc_tip                 = body.ifc_tip,
            ifc_kat                 = body.ifc_kat,
            metraj                  = body.metraj,
            metraj_birimi           = body.metraj_birimi,
            metraj_kaynagi          = body.metraj_kaynagi,
        )
        db.add(eslestirme)

    db.commit()

    logger.info(
        "BIM mapping: model=%d global_id=%s → is_kalemi=%d metraj=%s%s user=%s",
        model_id, body.ifc_global_id, body.is_kalemi_id,
        body.metraj, body.metraj_birimi or "", user.email,
    )
    return {
        "status":        "ok",
        "model_id":      model_id,
        "ifc_global_id": body.ifc_global_id,
        "is_kalemi_id":  body.is_kalemi_id,
        "metraj":        body.metraj,
        "metraj_birimi": body.metraj_birimi,
    }


# ── POST /api/bim/model/{model_id}/mapping/bulk ──────────────────────────────

@bim_router.post(
    "/model/{model_id}/mapping/bulk",
    summary="Toplu element–iş kalemi eşleştirmesi kaydet/güncelle",
)
async def bim_mapping_bulk(
    request: Request,
    model_id: int,
    body: BulkMappingBody,
    db: Session = Depends(database.get_db),
):
    user = _bim_kullanici_dogrula(request, db)

    if not body.mappings:
        raise HTTPException(status_code=400, detail="'mappings' listesi boş olamaz.")

    bim_model = db.query(models.BimModel).filter(
        models.BimModel.id == model_id,
        models.BimModel.durum != "silindi",
    ).first()
    if not bim_model:
        raise HTTPException(status_code=404, detail="BIM modeli bulunamadı.")
    require_site(user, bim_model.santiye_id, db, "write")

    for item in body.mappings:
        _validate_mapping(user, bim_model, item.is_kalemi_id, db)
    basarili = 0
    hatalar: list[dict] = []

    for item in body.mappings:
        try:
            with db.begin_nested():
                eslestirme = db.query(models.BimElementEslestirme).filter_by(
                    bim_model_id=model_id,
                    ifc_global_id=item.ifc_global_id,
                ).first()
                if eslestirme:
                    eslestirme.is_kalemi_id            = item.is_kalemi_id
                    eslestirme.eslestiren_kullanici_id = user.id
                    eslestirme.eslestirme_tarihi       = dt.utcnow()
                    if item.ifc_tip        is not None: eslestirme.ifc_tip        = item.ifc_tip
                    if item.ifc_kat        is not None: eslestirme.ifc_kat        = item.ifc_kat
                    if item.metraj         is not None: eslestirme.metraj         = item.metraj
                    if item.metraj_birimi  is not None: eslestirme.metraj_birimi  = item.metraj_birimi
                    if item.metraj_kaynagi is not None: eslestirme.metraj_kaynagi = item.metraj_kaynagi
                else:
                    db.add(models.BimElementEslestirme(
                        bim_model_id            = model_id,
                        ifc_global_id           = item.ifc_global_id,
                        is_kalemi_id            = item.is_kalemi_id,
                        eslestiren_kullanici_id = user.id,
                        ifc_tip                 = item.ifc_tip,
                        ifc_kat                 = item.ifc_kat,
                        metraj                  = item.metraj,
                        metraj_birimi           = item.metraj_birimi,
                        metraj_kaynagi          = item.metraj_kaynagi,
                    ))
            basarili += 1
        except Exception as exc:
            hatalar.append({
                "ifc_global_id": item.ifc_global_id,
                "hata": str(exc)[:120],
            })

    db.commit()

    logger.info(
        "BIM bulk mapping: model=%d basarili=%d hata=%d user=%s",
        model_id, basarili, len(hatalar), user.email,
    )
    return {
        "status": "ok" if not hatalar else "partial",
        "model_id": model_id,
        "basarili": basarili,
        "hata_sayisi": len(hatalar),
        "hatalar": hatalar,
    }


# ── POST /api/bim/model/{model_id}/mapping/suggest ───────────────────────────

@bim_router.post(
    "/model/{model_id}/mapping/suggest",
    summary="IFC element adına göre iş kalemi önerileri getir (fuzzy match)",
)
async def bim_mapping_suggest(
    request: Request,
    model_id: int,
    body: SuggestBody,
    db: Session = Depends(database.get_db),
):
    """
    IFC element adını mevcut iş kalemleriyle fuzzy karşılaştırır,
    benzerlik skoru 0.4 üstündeki sonuçları sıralı döndürür.
    mappingPanel'deki 'Öneriler' butonu için kullanılır.
    """
    user = _bim_kullanici_dogrula(request, db)

    bim_model = db.query(models.BimModel).filter(
        models.BimModel.id == model_id,
        models.BimModel.durum != "silindi",
    ).first()
    if not bim_model:
        raise HTTPException(status_code=404, detail="BIM modeli bulunamadı.")
    require_site(user, bim_model.santiye_id, db, "write")

    is_kalemleri = (
        db.query(models.IsKalemi)
        .filter(models.IsKalemi.santiye_id == bim_model.santiye_id)
        .all()
    )

    aranan = body.ifc_element_adi.lower()
    oneriler = []
    for ik in is_kalemleri:
        skor = SequenceMatcher(None, aranan, ik.tanim.lower()).ratio()
        if skor >= 0.4:
            oneriler.append({
                "is_kalemi_id":    ik.id,
                "is_kalemi_tanim": ik.tanim,
                "benzerlik_skoru": round(skor, 3),
                "poz_no":          ik.poz_no,
            })

    oneriler.sort(key=lambda x: x["benzerlik_skoru"], reverse=True)

    return {
        "model_id":        model_id,
        "ifc_element_adi": body.ifc_element_adi,
        "oneriler":        oneriler,
    }


# ── DELETE /api/bim/model/{model_id}/mapping/{eslestirme_id} ─────────────────

@bim_router.delete(
    "/model/{model_id}/mapping/{eslestirme_id}",
    summary="Element–iş kalemi eşleştirmesini sil",
)
async def bim_mapping_sil(
    request: Request,
    model_id: int,
    eslestirme_id: int,
    db: Session = Depends(database.get_db),
):
    user = _bim_kullanici_dogrula(request, db)

    eslestirme = (
        db.query(models.BimElementEslestirme)
        .filter(
            models.BimElementEslestirme.id == eslestirme_id,
            models.BimElementEslestirme.bim_model_id == model_id,
        )
        .first()
    )
    if not eslestirme:
        raise HTTPException(status_code=404, detail="Eşleştirme bulunamadı.")

    bim_model = db.query(models.BimModel).filter(models.BimModel.id == model_id).first()
    if not bim_model:
        raise HTTPException(status_code=404, detail="BIM modeli bulunamadı.")
    require_site(user, bim_model.santiye_id, db, "write")
    _bim_santiye_yetkisi_kontrol(user, bim_model.santiye_id, db)

    db.delete(eslestirme)
    db.commit()

    logger.info(
        "BIM mapping silindi: model=%d eslestirme=%d user=%s",
        model_id, eslestirme_id, user.email,
    )
    return {"status": "ok", "eslestirme_id": eslestirme_id}


# ── POST /api/bim/ai/eslestirme-oner ─────────────────────────────────────────

# Basit in-memory rate limiter: {user_id: [timestamp, ...]}
import time as _time
from collections import defaultdict as _defaultdict
_ai_suggest_calls: dict = _defaultdict(list)
_AI_RATE_LIMIT = 10     # dakikada max istek sayısı
_AI_RATE_WINDOW = 60.0  # saniye


class AiElementBilgi(BaseModel):
    ifc_type: str
    name: str
    object_type: Optional[str] = None
    predefined_type: Optional[str] = None
    storey: Optional[str] = None
    properties: Optional[dict] = None


class AiEslestirmeOnerBody(BaseModel):
    santiye_id: int
    element: AiElementBilgi


@bim_router.post(
    "/ai/eslestirme-oner",
    summary="IFC elementi için AI destekli iş kalemi önerisi (ÇŞB kataloğu + Gemini)",
)
async def bim_ai_eslestirme_oner(
    request: Request,
    body: AiEslestirmeOnerBody,
    db: Session = Depends(database.get_db),
):
    """
    Verilen IFC element bilgisine göre ÇŞB kataloğundan en uygun
    iş kalemlerini Gemini ile önerir; ayrıca DB'den malzeme reçetesini ekler.
    """
    user = _bim_kullanici_dogrula(request, db)
    _bim_santiye_yetkisi_kontrol(user, body.santiye_id, db)

    # ── Rate limit kontrolü ──────────────────────────────────────────────────
    now = _time.time()
    pencere = _AI_RATE_WINDOW
    _ai_suggest_calls[user.id] = [
        t for t in _ai_suggest_calls[user.id] if now - t < pencere
    ]
    if len(_ai_suggest_calls[user.id]) >= _AI_RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Dakikada 10 AI önerisi limitine ulaşıldı. Biraz bekleyin.",
        )
    _ai_suggest_calls[user.id].append(now)

    # ── Adım 1: Katalog listesini çek ────────────────────────────────────────
    katalog_listesi = (
        db.query(models.CsbIsKalemiKatalog)
        .filter(models.CsbIsKalemiKatalog.aktif == 1)
        .all()
    )
    katalog_text = "\n".join(
        f"ID:{k.id} | Poz:{k.poz_no} | {k.grup} > {k.alt_grup or '-'} | {k.ad} | Birim:{k.birim}"
        for k in katalog_listesi
    )

    # ── Adım 2: Gemini prompt ────────────────────────────────────────────────
    el = body.element
    props_json = json.dumps(el.properties or {}, ensure_ascii=False)
    prompt = f"""Sen bir inşaat mühendisi yapay zeka asistanısın.

Aşağıdaki IFC BIM elementini incele ve en uygun ÇŞB iş kalemlerini öner.

## IFC Element Bilgileri
- Tip: {el.ifc_type}
- İsim: {el.name}
- Obje Tipi: {el.object_type or '-'}
- Ön Tanımlı Tip: {el.predefined_type or '-'}
- Kat: {el.storey or '-'}
- Özellikler: {props_json}

## Mevcut ÇŞB İş Kalemi Kataloğu
{katalog_text}

## Görev
Bu element için en uygun 1-3 iş kalemini öner. Her öneri için:
1. Katalog ID'si (yukarıdaki listeden)
2. Eşleşme güven skoru (0-100)
3. Kısa gerekçe (1 cümle, Türkçe)
4. Elementten çıkarılabilecek metraj değeri ve birimi (properties'den)

SADECE aşağıdaki JSON formatında yanıt ver, başka hiçbir şey yazma:
{{
  "oneriler": [
    {{
      "katalog_id": 5,
      "poz_no": "16.003/1",
      "guven_skoru": 92,
      "gerekce": "C25/30 kolon elementi, beton dökümü iş kalemiyle eşleşiyor",
      "metraj": 2.88,
      "metraj_birimi": "m³",
      "metraj_kaynagi": "Qto_ColumnBaseQuantities.GrossVolume"
    }}
  ]
}}"""

    # ── Adım 3: Gemini çağrısı ────────────────────────────────────────────────
    ai = _get_ai_client()
    if ai is None:
        raise HTTPException(
            status_code=503,
            detail="AI servisi şu an kullanılamıyor. GEMINI_API_KEY ayarını kontrol edin.",
        )

    try:
        response = ai.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        response_text = response.text
    except Exception as exc:
        logger.error("Gemini AI öneri hatası: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=f"AI servisi yanıt vermedi: {str(exc)[:200]}",
        )

    # ── Adım 4: JSON parse ────────────────────────────────────────────────────
    try:
        # Gemini bazen ```json ... ``` wrapper ekler
        clean = response_text.strip()
        if clean.startswith("```"):
            clean = clean.split("```", 2)[1]
            if clean.startswith("json"):
                clean = clean[4:]
            clean = clean.rsplit("```", 1)[0]
        parsed = json.loads(clean.strip())
        oneriler_raw: list = parsed.get("oneriler", [])
    except Exception:
        logger.warning("Gemini yanıtı parse edilemedi: %s", response_text[:300])
        return {
            "status": "error",
            "error": "AI yanıtı işlenemedi",
            "raw": response_text[:500],
        }

    # ── Adım 5: DB'den katalog detayı + malzeme reçetesi ekle ─────────────────
    katalog_map = {k.id: k for k in katalog_listesi}
    oneriler_zengin = []

    for oneri in oneriler_raw:
        kid = oneri.get("katalog_id")
        katalog = katalog_map.get(kid)
        if katalog is None:
            # Gemini yanlış ID verdiyse poz_no ile tekrar ara
            poz = oneri.get("poz_no", "")
            katalog = next((k for k in katalog_listesi if k.poz_no == poz), None)

        recete = []
        if katalog:
            csb_malzemeler = (
                db.query(models.CsbIsKalemiMalzeme)
                .filter(models.CsbIsKalemiMalzeme.is_kalemi_katalog_id == katalog.id)
                .all()
            )
            for cm in csb_malzemeler:
                malzeme = db.query(models.MalzemeKatalog).filter(
                    models.MalzemeKatalog.id == cm.malzeme_katalog_id
                ).first()
                recete.append({
                    "malzeme":              malzeme.ad if malzeme else f"#{cm.malzeme_katalog_id}",
                    "miktar_birim_basina":  cm.miktar,
                    "birim":                cm.birim,
                    "zorunlu":              bool(cm.zorunlu),
                })

        oneriler_zengin.append({
            "katalog_id":     katalog.id   if katalog else kid,
            "poz_no":         katalog.poz_no if katalog else oneri.get("poz_no"),
            "ad":             katalog.ad   if katalog else oneri.get("poz_no"),
            "birim":          katalog.birim if katalog else None,
            "guven_skoru":    oneri.get("guven_skoru", 0),
            "gerekce":        oneri.get("gerekce", ""),
            "metraj":         oneri.get("metraj"),
            "metraj_birimi":  oneri.get("metraj_birimi"),
            "metraj_kaynagi": oneri.get("metraj_kaynagi"),
            "malzeme_recetesi": recete,
        })

    logger.info(
        "BIM AI öneri: santiye=%d element=%s tip=%s oneri_sayisi=%d user=%s",
        body.santiye_id, el.name, el.ifc_type, len(oneriler_zengin), user.email,
    )
    return {"status": "ok", "oneriler": oneriler_zengin}


# ── POST /api/bim/model/{model_id}/element/{eslestirme_id}/ilerleme ───────────

@bim_router.post(
    "/model/{model_id}/element/{eslestirme_id}/ilerleme",
    summary="BIM elementi üzerinden iş kalemi ilerleme güncelle — stok ve hakediş tetikle",
)
async def bim_element_ilerleme_guncelle(request: Request, model_id: int, eslestirme_id: int,
                                      body: ElementIlerlemeBody, db: Session = Depends(database.get_db)):
    from app import _save_progress
    user = _bim_kullanici_dogrula(request, db)
    model = db.query(models.BimModel).filter_by(id=model_id).first()
    if not model or model.durum == "silindi":
        raise HTTPException(404, "BIM modeli bulunamadı.")
    require_site(user, model.santiye_id, db, "write")
    mapping = db.query(models.BimElementEslestirme).filter_by(id=eslestirme_id, bim_model_id=model_id).first()
    if not mapping or not mapping.is_kalemi_id:
        raise HTTPException(404, "BIM element eşleştirmesi bulunamadı.")
    ik = _validate_mapping(user, model, mapping.is_kalemi_id, db)
    result = _save_progress(db, user, ik.id, {"yuzde": body.yuzde, "notlar": body.notlar})
    return {**result, "is_kalemi_id": ik.id, "is_kalemi_tanim": ik.tanim,
            "durum_guncellendi": body.yuzde == 100, "stok_hareketleri": [],
            "hakedis_guncellendi": bool(result["hakedis_guncelleme"])}


def _validate_mapping(user, model, work_id, db, action="write"):
    ik = db.query(models.IsKalemi).filter_by(id=work_id, santiye_id=model.santiye_id).first()
    if not ik:
        raise HTTPException(422, "İş kalemi modelin şantiyesine ait olmalıdır.")
    require_hierarchy(user, ik, db, action)
    return ik
