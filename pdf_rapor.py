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
