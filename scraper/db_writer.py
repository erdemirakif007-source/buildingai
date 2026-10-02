"""
Scrape sonuçlarını scrape_fiyatlar tablosuna yazan yardımcı modül.

UPSERT stratejisi: (malzeme_id, referans_merkez_id, tarih, kaynak_url)
kombinasyonu eşleşirse mevcut satırı sil, yerine yenisini ekle.
"""
import logging
import pathlib
import sqlite3

logger = logging.getLogger("buildingai.scraper.db_writer")

DB_PATH = pathlib.Path(__file__).parent.parent / "santiye_proje.db"

# TCMB ortalama kur — admin panelinden sistem_ayarlari tablosuyla güncellenebilir
USD_KUR_VARSAYILAN: float = 38.50

# kum_turu → malzemeler.ad eşlemesi
_KUM_TURU_TO_AD: dict[str, str] = {
    "sap":  "Şap Kumu",
    "kaba": "Kaba Kum",
}


# ── Bağlantı ────────────────────────────────────────────────────────────────

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ── Yardımcı haritalar ───────────────────────────────────────────────────────

def load_malzeme_map(conn: sqlite3.Connection) -> dict[str, int]:
    """malzemeler.ad → id"""
    rows = conn.execute("SELECT id, ad FROM malzemeler").fetchall()
    return {r["ad"]: r["id"] for r in rows}


def load_merkez_map(conn: sqlite3.Connection) -> dict[str, int]:
    """referans_merkezler.kod → id"""
    rows = conn.execute("SELECT id, kod FROM referans_merkezler").fetchall()
    return {r["kod"]: r["id"] for r in rows}


def ensure_malzeme(
    conn: sqlite3.Connection,
    kategori: str,
    alt_kategori: str | None,
    ad: str,
    birim: str,
    scrape_tipi: str,
) -> int:
    """Malzeme yoksa oluştur, id döndür."""
    conn.execute(
        "INSERT OR IGNORE INTO malzemeler "
        "(kategori, alt_kategori, ad, birim, scrape_tipi) VALUES (?,?,?,?,?)",
        (kategori, alt_kategori, ad, birim, scrape_tipi),
    )
    row = conn.execute(
        "SELECT id FROM malzemeler WHERE kategori = ? AND ad = ?",
        (kategori, ad),
    ).fetchone()
    return row["id"]


def usd_to_try(fiyat_usd: float, kur: float = USD_KUR_VARSAYILAN) -> float:
    return round(fiyat_usd * kur, 2)


# ── Temel UPSERT ─────────────────────────────────────────────────────────────

