from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import datetime
import os

PRIMARY = colors.HexColor('#e67e22')
GRAY = colors.HexColor('#a0a0a0')

def load_fonts():
    font_paths = [
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
        ("C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/calibrib.ttf"),
        ("C:/Windows/Fonts/tahoma.ttf", "C:/Windows/Fonts/tahomabd.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
    ]
    for regular, bold in font_paths:
        if os.path.exists(regular):
            try:
                pdfmetrics.registerFont(TTFont('TurkceFont', regular))
                if os.path.exists(bold):
                    pdfmetrics.registerFont(TTFont('TurkceFont-Bold', bold))
                else:
                    pdfmetrics.registerFont(TTFont('TurkceFont-Bold', regular))
                return True
            except:
                continue
    return False

FONT_LOADED = load_fonts()
NORMAL_FONT = 'TurkceFont' if FONT_LOADED else 'Helvetica'
BOLD_FONT = 'TurkceFont-Bold' if FONT_LOADED else 'Helvetica-Bold'

def temizle(metin: str) -> str:
    if not metin:
        return ""
    satirlar = metin.split('\n')
    sonuc = []
    for satir in satirlar:
        satir = satir.strip()
        if not satir:
            sonuc.append('<br/>')
            continue
        if satir.startswith('## '):
            baslik = satir[3:].replace('**', '').replace('*', '')
            sonuc.append(f'<b>{baslik}</b><br/>')
        elif '**' in satir:
            import re
            satir = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', satir)
            sonuc.append(satir + '<br/>')
        elif satir.startswith('* ') or satir.startswith('- '):
            satir = '• ' + satir[2:]
            sonuc.append(satir + '<br/>')
        else:
            sonuc.append(satir + '<br/>')
    return ' '.join(sonuc)

def rapor_olustur(kullanici_adi, sehir, hava_durumu, analiz_metni, ingilizce_metni="", dil="tr"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

    baslik_style = ParagraphStyle('Baslik', fontSize=22, textColor=PRIMARY, fontName=BOLD_FONT, alignment=TA_CENTER, spaceAfter=5)
    alt_baslik_style = ParagraphStyle('AltBaslik', fontSize=10, textColor=GRAY, fontName=NORMAL_FONT, alignment=TA_CENTER, spaceAfter=15)
    bolum_baslik_style = ParagraphStyle('BolumBaslik', fontSize=13, textColor=PRIMARY, fontName=BOLD_FONT, spaceBefore=15, spaceAfter=8)
    metin_style = ParagraphStyle('Metin', fontSize=10, textColor=colors.HexColor('#222222'), fontName=NORMAL_FONT, leading=16, spaceAfter=6)
    kucuk_style = ParagraphStyle('Kucuk', fontSize=8, textColor=GRAY, fontName=NORMAL_FONT, alignment=TA_CENTER)

    elements = []
    tarih = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph("BUILDINGAI PRO", baslik_style))
    baslik_text = f"Santiye Analiz Raporu - {tarih}" if dil == "tr" else f"Site Analysis Report - {tarih}"
    elements.append(Paragraph(baslik_text, alt_baslik_style))
    elements.append(HRFlowable(width="100%", thickness=2, color=PRIMARY))
    elements.append(Spacer(1, 0.5*cm))

    if dil == "tr":
        info_data = [["Muhendis", kullanici_adi], ["Sehir / Santiye", sehir], ["Hava Durumu", hava_durumu], ["Tarih", tarih]]
    else:
        info_data = [["Engineer", kullanici_adi], ["City / Site", sehir], ["Weather", hava_durumu], ["Date", tarih]]

    info_table = Table(info_data, colWidths=[4.5*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
        ('FONTNAME', (0, 0), (0, -1), BOLD_FONT),
        ('FONTNAME', (1, 0), (1, -1), NORMAL_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.6*cm))

    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#dddddd')))
    elements.append(Paragraph("AI Analizi" if dil == "tr" else "AI Analysis", bolum_baslik_style))
    elements.append(Paragraph(temizle(analiz_metni), metin_style))
    elements.append(Spacer(1, 0.4*cm))

    if ingilizce_metni and ingilizce_metni.strip():
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#dddddd')))
        elements.append(Paragraph("English Technical Report" if dil == "tr" else "Turkce Rapor", bolum_baslik_style))
        elements.append(Paragraph(temizle(ingilizce_metni), metin_style))
        elements.append(Spacer(1, 0.4*cm))

    elements.append(Spacer(1, 1*cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=PRIMARY))
    elements.append(Spacer(1, 0.2*cm))
    footer = "Bu rapor BuildingAI Pro tarafindan olusturulmustur. buildingaipro.com" if dil == "tr" else "Generated by BuildingAI Pro. buildingaipro.com"
    elements.append(Paragraph(footer, kucuk_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def haftalik_rapor_olustur(kullanici_adi, sehir, hafta_verisi):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

    baslik_style = ParagraphStyle('Baslik', fontSize=22, textColor=PRIMARY, fontName=BOLD_FONT, alignment=TA_CENTER, spaceAfter=5)
    alt_baslik_style = ParagraphStyle('AltBaslik', fontSize=10, textColor=GRAY, fontName=NORMAL_FONT, alignment=TA_CENTER, spaceAfter=15)
    bolum_baslik_style = ParagraphStyle('BolumBaslik', fontSize=13, textColor=PRIMARY, fontName=BOLD_FONT, spaceBefore=15, spaceAfter=8)
    metin_style = ParagraphStyle('Metin', fontSize=10, textColor=colors.HexColor('#222222'), fontName=NORMAL_FONT, leading=16, spaceAfter=6)
    kucuk_style = ParagraphStyle('Kucuk', fontSize=8, textColor=GRAY, fontName=NORMAL_FONT, alignment=TA_CENTER)

    elements = []
    tarih = datetime.datetime.now().strftime("%d.%m.%Y")
    hafta_basi = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%d.%m.%Y")

    # Kapak
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("BUILDINGAI PRO", baslik_style))
    elements.append(Paragraph(f"Haftalik Ozet Raporu", alt_baslik_style))
    elements.append(Paragraph(f"{hafta_basi} - {tarih}", alt_baslik_style))
    elements.append(HRFlowable(width="100%", thickness=2, color=PRIMARY))
    elements.append(Spacer(1, 0.5*cm))

    # Bilgi tablosu
    info_data = [
        ["Muhendis / Muteahhit", kullanici_adi],
        ["Sehir / Santiye", sehir],
        ["Rapor Tarihi", tarih],
        ["Kapsanan Hafta", f"{hafta_basi} - {tarih}"]
    ]
    info_table = Table(info_data, colWidths=[4.5*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f5f5f5')),
        ('BACKGROUND', (1,0), (1,-1), colors.white),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#333333')),
        ('FONTNAME', (0,0), (0,-1), BOLD_FONT),
        ('FONTNAME', (1,0), (1,-1), NORMAL_FONT),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.6*cm))

    # 1. Haftalık Özet (AI yorumu)
    if hafta_verisi.get('ai_yorum'):
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#dddddd')))
        elements.append(Paragraph("AI Haftalik Degerlendirme", bolum_baslik_style))
        elements.append(Paragraph(temizle(hafta_verisi['ai_yorum']), metin_style))
        elements.append(Spacer(1, 0.3*cm))

    # 2. ISG Raporu
    isg_kayitlar = hafta_verisi.get('isg_kayitlar', [])
    if isg_kayitlar:
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#dddddd')))
        elements.append(Paragraph("ISG Raporu", bolum_baslik_style))
        isg_data = [["Tarih", "Durum", "Notlar"]]
        for k in isg_kayitlar[:10]:
            isg_data.append([k.get('tarih',''), k.get('durum',''), k.get('notlar','')[:60]])
        isg_table = Table(isg_data, colWidths=[3*cm, 3.5*cm, 10*cm])
        isg_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), PRIMARY),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), BOLD_FONT),
            ('FONTNAME', (0,1), (-1,-1), NORMAL_FONT),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('PADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#fafafa')]),
        ]))
        elements.append(isg_table)
        elements.append(Spacer(1, 0.3*cm))

    # 3. Malzeme/Stok Özeti
    stok_verisi = hafta_verisi.get('stok', {})
    if stok_verisi:
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#dddddd')))
        elements.append(Paragraph("Malzeme ve Stok Ozeti", bolum_baslik_style))
        stok_data = [["Malzeme", "Mevcut Stok", "Haftalik Giris", "Haftalik Cikis", "Durum"]]
        malzeme_ad = {'demir':'Demir','cimento':'Cimento','beton':'Beton','tugla':'Tugla','kum':'Kum'}
        for m, s in stok_verisi.items():
            durum = "Kritik!" if s.get('bitis_gun') and s['bitis_gun'] <= 7 else "Normal"
            stok_data.append([
                malzeme_ad.get(m, m),
                str(s.get('mevcut', 0)),
                str(s.get('haftalik_giris', 0)),
                str(s.get('haftalik_cikis', 0)),
                durum
            ])
        stok_table = Table(stok_data, colWidths=[3*cm, 3*cm, 3*cm, 3*cm, 4.5*cm])
        stok_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), PRIMARY),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), BOLD_FONT),
            ('FONTNAME', (0,1), (-1,-1), NORMAL_FONT),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('PADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#fafafa')]),
        ]))
        elements.append(stok_table)
        elements.append(Spacer(1, 0.3*cm))

    # 4. Fotoğraf/Analiz Galerisi
    foto_listesi = hafta_verisi.get('foto_analizler', [])
    if foto_listesi:
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#dddddd')))
        elements.append(Paragraph("Kamera Analizi Ozeti", bolum_baslik_style))
        for f in foto_listesi[:5]:
            elements.append(Paragraph(f"• {f.get('tarih','')} — {f.get('tip','')} analizi", metin_style))
            if f.get('ozet'):
                elements.append(Paragraph(temizle(f['ozet'][:300]), metin_style))
        elements.append(Spacer(1, 0.3*cm))

    # Footer
    elements.append(Spacer(1, 1*cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=PRIMARY))
    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph("Bu rapor BuildingAI Pro tarafindan otomatik olusturulmustur. buildingaipro.com", kucuk_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
