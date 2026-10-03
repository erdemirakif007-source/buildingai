"""Complete the existing hakediş screen's API using its current ORM records.

Only drafts can change. Approval is an explicit site reviewer action and freezes
the quantity/price snapshot. Cancellation preserves the draft and its journal.
"""
import datetime as dt
import urllib.parse as _up
from decimal import Decimal
from io import BytesIO
from xml.sax.saxutils import escape


def _cd(filename: str) -> str:
    """RFC 5987 Content-Disposition — Türkçe dosya adlarını destekler."""
    encoded = _up.quote(filename, safe="")
    ascii_fb = filename.encode("ascii", errors="replace").decode("ascii")
    return f'attachment; filename="{ascii_fb}"; filename*=UTF-8\'\'{encoded}'

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update
from sqlalchemy.orm import Session
import database
import models
from access_control import require_site, require_hierarchy, scope_query
from financial_values import amount, number

router = APIRouter(prefix="/api/hakedis", tags=["Hakediş"])


def principal(request, db):
    from app import kullanici_dogrula, _request_token
    return kullanici_dogrula(_request_token(request), db)


def payment(db, user, payment_id, action="read"):
    row = scope_query(db, user, models.Hakedis).filter_by(id=payment_id).with_for_update().first()
    if not row or row.durum == "iptal":
        raise HTTPException(404, "Hakediş bulunamadı.")
    require_site(user, row.santiye_id, db, action)
    return row


def journal(row, user, event):
    line = f"[{dt.datetime.utcnow().isoformat()}Z] kullanıcı={user.id} {event}"
    row.notlar = ((row.notlar or "") + "\n" + line).strip()
    row.updated_at = dt.datetime.utcnow()


def draft_only(row):
    if row.durum != "taslak":
        raise HTTPException(409, "Yalnızca taslak hakediş düzenlenebilir.")


def previous_lines(db, row, work_id):
    query = db.query(models.HakedisKalemi).join(models.Hakedis).filter(
        models.HakedisKalemi.is_kalemi_id == work_id,
        models.Hakedis.santiye_id == row.santiye_id,
        models.Hakedis.organization_id == row.organization_id,
        models.Hakedis.durum == "onaylandi",
        models.Hakedis.hakedis_no < row.hakedis_no,
    )
    contract_link = db.get(models.PaymentContract, row.id)
    if contract_link:
        query = query.join(models.PaymentContract, models.PaymentContract.payment_id == models.Hakedis.id).filter(
            models.PaymentContract.contract_id == contract_link.contract_id)
    return query.all()


def recalculate(db, user, row):
    total = 0
    for line in row.kalemler:
        work = db.get(models.IsKalemi, line.is_kalemi_id)
        require_hierarchy(user, work, db)
        if work.santiye_id != row.santiye_id:
            raise HTTPException(409, "Hakediş ve iş kalemi şantiyeleri uyuşmuyor.")
        prior = previous_lines(db, row, work.id)
        prior_quantity = sum((number(p.bu_donem_miktar) for p in prior), Decimal(0))
        cumulative = prior_quantity + number(line.bu_donem_miktar)
        if cumulative > number(line.sozlesme_metraj):
            raise HTTPException(422, "Kümülatif miktar kayıtlı iş kalemi metrajını aşamaz.")
        period_amount = amount(line.bu_donem_miktar, line.birim_fiyat)
        cumulative_amount = sum(p.bu_donem_tutar or 0 for p in prior) + period_amount
        if period_amount < 0:
            raise HTTPException(409, "Önceki hakediş tutarıyla çelişki var; düzeltme incelemesi gerekir.")
        line.onceki_toplam_miktar = float(prior_quantity)
        line.kumulatif_miktar = float(cumulative)
        line.bu_donem_tutar = period_amount
        line.kumulatif_tutar = cumulative_amount
        total += period_amount
    row.toplam_tutar = total


