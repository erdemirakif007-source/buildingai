from fastapi import FastAPI, Depends, HTTPException, status, Body, Request, UploadFile, File
from fastapi.responses import HTMLResponse, Response, JSONResponse, FileResponse, RedirectResponse
from typing import Optional, List
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from google import genai
from dotenv import load_dotenv
import logging
import datetime
import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import httpx
import pdfplumber
import io

load_dotenv()

GMAIL_ADRES = os.getenv("GMAIL_ADRES")
GMAIL_UYGULAMA_SIFRESI = os.getenv("GMAIL_UYGULAMA_SIFRESI")

# ── Google OAuth2 Config ──────────────────────────────────────
GOOGLE_CLIENT_ID     = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_AUTH_URL      = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL     = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL  = "https://www.googleapis.com/oauth2/v2/userinfo"
PRODUCTION_DOMAIN    = "buildingai.com.tr"

import urllib.parse as _urlparse

LOCALHOST_CALLBACK = "http://127.0.0.1:8000/auth/callback/"

def _get_redirect_uri(request: Request) -> str:
    """
    Ortama göre doğru callback URI döner.
    - buildingai.com.tr  → https://buildingai.com.tr/auth/callback/
    - localhost (her port) → http://127.0.0.1:8000/auth/callback/
    """
    host = request.headers.get("host", "")
    if PRODUCTION_DOMAIN in host:
        return f"https://{PRODUCTION_DOMAIN}/auth/callback/"
    return LOCALHOST_CALLBACK
import models, schemas, auth, database
from models import Santiye, ResetToken, LoginAttempt
from interface import NEW_HTML_TEMPLATE
from admin_panel import ADMIN_HTML
from weather import hava_getir
from pdf_rapor import rapor_olustur
from santiye_beyni import ŞantiyeAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('buildingai.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("buildingai")

models.Base.metadata.create_all(bind=database.engine)

class InMemoryRateLimiter:
    def __init__(self, requests: int, window: int):
        self.requests = requests
        self.window = window
        self.cache: dict[str, list[float]] = {}
        
    def __call__(self, request: Request):
        token = request.headers.get("Authorization") or request.cookies.get("access_token")
        identifier = token if token else (request.client.host if request.client else "127.0.0.1")
        
        import time
        now = time.time()
        if identifier not in self.cache:
            self.cache[identifier] = []
            
        current_window = now - self.window
        self.cache[identifier] = [t for t in self.cache[identifier] if t > current_window]
        
        if len(self.cache[identifier]) >= self.requests:
            raise HTTPException(status_code=429, detail="Çok fazla istek yaptınız. Lütfen bekleyin.")
            
        self.cache[identifier].append(now)

global_rate_limiter = InMemoryRateLimiter(requests=120, window=60)

app = FastAPI(dependencies=[Depends(global_rate_limiter)])
app.mount("/static", StaticFiles(directory="static"), name="static")

import signal, sys
def handle_shutdown(signum, frame):
    print("[BuildingAI] Servis güvenli şekilde kapatılıyor...")
    sys.exit(0)
signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# Rate Limiter (SlowAPI)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://buildingai.tr",
        "https://buildingaipro.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Security Headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Beklenmeyen bir hata oluştu. Lütfen tekrar deneyin."}
    )

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ai_client = genai.Client(api_key=GEMINI_API_KEY)

def _gemini_hata_yakala(e: Exception) -> HTTPException:
    """Google Gemini API hatalarını anlamlı HTTP exception'a çevirir."""
    err = str(e).lower()
    if "429" in err or "resource_exhausted" in err or "quota" in err:
        return HTTPException(status_code=429, detail="Günlük AI kota limitine ulaşıldı. Yarın tekrar deneyin veya Google AI'da ödeme planı ekleyin.")
    if "503" in err or "service unavailable" in err or "overloaded" in err:
        return HTTPException(status_code=503, detail="AI servisi şu an yoğun, lütfen birkaç saniye sonra tekrar deneyin.")
    return HTTPException(status_code=500, detail=f"AI hatası: {str(e)}")

# ── Şantiye Beyin Merkezi ──────────────────────────────────────────────────
santiye_agent = ŞantiyeAgent(ai_client=ai_client)
# In-memory contextual memory: session_id → [{"rol": "user"|"ai", "icerik": str}]
chat_sessions: dict = {}

# --- 📋 PLAN LİMİTLERİ ---
PLAN_LIMITS = {
    "free": {
        "ai_gunluk": 10, "kamera_haftalik": 3,
        "sesli_rapor_gunluk": 1, "gunluk_rapor_gunluk": 1,
        "arsiv_max": 10, "santiye_max": 0,
        "stok": False, "fiyat_takip": False, "deprem_analiz": False,
        "haftalik_rapor": False, "pdf_filigran": True,
    },
    "pro": {
        "ai_gunluk": -1, "kamera_haftalik": 20,
        "sesli_rapor_gunluk": 5, "gunluk_rapor_gunluk": 5,
        "arsiv_max": 100, "santiye_max": 5,
        "stok": True, "fiyat_takip": True, "deprem_analiz": True,
        "haftalik_rapor": False, "pdf_filigran": True,
    },
    "max": {
        "ai_gunluk": -1, "kamera_haftalik": -1,
        "sesli_rapor_gunluk": -1, "gunluk_rapor_gunluk": -1,
        "arsiv_max": -1, "santiye_max": -1,
        "stok": True, "fiyat_takip": True, "deprem_analiz": True,
        "haftalik_rapor": True, "pdf_filigran": False,
    },
    "admin": {
        "ai_gunluk": -1, "kamera_haftalik": -1,
        "sesli_rapor_gunluk": -1, "gunluk_rapor_gunluk": -1,
        "arsiv_max": -1, "santiye_max": -1,
        "stok": True, "fiyat_takip": True, "deprem_analiz": True,
        "haftalik_rapor": True, "pdf_filigran": False,
    },
}

def get_user_plan(user) -> str:
    if user.email == ADMIN_EMAIL:
        return "admin"
    return getattr(user, 'plan', 'free') or 'free'

def get_plan_limit(plan: str, ozellik: str):
    return PLAN_LIMITS.get(plan, PLAN_LIMITS["free"]).get(ozellik)

async def ai_cevap(prompt: str) -> str:
    response = ai_client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=prompt
    )
    return response.text

# reset_tokens ve login_attempts artık DB'de (ResetToken, LoginAttempt tabloları)

