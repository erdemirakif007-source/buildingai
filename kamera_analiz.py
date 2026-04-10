"""
BuildingAI — Yerel Kamera & Video Analiz Motoru
================================================
YOLOv11 tabanlı PPE tespiti + OpenCV hareket algılama.
Harici AI API kullanılmaz — tamamen yerel çalışır.

Desteklenen kaynaklar:
  - Tek frame (IP kamera stream, fotoğraf yükleme)
  - Video dosyası (FFmpeg keyframe çıkarma → batch analiz)

Output formatı:
  {
    "risk_level": "YÜKSEK|ORTA|DÜŞÜK",
    "violations": [...],
    "confidence": 0.87,
    "timestamp": "2024-01-01T12:00:00",
    "site_id": 1,
    "kisi_sayisi": 3,
    "ppe_uyum_orani": 0.67
  }
"""

from __future__ import annotations

import base64
import json
import logging
import os
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np

logger = logging.getLogger("buildingai.kamera_analiz")

# ──────────────────────────────────────────────────────────────────────────────
# Sabitler
# ──────────────────────────────────────────────────────────────────────────────

# PPE özel model dosyası (varsa static/models/ altında olmalı)
PPE_MODEL_PATH = os.path.join("static", "models", "ppe_yolov11n.pt")

# Hareket tespiti eşiği (piksel sayısı) — düşürünce hassasiyet artar
HAREKET_ESIK = 1200

# YOLO conf eşiği
YOLO_CONF = 0.35

# Thumbnail max genişliği (px)
THUMB_MAX_W = 640

# Video analiz için varsayılan FPS
VIDEO_FPS = 1.0

# ──────────────────────────────────────────────────────────────────────────────
# PPE sınıf haritası
# ──────────────────────────────────────────────────────────────────────────────
# Değer:
#   True  → uyumlu (PPE VAR)
#   False → ihlal  (PPE YOK)
#   None  → nötr  (sadece tespit)
PPE_SINIF_HARITASI: Dict[str, Optional[bool]] = {
    # Standart construction PPE sınıfları
    "hardhat":          True,
    "helmet":           True,
    "no_hardhat":       False,
    "no_helmet":        False,
    "safety_vest":      True,
    "vest":             True,
    "no_safety_vest":   False,
    "no_vest":          False,
    "safety_cone":      None,
    "safety_boots":     True,
    "no_safety_boots":  False,
    "gloves":           True,
    "no_gloves":        False,
    "goggles":          True,
    "no_goggles":       False,
    # COCO standart modeli
    "person":           None,
}

# Risk sıralaması (karşılaştırma için)
RISK_SIRASI = {"YÜKSEK": 3, "ORTA": 2, "DÜŞÜK": 1, "BİLİNMİYOR": 0}


# ──────────────────────────────────────────────────────────────────────────────
# Singleton Model Yükleyici
# ──────────────────────────────────────────────────────────────────────────────

