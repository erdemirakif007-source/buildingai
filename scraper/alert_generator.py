"""
scrape_fiyatlar tablosundaki son fiyat hareketlerini analiz eder ve
%5+ değişim saptandığında malzeme_uyari tablosuna alert yazar.

Kullanım:
    python -c "from scraper.alert_generator import AlertGenerator; \
    g = AlertGenerator('santiye_proje.db'); g.uret_tum_alertler()"
"""
import logging
import pathlib
import sqlite3
from datetime import datetime, timedelta

logger = logging.getLogger("buildingai.scraper.alert_generator")

DEGISIM_ESIGI = 5.0  # % — bu eşiğin altındaki değişimler alert üretmez
KIYASLAMA_PENCERE_GUN = 7  # son N günlük ortalamayı referans al


class AlertGenerator:
    def __init__(self, db_path: str | pathlib.Path | None = None):
        if db_path is None:
            db_path = pathlib.Path(__file__).parent.parent / "santiye_proje.db"
        self.db_path = pathlib.Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _son_iki_fiyat(self, conn: sqlite3.Connection) -> list[dict]:
        """Her malzeme için son iki farklı güne ait ortalama fiyatı döndürür."""
        pencere_basi = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
        rows = conn.execute(
            """
            WITH gunluk AS (
                SELECT
                    m.id         AS malzeme_id,
                    m.ad         AS malzeme_ad,
                    sf.tarih,
                    AVG(sf.fiyat) AS ort_fiyat,
                    ROW_NUMBER() OVER (
                        PARTITION BY m.id
                        ORDER BY sf.tarih DESC
                    ) AS rn
                FROM scrape_fiyatlar sf
                JOIN malzemeler m ON sf.malzeme_id = m.id
                WHERE sf.tarih >= ?
                GROUP BY m.id, sf.tarih
            )
            SELECT
                g1.malzeme_id,
                g1.malzeme_ad,
                g2.tarih   AS onceki_tarih,
                g2.ort_fiyat AS onceki_fiyat,
                g1.tarih   AS yeni_tarih,
                g1.ort_fiyat AS yeni_fiyat
            FROM gunluk g1
            JOIN gunluk g2
              ON g1.malzeme_id = g2.malzeme_id
             AND g1.rn = 1
             AND g2.rn = 2
            """,
            (pencere_basi,),
        ).fetchall()
        return [dict(r) for r in rows]

    def _alert_var_mi(self, conn: sqlite3.Connection, malzeme_ad: str, eski_fiyat: str, yeni_fiyat: str) -> bool:
        """Aynı malzeme + aynı fiyat geçişi bugün zaten yazılmış mı?"""
        row = conn.execute(
            """SELECT id FROM malzeme_uyari
               WHERE malzeme = ?
                 AND onceki = ?
                 AND yeni = ?
                 AND DATE(created_at) = DATE('now')
               LIMIT 1""",
            (malzeme_ad, eski_fiyat, yeni_fiyat),
        ).fetchone()
        return row is not None

    def uret_tum_alertler(self) -> dict:
        conn = self._connect()
        try:
            cifler = self._son_iki_fiyat(conn)
            uretilen = 0
            atlanan = 0

            for c in cifler:
                onceki = float(c["onceki_fiyat"])
                yeni = float(c["yeni_fiyat"])
                malzeme_ad = c["malzeme_ad"]
                yeni_tarih = c["yeni_tarih"]

                if onceki <= 0:
                    atlanan += 1
                    continue

                degisim = ((yeni - onceki) / onceki) * 100

                if abs(degisim) < DEGISIM_ESIGI:
                    atlanan += 1
                    continue

                if self._alert_var_mi(conn, malzeme_ad, f"{onceki:.2f}", f"{yeni:.2f}"):
                    logger.debug("Alert zaten var: %s / %s", malzeme_ad, yeni_tarih)
                    atlanan += 1
                    continue

                conn.execute(
                    """INSERT INTO malzeme_uyari
                           (malzeme, onceki, yeni, degisim, status, created_at)
                       VALUES (?, ?, ?, ?, 'pending', ?)""",
                    (
                        malzeme_ad,
                        f"{onceki:.2f}",
                        f"{yeni:.2f}",
                        f"{degisim:+.1f}",
                        datetime.utcnow().isoformat(),
                    ),
                )
                logger.info(
                    "Alert üretildi: %s — %+.1f%% (%.2f → %.2f)",
                    malzeme_ad, degisim, onceki, yeni,
                )
                uretilen += 1

            conn.commit()
            result = {
                "uretilen": uretilen,
                "atlanan": atlanan,
                "toplam_karsilastirilan": len(cifler),
            }
            print(result)
            return result

        finally:
            conn.close()
