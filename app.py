from fastapi import FastAPI, Depends, HTTPException, status, Body, Request
from fastapi.responses import HTMLResponse, Response, JSONResponse
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

load_dotenv()

GMAIL_ADRES = os.getenv("GMAIL_ADRES")
GMAIL_UYGULAMA_SIFRESI = os.getenv("GMAIL_UYGULAMA_SIFRESI")
import models, schemas, auth, database
from interface import HTML_TEMPLATE
from admin_panel import ADMIN_HTML
from weather import hava_getir
from pdf_rapor import rapor_olustur

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

app = FastAPI()

# Rate Limiter
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

async def ai_cevap(prompt: str) -> str:
    response = ai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# Şifre sıfırlama token'larını geçici hafızada tut
reset_tokens = {}

# Başarısız giriş takibi: {email: {"count": int, "locked_until": datetime | None}}
login_attempts: dict = {}

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

# --- 🧠 AI ANALİZ ---
@app.post("/sor")
@limiter.limit("60/minute")
async def ask_ai(request: Request, body: dict = Body(...), db: Session = Depends(database.get_db)):
    soru = body.get("soru")
    hava = body.get("hava")
    dil = body.get("dil", "tr")
    token = body.get("token", "")
    user = kullanici_dogrula(token, db)
    if not kullanim_kontrol(user, db, 'sor', 10, 'gun'):
        raise HTTPException(status_code=429, detail="Günlük AI soru limitinize (10) ulaştınız. Pro'ya geçerek sınırsız kullanın.")
    kullanim_kaydet(user.id, 'sor', db)

    if dil == "en":
        system_prompt = f"""You are a senior construction engineer with 30 years of experience. 
Current weather conditions at the site: {hava}

STRICT RULES:
- Answer ONLY based on Turkish construction regulations (TSE standards, TBDY, TS 500, İSG regulations)
- If the topic is not in your regulations, clearly state it
- Structure your answer with these exact sections:

## 📋 HOW TO DO IT
Step-by-step technical procedure based on regulations.

## ⚠️ RISKS
List the main risks for this operation under current conditions.

## 🛡️ PRECAUTIONS
Required precautions and safety measures per regulations.

## 📐 TECHNICAL VALUES
Relevant measurements, ratios, limits from standards (if applicable).

Keep each section concise and technical. No unnecessary filler text."""
    else:
        system_prompt = f"""Sen 30 yıllık deneyime sahip kıdemli bir inşaat mühendisisin.
Şantiyenin mevcut hava koşulları: {hava}

KESİN KURALLAR:
- SADECE Türk inşaat yönetmeliklerine göre cevap ver (TSE standartları, TBDY, TS 500, İSG yönetmelikleri)
- Konu yönetmeliklerde yoksa bunu açıkça belirt
- Cevabını şu başlıklar altında ver:

## 📋 NASIL YAPILIR
Yönetmeliklere göre adım adım teknik prosedür.

## ⚠️ RİSKLER
Mevcut koşullarda bu işlem için başlıca riskler.

## 🛡️ ÖNLEMLER
Yönetmeliklere göre alınması gereken önlemler ve güvenlik tedbirleri.

## 📐 TEKNİK DEĞERLER
İlgili ölçüler, oranlar, standartlardan limitler (varsa).

Her bölümü kısa ve teknik tut. Gereksiz dolgu metin yok."""

    try:
        logger.info(f"AI QUERY: type=sor")
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
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                f"{system_prompt}\nSoru: {soru}"
            ]
        )
        return {"cevap": response.text}
    except Exception as e:
        return {"cevap": f"Fotoğraf analizi hatası: {str(e)}"}

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
        full_name=user.full_name
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

    # Hesap kilitli mi kontrol et
    attempt = login_attempts.get(email)
    if attempt and attempt.get("locked_until"):
        if datetime.datetime.utcnow() < attempt["locked_until"]:
            remaining = int((attempt["locked_until"] - datetime.datetime.utcnow()).total_seconds() / 60) + 1
            raise HTTPException(
                status_code=429,
                detail=f"Çok fazla başarısız giriş denemesi. Hesap {remaining} dakika kilitli."
            )
        else:
            # Kilit süresi doldu, sıfırla
            login_attempts.pop(email, None)

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not auth.verify_password(password[:72], user.hashed_password):
        # Başarısız denemeyi kaydet
        rec = login_attempts.setdefault(email, {"count": 0, "locked_until": None})
        rec["count"] += 1
        if rec["count"] >= 5:
            rec["locked_until"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
            rec["count"] = 0
            logger.warning(f"ACCOUNT LOCKED: {email}")
            raise HTTPException(status_code=429, detail="5 başarısız deneme. Hesap 15 dakika kilitlendi.")
        logger.warning(f"LOGIN FAILED: {email}")
        raise HTTPException(status_code=400, detail="E-posta veya şifre hatalı!")

    # Başarılı girişte sayacı temizle
    login_attempts.pop(email, None)
    logger.info(f"LOGIN SUCCESS: {email}")

    token = auth.create_access_token({"email": user.email})
    return {
        "status": "success",
        "full_name": user.full_name,
        "email": user.email,
        "plan": getattr(user, 'plan', 'free'),
        "token": token
    }

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
    reset_tokens[kod] = {"email": email, "created_at": datetime.datetime.utcnow()}

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

    token_data = reset_tokens.get(kod)
    if not token_data:
        raise HTTPException(status_code=400, detail="Geçersiz kod.")

    gecen = (datetime.datetime.utcnow() - token_data["created_at"]).total_seconds()
    if gecen > 3600:
        del reset_tokens[kod]
        raise HTTPException(status_code=400, detail="Kodun süresi dolmuş. Yeni kod isteyin.")

    if len(yeni_sifre) < 8:
        raise HTTPException(status_code=400, detail="Şifre en az 8 karakter olmalıdır.")

    user = db.query(models.User).filter(models.User.email == token_data["email"]).first()
    user.hashed_password = auth.get_password_hash(yeni_sifre[:72])
    db.commit()
    del reset_tokens[kod]
    logger.info(f"PASSWORD RESET SUCCESS: {token_data['email']}")
    return {"mesaj": "Şifreniz güncellendi!"}

@app.get("/", response_class=HTMLResponse)
@limiter.limit("60/minute")
async def main_page(request: Request):
    return HTML_TEMPLATE

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
            model="gemini-2.5-flash",
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
    """Admin ve Pro sınırsız. Returns True if allowed."""
    if user.email == ADMIN_EMAIL or getattr(user, 'plan', 'free') == 'pro':
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
Analyze this construction site photo for safety violations.
Structure your response:
## 🦺 SAFETY VIOLATIONS DETECTED
List any missing PPE (helmets, vests, gloves, boots) or unsafe behaviors.
## ✅ COMPLIANT ITEMS
What safety measures are correctly in place.
## ⚠️ IMMEDIATE ACTIONS REQUIRED
Priority actions to fix violations per İSG regulations.
## 📊 SAFETY SCORE
Give a score out of 100."""
        elif analiz_tipi == "ilerleme":
            prompt_text = f"""You are a construction site progress analyst. Weather: {hava}
Analyze this construction site photo for progress tracking.
## 📋 CURRENT PROGRESS STATUS
What stage of construction is visible.
## ✅ COMPLETED WORK
What has been finished.
## 🔄 ONGOING WORK
What is currently in progress.
## 📅 ESTIMATED TIMELINE
Based on visible progress, estimate completion timeline.
## ⚠️ POTENTIAL DELAYS
Any visible issues that could cause delays."""
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
Any specific technical observations."""
    else:
        if analiz_tipi == "guvenlik":
            prompt_text = f"""Sen bir şantiye iş güvenliği uzmanısın. Hava: {hava}
Bu şantiye fotoğrafını İSG yönetmeliklerine göre güvenlik ihlalleri için analiz et.
## 🦺 TESPİT EDİLEN GÜVENLİK İHLALLERİ
Eksik KKD (baret, yelek, eldiven, bot) veya güvensiz davranışlar.
## ✅ UYGUN OLAN UNSURLAR
Doğru uygulanan güvenlik önlemleri.
## ⚠️ ACİL ALINMASI GEREKEN ÖNLEMLER
İSG yönetmeliğine göre öncelikli düzeltici aksiyonlar.
## 📊 GÜVENLİK SKORU
100 üzerinden güvenlik puanı ver."""
        elif analiz_tipi == "ilerleme":
            prompt_text = f"""Sen bir şantiye ilerleme analistisin. Hava: {hava}
Bu şantiye fotoğrafını ilerleme takibi için analiz et.
## 📋 MEVCUT İLERLEME DURUMU
Fotoğrafta görünen inşaat aşaması.
## ✅ TAMAMLANAN İŞLER
Bitirilen çalışmalar.
## 🔄 DEVAM EDEN İŞLER
Şu an süren çalışmalar.
## 📅 TAHMİNİ SÜRE
Görünen ilerlemeye göre tamamlanma tahmini.
## ⚠️ OLASI GECİKMELER
Gecikmeye yol açabilecek görünür sorunlar."""
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
Özel teknik gözlemler."""

    try:
        import base64
        from google.genai import types
        image_bytes = base64.b64decode(resim_base64)
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                prompt_text
            ]
        )
        sonuc = response.text

        # Arşive kaydet
        analiz = models.KameraAnaliz(
            user_id=user.id,
            analiz_tipi=analiz_tipi,
            sonuc=sonuc,
            resim_base64=resim_base64[:500],  # Sadece başını sakla (yer tasarrufu)
            sehir=sehir,
            hava=hava,
            dil=dil
        )
        db.add(analiz)
        db.commit()

        return {"cevap": sonuc, "analiz_id": analiz.id}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analiz hatası: {str(e)}")

# --- 📁 KİŞİSEL ARŞİV ---
@app.get("/arsiv")
@limiter.limit("60/minute")
def arsiv_getir(request: Request, token: str, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    is_pro = user.email == ADMIN_EMAIL or getattr(user, 'plan', 'free') == 'pro'
    arsiv_limit = 50 if is_pro else 10

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

# --- 📊 KULLANIM DURUMU ---
@app.get("/kullanim-durumu")
@limiter.limit("60/minute")
def kullanim_durumu(request: Request, token: str, db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)
    is_pro = user.email == ADMIN_EMAIL or getattr(user, 'plan', 'free') == 'pro'

    bugun = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    bugun_hafta = datetime.datetime.utcnow() - datetime.timedelta(days=datetime.datetime.utcnow().weekday())
    bugun_hafta = bugun_hafta.replace(hour=0, minute=0, second=0, microsecond=0)

    def count(tip, baslangic):
        return db.query(models.Usage).filter(
            models.Usage.user_id == user.id,
            models.Usage.tip == tip,
            models.Usage.created_at >= baslangic
        ).count()

    return {
        "plan": "pro" if is_pro else "free",
        "kullanim": {
            "sor":          {"kullanilan": count('sor', bugun),                 "limit": None if is_pro else 10},
            "kamera":       {"kullanilan": count('kamera', bugun_hafta),        "limit": None if is_pro else 3},
            "sesli_rapor":  {"kullanilan": count('sesli_rapor', bugun),         "limit": None if is_pro else 1},
            "gunluk_rapor": {"kullanilan": count('gunluk_rapor', bugun),        "limit": None if is_pro else 1},
        }
    }

# --- 💳 ÖDEME BİLDİRİMİ ---
@app.post("/odeme-bildirimi")
async def odeme_bildirimi(request: Request, token: str = Body(...), db: Session = Depends(database.get_db)):
    user = kullanici_dogrula(token, db)

    terminal_komutu = f'sqlite3 buildingai.db "UPDATE users SET plan=\'pro\' WHERE email=\'{user.email}\';"'

    admin_html = f"""
    <h2>💳 Yeni Ödeme Bildirimi</h2>
    <p><b>Kullanıcı:</b> {user.full_name} ({user.email})</p>
    <p><b>Tarih:</b> {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
    <hr>
    <p>Ödemeyi onaylamak için aşağıdaki komutu çalıştır:</p>
    <pre style="background:#111;color:#0f0;padding:12px;border-radius:8px;">{terminal_komutu}</pre>
    """

    kullanici_html = f"""
    <h2>✅ Ödeme Bildiriminiz Alındı</h2>
    <p>Merhaba {user.full_name or user.email},</p>
    <p>Pro plana geçiş talebiniz alındı. Ödemeniz onaylandıktan sonra hesabınız yükseltilecektir.</p>
    <p>Genellikle 24 saat içinde işleme alınır. Herhangi bir sorunuz için <a href="mailto:{ADMIN_EMAIL}">{ADMIN_EMAIL}</a> adresine yazabilirsiniz.</p>
    <p><b>BuildingAI Pro Ekibi</b></p>
    """

    email_gonder(ADMIN_EMAIL, f"💳 Ödeme Bildirimi: {user.email}", admin_html)
    email_gonder(user.email, "BuildingAI Pro - Ödeme Bildiriminiz Alındı", kullanici_html)

    logger.info(f"PAYMENT NOTIFICATION: {user.email}")
    return {"mesaj": "Ödeme bildiriminiz alındı. 24 saat içinde hesabınız Pro'ya yükseltilecektir."}

# --- 🔧 ADMIN PANELİ ---
def admin_kontrol(token: str, db: Session):
    user = kullanici_dogrula(token, db)
    if user.email != ADMIN_EMAIL:
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