@router.post("/olustur")
def create(request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    site = require_site(user, body.get("santiye_id"), db, "write")
    db.query(models.Santiye).filter_by(id=site.id).with_for_update().first()
    try:
        start = dt.date.fromisoformat(body.get("donem_baslangic", ""))
        end = dt.date.fromisoformat(body.get("donem_bitis", ""))
        if start > end:
            raise ValueError()
    except (ValueError, TypeError):
        raise HTTPException(422, "Geçerli başlangıç ve bitiş tarihlerini girin.")
    existing = db.query(models.Hakedis).filter_by(santiye_id=site.id).all()
    if any(p.durum in {"taslak", "onay_bekliyor", "reddedildi"} for p in existing):
        raise HTTPException(409, "Bu şantiyede sonuçlandırılmamış hakediş var.")
    if any(p.durum == "onaylandi" and p.donem_bitis >= start.isoformat() for p in existing):
        raise HTTPException(409, "Dönem, önceki onaylı hakedişten sonra başlamalıdır.")
    works = db.query(models.IsKalemi).filter_by(santiye_id=site.id).filter(models.IsKalemi.durum != "iptal").all()
    if db.query(models.ContractLine).join(models.Contract).filter(models.Contract.santiye_id == site.id).first():
        raise HTTPException(409, "Sözleşmeli proje için sözleşme hakedişini kullanın.")
    if not works:
        raise HTTPException(422, "Önce şantiyeye iş kalemi ekleyin.")
    row = models.Hakedis(organization_id=site.organization_id, santiye_id=site.id,
        hakedis_no=max((p.hakedis_no for p in existing), default=0) + 1,
        donem_baslangic=start.isoformat(), donem_bitis=end.isoformat(),
        hazirlayan_id=user.id, durum="taslak",
        onceki_toplam=sum(p.toplam_tutar or 0 for p in existing if p.durum == "onaylandi"))
    try:
        db.add(row)
        db.flush()
        for work in works:
            require_hierarchy(user, work, db)
            row.kalemler.append(models.HakedisKalemi(is_kalemi_id=work.id,
                sozlesme_metraj=work.metraj, birim_fiyat=work.birim_fiyat,
                bu_donem_miktar=0))
        recalculate(db, user, row)
        journal(row, user, "Taslak oluşturuldu; miktarlar inceleme bekliyor.")
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Eşzamanlı hakediş işlemi var; listeyi yenileyin.")
    return {"ok": True, "hakedis_id": row.id}


@router.patch("/kalem-guncelle")
def update_line(request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    line = db.query(models.HakedisKalemi).filter_by(id=body.get("hakedis_kalem_id")).first()
    if not line:
        raise HTTPException(404, "Hakediş kalemi bulunamadı.")
    row = payment(db, user, line.hakedis_id, "write")
    draft_only(row)
    if db.get(models.PaymentContract, row.id):
        raise HTTPException(409, "Sözleşmeli hakediş miktarı yalnız kontrol edilmiş ölçümden eklenebilir.")
    quantity = number(body.get("bu_donem_miktar"), "Miktar")
    old_quantity = line.bu_donem_miktar
    line.bu_donem_miktar = float(quantity)
    line.notlar = f"MANUEL: kullanıcı={user.id}; ilerleme tahmini bu miktarı değiştiremez."
    recalculate(db, user, row)
    journal(row, user, f"Kalem {line.id} miktarı: {old_quantity} → {quantity}")
    db.commit()
    return {"ok": True, "kalem": {"id": line.id, "kumulatif_miktar": line.kumulatif_miktar,
        "bu_donem_tutar": Decimal(line.bu_donem_tutar) / 100,
        "kumulatif_tutar": Decimal(line.kumulatif_tutar) / 100,
        "hakedis_toplam_tutar": Decimal(row.toplam_tutar) / 100}}


@router.patch("/durum-guncelle/{payment_id}")
def transition(request: Request, payment_id: int, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    target = body.get("durum")
    row = payment(db, user, payment_id, "review" if target in {"onaylandi", "reddedildi"} else "write")
    allowed = {"taslak": {"onay_bekliyor"}, "onay_bekliyor": {"onaylandi", "reddedildi", "taslak"}, "reddedildi": {"taslak"}}
    if target == row.durum:
        return {"ok": True, "durum": row.durum}
    if target not in allowed.get(row.durum, set()):
        raise HTTPException(409, "Bu hakediş durum geçişine izin verilmiyor.")
    reason = str(body.get("reason") or "").strip()
    if target == "reddedildi" and not reason:
        raise HTTPException(422, "Geri gönderme gerekçesi girin.")
    if target in {"onaylandi", "reddedildi"} and row.hazirlayan_id == user.id:
        raise HTTPException(403, "Hazırlayan kişi kendi hakedişine karar veremez.")
    contract_link = db.get(models.PaymentContract, row.id)
    if contract_link and target in {"onay_bekliyor", "onaylandi"}:
        allocations = db.query(models.PaymentAllocation).filter_by(payment_id=row.id).all()
        if not allocations:
            raise HTTPException(422, "Önce kontrol edilmiş ölçüm miktarı ekleyin.")
        for line in row.kalemler:
            used = sum((Decimal(a.quantity) for a in allocations
                if db.get(models.FieldMeasurement, a.measurement_id).work_item_id == line.is_kalemi_id), Decimal(0))
            if used != Decimal(str(line.bu_donem_miktar)):
                raise HTTPException(409, "Hakediş kalemi ile ölçüm tahsisleri uyuşmuyor.")
    if target in {"onay_bekliyor", "onaylandi"}:
        if not row.kalemler:
            raise HTTPException(422, "Hakedişte iş kalemi bulunmuyor.")
        recalculate(db, user, row)
    previous = row.durum
    changed = db.execute(update(models.Hakedis).where(
        models.Hakedis.id == row.id, models.Hakedis.durum == previous
    ).values(durum=target))
    if changed.rowcount != 1:
        db.rollback()
        raise HTTPException(409, "Hakediş başka kullanıcı tarafından değiştirildi; yenileyin.")
    db.add(models.PaymentDecision(payment_id=row.id, actor_id=user.id,
        previous_status=previous, new_status=target, reason=reason))
    journal(row, user, f"Durum: {previous} → {target}" + (f"; gerekçe: {reason}" if reason else ""))
    row.durum = target
    if target == "onaylandi":
        row.onaylayan_id = user.id
    db.commit()
    return {"ok": True, "durum": row.durum}


@router.get("/decisions/{payment_id}")
def decisions(request: Request, payment_id: int, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    payment(db, user, payment_id)
    rows = db.query(models.PaymentDecision).filter_by(payment_id=payment_id).order_by(models.PaymentDecision.id).all()
    _actor_ids = list({r.actor_id for r in rows})
    _actor_map = {u.id: (u.full_name or u.email)
                  for u in db.query(models.User).filter(models.User.id.in_(_actor_ids)).all()} if _actor_ids else {}
    return {"decisions": [
        {"actor_id": x.actor_id,
         "actor_ad": _actor_map.get(x.actor_id),
         "previous_status": x.previous_status,
         "new_status": x.new_status,
         "reason": x.reason,
         "created_at": x.created_at.isoformat()}
        for x in rows
    ]}


@router.delete("/sil/{payment_id}")
def cancel(request: Request, payment_id: int, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    row = payment(db, user, payment_id, "write")
    draft_only(row)
    for allocation in db.query(models.PaymentAllocation).filter_by(payment_id=row.id).all():
        db.execute(models.FieldMeasurement.__table__.update().where(
            models.FieldMeasurement.id == allocation.measurement_id
        ).values(allocated_quantity=models.FieldMeasurement.allocated_quantity - allocation.quantity))
        db.delete(allocation)
    journal(row, user, "Taslak iptal edildi; geçmiş ve kalemler korundu.")
    row.durum = "iptal"
    db.commit()
    return {"ok": True}


@router.get("/pdf/{payment_id}")
def export_pdf(request: Request, payment_id: int, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    row = payment(db, user, payment_id)
    from pdf_rapor import NORMAL_FONT, BOLD_FONT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    style = ParagraphStyle("payment", fontName=NORMAL_FONT, fontSize=9, leading=12)
    title = ParagraphStyle("title", parent=style, fontName=BOLD_FONT, fontSize=16, leading=22)
    def money(value):
        return f"{Decimal(value or 0) / 100:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".") + " TL"
    stream = BytesIO()
    elements = [Paragraph(f"BuildingAI — Hakediş #{row.hakedis_no}", title),
        Paragraph(escape(f"{row.santiye.ad} | {row.donem_baslangic} – {row.donem_bitis}"), style),
        Paragraph(escape(f"Durum: {row.durum}. KDV kapsamı kayıtta belirtilmemiştir."), style),
        Paragraph("Bu çıktı kayıtlı miktar ve birim fiyat özetidir; ödeme yapıldığını göstermez.", style), Spacer(1,16)]
    data = [["İş kalemi", "Birim", "Bu dönem miktar", "Birim fiyat", "Dönem tutarı"]]
    for line in row.kalemler:
        require_hierarchy(user, line.is_kalemi, db)
        if line.is_kalemi.santiye_id != row.santiye_id:
            raise HTTPException(409, "Hakedişte tutarsız iş kalemi ilişkisi var.")
        data.append([Paragraph(escape(line.is_kalemi.tanim), style), line.is_kalemi.birim,
                     str(line.bu_donem_miktar), money(line.birim_fiyat), money(line.bu_donem_tutar)])
    table = Table(data, colWidths=[167,42,90,95,95], repeatRows=1)
    table.setStyle(TableStyle([("FONTNAME",(0,0),(-1,-1),NORMAL_FONT),
        ("FONTSIZE",(0,0),(-1,-1),8),("VALIGN",(0,0),(-1,-1),"TOP"),
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#fff0e5")),
        ("GRID",(0,0),(-1,-1),.3,colors.HexColor("#dddddd")),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    elements += [table, Spacer(1,16), Paragraph(f"Bu dönem: {money(row.toplam_tutar)}", title),
                 Paragraph(f"Önceki onaylı hakedişler: {money(row.onceki_toplam)}", style)]
    SimpleDocTemplate(stream,pagesize=A4,rightMargin=36,leftMargin=36).build(elements)
    return Response(stream.getvalue(),media_type="application/pdf",headers={
        "Content-Disposition": _cd(f"BuildingAI_Hakedis_{row.hakedis_no}.pdf"),
        "Cache-Control": "private, no-store"})
