# -*- coding: utf-8 -*-
"""
ÇŞB (Çevre ve Şehircilik Bakanlığı) birim fiyat pozlarına dayalı katalog seed data.
Tablolar: csb_malzeme_katalog, csb_is_kalemi_katalog, csb_is_kalemi_malzeme
"""
import logging

logger = logging.getLogger("buildingai")

# ─── Malzeme Katalogu ────────────────────────────────────────────────────────
# (poz_no, kategori, alt_kategori, ad, birim, aciklama)
MALZEME_KATALOG_DATA = [
    # AGREGALAR
    ("10.130.1001", "Agrega", "Kaba Agrega", "Çakıl (elenmesi gerekmeyen iri agrega)", "m³", "TS 706 EN 12620+A1"),
    ("10.130.1002", "Agrega", "Kaba Agrega", "Çakıl (elenmiş ve yıkanmış)", "m³", "TS 706 EN 12620+A1"),
    ("10.130.1004", "Agrega", "İnce Agrega", "Kum (elenmesi gerekmeyen ince agrega)", "m³", "TS 706 EN 12620+A1"),
    ("10.130.1005", "Agrega", "İnce Agrega", "Kum (elenmiş ve yıkanmış)", "m³", "TS 706 EN 12620+A1"),
    ("10.130.1007", "Agrega", "İnce Agrega", "İnce sıva veya derz kumu (elenmiş ve yıkanmış)", "m³", None),
    ("10.130.1008", "Agrega", "Kırma Taş", "32 mm'ye kadar kırmataş", "m³", None),
    ("10.130.1009", "Agrega", "Kırma Taş", "63 mm'ye kadar kırmataş (karışık)", "m³", None),
    # BAĞLAYICILAR
    ("10.130.1101", "Bağlayıcı", "Çimento", "Portland Çimentosu (Torbalı) CEM I 42,5R", "ton", "TS EN 197-1"),
    ("10.130.1102", "Bağlayıcı", "Çimento", "Portland Çimentosu (Dökme) CEM I 42,5R", "ton", "TS EN 197-1"),
    ("10.130.1103", "Bağlayıcı", "Çimento", "Katkılı Çimento (Torbalı) CEM II", "ton", "TS EN 197-1"),
    ("10.130.1104", "Bağlayıcı", "Çimento", "Katkılı Çimento (Dökme) CEM II", "ton", "TS EN 197-1"),
    ("10.130.1110", "Bağlayıcı", "Kireç", "Sönmüş Kireç", "ton", None),
    ("10.130.1111", "Bağlayıcı", "Kireç", "Sönmemiş Kireç", "ton", None),
    ("10.130.1120", "Bağlayıcı", "Alçı", "Yapı Alçısı", "ton", "TS EN 13279-1"),
    ("10.130.1121", "Bağlayıcı", "Alçı", "Saten Alçı", "ton", None),
    ("10.130.1122", "Bağlayıcı", "Alçı", "Makine Alçısı", "ton", None),
    # HAZIR BETON
    ("10.130.1200", "Hazır Beton", "Normal", "C16/20 Hazır Beton", "m³", "TS EN 206"),
    ("10.130.1201", "Hazır Beton", "Normal", "C20/25 Hazır Beton", "m³", "TS EN 206"),
    ("10.130.1202", "Hazır Beton", "Normal", "C25/30 Hazır Beton", "m³", "TS EN 206"),
    ("10.130.1203", "Hazır Beton", "Normal", "C30/37 Hazır Beton", "m³", "TS EN 206"),
    ("10.130.1204", "Hazır Beton", "Normal", "C35/45 Hazır Beton", "m³", "TS EN 206"),
    ("10.130.1205", "Hazır Beton", "Normal", "C40/50 Hazır Beton", "m³", "TS EN 206"),
    ("10.130.1210", "Hazır Beton", "Özel", "Kendiliğinden Yerleşen Beton (KYB) C30/37", "m³", None),
    ("10.130.1211", "Hazır Beton", "Özel", "Lifli Beton C30/37", "m³", None),
    ("10.130.1215", "Hazır Beton", "Şap", "Şap Betonu", "m³", None),
    # DEMİR-ÇELİK
    ("10.130.1301", "Demir-Çelik", "Nervürlü Demir", "Nervürlü Çelik Çubuğu Ø8 (B420C)", "ton", "TS 708"),
    ("10.130.1302", "Demir-Çelik", "Nervürlü Demir", "Nervürlü Çelik Çubuğu Ø10 (B420C)", "ton", "TS 708"),
    ("10.130.1303", "Demir-Çelik", "Nervürlü Demir", "Nervürlü Çelik Çubuğu Ø12 (B420C)", "ton", "TS 708"),
    ("10.130.1304", "Demir-Çelik", "Nervürlü Demir", "Nervürlü Çelik Çubuğu Ø14 (B420C)", "ton", "TS 708"),
    ("10.130.1305", "Demir-Çelik", "Nervürlü Demir", "Nervürlü Çelik Çubuğu Ø16 (B420C)", "ton", "TS 708"),
    ("10.130.1306", "Demir-Çelik", "Nervürlü Demir", "Nervürlü Çelik Çubuğu Ø18 (B420C)", "ton", "TS 708"),
    ("10.130.1307", "Demir-Çelik", "Nervürlü Demir", "Nervürlü Çelik Çubuğu Ø20 (B420C)", "ton", "TS 708"),
    ("10.130.1308", "Demir-Çelik", "Nervürlü Demir", "Nervürlü Çelik Çubuğu Ø22 (B420C)", "ton", "TS 708"),
    ("10.130.1309", "Demir-Çelik", "Nervürlü Demir", "Nervürlü Çelik Çubuğu Ø25 (B420C)", "ton", "TS 708"),
    ("10.130.1310", "Demir-Çelik", "Nervürlü Demir", "Nervürlü Çelik Çubuğu Ø28 (B420C)", "ton", "TS 708"),
    ("10.130.1311", "Demir-Çelik", "Nervürlü Demir", "Nervürlü Çelik Çubuğu Ø32 (B420C)", "ton", "TS 708"),
    ("10.130.1320", "Demir-Çelik", "Hasır Çelik", "Çelik Hasır Q131/131 (Ø5/5 - 150/150)", "ton", "TS 4559"),
    ("10.130.1321", "Demir-Çelik", "Hasır Çelik", "Çelik Hasır Q188/188 (Ø6/6 - 150/150)", "ton", "TS 4559"),
    ("10.130.1322", "Demir-Çelik", "Hasır Çelik", "Çelik Hasır Q221/221 (Ø6/6 - 125/125)", "ton", "TS 4559"),
    ("10.130.1323", "Demir-Çelik", "Hasır Çelik", "Çelik Hasır Q335/335 (Ø8/8 - 150/150)", "ton", "TS 4559"),
    ("10.130.1330", "Demir-Çelik", "Profil", "IPE Profil (çeşitli)", "ton", None),
    ("10.130.1331", "Demir-Çelik", "Profil", "HEA Profil (çeşitli)", "ton", None),
    ("10.130.1332", "Demir-Çelik", "Profil", "Kutu Profil (çeşitli)", "ton", None),
    ("10.130.1340", "Demir-Çelik", "Tel", "Bağ Teli (yumuşak)", "kg", None),
    ("10.130.1341", "Demir-Çelik", "Tel", "Çivi (çeşitli)", "kg", None),
    # KALIP MALZEMELERİ
    ("10.130.1401", "Kalıp", "Ahşap", "Kalıp Tahtası (çam, 2.5 cm)", "m³", None),
    ("10.130.1402", "Kalıp", "Ahşap", "Kalıp Tahtası (çam, 3.0 cm)", "m³", None),
    ("10.130.1403", "Kalıp", "Ahşap", "Kereste (çam, çeşitli)", "m³", None),
    ("10.130.1404", "Kalıp", "Ahşap", "Kadron (çam, 5x10 cm)", "m³", None),
    ("10.130.1410", "Kalıp", "Panel", "Plywood (su kontrası 18 mm)", "m²", None),
    ("10.130.1411", "Kalıp", "Panel", "Film Kaplı Plywood (18 mm)", "m²", None),
    ("10.130.1420", "Kalıp", "Çelik", "Çelik Panel Kalıp (kiralık)", "m²", "Günlük kira bedeli"),
    ("10.130.1421", "Kalıp", "Çelik", "Tünel Kalıp Sistemi (kiralık)", "m²", "Günlük kira bedeli"),
    # YALITIM
    ("10.130.1501", "Yalıtım", "Isı Yalıtımı", "EPS (Strafor) 2 cm", "m²", "TS EN 13163"),
    ("10.130.1502", "Yalıtım", "Isı Yalıtımı", "EPS (Strafor) 3 cm", "m²", "TS EN 13163"),
    ("10.130.1503", "Yalıtım", "Isı Yalıtımı", "EPS (Strafor) 5 cm", "m²", "TS EN 13163"),
    ("10.130.1504", "Yalıtım", "Isı Yalıtımı", "EPS (Strafor) 8 cm", "m²", "TS EN 13163"),
    ("10.130.1505", "Yalıtım", "Isı Yalıtımı", "EPS (Strafor) 10 cm", "m²", "TS EN 13163"),
    ("10.130.1510", "Yalıtım", "Isı Yalıtımı", "XPS 3 cm", "m²", "TS EN 13164"),
    ("10.130.1511", "Yalıtım", "Isı Yalıtımı", "XPS 5 cm", "m²", "TS EN 13164"),
    ("10.130.1512", "Yalıtım", "Isı Yalıtımı", "XPS 8 cm", "m²", "TS EN 13164"),
    ("10.130.1520", "Yalıtım", "Isı Yalıtımı", "Taş Yünü Levha 5 cm", "m²", "TS EN 13162"),
    ("10.130.1521", "Yalıtım", "Isı Yalıtımı", "Taş Yünü Levha 8 cm", "m²", "TS EN 13162"),
    ("10.130.1530", "Yalıtım", "Su Yalıtımı", "Bitümlü Membran (3 mm, -10°C)", "m²", None),
    ("10.130.1531", "Yalıtım", "Su Yalıtımı", "Bitümlü Membran (4 mm, -20°C)", "m²", None),
    ("10.130.1532", "Yalıtım", "Su Yalıtımı", "Polietilen Örtü (0.5 mm)", "m²", None),
    ("10.130.1533", "Yalıtım", "Su Yalıtımı", "Su Yalıtım Harcı (çimento esaslı)", "kg", None),
    ("10.130.1540", "Yalıtım", "Ses Yalıtımı", "Ses Yalıtım Keçesi", "m²", None),
    # TUĞLA / BLOK / GAZBETON
    ("10.130.1601", "Duvar", "Tuğla", "Yatay Delikli Tuğla (8.5 cm)", "adet", "TS EN 771-1"),
    ("10.130.1602", "Duvar", "Tuğla", "Yatay Delikli Tuğla (13.5 cm)", "adet", "TS EN 771-1"),
    ("10.130.1603", "Duvar", "Tuğla", "Yatay Delikli Tuğla (19 cm)", "adet", "TS EN 771-1"),
    ("10.130.1610", "Duvar", "Gazbeton", "Gazbeton Blok (G2, 10 cm)", "m³", "TS EN 771-4"),
    ("10.130.1611", "Duvar", "Gazbeton", "Gazbeton Blok (G2, 15 cm)", "m³", "TS EN 771-4"),
    ("10.130.1612", "Duvar", "Gazbeton", "Gazbeton Blok (G2, 20 cm)", "m³", "TS EN 771-4"),
    ("10.130.1613", "Duvar", "Gazbeton", "Gazbeton Blok (G2, 25 cm)", "m³", "TS EN 771-4"),
    ("10.130.1614", "Duvar", "Gazbeton", "Gazbeton Blok (G4, 20 cm)", "m³", "TS EN 771-4"),
    ("10.130.1620", "Duvar", "Bims", "Bims Blok (20 cm)", "adet", None),
    ("10.130.1621", "Duvar", "Bims", "Bims Blok (15 cm)", "adet", None),
    ("10.130.1625", "Duvar", "Briket", "Briket (20 cm)", "adet", None),
    # SIVA / HARÇ / BOYA
    ("10.130.1701", "Sıva-Harç", "Hazır Sıva", "Çimento Esaslı Hazır Sıva (İç)", "kg", None),
    ("10.130.1702", "Sıva-Harç", "Hazır Sıva", "Çimento Esaslı Hazır Sıva (Dış)", "kg", None),
    ("10.130.1703", "Sıva-Harç", "Hazır Sıva", "Alçı Esaslı Makine Sıvası", "kg", None),
    ("10.130.1710", "Sıva-Harç", "Yapıştırıcı", "Seramik Yapıştırıcısı (iç mekan)", "kg", None),
    ("10.130.1711", "Sıva-Harç", "Yapıştırıcı", "Seramik Yapıştırıcısı (dış mekan, esnek)", "kg", None),
    ("10.130.1712", "Sıva-Harç", "Yapıştırıcı", "Gazbeton Yapıştırıcısı", "kg", None),
    ("10.130.1713", "Sıva-Harç", "Yapıştırıcı", "EPS Yapıştırıcısı (mantolama)", "kg", None),
    ("10.130.1720", "Sıva-Harç", "Derz", "Derz Dolgu (iç mekan)", "kg", None),
    ("10.130.1721", "Sıva-Harç", "Derz", "Derz Dolgu (dış mekan, esnek)", "kg", None),
    ("10.130.1730", "Sıva-Harç", "Boya", "İç Cephe Boyası (plastik)", "lt", None),
    ("10.130.1731", "Sıva-Harç", "Boya", "İç Cephe Boyası (silikonlu)", "lt", None),
    ("10.130.1732", "Sıva-Harç", "Boya", "Dış Cephe Boyası (silikonlu)", "lt", None),
    ("10.130.1733", "Sıva-Harç", "Boya", "Antipas (antikorozif astar)", "lt", None),
    ("10.130.1734", "Sıva-Harç", "Boya", "Astar (iç cephe)", "lt", None),
    # KAPLAMA
    ("10.130.1801", "Kaplama", "Seramik", "Yer Seramiği (30x30 - 1. kalite)", "m²", None),
    ("10.130.1802", "Kaplama", "Seramik", "Yer Seramiği (40x40 - 1. kalite)", "m²", None),
    ("10.130.1803", "Kaplama", "Seramik", "Yer Seramiği (60x60 - 1. kalite)", "m²", None),
    ("10.130.1804", "Kaplama", "Seramik", "Duvar Seramiği (25x40 - 1. kalite)", "m²", None),
    ("10.130.1805", "Kaplama", "Seramik", "Duvar Seramiği (30x60 - 1. kalite)", "m²", None),
    ("10.130.1810", "Kaplama", "Granit", "Granit Yer Kaplaması (2 cm)", "m²", None),
    ("10.130.1811", "Kaplama", "Mermer", "Mermer Yer Kaplaması (2 cm)", "m²", None),
    ("10.130.1812", "Kaplama", "Mermer", "Mermer Denizlik", "m", None),
    ("10.130.1820", "Kaplama", "Parke", "Laminat Parke (AC4)", "m²", None),
    ("10.130.1821", "Kaplama", "Parke", "Laminat Parke (AC5)", "m²", None),
    ("10.130.1822", "Kaplama", "Parke", "Masif Parke (meşe)", "m²", None),
    # DOĞRAMA
    ("10.130.1901", "Doğrama", "PVC", "PVC Pencere Profili (5 odacık)", "m²", None),
    ("10.130.1902", "Doğrama", "PVC", "PVC Pencere Profili (7 odacık)", "m²", None),
    ("10.130.1910", "Doğrama", "Alüminyum", "Alüminyum Doğrama (ısı yalıtımlı)", "m²", None),
    ("10.130.1920", "Doğrama", "Cam", "4 mm Düz Cam", "m²", None),
    ("10.130.1921", "Doğrama", "Cam", "Isıcam (4+12+4 mm)", "m²", None),
    ("10.130.1922", "Doğrama", "Cam", "Isıcam (4+12+4 mm, Low-E)", "m²", None),
    ("10.130.1930", "Doğrama", "Kapı", "İç Kapı (lake, kasalı)", "adet", None),
    ("10.130.1931", "Doğrama", "Kapı", "Çelik Kapı (dış)", "adet", None),
    ("10.130.1932", "Doğrama", "Kapı", "Yangın Kapısı (90 dk)", "adet", None),
    # TESİSAT
    ("10.130.2001", "Tesisat", "Boru", "PPR Boru Ø20 (PN20)", "m", None),
    ("10.130.2002", "Tesisat", "Boru", "PPR Boru Ø25 (PN20)", "m", None),
    ("10.130.2003", "Tesisat", "Boru", "PPR Boru Ø32 (PN20)", "m", None),
    ("10.130.2010", "Tesisat", "Boru", "PVC Pis Su Borusu Ø50", "m", None),
    ("10.130.2011", "Tesisat", "Boru", "PVC Pis Su Borusu Ø75", "m", None),
    ("10.130.2012", "Tesisat", "Boru", "PVC Pis Su Borusu Ø100", "m", None),
    ("10.130.2013", "Tesisat", "Boru", "PVC Pis Su Borusu Ø125", "m", None),
    ("10.130.2020", "Tesisat", "Elektrik", "NYM Kablo 3x1.5 mm²", "m", None),
    ("10.130.2021", "Tesisat", "Elektrik", "NYM Kablo 3x2.5 mm²", "m", None),
    ("10.130.2022", "Tesisat", "Elektrik", "NYM Kablo 5x2.5 mm²", "m", None),
    ("10.130.2030", "Tesisat", "Elektrik", "Plastik Spiral Boru Ø16", "m", None),
    ("10.130.2031", "Tesisat", "Elektrik", "Plastik Spiral Boru Ø20", "m", None),
    # MANTOLAMA / DIŞ CEPHE
    ("10.130.2101", "Dış Cephe", "Mantolama", "Mantolama File (160 gr/m²)", "m²", None),
    ("10.130.2102", "Dış Cephe", "Mantolama", "Mantolama Dübeli (10x120 mm)", "adet", None),
    ("10.130.2103", "Dış Cephe", "Mantolama", "Köşe Profili (PVC, fileli)", "m", None),
    ("10.130.2104", "Dış Cephe", "Mantolama", "Denizlik Profili (alüminyum)", "m", None),
    # DİĞER
    ("10.130.2201", "Diğer", "Dolgu", "Grobeton (C8/10)", "m³", None),
    ("10.130.2202", "Diğer", "Dolgu", "Stabilize Malzeme", "m³", None),
    ("10.130.2203", "Diğer", "İskele", "Cephe İskelesi (boru iskele, kiralık)", "m²", "Aylık kira"),
    ("10.130.2204", "Diğer", "Güvenlik", "Güvenlik Filesi", "m²", None),
    ("10.130.2205", "Diğer", "Güvenlik", "Güvenlik Ağı", "m²", None),
]