def _upsert(
    conn: sqlite3.Connection,
    malzeme_id: int,
    referans_merkez_id: int | None,
    fiyat: float,
    kdv_dahil: bool,
    tarih: str,
    kaynak: str,
    kaynak_url: str,
    match_source_url: bool = True,
) -> None:
    if match_source_url:
        conn.execute(
            """DELETE FROM scrape_fiyatlar
               WHERE malzeme_id = ?
                 AND (referans_merkez_id IS ? OR referans_merkez_id = ?)
                 AND tarih = ?
                 AND kaynak_url = ?""",
            (malzeme_id, referans_merkez_id, referans_merkez_id, tarih, kaynak_url),
        )
    else:
        conn.execute(
            """DELETE FROM scrape_fiyatlar
               WHERE malzeme_id = ?
                 AND (referans_merkez_id IS ? OR referans_merkez_id = ?)
                 AND tarih = ?""",
            (malzeme_id, referans_merkez_id, referans_merkez_id, tarih),
        )
    conn.execute(
        """INSERT INTO scrape_fiyatlar
               (malzeme_id, referans_merkez_id, fiyat, kdv_dahil, tarih, kaynak, kaynak_url)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (malzeme_id, referans_merkez_id, fiyat, 1 if kdv_dahil else 0,
         tarih, kaynak, kaynak_url),
    )


# ── Endeks scraper'ları (demir, hasır, filmaşin) ─────────────────────────────

def kaydet_endeks(
    conn: sqlite3.Connection,
    kayitlar: list[dict],
    malzeme_map: dict[str, int],
    merkez_map: dict[str, int],
) -> tuple[int, int]:
    """
    Endeks scraper çıktısını yazar.

    Her scraper dict'inde `malzeme_ad` zorunludur.
    Merkez kodu için `merkez_kod` (demir) veya `referans_merkez_kod`
    (hasır/filmaşin) alanlarından birini kabul eder.

    Filmaşin USD fiyatları runner tarafından TRY'ye çevrilmiş olarak
    gelmeli — bu fonksiyon para birimini kontrol etmez.

    Döner: (eklendi, atlandi)
    """
    eklendi = atlandi = 0

    for k in kayitlar:
        malzeme_id = malzeme_map.get(k["malzeme_ad"])
        if malzeme_id is None:
            logger.warning("Malzeme eşleşmedi, atlandı: '%s'", k["malzeme_ad"])
            atlandi += 1
            continue

        merkez_kod = k.get("merkez_kod") or k.get("referans_merkez_kod")
        referans_merkez_id = merkez_map.get(merkez_kod) if merkez_kod else None

        _upsert(
            conn,
            malzeme_id=malzeme_id,
            referans_merkez_id=referans_merkez_id,
            fiyat=k["fiyat"],
            kdv_dahil=bool(k["kdv_dahil"]),
            tarih=k["tarih"],
            kaynak=k["kaynak"],
            kaynak_url=k["kaynak_url"],
            match_source_url=False,
        )
        eklendi += 1

    conn.commit()
    return eklendi, atlandi


# ── Ürün scraper'ları ────────────────────────────────────────────────────────

def kaydet_urun_cimento(
    conn: sqlite3.Connection,
    kayitlar: list[dict],
    malzeme_map: dict[str, int],
) -> tuple[int, int]:
    """
    Çimento ürün scraper çıktısını yazar.
    Yeni marka/ürün kombinasyonları malzemeler tablosuna dinamik olarak eklenir.
    """
    eklendi = atlandi = 0

    for k in kayitlar:
        ad = f"{k['marka']} {k['urun_adi']}".strip()
        if not ad:
            atlandi += 1
            continue

        malzeme_id = malzeme_map.get(ad)
        if malzeme_id is None:
            malzeme_id = ensure_malzeme(conn, "cimento", None, ad, "torba", "proemtia_urun")
            malzeme_map[ad] = malzeme_id
            logger.info("Yeni malzeme eklendi: çimento / '%s'", ad)

        _upsert(
            conn,
            malzeme_id=malzeme_id,
            referans_merkez_id=None,
            fiyat=k["fiyat_kdv_dahil"],
            kdv_dahil=True,
            tarih=k["tarih"],
            kaynak=k["kaynak"],
            kaynak_url=k["urun_url"],
        )
        eklendi += 1

    conn.commit()
    return eklendi, atlandi


def kaydet_urun_kum(
    conn: sqlite3.Connection,
    kayitlar: list[dict],
    malzeme_map: dict[str, int],
) -> tuple[int, int]:
    """
    Kum ürün scraper çıktısını yazar.
    kum_turu="diger" olan kayıtlar atlanır.
    """
    eklendi = atlandi = 0

    for k in kayitlar:
        malzeme_ad = _KUM_TURU_TO_AD.get(k["kum_turu"])
        if malzeme_ad is None:
            logger.debug("kum_turu='%s' için eşleme yok, atlandı", k["kum_turu"])
            atlandi += 1
            continue

        malzeme_id = malzeme_map.get(malzeme_ad)
        if malzeme_id is None:
            logger.warning("Malzeme bulunamadı: '%s'", malzeme_ad)
            atlandi += 1
            continue

        _upsert(
            conn,
            malzeme_id=malzeme_id,
            referans_merkez_id=None,
            fiyat=k["fiyat_kdv_dahil"],
            kdv_dahil=True,
            tarih=k["tarih"],
            kaynak=k["kaynak"],
            kaynak_url=k["urun_url"],
        )
        eklendi += 1

    conn.commit()
    return eklendi, atlandi


def kaydet_urun_gazbeton(
    conn: sqlite3.Connection,
    kayitlar: list[dict],
    malzeme_map: dict[str, int],
) -> tuple[int, int]:
    """
    Gazbeton ürün scraper çıktısını yazar.
    Tüm ürünler 'Gazbeton Düz Duvar Bloğu' malzemesine eşlenir.
    Fiyat birimi TL/adet'tir; malzemeler tablosundaki m3 birimi referans birimdir.
    """
    MALZEME_AD = "Gazbeton Düz Duvar Bloğu"
    malzeme_id = malzeme_map.get(MALZEME_AD)
    if malzeme_id is None:
        logger.error("Malzeme bulunamadı: '%s' — gazbeton yazılamadı", MALZEME_AD)
        return 0, len(kayitlar)

    eklendi = 0
    for k in kayitlar:
        _upsert(
            conn,
            malzeme_id=malzeme_id,
            referans_merkez_id=None,
            fiyat=k["fiyat_kdv_dahil"],
            kdv_dahil=True,
            tarih=k["tarih"],
            kaynak=k["kaynak"],
            kaynak_url=k["urun_url"],
        )
        eklendi += 1

    conn.commit()
    return eklendi, 0
