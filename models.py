from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id               = Column(Integer, primary_key=True, index=True)
    email            = Column(String, unique=True, index=True, nullable=False)
    hashed_password  = Column(String, nullable=False)
    full_name        = Column(String, default="")
    plan             = Column(String, default="free")   # "free" | "pro" | "admin"
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
