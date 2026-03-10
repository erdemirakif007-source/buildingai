import math

class Calculator:
    def hesapla(self, tip: str, v1: float, v2: float, v3: float):
        try:
            if tip == 'beton':
                hacim = v1 * v2 * v3
                mikser = math.ceil(hacim / 12)
                return {"sonuc": f"{hacim:.2f} m³", "detay": f"Yaklaşık {mikser} mikser (12m³ kapasiteli) beton gerekir."}
            elif tip == 'demir_ag':
                agirlik = ((v1**2) / 162) * v2
                return {"sonuc": f"{agirlik:.2f} kg", "detay": f"Toplam {agirlik/1000:.3f} ton donatı siparişi geçilmeli."}
            elif tip == 'as_alan':
                alan = (math.pi * (v1/2)**2) * v2 / 100 # mm2'den cm2'ye
                return {"sonuc": f"{alan:.2f} cm²", "detay": f"{int(v2)} adet Ø{int(v1)} donatının toplam kesit alanı."}
            elif tip == 'etriye':
                boy = (v1 + v2) * 2 + 0.20 # 20cm kanca payı
                return {"sonuc": f"{boy:.2f} m", "detay": f"Tek etriye kesim boyu. Kanca ve paspayı (yaklaşık) dahildir."}
            elif tip == 'tugla':
                adet_m2 = 25 if v2 > 10 else 40
                toplam = v1 * adet_m2
                return {"sonuc": f"{toplam:.0f} Adet", "detay": f"{v1} m² alan için %5 fire dahil tahmini tuğla sarfiyatı."}
            elif tip == 'seramik':
                fireli = v1 * 1.10
                return {"sonuc": f"{fireli:.2f} m²", "detay": f"Kesim ve köşe fireleri (%10) dahil edilmiştir."}
            elif tip == 'boya':
                litre = v1 * 0.15 # Ortalama 0.15 lt/m2
                return {"sonuc": f"{litre:.1f} Litre", "detay": f"Çift kat uygulama için tahmini boya sarfiyatı."}
            elif tip == 'kubaj':
                hacim = ((v1 + v2) / 2) * v3
                kamyon = math.ceil(hacim / 18)
                return {"sonuc": f"{hacim:.2f} m³", "detay": f"Kazı/Dolgu hacmi. Yaklaşık {kamyon} kamyon (18m³) sefer yapar."}
            elif tip == 'egim':
                yuzde = (v1 / v2) * 100
                derece = math.degrees(math.atan(v1 / v2))
                return {"sonuc": f"% {yuzde:.1f}", "detay": f"Rampa açısı yaklaşık {derece:.1f} derecedir."}
            elif tip == 'isi':
                u_val = 0.035 / (v1 / 100) # Yaklaşık EPS iletkenliği
                return {"sonuc": f"{u_val:.2f} W/m²K", "detay": f"Sivas şartlarında bu ısı iletim katsayısı (U) ne kadar düşükse o kadar iyidir."}
            else:
                return {"sonuc": "Bilinmeyen Hesap", "detay": "Bu araç henüz yapım aşamasında."}
        except Exception as e:
            return {"sonuc": "Hesap Hatası", "detay": str(e)}