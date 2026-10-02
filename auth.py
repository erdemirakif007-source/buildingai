from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
import os
import hashlib
import hmac
from fastapi import HTTPException

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY .env dosyasında tanımlanmamış!")
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 7

def get_password_hash(password: str) -> str:
    if not isinstance(password, str) or len(password.encode("utf-8")) > 72:
        raise HTTPException(422, "Şifre UTF-8 olarak en fazla 72 bayt olabilir.")
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    if not isinstance(plain, str) or len(plain.encode("utf-8")) > 72:
        return False
    try:
        return pwd_context.verify(plain, hashed)
    except (ValueError, TypeError):
        return False

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token süresi dolmuş. Lütfen tekrar giriş yapın.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Geçersiz token.")


def _credential_stamp(user):
    material = f"{user.id}:{user.hashed_password or ''}:{user.google_sub or ''}"
    return hmac.new(SECRET_KEY.encode(), material.encode(), hashlib.sha256).hexdigest()


def create_user_token(user):
    return create_access_token({"email": user.email, "sub": str(user.id), "credential": _credential_stamp(user)})


def validate_user_token(payload, user):
    if payload.get("sub") != str(user.id) or not hmac.compare_digest(
            str(payload.get("credential", "")), _credential_stamp(user)):
        raise HTTPException(401, "Oturum geçersiz. Lütfen yeniden giriş yapın.")
