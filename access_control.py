"""Existing ProjectMember policy shared by API, archive and BIM routes."""
from fastapi import HTTPException
from sqlalchemy import and_, or_
import models

_ROLE_ALIASES = {"santiye_sefi": "santi_sefi", "mutahhit": "muteahhit"}
CANONICAL_ROLES = {"muhendis", "santi_sefi", "muteahhit", "yonetici", "proje_muduru"}
# WRITE_ROLES includes legacy aliases so old DB values continue to work.
WRITE_ROLES = CANONICAL_ROLES | set(_ROLE_ALIASES)
REVIEW_ROLES = WRITE_ROLES - {"muhendis"}


def normalize_role(role: str) -> str:
    """Eski yazım varyantlarını kanonik forma döndürür ('mutahhit' → 'muteahhit')."""
    return _ROLE_ALIASES.get(role, role)


def is_org_owner(user, db):
    return bool(user.organization_id and db.query(models.Organization).filter_by(
        id=user.organization_id, owner_user_id=user.id).first())


def memberships(user, db):
    return db.query(models.ProjectMember).filter_by(
        user_id=user.id, organization_id=user.organization_id, status="active").all()


def allowed_site_ids(user, db):
    query = db.query(models.Santiye).filter(models.Santiye.aktif.is_(True))
    if not user.organization_id:
        return [s.id for s in query.filter_by(user_id=user.id, organization_id=None)]
    query = query.filter_by(organization_id=user.organization_id)
    if not is_org_owner(user, db):
        member_rows = memberships(user, db)
        # A NULL site is an explicit organization-wide membership, never a fallback.
        if not any(m.santiye_id is None for m in member_rows):
            query = query.filter(models.Santiye.id.in_([m.santiye_id for m in member_rows]))
    return [s.id for s in query]


def require_site(user, site_id, db, action="read"):
    site = db.query(models.Santiye).filter_by(id=site_id, aktif=True).first()
    if not site or site.id not in allowed_site_ids(user, db):
        raise HTTPException(404, "Şantiye bulunamadı.")
    if action != "read" and not (is_org_owner(user, db) or
            (site.organization_id is None and site.user_id == user.id)):
        roles = REVIEW_ROLES if action == "review" else WRITE_ROLES
        if not any(m.role in roles and m.santiye_id in (None, site.id) for m in memberships(user, db)):
            raise HTTPException(403, "Bu işlem için şantiye rolünüz yeterli değil.")
    return site


def require_record(user, row, db, action="read"):
    if row is None:
        raise HTTPException(404, "Kayıt bulunamadı.")
    if getattr(row, "organization_id", user.organization_id) != user.organization_id:
        raise HTTPException(404, "Kayıt bulunamadı.")
    site_id = getattr(row, "santiye_id", None)
    if site_id:
        return require_site(user, site_id, db, action)
    owner_id = getattr(row, "user_id", getattr(row, "giren_id", None))
    if owner_id != user.id and not is_org_owner(user, db):
        raise HTTPException(404, "Kayıt bulunamadı.")
    if action == "review" and not is_org_owner(user, db):
        raise HTTPException(403, "İnceleme için yönetici yetkisi gerekli.")
    return row


def require_hierarchy(user, row, db, action="read"):
    if row is None:
        raise HTTPException(404, "Kayıt bulunamadı.")
    if isinstance(row, models.Santiye):
        return require_site(user, row.id, db, action)
    if isinstance(row, models.Kat):
        return require_hierarchy(user, row.bina, db, action)
    if isinstance(row, models.Mahal):
        return require_hierarchy(user, row.kat, db, action)
    site = require_site(user, row.santiye_id, db, action)
    if isinstance(row, models.IsKalemi) and row.mahal_id:
        parent_site = require_hierarchy(user, row.mahal, db, action)
        if parent_site.id != site.id:
            raise HTTPException(409, "İş kalemi ve mahal şantiyeleri uyuşmuyor.")
    return site


def scope_query(db, user, model):
    """Apply scope before sorting/limits; unassigned records stay owner-only."""
    query = db.query(model)
    clauses = []
    if hasattr(model, "organization_id"):
        clauses.append(model.organization_id == user.organization_id)
    if model is models.Santiye:
        clauses.append(model.id.in_(allowed_site_ids(user, db)))
    elif hasattr(model, "santiye_id"):
        site_clause = model.santiye_id.in_(allowed_site_ids(user, db))
        if is_org_owner(user, db):
            unassigned = model.santiye_id.is_(None)
        else:
            owner = getattr(model, "user_id", getattr(model, "giren_id", getattr(model, "kullanici_id", None)))
            if owner is not None:
                unassigned = and_(model.santiye_id.is_(None), owner == user.id)
            elif hasattr(model, "organization_id"):
                # No per-row owner, but already org-scoped above — site-less rows visible to all members.
                unassigned = model.santiye_id.is_(None)
            else:
                unassigned = False
        clauses.append(or_(site_clause, unassigned))
    elif hasattr(model, "user_id") and not is_org_owner(user, db):
        clauses.append(model.user_id == user.id)
    elif user.organization_id is None and hasattr(model, "organization_id") and not hasattr(model, "user_id"):
        clauses.append(False)
    return query.filter(*clauses)
