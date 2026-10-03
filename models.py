from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, UniqueConstraint, Float, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base
import datetime
from datetime import datetime as dt

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ProjectMember(Base):
    __tablename__ = "project_members"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    santiye_id = Column(Integer, ForeignKey("santiyeler.id"), nullable=True)
    role = Column(String, nullable=False, default="muhendis")
    status = Column(String, nullable=False, default="active")
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Invitation(Base):
    __tablename__ = "invitations"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False, default="muhendis")
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="pending")
    santiye_ids_json = Column(Text, nullable=True)  # JSON list of int; NULL = org-wide
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class User(Base):
    __tablename__ = "users"
    id               = Column(Integer, primary_key=True, index=True)
    organization_id  = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    email            = Column(String, unique=True, index=True, nullable=False)
    hashed_password  = Column(String, nullable=True)
    full_name        = Column(String, default="")
    telefon          = Column(String, default="")
    role             = Column(String, default="santi_sefi", index=True)
    plan             = Column(String, default="free")   # "free" | "pro" | "max" | "admin"
    is_admin         = Column(Boolean, default=False, nullable=False)
    auth_provider    = Column(String, default="local", nullable=False)
    google_sub       = Column(String, unique=True, nullable=True)
    email_verified   = Column(Boolean, default=False, nullable=False)
    avatar_url       = Column(String, nullable=True, default=None)
    avatar_position  = Column(String, nullable=True, default="50% 50%")
    avatar_scale     = Column(String, nullable=True, default="1")
    created_at       = Column(DateTime, default=datetime.datetime.utcnow)

    reports          = relationship("Report", back_populates="owner")
    kamera_analizler = relationship("KameraAnaliz", back_populates="owner")
    cameras          = relationship("Camera", back_populates="owner")
    archive_records  = relationship("ArchiveRecord", back_populates="owner")
    daily_reports    = relationship("DailyReport", back_populates="owner")

class Report(Base):
    __tablename__ = "reports"
    id         = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    tarih      = Column(String)
    content    = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner      = relationship("User", back_populates="reports")

class KameraAnaliz(Base):
    __tablename__ = "kamera_analizler"
    id           = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    santiye_id   = Column(Integer, ForeignKey("santiyeler.id"), nullable=True, index=True)
    analiz_tipi  = Column(String)   # "guvenlik" | "ilerleme" | "genel"
    sonuc        = Column(Text)
    ihlaller     = Column(Text, default="")   # TODO(PostgreSQL): Text yerine JSONB olarak güncellenmeli
    resim_base64 = Column(Text, default="")
    sehir        = Column(String, default="")
    hava         = Column(String, default="")
    dil          = Column(String, default="tr")
    created_at   = Column(DateTime, default=datetime.datetime.utcnow)

    owner        = relationship("User", back_populates="kamera_analizler")

class Usage(Base):
    __tablename__ = "usage"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tip        = Column(String, nullable=False)  # 'sor', 'kamera', 'sesli_rapor', 'gunluk_rapor'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MalzemeFiyat(Base):
    __tablename__ = "malzeme_fiyat"
    id         = Column(Integer, primary_key=True, index=True)
    malzeme    = Column(String, nullable=False)  # 'demir', 'cimento', 'beton', 'tugla', 'kum'
    fiyat      = Column(String, nullable=False)  # TODO(PostgreSQL): Hesaplamalar için String yerine Numeric/Decimal olmalı
    birim      = Column(String, default="")      # 'ton', 'm³', 'adet', 'çuval'
    sehir      = Column(String, default="genel") # 'genel', 'Istanbul', 'Ankara' etc.
    kaynak     = Column(String, default="admin") # 'admin' or 'kullanici'
    giren_id   = Column(Integer, nullable=True)  # user_id who entered
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class OzelMalzeme(Base):
    __tablename__ = "ozel_malzeme"
    id              = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    malzeme_key     = Column(String, nullable=False)
    ad              = Column(String, nullable=False)
    birim           = Column(String, nullable=False)
    created_by      = Column(Integer, nullable=False)
    created_at      = Column(DateTime, default=datetime.datetime.utcnow)
    aktif           = Column(Boolean, default=True)

