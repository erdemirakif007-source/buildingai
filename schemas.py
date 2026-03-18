from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

# Kullanıcı Kayıt Şeması
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    plan: Optional[str] = "free"

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