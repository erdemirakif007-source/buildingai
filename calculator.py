import math

class Calculator:
    def hesapla(self, tip: str, v1: float, v2: float, v3: float):
        try:
            if tip == 'beton':
                hacim = v1 * v2 * v3
                mikser = math.ceil(hacim / 12)
                return {"sonuc": f"{hacim:.2f} m³", "detay": f"Yaklaşık {mikser} mikser gerekir.", "adimlar": [
                    "Formül: Hacim = Boy × En × Yükseklik",
                    f"Hacim = {v1} × {v2} × {v3} = {hacim:.2f} m³",
                    f"Mikser = ⌈{hacim:.2f} ÷ 12⌉ = {mikser} adet (12m³ kapasiteli)",
                ]}
            elif tip == 'demir_ag':
                ag = ((v1**2) / 162) * v2
                return {"sonuc": f"{ag:.2f} kg", "detay": f"Toplam {ag/1000:.3f} ton.", "adimlar": [
                    "Formül: Ağırlık = (Çap² ÷ 162) × Uzunluk",
                    f"= ({v1}² ÷ 162) × {v2}",
                    f"= ({v1**2:.0f} ÷ 162) × {v2} = {ag:.2f} kg",
                    f"= {ag/1000:.3f} ton",
                ]}
            elif tip == 'as_alan':
                alan = (math.pi * (v1/2)**2) * v2 / 100
                return {"sonuc": f"{alan:.2f} cm²", "detay": f"{int(v2)} adet Ø{int(v1)} donatı kesit alanı.", "adimlar": [
                    "Formül: As = π × (d/2)² × n",
                    f"= π × ({v1}/2)² × {int(v2)}",
                    f"= π × {(v1/2)**2:.2f} × {int(v2)}",
                    f"= {alan:.2f} cm²",
                ]}
            elif tip == 'etriye':
                boy = (v1 + v2) * 2 + 0.20
                return {"sonuc": f"{boy:.2f} m", "detay": "Kanca ve paspayı dahil.", "adimlar": [
                    "Formül: Boy = (En + Boy) × 2 + Kanca Payı",
                    f"= ({v1} + {v2}) × 2 + 0.20m",
                    f"= {(v1+v2)*2:.2f} + 0.20 = {boy:.2f} m",
                ]}
            elif tip == 'tugla':
                adet_m2 = 25 if v2 > 10 else 40
                toplam = v1 * adet_m2
                return {"sonuc": f"{toplam:.0f} Adet", "detay": f"{v1} m² için fire dahil tahmin.", "adimlar": [
                    f"Tuğla tipi: {'Normal (25 adet/m²)' if adet_m2 == 25 else 'Delikli (40 adet/m²)'}",
                    f"Alan = {v1} m²",
                    f"Toplam = {v1} × {adet_m2} = {toplam:.0f} adet",
                    "%5 fire dahildir",
                ]}
            elif tip == 'seramik':
                fireli = v1 * 1.10
                return {"sonuc": f"{fireli:.2f} m²", "detay": "%10 fire dahil.", "adimlar": [
                    "Fire oranı = %10 (kesim + köşe kayıpları)",
                    f"Net alan = {v1} m²",
                    f"Fire dahil = {v1} × 1.10 = {fireli:.2f} m²",
                ]}
            elif tip == 'boya':
                litre = v1 * 0.15
                return {"sonuc": f"{litre:.1f} Litre", "detay": "Çift kat tahmini.", "adimlar": [
                    "Sarfiyat = 0.15 lt/m² (çift kat ortalama)",
                    f"Alan = {v1} m²",
                    f"Toplam = {v1} × 0.15 = {litre:.1f} litre",
                ]}
            elif tip == 'kubaj':
                hacim = ((v1 + v2) / 2) * v3
                kamyon = math.ceil(hacim / 18)
                return {"sonuc": f"{hacim:.2f} m³", "detay": f"{kamyon} kamyon sefer yapar.", "adimlar": [
                    "Formül: Hacim = ((Uzunluk + Genişlik) / 2) × Derinlik",
                    f"= (({v1} + {v2}) / 2) × {v3}",
                    f"= {(v1+v2)/2:.2f} × {v3} = {hacim:.2f} m³",
                    f"Kamyon = ⌈{hacim:.2f} ÷ 18⌉ = {kamyon} kamyon",
                ]}
            elif tip == 'egim':
                yuzde = (v1 / v2) * 100
                derece = math.degrees(math.atan(v1 / v2))
                return {"sonuc": f"%{yuzde:.1f}", "detay": f"Rampa açısı {derece:.1f}°", "adimlar": [
                    "Formül: Eğim% = (Yükseklik ÷ Yatay Mesafe) × 100",
                    f"= ({v1} ÷ {v2}) × 100 = %{yuzde:.1f}",
                    f"Açı = arctan({v1}/{v2}) = {derece:.1f}°",
                ]}
            elif tip == 'isi':
                u_val = 0.035 / (v1 / 100)
                return {"sonuc": f"{u_val:.2f} W/m²K", "detay": "U ne kadar düşükse o kadar iyi.", "adimlar": []}
            else:
                return {"sonuc": "Bilinmeyen Hesap", "detay": "Bu araç henüz yapım aşamasında."}
        except Exception as e:
            return {"sonuc": "Hesap Hatası", "detay": str(e)}