class MalzemeKatalog(Base):
    __tablename__ = "malzeme_katalog"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False, unique=True)
    ad = Column(String, nullable=False)
    varsayilan_birim = Column(String, nullable=False)
    kategori = Column(String, default="genel")
    sistem = Column(Boolean, default=True)
    organization_id = Column(Integer, nullable=True)
    aktif = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MalzemeCesit(Base):
    __tablename__ = "malzeme_cesit"
    id = Column(Integer, primary_key=True, index=True)
    katalog_id = Column(Integer, nullable=False, index=True)
    key = Column(String, nullable=False)
    ad = Column(String, nullable=False)
    birim = Column(String, nullable=False)
    min_fiyat = Column(Float, nullable=True)
    max_fiyat = Column(Float, nullable=True)
    sistem = Column(Boolean, default=True)
    organization_id = Column(Integer, nullable=True)
    aktif = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Tedarikci(Base):
    __tablename__ = "tedarikci"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    ad = Column(String, nullable=False)
    yetkili_kisi = Column(String, nullable=True)
    telefon = Column(String, nullable=True)
    email = Column(String, nullable=True)
    sehir = Column(String, nullable=True)
    vergi_no = Column(String, nullable=True)
    adres = Column(String, nullable=True)
    notlar = Column(String, nullable=True)
    aktif = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SatinAlma(Base):
    __tablename__ = "satin_alma"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    santiye_id = Column(Integer, nullable=True)
    tedarikci_id = Column(Integer, nullable=True)
    cesit_id = Column(Integer, nullable=True)
    malzeme_ad = Column(String, nullable=True)
    miktar = Column(Float, nullable=False)
    birim = Column(String, nullable=True)
    birim_fiyat = Column(Float, nullable=False)
    toplam_tutar = Column(Float, nullable=True)
    fatura_no = Column(String, nullable=True)
    durum = Column(String, default="onaylandi")
    giren_id = Column(Integer, nullable=True)
    tarih = Column(DateTime, nullable=True)
    notlar = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DashboardAyar(Base):
    __tablename__ = "dashboard_ayar"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    cesit_id = Column(Integer, nullable=True)
    santiye_id = Column(Integer, nullable=True)
    siralama = Column(Integer, default=0)
    aktif = Column(Boolean, default=True)

class MalzemeUyari(Base):
    __tablename__ = "malzeme_uyari"
    id         = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    malzeme    = Column(String, nullable=False)
    onceki     = Column(String, nullable=False)  # TODO(PostgreSQL): Numeric olarak güncellenmeli
    yeni       = Column(String, nullable=False)  # TODO(PostgreSQL): Numeric olarak güncellenmeli
    degisim    = Column(String, nullable=False)  # TODO(PostgreSQL): Numeric veya Float (Yüzdelik değişim için) olmalı
    santiye_id = Column(Integer, nullable=True)
    status     = Column(String, default="pending", index=True)  # pending | in_review | approved | rejected | correction_requested
    decided_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ReviewDecision(Base):
    __tablename__ = "review_decisions"
    __table_args__ = (
        UniqueConstraint("user_id", "source_type", "source_id", name="uq_review_decisions_user_source"),
    )

    id                = Column(Integer, primary_key=True, index=True)
    organization_id   = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    user_id           = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    source_type       = Column(String, nullable=False, index=True)   # evidence | alert | report
    source_id         = Column(Integer, nullable=False, index=True)
    status            = Column(String, default="pending", index=True)  # pending | in_review | approved | rejected | correction_requested
    decision_note     = Column(Text, default="")
    decided_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    decided_at        = Column(DateTime, nullable=True, index=True)
    created_at        = Column(DateTime, default=dt.utcnow, index=True)
    updated_at        = Column(DateTime, default=dt.utcnow, index=True)
    archived_at       = Column(DateTime, nullable=True)
    archived_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

