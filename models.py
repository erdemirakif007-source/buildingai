from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime
from datetime import datetime as dt

class User(Base):
    __tablename__ = "users"
    id               = Column(Integer, primary_key=True, index=True)
    email            = Column(String, unique=True, index=True, nullable=False)
    hashed_password  = Column(String, nullable=False)
    full_name        = Column(String, default="")
    plan             = Column(String, default="free")   # "free" | "pro" | "max" | "admin"
    is_admin         = Column(Boolean, default=False, nullable=False)
    created_at       = Column(DateTime, default=datetime.datetime.utcnow)

    reports          = relationship("Report", back_populates="owner")
    kamera_analizler = relationship("KameraAnaliz", back_populates="owner")
    cameras          = relationship("Camera", back_populates="owner")

class Report(Base):
    __tablename__ = "reports"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    tarih      = Column(String)
    content    = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner      = relationship("User", back_populates="reports")

class KameraAnaliz(Base):
    __tablename__ = "kamera_analizler"
    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
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

class MalzemeUyari(Base):
    __tablename__ = "malzeme_uyari"
    id         = Column(Integer, primary_key=True, index=True)
    malzeme    = Column(String, nullable=False)
    onceki     = Column(String, nullable=False)  # TODO(PostgreSQL): Numeric olarak güncellenmeli
    yeni       = Column(String, nullable=False)  # TODO(PostgreSQL): Numeric olarak güncellenmeli
    degisim    = Column(String, nullable=False)  # TODO(PostgreSQL): Numeric veya Float (Yüzdelik değişim için) olmalı
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Stok(Base):
    __tablename__ = "stok"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    santiye_id = Column(Integer, ForeignKey("santiyeler.id"), nullable=True)
    malzeme    = Column(String, nullable=False)  # 'demir', 'cimento', 'beton', 'tugla', 'kum', 'diger'
    malzeme_ad = Column(String, default="")      # custom name if 'diger'
    miktar     = Column(String, nullable=False)  # TODO(PostgreSQL): String yerine Float/Numeric olmalı e.g. 5.5
    birim      = Column(String, default="")      # 'ton', 'm³', 'adet', 'çuval'
    tip        = Column(String, nullable=False)  # 'giris' | 'cikis'
    tedarikci  = Column(String, default="")
    fiyat      = Column(String, default="")      # TODO(PostgreSQL): String yerine Numeric olmalı
    notlar     = Column(String, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Santiye(Base):
    __tablename__ = "santiyeler"
    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    ad           = Column(String, nullable=False)
    konum        = Column(String, default="")
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
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    name       = Column(String, nullable=False)        # e.g. "CAM-01 Ana Giriş"
    url        = Column(String, default="")            # RTSP / HTTP / MJPEG URL
    location   = Column(String, default="")            # Physical location label
    tip        = Column(String, default="ip")          # "ip" | "rtsp" | "usb" | "http"
    aktif      = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner      = relationship("User", back_populates="cameras")

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
