"""Unit-price contract, field measurement and payment provenance endpoints."""
import datetime as dt
import uuid
from decimal import Decimal

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import database
import models
from access_control import require_site, require_hierarchy, scope_query
from financial_values import amount, kurus, number

router = APIRouter(prefix="/api/v2", tags=["Saha ve sözleşme"])

STARTER_MATERIALS = (
    ("beton", "Beton", "m³", "Beton, çimento ve agrega"),
    ("cimento", "Çimento", "kg", "Beton, çimento ve agrega"),
    ("agrega", "Agrega", "m³", "Beton, çimento ve agrega"),
    ("donati", "Donatı çeliği", "kg", "Donatı ve çelik"),
    ("baglanti", "Çelik bağlantı elemanı", "adet", "Donatı ve çelik"),
    ("kalip", "Kalıp malzemesi", "adet", "Kalıp ve iskele"),
    ("iskele", "İskele malzemesi", "adet", "Kalıp ve iskele"),
    ("duvar", "Duvar malzemesi", "adet", "Duvar ve çatı"),
    ("cati", "Çatı malzemesi", "adet", "Duvar ve çatı"),
    ("su_yalitimi", "Su yalıtımı", "m²", "Yalıtım"),
    ("isi_yalitimi", "Isı yalıtımı", "m²", "Yalıtım"),
    ("kimyasal", "Yapı kimyasalı", "kg", "Yapı kimyasalları ve tamir"),
    ("grout", "Grout", "kg", "Yapı kimyasalları ve tamir"),
    ("tamir_harci", "Tamir harcı", "kg", "Yapı kimyasalları ve tamir"),
    ("ankraj", "Ankraj", "adet", "Ankraj ve dübel"),
    ("kimyasal_dubel", "Kimyasal dübel", "adet", "Ankraj ve dübel"),
    ("altyapi_borusu", "Altyapı borusu", "m", "Altyapı boruları"),
    ("boru_baglantisi", "Boru bağlantı parçası", "adet", "Altyapı boruları"),
    ("elektrik", "Elektrik malzemesi", "adet", "Elektrik ve mekanik"),
    ("mekanik", "Mekanik malzeme", "adet", "Elektrik ve mekanik"),
    ("sarf", "Sarf malzemesi", "adet", "Sarf ve İSG"),
    ("isg", "İSG ekipmanı", "adet", "Sarf ve İSG"),
)


def principal(request, db):
    from app import kullanici_dogrula, _request_token
    return kullanici_dogrula(_request_token(request), db)


def quantity(value, label="Miktar"):
    raw = number(value, label)
    if raw != raw.quantize(Decimal("0.001")):
        raise HTTPException(422, f"{label} en fazla üç ondalık basamak içerebilir.")
    return raw


def contract(db, user, contract_id, action="read"):
    row = db.get(models.Contract, contract_id)
    if row is None:
        raise HTTPException(404, "Sözleşme bulunamadı.")
    require_site(user, row.santiye_id, db, action)
    return row


def measurement(db, user, record_id, action="read"):
    row = db.get(models.FieldMeasurement, record_id)
    if row is None:
        raise HTTPException(404, "Ölçüm bulunamadı.")
    require_site(user, row.santiye_id, db, action)
    return row


def serialize_measurement(db, row):
    links = db.query(models.MeasurementEvidence).filter_by(measurement_id=row.id).all()
    return {"id": row.id, "santiye_id": row.santiye_id, "area_id": row.area_id,
        "contract_line_id": row.contract_line_id, "work_item_id": row.work_item_id,
        "work_date": row.work_date, "reported_quantity": str(row.reported_quantity) if row.reported_quantity is not None else None,
        "accepted_quantity": str(row.accepted_quantity), "allocated_quantity": str(row.allocated_quantity),
        "remaining_quantity": str(Decimal(row.accepted_quantity) - Decimal(row.allocated_quantity)),
        "unit": row.unit, "basis": row.basis, "status": row.status,
        "created_by": row.created_by, "reviewed_by": row.reviewed_by,
        "review_reason": row.review_reason, "evidence_ids": [link.archive_record_id for link in links]}