class _PPEModelYukleyici:
    """
    Uygulama ömrü boyunca tek YOLO instance tutar.
    İlk analiz çağrısında lazy-load yapar.
    """
    _instance: Optional["_PPEModelYukleyici"] = None

    def __new__(cls) -> "_PPEModelYukleyici":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
            cls._instance._model_yuklendi = False
            cls._instance._aktif = False
        return cls._instance

    def _yukleme_yap(self) -> None:
        if self._model_yuklendi:
            return
        self._model_yuklendi = True
        try:
            from ultralytics import YOLO  # type: ignore
            if os.path.exists(PPE_MODEL_PATH):
                self._model = YOLO(PPE_MODEL_PATH)
                logger.info(f"[YOLO] PPE özel modeli yüklendi: {PPE_MODEL_PATH}")
            else:
                self._model = YOLO("yolo11n.pt")  # otomatik indirir
                logger.info("[YOLO] YOLOv11n standart modeli yüklendi")
            self._aktif = True
        except ImportError:
            logger.warning("[YOLO] ultralytics kurulu değil — analiz devre dışı")
        except Exception as exc:
            logger.error(f"[YOLO] Model yükleme hatası: {exc}")

    @property
    def hazir(self) -> bool:
        self._yukleme_yap()
        return self._aktif

    def infer(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Tek frame üzerinde çıkarım yap.
        Returns: [{"class": str, "confidence": float, "bbox": [x1,y1,x2,y2]}, ...]
        """
        self._yukleme_yap()
        if not self._aktif or self._model is None:
            return []
        results = self._model(frame, verbose=False, conf=YOLO_CONF)
        detections: List[Dict[str, Any]] = []
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf   = float(box.conf[0])
                name   = r.names[cls_id].lower().replace(" ", "_")
                bbox   = [round(v, 1) for v in box.xyxy[0].tolist()]
                detections.append({
                    "class":      name,
                    "class_id":   cls_id,
                    "confidence": round(conf, 3),
                    "bbox":       bbox,
                })
        return detections


# Uygulama geneli singleton
_model = _PPEModelYukleyici()

# Bloklama işlemleri için thread pool
_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="yolo")


# ──────────────────────────────────────────────────────────────────────────────
# Hareket Tespiti
# ──────────────────────────────────────────────────────────────────────────────

def hareket_var_mi(frame1: np.ndarray, frame2: np.ndarray,
                   esik: int = HAREKET_ESIK) -> bool:
    """
    İki frame arasında OpenCV absdiff ile hareket tespiti.
    True → hareket var → YOLO tetikle
    False → statik sahne → atla (performans optimizasyonu)
    """
    g1 = cv2.GaussianBlur(cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY), (21, 21), 0)
    g2 = cv2.GaussianBlur(cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY), (21, 21), 0)
    diff = cv2.absdiff(g1, g2)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    return int(cv2.countNonZero(thresh)) > esik


# ──────────────────────────────────────────────────────────────────────────────
# İhlal & Risk Hesaplama
# ──────────────────────────────────────────────────────────────────────────────

def ihlal_ve_risk_hesapla(
    detections: List[Dict[str, Any]],
    site_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Tespit listesinden ihlaller, risk seviyesi ve uyum oranı hesapla.
    """
    kisi_sayisi = sum(1 for d in detections if d["class"] == "person")

    ihlaller: List[str] = []
    uyumlu_sayisi = 0
    uyumsuz_sayisi = 0
    conf_list = [d["confidence"] for d in detections]

    for det in detections:
        sinif = det["class"]
        durum = PPE_SINIF_HARITASI.get(sinif)
        if durum is True:
            uyumlu_sayisi += 1
        elif durum is False:
            uyumsuz_sayisi += 1
            ihlaller.append(sinif)

    toplam_ppe = uyumlu_sayisi + uyumsuz_sayisi
    if toplam_ppe == 0:
        # Sadece kişi ya da bilinmeyen sınıflar var — oran bilinmiyor
        ppe_uyum_orani: float = -1.0
    else:
        ppe_uyum_orani = round(uyumlu_sayisi / toplam_ppe, 2)

    # Risk seviyesi belirleme
    if uyumsuz_sayisi >= 3 or (kisi_sayisi > 0 and uyumsuz_sayisi >= kisi_sayisi):
        risk = "YÜKSEK"
    elif uyumsuz_sayisi >= 1:
        risk = "ORTA"
    elif kisi_sayisi > 0 and toplam_ppe == 0:
        # Kişi var ama PPE bilgisi yok (standart COCO modeli)
        risk = "ORTA"
    else:
        risk = "DÜŞÜK"

    ort_conf = round(sum(conf_list) / len(conf_list), 3) if conf_list else 0.0

    return {
        "risk_level":     risk,
        "violations":     ihlaller,
        "confidence":     ort_conf,
        "kisi_sayisi":    kisi_sayisi,
        "ppe_uyum_orani": ppe_uyum_orani,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Frame Dönüştürücüler
# ──────────────────────────────────────────────────────────────────────────────

def bytes_to_frame(image_bytes: bytes) -> Optional[np.ndarray]:
    """JPEG/PNG bytes → OpenCV BGR frame"""
    arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def base64_to_frame(b64_str: str) -> Optional[np.ndarray]:
    """Base64 string → OpenCV BGR frame"""
    # data:image/jpeg;base64,... prefix varsa temizle
    if "," in b64_str:
        b64_str = b64_str.split(",", 1)[1]
    try:
        return bytes_to_frame(base64.b64decode(b64_str))
    except Exception:
        return None


def frame_to_thumbnail_b64(frame: np.ndarray, max_w: int = THUMB_MAX_W) -> str:
    """Frame → base64 JPEG thumbnail"""
    h, w = frame.shape[:2]
    if w > max_w:
        scale = max_w / w
        frame = cv2.resize(frame, (max_w, int(h * scale)))
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 72])
    if not ok:
        return ""
    return base64.b64encode(buf.tobytes()).decode()


# ──────────────────────────────────────────────────────────────────────────────
# Tek Frame Analiz
# ──────────────────────────────────────────────────────────────────────────────