# ─── İş Kalemi Katalogu ──────────────────────────────────────────────────────
# (poz_no, grup, alt_grup, ad, birim)
IS_KALEMI_KATALOG_DATA = [
    # HAFRIYAT
    ("14.001", "Hafriyat", "Kazı", "Her derinlikte makine ile yumuşak ve sert toprak kazılması", "m³"),
    ("14.002", "Hafriyat", "Kazı", "Her derinlikte makine ile küskülük kazılması", "m³"),
    ("14.003", "Hafriyat", "Kazı", "Her derinlikte makine ile kaya kazılması", "m³"),
    ("14.010", "Hafriyat", "Dolgu", "Makine ile her mesafeden toprak taşınması", "m³"),
    ("14.011", "Hafriyat", "Dolgu", "Sıkıştırılmış temel dolgusu yapılması", "m³"),
    ("14.012", "Hafriyat", "Dolgu", "Grobeton (C8/10) ile dolgu yapılması", "m³"),
    # BETON İŞLERİ
    ("16.001/1", "Beton İşleri", "Döküm", "C16/20 Hazır Beton Dökülmesi (Beton Pompasıyla)", "m³"),
    ("16.002/1", "Beton İşleri", "Döküm", "C20/25 Hazır Beton Dökülmesi (Beton Pompasıyla)", "m³"),
    ("16.003/1", "Beton İşleri", "Döküm", "C25/30 Hazır Beton Dökülmesi (Beton Pompasıyla)", "m³"),
    ("16.004/1", "Beton İşleri", "Döküm", "C30/37 Hazır Beton Dökülmesi (Beton Pompasıyla)", "m³"),
    ("16.005/1", "Beton İşleri", "Döküm", "C35/45 Hazır Beton Dökülmesi (Beton Pompasıyla)", "m³"),
    ("16.050", "Beton İşleri", "Kalıp", "Düz Yüzeyli Beton ve Betonarme Kalıbı", "m²"),
    ("16.051", "Beton İşleri", "Kalıp", "Eğri Yüzeyli Beton ve Betonarme Kalıbı", "m²"),
    ("16.052", "Beton İşleri", "Kalıp", "Plywood ile Düz Yüzeyli Kalıp", "m²"),
    ("16.053", "Beton İşleri", "Kalıp", "Çelik Panel Kalıp ile Düz Yüzeyli Kalıp", "m²"),
    ("16.054", "Beton İşleri", "Kalıp", "Tünel Kalıp ile Betonarme Yapı", "m²"),
    ("16.070", "Beton İşleri", "Donatı", "Nervürlü Çelik Çubuğu (Ø8-Ø12) Bükülmesi ve Yerine Konulması", "ton"),
    ("16.071", "Beton İşleri", "Donatı", "Nervürlü Çelik Çubuğu (Ø14-Ø28) Bükülmesi ve Yerine Konulması", "ton"),
    ("16.072", "Beton İşleri", "Donatı", "Nervürlü Çelik Çubuğu (Ø32 ve üzeri) Bükülmesi ve Yerine Konulması", "ton"),
    ("16.073", "Beton İşleri", "Donatı", "Çelik Hasır Serilmesi", "ton"),
    # DUVAR İŞLERİ
    ("18.001", "Duvar İşleri", "Tuğla", "Yatay Delikli Tuğla ile Duvar (8.5 cm)", "m²"),
    ("18.002", "Duvar İşleri", "Tuğla", "Yatay Delikli Tuğla ile Duvar (13.5 cm)", "m²"),
    ("18.003", "Duvar İşleri", "Tuğla", "Yatay Delikli Tuğla ile Duvar (19 cm)", "m²"),
    ("18.010", "Duvar İşleri", "Gazbeton", "Gazbeton ile Duvar Yapılması (10 cm)", "m²"),
    ("18.011", "Duvar İşleri", "Gazbeton", "Gazbeton ile Duvar Yapılması (15 cm)", "m²"),
    ("18.012", "Duvar İşleri", "Gazbeton", "Gazbeton ile Duvar Yapılması (20 cm)", "m²"),
    ("18.013", "Duvar İşleri", "Gazbeton", "Gazbeton ile Duvar Yapılması (25 cm)", "m²"),
    ("18.020", "Duvar İşleri", "Bims", "Bims Blok ile Duvar Yapılması (20 cm)", "m²"),
    # SIVA İŞLERİ
    ("19.001", "Sıva İşleri", "İç Sıva", "Çimento Esaslı İç Sıva (hazır harç)", "m²"),
    ("19.002", "Sıva İşleri", "İç Sıva", "Alçı Esaslı Makine Sıvası", "m²"),
    ("19.003", "Sıva İşleri", "Dış Sıva", "Çimento Esaslı Dış Sıva (hazır harç)", "m²"),
    ("19.010", "Sıva İşleri", "Şap", "Şap Yapılması (3 cm)", "m²"),
    ("19.011", "Sıva İşleri", "Şap", "Şap Yapılması (5 cm)", "m²"),
    ("19.020", "Sıva İşleri", "Derz", "Seramik Arası Derz Dolgusu", "m²"),
    # KAPLAMA İŞLERİ
    ("20.001", "Kaplama", "Seramik", "Yer Seramiği Döşenmesi (yapıştırıcı ile)", "m²"),
    ("20.002", "Kaplama", "Seramik", "Duvar Seramiği Yapıştırılması", "m²"),
    ("20.003", "Kaplama", "Seramik", "Granit Yer Kaplaması Yapılması", "m²"),
    ("20.010", "Kaplama", "Mermer", "Mermer Yer Kaplaması Yapılması", "m²"),
    ("20.011", "Kaplama", "Mermer", "Mermer Denizlik Yapılması", "m"),
    ("20.020", "Kaplama", "Parke", "Laminat Parke Döşenmesi", "m²"),
    ("20.021", "Kaplama", "Parke", "Masif Parke Döşenmesi", "m²"),
    # BOYA İŞLERİ
    ("21.001", "Boya", "İç", "İç Cephe Boyası Yapılması (plastik, 2 kat)", "m²"),
    ("21.002", "Boya", "İç", "İç Cephe Boyası Yapılması (silikonlu, 2 kat)", "m²"),
    ("21.003", "Boya", "Dış", "Dış Cephe Boyası Yapılması (silikonlu, 2 kat)", "m²"),
    ("21.010", "Boya", "Astar", "Astar Sürülmesi (iç cephe)", "m²"),
    ("21.011", "Boya", "Metal", "Antipas + Sentetik Boya (2 kat)", "m²"),
    # YALITIM İŞLERİ
    ("22.001", "Yalıtım", "Isı", "EPS ile Dış Cephe Mantolama (5 cm)", "m²"),
    ("22.002", "Yalıtım", "Isı", "EPS ile Dış Cephe Mantolama (8 cm)", "m²"),
    ("22.003", "Yalıtım", "Isı", "EPS ile Dış Cephe Mantolama (10 cm)", "m²"),
    ("22.010", "Yalıtım", "Isı", "XPS ile Temel Perdesi Yalıtımı (5 cm)", "m²"),
    ("22.011", "Yalıtım", "Isı", "XPS ile Teras/Çatı Yalıtımı (5 cm)", "m²"),
    ("22.020", "Yalıtım", "Su", "Bitümlü Membran ile Su Yalıtımı (3 mm, çift kat)", "m²"),
    ("22.021", "Yalıtım", "Su", "Bitümlü Membran ile Su Yalıtımı (4 mm, tek kat)", "m²"),
    ("22.022", "Yalıtım", "Su", "Çimento Esaslı Su Yalıtımı (sürme, 2 kat)", "m²"),
    ("22.030", "Yalıtım", "Ses", "Döşemede Ses Yalıtım Keçesi Serilmesi", "m²"),
    # DOĞRAMA İŞLERİ
    ("23.001", "Doğrama", "PVC Pencere", "PVC Pencere Takılması (5 odacık, ısıcamlı)", "m²"),
    ("23.002", "Doğrama", "PVC Pencere", "PVC Pencere Takılması (7 odacık, Low-E ısıcamlı)", "m²"),
    ("23.010", "Doğrama", "Alüminyum", "Alüminyum Doğrama Takılması (ısı yalıtımlı)", "m²"),
    ("23.020", "Doğrama", "İç Kapı", "Lake İç Kapı Takılması (kasalı)", "adet"),
    ("23.021", "Doğrama", "Dış Kapı", "Çelik Kapı Takılması", "adet"),
    ("23.022", "Doğrama", "Yangın", "Yangın Kapısı Takılması (90 dk)", "adet"),
    # ÇATI İŞLERİ
    ("24.001", "Çatı", "Ahşap", "Ahşap Çatı Makası Yapılması", "m²"),
    ("24.002", "Çatı", "Örtü", "Kiremit ile Çatı Örtüsü", "m²"),
    ("24.003", "Çatı", "Örtü", "Membran Çatı Örtüsü (PVC, mekanik tespit)", "m²"),
    ("24.010", "Çatı", "Yağmur Suyu", "PVC Yağmur Oluğu (Ø120)", "m"),
    ("24.011", "Çatı", "Yağmur Suyu", "PVC Yağmur İniş Borusu (Ø100)", "m"),
    # İSKELE İŞLERİ
    ("15.001", "İskele", "Dış Cephe", "Boru İskele Kurulması ve Sökülmesi", "m²"),
    ("15.002", "İskele", "Dış Cephe", "Ön Yapımlı Cephe İskelesi (3-51 m)", "m²"),
    # TESİSAT İŞLERİ
    ("27.001", "Tesisat", "Temiz Su", "PPR Boru Döşenmesi (Ø20)", "m"),
    ("27.002", "Tesisat", "Temiz Su", "PPR Boru Döşenmesi (Ø25)", "m"),
    ("27.003", "Tesisat", "Temiz Su", "PPR Boru Döşenmesi (Ø32)", "m"),
    ("27.010", "Tesisat", "Pis Su", "PVC Atık Su Borusu Döşenmesi (Ø50)", "m"),
    ("27.011", "Tesisat", "Pis Su", "PVC Atık Su Borusu Döşenmesi (Ø75)", "m"),
    ("27.012", "Tesisat", "Pis Su", "PVC Atık Su Borusu Döşenmesi (Ø100)", "m"),
    ("27.013", "Tesisat", "Pis Su", "PVC Atık Su Borusu Döşenmesi (Ø125)", "m"),
    ("27.050", "Tesisat", "Elektrik", "NYM Kablo Çekilmesi (3x1.5 mm²)", "m"),
    ("27.051", "Tesisat", "Elektrik", "NYM Kablo Çekilmesi (3x2.5 mm²)", "m"),
    ("27.052", "Tesisat", "Elektrik", "NYM Kablo Çekilmesi (5x2.5 mm²)", "m"),
    ("27.060", "Tesisat", "Elektrik", "Plastik Spiral Boru Döşenmesi (Ø16)", "m"),
    ("27.061", "Tesisat", "Elektrik", "Plastik Spiral Boru Döşenmesi (Ø20)", "m"),
]

