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
from sqlalchemy import text
from sqlalchemy.orm import Session

import auth
import database
import models

logger = logging.getLogger("buildingai.bim")


# ── Yetki yardımcısı ──────────────────────────────────────────────────────────

def _bim_santiye_yetkisi_kontrol(user: models.User, santiye_id: int, db: Session) -> None:
    """
    Kullanıcının verilen şantiyeye (aynı organization) erişim hakkı olup olmadığını
    kontrol eder. Hak yoksa HTTPException 403 fırlatır.
    """
    if not user.organization_id:
        raise HTTPException(status_code=403, detail="Kullanıcının organizasyonu tanımlanmamış.")
    santiye = db.query(models.Santiye).filter(
        models.Santiye.id == santiye_id,
        models.Santiye.organization_id == user.organization_id,
    ).first()
    if not santiye:
        raise HTTPException(status_code=403, detail="Bu şantiyeye erişim yetkiniz yok.")

# ── Depolama ayarları ───────────────────────────────────────────────────────
BIM_UPLOAD_ROOT = Path("uploads/bim")
BIM_UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB

# ── Router ──────────────────────────────────────────────────────────────────
bim_router = APIRouter(prefix="/api/bim", tags=["BIM Viewer"])


# ── Auth yardımcısı ─────────────────────────────────────────────────────────

def _bim_kullanici_dogrula(request: Request, db: Session) -> models.User:
    """
    Authorization header'dan (Bearer <token>) ya da query param 'token'
    üzerinden kullanıcıyı doğrular. HTTPException 401 fırlatır.
    """
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip() if auth_header else ""
    if not token:
        token = request.query_params.get("token", "")
    if not token:
        raise HTTPException(status_code=401, detail="Yetkilendirme başlığı eksik.")
    try:
        payload = auth.verify_token(token)
        email = payload.get("email")
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı.")
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Token geçersiz.")


# ── Pydantic şemaları ────────────────────────────────────────────────────────

class MappingItem(BaseModel):
    ifc_global_id: str
    is_kalemi_id: int


class BulkMappingBody(BaseModel):
    mappings: List[MappingItem]