@router.get("/santiye/{site_id}/areas")
def areas(site_id: int, request: Request, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    require_site(user, site_id, db)
    rows = db.query(models.WorkArea).filter_by(santiye_id=site_id).order_by(models.WorkArea.id).all()
    return {"areas": [{"id": x.id, "name": x.name, "kind": x.kind, "parent_id": x.parent_id} for x in rows]}


@router.get("/santiye/{site_id}/capabilities")
def site_capabilities(site_id: int, request: Request, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    require_site(user, site_id, db)
    result = {"user_id": user.id, "can_write": False, "can_review": False}
    for action, key in (("write", "can_write"), ("review", "can_review")):
        try:
            require_site(user, site_id, db, action)
            result[key] = True
        except HTTPException:
            pass
    return result


@router.post("/santiye/{site_id}/areas")
def add_area(site_id: int, request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    require_site(user, site_id, db, "write")
    name = str(body.get("name") or "").strip()
    if not name:
        raise HTTPException(422, "Çalışma alanı adını girin.")
    parent_id = body.get("parent_id")
    if parent_id and (not (parent := db.get(models.WorkArea, parent_id)) or parent.santiye_id != site_id):
        raise HTTPException(422, "Üst alan aynı projede olmalıdır.")
    row = models.WorkArea(santiye_id=site_id, name=name, kind=str(body.get("kind") or "bolge"), parent_id=parent_id)
    db.add(row)
    db.commit()
    return {"id": row.id}


@router.get("/santiye/{site_id}/contracts")
def contracts(site_id: int, request: Request, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    require_site(user, site_id, db)
    rows = db.query(models.Contract).filter_by(santiye_id=site_id).order_by(models.Contract.id).all()
    return {"contracts": [{"id": x.id, "name": x.name, "reference": x.reference,
        "direction": x.direction, "counterparty": x.counterparty, "currency": x.currency,
        "pricing_type": x.pricing_type, "start_date": x.start_date, "end_date": x.end_date} for x in rows]}


@router.post("/santiye/{site_id}/contracts")
def add_contract(site_id: int, request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    require_site(user, site_id, db, "write")
    if body.get("direction") not in ("employer", "subcontractor"):
        raise HTTPException(422, "Sözleşme yönü işveren veya taşeron olmalıdır.")
    if body.get("pricing_type", "unit_price") != "unit_price":
        raise HTTPException(422, "Bu akış yalnız birim fiyatlı sözleşmeleri destekler.")
    name, party = str(body.get("name") or "").strip(), str(body.get("counterparty") or "").strip()
    if not name or not party:
        raise HTTPException(422, "Sözleşme adı ve karşı taraf zorunludur.")
    currency = str(body.get("currency") or "TRY").upper()
    if len(currency) != 3 or not currency.isalpha():
        raise HTTPException(422, "Üç harfli para birimi girin.")
    row = models.Contract(santiye_id=site_id, name=name, counterparty=party,
        reference=body.get("reference"), direction=body["direction"], currency=currency,
        start_date=body.get("start_date"), end_date=body.get("end_date"))
    db.add(row)
    db.commit()
    return {"id": row.id}


@router.get("/contracts/{contract_id}/lines")
def contract_lines(contract_id: int, request: Request, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    contract(db, user, contract_id)
    rows = db.query(models.ContractLine).filter_by(contract_id=contract_id).order_by(models.ContractLine.id).all()
    return {"lines": [{"id": x.id, "work_item_id": x.work_item_id, "code": x.code,
        "description": x.description, "unit": x.unit, "quantity": str(x.quantity),
        "unit_price": str(Decimal(x.unit_price_kurus) / 100), "revision_of_id": x.revision_of_id} for x in rows]}


@router.post("/contracts/{contract_id}/lines")
def add_contract_line(contract_id: int, request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    owner = contract(db, user, contract_id, "write")
    work = db.get(models.IsKalemi, body.get("work_item_id"))
    require_hierarchy(user, work, db)
    if work.santiye_id != owner.santiye_id:
        raise HTTPException(422, "İş kalemi sözleşmeyle aynı projede olmalıdır.")
    qty = quantity(body.get("quantity"))
    if qty <= 0:
        raise HTTPException(422, "Sözleşme miktarı sıfırdan büyük olmalıdır.")
    revision = body.get("revision_of_id")
    if revision and (not (prior := db.get(models.ContractLine, revision)) or prior.contract_id != contract_id):
        raise HTTPException(422, "Revizyon bağlantısı aynı sözleşmede olmalıdır.")
    row = models.ContractLine(contract_id=contract_id, work_item_id=work.id,
        code=str(body.get("code") or work.poz_no or "").strip(),
        description=str(body.get("description") or work.tanim).strip(), unit=str(body.get("unit") or work.birim).strip(),
        quantity=qty, unit_price_kurus=kurus(body.get("unit_price")), revision_of_id=revision)
    if not row.code or not row.description or not row.unit:
        raise HTTPException(422, "Kod, açıklama ve birim zorunludur.")
    try:
        db.add(row)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Bu iş kalemi sözleşmeye zaten bağlı.")
    return {"id": row.id}


@router.get("/santiye/{site_id}/measurements")
def measurements(site_id: int, request: Request, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    require_site(user, site_id, db)
    rows = db.query(models.FieldMeasurement).filter_by(santiye_id=site_id).order_by(models.FieldMeasurement.id.desc()).all()
    return {"measurements": [serialize_measurement(db, row) for row in rows]}


@router.post("/santiye/{site_id}/measurements")
def add_measurement(site_id: int, request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    require_site(user, site_id, db, "write")
    key = body.get("request_key")
    if key:
        prior = db.query(models.FieldMeasurement).filter_by(santiye_id=site_id, request_key=key).first()
        if prior:
            if any((
                body.get("contract_line_id") != prior.contract_line_id,
                body.get("area_id") != prior.area_id,
                body.get("basis") != prior.basis,
                body.get("work_date") != prior.work_date,
                body.get("reported_quantity") is not None and quantity(body["reported_quantity"]) != prior.reported_quantity,
            )):
                raise HTTPException(409, "Bu tekrar önleme anahtarı başka bir ölçüme ait.")
            return serialize_measurement(db, prior)
    row = models.FieldMeasurement(santiye_id=site_id, created_by=user.id, request_key=key)
    db.add(row)
    fill_measurement(db, row, site_id, body)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        prior = db.query(models.FieldMeasurement).filter_by(santiye_id=site_id, request_key=key).first() if key else None
        if prior:
            return serialize_measurement(db, prior)
        raise HTTPException(409, "Kayıt çakıştı; listeyi yenileyin.")
    return serialize_measurement(db, row)


def fill_measurement(db, row, site_id, body):
    if body.get("area_id"):
        area = db.get(models.WorkArea, body["area_id"])
        if not area or area.santiye_id != site_id:
            raise HTTPException(422, "Çalışma alanı aynı projede olmalıdır.")
        row.area_id = area.id
    if body.get("contract_line_id"):
        line = db.get(models.ContractLine, body["contract_line_id"])
        owner = db.get(models.Contract, line.contract_id) if line else None
        if not owner or owner.santiye_id != site_id:
            raise HTTPException(422, "Sözleşme kalemi aynı projede olmalıdır.")
        row.contract_line_id, row.work_item_id, row.unit = line.id, line.work_item_id, line.unit
    for key in ("work_date", "basis"):
        if key in body:
            setattr(row, key, body[key])
    if "reported_quantity" in body and body["reported_quantity"] is not None:
        row.reported_quantity = quantity(body["reported_quantity"])
    if "evidence_ids" in body:
        db.flush()
        for link in db.query(models.MeasurementEvidence).filter_by(measurement_id=row.id).all():
            db.delete(link)
        db.flush()
        for record_id in dict.fromkeys(body["evidence_ids"]):
            evidence = db.get(models.ArchiveRecord, record_id)
            if not evidence or evidence.santiye_id != site_id:
                raise HTTPException(422, "Dayanak kaydı aynı projede olmalıdır.")
            db.add(models.MeasurementEvidence(measurement_id=row.id, archive_record_id=record_id))


@router.patch("/measurements/{record_id}")
def edit_measurement(record_id: int, request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    row = measurement(db, user, record_id, "write")
    if row.status != "draft" or row.created_by != user.id:
        raise HTTPException(409, "Yalnız kendi taslak ölçümünüzü düzenleyebilirsiniz.")
    fill_measurement(db, row, row.santiye_id, body)
    db.commit()
    return serialize_measurement(db, row)


@router.post("/measurements/{record_id}/submit")
def submit_measurement(record_id: int, request: Request, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    row = measurement(db, user, record_id, "write")
    if row.created_by != user.id or row.status != "draft":
        raise HTTPException(409, "Yalnız kendi taslağınızı kontrole gönderebilirsiniz.")
    if not all((row.contract_line_id, row.work_date, row.basis, row.reported_quantity is not None)):
        raise HTTPException(422, "Sözleşme kalemi, tarih, miktar ve ölçüm dayanağını tamamlayın.")
    if row.reported_quantity <= 0:
        raise HTTPException(422, "Bildirilen miktar sıfırdan büyük olmalıdır.")
    db.add(models.MeasurementDecision(measurement_id=row.id, actor_id=user.id,
        previous_status=row.status, new_status="pending"))
    row.status = "pending"
    db.commit()
    return serialize_measurement(db, row)


@router.post("/measurements/{record_id}/review")
def review_measurement(record_id: int, request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    row = measurement(db, user, record_id, "review")
    if row.status != "pending":
        raise HTTPException(409, "Ölçüm kontrol beklemiyor.")
    if row.created_by == user.id:
        raise HTTPException(403, "Hazırlayan kişi kendi ölçümünü kontrol edemez.")
    accepted = quantity(body.get("accepted_quantity"), "Kabul miktarı")
    if accepted > Decimal(row.reported_quantity):
        raise HTTPException(422, "Kabul miktarı bildirilen miktarı aşamaz.")
    reason = str(body.get("reason") or "").strip()
    if accepted != Decimal(row.reported_quantity) and not reason:
        raise HTTPException(422, "Kısmi kabul veya geri gönderme için gerekçe girin.")
    target = "accepted" if accepted > 0 else "returned"
    db.add(models.MeasurementDecision(measurement_id=row.id, actor_id=user.id,
        previous_status=row.status, new_status=target, reason=reason))
    row.status, row.accepted_quantity, row.reviewed_by, row.review_reason = target, accepted, user.id, reason
    db.commit()
    return serialize_measurement(db, row)


@router.get("/measurements/{record_id}/decisions")
def measurement_decisions(record_id: int, request: Request, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    measurement(db, user, record_id)
    rows = db.query(models.MeasurementDecision).filter_by(measurement_id=record_id).order_by(models.MeasurementDecision.id).all()
    return {"decisions": [{"actor_id": x.actor_id, "previous_status": x.previous_status,
        "new_status": x.new_status, "reason": x.reason, "created_at": x.created_at.isoformat()} for x in rows]}


@router.post("/contracts/{contract_id}/payments")
def create_payment(contract_id: int, request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    owner = contract(db, user, contract_id, "write")
    try:
        start = dt.date.fromisoformat(body.get("start_date", ""))
        end = dt.date.fromisoformat(body.get("end_date", ""))
        if end < start:
            raise ValueError()
    except (ValueError, TypeError):
        raise HTTPException(422, "Geçerli hakediş dönemi girin.")
    site = db.query(models.Santiye).filter_by(id=owner.santiye_id).with_for_update().first()
    existing = db.query(models.Hakedis).filter_by(santiye_id=site.id).all()
    if any(x.durum in ("taslak", "onay_bekliyor", "reddedildi") for x in existing):
        raise HTTPException(409, "Önce açık hakedişi sonuçlandırın.")
    lines = db.query(models.ContractLine).filter_by(contract_id=contract_id).all()
    if not lines:
        raise HTTPException(422, "Sözleşmeye iş kalemi ekleyin.")
    row = models.Hakedis(santiye_id=site.id, organization_id=site.organization_id,
        hakedis_no=max((x.hakedis_no for x in existing), default=0) + 1,
        donem_baslangic=start.isoformat(), donem_bitis=end.isoformat(), hazirlayan_id=user.id,
        durum="taslak", onceki_toplam=sum(x.toplam_tutar or 0 for x in existing if x.durum == "onaylandi"))
    try:
        db.add(row)
        db.flush()
        db.add(models.PaymentContract(payment_id=row.id, contract_id=contract_id))
        for line in lines:
            db.add(models.HakedisKalemi(hakedis_id=row.id, is_kalemi_id=line.work_item_id,
                sozlesme_metraj=float(line.quantity), birim_fiyat=line.unit_price_kurus,
                bu_donem_miktar=0))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Hakediş numarası çakıştı; listeyi yenileyin.")
    return {"id": row.id, "contract_id": contract_id}


@router.post("/payments/{payment_id}/allocations")
def allocate(payment_id: int, request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    payment = scope_query(db, user, models.Hakedis).filter_by(id=payment_id).first()
    link = db.get(models.PaymentContract, payment_id)
    if not payment or not link:
        raise HTTPException(404, "Sözleşmeli hakediş bulunamadı.")
    require_site(user, payment.santiye_id, db, "write")
    if payment.durum != "taslak":
        raise HTTPException(409, "Yalnız taslağa miktar eklenebilir.")
    row = measurement(db, user, body.get("measurement_id"))
    contract_line = db.get(models.ContractLine, row.contract_line_id) if row.contract_line_id else None
    if row.santiye_id != payment.santiye_id or not contract_line or contract_line.contract_id != link.contract_id:
        raise HTTPException(422, "Ölçüm bu hakedişin sözleşmesine ait değil.")
    qty = quantity(body.get("quantity"))
    if qty <= 0 or row.status != "accepted":
        raise HTTPException(422, "Kontrol edilmiş, pozitif miktar seçin.")
    # Atomic predicate is effective on SQLite too, where SELECT FOR UPDATE is ignored.
    result = db.execute(update(models.FieldMeasurement).where(
        models.FieldMeasurement.id == row.id,
        models.FieldMeasurement.status == "accepted",
        models.FieldMeasurement.allocated_quantity + qty <= models.FieldMeasurement.accepted_quantity,
    ).values(allocated_quantity=models.FieldMeasurement.allocated_quantity + qty))
    if result.rowcount != 1:
        db.rollback()
        raise HTTPException(409, "Kabul edilmiş miktarın kullanılabilir bakiyesi yetersiz.")
    from hakedis_api import recalculate
    payment_line = db.query(models.HakedisKalemi).filter_by(hakedis_id=payment_id, is_kalemi_id=contract_line.work_item_id).first()
    if not payment_line:
        db.rollback()
        raise HTTPException(409, "Hakediş kalemi bulunamadı.")
    allocation = db.query(models.PaymentAllocation).filter_by(payment_id=payment_id, measurement_id=row.id).first()
    if allocation:
        allocation.quantity = Decimal(allocation.quantity) + qty
        allocation.amount_kurus = amount(allocation.quantity, contract_line.unit_price_kurus)
    else:
        db.add(models.PaymentAllocation(payment_id=payment_id, measurement_id=row.id,
            quantity=qty, amount_kurus=amount(qty, contract_line.unit_price_kurus)))
    payment_line.bu_donem_miktar = float(quantity(payment_line.bu_donem_miktar) + qty)
    recalculate(db, user, payment)
    db.commit()
    return {"payment_id": payment_id, "measurement_id": row.id,
        "quantity": str(qty), "period_amount": str(Decimal(payment_line.bu_donem_tutar) / 100)}


@router.get("/payments/{payment_id}/allocations")
def allocations(payment_id: int, request: Request, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    payment = scope_query(db, user, models.Hakedis).filter_by(id=payment_id).first()
    if not payment:
        raise HTTPException(404, "Hakediş bulunamadı.")
    require_site(user, payment.santiye_id, db)
    rows = db.query(models.PaymentAllocation).filter_by(payment_id=payment_id).all()
    return {"allocations": [{"measurement": serialize_measurement(db, db.get(models.FieldMeasurement, x.measurement_id)),
        "quantity": str(x.quantity), "amount": str(Decimal(x.amount_kurus) / 100)} for x in rows]}


@router.get("/payments/{payment_id}/capabilities")
def payment_capabilities(payment_id: int, request: Request, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    payment = scope_query(db, user, models.Hakedis).filter_by(id=payment_id).first()
    if not payment:
        raise HTTPException(404, "Hakediş bulunamadı.")
    require_site(user, payment.santiye_id, db)
    can_review = False
    try:
        require_site(user, payment.santiye_id, db, "review")
        can_review = payment.hazirlayan_id != user.id
    except HTTPException:
        pass
    link = db.get(models.PaymentContract, payment_id)
    return {"can_review": can_review, "can_submit": payment.hazirlayan_id == user.id,
        "contract_id": link.contract_id if link else None,
        "approval_label": "İç kayıt onayı"}


@router.get("/materials")
def materials(request: Request, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    existing = db.query(models.MalzemeKatalog).filter(
        models.MalzemeKatalog.aktif.is_(True),
        (models.MalzemeKatalog.organization_id.is_(None)) |
        (models.MalzemeKatalog.organization_id == user.organization_id)).all()
    customs = db.query(models.OzelMalzeme).filter_by(organization_id=user.organization_id, aktif=True).all() if user.organization_id else []
    listed = [{"key": x.key, "name": x.ad, "unit": x.varsayilan_birim, "group": x.kategori,
        "source": "catalog", "stock_quantity": None} for x in existing]
    listed += [{"key": f"custom:{x.id}", "name": x.ad, "unit": x.birim, "group": "Özel",
        "source": "custom", "stock_quantity": None} for x in customs]
    keys = {x["key"] for x in listed}
    listed += [{"key": key, "name": name, "unit": unit, "group": group,
        "source": "starter", "stock_quantity": None} for key, name, unit, group in STARTER_MATERIALS if key not in keys]
    return {"materials": listed}


@router.post("/materials")
def create_material(request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    if not user.organization_id:
        raise HTTPException(422, "Özel katalog için organizasyon gerekli.")
    name, unit = str(body.get("name") or "").strip(), str(body.get("unit") or "").strip()
    if not name or not unit:
        raise HTTPException(422, "Malzeme adı ve birimi girin.")
    names = [x["name"].casefold() for x in materials(request, db)["materials"]]
    if name.casefold() in names:
        raise HTTPException(409, "Benzer ad katalogda var; mevcut ürünü kontrol edin.")
    row = models.OzelMalzeme(organization_id=user.organization_id,
        malzeme_key=f"ozel_{uuid.uuid4().hex[:12]}", ad=name, birim=unit, created_by=user.id)
    db.add(row)
    db.commit()
    return {"key": f"custom:{row.id}", "name": row.ad, "unit": row.birim}


def inventory_balance(db, site_id, material_key, variant, unit):
    rows = db.query(models.InventoryMovement).filter(
        models.InventoryMovement.material_key == material_key,
        models.InventoryMovement.variant == variant,
        (models.InventoryMovement.site_id == site_id) |
        (models.InventoryMovement.destination_site_id == site_id)).all()
    if any(x.unit != unit for x in rows):
        raise HTTPException(422, "Bu malzeme/varyant için başka birim kullanılmış; dönüşümü açıkça tanımlayın.")
    balance = Decimal(0)
    for x in rows:
        q = Decimal(x.quantity)
        if x.site_id == site_id:
            balance += q if x.kind in ("receipt", "return", "correction_in") else -q
        if x.destination_site_id == site_id:
            balance += q
    return balance


@router.get("/santiye/{site_id}/inventory")
def inventory(site_id: int, request: Request, db: Session = Depends(database.get_db)):
    user = principal(request, db)
    require_site(user, site_id, db)
    rows = db.query(models.InventoryMovement).filter(
        (models.InventoryMovement.site_id == site_id) |
        (models.InventoryMovement.destination_site_id == site_id)).order_by(models.InventoryMovement.id).all()
    keys = {(x.material_key, x.variant, x.unit) for x in rows}
    balances = [{"material_key": key, "variant": variant, "unit": unit,
        "quantity": str(inventory_balance(db, site_id, key, variant, unit))} for key, variant, unit in sorted(keys)]
    legacy_count = db.query(models.Stok).filter_by(santiye_id=site_id).count()
    return {"balances": balances, "movements": [{"id": x.id, "kind": x.kind,
        "material_key": x.material_key, "variant": x.variant, "unit": x.unit,
        "quantity": str(x.quantity), "site_id": x.site_id,
        "destination_site_id": x.destination_site_id, "work_item_id": x.work_item_id,
        "price": str(Decimal(x.price_kurus)/100) if x.price_kurus is not None else None,
        "price_currency": x.price_currency, "price_source": x.price_source,
        "price_scope": x.price_scope, "created_at": x.created_at.isoformat()} for x in rows],
        "legacy_unreconciled_count": legacy_count}


@router.post("/santiye/{site_id}/inventory/movements")
def add_inventory_movement(site_id: int, request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    user = principal(request, db)
    site = require_site(user, site_id, db, "write")
    key = str(body.get("material_key") or "").strip()
    variant = str(body.get("variant") or "").strip()
    unit = str(body.get("unit") or "").strip()
    kind = body.get("kind")
    request_key = str(body.get("request_key") or "").strip()
    if not key or not unit or not request_key or kind not in ("receipt", "issue", "transfer", "return", "correction_in", "correction_out"):
        raise HTTPException(422, "Malzeme, birim, hareket türü ve tekrar önleme anahtarını girin.")
    catalog = {x["key"]: x for x in materials(request, db)["materials"]}
    if key not in catalog:
        raise HTTPException(422, "Malzeme katalogda bulunamadı.")
    existing = db.query(models.InventoryMovement).filter_by(request_key=request_key).first()
    if existing:
        if (existing.organization_id != user.organization_id or existing.site_id != site_id or
            existing.material_key != key or existing.variant != variant or existing.unit != unit or
            existing.kind != kind or Decimal(existing.quantity) != quantity(body.get("quantity"))):
            raise HTTPException(409, "Tekrar önleme anahtarı başka işleme ait.")
        return {"id": existing.id, "replayed": True}
    qty = quantity(body.get("quantity"))
    if qty <= 0:
        raise HTTPException(422, "Hareket miktarı sıfırdan büyük olmalıdır.")
    dest = body.get("destination_site_id")
    if kind == "transfer":
        if not dest or int(dest) == site_id:
            raise HTTPException(422, "Transfer için farklı hedef proje seçin.")
        target = require_site(user, dest, db, "write")
        if target.organization_id != site.organization_id:
            raise HTTPException(422, "Transfer aynı organizasyonda olmalıdır.")
    elif dest:
        raise HTTPException(422, "Hedef proje yalnız transferde kullanılabilir.")
    work_id = body.get("work_item_id")
    if work_id:
        work = db.get(models.IsKalemi, work_id)
        if not work or work.santiye_id != site_id:
            raise HTTPException(422, "İş kalemi aynı projede olmalıdır.")
    # Acquire a database write lock before reading the ledger. This is a row lock
    # on PostgreSQL and a writer lock on SQLite, including concurrent requests.
    lock_ids = sorted({site_id, int(dest)} if kind == "transfer" else {site_id})
    for lock_id in lock_ids:
        db.query(models.Santiye).filter_by(id=lock_id).update(
            {models.Santiye.updated_at: models.Santiye.updated_at}, synchronize_session=False)
    balance = inventory_balance(db, site_id, key, variant, unit)
    if kind in ("issue", "transfer", "correction_out") and balance < qty:
        raise HTTPException(409, "Stok bakiyesi yetersiz; hareket kaydedilmedi.")
    if kind == "transfer":
        inventory_balance(db, int(dest), key, variant, unit)
    price = body.get("price")
    row = models.InventoryMovement(organization_id=user.organization_id, site_id=site_id,
        destination_site_id=dest, material_key=key, variant=variant, unit=unit, kind=kind,
        quantity=qty, work_item_id=work_id, request_key=request_key,
        price_kurus=kurus(price) if price is not None else None,
        price_currency=body.get("price_currency"), price_source=body.get("price_source"),
        price_scope=body.get("price_scope"), note=body.get("note"), actor_id=user.id)
    if price is not None and (not row.price_currency or not row.price_source):
        raise HTTPException(422, "Fiyat için kaynak ve para birimi girin.")
    try:
        db.add(row)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Eşzamanlı stok işlemi; hareket listesini yenileyin.")
    return {"id": row.id, "replayed": False,
        "balance": str(inventory_balance(db, site_id, key, variant, unit))}