# ─── İş Kalemi ↔ Malzeme İlişki Data ────────────────────────────────────────
# (is_kalemi_poz, malzeme_poz, miktar, birim, zorunlu, aciklama)
IS_KALEMI_MALZEME_DATA = [
    # ── Hafriyat ──
    # 14.011 - Temel dolgusu
    ("14.011", "10.130.2202", 1.30, "m³", 1, "fire ve sıkışma payı dahil"),
    # 14.012 - Grobeton dolgu
    ("14.012", "10.130.2201", 1.05, "m³", 1, "fire dahil"),
    ("14.012", "10.130.1341", 0.05, "kg", 0, "gerekirse çivi"),

    # ── Beton İşleri: Döküm ──
    # 16.001/1 - C16/20
    ("16.001/1", "10.130.1200", 1.03, "m³", 1, "fire dahil"),
    ("16.001/1", "10.130.1340", 0.3,  "kg", 0, "bağ teli (donatı varsa)"),
    # 16.002/1 - C20/25
    ("16.002/1", "10.130.1201", 1.03, "m³", 1, "fire dahil"),
    ("16.002/1", "10.130.1340", 0.3,  "kg", 0, "bağ teli (donatı varsa)"),
    # 16.003/1 - C25/30
    ("16.003/1", "10.130.1202", 1.03, "m³", 1, "fire dahil"),
    ("16.003/1", "10.130.1340", 0.5,  "kg", 1, "bağlama teli"),
    # 16.004/1 - C30/37
    ("16.004/1", "10.130.1203", 1.03, "m³", 1, "fire dahil"),
    ("16.004/1", "10.130.1340", 0.5,  "kg", 1, "bağlama teli"),
    # 16.005/1 - C35/45
    ("16.005/1", "10.130.1204", 1.03, "m³", 1, "fire dahil"),
    ("16.005/1", "10.130.1340", 0.5,  "kg", 1, "bağlama teli"),

    # ── Beton İşleri: Kalıp ──
    # 16.050 - Düz kalıp (ahşap)
    ("16.050", "10.130.1401", 0.015, "m³", 1, "2.5 cm kalıp tahtası"),
    ("16.050", "10.130.1404", 0.005, "m³", 1, "kadron"),
    ("16.050", "10.130.1341", 0.15,  "kg", 1, "çivi"),
    # 16.051 - Eğri yüzeyli kalıp
    ("16.051", "10.130.1401", 0.020, "m³", 1, "2.5 cm kalıp tahtası, daha fazla kesim"),
    ("16.051", "10.130.1404", 0.008, "m³", 1, "kadron"),
    ("16.051", "10.130.1341", 0.25,  "kg", 1, "çivi"),
    # 16.052 - Plywood kalıp
    ("16.052", "10.130.1411", 1.05, "m²", 1, "fire dahil"),
    ("16.052", "10.130.1404", 0.004, "m³", 1, "kadron ve takviye"),
    # 16.053 - Çelik panel kalıp
    ("16.053", "10.130.1420", 1.0,  "m²", 1, "günlük kira"),
    ("16.053", "10.130.1341", 0.05, "kg", 1, "bağlantı çivisi"),
    # 16.054 - Tünel kalıp
    ("16.054", "10.130.1421", 1.0,  "m²", 1, "günlük kira"),

    # ── Beton İşleri: Donatı ──
    # 16.070 - Ø8-12
    ("16.070", "10.130.1301", 0.40, "ton", 0, "Ø8 kullanılırsa"),
    ("16.070", "10.130.1302", 0.30, "ton", 0, "Ø10 kullanılırsa"),
    ("16.070", "10.130.1303", 0.30, "ton", 0, "Ø12 kullanılırsa"),
    ("16.070", "10.130.1340", 15.0, "kg",  1, "bağlama teli"),
    # 16.071 - Ø14-28
    ("16.071", "10.130.1304", 0.20, "ton", 0, "Ø14 kullanılırsa"),
    ("16.071", "10.130.1305", 0.25, "ton", 0, "Ø16 kullanılırsa"),
    ("16.071", "10.130.1306", 0.20, "ton", 0, "Ø18 kullanılırsa"),
    ("16.071", "10.130.1307", 0.20, "ton", 0, "Ø20 kullanılırsa"),
    ("16.071", "10.130.1309", 0.15, "ton", 0, "Ø25 kullanılırsa"),
    ("16.071", "10.130.1340", 12.0, "kg",  1, "bağlama teli"),
    # 16.072 - Ø32+
    ("16.072", "10.130.1311", 1.00, "ton", 1, "Ø32 nervürlü demir"),
    ("16.072", "10.130.1340", 10.0, "kg",  1, "bağlama teli"),
    # 16.073 - Çelik hasır
    ("16.073", "10.130.1320", 0.25, "ton", 0, "Q131 hasır"),
    ("16.073", "10.130.1321", 0.30, "ton", 0, "Q188 hasır"),
    ("16.073", "10.130.1322", 0.25, "ton", 0, "Q221 hasır"),
    ("16.073", "10.130.1323", 0.20, "ton", 0, "Q335 hasır"),
    ("16.073", "10.130.1340", 8.0,  "kg",  1, "bağlama teli"),

    # ── Duvar İşleri ──
    # 18.001 - Tuğla 8.5 cm
    ("18.001", "10.130.1601", 40,    "adet", 1, "fire dahil"),
    ("18.001", "10.130.1103", 0.008, "ton",  1, "harç çimentosu"),
    ("18.001", "10.130.1005", 0.010, "m³",   1, "harç kumu"),
    # 18.002 - Tuğla 13.5 cm
    ("18.002", "10.130.1602", 28,    "adet", 1, "fire dahil"),
    ("18.002", "10.130.1101", 0.012, "ton",  1, "harç çimentosu"),
    ("18.002", "10.130.1005", 0.015, "m³",   1, "harç kumu"),
    # 18.003 - Tuğla 19 cm
    ("18.003", "10.130.1603", 22,    "adet", 1, "fire dahil"),
    ("18.003", "10.130.1101", 0.016, "ton",  1, "harç çimentosu"),
    ("18.003", "10.130.1005", 0.020, "m³",   1, "harç kumu"),
    # 18.010 - Gazbeton 10 cm
    ("18.010", "10.130.1610", 0.12, "m³", 1, "fire dahil"),
    ("18.010", "10.130.1712", 3.5,  "kg", 1, "gazbeton yapıştırıcısı"),
    # 18.011 - Gazbeton 15 cm
    ("18.011", "10.130.1611", 0.17, "m³", 1, "fire dahil"),
    ("18.011", "10.130.1712", 4.5,  "kg", 1, "gazbeton yapıştırıcısı"),
    # 18.012 - Gazbeton 20 cm
    ("18.012", "10.130.1612", 0.22, "m³", 1, "fire dahil"),
    ("18.012", "10.130.1712", 5.5,  "kg", 1, "gazbeton yapıştırıcısı"),
    # 18.013 - Gazbeton 25 cm
    ("18.013", "10.130.1613", 0.27, "m³", 1, "fire dahil"),
    ("18.013", "10.130.1712", 6.5,  "kg", 1, "gazbeton yapıştırıcısı"),
    # 18.020 - Bims 20 cm
    ("18.020", "10.130.1620", 32,    "adet", 1, "fire dahil"),
    ("18.020", "10.130.1103", 0.014, "ton",  1, "harç çimentosu"),
    ("18.020", "10.130.1005", 0.018, "m³",   1, "harç kumu"),

    # ── Sıva İşleri ──
    # 19.001 - İç sıva (çimento esaslı hazır)
    ("19.001", "10.130.1701", 14.0, "kg", 1, "~1.4 kg/m²/mm, 10mm sıva"),
    # 19.002 - Alçı makine sıvası
    ("19.002", "10.130.1703", 12.0, "kg", 1, "~12 kg/m² (10mm)"),
    ("19.002", "10.130.1121", 0.3,  "kg", 0, "son kat saten gerekirse"),
    # 19.003 - Dış sıva
    ("19.003", "10.130.1702", 16.0, "kg", 1, "~1.6 kg/m²/mm, 10mm dış sıva"),
    # 19.010 - Şap 3 cm
    ("19.010", "10.130.1215", 0.033, "m³", 1, "3 cm şap betonu"),
    # 19.011 - Şap 5 cm
    ("19.011", "10.130.1215", 0.055, "m³", 1, "5 cm şap betonu"),
    # 19.020 - Derz dolgu
    ("19.020", "10.130.1720", 0.4,  "kg", 1, "iç mekan derz dolgusu"),

    # ── Kaplama İşleri ──
    # 20.001 - Yer seramiği (40x40)
    ("20.001", "10.130.1802", 1.05, "m²", 1, "40x40 seramik, fire dahil"),
    ("20.001", "10.130.1710", 4.5,  "kg", 1, "yapıştırıcı"),
    ("20.001", "10.130.1720", 0.3,  "kg", 1, "derz dolgu"),
    # 20.002 - Duvar seramiği
    ("20.002", "10.130.1804", 1.05, "m²", 1, "25x40 duvar seramiği, fire dahil"),
    ("20.002", "10.130.1710", 4.0,  "kg", 1, "yapıştırıcı"),
    ("20.002", "10.130.1720", 0.3,  "kg", 1, "derz dolgu"),
    # 20.003 - Granit yer
    ("20.003", "10.130.1810", 1.03, "m²", 1, "granit 2cm, fire dahil"),
    ("20.003", "10.130.1711", 5.0,  "kg", 1, "esnek yapıştırıcı"),
    ("20.003", "10.130.1721", 0.4,  "kg", 1, "dış mekan derz dolgusu"),
    # 20.010 - Mermer yer
    ("20.010", "10.130.1811", 1.03, "m²", 1, "mermer 2cm, fire dahil"),
    ("20.010", "10.130.1710", 5.0,  "kg", 1, "yapıştırıcı"),
    ("20.010", "10.130.1720", 0.3,  "kg", 1, "derz dolgu"),
    # 20.011 - Mermer denizlik
    ("20.011", "10.130.1812", 1.05, "m",  1, "fire dahil"),
    ("20.011", "10.130.1710", 0.8,  "kg", 1, "yapıştırıcı"),
    # 20.020 - Laminat parke
    ("20.020", "10.130.1820", 1.08, "m²", 1, "AC4 laminat, fire dahil"),
    ("20.020", "10.130.1532", 1.10, "m²", 1, "nem bariyeri altpas"),
    # 20.021 - Masif parke
    ("20.021", "10.130.1822", 1.08, "m²", 1, "meşe masif, fire dahil"),
    ("20.021", "10.130.1532", 1.10, "m²", 1, "nem bariyeri"),

    # ── Boya İşleri ──
    # 21.001 - İç boya plastik
    ("21.001", "10.130.1730", 0.25, "lt", 1, "2 kat toplam tüketim"),
    ("21.001", "10.130.1734", 0.10, "lt", 1, "astar 1 kat"),
    ("21.001", "10.130.1121", 0.50, "kg", 0, "saten macun gerekirse"),
    # 21.002 - İç boya silikonlu
    ("21.002", "10.130.1731", 0.25, "lt", 1, "2 kat toplam tüketim"),
    ("21.002", "10.130.1734", 0.10, "lt", 1, "astar"),
    ("21.002", "10.130.1121", 0.50, "kg", 0, "saten macun gerekirse"),
    # 21.003 - Dış boya silikonlu
    ("21.003", "10.130.1732", 0.30, "lt", 1, "2 kat dış cephe boyası"),
    ("21.003", "10.130.1734", 0.12, "lt", 1, "dış cephe astar"),
    # 21.010 - Astar
    ("21.010", "10.130.1734", 0.12, "lt", 1, "1 kat astar"),
    # 21.011 - Antipas + sentetik boya
    ("21.011", "10.130.1733", 0.15, "lt", 1, "antipas astar 1 kat"),
    ("21.011", "10.130.1732", 0.20, "lt", 1, "sentetik boya 2 kat"),

    # ── Yalıtım İşleri ──
    # 22.001 - EPS mantolama 5 cm
    ("22.001", "10.130.1503", 1.05, "m²", 1, "EPS 5cm, fire dahil"),
    ("22.001", "10.130.1713", 5.0,  "kg", 1, "yapıştırma + sıvalama"),
    ("22.001", "10.130.2101", 1.15, "m²", 1, "bindirmeli file"),
    ("22.001", "10.130.2102", 6,    "adet",1, "dübel"),
    ("22.001", "10.130.1732", 0.35, "lt", 1, "son kat boya"),
    ("22.001", "10.130.1734", 0.15, "lt", 1, "astar"),
    # 22.002 - EPS mantolama 8 cm
    ("22.002", "10.130.1504", 1.05, "m²", 1, "EPS 8cm, fire dahil"),
    ("22.002", "10.130.1713", 5.0,  "kg", 1, "yapıştırma + sıvalama"),
    ("22.002", "10.130.2101", 1.15, "m²", 1, "bindirmeli file"),
    ("22.002", "10.130.2102", 6,    "adet",1, "dübel"),
    ("22.002", "10.130.1732", 0.35, "lt", 1, "son kat boya"),
    ("22.002", "10.130.1734", 0.15, "lt", 1, "astar"),
    # 22.003 - EPS mantolama 10 cm
    ("22.003", "10.130.1505", 1.05, "m²", 1, "EPS 10cm, fire dahil"),
    ("22.003", "10.130.1713", 5.0,  "kg", 1, "yapıştırma + sıvalama"),
    ("22.003", "10.130.2101", 1.15, "m²", 1, "bindirmeli file"),
    ("22.003", "10.130.2102", 6,    "adet",1, "dübel"),
    ("22.003", "10.130.1732", 0.35, "lt", 1, "son kat boya"),
    ("22.003", "10.130.1734", 0.15, "lt", 1, "astar"),
    # 22.010 - XPS temel perdesi 5 cm
    ("22.010", "10.130.1511", 1.05, "m²", 1, "XPS 5cm, fire dahil"),
    ("22.010", "10.130.2102", 4,    "adet",1, "dübel"),
    # 22.011 - XPS teras/çatı 5 cm
    ("22.011", "10.130.1511", 1.05, "m²", 1, "XPS 5cm, fire dahil"),
    ("22.011", "10.130.2102", 4,    "adet",1, "dübel"),
    # 22.020 - Membran 3+4mm çift kat
    ("22.020", "10.130.1530", 1.10, "m²", 1, "1. kat 3mm, bindirme dahil"),
    ("22.020", "10.130.1531", 1.10, "m²", 1, "2. kat 4mm, bindirme dahil"),
    ("22.020", "10.130.1734", 0.30, "lt", 1, "bitüm esaslı astar"),
    # 22.021 - Membran 4mm tek kat
    ("22.021", "10.130.1531", 1.10, "m²", 1, "4mm membran, bindirme dahil"),
    ("22.021", "10.130.1734", 0.25, "lt", 1, "astar"),
    # 22.022 - Çimento esaslı su yalıtımı
    ("22.022", "10.130.1533", 3.0,  "kg", 1, "2 kat uygulama"),
    ("22.022", "10.130.1734", 0.15, "lt", 1, "astar"),
    # 22.030 - Ses yalıtım keçesi
    ("22.030", "10.130.1540", 1.05, "m²", 1, "fire dahil"),

    # ── Doğrama İşleri ──
    # 23.001 - PVC pencere 5 odacık + ısıcam
    ("23.001", "10.130.1901", 1.0,  "m²", 1, "PVC 5 odacık profil"),
    ("23.001", "10.130.1921", 1.0,  "m²", 1, "ısıcam 4+12+4"),
    # 23.002 - PVC pencere 7 odacık + Low-E
    ("23.002", "10.130.1902", 1.0,  "m²", 1, "PVC 7 odacık profil"),
    ("23.002", "10.130.1922", 1.0,  "m²", 1, "low-e ısıcam"),
    # 23.010 - Alüminyum doğrama
    ("23.010", "10.130.1910", 1.0,  "m²", 1, "ısı yalıtımlı alüminyum"),
    ("23.010", "10.130.1921", 1.0,  "m²", 1, "ısıcam"),
    # 23.020 - Lake iç kapı
    ("23.020", "10.130.1930", 1,    "adet",1, "kasalı lake iç kapı"),
    # 23.021 - Çelik dış kapı
    ("23.021", "10.130.1931", 1,    "adet",1, "çelik dış kapı"),
    # 23.022 - Yangın kapısı
    ("23.022", "10.130.1932", 1,    "adet",1, "90 dk yangın kapısı"),

    # ── Çatı İşleri ──
    # 24.001 - Ahşap çatı makası
    ("24.001", "10.130.1403", 0.018, "m³", 1, "kereste m² başına"),
    ("24.001", "10.130.1404", 0.005, "m³", 1, "kadron"),
    ("24.001", "10.130.1341", 0.20,  "kg", 1, "çivi"),
    # 24.002 - Kiremit çatı (membran alt örtü dahil)
    ("24.002", "10.130.1403", 0.012, "m³", 0, "tahta mıhlatma"),
    ("24.002", "10.130.1530", 1.10,  "m²", 1, "alt su yalıtım örtüsü"),
    # 24.003 - Membran çatı PVC
    ("24.003", "10.130.1511", 1.05,  "m²", 1, "XPS ısı yalıtımı alt tabaka"),
    ("24.003", "10.130.1531", 1.10,  "m²", 1, "membran örtü"),
    # 24.010 - PVC yağmur oluğu: boru yok, standart malzeme listede değil
    ("24.010", "10.130.2010", 1.05,  "m",  0, "alternatif PVC boru Ø50 (yaklaşık)"),
    # 24.011 - PVC iniş borusu
    ("24.011", "10.130.2012", 1.05,  "m",  1, "PVC boru Ø100, fire dahil"),

    # ── İskele ──
    # 15.001 - Boru iskele
    ("15.001", "10.130.2203", 1.0,  "m²", 1, "aylık kira, iskele m² başına"),
    ("15.001", "10.130.2204", 1.0,  "m²", 1, "güvenlik filesi"),
    # 15.002 - Ön yapımlı cephe iskelesi
    ("15.002", "10.130.2203", 1.0,  "m²", 1, "aylık kira"),
    ("15.002", "10.130.2205", 1.0,  "m²", 1, "güvenlik ağı"),

    # ── Tesisat: Temiz Su ──
    # 27.001 - PPR Ø20
    ("27.001", "10.130.2001", 1.05, "m", 1, "fire dahil"),
    # 27.002 - PPR Ø25
    ("27.002", "10.130.2002", 1.05, "m", 1, "fire dahil"),
    # 27.003 - PPR Ø32
    ("27.003", "10.130.2003", 1.05, "m", 1, "fire dahil"),

    # ── Tesisat: Pis Su ──
    # 27.010 - PVC Ø50
    ("27.010", "10.130.2010", 1.05, "m", 1, "fire dahil"),
    # 27.011 - PVC Ø75
    ("27.011", "10.130.2011", 1.05, "m", 1, "fire dahil"),
    # 27.012 - PVC Ø100
    ("27.012", "10.130.2012", 1.05, "m", 1, "fire dahil"),
    # 27.013 - PVC Ø125
    ("27.013", "10.130.2013", 1.05, "m", 1, "fire dahil"),

    # ── Tesisat: Elektrik ──
    # 27.050 - NYM 3x1.5
    ("27.050", "10.130.2020", 1.05, "m", 1, "fire dahil"),
    ("27.050", "10.130.2030", 1.05, "m", 1, "spiral Ø16 boru"),
    # 27.051 - NYM 3x2.5
    ("27.051", "10.130.2021", 1.05, "m", 1, "fire dahil"),
    ("27.051", "10.130.2030", 1.05, "m", 1, "spiral Ø16 boru"),
    # 27.052 - NYM 5x2.5
    ("27.052", "10.130.2022", 1.05, "m", 1, "fire dahil"),
    ("27.052", "10.130.2031", 1.05, "m", 1, "spiral Ø20 boru"),
    # 27.060 - Spiral Ø16
    ("27.060", "10.130.2030", 1.05, "m", 1, "fire dahil"),
    # 27.061 - Spiral Ø20
    ("27.061", "10.130.2031", 1.05, "m", 1, "fire dahil"),
]