class SingleMappingBody(BaseModel):
    ifc_global_id: str
    is_kalemi_id: int


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
    _bim_santiye_yetkisi_kontrol(user, santiye_id, db)

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
async def bim_model_progress(
    request: Request,
    model_id: int,
    db: Session = Depends(database.get_db),
):
    """
    BIM model elemanlarına atanmış iş kalemlerinin ilerleme durumunu döner.
    Response formatı progressColoring.ts'deki ElementProgressMapping interface'ine uyumludur.
    """
    user = _bim_kullanici_dogrula(request, db)

    bim_model = db.query(models.BimModel).filter(models.BimModel.id == model_id).first()
    if not bim_model:
        raise HTTPException(status_code=404, detail="BIM modeli bulunamadı.")
    _bim_santiye_yetkisi_kontrol(user, bim_model.santiye_id, db)

    # JOIN + correlated subquery — text() ile okunabilirlik korunur
    q = text("""
        SELECT
            e.id              AS eslestirme_id,
            e.ifc_global_id,
            e.ifc_tip,
            e.ifc_kat,
            e.is_kalemi_id,
            ik.tanim          AS is_kalemi_tanim,
            ik.birim          AS is_kalemi_birim,
            ik.durum          AS is_kalemi_durum,
            ik.metraj         AS is_kalemi_metraj,
            (
                SELECT irl.yuzde
                FROM ilerleme_kayitlari irl
                WHERE irl.is_kalemi_id = e.is_kalemi_id
                ORDER BY irl.created_at DESC
                LIMIT 1
            ) AS tamamlanma_yuzdesi
        FROM bim_element_eslestirme e
        LEFT JOIN is_kalemleri ik ON ik.id = e.is_kalemi_id
        WHERE e.bim_model_id = :model_id
        ORDER BY e.ifc_global_id
    """)

    with database.engine.connect() as conn:
        rows = conn.execute(q, {"model_id": model_id}).fetchall()

    mappings = []
    for row in rows:
        d = _row_to_dict(row)
        pct = d.get("tamamlanma_yuzdesi")
        mappings.append({
            "eslestirme_id":      d["eslestirme_id"],
            "ifc_global_id":      d["ifc_global_id"],
            "ifc_tip":            d.get("ifc_tip"),
            "ifc_kat":            d.get("ifc_kat"),
            "is_kalemi_id":       d.get("is_kalemi_id"),
            "is_kalemi_tanim":    d.get("is_kalemi_tanim"),
            "is_kalemi_birim":    d.get("is_kalemi_birim"),
            "is_kalemi_durum":    _normalize_durum(d.get("is_kalemi_durum")),
            "is_kalemi_metraj":   d.get("is_kalemi_metraj"),
            "tamamlanma_yuzdesi": float(pct) if pct is not None else None,
            "renk_kodu": _progress_renk(pct, _normalize_durum(d.get("is_kalemi_durum"))),
        })

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

    eslestirme = db.query(models.BimElementEslestirme).filter_by(
        bim_model_id=model_id,
        ifc_global_id=body.ifc_global_id,
    ).first()

    if eslestirme:
        eslestirme.is_kalemi_id = body.is_kalemi_id
        eslestirme.eslestiren_kullanici_id = user.id
        eslestirme.eslestirme_tarihi = dt.utcnow()
    else:
        eslestirme = models.BimElementEslestirme(
            bim_model_id=model_id,
            ifc_global_id=body.ifc_global_id,
            is_kalemi_id=body.is_kalemi_id,
            eslestiren_kullanici_id=user.id,
        )
        db.add(eslestirme)

    db.commit()

    logger.info(
        "BIM mapping: model=%d global_id=%s → is_kalemi=%d user=%s",
        model_id, body.ifc_global_id, body.is_kalemi_id, user.email,
    )
    return {
        "status": "ok",
        "model_id": model_id,
        "ifc_global_id": body.ifc_global_id,
        "is_kalemi_id": body.is_kalemi_id,
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
                    eslestirme.is_kalemi_id = item.is_kalemi_id
                    eslestirme.eslestiren_kullanici_id = user.id
                    eslestirme.eslestirme_tarihi = dt.utcnow()
                else:
                    db.add(models.BimElementEslestirme(
                        bim_model_id=model_id,
                        ifc_global_id=item.ifc_global_id,
                        is_kalemi_id=item.is_kalemi_id,
                        eslestiren_kullanici_id=user.id,
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
    _bim_santiye_yetkisi_kontrol(user, bim_model.santiye_id, db)

    db.delete(eslestirme)
    db.commit()

    logger.info(
        "BIM mapping silindi: model=%d eslestirme=%d user=%s",
        model_id, eslestirme_id, user.email,
    )
    return {"status": "ok", "eslestirme_id": eslestirme_id}


# ── POST /api/bim/model/{model_id}/element/{eslestirme_id}/ilerleme ───────────

@bim_router.post(
    "/model/{model_id}/element/{eslestirme_id}/ilerleme",
    summary="BIM elementi üzerinden iş kalemi ilerleme güncelle — stok ve hakediş tetikle",
)
async def bim_element_ilerleme_guncelle(
    request: Request,
    model_id: int,
    eslestirme_id: int,
    body: ElementIlerlemeBody,
    db: Session = Depends(database.get_db),
):
    """
    Tek bir BIM elementinin ilerleme yüzdesini günceller.

    Yan etkiler (yuzde == 100 ise):
      • is_kalemleri.durum → 'tamamlandi'
      • CsbIsKalemiMalzeme reçetesinden otomatik stok çıkışı (StokHareket)
      • StokEsik kontrolü — kritik seviye uyarıları response'a eklenir
      • Taslak hakedişte ilgili HakedisKalemi güncellenir
    """
    user = _bim_kullanici_dogrula(request, db)

    # ── 1. Eşleştirme kaydını doğrula ───────────────────────────────────────
    eslestirme = (
        db.query(models.BimElementEslestirme)
        .filter(
            models.BimElementEslestirme.id == eslestirme_id,
            models.BimElementEslestirme.bim_model_id == model_id,
        )
        .first()
    )
    if not eslestirme:
        raise HTTPException(status_code=404, detail="BIM element eşleştirmesi bulunamadı.")
    if not eslestirme.is_kalemi_id:
        raise HTTPException(status_code=400, detail="Bu element henüz bir iş kalemine eşlenmemiş.")

    # ── 2. Model erişilebilirlik kontrolü ────────────────────────────────────
    bim_model = (
        db.query(models.BimModel)
        .filter(models.BimModel.id == model_id, models.BimModel.durum != "silindi")
        .first()
    )
    if not bim_model:
        raise HTTPException(status_code=404, detail="BIM modeli bulunamadı.")

    # ── 3. İş kalemi ────────────────────────────────────────────────────────
    try:
        is_kalemi = db.query(models.IsKalemi).filter(
            models.IsKalemi.id == eslestirme.is_kalemi_id
        ).with_for_update().first()
    except Exception:
        # SQLite FOR UPDATE desteklemiyor; PostgreSQL'de kilitler çalışır
        is_kalemi = db.query(models.IsKalemi).filter(
            models.IsKalemi.id == eslestirme.is_kalemi_id
        ).first()
    if not is_kalemi:
        raise HTTPException(status_code=404, detail="İş kalemi bulunamadı.")

    # ── 4. Yüzde sınırla ve tamamlanma bayrağı ──────────────────────────────
    yuzde = max(0.0, min(100.0, body.yuzde))
    yuzde_tam = yuzde >= 100.0

    # ── 5. IlerlemeKaydi oluştur ─────────────────────────────────────────────
    notlar_metin = body.notlar.strip() if body.notlar else "BIM üzerinden güncellendi"
    ilerleme_kaydi = models.IlerlemeKaydi(
        is_kalemi_id=is_kalemi.id,
        raporlayan_id=user.id,
        yuzde=yuzde,
        tarih=dt.utcnow().date().isoformat(),
        notlar=notlar_metin,
    )
    db.add(ilerleme_kaydi)
    db.flush()  # id'yi al, commit etme

    # ── 6. Tamamlandı durumu ─────────────────────────────────────────────────
    onceki_durum = is_kalemi.durum
    if yuzde_tam:
        is_kalemi.durum = "tamamlandi"

    # ── 7. Stok sarf + eşik kontrolü ────────────────────────────────────────
    # Stok çıkışı yalnızca bu çağrı ile GERÇEKTEN tamamlandı ise tetiklenir.
    # Daha önce "tamamlandi" olan kalemlerde tekrar çıkış yapılmaz (idempotan).
    stok_hareketleri: list[dict] = []
    esik_uyarilari:   list[dict] = []

    if yuzde_tam and is_kalemi.katalog_id and onceki_durum != "tamamlandi":
        santiye = db.query(models.Santiye).filter(
            models.Santiye.id == is_kalemi.santiye_id
        ).first()
        org_id = santiye.organization_id if santiye else None

        recete = (
            db.query(models.CsbIsKalemiMalzeme)
            .filter(models.CsbIsKalemiMalzeme.is_kalemi_katalog_id == is_kalemi.katalog_id)
            .all()
        )

        for rec in recete:
            # malzeme adını doğrudan malzemeler tablosundan al (ORM modeli yok)
            with database.engine.connect() as conn:
                malzeme_row = conn.execute(
                    text("SELECT ad, birim FROM malzemeler WHERE id = :id"),
                    {"id": rec.malzeme_katalog_id},
                ).fetchone()

            if not malzeme_row:
                continue

            malzeme_adi = malzeme_row.ad
            sarfiyat    = rec.miktar * (is_kalemi.metraj or 0)

            hareket = models.StokHareket(
                malzeme=malzeme_adi,
                malzeme_ad=malzeme_adi,
                miktar=sarfiyat,
                tip="cikis",
                kaynak="sarf",
                kullanici_id=user.id,
                santiye_id=is_kalemi.santiye_id,
                organization_id=org_id,
                notlar=f"BIM sarf — {is_kalemi.tanim[:50]}",
            )
            db.add(hareket)
            stok_hareketleri.append({
                "malzeme":  malzeme_adi,
                "miktar":   round(sarfiyat, 4),
                "birim":    rec.birim,
                "tip":      "cikis",
                "kaynak":   "sarf",
            })

            # Eşik kontrolü: mevcut net stok (bu çıkış hariç) - sarfiyat
            with database.engine.connect() as conn:
                esik_row = conn.execute(
                    text("""
                        SELECT
                          COALESCE(SUM(CASE WHEN tip='giris' THEN miktar ELSE 0 END), 0)
                          - COALESCE(SUM(CASE WHEN tip='cikis' THEN miktar ELSE 0 END), 0)
                          - :sarfiyat AS net
                        FROM stok_hareketler
                        WHERE malzeme = :malzeme AND santiye_id = :santiye_id
                    """),
                    {
                        "malzeme":    malzeme_adi,
                        "santiye_id": is_kalemi.santiye_id,
                        "sarfiyat":   sarfiyat,
                    },
                ).fetchone()

            kalan = float(esik_row.net or 0) if esik_row else 0.0

            esik = db.query(models.StokEsik).filter(
                models.StokEsik.malzeme == malzeme_adi,
                models.StokEsik.santiye_id == is_kalemi.santiye_id,
            ).first()
            if esik and kalan < esik.min_miktar:
                esik_uyarilari.append({
                    "malzeme":    malzeme_adi,
                    "kalan":      round(kalan, 3),
                    "min_miktar": esik.min_miktar,
                    "acik":       kalan < 0,
                })

    # ── 8. Aktif taslak hakediş güncelle ────────────────────────────────────
    hakedis_guncellendi = False
    hakedis = (
        db.query(models.Hakedis)
        .filter(
            models.Hakedis.santiye_id == is_kalemi.santiye_id,
            models.Hakedis.durum == "taslak",
        )
        .order_by(models.Hakedis.hakedis_no.desc())
        .first()
    )
    if hakedis:
        hk = db.query(models.HakedisKalemi).filter(
            models.HakedisKalemi.hakedis_id == hakedis.id,
            models.HakedisKalemi.is_kalemi_id == is_kalemi.id,
        ).first()
        if hk:
            hk.bu_donem_miktar = round(is_kalemi.metraj * yuzde / 100.0, 4)
            hk.bu_donem_tutar  = round(hk.bu_donem_miktar * is_kalemi.birim_fiyat)
            hakedis_guncellendi = True

    db.commit()
    db.refresh(ilerleme_kaydi)

    logger.info(
        "BIM ilerleme: model=%d eslestirme=%d is_kalemi=%d yuzde=%.1f stok=%d hakedis=%s user=%s",
        model_id, eslestirme_id, is_kalemi.id, yuzde,
        len(stok_hareketleri), hakedis_guncellendi, user.email,
    )

    return {
        "ilerleme_id":        ilerleme_kaydi.id,
        "yuzde":              yuzde,
        "is_kalemi_id":       is_kalemi.id,
        "is_kalemi_tanim":    is_kalemi.tanim,
        "durum_guncellendi":  yuzde_tam,
        "stok_hareketleri":   stok_hareketleri,
        "esik_uyarilari":     esik_uyarilari,
        "hakedis_guncellendi": hakedis_guncellendi,
    }
