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
    ihlaller     = Column(Text, default="")   # JSON string
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
    fiyat      = Column(String, nullable=False)  # price as string e.g. "32.50"
    birim      = Column(String, default="")      # 'ton', 'm³', 'adet', 'çuval'
    sehir      = Column(String, default="genel") # 'genel', 'Istanbul', 'Ankara' etc.
    kaynak     = Column(String, default="admin") # 'admin' or 'kullanici'
    giren_id   = Column(Integer, nullable=True)  # user_id who entered
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MalzemeUyari(Base):
    __tablename__ = "malzeme_uyari"
    id         = Column(Integer, primary_key=True, index=True)
    malzeme    = Column(String, nullable=False)
    onceki     = Column(String, nullable=False)  # previous price
    yeni       = Column(String, nullable=False)  # new price
    degisim    = Column(String, nullable=False)  # percentage change e.g. "+8.5"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Stok(Base):
    __tablename__ = "stok"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    malzeme    = Column(String, nullable=False)  # 'demir', 'cimento', 'beton', 'tugla', 'kum', 'diger'
    malzeme_ad = Column(String, default="")      # custom name if 'diger'
    miktar     = Column(String, nullable=False)  # stored as string e.g. "5.5"
    birim      = Column(String, default="")      # 'ton', 'm³', 'adet', 'çuval'
    tip        = Column(String, nullable=False)  # 'giris' | 'cikis'
    tedarikci  = Column(String, default="")
    fiyat      = Column(String, default="")      # unit price
    notlar     = Column(String, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Santiye(Base):
    __tablename__ = "santiyeler"
    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    ad           = Column(String, nullable=False)
    konum        = Column(String, default="")
    lat          = Column(String, default="")
    lon          = Column(String, default="")
    ilerleme     = Column(Integer, default=0)      # 0-100
    isci_sayisi  = Column(Integer, default=0)
    durum        = Column(String, default="iyi")   # 'iyi' | 'dikkat' | 'sorun'
    isg_durumu   = Column(String, default="Normal")
    notlar       = Column(String, default="")
    aktif        = Column(Boolean, default=True)
    created_at   = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.datetime.utcnow)

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
