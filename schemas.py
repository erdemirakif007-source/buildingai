from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List

# Kullanıcı Kayıt Şeması
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    sirket_adi: Optional[str] = None
    telefon: Optional[str] = None

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Şifre en az 8 karakter olmalıdır.')
        if len(v) > 72:
            raise ValueError('Şifre çok uzun.')
        return v

    @field_validator('full_name')
    @classmethod
    def name_valid(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('İsim çok kısa.')
        return v.strip()

# Kullanıcı Bilgi Şeması
class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True

# Giriş Kartı (Token) Şeması
class Token(BaseModel):
    access_token: str
    token_type: str


# ─────────────────────────────────────────────
# Hiyerarşi Şemaları: Bina / Kat / Mahal / İş Kalemi / İlerleme
# birim_fiyat ve toplam_fiyat API'da TL, DB'de kuruş (integer) olarak saklanır.
# ─────────────────────────────────────────────

# ── Bina ──────────────────────────────────────

class BinaCreate(BaseModel):
    ad: str
    bina_tipi: Optional[str] = "konut"  # konut | ticari | sanayi | karma
    toplam_kat: Optional[int] = None


class BinaUpdate(BaseModel):
    ad: Optional[str] = None
    bina_tipi: Optional[str] = None
    toplam_kat: Optional[int] = None


class BinaResponse(BaseModel):
    id: int
    santiye_id: int
    ad: str
    bina_tipi: Optional[str]
    toplam_kat: Optional[int]

    class Config:
        from_attributes = True


# ── Kat ───────────────────────────────────────

class KatCreate(BaseModel):
    kat_no: int
    etiket: Optional[str] = None
    brut_alan_m2: Optional[float] = None


class KatUpdate(BaseModel):
    kat_no: Optional[int] = None
    etiket: Optional[str] = None
    brut_alan_m2: Optional[float] = None


class KatResponse(BaseModel):
    id: int
    bina_id: int
    kat_no: int
    etiket: Optional[str]
    brut_alan_m2: Optional[float]

    class Config:
        from_attributes = True


# ── Mahal ─────────────────────────────────────

class MahalCreate(BaseModel):
    ad: str
    mahal_tipi: Optional[str] = None  # salon | yatak_odasi | banyo | koridor | merdiven | genel
    alan_m2: Optional[float] = None


class MahalUpdate(BaseModel):
    ad: Optional[str] = None
    mahal_tipi: Optional[str] = None
    alan_m2: Optional[float] = None


class MahalResponse(BaseModel):
    id: int
    kat_id: int
    ad: str
    mahal_tipi: Optional[str]
    alan_m2: Optional[float]

    class Config:
        from_attributes = True


# ── İş Kalemi ─────────────────────────────────
# birim_fiyat_tl: API'ya TL gelir, DB'ye kuruş (int) yazılır.
# toplam_fiyat_tl: DB'den kuruş okunur, API'ya TL döndürülür.

class IsKalemiCreate(BaseModel):
    katalog_id: Optional[int] = None  # csb_is_kalemi_katalog.id — verilirse ad/birim/poz_no otomatik dolar
    poz_no: Optional[str] = None
    tanim: Optional[str] = None   # katalog_id varsa zorunlu değil
    birim: Optional[str] = None   # katalog_id varsa zorunlu değil
    metraj: float = 0
    birim_fiyat_tl: float = 0     # API'a TL olarak gönderilir
    durum: Optional[str] = "planli"  # planli | devam_eden | tamamlandi | iptal
    notlar: Optional[str] = None

    @field_validator("birim_fiyat_tl")
    @classmethod
    def fiyat_negatif_olamaz(cls, v):
        if v < 0:
            raise ValueError("Birim fiyat negatif olamaz.")
        return v

    @field_validator("metraj")
    @classmethod
    def metraj_negatif_olamaz(cls, v):
        if v < 0:
            raise ValueError("Metraj negatif olamaz.")
        return v


class IsKalemiUpdate(BaseModel):
    poz_no: Optional[str] = None
    tanim: Optional[str] = None
    birim: Optional[str] = None
    metraj: Optional[float] = None
    birim_fiyat_tl: Optional[float] = None
    durum: Optional[str] = None


class IsKalemiResponse(BaseModel):
    id: int
    santiye_id: int
    mahal_id: Optional[int]
    poz_no: Optional[str]
    tanim: str
    birim: str
    metraj: float
    birim_fiyat_tl: float   # kuruştan TL'ye çevrilmiş
    toplam_fiyat_tl: float  # kuruştan TL'ye çevrilmiş
    durum: str

    class Config:
        from_attributes = True

    @classmethod
    def from_model(cls, m) -> "IsKalemiResponse":
        return cls(
            id=m.id,
            santiye_id=m.santiye_id,
            mahal_id=m.mahal_id,
            poz_no=m.poz_no,
            tanim=m.tanim,
            birim=m.birim,
            metraj=m.metraj,
            birim_fiyat_tl=m.birim_fiyat / 100,
            toplam_fiyat_tl=m.toplam_fiyat / 100,
            durum=m.durum,
        )


# ── İlerleme Kaydı ────────────────────────────

class IlerlemeKaydiCreate(BaseModel):
    yuzde: float
    tarih: str   # ISO 8601 tarih, ör: "2026-05-09"
    notlar: Optional[str] = None

    @field_validator("yuzde")
    @classmethod
    def yuzde_aralik(cls, v):
        if not (0 <= v <= 100):
            raise ValueError("Yüzde 0-100 arasında olmalıdır.")
        return v


class IlerlemeKaydiResponse(BaseModel):
    id: int
    is_kalemi_id: int
    raporlayan_id: Optional[int]
    yuzde: float
    tarih: str
    notlar: Optional[str]

    class Config:
        from_attributes = True


# ── Hiyerarşi Ağacı (iç içe) ─────────────────

class IsKalemiHiyerarsi(BaseModel):
    id: int
    poz_no: Optional[str]
    tanim: str
    birim: str
    metraj: float
    birim_fiyat_tl: float
    toplam_fiyat_tl: float
    durum: str
    son_ilerleme_yuzde: Optional[float]  # en son ilerleme_kaydi.yuzde


class MahalHiyerarsi(BaseModel):
    id: int
    ad: str
    mahal_tipi: Optional[str]
    alan_m2: Optional[float]
    is_kalemleri: List[IsKalemiHiyerarsi]


class KatHiyerarsi(BaseModel):
    id: int
    kat_no: int
    etiket: Optional[str]
    brut_alan_m2: Optional[float]
    mahaller: List[MahalHiyerarsi]


class BinaHiyerarsi(BaseModel):
    id: int
    ad: str
    bina_tipi: Optional[str]
    toplam_kat: Optional[int]
    katlar: List[KatHiyerarsi]


class SantiyeHiyerarsiResponse(BaseModel):
    santiye_id: int
    binalar: List[BinaHiyerarsi]
    # Mahal bağlı olmayan (doğrudan şantiyeye ait) iş kalemleri
    mahalsiz_is_kalemleri: List[IsKalemiHiyerarsi]


# ── Excel Import Yanıtı ───────────────────────

class ExcelImportHata(BaseModel):
    satir: int
    sebep: str


class ExcelImportResponse(BaseModel):
    basarili: int
    hatali: int
    hatalar: List[ExcelImportHata]