class Stok(Base):
    __tablename__ = "stok"
    id         = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    santiye_id = Column(Integer, ForeignKey("santiyeler.id"), nullable=True)
    malzeme    = Column(String, nullable=False)  # 'demir', 'cimento', 'beton', 'tugla', 'kum', 'diger'
    malzeme_ad = Column(String, default="")      # custom name if 'diger'
    miktar     = Column(Float, nullable=True)
    birim      = Column(String, default="")      # 'ton', 'm³', 'adet', 'çuval'
    tip        = Column(String, nullable=False)  # 'giris' | 'cikis'
    tedarikci  = Column(String, default="")
    fiyat      = Column(Float, nullable=True)
    notlar     = Column(String, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class StokHareket(Base):
    __tablename__ = "stok_hareketler"
    id              = Column(Integer, primary_key=True)
    malzeme         = Column(String)
    malzeme_ad      = Column(String, nullable=True)
    miktar          = Column(Float)
    fiyat           = Column(Float, nullable=True)
    tip             = Column(String)                  # 'giris' | 'cikis'
    kaynak          = Column(String, nullable=True)   # 'manuel' | 'sarf' | 'ai_asistan'
    kullanici_id    = Column(Integer, ForeignKey("users.id"))
    santiye_id      = Column(Integer, ForeignKey("santiyeler.id"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    notlar          = Column(String, nullable=True)
    created_at      = Column(DateTime, default=datetime.datetime.utcnow)

class StokEsik(Base):
    __tablename__ = "stok_esik"
    id              = Column(Integer, primary_key=True)
    malzeme         = Column(String)
    malzeme_ad      = Column(String, nullable=True)
    min_miktar      = Column(Float, default=0)
    max_miktar      = Column(Float, nullable=True)
    santiye_id      = Column(Integer, ForeignKey("santiyeler.id"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    created_at      = Column(DateTime, default=datetime.datetime.utcnow)

class Santiye(Base):
    __tablename__ = "santiyeler"
    id           = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    ad           = Column(String, nullable=False)
    konum        = Column(String, default="")
    sehir        = Column(String, nullable=True)
    lat          = Column(String, default="")    # TODO(PostgreSQL): String yerine Float veya PostGIS Geometry/Geography
    lon          = Column(String, default="")    # TODO(PostgreSQL): String yerine Float veya PostGIS Geometry/Geography
    ilerleme     = Column(Integer, default=0)      # 0-100
    isci_sayisi  = Column(Integer, default=0)
    durum        = Column(String, default="iyi")   # 'iyi' | 'dikkat' | 'sorun'
    isg_durumu   = Column(String, default="Normal")
    notlar       = Column(String, default="")
    foto         = Column(Text, default=None, nullable=True)
    aktif        = Column(Boolean, default=True)
    created_at   = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.datetime.utcnow)

class Camera(Base):
    __tablename__ = "cameras"
    id         = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    name       = Column(String, nullable=False)        # e.g. "CAM-01 Ana Giriş"
    url        = Column(String, default="")            # RTSP / HTTP / MJPEG URL
    location   = Column(String, default="")            # Physical location label
    tip        = Column(String, default="ip")          # "ip" | "rtsp" | "usb" | "http"
    aktif      = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner      = relationship("User", back_populates="cameras")


class ArchiveRecord(Base):
    __tablename__ = "archive_records"
    id              = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    user_id         = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    santiye_id      = Column(Integer, ForeignKey("santiyeler.id"), nullable=True, index=True)
    camera_id       = Column(Integer, nullable=True, index=True)
    source_type     = Column(String, default="manual", index=True)   # manual | ai | camera | report
    source_ref_type = Column(String, default="")
    source_ref_id   = Column(Integer, nullable=True, index=True)
    media_type      = Column(String, default="photo", index=True)    # photo | video | report
    file_url        = Column(Text, default="")
    thumbnail_url   = Column(Text, default="")
    file_name       = Column(String, default="")
    mime_type       = Column(String, default="")
    file_size       = Column(Integer, default=0)
    title           = Column(String, default="")
    description     = Column(Text, default="")
    event_type      = Column(String, default="", index=True)
    tags            = Column(Text, default="[]")
    zone_label      = Column(String, default="")
    captured_at     = Column(DateTime, nullable=True, index=True)
    duration_seconds = Column(String, default="")
    gps_lat         = Column(String, default="")
    gps_lon         = Column(String, default="")
    exif_payload    = Column(Text, default="")
    ai_suggestions  = Column(Text, default="")
    ai_status       = Column(String, default="none", index=True)  # none | processing | ready | failed
    ai_suggestion_json = Column(Text, default="")
    ai_description  = Column(Text, default="")
    ai_risk_level   = Column(String, default="")
    ai_detected_type = Column(String, default="")
    final_description = Column(Text, default="")
    final_risk_level = Column(String, default="")
    reviewed_by     = Column(Integer, nullable=True, index=True)
    reviewed_at     = Column(DateTime, nullable=True, index=True)
    review_note     = Column(Text, default="")
    status          = Column(String, default="active", index=True)   # active | archived | deleted
    verification_status = Column(String, default="DRAFT", index=True)
    workflow_status = Column(String, default="NEW", index=True)
    deleted_at      = Column(DateTime, nullable=True, index=True)
    uploaded_at     = Column(DateTime, default=dt.utcnow, index=True)
    created_at      = Column(DateTime, default=dt.utcnow, index=True)
    updated_at      = Column(DateTime, default=dt.utcnow)

    owner           = relationship("User", back_populates="archive_records")


class DailyReport(Base):
    __tablename__ = "daily_reports"
    id           = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    santiye_id   = Column(Integer, ForeignKey("santiyeler.id"), nullable=True, index=True)
    report_date  = Column(String, nullable=False, index=True)  # YYYY-MM-DD
    status       = Column(String, default="draft", index=True)
    verification_status = Column(String, default="DRAFT", index=True)
    workflow_status = Column(String, default="NEW", index=True)
    summary      = Column(Text, default="")
    created_at   = Column(DateTime, default=dt.utcnow, index=True)
    updated_at   = Column(DateTime, default=dt.utcnow)

    owner        = relationship("User", back_populates="daily_reports")


class DailyReportItem(Base):
    __tablename__ = "daily_report_items"
    id              = Column(Integer, primary_key=True, index=True)
    daily_report_id = Column(Integer, ForeignKey("daily_reports.id"), nullable=False, index=True)
    archive_record_id = Column(Integer, ForeignKey("archive_records.id"), nullable=True, index=True)
    source_type     = Column(String, default="manual", index=True)   # manual | kamera | rapor
    source_ref_id   = Column(Integer, nullable=True, index=True)
    section_key     = Column(String, nullable=False, index=True)
    section_label   = Column(String, default="")
    note            = Column(Text, default="")
    sort_order      = Column(Integer, default=0)
    created_at      = Column(DateTime, default=dt.utcnow, index=True)
    updated_at      = Column(DateTime, default=dt.utcnow)


class DailyReportSahaKaydi(Base):
    __tablename__ = "daily_report_saha_kayitlari"
    id              = Column(Integer, primary_key=True, index=True)
    report_id       = Column(Integer, ForeignKey("daily_reports.id"), nullable=False, index=True)
    saha_kaydi_id   = Column(Integer, ForeignKey("archive_records.id"), nullable=False, index=True)
    included_at     = Column(DateTime, default=dt.utcnow, index=True)
    snapshot_json   = Column(Text, default="")

class ResetToken(Base):
    __tablename__ = "reset_tokens"
    id         = Column(Integer, primary_key=True)
    email      = Column(String, nullable=False)
    token      = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used       = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.utcnow)

class LoginAttempt(Base):
    __tablename__ = "login_attempts"
    id            = Column(Integer, primary_key=True)
    email         = Column(String, nullable=False, unique=True, index=True)
    attempt_count = Column(Integer, default=0)
    last_attempt  = Column(DateTime, default=dt.utcnow)
    locked_until  = Column(DateTime, nullable=True)


class VideoAnaliz(Base):
    """
    YOLOv11 tabanlı yerel kamera/video analiz sonuçları.
    Hem video upload hem IP kamera stream kayıtları burada tutulur.
    """
    __tablename__ = "video_analizler"
    id              = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    user_id         = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    santiye_id      = Column(Integer, ForeignKey("santiyeler.id"), nullable=True, index=True)
    kaynak_tipi     = Column(String, default="video")   # "video" | "stream" | "foto"
    risk_level      = Column(String, default="DÜŞÜK")   # "YÜKSEK" | "ORTA" | "DÜŞÜK" | "BİLİNMİYOR"
    violations      = Column(Text, default="[]")         # JSON list of violation class names
    ihlal_frekanslari = Column(Text, default="{}")       # JSON dict { sinif: sayi }
    confidence      = Column(String, default="0.0")
    kisi_sayisi     = Column(Integer, default=0)
    ppe_uyum_orani  = Column(String, default="-1")       # -1 = bilinmiyor
    analiz_edilen_kare = Column(Integer, default=1)
    toplam_kare     = Column(Integer, default=1)
    thumbnail       = Column(Text, default="")           # base64 JPEG, max 640px
    tespitler       = Column(Text, default="[]")         # JSON raw YOLO detections (tek kare için)
    created_at      = Column(DateTime, default=dt.utcnow, index=True)


class DecisionMessage(Base):
    __tablename__ = "decision_messages"
    id          = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    decision_id = Column(Integer, ForeignKey("review_decisions.id"), nullable=False, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    message     = Column(Text, nullable=False)
    created_at  = Column(DateTime, default=dt.utcnow, nullable=False, index=True)


# ─────────────────────────────────────────────
# Hiyerarşi Modelleri: Bina → Kat → Mahal → İş Kalemi
# ─────────────────────────────────────────────

class Bina(Base):
    __tablename__ = "binalar"
    id           = Column(Integer, primary_key=True, index=True)
    santiye_id   = Column(Integer, ForeignKey("santiyeler.id", ondelete="CASCADE"), nullable=False, index=True)
    ad           = Column(String, nullable=False)
    bina_tipi    = Column(String, default="konut")  # konut | ticari | sanayi | karma
    toplam_kat   = Column(Integer, nullable=True)
    created_at   = Column(DateTime, default=dt.utcnow)

    santiye      = relationship("Santiye", back_populates="binalar")
    katlar       = relationship("Kat", back_populates="bina", cascade="all, delete-orphan")


class Kat(Base):
    __tablename__ = "katlar"
    id           = Column(Integer, primary_key=True, index=True)
    bina_id      = Column(Integer, ForeignKey("binalar.id", ondelete="CASCADE"), nullable=False, index=True)
    kat_no       = Column(Integer, nullable=False)
    etiket       = Column(String, nullable=True)   # ör: "Zemin Kat", "1. Normal Kat", "Çatı"
    brut_alan_m2 = Column(Float, nullable=True)
    created_at   = Column(DateTime, default=dt.utcnow)

    bina         = relationship("Bina", back_populates="katlar")
    mahaller     = relationship("Mahal", back_populates="kat", cascade="all, delete-orphan")


class Mahal(Base):
    __tablename__ = "mahaller"
    id           = Column(Integer, primary_key=True, index=True)
    kat_id       = Column(Integer, ForeignKey("katlar.id", ondelete="CASCADE"), nullable=False, index=True)
    ad           = Column(String, nullable=False)
    mahal_tipi   = Column(String, nullable=True)  # salon | yatak_odasi | banyo | koridor | merdiven | genel
    alan_m2      = Column(Float, nullable=True)
    created_at   = Column(DateTime, default=dt.utcnow)

    kat          = relationship("Kat", back_populates="mahaller")
    is_kalemleri = relationship("IsKalemi", back_populates="mahal")


class IsKalemi(Base):
    __tablename__ = "is_kalemleri"
    id            = Column(Integer, primary_key=True, index=True)
    mahal_id      = Column(Integer, ForeignKey("mahaller.id", ondelete="SET NULL"), nullable=True, index=True)
    santiye_id    = Column(Integer, ForeignKey("santiyeler.id", ondelete="CASCADE"), nullable=False, index=True)
    katalog_id    = Column(Integer, ForeignKey("csb_is_kalemi_katalog.id"), nullable=True, index=True)
    poz_no        = Column(String, nullable=True)   # Türk metraj poz no, ör: "04.613/2A"
    tanim         = Column(String, nullable=False)
    birim         = Column(String, nullable=False)  # m2, m3, kg, mt, adet, ton vb.
    metraj        = Column(Float, nullable=False, default=0)
    birim_fiyat   = Column(Integer, nullable=False, default=0)   # KURUŞ cinsinden
    toplam_fiyat  = Column(Integer, nullable=False, default=0)   # KURUŞ cinsinden
    durum         = Column(String, default="planli")             # planli | devam_eden | tamamlandi | iptal
    created_at    = Column(DateTime, default=dt.utcnow)
    updated_at    = Column(DateTime, default=dt.utcnow)

    mahal              = relationship("Mahal", back_populates="is_kalemleri")
    katalog            = relationship("CsbIsKalemiKatalog", back_populates="is_kalemleri")
    ilerleme_kayitlari = relationship("IlerlemeKaydi", back_populates="is_kalemi", cascade="all, delete-orphan")
    malzemeler         = relationship("IsKalemiMalzeme", back_populates="is_kalemi", cascade="all, delete-orphan")


class IlerlemeKaydi(Base):
    __tablename__ = "ilerleme_kayitlari"
    id             = Column(Integer, primary_key=True, index=True)
    is_kalemi_id   = Column(Integer, ForeignKey("is_kalemleri.id", ondelete="CASCADE"), nullable=False, index=True)
    raporlayan_id  = Column(Integer, ForeignKey("users.id"), nullable=True)
    yuzde          = Column(Float, nullable=False, default=0)  # 0-100
    tarih          = Column(String, nullable=False)            # DATE olarak TEXT saklanır (ISO 8601)
    notlar         = Column(Text, nullable=True)
    created_at     = Column(DateTime, default=dt.utcnow)

    is_kalemi      = relationship("IsKalemi", back_populates="ilerleme_kayitlari")


class IsKalemiMalzeme(Base):
    """İş kalemi ↔ malzeme_katalog bağlantı tablosu."""
    __tablename__ = "is_kalemi_malzeme"
    __table_args__ = (
        UniqueConstraint("is_kalemi_id", "malzeme_id", name="uq_ik_malzeme"),
    )
    id                 = Column(Integer, primary_key=True, index=True)
    is_kalemi_id       = Column(Integer, ForeignKey("is_kalemleri.id", ondelete="CASCADE"), nullable=False, index=True)
    # Keep the Python/API attribute while matching the already-migrated column.
    malzeme_katalog_id = Column("malzeme_id", Integer, ForeignKey("malzemeler.id"), nullable=False, index=True)
    miktar             = Column(Float, nullable=False, default=1.0)
    birim              = Column(String, nullable=True)
    zorunlu            = Column(Integer, nullable=False, default=0)
    notlar             = Column(Text, nullable=True)
    kaynak             = Column(String, nullable=False, default="manuel")
    created_at         = Column(DateTime, default=dt.utcnow)

    is_kalemi  = relationship("IsKalemi", back_populates="malzemeler")
    malzeme    = relationship("BirlesikMalzeme")


# Santiye modeline binalar relationship'i eklenir (mevcut sınıf tanımı değiştirilmez)
Santiye.binalar = relationship("Bina", back_populates="santiye", cascade="all, delete-orphan")


# ─────────────────────────────────────────────
# BIM Modelleri
# ─────────────────────────────────────────────

class BimModel(Base):
    __tablename__ = "bim_modeller"
    id                    = Column(Integer, primary_key=True, index=True)
    santiye_id            = Column(Integer, ForeignKey("santiyeler.id", ondelete="CASCADE"), nullable=False, index=True)
    blok_id               = Column(Integer, nullable=True)
    dosya_adi             = Column(String, nullable=False)
    orijinal_dosya_adi    = Column(String, nullable=False)
    fragment_dosya_yolu   = Column(String, nullable=True)
    ifc_dosya_yolu        = Column(String, nullable=True)
    dosya_boyutu          = Column(Integer, nullable=True)
    yukleme_tarihi        = Column(DateTime, default=dt.utcnow)
    yukleyen_kullanici_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    durum                 = Column(String, default="aktif")
    metadata_json         = Column(Text, nullable=True)

    santiye       = relationship("Santiye")
    eslestirmeler = relationship("BimElementEslestirme", back_populates="model", cascade="all, delete-orphan")


class BimElementEslestirme(Base):
    __tablename__ = "bim_element_eslestirme"
    __table_args__ = (
        UniqueConstraint("bim_model_id", "ifc_global_id", name="idx_bim_eslestirme_global_id"),
    )
    id                      = Column(Integer, primary_key=True, index=True)
    bim_model_id            = Column(Integer, ForeignKey("bim_modeller.id", ondelete="CASCADE"), nullable=False, index=True)
    ifc_global_id           = Column(String, nullable=False)
    ifc_tip                 = Column(String, nullable=True)
    ifc_kat                 = Column(String, nullable=True)
    is_kalemi_id            = Column(Integer, ForeignKey("is_kalemleri.id"), nullable=True)
    eslestirme_tarihi       = Column(DateTime, default=dt.utcnow)
    eslestiren_kullanici_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    metraj                  = Column(Float, nullable=True)
    metraj_birimi           = Column(String, nullable=True)
    metraj_kaynagi          = Column(String, nullable=True)  # "ifc_quantity" | "manuel"

    model     = relationship("BimModel", back_populates="eslestirmeler")
    is_kalemi = relationship("IsKalemi")


# ─────────────────────────────────────────────
# ÇŞB Birim Fiyat Katalog Modelleri
# ─────────────────────────────────────────────

class CsbIsKalemiKatalog(Base):
    __tablename__ = "csb_is_kalemi_katalog"
    id       = Column(Integer, primary_key=True, index=True)
    poz_no   = Column(String, unique=True, nullable=False, index=True)
    grup     = Column(String, nullable=False)
    alt_grup = Column(String, nullable=True)
    ad       = Column(String, nullable=False)
    birim    = Column(String, nullable=False)
    aciklama = Column(Text, nullable=True)
    aktif    = Column(Integer, default=1)

    malzemeler   = relationship("CsbIsKalemiMalzeme", back_populates="is_kalemi")
    is_kalemleri = relationship("IsKalemi", back_populates="katalog")


class BirlesikMalzeme(Base):
    """Existing migrations/merge_malzeme_v2.py catalog, previously unmapped."""
    __tablename__ = "malzemeler"
    __table_args__ = (UniqueConstraint("kategori", "ad"),)
    id = Column(Integer, primary_key=True)
    kategori = Column(String, nullable=False)
    alt_kategori = Column(String)
    ad = Column(String, nullable=False)
    birim = Column(String, nullable=False)
    scrape_tipi = Column(String, nullable=False)
    aktif = Column(Integer, nullable=False, default=1)
    olusturma_tarihi = Column(String, nullable=False, default=lambda: dt.utcnow().isoformat())
    poz_no = Column(String)
    aciklama = Column(Text)


class CsbIsKalemiMalzeme(Base):
    """CSB iş kalemi kataloğu ↔ birleşik malzemeler tablosu ilişkisi."""
    __tablename__ = "csb_is_kalemi_malzeme"
    __table_args__ = (
        UniqueConstraint("is_kalemi_katalog_id", "malzeme_katalog_id",
                         name="uq_csb_ik_m"),
    )
    id                   = Column(Integer, primary_key=True, index=True)
    is_kalemi_katalog_id = Column(Integer, ForeignKey("csb_is_kalemi_katalog.id"), nullable=False, index=True)
    malzeme_katalog_id   = Column(Integer, ForeignKey("malzemeler.id"), nullable=False, index=True)
    miktar               = Column(Float, nullable=False)
    birim                = Column(String, nullable=False)
    zorunlu              = Column(Integer, default=1)
    aciklama             = Column(Text, nullable=True)

    is_kalemi = relationship("CsbIsKalemiKatalog", back_populates="malzemeler")


# ─────────────────────────────────────────────
# Hakediş Modeli
# ─────────────────────────────────────────────

class Hakedis(Base):
    __tablename__ = "hakedisler"
    __table_args__ = (
        UniqueConstraint("santiye_id", "hakedis_no", name="uq_hakedis_santiye_no"),
    )
    id                = Column(Integer, primary_key=True, index=True)
    organization_id   = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    santiye_id        = Column(Integer, ForeignKey("santiyeler.id", ondelete="CASCADE"), nullable=False, index=True)
    hakedis_no        = Column(Integer, nullable=False)
    donem_baslangic   = Column(String, nullable=False)
    donem_bitis       = Column(String, nullable=False)
    durum             = Column(String, default="taslak", index=True)  # taslak | onay_bekliyor | onaylandi | reddedildi
    hazirlayan_id     = Column(Integer, ForeignKey("users.id"), nullable=True)
    onaylayan_id      = Column(Integer, ForeignKey("users.id"), nullable=True)
    toplam_tutar      = Column(Integer, default=0)       # kuruş cinsinden
    onceki_toplam     = Column(Integer, default=0)       # kuruş — önceki hakedişlerin kümülatif toplamı
    notlar            = Column(Text, nullable=True)
    created_at        = Column(DateTime, default=dt.utcnow)
    updated_at        = Column(DateTime, default=dt.utcnow)

    santiye           = relationship("Santiye")
    kalemler          = relationship("HakedisKalemi", back_populates="hakedis", cascade="all, delete-orphan")


class HakedisKalemi(Base):
    __tablename__ = "hakedis_kalemleri"
    __table_args__ = (
        UniqueConstraint("hakedis_id", "is_kalemi_id", name="uq_hakedis_kalem"),
    )
    id                   = Column(Integer, primary_key=True, index=True)
    hakedis_id           = Column(Integer, ForeignKey("hakedisler.id", ondelete="CASCADE"), nullable=False, index=True)
    is_kalemi_id         = Column(Integer, ForeignKey("is_kalemleri.id", ondelete="CASCADE"), nullable=False, index=True)
    sozlesme_metraj      = Column(Float, default=0)
    onceki_toplam_miktar = Column(Float, default=0)
    bu_donem_miktar      = Column(Float, default=0)
    kumulatif_miktar     = Column(Float, default=0)
    birim_fiyat          = Column(Integer, default=0)     # kuruş — snapshot
    bu_donem_tutar       = Column(Integer, default=0)     # kuruş
    kumulatif_tutar      = Column(Integer, default=0)     # kuruş
    notlar               = Column(Text, nullable=True)

    hakedis              = relationship("Hakedis", back_populates="kalemler")
    is_kalemi            = relationship("IsKalemi")


# Dalga 2 records are additive: older building, progress and payment rows stay intact.
class WorkArea(Base):
    __tablename__ = "work_areas"
    id = Column(Integer, primary_key=True)
    santiye_id = Column(Integer, ForeignKey("santiyeler.id"), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("work_areas.id"), nullable=True)
    name = Column(String, nullable=False)
    kind = Column(String, nullable=False, default="bolge")
    created_at = Column(DateTime, default=dt.utcnow, nullable=False)


class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True)
    santiye_id = Column(Integer, ForeignKey("santiyeler.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    reference = Column(String, nullable=True)
    direction = Column(String, nullable=False)  # employer | subcontractor
    counterparty = Column(String, nullable=False)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    currency = Column(String, nullable=False, default="TRY")
    pricing_type = Column(String, nullable=False, default="unit_price")
    created_at = Column(DateTime, default=dt.utcnow, nullable=False)


class ContractLine(Base):
    __tablename__ = "contract_lines"
    __table_args__ = (UniqueConstraint("contract_id", "work_item_id"),)
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False, index=True)
    work_item_id = Column(Integer, ForeignKey("is_kalemleri.id"), nullable=False, index=True)
    code = Column(String, nullable=False)
    description = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    quantity = Column(Numeric(18, 3), nullable=False)
    unit_price_kurus = Column(Integer, nullable=False)
    revision_of_id = Column(Integer, ForeignKey("contract_lines.id"), nullable=True)


class FieldMeasurement(Base):
    __tablename__ = "field_measurements"
    __table_args__ = (
        UniqueConstraint("santiye_id", "request_key"),
        CheckConstraint("accepted_quantity >= 0 AND allocated_quantity >= 0 AND allocated_quantity <= accepted_quantity"),
    )
    id = Column(Integer, primary_key=True)
    santiye_id = Column(Integer, ForeignKey("santiyeler.id"), nullable=False, index=True)
    area_id = Column(Integer, ForeignKey("work_areas.id"), nullable=True)
    contract_line_id = Column(Integer, ForeignKey("contract_lines.id"), nullable=True, index=True)
    work_item_id = Column(Integer, ForeignKey("is_kalemleri.id"), nullable=True)
    work_date = Column(String, nullable=True)
    reported_quantity = Column(Numeric(18, 3), nullable=True)
    unit = Column(String, nullable=True)
    basis = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="draft")
    accepted_quantity = Column(Numeric(18, 3), nullable=False, default=0)
    allocated_quantity = Column(Numeric(18, 3), nullable=False, default=0)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_reason = Column(Text, nullable=True)
    request_key = Column(String, nullable=True)
    created_at = Column(DateTime, default=dt.utcnow, nullable=False)


class MeasurementEvidence(Base):
    __tablename__ = "measurement_evidence"
    __table_args__ = (UniqueConstraint("measurement_id", "archive_record_id"),)
    id = Column(Integer, primary_key=True)
    measurement_id = Column(Integer, ForeignKey("field_measurements.id"), nullable=False, index=True)
    archive_record_id = Column(Integer, ForeignKey("archive_records.id"), nullable=False)


class MeasurementDecision(Base):
    __tablename__ = "measurement_decisions"
    id = Column(Integer, primary_key=True)
    measurement_id = Column(Integer, ForeignKey("field_measurements.id"), nullable=False, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    previous_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=dt.utcnow, nullable=False)


class PaymentContract(Base):
    __tablename__ = "payment_contracts"
    payment_id = Column(Integer, ForeignKey("hakedisler.id"), primary_key=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False, index=True)


class PaymentAllocation(Base):
    __tablename__ = "payment_allocations"
    __table_args__ = (UniqueConstraint("payment_id", "measurement_id"),)
    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("hakedisler.id"), nullable=False, index=True)
    measurement_id = Column(Integer, ForeignKey("field_measurements.id"), nullable=False, index=True)
    quantity = Column(Numeric(18, 3), nullable=False)
    amount_kurus = Column(Integer, nullable=False)


class PaymentDecision(Base):
    __tablename__ = "payment_decisions"
    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("hakedisler.id"), nullable=False, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    previous_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=dt.utcnow, nullable=False)


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"
    __table_args__ = (
        UniqueConstraint("request_key"),
        CheckConstraint("quantity > 0"),
    )
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    site_id = Column(Integer, ForeignKey("santiyeler.id"), nullable=False, index=True)
    destination_site_id = Column(Integer, ForeignKey("santiyeler.id"), nullable=True)
    material_key = Column(String, nullable=False, index=True)
    variant = Column(String, nullable=False, default="")
    unit = Column(String, nullable=False)
    kind = Column(String, nullable=False)  # receipt | issue | transfer | return | correction_in | correction_out
    quantity = Column(Numeric(18, 3), nullable=False)
    work_item_id = Column(Integer, ForeignKey("is_kalemleri.id"), nullable=True)
    request_key = Column(String, nullable=False)
    price_kurus = Column(Integer, nullable=True)
    price_currency = Column(String, nullable=True)
    price_source = Column(String, nullable=True)
    price_scope = Column(String, nullable=True)
    note = Column(Text, nullable=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=dt.utcnow, nullable=False)