def email_gonder(alici: str, konu: str, html_icerik: str) -> bool:
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = konu
        msg['From'] = f"BuildingAI Pro <{GMAIL_ADRES}>"
        msg['To'] = alici
        msg.attach(MIMEText(html_icerik, 'html', 'utf-8'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_ADRES, GMAIL_UYGULAMA_SIFRESI)
            server.sendmail(GMAIL_ADRES, alici, msg.as_string())
        return True
    except Exception as e:
        logger.error(f"Email error: {str(e)}")
        return False

# --- 🛰️ HAVA DURUMU ---
@app.get("/hava")
@limiter.limit("60/minute")
async def get_weather(request: Request, sehir: str = "Sivas"):
    return await hava_getir(sehir)

# ── 🧠 CHAT HUB — Contextual Memory + RAG + Live Data ────────────────────
@app.post("/api/chat")
@limiter.limit("40/minute")
async def chat_hub(request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    soru = (body.get("soru") or "").strip()
    session_id = (body.get("session_id") or "anonymous")[:64]
    token_str = body.get("token", "")

    if not soru:
        raise HTTPException(status_code=400, detail="Soru boş olamaz.")

    # Optional auth — rate limit is stricter for anonymous
    try:
        kullanici = kullanici_dogrula(token_str, db)
        if not kullanim_kontrol(kullanici, db, 'sor', 40, 'gun'):
            raise HTTPException(status_code=429, detail="Günlük Chat Hub limitinize ulaştınız. Pro plana geçin.")
        kullanim_kaydet(kullanici.id, 'sor', db)
    except HTTPException:
        raise
    except Exception:
        kullanici = None  # unauthenticated — still allow (global rate limiter applies)

    # Contextual memory
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    gecmis = chat_sessions[session_id]
    gecmis.append({"rol": "user", "icerik": soru})

    # Generate response via Şantiye Brain
    result = await santiye_agent.generate_response(soru, gecmis, ai_client=ai_client)

    # Store AI reply in memory (keep last 20 turns)
    gecmis.append({"rol": "ai", "icerik": result["cevap"]})
    if len(gecmis) > 20:
        chat_sessions[session_id] = gecmis[-20:]

    logger.info(f"[CHAT HUB] session={session_id} kaynak={result['kaynak']} mesaj={len(gecmis)}")

    return {
        "cevap":        result["cevap"],
        "canli_durum":  result["canli_durum"],
        "kaynak":       result["kaynak"],
        "mesaj_sayisi": len(gecmis),
    }


# --- 🧠 AI ANALİZ ---
@app.post("/sor")
@limiter.limit("60/minute")
async def ask_ai(request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    soru = body.get("soru")
    hava = body.get("hava")
    dil = body.get("dil", "tr")
    token = body.get("token", "")
    konusma_tonu = body.get("konusma_tonu", "saha_arkadasi")
    user = kullanici_dogrula(token, db)
    if not kullanim_kontrol(user, db, 'sor', 10, 'gun'):
        raise HTTPException(status_code=429, detail="Günlük AI soru limitinize (10) ulaştınız. Pro'ya geçerek sınırsız kullanın.")
    kullanim_kaydet(user.id, 'sor', db)

    # Konuşma tonu inject
    TEMEL_KURALLAR = "Markdown kullanma. ** ## --- yasak. Soru anlaşılmıyorsa tahmin yürütme, bir şey sor. Teknik bilgi ver ama bürokratik dil kullanma."
    TON_PROMPTLARI = {
        "saha_arkadasi": "Şantiyede birlikte çalışan, işi bilen kıdemli bir mühendis gibi konuş. Samimi ve doğrudan ol, gereksiz resmiyet yok. Pratik tavsiye ver, olaylar arasında bağlantı kur. Markdown kullanma. Emoji az kullan. Maksimum 5-6 cümle. Bürokratik dil yasak.",
        "hizli_bakis": "Bilgiyi kısa maddeler ve emoji ile ver. Her madde tek satır. Format: emoji + kategori + bilgi. En sona 'Bugün yap:' başlığıyla max 3 aksiyon maddesi ekle. Markdown kullanma, ** ve ## yasak. Listeler 1. 2. 3. formatında.",
        "hikaye_modu": "Rapor sunmak yerine günün fotoğrafını çek. Olayları birbirine bağla, neden-sonuç ilişkisi kur. Sahada konuşur gibi yaz ama akış halinde. Markdown kullanma. Maksimum 5-6 cümle. Bürokratik dil yasak.",
    }
    ton_metni = TON_PROMPTLARI.get(konusma_tonu, TON_PROMPTLARI["saha_arkadasi"])

    if dil == "en":
        system_prompt = f"""You are a senior construction engineer with 30 years of experience.
Current weather conditions at the site: {hava}

TONE: {ton_metni}
RULES: {TEMEL_KURALLAR}

STOCK COMMANDS: If the user gives a stock command (e.g. "add 500kg iron to Sivas site", "deduct 40kg iron from Ankara site"), respond ONLY with this JSON:
{{"stok_komutu": true, "islem": "ekle or cikar", "santiye_adi": "site name", "malzeme": "material name in Turkish (demir/cimento/beton/tugla/kum)", "miktar": number, "birim": "kg/ton/adet/cuval"}}
Otherwise answer normally."""
    else:
        system_prompt = f"""Sen 30 yıllık deneyime sahip kıdemli bir inşaat mühendisisin.
Şantiyenin mevcut hava koşulları: {hava}

KONUŞMA TONU: {ton_metni}
TEMEL KURALLAR: {TEMEL_KURALLAR}

STOK KOMUTU: Kullanıcı stok ile ilgili bir komut verirse (örn: 'Sivas Hafik şantiyesine 500kg demir ekle', 'Ankara şantiyesinden 40kg demir düş', 'şantiyedeki demiri 200kg azalt') SADECE şu JSON ile yanıt ver:
{{"stok_komutu": true, "islem": "ekle veya cikar", "santiye_adi": "şantiye adı", "malzeme": "malzeme adı (demir/cimento/beton/tugla/kum)", "miktar": sayı, "birim": "kg/ton/adet/cuval"}}
Stok komutu değilse normal yanıt ver."""

    try:
        logger.info(f"AI QUERY: type=sor, ton={konusma_tonu}")
        cevap = await ai_cevap(f"{system_prompt}\n\nSoru/Question: {soru}")
        return {"cevap": cevap}
    except Exception as e:
        logger.error(f"API ERROR: {str(e)}")
        return {"cevap": f"Hata: {str(e)}"}

@app.post("/cevir")
@limiter.limit("60/minute")
async def translate_to_english(request: Request, payload: dict = Body(...)):
    metin = payload.get("metin")
    prompt = f"Aşağıdaki inşaat teknik analizini profesyonel IELTS 7.5 seviyesinde İngilizce teknik rapora çevir:\n\n{metin}"
    try:
        cevap = await ai_cevap(prompt)
        return {"cevap": cevap}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Çeviri yapılamadı.")

@app.post("/sor_foto")
@limiter.limit("60/minute")
async def ask_ai_with_photo(request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    soru = body.get("soru")
    resim_base64 = body.get("resim_base64")
    hava = body.get("hava", "Bilinmiyor")
    token = body.get("token", "")
    user = kullanici_dogrula(token, db)
    if not kullanim_kontrol(user, db, 'sor', 10, 'gun'):
        raise HTTPException(status_code=429, detail="Günlük AI soru limitinize (10) ulaştınız. Pro'ya geçerek sınırsız kullanın.")
    kullanim_kaydet(user.id, 'sor', db)
    system_prompt = f"Sen bir inşaat mühendisi asistanısın. Hava: {hava}. Fotoğrafı analiz et ve teknik cevap ver."
    try:
        import base64
        from google.genai import types
        image_bytes = base64.b64decode(resim_base64)
        response = ai_client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                f"{system_prompt}\nSoru: {soru}"
            ]
        )
        return {"cevap": response.text}
    except Exception as e:
        raise _gemini_hata_yakala(e)

# --- 📊 MÜHENDİSLİK HESAPLAMALARI ---
@app.get("/hesapla")
@limiter.limit("60/minute")
async def calculate_engineering(request: Request, tip: str, v1: float, v2: float = 0, v3: float = 0):
    if tip == 'beton':
        hacim = v1 * v2 * v3
        return {"sonuc": f"{hacim:.2f} m³", "detay": f"{v1}x{v2}x{v3} boyutlarındaki beton dökümü."}
    elif tip == 'demir_ag':
        agirlik = (v1 * v1 / 162) * v2
        return {"sonuc": f"{agirlik:.2f} kg", "detay": f"Φ{v1} donatı, {v2}m uzunluk için toplam ağırlık."}
    elif tip == 'as_alan':
        alan = 3.14159 * (v1/2)**2 * v2 / 100
        return {"sonuc": f"{alan:.2f} cm²", "detay": f"{int(v2)} adet Φ{v1} donatının toplam kesit alanı."}
    elif tip == 'etriye':
        boy = 2 * (v1 + v2) + 24 * v3 / 10
        return {"sonuc": f"{boy:.1f} cm", "detay": f"{v1}x{v2} kesit, Φ{v3} etriye - kancalar dahil toplam boy."}
    elif tip == 'tugla':
        adet = v1 * v2 * 50 * 1.05
        return {"sonuc": f"{int(adet)} adet", "detay": f"{v1}x{v2}m duvar için %5 fire payı dahil tuğla adedi."}
    elif tip == 'seramik':
        paket = v1 * 1.10 / 1.44
        return {"sonuc": f"{paket:.1f} paket", "detay": f"{v1}m² alan için %10 fire ile 60x60cm seramik paketi."}
    elif tip == 'boya':
        litre = v1 / 8
        return {"sonuc": f"{litre:.1f} litre", "detay": f"{v1}m² yüzey için 2 kat boya (8m²/lt verimle)."}
    elif tip == 'kubaj':
        hacim = v1 * v2 * v3
        return {"sonuc": f"{hacim:.2f} m³", "detay": f"{v1}x{v2}x{v3}m hafriyat hacmi."}
    elif tip == 'egim':
        egim = (v1 / v2) * 100
        aci = round(__import__('math').degrees(__import__('math').atan(v1/v2)), 1)
        return {"sonuc": f"%{egim:.1f} ({aci}°)", "detay": f"{v1}m yükseklik, {v2}m yatay mesafe için eğim."}
    return {"sonuc": "Hata", "detay": "Hesaplama türü anlaşılamadı."}

# --- 💾 RAPOR SİSTEMİ ---
@app.post("/rapor_kaydet")
@limiter.limit("60/minute")
def save_report(request: Request, payload: dict = Body(...), db: Session = Depends(database.get_db)):
    token = payload.get("token")
    rapor_metni = payload.get("rapor_metni")
    import datetime
    tarih = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    user = kullanici_dogrula(token, db)
    new_report = models.Report(content=rapor_metni, user_id=user.id, tarih=tarih)
    db.add(new_report)
    db.commit()
    return {"mesaj": "Rapor başarıyla arşivlendi."}

@app.get("/rapor_listesi")
@limiter.limit("60/minute")
def list_reports(request: Request, db: Session = Depends(database.get_db)):
    reports = db.query(models.Report).all()
    return {"raporlar": [r.created_at.strftime("%Y-%m-%d %H:%M") for r in reports]}

@app.get("/rapor_getir")
@limiter.limit("60/minute")
def get_report(request: Request, tarih: str, db: Session = Depends(database.get_db)):
    report = db.query(models.Report).first()
    return {"icerik": report.content if report else "Rapor bulunamadı."}

# --- 📄 PDF İNDİR ---
@app.post("/pdf-indir")
@limiter.limit("60/minute")
async def pdf_indir(request: Request, payload: dict = Body(...)):
    kullanici_adi = payload.get("kullanici_adi", "Mühendis")
    sehir = payload.get("sehir", "Sivas")
    hava = payload.get("hava", "")
    analiz = payload.get("analiz", "")
    ingilizce = payload.get("ingilizce", "")
    dil = payload.get("dil", "tr")

    if not analiz:
        raise HTTPException(status_code=400, detail="Analiz metni boş olamaz.")

    pdf_bytes = rapor_olustur(
        kullanici_adi=kullanici_adi,
        sehir=sehir,
        hava_durumu=hava,
        analiz_metni=analiz,
        ingilizce_metni=ingilizce,
        dil=dil
    )

    tarih = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M")
    dosya_adi = f"BuildingAI_Rapor_{tarih}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        
        headers={"Content-Disposition": f"attachment; filename={dosya_adi}"}
    )

# --- 🔐 ÜYELİK SİSTEMİ ---
@app.post("/register", response_model=schemas.UserOut)
@limiter.limit("3/minute")
def register_user(request: Request, user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı!")
    new_user = models.User(
        email=user.email,
        hashed_password=auth.get_password_hash(user.password),
        full_name=user.full_name,
        plan=user.plan if user.plan in ('free', 'pro', 'max') else 'free'
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
@limiter.limit("5/minute")
def login(request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    email = body.get("email")
    password = body.get("password")

    # Hesap kilitli mi kontrol et (DB)
    attempt = db.query(LoginAttempt).filter(LoginAttempt.email == email).first()
    if attempt and attempt.locked_until:
        if datetime.datetime.utcnow() < attempt.locked_until:
            remaining = int((attempt.locked_until - datetime.datetime.utcnow()).total_seconds() / 60) + 1
            raise HTTPException(
                status_code=429,
                detail=f"Çok fazla başarısız giriş denemesi. Hesap {remaining} dakika kilitli."
            )
        else:
            # Kilit süresi doldu, sıfırla
            attempt.attempt_count = 0
            attempt.locked_until = None
            db.commit()

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not auth.verify_password(password[:72], user.hashed_password):
        # Başarısız denemeyi DB'ye kaydet
        if not attempt:
            attempt = LoginAttempt(email=email, attempt_count=0)
            db.add(attempt)
        attempt.attempt_count += 1
        attempt.last_attempt = datetime.datetime.utcnow()
        if attempt.attempt_count >= 5:
            attempt.locked_until = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
            attempt.attempt_count = 0
            db.commit()
            logger.warning(f"ACCOUNT LOCKED: {email}")
            raise HTTPException(status_code=429, detail="5 başarısız deneme. Hesap 15 dakika kilitlendi.")
        db.commit()
        logger.warning(f"LOGIN FAILED: {email}")
        raise HTTPException(status_code=400, detail="E-posta veya şifre hatalı!")

    # Başarılı girişte sayacı temizle
    if attempt:
        attempt.attempt_count = 0
        attempt.locked_until = None
        db.commit()
    logger.info(f"LOGIN SUCCESS: {email}")

    token = auth.create_access_token({"email": user.email})
    return {
        "status": "success",
        "full_name": user.full_name,
        "email": user.email,
        "plan": getattr(user, 'plan', 'free'),
        "token": token
    }

# ════════════════════════════════════════════════════════════════
#  GOOGLE OAUTH2
# ════════════════════════════════════════════════════════════════

@app.get("/auth/google/login")
async def google_login(request: Request):
    """Kullanıcıyı Google'ın OAuth sayfasına yönlendirir."""
    if not GOOGLE_CLIENT_ID or GOOGLE_CLIENT_ID == "YOUR_GOOGLE_CLIENT_ID_HERE":
        raise HTTPException(
            status_code=503,
            detail="Google OAuth henüz yapılandırılmamış. .env dosyasına GOOGLE_CLIENT_ID ve GOOGLE_CLIENT_SECRET ekleyin."
        )
    redirect_uri = _get_redirect_uri(request)
    logger.info(f"[GOOGLE LOGIN] redirect_uri → {redirect_uri}")
    params = {
        "client_id":     GOOGLE_CLIENT_ID,
        "redirect_uri":  redirect_uri,
        "response_type": "code",
        "scope":         "openid email profile",
        "access_type":   "online",
        "prompt":        "select_account",
    }
    url = GOOGLE_AUTH_URL + "?" + _urlparse.urlencode(params)
    return RedirectResponse(url=url)


@app.get("/auth/callback/")
@app.get("/auth/google/callback")
async def google_callback(request: Request, code: Optional[str] = None, error: Optional[str] = None, db: Session = Depends(database.get_db)):
    """
    Google'dan dönen code ile:
      1) Access token al  2) Kullanıcı bilgilerini çek
      3) get_or_create_user → JWT → /app?oauth_token=...
    """
    # Kullanıcı izin vermediyse
    if error or not code:
        return RedirectResponse(url="/app?oauth_error=cancelled")

    redirect_uri = _get_redirect_uri(request)

    # ── Adım 1: Code → Access Token ──────────────────────────
    async with httpx.AsyncClient(timeout=15) as client:
        token_resp = await client.post(GOOGLE_TOKEN_URL, data={
            "code":          code,
            "client_id":     GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri":  redirect_uri,
            "grant_type":    "authorization_code",
        })

    if token_resp.status_code != 200:
        logger.error(f"Google token exchange failed: {token_resp.text}")
        return RedirectResponse(url="/app?oauth_error=token_failed")

    access_token = token_resp.json().get("access_token")

    # ── Adım 2: Kullanıcı Bilgilerini Al ─────────────────────
    async with httpx.AsyncClient(timeout=15) as client:
        info_resp = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )

    if info_resp.status_code != 200:
        return RedirectResponse(url="/app?oauth_error=userinfo_failed")

    g_info    = info_resp.json()
    g_email   = g_info.get("email", "").lower().strip()
    g_name    = g_info.get("name", g_email.split("@")[0])
    g_sub     = g_info.get("id", "")          # Google kullanıcı ID'si

    if not g_email:
        return RedirectResponse(url="/app?oauth_error=no_email")

    # ── Adım 3: Bul veya Oluştur ─────────────────────────────
    user = db.query(models.User).filter(models.User.email == g_email).first()

    if not user:
        # Yeni kullanıcı → otomatik kayıt (ücretsiz plan)
        # Şifre: Google sub ile türetilmiş rastgele hash (girilemez)
        dummy_pw = auth.get_password_hash(f"GOOGLE_OAUTH_{g_sub}_NOLOGIN")
        user = models.User(
            email=g_email,
            hashed_password=dummy_pw,
            full_name=g_name,
            plan="free",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"GOOGLE AUTO-REGISTER: {g_email}")
    else:
        logger.info(f"GOOGLE LOGIN: {g_email}")

    # ── Adım 4: JWT üret ve uygulamaya yönlendir ─────────────
    jwt_token = auth.create_access_token({"email": user.email})
    return RedirectResponse(url=f"/app?oauth_token={jwt_token}")


@app.get("/beni-tanı")
@limiter.limit("60/minute")
def beni_tani(request: Request, token: str, db: Session = Depends(database.get_db)):
    try:
        payload = auth.verify_token(token)
        email = payload.get("email")
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı.")
        return {
            "status": "success",
            "full_name": user.full_name,
            "email": user.email,
            "plan": getattr(user, 'plan', 'free')
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Token geçersiz veya süresi dolmuş.")

# --- 🔑 ŞİFRE SIFIRLAMA ---
@app.post("/sifre-sifirla")
@limiter.limit("5/minute")
def request_password_reset(request: Request, payload: dict = Body(...), db: Session = Depends(database.get_db)):
    email = payload.get("email")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return {"mesaj": "Kod gönderildi."}  # Security: don't reveal if email exists

    kod = str(random.randint(100000, 999999))
    db_token = ResetToken(
        email=email,
        token=kod,
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    )
    db.add(db_token)
    db.commit()

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:500px;margin:0 auto;background:#1a1d21;color:#f0f0f0;padding:30px;border-radius:12px;">
        <h2 style="color:#e67e22;text-align:center;">🏗️ BuildingAI Pro</h2>
        <h3 style="text-align:center;">Şifre Sıfırlama Kodu</h3>
        <p style="color:#a0a0a0;">Merhaba <b style="color:white">{user.full_name}</b>,</p>
        <p style="color:#a0a0a0;">Aşağıdaki 6 haneli kodu kullanarak şifrenizi sıfırlayın:</p>
        <div style="background:#e67e22;color:white;font-size:40px;font-weight:bold;text-align:center;padding:25px;border-radius:10px;letter-spacing:12px;margin:20px 0;">
            {kod}
        </div>
        <p style="color:#a0a0a0;font-size:12px;text-align:center;">Bu kod <b>1 saat</b> geçerlidir.</p>
        <hr style="border-color:#333;margin:20px 0;">
        <p style="color:#555;font-size:11px;text-align:center;">BuildingAI Pro — buildingai.tr</p>
    </div>
    """

    if email_gonder(email, "BuildingAI Pro - Şifre Sıfırlama Kodu", html):
        logger.info(f"RESET CODE SENT: {email}")
        return {"mesaj": "6 haneli kod e-posta adresinize gönderildi."}
    else:
        raise HTTPException(status_code=500, detail="Email gönderilemedi.")

@app.post("/sifre-guncelle")
@limiter.limit("5/minute")
def update_password(request: Request, payload: dict = Body(...), db: Session = Depends(database.get_db)):
    kod = payload.get("token")
    yeni_sifre = payload.get("yeni_sifre")

    db_token = db.query(ResetToken).filter(
        ResetToken.token == kod,
        ResetToken.expires_at > datetime.datetime.utcnow(),
        ResetToken.used == False
    ).first()
    if not db_token:
        raise HTTPException(status_code=400, detail="Geçersiz veya süresi dolmuş kod.")

    if len(yeni_sifre) < 8:
        raise HTTPException(status_code=400, detail="Şifre en az 8 karakter olmalıdır.")

    user = db.query(models.User).filter(models.User.email == db_token.email).first()
    user.hashed_password = auth.get_password_hash(yeni_sifre[:72])
    db_token.used = True
    db.commit()
    logger.info(f"PASSWORD RESET SUCCESS: {db_token.email}")
    return {"mesaj": "Şifreniz güncellendi!"}

@app.get("/", response_class=HTMLResponse)
@limiter.limit("60/minute")
async def root(request: Request):
    token = request.cookies.get("access_token") or request.headers.get("Authorization")
    if token:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/app")
    else:
        return HTMLResponse(Path("landing.html").read_text(encoding="utf-8"))

@app.get("/app", response_class=HTMLResponse)
@limiter.limit("60/minute")
async def main_page(request: Request):
    return NEW_HTML_TEMPLATE

@app.get("/landing", response_class=HTMLResponse)
@limiter.limit("60/minute")
async def landing_redirect(request: Request):
    return Path("landing.html").read_text(encoding="utf-8")

@app.get("/kvkk", response_class=HTMLResponse)
async def kvkk_page():
    return HTMLResponse(Path("kvkk.html").read_text(encoding="utf-8"))

# --- 🎤 SESLİ RAPOR ---
@app.post("/sesli-rapor")
@limiter.limit("10/minute")
async def sesli_rapor(request: Request, payload: dict = Body(...), db: Session = Depends(database.get_db)):
    audio_base64 = payload.get("audio_base64")
    hava = payload.get("hava", "")
    dil = payload.get("dil", "tr")
    token = payload.get("token", "")
    user = kullanici_dogrula(token, db)
    if not kullanim_kontrol(user, db, 'sesli_rapor', 1, 'gun'):
        raise HTTPException(status_code=429, detail="Günlük sesli rapor limitinize (1) ulaştınız. Pro'ya geçerek sınırsız kullanın.")
    kullanim_kaydet(user.id, 'sesli_rapor', db)
    if not audio_base64:
        raise HTTPException(status_code=400, detail="Ses verisi boş.")
    try:
        from google.genai import types as genai_types
        audio_bytes = base64.b64decode(audio_base64)
        transkript_response = ai_client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[
                genai_types.Part.from_bytes(data=audio_bytes, mime_type="audio/webm"),
                "Bu ses kaydını Türkçe metne çevir. Sadece metni yaz, başka hiçbir şey ekleme."
            ]
        )
        transkript = transkript_response.text
        if dil == "tr":
            prompt = f"""Sen 30 yıllık deneyimli bir inşaat mühendisisin. Hava: {hava}

Aşağıdaki saha notunu profesyonel bir günlük şantiye raporuna dönüştür:
"{transkript}"

## 📋 GÜNLÜK RAPOR
Tarih ve genel durum.

## ✅ YAPILAN İŞLER
Bugün tamamlanan işler.

## ⚠️ SORUNLAR VE RİSKLER
Karşılaşılan sorunlar.

## 📅 YARIN YAPILACAKLAR
Önerilen sonraki adımlar."""
        else:
            prompt = f"""You are a senior construction engineer. Weather: {hava}
Convert this site note to a professional daily construction report:
"{transkript}"
Format: ## DAILY REPORT / ## COMPLETED WORK / ## ISSUES & RISKS / ## TOMORROW'S PLAN"""
        rapor = await ai_cevap(prompt)
        logger.info("AI QUERY: type=sesli-rapor")
        return {"rapor": rapor, "transkript": transkript}
    except Exception as e:
        logger.error(f"SESLI RAPOR ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- 📝 GÜNLÜK RAPOR OLUŞTUR ---
@app.post("/gunluk-rapor-olustur")
@limiter.limit("20/minute")
async def gunluk_rapor_olustur(request: Request, payload: dict = Body(...), db: Session = Depends(database.get_db)):
    veriler = payload.get("veriler", "")
    hava = payload.get("hava", "")
    dil = payload.get("dil", "tr")
    token = payload.get("token", "")
    user = kullanici_dogrula(token, db)
    if not kullanim_kontrol(user, db, 'gunluk_rapor', 1, 'gun'):
        raise HTTPException(status_code=429, detail="Günlük rapor limitinize (1) ulaştınız. Pro'ya geçerek sınırsız kullanın.")
    kullanim_kaydet(user.id, 'gunluk_rapor', db)
    if not veriler:
        raise HTTPException(status_code=400, detail="Rapor verisi boş.")
    if dil == "tr":
        prompt = f"""Sen deneyimli bir inşaat mühendisisin. Hava: {hava}

Aşağıdaki şantiye verilerinden profesyonel günlük rapor oluştur:
{veriler}

## 📋 GÜNLÜK RAPOR ÖZETİ
Genel değerlendirme.

## ✅ TAMAMLANAN İŞLER
Bugün yapılanlar.

## 👷 PERSONEL DURUMU
Personel ve devam bilgisi.

## ⚠️ SORUNLAR
Karşılaşılan sorunlar ve riskler.

## 📅 YARIN PLANI
Yarın yapılacaklar."""
    else:
        prompt = f"Create professional daily construction report from: {veriler}. Weather: {hava}"
    rapor = await ai_cevap(prompt)
    logger.info("AI QUERY: type=gunluk-rapor")
    return {"rapor": rapor}

# --- 🔊 SESLİ OKUMA (Edge TTS) ---
@app.post("/sesli-oku")
@limiter.limit("30/minute")
async def sesli_oku(request: Request, payload: dict = Body(...)):
    metin = payload.get("metin", "")[:3000]
    dil = payload.get("dil", "tr")
    if not metin:
        raise HTTPException(status_code=400, detail="Metin boş olamaz.")
    try:
        import edge_tts
        from io import BytesIO
        voice = "tr-TR-AhmetNeural" if dil == "tr" else "en-US-JennyNeural"
        communicate = edge_tts.Communicate(metin, voice)
        audio_buffer = BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        audio_buffer.seek(0)
        audio_base64 = base64.b64encode(audio_buffer.read()).decode()
        return {"audio_base64": audio_base64, "format": "mp3"}
    except Exception as e:
        logger.error(f"TTS ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- 📸 KAMERA ANALİZİ ---
ADMIN_EMAIL = "erdemirakif007@gmail.com"

def kullanici_dogrula(token: str, db: Session):
    try:
        payload = auth.verify_token(token)
        email = payload.get("email")
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı.")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Token geçersiz.")

def kullanim_kontrol(user, db: Session, tip: str, limit: int, periyot: str = "gun") -> bool:
    """Admin, Pro ve Max sınırsız. Returns True if allowed."""
    if get_user_plan(user) in ('admin', 'pro', 'max'):
        return True
    if periyot == "gun":
        baslangic = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    else:  # hafta
        bugun = datetime.datetime.utcnow()
        baslangic = bugun - datetime.timedelta(days=bugun.weekday())
        baslangic = baslangic.replace(hour=0, minute=0, second=0, microsecond=0)
    count = db.query(models.Usage).filter(
        models.Usage.user_id == user.id,
        models.Usage.tip == tip,
        models.Usage.created_at >= baslangic
    ).count()
    return count < limit

def kullanim_kaydet(user_id: int, tip: str, db: Session):
    usage = models.Usage(user_id=user_id, tip=tip)
    db.add(usage)
    db.commit()

import datetime as dt_module


def _compress_resim(resim_base64: str, max_width: int = 1024, quality: int = 60) -> str:
    """Görüntüyü max_width px genişliğe küçültür, %quality JPEG olarak saklar.
    Dönen değer saf base64 (prefix yok); frontend'e gönderilirken
    'data:image/jpeg;base64,' prefixi eklenir.
    """
    try:
        import cv2
        import numpy as np
        # Strip data URI prefix if present
        raw = resim_base64
        if ',' in raw:
            raw = raw.split(',', 1)[1]
        img_bytes = base64.b64decode(raw)
        img_arr = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        if img is None:
            return raw
        h, w = img.shape[:2]
        if w > max_width:
            scale = max_width / w
            img = cv2.resize(img, (max_width, int(h * scale)), interpolation=cv2.INTER_AREA)
        _, buf = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality])
        return base64.b64encode(buf.tobytes()).decode('utf-8')
    except Exception:
        # Fallback: strip prefix only
        return resim_base64.split(',', 1)[-1] if ',' in resim_base64 else resim_base64


@app.post("/kamera-analiz")
@limiter.limit("60/minute")
async def kamera_analiz(request: Request, payload: dict = Body(...), db: Session = Depends(database.get_db)):
    token = payload.get("token")
    resim_base64 = payload.get("resim_base64")
    analiz_tipi = payload.get("analiz_tipi", "genel")  # genel | guvenlik | ilerleme
    hava = payload.get("hava", "")
    sehir = payload.get("sehir", "Sivas")
    dil = payload.get("dil", "tr")

    user = kullanici_dogrula(token, db)
    logger.info(f"AI QUERY: user {user.id}, type: kamera-analiz, tip: {analiz_tipi}")

    if not kullanim_kontrol(user, db, 'kamera', 3, 'hafta'):
        raise HTTPException(status_code=429, detail="Haftalık kamera analizi limitinize (3) ulaştınız. Pro'ya geçerek sınırsız kullanın.")
    kullanim_kaydet(user.id, 'kamera', db)

    # Analiz tipine göre prompt
    if dil == "en":
        if analiz_tipi == "guvenlik":
            prompt_text = f"""You are a construction site safety inspector. Weather: {hava}
Analyze this construction site photo and respond ONLY with the following JSON format, nothing else:
{{
  "guvenlik_skoru": 75,
  "ihlaller": [
    {{"aciklama": "Missing helmet", "x": 0.3, "y": 0.1, "w": 0.1, "h": 0.15}},
    {{"aciklama": "No safety vest", "x": 0.6, "y": 0.2, "w": 0.12, "h": 0.2}}
  ],
  "normalized_boxes": [
    {{"label": "Missing helmet", "box": [0.1, 0.3, 0.25, 0.4], "risk": "high"}},
    {{"label": "No safety vest", "box": [0.2, 0.6, 0.4, 0.72], "risk": "medium"}}
  ],
  "uygun_unsurlar": ["Scaffolding guardrails present", "Warning signs visible"],
  "acil_onlemler": ["Distribute helmets to all workers", "Safety vest is mandatory"],
  "ozet": "2 critical violations detected on site."
}}
CRITICAL — normalized_boxes precision rules:
- Draw a TIGHT rectangle around the hazard object itself, NOT the whole scene.
- Example: for a missing helmet mark only the worker's head area (not full body).
- Box size should be proportional to the actual object. Width/height rarely exceeds 0.20.
- Format: [ymin, xmin, ymax, xmax], values 0.0–1.0.
Only mark violations you actually see — do not fabricate."""
        elif analiz_tipi == "ilerleme":
            prompt_text = f"""You are a construction site progress analyst. Weather: {hava}
Analyze this construction site photo and respond ONLY with the following JSON format:
{{
  "ilerleme_yuzdesi": 65,
  "tamamlanan_isler": ["Foundation complete", "Columns erected"],
  "devam_eden_isler": ["Slab work ongoing"],
  "tahmini_sure": "3-4 weeks",
  "olasi_gecikmeler": ["Weather conditions pose a risk"],
  "normalized_boxes": [
    {{"label": "Incomplete slab area", "box": [0.3, 0.2, 0.7, 0.6], "risk": "medium"}}
  ],
  "ozet": "Construction is 65% complete, overall progress is good."
}}
CRITICAL — normalized_boxes precision rules:
- Draw a TIGHT rectangle only around the specific incomplete/problematic zone, not the whole image.
- Width/height should rarely exceed 0.25. Format: [ymin, xmin, ymax, xmax].
Only mark areas you actually see — do not fabricate."""
        else:
            prompt_text = f"""You are a senior construction engineer. Weather: {hava}
Analyze this construction site photo comprehensively.
## 📋 SITE OVERVIEW
General assessment of the construction site.
## ⚠️ RISKS & ISSUES
Any visible problems or risks.
## 🛡️ RECOMMENDATIONS
Technical recommendations based on TSE standards.
## 📐 TECHNICAL NOTES
Any specific technical observations.
At the end of your response also append this JSON block (start with ```json):
{{"kategoriler": {{"guvenlik": {{"skor": 80, "durum": "iyi", "ozet": "..."}}, "ilerleme": {{"skor": 60, "durum": "orta", "ozet": "..."}}, "malzeme": {{"durum": "normal", "ozet": "..."}}, "risk": {{"seviye": "dusuk", "ozet": "..."}}}}, "normalized_boxes": [{{"label": "Exposed cables", "box": [0.2, 0.1, 0.35, 0.3], "risk": "high"}}, {{"label": "Water pooling", "box": [0.6, 0.5, 0.8, 0.7], "risk": "medium"}}]}}
CRITICAL — normalized_boxes precision rules:
- Mark only the NARROW area where the specific hazard is (e.g., just the cable path, not the wall; just the puddle, not the floor).
- Width/height should rarely exceed 0.20. Format: [ymin, xmin, ymax, xmax].
Only include boxes for risks you actually see — do not fabricate."""
    else:
        if analiz_tipi == "guvenlik":
            prompt_text = f"""Sen bir şantiye iş güvenliği uzmanısın. Hava: {hava}
Bu şantiye fotoğrafını analiz et ve SADECE şu JSON formatında cevap ver, başka hiçbir şey yazma:
{{
  "guvenlik_skoru": 75,
  "ihlaller": [
    {{"aciklama": "Baret eksik", "x": 0.3, "y": 0.1, "w": 0.1, "h": 0.15}},
    {{"aciklama": "Yelek yok", "x": 0.6, "y": 0.2, "w": 0.12, "h": 0.2}}
  ],
  "normalized_boxes": [
    {{"label": "Baret eksik", "box": [0.1, 0.3, 0.25, 0.4], "risk": "yüksek"}},
    {{"label": "Yelek yok", "box": [0.2, 0.6, 0.4, 0.72], "risk": "orta"}}
  ],
  "uygun_unsurlar": ["İskele korkulukları mevcut", "Uyarı levhaları var"],
  "acil_onlemler": ["Tüm işçilere baret dağıtılmalı", "Güvenlik yeleği zorunlu"],
  "ozet": "Sahada 2 kritik ihlal tespit edildi."
}}
KRİTİK — normalized_boxes hassasiyet kuralları:
- İhlalin TAM ÜSTÜNE dar bir kutu çiz, tüm sahneyi değil.
- Örnek: baret eksik işçi için sadece kafa bölgesini işaretle (tüm vücudu değil).
- Kutu genişliği/yüksekliği nadiren 0.20'yi geçmeli.
- Format: [ymin, xmin, ymax, xmax], değerler 0.0–1.0.
Gerçekten gördüğün ihlalleri işaretle, uydurma."""
        elif analiz_tipi == "ilerleme":
            prompt_text = f"""Sen bir şantiye ilerleme analistisin. Hava: {hava}
Bu şantiye fotoğrafını analiz et ve SADECE şu JSON formatında cevap ver:
{{
  "ilerleme_yuzdesi": 65,
  "tamamlanan_isler": ["Temel bitti", "Kolonlar dikildi"],
  "devam_eden_isler": ["Döşeme devam ediyor"],
  "tahmini_sure": "3-4 hafta",
  "olasi_gecikmeler": ["Hava koşulları risk oluşturuyor"],
  "normalized_boxes": [
    {{"label": "Tamamlanmamış döşeme", "box": [0.3, 0.2, 0.7, 0.6], "risk": "orta"}}
  ],
  "ozet": "İnşaat %65 tamamlandı, genel ilerleme iyi."
}}
KRİTİK — normalized_boxes hassasiyet kuralları:
- Sadece eksik/sorunlu bölgenin TAM ÜSTÜNE dar kutu çiz, tüm fotoğrafı değil.
- Kutu genişliği/yüksekliği nadiren 0.25'i geçmeli.
- Format: [ymin, xmin, ymax, xmax].
Gerçekten gördüğün alanları işaretle, uydurma."""
        else:
            prompt_text = f"""Sen kıdemli bir inşaat mühendisisin. Hava: {hava}
Bu şantiye fotoğrafını kapsamlı analiz et.
## 📋 GENEL DURUM
Şantiyenin genel değerlendirmesi.
## ⚠️ RİSKLER VE SORUNLAR
Görünen problemler veya riskler.
## 🛡️ ÖNERİLER
TSE standartlarına göre teknik öneriler.
## 📐 TEKNİK NOTLAR
Özel teknik gözlemler.
Cevabının sonuna şu JSON bloğunu da ekle (```json ile başlat):
{{"kategoriler": {{"guvenlik": {{"skor": 80, "durum": "iyi", "ozet": "..."}}, "ilerleme": {{"skor": 60, "durum": "orta", "ozet": "..."}}, "malzeme": {{"durum": "normal", "ozet": "..."}}, "risk": {{"seviye": "dusuk", "ozet": "..."}}}}, "normalized_boxes": [{{"label": "Açık kablo", "box": [0.2, 0.1, 0.35, 0.3], "risk": "yüksek"}}, {{"label": "Su birikintisi", "box": [0.6, 0.5, 0.8, 0.7], "risk": "orta"}}]}}
KRİTİK — normalized_boxes hassasiyet kuralları:
- Risk nesnesinin TAM ÜSTÜNE dar kutu çiz. Örnek: kablo geçen dar bir alan (duvarın tamamı değil), su birikintisi (zeminin tamamı değil).
- Kutu genişliği/yüksekliği nadiren 0.20'yi geçmeli.
- Format: [ymin, xmin, ymax, xmax].
Sadece gerçekten gördüğün riskleri ekle, uydurma."""

    import asyncio as _asyncio
    import base64 as _b64mod
    import json as _json
    import re as _re
    import time as _time
    from google.genai import types as _types

    # ── YOLO'yu Gemini ile eş zamanlı başlat (thread-pool executor) ──────────
    _yolo_task = _asyncio.ensure_future(
        _ka.frame_analiz_b64(resim_base64, site_id=None, thumbnail=False)
    )

    try:
        image_bytes = _b64mod.b64decode(
            resim_base64.split(',', 1)[-1] if ',' in resim_base64 else resim_base64
        )

        # Gemini retry (503/overloaded → exponential backoff)
        response = None
        for attempt in range(3):
            try:
                response = ai_client.models.generate_content(
                    model="gemini-3.1-flash-lite-preview",
                    contents=[
                        _types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                        prompt_text
                    ]
                )
                break
            except Exception as exc:
                err_str = str(exc).lower()
                if "503" in err_str or "service unavailable" in err_str or "overloaded" in err_str:
                    if attempt < 2:
                        _time.sleep(2 ** attempt)
                        continue
                raise

        if response is None:
            raise HTTPException(status_code=503, detail="AI servisi şu an yoğun, lütfen birkaç saniye sonra tekrar deneyin.")

        sonuc = response.text

        # JSON ayrıştırma
        parsed_data = None
        try:
            parsed_data = _json.loads(sonuc)
        except Exception:
            match = _re.search(r'```json\s*(.*?)\s*```', sonuc, _re.DOTALL)
            if match:
                try:
                    parsed_data = _json.loads(match.group(1))
                except Exception:
                    pass

        # normalized_boxes → gemini_risk_boxes
        gemini_boxes = []
        if isinstance(parsed_data, dict):
            gemini_boxes = parsed_data.get("normalized_boxes") or []

        # ── YOLO sonucunu al (en fazla 20 sn bekle) ──────────────────────────
        yolo_tespitler = []
        yolo_kisi = 0
        try:
            yolo_result = await _asyncio.wait_for(_asyncio.shield(_yolo_task), timeout=20.0)
            if isinstance(yolo_result, dict) and "hata" not in yolo_result:
                yolo_tespitler = yolo_result.get("tespitler", [])
                yolo_kisi     = yolo_result.get("kisi_sayisi", 0)
        except Exception as _ye:
            logger.warning(f"[kamera-analiz] YOLO fusion hatası (devam ediyor): {_ye}")

        # Arşive kaydet (sıkıştırılmış görüntü)
        analiz = models.KameraAnaliz(
            user_id=user.id,
            analiz_tipi=analiz_tipi,
            sonuc=sonuc,
            resim_base64=_compress_resim(resim_base64),  # max 1024px, %60 JPEG
            sehir=sehir,
            hava=hava,
            dil=dil
        )
        db.add(analiz)
        db.commit()

        return {
            # Geriye dönük uyumluluk alanları
            "cevap": sonuc,
            "analiz_metni": sonuc,
            "analiz_id": analiz.id,
            "analiz_tipi": analiz_tipi,
            "parsed": parsed_data,
            "gemini_boxes": gemini_boxes,
            # Yeni unified visual_data paketi
            "visual_data": {
                "yolo_boxes": yolo_tespitler,        # [{class, confidence, bbox:[x1,y1,x2,y2]}]
                "gemini_risk_boxes": gemini_boxes,   # [{label, box:[ymin,xmin,ymax,xmax], risk}]
                "yolo_kisi_sayisi": yolo_kisi,
            },
        }

    except HTTPException:
        if not _yolo_task.done():
            _yolo_task.cancel()
        raise
    except Exception as e:
        if not _yolo_task.done():
            _yolo_task.cancel()
        import traceback
        traceback.print_exc()
        raise _gemini_hata_yakala(e)

# --- 📁 KİŞİSEL ARŞİV ---
@app.get("/arsiv")
@limiter.limit("60/minute")
def arsiv_getir(request: Request, token: str, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    plan = get_user_plan(user)
    arsiv_max = get_plan_limit(plan, "arsiv_max")
    arsiv_limit = 9999 if arsiv_max == -1 else arsiv_max

    raporlar = db.query(models.Report).filter(
        models.Report.user_id == user.id
    ).order_by(models.Report.created_at.desc()).limit(arsiv_limit).all()

    kamera = db.query(models.KameraAnaliz).filter(
        models.KameraAnaliz.user_id == user.id
    ).order_by(models.KameraAnaliz.created_at.desc()).limit(arsiv_limit).all()

    return {
        "raporlar": [{"id": r.id, "tarih": r.tarih, "ozet": r.content[:150] + "...", "created_at": str(r.created_at)} for r in raporlar],
        "kamera_analizler": [{"id": k.id, "tip": k.analiz_tipi, "ozet": k.sonuc[:150] + "...", "sehir": k.sehir, "created_at": str(k.created_at)} for k in kamera]
    }

@app.get("/arsiv/{tip}/{id}")
@limiter.limit("60/minute")
def arsiv_detay(request: Request, tip: str, id: int, token: str, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    if tip == "rapor":
        item = db.query(models.Report).filter(models.Report.id == id, models.Report.user_id == user.id).first()
    else:
        item = db.query(models.KameraAnaliz).filter(models.KameraAnaliz.id == id, models.KameraAnaliz.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı.")
    return item

# --- 🗑️ KANIT SİL ---
@app.delete("/kanit-sil/{id}")
@limiter.limit("60/minute")
def kanit_sil(request: Request, id: int, token: str, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    item = db.query(models.KameraAnaliz).filter(models.KameraAnaliz.id == id, models.KameraAnaliz.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı.")
    db.delete(item)
    db.commit()
    return {"ok": True}

@app.delete("/rapor-sil/{id}")
@limiter.limit("60/minute")
def rapor_sil(request: Request, id: int, token: str, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    item = db.query(models.Report).filter(models.Report.id == id, models.Report.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Rapor bulunamadı.")
    db.delete(item)
    db.commit()
    return {"ok": True}

# --- 📷 KAMERA YÖNETİMİ ---
@app.get("/cameras")
@limiter.limit("60/minute")
def cameras_list(request: Request, token: str, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    cams = db.query(models.Camera).filter(models.Camera.user_id == user.id).order_by(models.Camera.created_at.asc()).all()
    return [{"id": c.id, "name": c.name, "url": c.url, "location": c.location, "tip": c.tip, "aktif": c.aktif, "created_at": str(c.created_at)} for c in cams]

@app.post("/cameras")
@limiter.limit("30/minute")
async def camera_ekle(request: Request, payload: dict = Body(...), db: Session = Depends(database.get_db)):
    token = payload.get("token")
    user = kullanici_dogrula(token, db)
    name = (payload.get("name") or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Kamera adı zorunludur.")
    cam = models.Camera(
        user_id=user.id,
        name=name,
        url=payload.get("url", ""),
        location=payload.get("location", ""),
        tip=payload.get("tip", "ip"),
    )
    db.add(cam)
    db.commit()
    db.refresh(cam)
    return {"id": cam.id, "name": cam.name, "url": cam.url, "location": cam.location, "tip": cam.tip, "aktif": cam.aktif, "created_at": str(cam.created_at)}

@app.delete("/cameras/{cam_id}")
@limiter.limit("30/minute")
def camera_sil(request: Request, cam_id: int, token: str, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    cam = db.query(models.Camera).filter(models.Camera.id == cam_id, models.Camera.user_id == user.id).first()
    if not cam:
        raise HTTPException(status_code=404, detail="Kamera bulunamadı.")
    db.delete(cam)
    db.commit()
    return {"ok": True}

# --- 📊 KULLANIM DURUMU ---
@app.get("/kullanim-durumu")
@limiter.limit("60/minute")
def kullanim_durumu(request: Request, token: str, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    plan = get_user_plan(user)

    bugun = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    bugun_hafta = datetime.datetime.utcnow() - datetime.timedelta(days=datetime.datetime.utcnow().weekday())
    bugun_hafta = bugun_hafta.replace(hour=0, minute=0, second=0, microsecond=0)

    def count(tip, baslangic):
        return db.query(models.Usage).filter(
            models.Usage.user_id == user.id,
            models.Usage.tip == tip,
            models.Usage.created_at >= baslangic
        ).count()

    def lim(ozellik):
        v = get_plan_limit(plan, ozellik)
        return None if v == -1 else v

    return {
        "plan": plan,
        "kullanim": {
            "sor":          {"kullanilan": count('sor', bugun),          "limit": lim("ai_gunluk")},
            "kamera":       {"kullanilan": count('kamera', bugun_hafta), "limit": lim("kamera_haftalik")},
            "sesli_rapor":  {"kullanilan": count('sesli_rapor', bugun),  "limit": lim("sesli_rapor_gunluk")},
            "gunluk_rapor": {"kullanilan": count('gunluk_rapor', bugun), "limit": lim("gunluk_rapor_gunluk")},
        },
        "plan_ozellikleri": {
            "stok":           get_plan_limit(plan, "stok"),
            "fiyat_takip":    get_plan_limit(plan, "fiyat_takip"),
            "deprem_analiz":  get_plan_limit(plan, "deprem_analiz"),
            "haftalik_rapor": get_plan_limit(plan, "haftalik_rapor"),
            "santiye_max":    get_plan_limit(plan, "santiye_max"),
        }
    }

# --- 💰 MALZEME FİYATLARI ---
@app.get("/fiyatlar")
def fiyatlar_getir(sehir: str = "genel", db: Session = Depends(database.get_db)):
    malzemeler = ['demir', 'cimento', 'beton', 'tugla', 'kum']
    sonuc = {}
    uyarilar = []
    for m in malzemeler:
        fiyat = db.query(models.MalzemeFiyat).filter(
            models.MalzemeFiyat.malzeme == m,
            models.MalzemeFiyat.sehir == sehir
        ).order_by(models.MalzemeFiyat.created_at.desc()).first()
        if not fiyat:
            fiyat = db.query(models.MalzemeFiyat).filter(
                models.MalzemeFiyat.malzeme == m,
                models.MalzemeFiyat.sehir == "genel"
            ).order_by(models.MalzemeFiyat.created_at.desc()).first()
        if fiyat:
            sonuc[m] = {"fiyat": fiyat.fiyat, "birim": fiyat.birim, "tarih": str(fiyat.created_at)[:10]}
        else:
            sonuc[m] = {"fiyat": None, "birim": "", "tarih": None}
        uyari = db.query(models.MalzemeUyari).filter(
            models.MalzemeUyari.malzeme == m
        ).order_by(models.MalzemeUyari.created_at.desc()).first()
        if uyari:
            uyarilar.append({"malzeme": m, "degisim": uyari.degisim, "tarih": str(uyari.created_at)[:10]})
    return {"fiyatlar": sonuc, "uyarilar": uyarilar}

@app.get("/fiyat-gecmis/{malzeme}")
def fiyat_gecmis(malzeme: str, gun: int = 30, db: Session = Depends(database.get_db)):
    baslangic = datetime.datetime.utcnow() - datetime.timedelta(days=gun)
    kayitlar = db.query(models.MalzemeFiyat).filter(
        models.MalzemeFiyat.malzeme == malzeme,
        models.MalzemeFiyat.sehir == "genel",
        models.MalzemeFiyat.created_at >= baslangic
    ).order_by(models.MalzemeFiyat.created_at.asc()).all()
    gecmis_temiz = []
    for k in kayitlar:
        try:
            f = float(k.fiyat)
            if malzeme == 'tugla' and f >= 1:
                gecmis_temiz.append({"tarih": str(k.created_at)[:10], "fiyat": k.fiyat})
            elif malzeme != 'tugla' and f >= 100:
                gecmis_temiz.append({"tarih": str(k.created_at)[:10], "fiyat": k.fiyat})
        except:
            continue
    return {"gecmis": gecmis_temiz}

@app.post("/fiyat-gir")
def fiyat_gir(payload: dict = Body(...), db: Session = Depends(database.get_db)):
    token = payload.get("token")
    malzeme = payload.get("malzeme")
    fiyat = payload.get("fiyat")
    birim = payload.get("birim", "")
    sehir = payload.get("sehir", "genel")
    user = kullanici_dogrula(token, db)

    son_fiyat = db.query(models.MalzemeFiyat).filter(
        models.MalzemeFiyat.malzeme == malzeme,
        models.MalzemeFiyat.sehir == sehir
    ).order_by(models.MalzemeFiyat.created_at.desc()).first()

    if son_fiyat and son_fiyat.fiyat:
        try:
            eski = float(son_fiyat.fiyat)
            yeni = float(fiyat)
            degisim = ((yeni - eski) / eski) * 100
            if abs(degisim) >= 5:
                uyari = models.MalzemeUyari(
                    malzeme=malzeme,
                    onceki=str(eski),
                    yeni=str(yeni),
                    degisim=f"{degisim:+.1f}"
                )
                db.add(uyari)
        except Exception:
            pass

    yeni_fiyat = models.MalzemeFiyat(
        malzeme=malzeme,
        fiyat=str(fiyat),
        birim=birim,
        sehir=sehir,
        kaynak="admin" if user.email == ADMIN_EMAIL else "kullanici",
        giren_id=user.id
    )
    db.add(yeni_fiyat)
    db.commit()
    return {"mesaj": f"{malzeme} fiyatı güncellendi."}

# --- 📄 RESMİ FİYAT PDF ÇEKME ---
@app.get("/fiyat-pdf-cek")
async def fiyat_pdf_cek(db: Session = Depends(database.get_db)):
    PDF_URL = "https://webdosya.csb.gov.tr/v2/yfk/2026/03/2026-mart-in-aat-rayi-20260303131227.pdf"

    ARAMA_TERIMLERI = {
        "demir": ["nervürlü çelik", "inşaat demiri", "donatı çeliği", "nervurlu celik"],
        "cimento": ["çimento", "portland çimento", "cimento"],
        "beton": ["hazır beton", "beton c25", "beton c20", "hazir beton"],
        "tugla": ["tuğla", "dolu tuğla", "tugla"],
        "kum": ["kum", "ince kum", "kaba kum", "kum ocak"]
    }

    FALLBACK_URL = "https://webdosya.csb.gov.tr/v2/yfk/2026/03/2026-Mart-n-aat-B-F-20260303131312.pdf"

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(PDF_URL)
            if response.status_code != 200:
                response = await client.get(FALLBACK_URL)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"PDF indirilemedi: {response.status_code}")

        pdf_bytes = io.BytesIO(response.content)
        bulunan = {}

        with pdfplumber.open(pdf_bytes) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if not row:
                            continue
                        row_text = " ".join([str(c).lower() for c in row if c])
                        for malzeme, terimler in ARAMA_TERIMLERI.items():
                            if malzeme in bulunan:
                                continue
                            for terim in terimler:
                                if terim in row_text:
                                    for cell in reversed(row):
                                        if cell:
                                            temiz = str(cell).replace(".", "").replace(",", ".").strip()
                                            try:
                                                fiyat = float(temiz)
                                                if fiyat > 1:
                                                    bulunan[malzeme] = fiyat
                                                    break
                                            except Exception:
                                                continue
                                    if malzeme in bulunan:
                                        break

        birimler = {"demir": "ton", "cimento": "çuval", "beton": "m³", "tugla": "adet", "kum": "ton"}
        kaydedilenler = []
        for malzeme, fiyat in bulunan.items():
            yeni = models.MalzemeFiyat(
                malzeme=malzeme,
                fiyat=str(fiyat),
                birim=birimler.get(malzeme, ""),
                sehir="genel",
                kaynak="pdf_resmi",
                giren_id=None
            )
            db.add(yeni)
            kaydedilenler.append({"malzeme": malzeme, "fiyat": fiyat})

        db.commit()
        return {"mesaj": f"{len(kaydedilenler)} fiyat güncellendi.", "fiyatlar": kaydedilenler}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"PDF parse hatası: {str(e)}")

@app.api_route("/fiyat-ai-guncelle", methods=["GET", "POST"])
async def fiyat_ai_guncelle(db: Session = Depends(database.get_db)):
    try:
        prompt = """Bugünkü Türkiye piyasasında güncel inşaat malzeme fiyatlarını ver.
SADECE bu JSON formatında cevap ver, başka hiçbir şey yazma:
{
  "demir": {"fiyat": 31000, "birim": "ton"},
  "cimento": {"fiyat": 550, "birim": "çuval"},
  "beton": {"fiyat": 5200, "birim": "m³"},
  "tugla": {"fiyat": 9, "birim": "adet"},
  "kum": {"fiyat": 900, "birim": "ton"}
}
Fiyatlar KDV dahil Türkiye ortalaması olmalı. Sadece sayı, birim bilgisi yeterli."""

        response = ai_client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[prompt]
        )

        import json, re
        text = response.text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            raise ValueError("JSON parse edilemedi")
        data = json.loads(match.group())

        birimler = {"demir": "ton", "cimento": "çuval", "beton": "m³", "tugla": "adet", "kum": "ton"}
        kaydedilenler = []

        for malzeme, bilgi in data.items():
            if malzeme not in birimler:
                continue
            fiyat = str(bilgi.get("fiyat", ""))
            if not fiyat:
                continue

            son = db.query(models.MalzemeFiyat).filter(
                models.MalzemeFiyat.malzeme == malzeme,
                models.MalzemeFiyat.sehir == "genel"
            ).order_by(models.MalzemeFiyat.created_at.desc()).first()

            if son and son.fiyat:
                try:
                    eski = float(son.fiyat)
                    yeni = float(fiyat)
                    degisim = ((yeni - eski) / eski) * 100
                    if abs(degisim) >= 5:
                        db.add(models.MalzemeUyari(
                            malzeme=malzeme,
                            onceki=str(eski),
                            yeni=str(yeni),
                            degisim=f"{degisim:+.1f}"
                        ))
                except Exception:
                    pass

            db.add(models.MalzemeFiyat(
                malzeme=malzeme,
                fiyat=fiyat,
                birim=bilgi.get("birim", birimler[malzeme]),
                sehir="genel",
                kaynak="ai_gemini",
                giren_id=None
            ))
            kaydedilenler.append({"malzeme": malzeme, "fiyat": fiyat})

        # Generate 12 months of historical data
        gecmis_prompt = f"""Türkiye'de inşaat malzemelerinin son 12 aylık aylık ortalama fiyat geçmişini ver.
Bugün: {datetime.datetime.utcnow().strftime('%Y-%m')}.
SADECE bu JSON formatında cevap ver, başka hiçbir şey yazma:
{{
  "gecmis": [
    {{"ay": "2025-03", "demir": 24000, "cimento": 180, "beton": 2800, "tugla": 7, "kum": 750}},
    {{"ay": "2025-04", "demir": 25000, "cimento": 185, "beton": 2900, "tugla": 7, "kum": 760}}
  ]
}}
Fiyatlar KDV dahil Türkiye ortalaması, gerçekçi trend göstermeli. 12 ay toplam, en eskiden en yeniye."""

        gecmis_response = ai_client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[gecmis_prompt]
        )

        gecmis_text = gecmis_response.text.strip()
        gecmis_match = re.search(r'\{.*\}', gecmis_text, re.DOTALL)
        if gecmis_match:
            gecmis_data = json.loads(gecmis_match.group())
            malzemeler_list = ['demir', 'cimento', 'beton', 'tugla', 'kum']

            for ay_data in gecmis_data.get("gecmis", []):
                ay = ay_data.get("ay", "")
                if not ay:
                    continue
                try:
                    ay_tarihi = datetime.datetime.strptime(ay + "-01", "%Y-%m-%d")
                except Exception:
                    continue
                for malzeme in malzemeler_list:
                    fiyat = ay_data.get(malzeme)
                    if not fiyat:
                        continue
                    mevcut = db.query(models.MalzemeFiyat).filter(
                        models.MalzemeFiyat.malzeme == malzeme,
                        models.MalzemeFiyat.sehir == "genel",
                        models.MalzemeFiyat.kaynak == "ai_gecmis",
                        models.MalzemeFiyat.created_at >= ay_tarihi,
                        models.MalzemeFiyat.created_at < ay_tarihi + datetime.timedelta(days=32)
                    ).first()
                    if not mevcut:
                        db.add(models.MalzemeFiyat(
                            malzeme=malzeme,
                            fiyat=str(fiyat),
                            birim=birimler[malzeme],
                            sehir="genel",
                            kaynak="ai_gecmis",
                            giren_id=None,
                            created_at=ay_tarihi
                        ))

        db.commit()
        return {"mesaj": f"{len(kaydedilenler)} güncel fiyat + 12 aylık geçmiş AI ile güncellendi.", "fiyatlar": kaydedilenler}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI fiyat güncelleme hatası: {str(e)}")

# --- 📦 STOK YÖNETİMİ ---
@app.get("/stok")
def stok_getir(token: str, santiye_id: int = None, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    plan = get_user_plan(user)
    if not get_plan_limit(plan, "stok"):
        raise HTTPException(status_code=403, detail="PLAN_YETERSIZ:stok:pro")

    malzemeler = ['demir', 'cimento', 'beton', 'tugla', 'kum']
    yedi_gun_once = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    def _stok_hesapla(sid):
        sonuc = {}
        uyarilar = []
        for m in malzemeler:
            q = db.query(models.Stok).filter(models.Stok.user_id == user.id, models.Stok.malzeme == m)
            if sid is not None:
                q = q.filter(models.Stok.santiye_id == (sid if sid != 0 else None))
            girisler = q.filter(models.Stok.tip == 'giris').all()
            cikislar = q.filter(models.Stok.tip == 'cikis').all()
            toplam_giris = sum(float(x.miktar) for x in girisler)
            toplam_cikis = sum(float(x.miktar) for x in cikislar)
            mevcut = toplam_giris - toplam_cikis
            son_cikislar = q.filter(models.Stok.tip == 'cikis', models.Stok.created_at >= yedi_gun_once).all()
            haftalik = sum(float(x.miktar) for x in son_cikislar)
            gunluk = haftalik / 7 if haftalik > 0 else 0
            bitis = round(mevcut / gunluk) if gunluk > 0 else None
            sonuc[m] = {"mevcut": round(mevcut, 2), "toplam_giris": round(toplam_giris, 2),
                        "toplam_cikis": round(toplam_cikis, 2), "gunluk_oran": round(gunluk, 3), "bitis_gun": bitis}
            if bitis and bitis <= 7:
                uyarilar.append({"malzeme": m, "bitis_gun": bitis, "mevcut": round(mevcut, 2)})
        return sonuc, uyarilar

    # Tek şantiye seçiliyse — eski davranış
    if santiye_id:
        s = db.query(models.Santiye).filter(models.Santiye.id == santiye_id).first()
        santiye_adi = s.ad if s else None
        sonuc, uyarilar = _stok_hesapla(santiye_id)
        return {"stok": sonuc, "uyarilar": uyarilar, "santiye_adi": santiye_adi, "gruplar": None}

    # Tüm stoklar — şantiye bazlı grupla
    tum_santiye_idler = db.query(models.Stok.santiye_id).filter(
        models.Stok.user_id == user.id
    ).distinct().all()
    santiye_idler = [row[0] for row in tum_santiye_idler]

    santiye_adi_map = {}
    for sid in santiye_idler:
        if sid is not None:
            s = db.query(models.Santiye).filter(models.Santiye.id == sid).first()
            santiye_adi_map[sid] = s.ad if s else f"Şantiye #{sid}"

    gruplar = []
    tum_uyarilar = []
    for sid in santiye_idler:
        key_id = 0 if sid is None else sid
        sonuc, uyarilar = _stok_hesapla(key_id)
        tum_uyarilar.extend(uyarilar)
        gruplar.append({
            "santiye_id": sid,
            "santiye_adi": santiye_adi_map.get(sid, "Şantiyesiz"),
            "stok": sonuc
        })

    # Eğer hiç stok yoksa boş genel response
    if not gruplar:
        sonuc, uyarilar = _stok_hesapla(None)
        return {"stok": sonuc, "uyarilar": uyarilar, "santiye_adi": None, "gruplar": None}

    return {"stok": gruplar[0]["stok"] if len(gruplar) == 1 else {}, "uyarilar": tum_uyarilar,
            "santiye_adi": None, "gruplar": gruplar}

@app.get("/stok-gecmis/{malzeme}")
def stok_gecmis(malzeme: str, token: str, santiye_id: int = None, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    q = db.query(models.Stok).filter(
        models.Stok.user_id == user.id, models.Stok.malzeme == malzeme
    )
    if santiye_id:
        q = q.filter(models.Stok.santiye_id == santiye_id)
    kayitlar = q.order_by(models.Stok.created_at.desc()).limit(50).all()
    santiye_map = {}
    for k in kayitlar:
        if k.santiye_id and k.santiye_id not in santiye_map:
            s = db.query(models.Santiye).filter(models.Santiye.id == k.santiye_id).first()
            santiye_map[k.santiye_id] = s.ad if s else None
    return {"gecmis": [
        {
            "id": k.id, "tip": k.tip, "miktar": k.miktar,
            "birim": k.birim, "tedarikci": k.tedarikci,
            "fiyat": k.fiyat, "notlar": k.notlar,
            "tarih": str(k.created_at)[:10],
            "santiye_id": k.santiye_id,
            "santiye_adi": santiye_map.get(k.santiye_id) if k.santiye_id else None
        } for k in kayitlar
    ]}

@app.post("/stok-ekle")
def stok_ekle(payload: dict = Body(...), db: Session = Depends(database.get_db)):
    token = payload.get("token")
    user = kullanici_dogrula(token, db)
    plan = get_user_plan(user)
    if not get_plan_limit(plan, "stok"):
        raise HTTPException(status_code=403, detail="PLAN_YETERSIZ:stok:pro")
    kayit = models.Stok(
        user_id=user.id,
        santiye_id=payload.get("santiye_id"),
        malzeme=payload.get("malzeme"),
        malzeme_ad=payload.get("malzeme_ad", ""),
        miktar=str(payload.get("miktar")),
        birim=payload.get("birim", ""),
        tip=payload.get("tip", "giris"),
        tedarikci=payload.get("tedarikci", ""),
        fiyat=str(payload.get("fiyat", "")),
        notlar=payload.get("notlar", "")
    )
    db.add(kayit)
    db.commit()
    return {"mesaj": "Stok kaydedildi.", "id": kayit.id}

@app.delete("/stok-sil/{stok_id}")
def stok_sil(stok_id: int, token: str, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    kayit = db.query(models.Stok).filter(models.Stok.id == stok_id, models.Stok.user_id == user.id).first()
    if not kayit:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı.")
    db.delete(kayit)
    db.commit()
    return {"mesaj": "Silindi."}

# --- 💳 ÖDEME BİLDİRİMİ ---
@app.post("/odeme-bildirimi")
async def odeme_bildirimi(request: Request, payload: dict = Body(...), db: Session = Depends(database.get_db)):
    token = payload.get("token") if isinstance(payload, dict) else payload
    user = kullanici_dogrula(token, db)
    hedef_plan = payload.get("plan", "pro") if isinstance(payload, dict) else "pro"
    ad_soyad   = payload.get("ad_soyad", user.full_name or "") if isinstance(payload, dict) else ""
    telefon    = payload.get("telefon", "") if isinstance(payload, dict) else ""
    aciklama   = payload.get("aciklama", "") if isinstance(payload, dict) else ""

    plan_label = "MAX" if hedef_plan == "max" else "PRO"
    fiyat_label = "1.990 TL" if hedef_plan == "max" else "650 TL"
    terminal_komutu = f'sqlite3 buildingai.db "UPDATE users SET plan=\'{hedef_plan}\' WHERE email=\'{user.email}\';"'

    admin_html = f"""
    <h2>💳 Yeni Ödeme Bildirimi — {plan_label}</h2>
    <p><b>Kullanıcı:</b> {user.full_name} ({user.email})</p>
    <p><b>Hedef Plan:</b> {plan_label} ({fiyat_label}/ay)</p>
    <p><b>Ad Soyad:</b> {ad_soyad}</p>
    <p><b>Telefon:</b> {telefon}</p>
    <p><b>Açıklama:</b> {aciklama}</p>
    <p><b>Tarih:</b> {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
    <hr>
    <p>Ödemeyi onaylamak için aşağıdaki komutu çalıştır:</p>
    <pre style="background:#111;color:#0f0;padding:12px;border-radius:8px;">{terminal_komutu}</pre>
    """

    kullanici_html = f"""
    <h2>✅ Ödeme Bildiriminiz Alındı</h2>
    <p>Merhaba {user.full_name or user.email},</p>
    <p><b>{plan_label}</b> plana geçiş talebiniz alındı. Ödemeniz onaylandıktan sonra hesabınız yükseltilecektir.</p>
    <p>Genellikle 24 saat içinde işleme alınır. Herhangi bir sorunuz için <a href="mailto:{ADMIN_EMAIL}">{ADMIN_EMAIL}</a> adresine yazabilirsiniz.</p>
    <p><b>BuildingAI Pro Ekibi</b></p>
    """

    email_gonder(ADMIN_EMAIL, f"💳 Ödeme Bildirimi [{plan_label}]: {user.email}", admin_html)
    email_gonder(user.email, f"BuildingAI Pro - {plan_label} Ödeme Bildiriminiz Alındı", kullanici_html)

    logger.info(f"PAYMENT NOTIFICATION: {user.email} → {plan_label}")
    return {"mesaj": f"Ödeme bildiriminiz alındı. 24 saat içinde hesabınız {plan_label}'a yükseltilecektir."}

@app.post("/odeme-bildir")
async def odeme_bildir(request: Request, payload: dict = Body(...), db: Session = Depends(database.get_db)):
    return await odeme_bildirimi(request, payload, db)

# --- 🔧 ADMIN PANELİ ---
def admin_kontrol(token: str, db: Session):
    user = kullanici_dogrula(token, db)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Yetkisiz erişim.")
    return user

@app.get("/admin")
def admin_panel_page(request: Request):
    return HTMLResponse(content=ADMIN_HTML)

@app.get("/admin/kullanicilar")
def admin_kullanicilar(token: str, db: Session = Depends(database.get_db)):
    admin_kontrol(token, db)
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "plan": getattr(u, 'plan', 'free'),
            "created_at": str(u.created_at)
        } for u in users
    ]

@app.post("/admin/plan-degistir")
def admin_plan_degistir(payload: dict = Body(...), db: Session = Depends(database.get_db)):
    token = payload.get("token")
    user_id = payload.get("user_id")
    yeni_plan = payload.get("plan")
    admin_kontrol(token, db)
    if yeni_plan not in ('free', 'pro', 'max', 'admin'):
        raise HTTPException(status_code=400, detail="Geçersiz plan. free | pro | max | admin olmalı.")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    user.plan = yeni_plan
    db.commit()
    logger.info(f"ADMIN: {user.email} plani {yeni_plan} yapildi.")
    return {"mesaj": f"{user.email} artik {yeni_plan.upper()} kullanici."}

@app.delete("/admin/kullanici-sil/{user_id}")
def admin_kullanici_sil(user_id: int, token: str, db: Session = Depends(database.get_db)):
    admin_kontrol(token, db)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanici bulunamadi.")
    db.delete(user)
    db.commit()
    return {"mesaj": "Kullanici silindi."}

@app.get("/admin/istatistikler")
def admin_istatistikler(token: str, db: Session = Depends(database.get_db)):
    admin_kontrol(token, db)
    toplam_kullanici = db.query(models.User).count()
    pro_kullanici = db.query(models.User).filter(models.User.plan == 'pro').count()
    toplam_rapor = db.query(models.Report).count()
    toplam_kamera = db.query(models.KameraAnaliz).count()
    yedi_gun = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    yeni_kayit = db.query(models.User).filter(models.User.created_at >= yedi_gun).count()
    return {
        "toplam_kullanici": toplam_kullanici,
        "pro_kullanici": pro_kullanici,
        "free_kullanici": toplam_kullanici - pro_kullanici,
        "toplam_rapor": toplam_rapor,
        "toplam_kamera_analiz": toplam_kamera,
        "yeni_kayit_7gun": yeni_kayit,
        "tahmini_aylik_gelir": pro_kullanici * 10
    }


# --- 🏗️ ŞANTİYE YÖNETİMİ ---
@app.get("/santiyeler")
async def santiyeler_getir(request: Request, db: Session = Depends(database.get_db)):
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "") if auth else request.query_params.get("token", "")
    user = kullanici_dogrula(token, db)
    santiyeler = db.query(Santiye).filter(Santiye.user_id==user.id, Santiye.aktif==True).all()
    return {"santiyeler": [
        {
            "id": s.id, "ad": s.ad, "konum": s.konum,
            "lat": s.lat, "lon": s.lon,
            "ilerleme": s.ilerleme, "isci_sayisi": s.isci_sayisi,
            "durum": s.durum, "isg_durumu": s.isg_durumu,
            "notlar": s.notlar, "foto": s.foto or None,
            "guncelleme": str(s.updated_at)[:16]
        } for s in santiyeler
    ]}

@app.post("/santiye-ekle")
async def santiye_ekle(request: Request, payload: dict = Body(...), db: Session = Depends(database.get_db)):
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "") if auth else payload.get("token", "")
    user = kullanici_dogrula(token, db)
    plan = get_user_plan(user)
    santiye_max = get_plan_limit(plan, "santiye_max")
    if santiye_max == 0:
        raise HTTPException(status_code=403, detail="PLAN_YETERSIZ:santiye:pro")
    if santiye_max != -1:
        mevcut = db.query(Santiye).filter(Santiye.user_id==user.id, Santiye.aktif==True).count()
        if mevcut >= santiye_max:
            raise HTTPException(status_code=403, detail=f"PLAN_YETERSIZ:santiye:max")
    s = Santiye(
        user_id=user.id,
        ad=payload.get("ad", ""),
        konum=payload.get("konum", ""),
        lat=str(payload.get("lat", "")),
        lon=str(payload.get("lon", "")),
        ilerleme=int(payload.get("ilerleme", 0)),
        isci_sayisi=int(payload.get("isci_sayisi", 0)),
        durum=payload.get("durum", "iyi"),
        isg_durumu=payload.get("isg_durumu", "Normal"),
        notlar=payload.get("notlar", ""),
        foto=payload.get("foto", None)
    )
    db.add(s)
    db.commit()
    return {"mesaj": "Şantiye eklendi.", "id": s.id}

@app.post("/santiye-guncelle/{santiye_id}")
async def santiye_guncelle(santiye_id: int, request: Request, payload: dict = Body(...), db: Session = Depends(database.get_db)):
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "") if auth else payload.get("token", "")
    user = kullanici_dogrula(token, db)
    s = db.query(Santiye).filter(Santiye.id==santiye_id, Santiye.user_id==user.id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Şantiye bulunamadı.")
    for alan in ["ad", "konum", "lat", "lon", "notlar", "durum", "isg_durumu", "foto"]:
        if alan in payload:
            setattr(s, alan, payload[alan])
    if "ilerleme" in payload:
        s.ilerleme = int(payload["ilerleme"])
    if "isci_sayisi" in payload:
        s.isci_sayisi = int(payload["isci_sayisi"])
    s.updated_at = datetime.datetime.utcnow()
    db.commit()
    return {"mesaj": "Güncellendi."}

@app.delete("/santiye-sil/{santiye_id}")
async def santiye_sil(santiye_id: int, request: Request, db: Session = Depends(database.get_db)):
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "") if auth else request.query_params.get("token", "")
    user = kullanici_dogrula(token, db)
    s = db.query(Santiye).filter(Santiye.id==santiye_id, Santiye.user_id==user.id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Şantiye bulunamadı.")
    s.aktif = False
    db.commit()
    return {"mesaj": "Silindi."}

@app.post("/santiye-dosya-yukle/{santiye_id}")
async def santiye_dosya_yukle(
    santiye_id: int,
    token: str = "",
    dosyalar: List[UploadFile] = File(...),
    db: Session = Depends(database.get_db)
):
    """
    Şantiyeye özel PDF/Excel/Word dosyalarını data/{santiye_id}/ klasörüne kaydeder.
    santiye_beyni.py'deki read_documents() bu klasörü okuyacak şekilde güncellenir.
    """
    import shutil, os
    kullanici_dogrula(token, db)  # auth kontrolü
    izin = [".pdf", ".xlsx", ".xls", ".doc", ".docx"]
    kayit_klasoru = f"data/{santiye_id}"
    os.makedirs(kayit_klasoru, exist_ok=True)

    kaydedilen = []
    for dosya in dosyalar:
        ext = os.path.splitext(dosya.filename)[1].lower()
        if ext not in izin:
            continue
        hedef = f"{kayit_klasoru}/{dosya.filename}"
        with open(hedef, "wb") as f:
            shutil.copyfileobj(dosya.file, f)
        kaydedilen.append(dosya.filename)

    return {"basari": True, "kaydedilen": kaydedilen, "santiye_id": santiye_id}

# --- 🌍 DEPREM & JEOLOJİK RİSK ---
@app.get("/deprem-son")
async def deprem_son(lat: float = 39.7, lon: float = 37.0, radius: float = 500):
    import httpx
    from datetime import datetime, timedelta
    bitis = datetime.utcnow()
    baslangic = bitis - timedelta(days=30)
    url = (
        f"https://deprem.afad.gov.tr/apiv2/event/filter"
        f"?start={baslangic.strftime('%Y-%m-%dT%H:%M:%S')}"
        f"&end={bitis.strftime('%Y-%m-%dT%H:%M:%S')}"
        f"&lat={lat}&lon={lon}&maxrad={radius}"
        f"&orderby=timedesc&limit=50"
    )
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            res = await client.get(url)
            data = res.json()
        depremler = []
        for d in (data if isinstance(data, list) else []):
            depremler.append({
                "tarih": d.get("date", ""),
                "buyukluk": d.get("magnitude", 0),
                "derinlik": d.get("depth", 0),
                "konum": d.get("location", ""),
                "lat": d.get("latitude", 0),
                "lon": d.get("longitude", 0)
            })
        return {"depremler": depremler, "toplam": len(depremler)}
    except Exception as e:
        return {"depremler": [], "toplam": 0, "hata": str(e)}

@app.post("/deprem-risk-analiz")
async def deprem_risk_analiz(payload: dict = Body(...), db: Session = Depends(database.get_db)):
    token = payload.get("token")
    lat = payload.get("lat", 39.7477)
    lon = payload.get("lon", 37.0179)
    adres = payload.get("adres", "")
    user = kullanici_dogrula(token, db)

    import httpx, math
    from datetime import datetime, timedelta
    bitis = datetime.utcnow()
    baslangic = bitis - timedelta(days=365)
    url = (
        f"https://deprem.afad.gov.tr/apiv2/event/filter"
        f"?start={baslangic.strftime('%Y-%m-%dT%H:%M:%S')}"
        f"&end={bitis.strftime('%Y-%m-%dT%H:%M:%S')}"
        f"&lat={lat}&lon={lon}&maxrad=200"
        f"&orderby=magnitudedesc&limit=100"
    )
    deprem_verisi = []
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            res = await client.get(url)
            afad_data = res.json()
        if isinstance(afad_data, list):
            deprem_verisi = afad_data
    except:
        pass

    deprem_ozet = f"{len(deprem_verisi)} deprem son 1 yılda 200km çevrede tespit edildi."
    if deprem_verisi:
        en_buyuk = max(deprem_verisi, key=lambda x: float(x.get("magnitude", 0)))
        deprem_ozet += f" En büyük: {en_buyuk.get('magnitude')} - {en_buyuk.get('location', '')}"

    prompt = f"""Sen bir deprem mühendisi ve jeoloji uzmanısın.
Şantiye koordinatları: Enlem {lat}, Boylam {lon}
Adres: {adres}
AFAD verisi: {deprem_ozet}

Bu konum için TBDY 2018'e göre kapsamlı deprem risk analizi yap.
SADECE şu JSON formatında cevap ver, başka hiçbir şey yazma:
{{
  "risk_skoru": 65,
  "risk_seviyesi": "Yüksek",
  "zemin_sinifi": "Z3",
  "en_yakin_fay": {{
    "ad": "Kuzey Anadolu Fay Hattı",
    "mesafe_km": 45,
    "tip": "Aktif",
    "son_buyuk_deprem": "1999 - M7.4"
  }},
  "tbdy_parametreler": {{
    "Ss": 1.2,
    "S1": 0.4,
    "PGA": 0.35,
    "deprem_bolgesi": "1. Derece"
  }},
  "tarihsel_depremler": [
    {{"yil": 1999, "buyukluk": 7.4, "merkez": "Gölcük", "hasar": "Çok ağır"}},
    {{"yil": 1944, "buyukluk": 7.3, "merkez": "Bolu", "hasar": "Ağır"}}
  ],
  "oneriler": [
    "TBDY 2018 Bölüm 3 gerekliliklerini uygulayın",
    "Zemin etüdü zorunludur",
    "Güçlendirilmiş temel sistemi önerilir"
  ],
  "ozet": "Bu konum yüksek sismik aktivite bölgesindedir..."
}}
Koordinatlara göre gerçekçi ve doğru bilgi ver."""

    try:
        response = ai_client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[prompt]
        )
        import json, re
        text = response.text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            raise ValueError("JSON parse edilemedi")
        analiz = json.loads(match.group())
        analiz["koordinat"] = {"lat": lat, "lon": lon}
        analiz["adres"] = adres
        analiz["afad_deprem_sayisi"] = len(deprem_verisi)
        analiz["son_depremler"] = [
            {
                "tarih": d.get("date", "")[:10],
                "buyukluk": d.get("magnitude", 0),
                "konum": d.get("location", ""),
                "lat": d.get("latitude", 0),
                "lon": d.get("longitude", 0)
            } for d in deprem_verisi[:10]
        ]
        return analiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analiz hatası: {str(e)}")


@app.post("/haftalik-rapor-olustur")
async def haftalik_rapor_olustur_endpoint(payload: dict = Body(...), db: Session = Depends(database.get_db)):
    token = payload.get("token")
    sehir = payload.get("sehir", "Türkiye")
    user = kullanici_dogrula(token, db)

    import datetime as dt
    yedi_gun_once = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) - dt.timedelta(days=7)

    # ISG kayıtları (son 7 günlük raporlardan)
    raporlar = db.query(models.Report).filter(
        models.Report.user_id == user.id,
        models.Report.created_at >= yedi_gun_once
    ).order_by(models.Report.created_at.desc()).limit(20).all()

    isg_kayitlar = []
    for r in raporlar:
        isg_kayitlar.append({
            "tarih": str(r.created_at)[:10],
            "durum": "Normal",
            "notlar": r.content[:80] if r.content else ""
        })

    # Stok verisi
    malzemeler = ['demir', 'cimento', 'beton', 'tugla', 'kum']
    stok_ozet = {}
    for m in malzemeler:
        girisler = db.query(models.Stok).filter(models.Stok.user_id==user.id, models.Stok.malzeme==m, models.Stok.tip=='giris').all()
        cikislar = db.query(models.Stok).filter(models.Stok.user_id==user.id, models.Stok.malzeme==m, models.Stok.tip=='cikis').all()
        haftalik_giris = sum(float(s.miktar) for s in girisler if s.created_at >= yedi_gun_once)
        haftalik_cikis = sum(float(s.miktar) for s in cikislar if s.created_at >= yedi_gun_once)
        mevcut = sum(float(s.miktar) for s in girisler) - sum(float(s.miktar) for s in cikislar)
        if haftalik_giris > 0 or haftalik_cikis > 0 or mevcut > 0:
            stok_ozet[m] = {
                "mevcut": round(mevcut, 2),
                "haftalik_giris": round(haftalik_giris, 2),
                "haftalik_cikis": round(haftalik_cikis, 2)
            }

    # Kamera analizleri
    kamera_analizler = db.query(models.KameraAnaliz).filter(
        models.KameraAnaliz.user_id == user.id,
        models.KameraAnaliz.created_at >= yedi_gun_once
    ).order_by(models.KameraAnaliz.created_at.desc()).limit(5).all()

    foto_analizler = [{
        "tarih": str(k.created_at)[:10],
        "tip": k.analiz_tipi,
        "ozet": k.sonuc[:200] if k.sonuc else ""
    } for k in kamera_analizler]

    # AI yorumu
    rapor_icerigi = f"""
Kullanıcı: {user.full_name or user.email}
Şehir: {sehir}
Son 7 günde {len(raporlar)} günlük rapor girildi.
Stok durumu: {', '.join([f'{m}: {v["mevcut"]}' for m,v in stok_ozet.items()]) or 'Veri yok'}
Kamera analizi sayısı: {len(kamera_analizler)}
"""
    ai_prompt = f"""Sen bir inşaat proje yönetimi uzmanısın.
Aşağıdaki haftalık şantiye verilerini analiz et ve profesyonel bir haftalık değerlendirme yaz.
{rapor_icerigi}
Türkçe, 3-4 paragraf, somut öneriler içeren, gerçekçi bir değerlendirme yaz.
Sadece değerlendirme metnini yaz, başka hiçbir şey ekleme."""

    try:
        ai_response = ai_client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=[ai_prompt]
        )
        ai_yorum = ai_response.text
    except:
        ai_yorum = "Bu hafta şantiye verileri derlendi. Detaylar aşağıda yer almaktadır."

    hafta_verisi = {
        "ai_yorum": ai_yorum,
        "isg_kayitlar": isg_kayitlar,
        "stok": stok_ozet,
        "foto_analizler": foto_analizler
    }

    from pdf_rapor import haftalik_rapor_olustur
    pdf_bytes = haftalik_rapor_olustur(
        kullanici_adi=user.full_name or user.email,
        sehir=sehir,
        hafta_verisi=hafta_verisi
    )

    from fastapi.responses import Response
    tarih_str = dt.datetime.now().strftime("%Y%m%d")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=BuildingAI_Haftalik_{tarih_str}.pdf"}
    )

@app.get("/health")
async def health_check(db: Session = Depends(database.get_db)):
    from sqlalchemy import text
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {"status": "ok", "db": db_status, "version": "1.0.0"}


# ════════════════════════════════════════════════════════════════════════════
# 🤖  YOLO — YEREL KAMERA & VİDEO ANALİZ SİSTEMİ
# ════════════════════════════════════════════════════════════════════════════
# Tamamen local — harici AI API kullanılmaz.
# Desteklenen: video upload (FFmpeg keyframe), IP kamera frame (base64).
# ════════════════════════════════════════════════════════════════════════════

import json
import tempfile
import kamera_analiz as _ka


def _yolo_db_kaydet(
    user_id: int,
    sonuc: dict,
    kaynak_tipi: str,
    santiye_id: Optional[int],
    db: Session,
) -> models.VideoAnaliz:
    """Analiz sonucunu VideoAnaliz tablosuna yaz."""
    kayit = models.VideoAnaliz(
        user_id            = user_id,
        santiye_id         = santiye_id,
        kaynak_tipi        = kaynak_tipi,
        risk_level         = sonuc.get("risk_level", "BİLİNMİYOR"),
        violations         = json.dumps(sonuc.get("violations", []), ensure_ascii=False),
        ihlal_frekanslari  = json.dumps(sonuc.get("ihlal_frekanslari", {}), ensure_ascii=False),
        confidence         = str(sonuc.get("confidence", 0.0)),
        kisi_sayisi        = int(sonuc.get("kisi_sayisi", 0)),
        ppe_uyum_orani     = str(sonuc.get("ppe_uyum_orani", -1)),
        analiz_edilen_kare = int(sonuc.get("analiz_edilen_kare", 1)),
        toplam_kare        = int(sonuc.get("toplam_kare", 1)),
        thumbnail          = sonuc.get("thumbnail", ""),
        tespitler          = json.dumps(sonuc.get("tespitler", []), ensure_ascii=False),
    )
    db.add(kayit)
    db.commit()
    db.refresh(kayit)
    return kayit


# ── /yolo/frame — IP kamera / fotoğraf tek frame analizi ─────────────────────
@app.post("/yolo/frame")
@limiter.limit("30/minute")
async def yolo_frame_analiz(
    request: Request,
    payload: dict = Body(...),
    db: Session = Depends(database.get_db),
):
    """
    Tek frame PPE analizi.
    Body: { token, resim_base64, santiye_id? }
    Returns: { risk_level, violations, confidence, kisi_sayisi, ppe_uyum_orani,
               timestamp, site_id, analiz_id, thumbnail }
    """
    token      = payload.get("token", "")
    b64_resim  = payload.get("resim_base64", "")
    santiye_id = payload.get("santiye_id") or None

    user = kullanici_dogrula(token, db)

    if not kullanim_kontrol(user, db, "kamera", 3, "hafta"):
        raise HTTPException(
            status_code=429,
            detail="Haftalık kamera analizi limitine ulaştınız. Pro plana geçin.",
        )

    if not b64_resim:
        raise HTTPException(status_code=400, detail="resim_base64 boş olamaz.")

    sonuc = await _ka.frame_analiz_b64(b64_resim, site_id=santiye_id, thumbnail=True)

    if "hata" in sonuc:
        raise HTTPException(status_code=422, detail=sonuc["hata"])

    kayit = _yolo_db_kaydet(user.id, sonuc, "foto", santiye_id, db)
    kullanim_kaydet(user.id, "kamera", db)

    logger.info(
        f"[YOLO/frame] user={user.id} santiye={santiye_id} "
        f"risk={sonuc['risk_level']} kisi={sonuc['kisi_sayisi']}"
    )

    return {**sonuc, "analiz_id": kayit.id}


# ── /yolo/video — Video dosyası yükleme & batch analiz ──────────────────────
@app.post("/yolo/video")
@limiter.limit("10/minute")
async def yolo_video_analiz(
    request: Request,
    token: str,
    video: UploadFile = File(...),
    santiye_id: Optional[int] = None,
    fps: float = 1.0,
    hareket_filtre: bool = True,
    db: Session = Depends(database.get_db),
):
    """
    Video upload → FFmpeg keyframe → YOLOv11 batch analiz.
    Form fields: token (str), santiye_id (int?), fps (float, default 1.0),
                 hareket_filtre (bool, default true)
    File field: video (mp4/avi/mov/mkv)
    Returns: { risk_level, violations, confidence, kisi_sayisi, ppe_uyum_orani,
               analiz_edilen_kare, toplam_kare, timestamp, analiz_id, thumbnail }
    """
    user = kullanici_dogrula(token, db)

    if not kullanim_kontrol(user, db, "kamera", 3, "hafta"):
        raise HTTPException(
            status_code=429,
            detail="Haftalık kamera analizi limitine ulaştınız. Pro plana geçin.",
        )

    # İzin verilen uzantılar
    IZINLI_UZANTILAR = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv"}
    uzanti = Path(video.filename or "").suffix.lower()
    if uzanti not in IZINLI_UZANTILAR:
        raise HTTPException(
            status_code=415,
            detail=f"Desteklenmeyen video formatı. İzin verilenler: {', '.join(IZINLI_UZANTILAR)}",
        )

    # Maksimum dosya boyutu: 200 MB
    MAX_BOYUT = 200 * 1024 * 1024
    icerik = await video.read()
    if len(icerik) > MAX_BOYUT:
        raise HTTPException(status_code=413, detail="Video dosyası 200 MB'ı aşamaz.")

    # Geçici dosyaya yaz
    with tempfile.NamedTemporaryFile(suffix=uzanti, delete=False) as tmp:
        tmp.write(icerik)
        tmp_path = tmp.name

    try:
        fps = max(0.1, min(fps, 5.0))   # 0.1 – 5 FPS aralığında sınırla
        sonuc = await _ka.video_analiz(
            video_path=tmp_path,
            site_id=santiye_id,
            fps=fps,
            hareket_filtre=hareket_filtre,
        )
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    if "hata" in sonuc and sonuc.get("analiz_edilen_kare", 0) == 0:
        raise HTTPException(status_code=422, detail=sonuc["hata"])

    kayit = _yolo_db_kaydet(user.id, sonuc, "video", santiye_id, db)
    kullanim_kaydet(user.id, "kamera", db)

    logger.info(
        f"[YOLO/video] user={user.id} santiye={santiye_id} "
        f"risk={sonuc['risk_level']} kare={sonuc.get('analiz_edilen_kare')}/{sonuc.get('toplam_kare')}"
    )

    return {**sonuc, "analiz_id": kayit.id}


# ── /yolo/analizler — Geçmiş analiz listesi ──────────────────────────────────
@app.get("/yolo/analizler")
@limiter.limit("60/minute")
def yolo_analizler(
    request: Request,
    token: str,
    santiye_id: Optional[int] = None,
    limit: int = 20,
    db: Session = Depends(database.get_db),
):
    """
    Kullanıcının (ve opsiyonel olarak şantiyenin) geçmiş YOLO analizleri.
    Returns: { analizler: [...] }
    """
    user = kullanici_dogrula(token, db)
    limit = max(1, min(limit, 100))

    q = db.query(models.VideoAnaliz).filter(models.VideoAnaliz.user_id == user.id)
    if santiye_id:
        q = q.filter(models.VideoAnaliz.santiye_id == santiye_id)
    kayitlar = q.order_by(models.VideoAnaliz.created_at.desc()).limit(limit).all()

    return {
        "analizler": [
            {
                "id":              k.id,
                "kaynak_tipi":     k.kaynak_tipi,
                "risk_level":      k.risk_level,
                "violations":      json.loads(k.violations or "[]"),
                "confidence":      float(k.confidence or 0),
                "kisi_sayisi":     k.kisi_sayisi,
                "ppe_uyum_orani":  float(k.ppe_uyum_orani or -1),
                "analiz_edilen_kare": k.analiz_edilen_kare,
                "santiye_id":      k.santiye_id,
                "thumbnail":       k.thumbnail[:200] + "..." if len(k.thumbnail) > 200 else k.thumbnail,
                "created_at":      str(k.created_at),
            }
            for k in kayitlar
        ]
    }


# ── /yolo/analizler/{id} — Tek analiz detayı ─────────────────────────────────
@app.get("/yolo/analizler/{analiz_id}")
@limiter.limit("60/minute")
def yolo_analiz_detay(
    request: Request,
    analiz_id: int,
    token: str,
    db: Session = Depends(database.get_db),
):
    user = kullanici_dogrula(token, db)
    kayit = db.query(models.VideoAnaliz).filter(
        models.VideoAnaliz.id == analiz_id,
        models.VideoAnaliz.user_id == user.id,
    ).first()
    if not kayit:
        raise HTTPException(status_code=404, detail="Analiz bulunamadı.")

    return {
        "id":                kayit.id,
        "kaynak_tipi":       kayit.kaynak_tipi,
        "risk_level":        kayit.risk_level,
        "violations":        json.loads(kayit.violations or "[]"),
        "ihlal_frekanslari": json.loads(kayit.ihlal_frekanslari or "{}"),
        "confidence":        float(kayit.confidence or 0),
        "kisi_sayisi":       kayit.kisi_sayisi,
        "ppe_uyum_orani":    float(kayit.ppe_uyum_orani or -1),
        "analiz_edilen_kare": kayit.analiz_edilen_kare,
        "toplam_kare":       kayit.toplam_kare,
        "tespitler":         json.loads(kayit.tespitler or "[]"),
        "thumbnail":         kayit.thumbnail,
        "santiye_id":        kayit.santiye_id,
        "created_at":        str(kayit.created_at),
    }


# ── /yolo/durum — Model sağlık kontrolü (public) ─────────────────────────────
@app.get("/yolo/durum")
def yolo_durum():
    """YOLO model durumunu ve OpenCV versiyonunu döner. Token gerekmez."""
    return _ka.model_durum()

