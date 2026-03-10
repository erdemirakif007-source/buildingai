import httpx
from dotenv import load_dotenv
import os

load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

HAVA_IKONLARI = {
    "açık": "☀️",
    "az bulutlu": "⛅",
    "parçalı bulutlu": "🌤️",
    "bulutlu": "☁️",
    "kapalı": "🌫️",
    "yağmur": "🌧️",
    "hafif yağmur": "🌦️",
    "kar": "❄️",
    "sis": "🌫️",
    "fırtına": "⛈️",
}

def ikon_sec(desc: str) -> str:
    desc_lower = desc.lower()
    for kelime, ikon in HAVA_IKONLARI.items():
        if kelime in desc_lower:
            return ikon
    return "🌤️"

async def hava_getir(sehir: str = "Sivas") -> dict:
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={sehir},TR"
            f"&appid={WEATHER_API_KEY}"
            f"&units=metric"
            f"&lang=tr"
        )
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)
            data = response.json()

        if response.status_code != 200:
            return {"temp": "--°C", "cond": "Veri alınamadı"}

        temp        = round(data["main"]["temp"])
        hissedilen  = round(data["main"]["feels_like"])
        nem         = data["main"]["humidity"]
        ruzgar      = round(data["wind"]["speed"] * 3.6)  # m/s → km/h
        desc        = data["weather"][0]["description"].capitalize()
        ikon        = ikon_sec(desc)

        # ⚠️ İnşaat uyarıları
        uyarilar = []
        if temp <= 0:
            uyarilar.append("⚠️ DON RİSKİ — Beton dökümü tehlikeli!")
        elif temp <= 5:
            uyarilar.append("❄️ Soğuk hava — Antifriz önlem alın")
        if ruzgar >= 40:
            uyarilar.append("💨 Kuvvetli rüzgar — İskele kontrolü yapın")
        if nem >= 90:
            uyarilar.append("💧 Yüksek nem — Boyama/sıva uygun değil")

        uyari_str = " | ".join(uyarilar) if uyarilar else "Şantiye koşulları normal"

        cond = f"{ikon} {desc} | Hissedilen: {hissedilen}°C | Nem: %{nem} | Rüzgar: {ruzgar}km/h | {uyari_str}"

        return {"temp": f"{temp}°C", "cond": cond}

    except httpx.TimeoutException:
        return {"temp": "--°C", "cond": "⏱️ Zaman aşımı"}
    except Exception as e:
        return {"temp": "--°C", "cond": f"Bağlantı hatası"}