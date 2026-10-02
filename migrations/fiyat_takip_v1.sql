-- =============================================================
-- migrations/fiyat_takip_v1.sql
-- Fiyat Takip Modülü – Faz 1 şema ve seed data
-- =============================================================

PRAGMA journal_mode=WAL;

-- =============================================================
-- TABLOLAR
-- =============================================================

-- 1. referans_merkezler
CREATE TABLE IF NOT EXISTS referans_merkezler (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    kod                TEXT    NOT NULL UNIQUE,   -- 'istanbul', 'gebze', …
    ad                 TEXT    NOT NULL,
    sehir              TEXT    NOT NULL,
    aktif              INTEGER NOT NULL DEFAULT 1,
    olusturma_tarihi   TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- 2. il_eslestirme
CREATE TABLE IF NOT EXISTS il_eslestirme (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    il_adi              TEXT    NOT NULL UNIQUE,
    plaka_kodu          INTEGER NOT NULL,
    referans_merkez_id  INTEGER NOT NULL,
    mesafe_km           REAL    NOT NULL,
    FOREIGN KEY (referans_merkez_id) REFERENCES referans_merkezler(id)
);

-- 3. malzemeler
CREATE TABLE IF NOT EXISTS malzemeler (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    kategori           TEXT    NOT NULL,   -- 'demir','celik_hasir','filmasin','cimento','beton','kum','gazbeton','tugla'
    alt_kategori       TEXT,
    ad                 TEXT    NOT NULL,
    birim              TEXT    NOT NULL,   -- 'ton','m3','torba','adet'
    scrape_tipi        TEXT    NOT NULL,   -- 'proemtia_endeks','proemtia_urun'
    aktif              INTEGER NOT NULL DEFAULT 1,
    olusturma_tarihi   TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE (kategori, ad)
);

-- 4. scrape_fiyatlar
CREATE TABLE IF NOT EXISTS scrape_fiyatlar (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    malzeme_id          INTEGER NOT NULL,
    referans_merkez_id  INTEGER,             -- NULL = ulusal / endeks fiyatı
    fiyat               REAL    NOT NULL,
    kdv_dahil           INTEGER NOT NULL DEFAULT 0,
    tarih               TEXT    NOT NULL,
    kaynak              TEXT    NOT NULL,
    kaynak_url          TEXT,
    olusturma_tarihi    TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (malzeme_id)         REFERENCES malzemeler(id),
    FOREIGN KEY (referans_merkez_id) REFERENCES referans_merkezler(id)
);

-- 5. kullanici_fiyatlar
CREATE TABLE IF NOT EXISTS kullanici_fiyatlar (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_id       INTEGER NOT NULL,
    malzeme_id         INTEGER NOT NULL,
    proje_id           INTEGER,
    fiyat              REAL    NOT NULL,
    miktar             REAL,
    tedarikci          TEXT,
    not_text           TEXT,
    tarih              TEXT    NOT NULL,
    olusturma_tarihi   TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (malzeme_id) REFERENCES malzemeler(id)
);

-- 6. nakliye_katsayilari  (₺/ton/km)
CREATE TABLE IF NOT EXISTS nakliye_katsayilari (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    malzeme_kategori        TEXT    NOT NULL,
    katsayi                 REAL    NOT NULL,
    gecerlilik_baslangic    TEXT    NOT NULL,
    gecerlilik_bitis        TEXT,            -- NULL = hâlâ geçerli
    olusturma_tarihi        TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- =============================================================
-- İNDEKSLER
-- =============================================================

CREATE INDEX IF NOT EXISTS idx_scrape_malzeme_tarih
    ON scrape_fiyatlar (malzeme_id, tarih DESC);

CREATE INDEX IF NOT EXISTS idx_scrape_merkez_tarih
    ON scrape_fiyatlar (referans_merkez_id, tarih DESC);

CREATE INDEX IF NOT EXISTS idx_scrape_tarih
    ON scrape_fiyatlar (tarih DESC);

CREATE INDEX IF NOT EXISTS idx_kullanici_fiyat_kullanici
    ON kullanici_fiyatlar (kullanici_id, tarih DESC);

CREATE INDEX IF NOT EXISTS idx_kullanici_fiyat_malzeme
    ON kullanici_fiyatlar (malzeme_id, tarih DESC);

CREATE INDEX IF NOT EXISTS idx_kullanici_fiyat_proje
    ON kullanici_fiyatlar (proje_id);

-- =============================================================
-- SEED: referans_merkezler
-- =============================================================

INSERT OR IGNORE INTO referans_merkezler (kod, ad, sehir) VALUES
    ('istanbul',         'Proemtia İstanbul',        'İstanbul'),
    ('gebze',            'Proemtia Gebze',            'Kocaeli'),
    ('ankara',           'Proemtia Ankara',           'Ankara'),
    ('biga',             'Proemtia Biga',             'Çanakkale'),
    ('izmir',            'Proemtia İzmir',            'İzmir'),
    ('iskenderun_payas', 'Proemtia İskenderun/Payas', 'Hatay'),
    ('karabuk',          'Proemtia Karabük',          'Karabük');

-- =============================================================
-- SEED: il_eslestirme  (81 il – Bölüm 4.3)
-- =============================================================
-- Mesafeler karayolu km cinsinden, en yakın Proemtia merkezine göredir.

INSERT OR IGNORE INTO il_eslestirme (il_adi, plaka_kodu, referans_merkez_id, mesafe_km) VALUES

-- ── İstanbul bölgesi ──────────────────────────────────────────
('İstanbul',        34, (SELECT id FROM referans_merkezler WHERE kod = 'istanbul'),        0),
('Tekirdağ',        59, (SELECT id FROM referans_merkezler WHERE kod = 'istanbul'),      130),
('Edirne',          22, (SELECT id FROM referans_merkezler WHERE kod = 'istanbul'),      240),
('Kırklareli',      39, (SELECT id FROM referans_merkezler WHERE kod = 'istanbul'),      195),

-- ── Gebze bölgesi ────────────────────────────────────────────
('Kocaeli',         41, (SELECT id FROM referans_merkezler WHERE kod = 'gebze'),          10),
('Sakarya',         54, (SELECT id FROM referans_merkezler WHERE kod = 'gebze'),          70),
('Yalova',          77, (SELECT id FROM referans_merkezler WHERE kod = 'gebze'),          55),
('Bursa',           16, (SELECT id FROM referans_merkezler WHERE kod = 'gebze'),         100),
('Düzce',           81, (SELECT id FROM referans_merkezler WHERE kod = 'gebze'),         115),
('Bilecik',         11, (SELECT id FROM referans_merkezler WHERE kod = 'gebze'),         165),

-- ── Biga bölgesi ─────────────────────────────────────────────
('Çanakkale',       17, (SELECT id FROM referans_merkezler WHERE kod = 'biga'),           55),
('Balıkesir',       10, (SELECT id FROM referans_merkezler WHERE kod = 'biga'),          180),

-- ── İzmir bölgesi ────────────────────────────────────────────
('İzmir',           35, (SELECT id FROM referans_merkezler WHERE kod = 'izmir'),           0),
('Manisa',          45, (SELECT id FROM referans_merkezler WHERE kod = 'izmir'),          45),
('Aydın',            9, (SELECT id FROM referans_merkezler WHERE kod = 'izmir'),          95),
('Muğla',           48, (SELECT id FROM referans_merkezler WHERE kod = 'izmir'),         315),
('Denizli',         20, (SELECT id FROM referans_merkezler WHERE kod = 'izmir'),         250),
('Uşak',            64, (SELECT id FROM referans_merkezler WHERE kod = 'izmir'),         240),
('Afyonkarahisar',   3, (SELECT id FROM referans_merkezler WHERE kod = 'izmir'),         320),
('Kütahya',         43, (SELECT id FROM referans_merkezler WHERE kod = 'izmir'),         275),
('Burdur',          15, (SELECT id FROM referans_merkezler WHERE kod = 'izmir'),         350),
('Isparta',         32, (SELECT id FROM referans_merkezler WHERE kod = 'izmir'),         385),

-- ── Ankara bölgesi ───────────────────────────────────────────
('Ankara',           6, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),          0),
('Kırıkkale',       71, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),         70),
('Çankırı',         18, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),        140),
('Eskişehir',       26, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),        235),
('Kırşehir',        40, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),        185),
('Nevşehir',        50, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),        305),
('Aksaray',         68, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),        210),
('Konya',           42, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),        260),
('Yozgat',          66, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),        225),
('Niğde',           51, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),        340),
('Karaman',         70, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),        365),
('Kayseri',         38, (SELECT id FROM referans_merkezler WHERE kod = 'ankara'),        325),

