"""
migrations/malzeme_genislet_v1.py
──────────────────────────────────
Turkiye insaat sektorundeki kapsamli malzeme listesini malzemeler tablosuna ekler.
Idempotent: ad alani eslesiyorsa INSERT atlanir.
"""

import sqlite3
import pathlib
import sys

DB_PATH = pathlib.Path(__file__).parent.parent / "santiye_proje.db"

# (kategori, alt_kategori, ad, birim)
MALZEMELER = [

    # ── YAPI MALZEMELERI - BETON ─────────────────────────────────────────────
    ("beton", "Beton", "C16/20 Hazır Beton", "m3"),
    ("beton", "Beton", "C20/25 Hazır Beton", "m3"),
    ("beton", "Beton", "C25/30 Hazır Beton", "m3"),
    ("beton", "Beton", "C30/37 Hazır Beton", "m3"),
    ("beton", "Beton", "C35/45 Hazır Beton", "m3"),
    ("beton", "Beton", "C40/50 Hazır Beton", "m3"),
    ("beton", "Beton", "C45/55 Hazır Beton", "m3"),
    ("beton", "Beton", "C50/60 Hazır Beton", "m3"),

    # ── YAPI MALZEMELERI - DEMIR / CELIK ────────────────────────────────────
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø8",   "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø10",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø12",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø14",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø16",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø18",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø20",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø22",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø24",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø26",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø28",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Nervürlü Demir Ø32",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Çelik Hasır Q131",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Çelik Hasır Q188",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Çelik Hasır Q221",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Çelik Hasır Q283",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Çelik Hasır Q335",  "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Filmaşin",               "ton"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil HEA 100",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil HEA 120",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil HEA 140",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil HEA 160",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil HEA 200",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil HEB 100",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil HEB 120",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil HEB 140",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil HEB 160",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil HEB 200",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil IPE 100",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil IPE 120",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil IPE 140",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil IPE 160",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Profil IPE 200",  "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Köşebent L50x5",    "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Köşebent L60x6",    "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Çelik Levha 8mm",        "kg"),
    ("Yapi Malzemeleri", "Demir/Celik", "Kutu Profil 60x60",           "kg"),

    # ── YAPI MALZEMELERI - CIMENTO ───────────────────────────────────────────
    ("Yapi Malzemeleri", "Çimento", "Akçansa CEM I 42.5",         "torba"),
    ("Yapi Malzemeleri", "Çimento", "Akçansa CEM I 52.5",         "torba"),
    ("Yapi Malzemeleri", "Çimento", "Çimsa CEM II 32.5",          "torba"),
    ("Yapi Malzemeleri", "Çimento", "Beyaz Çimento",              "torba"),
    ("Yapi Malzemeleri", "Çimento", "Sülfata Dayanıklı Çimento", "torba"),
    ("Yapi Malzemeleri", "Çimento", "Harman Çimentosu CEM II",    "torba"),

    # ── YAPI MALZEMELERI - AGREGA ────────────────────────────────────────────
    ("Yapi Malzemeleri", "Agrega", "İnce Kum (0-2mm)",    "ton"),
    ("Yapi Malzemeleri", "Agrega", "Kaba Kum",                 "ton"),
    ("Yapi Malzemeleri", "Agrega", "Şap Kumu",             "ton"),
    ("Yapi Malzemeleri", "Agrega", "Çakıl (5-12mm)", "ton"),
    ("Yapi Malzemeleri", "Agrega", "Çakıl (12-22mm)","ton"),
    ("Yapi Malzemeleri", "Agrega", "Kırmataş (0-5mm)",  "ton"),
    ("Yapi Malzemeleri", "Agrega", "Kırmataş (5-12mm)", "ton"),
    ("Yapi Malzemeleri", "Agrega", "Mıcır (12-22mm)",   "ton"),
    ("Yapi Malzemeleri", "Agrega", "Stabilize Malzeme",        "ton"),
    ("Yapi Malzemeleri", "Agrega", "Dolgu Kumu",               "ton"),
    ("Yapi Malzemeleri", "Agrega", "Beton Kum (0-4mm)",        "ton"),

    # ── YAPI MALZEMELERI - TUGLA / BLOK ─────────────────────────────────────
    ("Yapi Malzemeleri", "Tuğla/Blok", "Yatay Delikli Tuğla",    "adet"),
    ("Yapi Malzemeleri", "Tuğla/Blok", "Düşey Delikli Tuğla", "adet"),
    ("Yapi Malzemeleri", "Tuğla/Blok", "Gazbeton G2",                  "m3"),
    ("Yapi Malzemeleri", "Tuğla/Blok", "Gazbeton G4",                  "m3"),
    ("Yapi Malzemeleri", "Tuğla/Blok", "Gazbeton Düz Duvar Bloğu", "m3"),
    ("Yapi Malzemeleri", "Tuğla/Blok", "Bims Blok",                    "adet"),
    ("Yapi Malzemeleri", "Tuğla/Blok", "Briket",                       "adet"),
    ("Yapi Malzemeleri", "Tuğla/Blok", "Karkas Tuğla",            "adet"),
    ("Yapi Malzemeleri", "Tuğla/Blok", "Pomza Blok",                   "adet"),
    ("Yapi Malzemeleri", "Tuğla/Blok", "Hafif Beton Blok",             "adet"),

    # ── KALIP ────────────────────────────────────────────────────────────────
    ("Kalıp", "Kalıp Malzemeleri", "Plywood 12mm",              "m2"),
    ("Kalıp", "Kalıp Malzemeleri", "Plywood 15mm",              "m2"),
    ("Kalıp", "Kalıp Malzemeleri", "Plywood 18mm",              "m2"),
    ("Kalıp", "Kalıp Malzemeleri", "Plywood 21mm",              "m2"),
    ("Kalıp", "Kalıp Malzemeleri", "Kalıp Yağı", "lt"),
    ("Kalıp", "Kalıp Malzemeleri", "Teleskopik Direk",          "adet"),
    ("Kalıp", "Kalıp Malzemeleri", "Kalıp Bağlantı Elemanı", "adet"),
    ("Kalıp", "Kalıp Malzemeleri", "Kalıp Çubuk Tie-Rod", "adet"),

    # ── YALITIM - ISI ────────────────────────────────────────────────────────
    ("Yalıtım", "Isı Yalıtımı", "XPS 3cm",  "m2"),
    ("Yalıtım", "Isı Yalıtımı", "XPS 4cm",  "m2"),
    ("Yalıtım", "Isı Yalıtımı", "XPS 5cm",  "m2"),
    ("Yalıtım", "Isı Yalıtımı", "XPS 6cm",  "m2"),
    ("Yalıtım", "Isı Yalıtımı", "XPS 8cm",  "m2"),
    ("Yalıtım", "Isı Yalıtımı", "XPS 10cm", "m2"),
    ("Yalıtım", "Isı Yalıtımı", "EPS 3cm",  "m2"),
    ("Yalıtım", "Isı Yalıtımı", "EPS 5cm",  "m2"),
    ("Yalıtım", "Isı Yalıtımı", "EPS 10cm", "m2"),
    ("Yalıtım", "Isı Yalıtımı", "Taşyünü Levha",  "m2"),
    ("Yalıtım", "Isı Yalıtımı", "Cam Yünü Levha",      "m2"),
    ("Yalıtım", "Isı Yalıtımı", "Rockwool Levha",                "m2"),

    # ── YALITIM - SU ─────────────────────────────────────────────────────────
    ("Yalıtım", "Su Yalıtımı", "Bitümlü Membran 4mm",      "m2"),
    ("Yalıtım", "Su Yalıtımı", "Bitümlü Membran 3mm",      "m2"),
    ("Yalıtım", "Su Yalıtımı", "PVC Su Yalıtım Membranı", "m2"),
    ("Yalıtım", "Su Yalıtımı", "Likit Membran",                      "kg"),
    ("Yalıtım", "Su Yalıtımı", "Bentonit Levha",                     "m2"),
    ("Yalıtım", "Su Yalıtımı", "Kristalize Su Yalıtımı","kg"),

    # ── YALITIM - SES ────────────────────────────────────────────────────────
    ("Yalıtım", "Ses Yalıtımı", "Akustik Levha",        "m2"),
    ("Yalıtım", "Ses Yalıtımı", "Ses Yalıtım Keçesi", "m2"),
    ("Yalıtım", "Ses Yalıtımı", "Akustik Cam Yünü",        "m2"),

    # ── INCE ISLER - SIVA ────────────────────────────────────────────────────
    ("İnce İşler", "Sıva", "Hazır İnce Sıva",    "torba"),
    ("İnce İşler", "Sıva", "Hazır Kaba Sıva",          "torba"),
    ("İnce İşler", "Sıva", "Alçı Sıva",           "torba"),
    ("İnce İşler", "Sıva", "Dış Cephe Sıvası","torba"),
    ("İnce İşler", "Sıva", "Yapıştırma Alçısı", "torba"),
    ("İnce İşler", "Sıva", "Makine Sıvası",            "torba"),

    # ── INCE ISLER - BOYA ────────────────────────────────────────────────────
    ("İnce İşler", "Boya", "İç Cephe Boyası",            "lt"),
    ("İnce İşler", "Boya", "Dış Cephe Boyası",           "lt"),
    ("İnce İşler", "Boya", "Astar Boya",                                "lt"),
    ("İnce İşler", "Boya", "Antipas Boya",                              "lt"),
    ("İnce İşler", "Boya", "Epoksi Boya",                               "lt"),
    ("İnce İşler", "Boya", "Silikon Esaslı Cephe Boyası",    "lt"),
    ("İnce İşler", "Boya", "Süper İç Cephe Boyası","lt"),

    # ── INCE ISLER - SERAMIK / FAYANS ───────────────────────────────────────
    ("İnce İşler", "Seramik/Fayans", "Yer Seramiği (30x30)",    "m2"),
    ("İnce İşler", "Seramik/Fayans", "Yer Seramiği (60x60)",    "m2"),
    ("İnce İşler", "Seramik/Fayans", "Duvar Fayansı (25x40)",     "m2"),
    ("İnce İşler", "Seramik/Fayans", "Duvar Fayansı (30x60)",     "m2"),
    ("İnce İşler", "Seramik/Fayans", "Granit Karo (60x60)",            "m2"),
    ("İnce İşler", "Seramik/Fayans", "Granit Karo (80x80)",            "m2"),
    ("İnce İşler", "Seramik/Fayans", "Porselen Karo (60x60)",          "m2"),
    ("İnce İşler", "Seramik/Fayans", "Seramik Yapıştırıcı", "torba"),
    ("İnce İşler", "Seramik/Fayans", "Derz Dolgu",                    "torba"),
    ("İnce İşler", "Seramik/Fayans", "Mermer (2cm)",                  "m2"),
    ("İnce İşler", "Seramik/Fayans", "Doğaltaş",             "m2"),

    # ── INCE ISLER - PARKE / ZEMIN ───────────────────────────────────────────
    ("İnce İşler", "Parke/Zemin", "Laminat Parke (8mm)",        "m2"),
    ("İnce İşler", "Parke/Zemin", "Laminat Parke (12mm)",       "m2"),
    ("İnce İşler", "Parke/Zemin", "Masif Parke",                "m2"),
    ("İnce İşler", "Parke/Zemin", "Vinil Zemin",                "m2"),
    ("İnce İşler", "Parke/Zemin", "Epoksi Zemin Kaplama",       "m2"),
    ("İnce İşler", "Parke/Zemin", "Karo Mozaik",                "m2"),
    ("İnce İşler", "Parke/Zemin", "Halatı Zemin",          "m2"),

    # ── INCE ISLER - ALCIPAN ─────────────────────────────────────────────────
    ("İnce İşler", "Alçıpan", "Normal Alçıpan 12.5mm",        "m2"),
    ("İnce İşler", "Alçıpan", "Suya Dayanıklı Alçıpan", "m2"),
    ("İnce İşler", "Alçıpan", "Yangın Dayanıklı Alçıpan", "m2"),
    ("İnce İşler", "Alçıpan", "Profil C50",  "m"),
    ("İnce İşler", "Alçıpan", "Profil C75",  "m"),
    ("İnce İşler", "Alçıpan", "Profil U50",  "m"),
    ("İnce İşler", "Alçıpan", "Profil U75",  "m"),
    ("İnce İşler", "Alçıpan", "Alçıpan Vidası", "kutu"),

    # ── TESISAT - SU ─────────────────────────────────────────────────────────
    ("Tesisat", "Su Tesisatı", "PPR Boru Ø20",  "m"),
    ("Tesisat", "Su Tesisatı", "PPR Boru Ø25",  "m"),
    ("Tesisat", "Su Tesisatı", "PPR Boru Ø32",  "m"),
    ("Tesisat", "Su Tesisatı", "PPR Boru Ø40",  "m"),
    ("Tesisat", "Su Tesisatı", "PPR Boru Ø50",  "m"),
    ("Tesisat", "Su Tesisatı", "PPR Boru Ø63",  "m"),
    ("Tesisat", "Su Tesisatı", "Bakır Boru 15mm", "m"),
    ("Tesisat", "Su Tesisatı", "Bakır Boru 22mm", "m"),
    ("Tesisat", "Su Tesisatı", "Bakır Boru 28mm", "m"),

    # ── TESISAT - KANALIZASYON ───────────────────────────────────────────────
    ("Tesisat", "Kanalizasyon", "PVC Boru Ø32",   "m"),
    ("Tesisat", "Kanalizasyon", "PVC Boru Ø40",   "m"),
    ("Tesisat", "Kanalizasyon", "PVC Boru Ø50",   "m"),
    ("Tesisat", "Kanalizasyon", "PVC Boru Ø63",   "m"),
    ("Tesisat", "Kanalizasyon", "PVC Boru Ø110",  "m"),
    ("Tesisat", "Kanalizasyon", "PVC Boru Ø125",  "m"),
    ("Tesisat", "Kanalizasyon", "PVC Boru Ø160",  "m"),
    ("Tesisat", "Kanalizasyon", "PVC Boru Ø200",  "m"),

    # ── TESISAT - DOGALGAZ ───────────────────────────────────────────────────
    ("Tesisat", "Doğalgaz", "Çelik Gaz Borusu",  "m"),
    ("Tesisat", "Doğalgaz", "PE Gaz Borusu",           "m"),

    # ── ELEKTRIK - KABLO ─────────────────────────────────────────────────────
    ("Elektrik", "Kablo", "NYA Kablo 1.5mm²",       "m"),
    ("Elektrik", "Kablo", "NYA Kablo 2.5mm²",       "m"),
    ("Elektrik", "Kablo", "NYA Kablo 4mm²",         "m"),
    ("Elektrik", "Kablo", "NYA Kablo 6mm²",         "m"),
    ("Elektrik", "Kablo", "NYM Kablo 2x1.5mm²",     "m"),
    ("Elektrik", "Kablo", "NYM Kablo 3x1.5mm²",     "m"),
    ("Elektrik", "Kablo", "NYM Kablo 3x2.5mm²",     "m"),
    ("Elektrik", "Kablo", "NYM Kablo 5x2.5mm²",     "m"),
    ("Elektrik", "Kablo", "NHXMH Kablo 3x1.5mm²",   "m"),
    ("Elektrik", "Kablo", "NHXMH Kablo 3x2.5mm²",   "m"),

    # ── ELEKTRIK - BORU / AKSESUAR ───────────────────────────────────────────
    ("Elektrik", "Boru/Aksesuar", "Spiral Boru 16mm",        "m"),
    ("Elektrik", "Boru/Aksesuar", "Spiral Boru 20mm",        "m"),
    ("Elektrik", "Boru/Aksesuar", "Spiral Boru 25mm",        "m"),
    ("Elektrik", "Boru/Aksesuar", "Rigid PVC Boru 16mm",     "m"),
    ("Elektrik", "Boru/Aksesuar", "Rigid PVC Boru 20mm",     "m"),
    ("Elektrik", "Boru/Aksesuar", "Priz",                    "adet"),
    ("Elektrik", "Boru/Aksesuar", "Anahtar",                 "adet"),
    ("Elektrik", "Boru/Aksesuar", "Sigorta Otomatik",        "adet"),
    ("Elektrik", "Boru/Aksesuar", "Elektrik Panosu",         "adet"),
    ("Elektrik", "Boru/Aksesuar", "LED Aydınlatma Armatürü", "adet"),
    ("Elektrik", "Boru/Aksesuar", "Topraklama İletkeni", "m"),

    # ── CATI ─────────────────────────────────────────────────────────────────
    ("Çatı", "Çatı Örtüsü", "Kiremit",                    "adet"),
    ("Çatı", "Çatı Örtüsü", "Shingle Çatı Örtüsü", "m2"),
    ("Çatı", "Çatı Örtüsü", "Trapez Sac",                 "m2"),
    ("Çatı", "Çatı Örtüsü", "Sandviç Panel",         "m2"),
    ("Çatı", "Çatı Aksesuarları", "Çatı Astarı",     "m2"),
    ("Çatı", "Çatı Aksesuarları", "Mahya",                          "m"),
    ("Çatı", "Çatı Aksesuarları", "Oluk Derekenar",                 "m"),
    ("Çatı", "Çatı Aksesuarları", "Rüzgar Tahtası",       "m"),
    ("Çatı", "Çatı Aksesuarları", "Dere Sacı",                 "m"),

    # ── MANTOLAMA ────────────────────────────────────────────────────────────
    ("Mantolama", "Mantolama", "Mantolama Yapıştırıcısı", "torba"),
    ("Mantolama", "Mantolama", "Cam Tülü File",                                "m2"),
    ("Mantolama", "Mantolama", "XPS Mantolama Levhası",                             "m2"),
    ("Mantolama", "Mantolama", "EPS Mantolama Levhası",                             "m2"),
    ("Mantolama", "Mantolama", "Mantolama Sıvası",                             "torba"),
    ("Mantolama", "Mantolama", "Mantolama Son Kat Boya",                                 "lt"),
    ("Mantolama", "Mantolama", "Mantolama Dübeli",                                  "adet"),

    # ── PREFABRIK ────────────────────────────────────────────────────────────
    ("Prefabrik", "Prefabrik Elemanlar", "Prekast Kolon",          "adet"),
    ("Prefabrik", "Prefabrik Elemanlar", "Prekast Kiriş",     "adet"),
    ("Prefabrik", "Prefabrik Elemanlar", "Prekast Döşeme Paneli", "m2"),
    ("Prefabrik", "Prefabrik Elemanlar", "Prefabrik Duvar Paneli", "m2"),
    ("Prefabrik", "Prefabrik Elemanlar", "Hollowcore Döşeme", "m2"),

    # ── YARDIMCI ─────────────────────────────────────────────────────────────
    ("Yardımcı", "Bağlantı Elemanları", "Bağ Teli",  "kg"),
    ("Yardımcı", "Bağlantı Elemanları", "Çivi",      "kg"),
    ("Yardımcı", "Bağlantı Elemanları", "Vida",           "kutu"),
    ("Yardımcı", "Bağlantı Elemanları", "Dübel",     "adet"),
    ("Yardımcı", "Bağlantı Elemanları", "Bulon",          "adet"),
    ("Yardımcı", "Bağlantı Elemanları", "Conta",          "adet"),
    ("Yardımcı", "İskele", "Çelik İskele",               "m2"),
    ("Yardımcı", "İskele", "Ahşap İskele",                    "m2"),
    ("Yardımcı", "Geoteknik", "Geotekstil",                             "m2"),
    ("Yardımcı", "Geoteknik", "Geosentetik",                            "m2"),
    ("Yardımcı", "Geoteknik", "Drenaj Çakılı",           "ton"),
    ("Yardımcı", "Sızdırmazlık", "Silikon Dolgu",        "adet"),
    ("Yardımcı", "Sızdırmazlık", "Poliüretan Köpük", "adet"),
    ("Yardımcı", "Sızdırmazlık", "İzolasyon Bandı", "m"),
]


def run(db_path: pathlib.Path = DB_PATH) -> None:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")

    try:
        inserted = 0
        skipped = 0

        with conn:
            for kategori, alt_kategori, ad, birim in MALZEMELER:
                cur = conn.execute(
                    "INSERT OR IGNORE INTO malzemeler "
                    "(kategori, alt_kategori, ad, birim, aktif, scrape_tipi) "
                    "VALUES (?, ?, ?, ?, 1, 'manuel')",
                    (kategori, alt_kategori, ad, birim),
                )
                if cur.rowcount:
                    inserted += 1
                else:
                    skipped += 1

        total = conn.execute("SELECT COUNT(*) FROM malzemeler").fetchone()[0]
        print(f"Eklendi: {inserted}, Atlandi (mevcut/csb cakisma): {skipped}")
        print(f"Toplam malzeme tablosunda: {total}")
        print("Migration tamamlandi.")

    except Exception as e:
        print(f"HATA: {e}", file=sys.stderr)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=str(DB_PATH))
    args = parser.parse_args()
    run(pathlib.Path(args.db))
