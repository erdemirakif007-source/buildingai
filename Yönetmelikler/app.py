from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import google.generativeai as genai
import secrets
import httpx
import models, schemas, auth, database
from interface import HTML_TEMPLATE

WEATHER_API_KEY = "YENI_KEY_BURAYA"

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# 🔑 AI KONFİGÜRASYONU
genai.configure(api_key="SENIN_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

# Şifre sıfırlama token'larını geçici hafızada tut
reset_tokens = {}

# --- 🛰️ HAVA DURUMU ---
@app.get("/hava")
async def get_weather(sehir: str = "Sivas"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={sehir},TR&appid={WEATHER_API_KEY}&units=metric&lang=tr"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            data = response.json()

        if response.status_code != 200:
            return {"temp": "--°C", "cond": "Veri alınamadı"}

        temp = round(data["main"]["temp"])
        desc = data["weather"][0]["description"].capitalize()
        hissedilen = round(data["main"]["feels_like"])
        nem = data["main"]["humidity"]

        uyari = ""
        if temp <= 0:
            uyari = " ⚠️ DON RİSKİ!"
        elif temp <= 5:
            uyari = " ❄️ Soğuk Hava"

        cond = f"{desc} | Hissedilen: {hissedilen}°C | Nem: %{nem}{uyari}"
        return {"temp": f"{temp}°C", "cond": cond}

    except Exception as e:
        return {"temp": "--°C", "cond": "Bağlantı hatası"}

# --- 🧠 AI ANALİZ ---
@app.post("/sor")
async def ask_ai(request: dict):
    soru = request.get("soru")
    hava = request.get("hava")
    system_prompt = f"Sen bir inşaat mühendisi asistanısın. Hava: {hava}. Teknik ve kısa yanıt ver."
    try:
        response = model.generate_content(f"{system_prompt}\nSoru: {soru}")
        return {"cevap": response.text}
    except Exception as e:
        return {"cevap": f"Hata: {str(e)}"}

@app.post("/cevir")
async def translate_to_english(payload: dict = Body(...)):
    metin = payload.get("metin")
    prompt = f"Aşağıdaki inşaat teknik analizini profesyonel IELTS 7.5 seviyesinde İngilizce teknik rapora çevir:\n\n{metin}"
    try:
        response = model.generate_content(prompt)
        return {"cevap": response.text}
    except:
        raise HTTPException(status_code=500, detail="Çeviri yapılamadı.")

@app.post("/sor_foto")
async def ask_ai_with_photo(request: dict):
    soru = request.get("soru")
    resim_base64 = request.get("resim_base64")
    hava = request.get("hava", "Bilinmiyor")
    system_prompt = f"Sen bir inşaat mühendisi asistanısın. Hava: {hava}. Fotoğrafı analiz et ve teknik cevap ver."
    try:
        from langchain_core.messages import HumanMessage
        import base64
        message = HumanMessage(
            content=[
                {"type": "text", "text": f"{system_prompt}\nSoru: {soru}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{resim_base64}"}}
            ]
        )
        response = model.invoke([message])
        return {"cevap": response.content}
    except Exception as e:
        return {"cevap": f"Fotoğraf analizi hatası: {str(e)}"}

# --- 📊 MÜHENDİSLİK HESAPLAMALARI ---
@app.get("/hesapla")
async def calculate_engineering(tip: str, v1: float, v2: float = 0, v3: float = 0):
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
def save_report(payload: dict = Body(...), db: Session = Depends(database.get_db)):
    rapor_metni = payload.get("rapor_metni")
    new_report = models.Report(content=rapor_metni, owner_id=1)
    db.add(new_report)
    db.commit()
    return {"mesaj": "Rapor başarıyla arşivlendi."}

@app.get("/rapor_listesi")
def list_reports(db: Session = Depends(database.get_db)):
    reports = db.query(models.Report).all()
    return {"raporlar": [r.created_at.strftime("%Y-%m-%d %H:%M") for r in reports]}

@app.get("/rapor_getir")
def get_report(tarih: str, db: Session = Depends(database.get_db)):
    report = db.query(models.Report).first()
    return {"icerik": report.content if report else "Rapor bulunamadı."}

# --- 🔐 ÜYELİK SİSTEMİ ---
@app.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
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
def login(request: dict, db: Session = Depends(database.get_db)):
    email = request.get("email")
    password = request.get("password")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not auth.verify_password(password[:72], user.hashed_password):
        raise HTTPException(status_code=400, detail="E-posta veya şifre hatalı!")
    return {
        "status": "success",
        "full_name": user.full_name,
        "email": user.email,
        "plan": getattr(user, 'plan', 'free')
    }

# --- 🔑 ŞİFRE SIFIRLAMA ---
@app.post("/sifre-sifirla")
def request_password_reset(payload: dict = Body(...), db: Session = Depends(database.get_db)):
    email = payload.get("email")
    user = db.query(models.User).filter(models.User.email == email).first()
    # Kullanıcı yoksa bile başarılı mesaj ver (güvenlik)
    token = secrets.token_urlsafe(32)
    reset_tokens[token] = email
    # Gerçek uygulamada burada email gönderilir
    # Şimdilik token'ı döndürüyoruz (test için)
    print(f"🔑 Şifre sıfırlama token: {token} - Email: {email}")
    return {"mesaj": "Sıfırlama bağlantısı e-posta adresinize gönderildi. (Demo: token terminalde görünür)"}

@app.post("/sifre-guncelle")
def update_password(payload: dict = Body(...), db: Session = Depends(database.get_db)):
    token = payload.get("token")
    yeni_sifre = payload.get("yeni_sifre")
    if token not in reset_tokens:
        raise HTTPException(status_code=400, detail="Geçersiz veya süresi dolmuş token.")
    email = reset_tokens[token]
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    user.hashed_password = auth.get_password_hash(yeni_sifre[:72])
    db.commit()
    del reset_tokens[token]
    return {"mesaj": "Şifreniz başarıyla güncellendi."}

@app.get("/", response_class=HTMLResponse)
async def main_page():
    return HTML_TEMPLATE