-- ── Karabük bölgesi ──────────────────────────────────────────
('Karabük',         78, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),         0),
('Bartın',          74, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),        55),
('Zonguldak',       67, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),        95),
('Kastamonu',       37, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       115),
('Bolu',            14, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       130),
('Sinop',           57, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       220),
('Çorum',           19, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       215),
('Amasya',           5, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       270),
('Tokat',           60, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       270),
('Samsun',          55, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       275),
('Ordu',            52, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       335),
('Giresun',         28, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       385),
('Trabzon',         61, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       430),
('Rize',            53, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       470),
('Artvin',           8, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       635),
('Sivas',           58, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       350),
('Gümüşhane',       29, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       435),
('Bayburt',         69, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       455),
('Erzincan',        24, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       580),
('Erzurum',         25, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       730),
('Kars',            36, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       870),
('Ardahan',         75, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       930),
('Iğdır',           76, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       985),
('Ağrı',             4, (SELECT id FROM referans_merkezler WHERE kod = 'karabuk'),       920),

-- ── İskenderun/Payas bölgesi ─────────────────────────────────
('Hatay',           31, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'),  30),
('Adana',            1, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 140),
('Osmaniye',        80, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'),  90),
('Mersin',          33, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 215),
('Antalya',          7, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 520),
('Gaziantep',       27, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 195),
('Kilis',           79, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 215),
('Kahramanmaraş',   46, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 195),
('Adıyaman',         2, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 305),
('Şanlıurfa',       63, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 340),
('Mardin',          47, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 435),
('Batman',          72, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 475),
('Siirt',           56, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 540),
('Şırnak',          73, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 590),
('Diyarbakır',      21, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 420),
('Malatya',         44, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 370),
('Elazığ',          23, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 435),
('Tunceli',         62, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 455),
('Bingöl',          12, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 530),
('Muş',             49, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 660),
('Bitlis',          13, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 710),
('Van',             65, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 890),
('Hakkari',         30, (SELECT id FROM referans_merkezler WHERE kod = 'iskenderun_payas'), 865);

-- =============================================================
-- SEED: malzemeler  (Faz 1)
-- =============================================================

-- Demir
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'demir','nervurlu','Nervürlü Demir Ø8','ton','proemtia_endeks' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Nervürlü Demir Ø8');
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'demir','nervurlu','Nervürlü Demir Ø10','ton','proemtia_endeks' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Nervürlü Demir Ø10');
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'demir','nervurlu','Nervürlü Demir Ø12','ton','proemtia_endeks' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Nervürlü Demir Ø12');
-- Çelik Hasır
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'celik_hasir',NULL,'Çelik Hasır Q131','ton','proemtia_endeks' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Çelik Hasır Q131');
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'celik_hasir',NULL,'Çelik Hasır Q188','ton','proemtia_endeks' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Çelik Hasır Q188');
-- Filmaşin
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'filmasin',NULL,'Filmaşin','ton','proemtia_endeks' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Filmaşin');
-- Çimento
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'cimento','cem1','Akçansa CEM I 42.5','torba','proemtia_urun' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Akçansa CEM I 42.5');
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'cimento','cem2','Bursa Çimento CEM II 42.5R','torba','proemtia_urun' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Bursa Çimento CEM II 42.5R');
-- Hazır Beton
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'beton',NULL,'Hazır Beton C20','m3','proemtia_urun' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Hazır Beton C20');
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'beton',NULL,'Hazır Beton C25','m3','proemtia_urun' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Hazır Beton C25');
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'beton',NULL,'Hazır Beton C30','m3','proemtia_urun' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Hazır Beton C30');
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'beton',NULL,'Hazır Beton C35','m3','proemtia_urun' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Hazır Beton C35');
-- Kum
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'kum',NULL,'Şap Kumu','ton','proemtia_urun' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Şap Kumu');
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'kum',NULL,'Kaba Kum','ton','proemtia_urun' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Kaba Kum');
-- Gazbeton
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'gazbeton',NULL,'Gazbeton Düz Duvar Bloğu','m3','proemtia_urun' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Gazbeton Düz Duvar Bloğu');
-- Tuğla
INSERT INTO malzemeler (kategori, alt_kategori, ad, birim, scrape_tipi) SELECT 'tugla',NULL,'Karkas Tuğla','adet','proemtia_urun' WHERE NOT EXISTS (SELECT 1 FROM malzemeler WHERE ad='Karkas Tuğla');

-- =============================================================
-- SEED: nakliye_katsayilari  (₺/ton/km, varsayılan)
-- =============================================================

INSERT OR IGNORE INTO nakliye_katsayilari (malzeme_kategori, katsayi, gecerlilik_baslangic) VALUES
('demir',       0.20, '2026-05-12'),
('celik_hasir', 0.20, '2026-05-12'),
('filmasin',    0.20, '2026-05-12'),
('beton',       0.25, '2026-05-12'),
('cimento',     0.15, '2026-05-12'),
('kum',         0.30, '2026-05-12'),
('gazbeton',    0.18, '2026-05-12'),
('tugla',       0.20, '2026-05-12');