def kare_analiz_et(
    frame: np.ndarray,
    site_id: Optional[int] = None,
    timestamp: Optional[str] = None,
    thumbnail: bool = False,
) -> Dict[str, Any]:
    """
    Bir BGR frame üzerinde tam PPE + ihlal + risk analizi.
    """
    detections = _model.infer(frame)
    sonuc = ihlal_ve_risk_hesapla(detections, site_id)
    sonuc["timestamp"] = timestamp or datetime.utcnow().isoformat()
    sonuc["site_id"]   = site_id
    sonuc["tespitler"] = detections
    if thumbnail:
        sonuc["thumbnail"] = frame_to_thumbnail_b64(frame)
    return sonuc


# ──────────────────────────────────────────────────────────────────────────────
# FFmpeg Keyframe Çıkarıcı
# ──────────────────────────────────────────────────────────────────────────────

def _ffmpeg_keyframe_cikart(
    video_path: str,
    fps: float,
    cikti_dizin: str,
) -> List[str]:
    """FFmpeg ile video'dan fps hızında keyframe çıkar."""
    pattern = os.path.join(cikti_dizin, "frame_%05d.jpg")
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", f"fps={fps}",
        "-q:v", "3",
        "-y",
        pattern,
    ]
    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=180,
        )
        return sorted(str(p) for p in Path(cikti_dizin).glob("frame_*.jpg"))
    except FileNotFoundError:
        logger.warning("[FFmpeg] bulunamadı — OpenCV fallback kullanılıyor")
        return []
    except subprocess.CalledProcessError as exc:
        logger.error(f"[FFmpeg] Hata: {exc}")
        return []
    except subprocess.TimeoutExpired:
        logger.error("[FFmpeg] Zaman aşımı (>180s)")
        return []


def _opencv_keyframe_cikart(
    video_path: str,
    fps: float,
    cikti_dizin: str,
) -> List[str]:
    """FFmpeg yoksa OpenCV VideoCapture ile keyframe çıkar."""
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    aralik = max(1, int(video_fps / fps))
    kaydedilenler: List[str] = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % aralik == 0:
            path = os.path.join(cikti_dizin, f"frame_{len(kaydedilenler):05d}.jpg")
            cv2.imwrite(path, frame)
            kaydedilenler.append(path)
        frame_idx += 1

    cap.release()
    return kaydedilenler


def keyframe_cikart(
    video_path: str,
    fps: float = VIDEO_FPS,
    cikti_dizin: Optional[str] = None,
) -> Tuple[List[str], str]:
    """
    Video'dan keyframe çıkar.
    Returns: (frame_path_list, cikti_dizin)
    """
    if cikti_dizin is None:
        cikti_dizin = tempfile.mkdtemp(prefix="bai_frames_")

    frames = _ffmpeg_keyframe_cikart(video_path, fps, cikti_dizin)
    if not frames:
        frames = _opencv_keyframe_cikart(video_path, fps, cikti_dizin)

    return frames, cikti_dizin


# ──────────────────────────────────────────────────────────────────────────────
# Video Toplu Analiz (sync — ThreadPoolExecutor'da çalıştırılır)
# ──────────────────────────────────────────────────────────────────────────────

