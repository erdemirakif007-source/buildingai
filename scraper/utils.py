"""Scraper yardımcı fonksiyonları."""
import re
import datetime


def parse_fiyat(raw: str) -> float | None:
    """
    Türkçe para formatını float'a çevirir.
    Örnekler: "34.400,00 TL" → 34400.0
              "1.234.567,89" → 1234567.89
              "32.800"       → 32800.0
    """
    if not raw:
        return None
    # Sadece rakam, nokta, virgül bırak
    cleaned = re.sub(r"[^\d.,]", "", raw.strip())
    if not cleaned:
        return None
    # Türkçe format: nokta binlik ayraç, virgül ondalık
    if "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    else:
        # Nokta yoksa ya da sadece binlik ayraç varsa
        cleaned = cleaned.replace(".", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_tarih_tr(raw: str) -> str | None:
    """
    "12.05.2026" veya "12/05/2026" → "2026-05-12" (ISO 8601).
    """
    raw = raw.strip()
    for fmt in ("%d.%m.%Y", "%d/%m/%Y"):
        try:
            return datetime.datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def bugun_iso() -> str:
    return datetime.date.today().isoformat()


def parse_para_birimi(raw: str) -> str:
    """
    Fiyat stringinden para birimini çıkarır.
    "30.000,00 TL" → "TRY"
    "635,00 USD"   → "USD"
    Tanınmazsa "TRY" döner.
    """
    upper = raw.upper()
    if "USD" in upper or "$" in upper:
        return "USD"
    if "EUR" in upper or "€" in upper:
        return "EUR"
    return "TRY"


def parse_archive_table(soup: "BeautifulSoup") -> list[dict]:  # type: ignore[name-defined]
    """
    Proemtia archive-table yapısını parse eder (hasır, filmaşin sayfaları).

    HTML kapalı tag içermediğinden BS4 html.parser tüm satırları iç içe yuvar:
      <tr data-date="YYYY-MM-DD">
        <td>GG.AA.YYYY        ← tarih td (outer)
          <td>FİYAT            ← fiyat td (iç içe)
            <tr ...>           ← sonraki satır buraya gömülü

    Fiyatı temiz okumak için her tag'ın yalnızca ilk NavigableString düğümü kullanılır.

    Döner: [{"tarih": "2026-05-13", "fiyat": 30000.0, "para_birimi": "TRY"}, ...]
    En yeni tarih öne gelecek şekilde sıralanmış liste.
    """
    from bs4 import NavigableString  # burada import — döngüsel import önlemi

    tablo = soup.find("table", class_="archive-table")
    if not tablo:
        return []

    def _first_text(tag) -> str:
        """Tag'ın ilk NavigableString çocuğunu döndürür."""
        return next(
            (str(c).strip() for c in tag.children
             if isinstance(c, NavigableString) and str(c).strip()),
            ""
        )

    sonuclar = []
    for satir in tablo.find_all("tr", attrs={"data-date": True}):
        data_date = satir.get("data-date", "").strip()
        outer_td = satir.find("td")
        if not outer_td:
            continue
        inner_td = outer_td.find("td")
        if not inner_td:
            continue
        fiyat_raw = _first_text(inner_td)
        fiyat = parse_fiyat(fiyat_raw)
        if fiyat is None:
            continue
        sonuclar.append({
            "tarih":       data_date,
            "fiyat":       fiyat,
            "para_birimi": parse_para_birimi(fiyat_raw),
        })

    sonuclar.sort(key=lambda r: r["tarih"], reverse=True)
    return sonuclar


def parse_product_card_base(card: "Tag", tarih: str, kaynak_url: str) -> dict | None:  # type: ignore[name-defined]
    """
    Tüm Proemtia ürün sayfalarında ortak olan product-card alanlarını çıkarır.

    Döner: {href, pid, satici_slug, satici, konum, fiyat_kdv_dahil,
             fiyat_kdv_haric, para_birimi, birim, attrs, tarih, kaynak, kaynak_url}
    Fiyat bulunamazsa None döner.
    """
    from urllib.parse import parse_qs, urlparse

    href = card.get("href", "")
    full_url = ("https://www.proemtia.com" + href) if href.startswith("/") else href
    qs           = parse_qs(urlparse(href).query)
    pid          = qs.get("pid",    [""])[0]
    satici_slug  = qs.get("satici", [""])[0]

    satici_span  = card.find("span", class_="success")
    satici       = satici_span.get_text(strip=True) if satici_span else ""

    konum_span   = card.find("span", class_="location")
    konum        = konum_span.get_text(strip=True) if konum_span else ""

    price_p = card.find("p", class_="price")
    if not price_p:
        return None
    price_raw        = price_p.get_text(strip=True)
    fiyat_kdv_dahil  = parse_fiyat(price_raw)
    if fiyat_kdv_dahil is None:
        return None

    # Birim: "₺/Ton" → "ton",  "₺/Adet" → "adet",  "₺/m²" → "m2"  vb.
    birim_m = re.search(r"[/]([\w²³]+)", price_raw)
    birim   = birim_m.group(1).lower().replace("²", "2").replace("³", "3") if birim_m else ""

    vat_span        = card.find("span", class_="vat")
    fiyat_kdv_haric = parse_fiyat(vat_span.get_text(strip=True)) if vat_span else None

    # Kart attribute satırları: {"Boyut": "25.00", "Kalite": "Standart"} gibi
    attrs: dict[str, str] = {}
    for div in card.select(".info div"):
        spans = div.find_all("span")
        if len(spans) == 2:
            key = spans[0].get_text(strip=True)
            val = spans[1].get_text(strip=True)
            if key:
                attrs[key] = val

    return {
        "pid":             pid,
        "satici_slug":     satici_slug,
        "satici":          satici,
        "konum":           konum,
        "fiyat_kdv_dahil": fiyat_kdv_dahil,
        "fiyat_kdv_haric": fiyat_kdv_haric,
        "para_birimi":     "TRY",
        "birim":           birim,
        "attrs":           attrs,
        "urun_url":        full_url,
        "tarih":           tarih,
        "kaynak":          "proemtia_urun",
        "kaynak_url":      kaynak_url,
    }