def seed_csb_katalog(engine) -> None:
    """
    CSB katalog seed. Malzeme verileri artık birleşik 'malzemeler' tablosunda;
    csb_is_kalemi_katalog ve csb_is_kalemi_malzeme tabloları doldurulur.
    İdempotent: zaten veri varsa tekrar eklemez.
    """
    import sqlite3 as _sqlite3
    import pathlib as _pathlib

    db_url = str(engine.url)
    if "sqlite" not in db_url:
        logger.info("CSB katalog seed yalnızca SQLite için; atlanıyor.")
        return

    db_path = db_url.replace("sqlite:///", "").replace("sqlite://", "")
    if db_path.startswith("./"):
        db_path = str(_pathlib.Path(__file__).parent / db_path[2:])

    try:
        con = _sqlite3.connect(db_path)
        con.execute("PRAGMA journal_mode=WAL")

        # ── 1. Malzeme verileri → birleşik malzemeler tablosu ──
        # csb_malzeme_katalog kaldırıldı; CSB malzemeleri poz_no dolu olarak malzemeler'de.
        csb_count = con.execute(
            "SELECT COUNT(*) FROM malzemeler WHERE poz_no IS NOT NULL AND aktif=1"
        ).fetchone()[0]
        if csb_count == 0:
            con.executemany(
                "INSERT OR IGNORE INTO malzemeler "
                "(poz_no, kategori, alt_kategori, ad, birim, aciklama, aktif, scrape_tipi) "
                "VALUES (?,?,?,?,?,?,1,'csb_katalog')",
                MALZEME_KATALOG_DATA,
            )
            logger.info("CSB malzeme seed (malzemeler tablosu): %d kayıt eklendi.", len(MALZEME_KATALOG_DATA))

        # ── 2. İş kalemi katalogu ──
        row = con.execute("SELECT COUNT(*) FROM csb_is_kalemi_katalog").fetchone()
        if row[0] == 0:
            con.executemany(
                "INSERT OR IGNORE INTO csb_is_kalemi_katalog "
                "(poz_no, grup, alt_grup, ad, birim, aktif) "
                "VALUES (?,?,?,?,?,1)",
                IS_KALEMI_KATALOG_DATA,
            )
            logger.info("CSB iş kalemi katalogu seed: %d kayıt eklendi.", len(IS_KALEMI_KATALOG_DATA))

        # ── 3. İlişki tablosu — malzeme_katalog_id artık malzemeler.id'ye işaret eder ──
        row = con.execute("SELECT COUNT(*) FROM csb_is_kalemi_malzeme").fetchone()
        if row[0] == 0:
            # poz_no → malzemeler.id (CSB malzemeleri poz_no ile aranır)
            malzeme_map = {
                r[0]: r[1]
                for r in con.execute(
                    "SELECT poz_no, id FROM malzemeler WHERE poz_no IS NOT NULL"
                )
            }
            is_kalemi_map = {
                r[0]: r[1]
                for r in con.execute("SELECT poz_no, id FROM csb_is_kalemi_katalog")
            }

            rows = []
            for ik_poz, m_poz, miktar, birim, zorunlu, aciklama in IS_KALEMI_MALZEME_DATA:
                ik_id = is_kalemi_map.get(ik_poz)
                m_id  = malzeme_map.get(m_poz)
                if ik_id is None or m_id is None:
                    logger.warning(
                        "CSB ilişki seed: poz bulunamadı ik=%s m=%s", ik_poz, m_poz
                    )
                    continue
                rows.append((ik_id, m_id, miktar, birim, zorunlu, aciklama))

            con.executemany(
                "INSERT OR IGNORE INTO csb_is_kalemi_malzeme "
                "(is_kalemi_katalog_id, malzeme_katalog_id, miktar, birim, zorunlu, aciklama) "
                "VALUES (?,?,?,?,?,?)",
                rows,
            )
            logger.info("CSB ilişki tablosu seed: %d kayıt eklendi.", len(rows))

        con.commit()
        con.close()

    except Exception:
        logger.exception("CSB katalog seed başarısız")