def _video_analiz_sync(
    video_path: str,
    site_id: Optional[int],
    fps: float,
    hareket_filtre: bool,
) -> Dict[str, Any]:
    """
    Senkron video analiz pipeline:
    1. FFmpeg/OpenCV ile keyframe çıkar (1 FPS)
    2. Hareket filtresi — statik kareleri atla
    3. YOLOv8 PPE analizi
    4. Toplu sonuç birleştir
    """
    frames, tmp_dir = keyframe_cikart(video_path, fps=fps)

    if not frames:
        return {
            "hata":          "Video'dan frame çıkarılamadı",
            "risk_level":    "BİLİNMİYOR",
            "violations":    [],
            "confidence":    0.0,
            "timestamp":     datetime.utcnow().isoformat(),
            "site_id":       site_id,
            "kisi_sayisi":   0,
            "ppe_uyum_orani": -1.0,
            "analiz_edilen_kare": 0,
            "toplam_kare":   0,
        }

    kare_sonuclari: List[Dict[str, Any]] = []
    onceki_frame: Optional[np.ndarray] = None
    max_kisi = 0
    tum_ihlaller: List[str] = []
    thumbnail_b64 = ""

    for frame_path in frames:
        frame = cv2.imread(frame_path)
        if frame is None:
            continue

        # Hareket filtresi
        if hareket_filtre and onceki_frame is not None:
            if not hareket_var_mi(onceki_frame, frame):
                onceki_frame = frame
                continue

        sonuc = kare_analiz_et(frame, site_id=site_id)
        kare_sonuclari.append(sonuc)
        max_kisi = max(max_kisi, sonuc["kisi_sayisi"])
        tum_ihlaller.extend(sonuc["violations"])

        # İlk analiz edilen kareyi thumbnail olarak sakla
        if not thumbnail_b64:
            thumbnail_b64 = frame_to_thumbnail_b64(frame)

        onceki_frame = frame

    # Temp dizini temizle
    shutil.rmtree(tmp_dir, ignore_errors=True)

    if not kare_sonuclari:
        return {
            "risk_level":    "DÜŞÜK",
            "violations":    [],
            "confidence":    0.0,
            "timestamp":     datetime.utcnow().isoformat(),
            "site_id":       site_id,
            "kisi_sayisi":   0,
            "ppe_uyum_orani": 1.0,
            "analiz_edilen_kare": 0,
            "toplam_kare":   len(frames),
        }

    # En kötü kareyi bul
    en_kotu = max(
        kare_sonuclari,
        key=lambda x: RISK_SIRASI.get(x["risk_level"], 0),
    )

    # İhlal frekansları
    ihlal_sayac: Dict[str, int] = {}
    for ihlal in tum_ihlaller:
        ihlal_sayac[ihlal] = ihlal_sayac.get(ihlal, 0) + 1

    ort_conf = round(
        sum(s["confidence"] for s in kare_sonuclari) / len(kare_sonuclari), 3
    )
    ppe_degerler = [
        s["ppe_uyum_orani"] for s in kare_sonuclari if s["ppe_uyum_orani"] >= 0
    ]
    ort_ppe = round(sum(ppe_degerler) / len(ppe_degerler), 2) if ppe_degerler else -1.0

    return {
        "risk_level":          en_kotu["risk_level"],
        "violations":          list(ihlal_sayac.keys()),
        "ihlal_frekanslari":   ihlal_sayac,
        "confidence":          ort_conf,
        "timestamp":           datetime.utcnow().isoformat(),
        "site_id":             site_id,
        "kisi_sayisi":         max_kisi,
        "ppe_uyum_orani":      ort_ppe,
        "analiz_edilen_kare":  len(kare_sonuclari),
        "toplam_kare":         len(frames),
        "thumbnail":           thumbnail_b64,
    }


async def video_analiz(
    video_path: str,
    site_id: Optional[int] = None,
    fps: float = VIDEO_FPS,
    hareket_filtre: bool = True,
) -> Dict[str, Any]:
    """
    Async wrapper — YOLO inference'ı bloklamamak için thread pool kullanır.
    FastAPI endpoint'lerinden çağrılır.
    """
    import asyncio
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        _executor,
        _video_analiz_sync,
        video_path, site_id, fps, hareket_filtre,
    )


# ──────────────────────────────────────────────────────────────────────────────
# IP Kamera / Fotoğraf Frame Analizi (Async)
# ──────────────────────────────────────────────────────────────────────────────

async def frame_analiz(
    image_bytes: bytes,
    site_id: Optional[int] = None,
    thumbnail: bool = True,
) -> Dict[str, Any]:
    """
    Tek frame analiz — IP kamera stream veya yüklenen fotoğraf.
    YOLO inference thread pool'da çalışır (non-blocking).
    """
    import asyncio

    frame = bytes_to_frame(image_bytes)
    if frame is None:
        return {
            "hata":        "Görüntü okunamadı",
            "risk_level":  "BİLİNMİYOR",
            "violations":  [],
            "confidence":  0.0,
            "timestamp":   datetime.utcnow().isoformat(),
            "site_id":     site_id,
        }

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        _executor,
        kare_analiz_et,
        frame, site_id, None, thumbnail,
    )


async def frame_analiz_b64(
    b64_str: str,
    site_id: Optional[int] = None,
    thumbnail: bool = True,
) -> Dict[str, Any]:
    """Base64 string → frame analiz"""
    frame = base64_to_frame(b64_str)
    if frame is None:
        return {
            "hata":       "Base64 görüntü çözümlenemedi",
            "risk_level": "BİLİNMİYOR",
            "violations": [],
            "confidence": 0.0,
            "timestamp":  datetime.utcnow().isoformat(),
            "site_id":    site_id,
        }
    import asyncio
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        _executor,
        kare_analiz_et,
        frame, site_id, None, thumbnail,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Model Sağlık Kontrolü
# ──────────────────────────────────────────────────────────────────────────────

def model_durum() -> Dict[str, Any]:
    """Model yüklü mü? Hangi model kullanılıyor?"""
    return {
        "yolo_aktif":    _model.hazir,
        "model_yolu":    PPE_MODEL_PATH if os.path.exists(PPE_MODEL_PATH) else "yolo11n.pt (standart)",
        "opencv_versiyon": cv2.__version__,
    }
