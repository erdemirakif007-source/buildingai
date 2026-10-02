/**
 * cameraPresets.ts
 *
 * Kamera ön-ayarları, animasyonlu geçişler ve ViewCube yönetimi.
 *
 * ─── ÖZELLİKLER ──────────────────────────────────────────────────────────────
 *
 *  CameraPresets
 *  ├── goToPreset()         → Animasyonlu kamera preset geçişi (lerp)
 *  ├── fitToModel()         → Tüm modeli kapsayan kamera konumu
 *  ├── fitToElement()       → Tek bir element'e zoom (ExpressID ile)
 *  ├── fitToStorey()        → Belirli bir kata zoom (elevation'a göre)
 *  ├── toggleProjection()   → Perspektif ↔ Ortografik geçiş
 *  ├── ViewCube             → Sağ üst köşede 3D navigasyon küpü (HTML/CSS)
 *  └── Keyboard Shortcuts   → Numpad + Home + F kısayolları
 *
 * ─── ANİMASYON STRATEJİSİ ────────────────────────────────────────────────────
 *
 *  GSAP veya Tween.js bağımlılığı yoktur.
 *  Animasyon, ease-in-out ile manuel lerp fonksiyonu kullanılarak
 *  requestAnimationFrame döngüsü üzerinden yapılır.
 *
 *  Easing: t < 0.5 ? 2t² : 1 − (−2t+2)²/2  (cubic ease-in-out)
 *
 * ─── ORTOGRAFIK PROJEKSIYON ──────────────────────────────────────────────────
 *
 *  toggleProjection() çağrıldığında:
 *  1. Mevcut kamera pozisyonu ve yönü korunur
 *  2. OrthographicCamera oluşturulur (ya da PerspectiveCamera'ya dönülür)
 *  3. OrbitControls yeni kameraya bağlanır
 *  4. Dışarıya onCameraChanged callback'i tetiklenir
 *
 * ─── VIEWCUBE ────────────────────────────────────────────────────────────────
 *
 *  HTML/CSS ile oluşturulmuş hafif 3D navigasyon küpü.
 *  Ayrı bir Three.js mini-sahnesi gerektirmez.
 *  CSS transform ile kamera rotasyonuyla senkron döner.
 *
 * ─── GELECEKTEKİ GELİŞTİRMELER ──────────────────────────────────────────────
 *  - ViewCube yüz üzerinde hover highlight
 *  - Custom preset kaydetme / yükleme
 *  - Walk-through / fly-through modu
 *  - First-person camera modu
 */
import * as THREE from 'three';
// ─── Sabitler ─────────────────────────────────────────────────────────────────
/**
 * Kamera preset tanımları.
 * position: kameranın dünya koordinatlarındaki hedef konumu
 * target:   OrbitControls'un baktığı nokta
 * up:       kameranın "yukarı" yön vektörü (üstten bakışta değişir)
 */
const PRESETS = {
    top: { position: [0, 100, 0], target: [0, 0, 0], up: [0, 0, -1] },
    bottom: { position: [0, -100, 0], target: [0, 0, 0], up: [0, 0, 1] },
    front: { position: [0, 0, 100], target: [0, 0, 0], up: [0, 1, 0] },
    back: { position: [0, 0, -100], target: [0, 0, 0], up: [0, 1, 0] },
    left: { position: [-100, 0, 0], target: [0, 0, 0], up: [0, 1, 0] },
    right: { position: [100, 0, 0], target: [0, 0, 0], up: [0, 1, 0] },
    isometric: { position: [70, 70, 70], target: [0, 0, 0], up: [0, 1, 0] },
};
/** Animasyon varsayılan süresi (ms) */
const DEFAULT_DURATION = 500;
/** Ortografik kamera frustum boyutu çarpanı */
const ORTHO_FRUSTUM_SIZE = 50;
// ─── Animasyon Yardımcısı ─────────────────────────────────────────────────────
/**
 * Kamerayı hedef pozisyona animasyonlu olarak taşır.
 *
 * Ease-in-out cubic algoritmasıyla yumuşak geçiş sağlar.
 * GSAP/Tween bağımlılığı gerekmez.
 *
 * @param camera    - THREE.PerspectiveCamera veya THREE.OrthographicCamera
 * @param controls  - OrbitControls (target güncellenir)
 * @param targetPos - Kameranın ulaşacağı konum
 * @param targetLookAt - Controls'un bakacağı nokta
 * @param duration  - Animasyon süresi (ms), varsayılan 500ms
 * @param targetUp  - Kameranın up vektörü (opsiyonel)
 * @param onComplete - Animasyon bitişinde çağrılacak callback
 */
function animateCamera(camera, controls, targetPos, targetLookAt, duration = DEFAULT_DURATION, targetUp, onComplete) {
    const startPos = camera.position.clone();
    const startTarget = controls.target.clone();
    const startUp = camera.up.clone();
    const startTime = performance.now();
    // Çalışan animasyonu iptal etmek için bir flag
    let cancelled = false;
    function update() {
        if (cancelled)
            return;
        const elapsed = performance.now() - startTime;
        const t = Math.min(elapsed / duration, 1);
        // Cubic ease-in-out: pürüzsüz hız profili
        const eased = t < 0.5
            ? 2 * t * t
            : 1 - Math.pow(-2 * t + 2, 2) / 2;
        camera.position.lerpVectors(startPos, targetPos, eased);
        controls.target.lerpVectors(startTarget, targetLookAt, eased);
        if (targetUp) {
            camera.up.lerpVectors(startUp, targetUp, eased);
        }
        controls.update();
        if (t < 1) {
            requestAnimationFrame(update);
        }
        else {
            // Animasyon tamamlandı — kesin değerlere snap et
            camera.position.copy(targetPos);
            controls.target.copy(targetLookAt);
            if (targetUp)
                camera.up.copy(targetUp);
            controls.update();
            onComplete?.();
        }
    }
    requestAnimationFrame(update);
    // Dışarıdan iptal edebilmek için token döndür
    // (şu an kullanılmıyor; ileride eklenebilir)
    return;
}
// ─── Ana Sınıf ────────────────────────────────────────────────────────────────
/**
 * BIM Viewer kamera ön-ayarları, animasyonlar ve ViewCube yöneticisi.
 *
 * KULLANIM ÖRNEĞİ:
 * ```ts
 * const presets = new CameraPresets(camera, controls, scene, viewport);
 * presets.goToPreset('isometric');
 * presets.fitToModel();
 * presets.toggleProjection();
 * ```
 */
export class CameraPresets {
    // ─── Constructor ──────────────────────────────────────────────────────────
    /**
     * @param camera   - Sahnedeki perspektif kamera
     * @param controls - OrbitControls
     * @param scene    - Three.js sahnesi (bounding box hesabı için)
     * @param viewport - Viewport DOM elementi (ViewCube ve klavye için)
     */
    constructor(camera, controls, scene, viewport) {
        this._orthoCamera = null;
        // ── Durum ────────────────────────────────────────────────────────────────
        /** Şu an ortografik mod mu? */
        this._isOrtho = false;
        /** Seçilen element ExpressID → mesh bounding box cache */
        this._elementBoxCache = new Map();
        /** Klavye event listener referansı (dispose için) */
        this._keyHandler = null;
        /** ViewCube DOM elementi */
        this._viewCubeEl = null;
        /** ViewCube rotasyon sync RAF ID */
        this._viewCubeRafId = null;
        // ── Callback'ler ─────────────────────────────────────────────────────────
        /**
         * Projeksiyon türü değiştiğinde çağrılır.
         * BIMViewer, renderer'ı güncellemek için bu callback'i kullanabilir.
         *
         * @param isOrtho - true: ortografik, false: perspektif
         * @param camera  - Aktif kamera (yeni tip)
         */
        this.onCameraChanged = null;
        this._perspCamera = camera;
        this._controls = controls;
        this._scene = scene;
        this._viewport = viewport;
        this._bindKeyboard();
        this._createViewCube();
        this._startViewCubeSync();
    }
    // ─── Public API ───────────────────────────────────────────────────────────
    /**
     * Kamerayı belirtilen preset konumuna animasyonla taşır.
     *
     * Preset'in pozisyonunu, mevcut modelin bounding box merkezine
     * göre ölçeklendirir — model yoksa ham preset değerleri kullanılır.
     *
     * @param preset - Preset adı ('top', 'front', 'isometric' vb.)
     * @param duration - Animasyon süresi ms (varsayılan 500)
     */
    goToPreset(preset, duration = DEFAULT_DURATION) {
        const def = PRESETS[preset];
        // Modelin merkezini bul (yoksa origin kullan)
        const center = this._getModelCenter();
        // Preset pozisyonunu model merkezine göre offset'le
        const rawPos = new THREE.Vector3(...def.position);
        const targetPos = center.clone().add(rawPos);
        const targetUp = new THREE.Vector3(...def.up);
        const activeCamera = this._getActiveCamera();
        animateCamera(activeCamera, this._controls, targetPos, center, // Her zaman modelin merkezine bak
        duration, targetUp);
        console.log(`[CameraPresets] Preset: ${preset} → pos(${targetPos.toArray().map(v => v.toFixed(1)).join(', ')})`);
    }
    /**
     * Kamerayı tüm modeli kapsayacak şekilde konumlandırır.
     *
     * ADIMLAR:
     * 1. Sahnedeki tüm mesh'lerin bounding box'ını hesapla
     * 2. FOV'a göre gerekli mesafeyi hesapla
     * 3. Animasyonla kamerayı taşı
     *
     * @param duration - Animasyon süresi ms (varsayılan 500)
     */
    fitToModel(duration = DEFAULT_DURATION) {
        const box = this._computeSceneBoundingBox();
        if (box.isEmpty()) {
            console.warn('[CameraPresets] fitToModel: Sahne boş veya model yok.');
            return;
        }
        this._fitToBox(box, duration);
        console.log('[CameraPresets] Tüm modele zoom yapıldı.');
    }
    /**
     * Belirli bir element'e zoom yapar.
     *
     * Element mesh'i sahnede bulunup bounding box'ı hesaplanır.
     * Bulunamazsa uyarı verir.
     *
     * @param expressId - IFC ExpressID
     * @param duration  - Animasyon süresi ms
     */
    fitToElement(expressId, duration = DEFAULT_DURATION) {
        // Cache'de varsa kullan
        let box = this._elementBoxCache.get(expressId);
        if (!box) {
            const found = this._findElementBox(expressId);
            if (found) {
                this._elementBoxCache.set(expressId, found);
                box = found;
            }
        }
        if (!box || box.isEmpty()) {
            console.warn(`[CameraPresets] fitToElement: Element bulunamadı veya box boş — expressId: ${expressId}`);
            return;
        }
        this._fitToBox(box, duration);
        console.log(`[CameraPresets] Element'e zoom: expressId=${expressId}`);
    }
    /**
     * Belirli bir kata zoom yapar.
     *
     * Elevation değeri ve kat yüksekliği kullanılarak bir sınırlayıcı
     * kutu oluşturulur, kamera bu kutuyu görecek şekilde konumlandırılır.
     *
     * @param storeyInfo - StoreyInfo objesi (elevation ve elementIds içerir)
     * @param duration   - Animasyon süresi ms
     */
    fitToStorey(storeyInfo, duration = DEFAULT_DURATION) {
        // Kat elemanlarının bounding box'ını hesapla
        const box = this._computeStoreyBoundingBox(storeyInfo);
        if (box.isEmpty()) {
            // Fallback: elevation'a dayalı tahmini kutu
            const estimated = this._estimateStoreyBox(storeyInfo);
            this._fitToBox(estimated, duration);
            console.log(`[CameraPresets] Kat'a zoom (tahmini): ${storeyInfo.name}`);
            return;
        }
        this._fitToBox(box, duration);
        console.log(`[CameraPresets] Kat'a zoom: ${storeyInfo.name} (elevation: ${storeyInfo.elevation.toFixed(2)}m)`);
    }
    /**
     * Perspektif ↔ Ortografik projeksiyon geçişi.
     *
     * GEÇIŞ MANTIĞI:
     * - Perspektif → Ortografik: PerspectiveCamera'nın mevcut pozisyon
     *   ve bakış yönü korunarak OrthographicCamera oluşturulur.
     * - Ortografik → Perspektif: PerspectiveCamera'ya geri dönülür,
     *   OrthoCamera dispose edilir.
     *
     * OrbitControls yeni kameraya yeniden bağlanmaz (same domElement kullanır);
     * bunun yerine controls.object değiştirilir.
     */
    toggleProjection() {
        if (!this._isOrtho) {
            this._switchToOrtho();
        }
        else {
            this._switchToPerspective();
        }
    }
    /** Şu an ortografik mod mu? */
    get isOrtho() {
        return this._isOrtho;
    }
    /** Şu an aktif olan kamera */
    get activeCamera() {
        return this._getActiveCamera();
    }
    /**
     * Element kutu cache'ini temizler.
     * Model yeniden yüklendiğinde çağrılmalı.
     */
    clearCache() {
        this._elementBoxCache.clear();
    }
    /**
     * Tüm kaynakları temizler.
     * BIMViewer.dispose() içinde çağrılmalı.
     */
    dispose() {
        // Klavye event listener'ını kaldır
        if (this._keyHandler) {
            window.removeEventListener('keydown', this._keyHandler);
            this._keyHandler = null;
        }
        // ViewCube sync döngüsünü durdur
        if (this._viewCubeRafId !== null) {
            cancelAnimationFrame(this._viewCubeRafId);
            this._viewCubeRafId = null;
        }
        // ViewCube DOM'dan kaldır
        if (this._viewCubeEl && this._viewCubeEl.parentNode) {
            this._viewCubeEl.parentNode.removeChild(this._viewCubeEl);
            this._viewCubeEl = null;
        }
        // OrthoCamera'yı temizle
        this._orthoCamera = null;
        this._elementBoxCache.clear();
        console.log('[CameraPresets] Kaynaklar temizlendi.');
    }
    // ─── Keyboard Shortcuts ───────────────────────────────────────────────────
    /**
     * Klavye kısayollarını bağlar.
     *
     * Numpad 1 → Ön
     * Numpad 3 → Sağ
     * Numpad 7 → Üst
     * Numpad 5 → Perspektif/Ortografik toggle
     * F        → Seçilen element'e zoom (fitToModel fallback)
     * Home     → Tüm modele zoom
     */
    _bindKeyboard() {
        this._keyHandler = (e) => {
            // Input alanları odakta ise kısayolları devre dışı bırak
            const target = e.target;
            if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA')
                return;
            switch (e.code) {
                case 'Numpad1':
                    e.preventDefault();
                    this.goToPreset('front');
                    break;
                case 'Numpad3':
                    e.preventDefault();
                    this.goToPreset('right');
                    break;
                case 'Numpad7':
                    e.preventDefault();
                    this.goToPreset('top');
                    break;
                case 'Numpad5':
                    e.preventDefault();
                    this.toggleProjection();
                    break;
                case 'KeyF':
                    e.preventDefault();
                    // Gelecekte: seçili element varsa fitToElement, yoksa fitToModel
                    this.fitToModel();
                    break;
                case 'Home':
                    e.preventDefault();
                    this.fitToModel();
                    break;
                default:
                    break;
            }
        };
        window.addEventListener('keydown', this._keyHandler);
    }
    // ─── Projeksiyon Geçiş Yardımcıları ──────────────────────────────────────
    /**
     * Perspektif → Ortografik geçiş.
     *
     * OrthographicCamera boyutları viewport aspect ratio'sundan hesaplanır.
     * Kamera pozisyonu korunur (sadece projeksiyon matrisi değişir).
     */
    _switchToOrtho() {
        const aspect = this._viewport.clientWidth / this._viewport.clientHeight;
        const size = ORTHO_FRUSTUM_SIZE;
        // Mevcut sahnenin bounding box'ına göre frustum boyutunu ölçekle
        const box = this._computeSceneBoundingBox();
        let frustumSize = size;
        if (!box.isEmpty()) {
            const boxSize = box.getSize(new THREE.Vector3());
            frustumSize = Math.max(boxSize.x, boxSize.y, boxSize.z) * 0.75;
        }
        this._orthoCamera = new THREE.OrthographicCamera(-frustumSize * aspect, // left
        frustumSize * aspect, // right
        frustumSize, // top
        -frustumSize, // bottom
        0.1, // near
        10000);
        // Perspektif kameranın konumunu koru
        this._orthoCamera.position.copy(this._perspCamera.position);
        this._orthoCamera.quaternion.copy(this._perspCamera.quaternion);
        this._orthoCamera.up.copy(this._perspCamera.up);
        this._orthoCamera.updateProjectionMatrix();
        // OrbitControls'u yeni kamera ile güncelle
        this._controls.object = this._orthoCamera;
        this._controls.update();
        this._isOrtho = true;
        this.onCameraChanged?.(true, this._orthoCamera);
        console.log('[CameraPresets] Ortografik moda geçildi.');
    }
    /**
     * Ortografik → Perspektif geçiş.
     *
     * PerspectiveCamera ortho kameranın konumuna geri getirilir.
     */
    _switchToPerspective() {
        if (this._orthoCamera) {
            // Ortho kameranın konumunu perspektif kameraya aktar
            this._perspCamera.position.copy(this._orthoCamera.position);
            this._perspCamera.quaternion.copy(this._orthoCamera.quaternion);
            this._perspCamera.up.copy(this._orthoCamera.up);
            this._perspCamera.updateProjectionMatrix();
            // OrbitControls'u perspektif kameraya geri al
            this._controls.object = this._perspCamera;
            this._controls.update();
            this._orthoCamera = null;
        }
        this._isOrtho = false;
        this.onCameraChanged?.(false, this._perspCamera);
        console.log('[CameraPresets] Perspektif moda geçildi.');
    }
    // ─── Kamera Yardımcıları ──────────────────────────────────────────────────
    /** Aktif kamerayı döndür (perspektif veya ortografik) */
    _getActiveCamera() {
        return this._isOrtho && this._orthoCamera
            ? this._orthoCamera
            : this._perspCamera;
    }
    /**
     * Modelin dünya koordinatlarındaki merkezini döndürür.
     * Model yoksa (0, 0, 0) döner.
     */
    _getModelCenter() {
        const box = this._computeSceneBoundingBox();
        if (box.isEmpty())
            return new THREE.Vector3(0, 0, 0);
        return box.getCenter(new THREE.Vector3());
    }
    /**
     * Bir bounding box'ı tam görecek şekilde kamerayı konumlandırır.
     *
     * Hesaplama:
     *   distance = (maxDim / 2) / tan(FOV / 2) × padding
     *
     * Kamera, kutudan izometrik yönde (1, 0.8, 1) belirtilen mesafede konumlanır.
     */
    _fitToBox(box, duration) {
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);
        const activeCamera = this._getActiveCamera();
        let distance;
        if (activeCamera instanceof THREE.PerspectiveCamera) {
            const fovRad = THREE.MathUtils.degToRad(activeCamera.fov);
            distance = (maxDim / 2) / Math.tan(fovRad / 2) * 1.5;
        }
        else {
            // Ortografik kamera: frustum boyutunu güncelle
            distance = maxDim * 2;
            this._updateOrthoFrustum(maxDim);
        }
        // Mevcut kamera yönünü koru (sadece mesafeyi ayarla)
        const dir = activeCamera.position.clone()
            .sub(this._controls.target)
            .normalize();
        // Sıfır vektör kontrolü (kamera tam hedefte ise varsayılan yön kullan)
        if (dir.lengthSq() < 0.001) {
            dir.set(1, 0.8, 1).normalize();
        }
        const targetPos = center.clone().addScaledVector(dir, distance);
        animateCamera(activeCamera, this._controls, targetPos, center, duration);
    }
    /**
     * Ortografik kamera frustum'unu yeni boyuta göre günceller.
     */
    _updateOrthoFrustum(size) {
        const cam = this._orthoCamera;
        if (!cam)
            return;
        const aspect = this._viewport.clientWidth / this._viewport.clientHeight;
        const half = size * 0.75;
        cam.left = -half * aspect;
        cam.right = half * aspect;
        cam.top = half;
        cam.bottom = -half;
        cam.updateProjectionMatrix();
    }
    // ─── Bounding Box Hesaplamaları ───────────────────────────────────────────
    /**
     * Sahnedeki tüm görünür mesh'lerin bounding box'ını hesaplar.
     *
     * GridHelper ve AxesHelper gibi yardımcı elemanlar hariç tutulur.
     * (İsimlerine veya type'larına göre filtrelenir)
     */
    _computeSceneBoundingBox() {
        const box = new THREE.Box3();
        this._scene.traverse((obj) => {
            // GridHelper ve AxesHelper'ı hariç tut
            if (obj instanceof THREE.GridHelper ||
                obj instanceof THREE.AxesHelper ||
                !obj.visible)
                return;
            if (obj instanceof THREE.Mesh) {
                const meshBox = new THREE.Box3().setFromObject(obj);
                if (!meshBox.isEmpty()) {
                    box.union(meshBox);
                }
            }
        });
        return box;
    }
    /**
     * Verilen expressId'ye sahip mesh'i sahnede bulur ve bounding box döndürür.
     *
     * @thatopen/fragments mesh'lerinde userData.expressID bulunabilir.
     * Eşleşen mesh yoksa null döner.
     */
    _findElementBox(expressId) {
        let found = null;
        this._scene.traverse((obj) => {
            if (found)
                return; // Zaten bulundu
            if (obj instanceof THREE.Mesh) {
                const id = obj.userData['expressID'];
                if (id === expressId || id === String(expressId)) {
                    found = new THREE.Box3().setFromObject(obj);
                }
            }
        });
        return found;
    }
    /**
     * Bir katın tüm elementlerinin bounding box'ını hesaplar.
     *
     * storeyInfo.elementIds kullanılarak sahnedeki eşleşen mesh'ler bulunur.
     * Her eleman için _findElementBox çağrısı pahalı olabilir;
     * bu nedenle tek bir traverse ile tüm katı taranır.
     */
    _computeStoreyBoundingBox(storeyInfo) {
        const idSet = new Set(storeyInfo.elementIds);
        const box = new THREE.Box3();
        this._scene.traverse((obj) => {
            if (obj instanceof THREE.Mesh) {
                const id = obj.userData['expressID'];
                const numId = typeof id === 'string' ? parseInt(id, 10) : id;
                if (numId !== undefined && !isNaN(numId) && idSet.has(numId)) {
                    const meshBox = new THREE.Box3().setFromObject(obj);
                    if (!meshBox.isEmpty()) {
                        box.union(meshBox);
                    }
                }
            }
        });
        return box;
    }
    /**
     * Element ID'leriyle eşleşen mesh bulunamazsa tahmini bir bounding box oluşturur.
     *
     * Tüm sahne bounding box'ının XZ boyutları alınır, Y ekseninde
     * elevation'a göre 3.5m yüksekliğinde bir dilim oluşturulur.
     */
    _estimateStoreyBox(storeyInfo) {
        const sceneBox = this._computeSceneBoundingBox();
        if (sceneBox.isEmpty()) {
            // Tamamen varsayılan: 20×3.5×20 metre kutu
            const el = storeyInfo.elevation;
            return new THREE.Box3(new THREE.Vector3(-10, el, -10), new THREE.Vector3(10, el + 3.5, 10));
        }
        const size = sceneBox.getSize(new THREE.Vector3());
        const center = sceneBox.getCenter(new THREE.Vector3());
        const el = storeyInfo.elevation;
        return new THREE.Box3(new THREE.Vector3(center.x - size.x / 2, el, center.z - size.z / 2), new THREE.Vector3(center.x + size.x / 2, el + 3.5, center.z + size.z / 2));
    }
    // ─── ViewCube ─────────────────────────────────────────────────────────────
    /**
     * HTML/CSS ViewCube oluşturur ve viewport'a ekler.
     *
     * CSS 3D transform ile her yüze isim etiketi verilir.
     * Tıklamalar preset geçişi tetikler.
     *
     * Tasarım: sağ üst köşe, 80×80px, yarı saydam koyu arka plan,
     * hover'da parlayan yüzeyler.
     */
    _createViewCube() {
        // ViewCube kapsayıcısı
        const wrapper = document.createElement('div');
        wrapper.id = 'bv-viewcube';
        wrapper.setAttribute('aria-label', 'ViewCube navigasyon küpü');
        wrapper.setAttribute('role', 'navigation');
        // Stil tanımları — inline CSS (harici dosya gerekmez)
        wrapper.style.cssText = `
      position: absolute;
      top: 16px;
      right: 16px;
      width: 80px;
      height: 80px;
      z-index: 100;
      perspective: 300px;
      perspective-origin: 50% 50%;
      user-select: none;
      pointer-events: auto;
    `;
        // Küp iç kapsayıcısı (CSS transform-style: preserve-3d)
        const cube = document.createElement('div');
        cube.id = 'bv-viewcube-inner';
        cube.style.cssText = `
      width: 100%;
      height: 100%;
      position: relative;
      transform-style: preserve-3d;
      transition: none;
    `;
        // Yüz tanımları: [preset, label, transform, bgColor]
        const faces = [
            ['front', 'Ön', 'translateZ(40px)', 'rgba(60,80,120,0.85)'],
            ['back', 'Arka', 'rotateY(180deg) translateZ(40px)', 'rgba(60,80,120,0.85)'],
            ['right', 'Sağ', 'rotateY(90deg) translateZ(40px)', 'rgba(70,90,130,0.85)'],
            ['left', 'Sol', 'rotateY(-90deg) translateZ(40px)', 'rgba(70,90,130,0.85)'],
            ['top', 'Üst', 'rotateX(90deg) translateZ(40px)', 'rgba(50,70,110,0.85)'],
            ['bottom', 'Alt', 'rotateX(-90deg) translateZ(40px)', 'rgba(50,70,110,0.85)'],
        ];
        for (const [preset, label, transform, bg] of faces) {
            const face = document.createElement('button');
            face.setAttribute('data-preset', preset);
            face.setAttribute('aria-label', `${label} görünümüne geç`);
            face.style.cssText = `
        position: absolute;
        width: 80px;
        height: 80px;
        background: ${bg};
        border: 1px solid rgba(100,140,220,0.4);
        color: rgba(180,210,255,0.9);
        font-size: 11px;
        font-family: 'Inter', system-ui, sans-serif;
        font-weight: 500;
        letter-spacing: 0.05em;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(4px);
        transition: background 0.15s, color 0.15s;
        outline: none;
        top: 0; left: 0;
        transform: ${transform};
        backface-visibility: visible;
      `;
            face.textContent = label;
            // Hover efekti
            face.addEventListener('mouseenter', () => {
                face.style.background = 'rgba(90,130,220,0.9)';
                face.style.color = '#ffffff';
            });
            face.addEventListener('mouseleave', () => {
                face.style.background = bg;
                face.style.color = 'rgba(180,210,255,0.9)';
            });
            // Tıklamada preset geçişi
            face.addEventListener('click', (e) => {
                e.stopPropagation();
                this.goToPreset(preset);
            });
            cube.appendChild(face);
        }
        wrapper.appendChild(cube);
        this._viewport.appendChild(wrapper);
        this._viewCubeEl = cube;
    }
    /**
     * ViewCube'u kamera rotasyonuyla senkron tutar.
     *
     * Her animation frame'de kameranın quaternion'undan elde edilen
     * Euler açıları CSS transform olarak küpe uygulanır.
     *
     * NOT: Kamera lookAt(target) kullandığı için quaternion doğrudan
     * CSS'e aktarılır (ters rotasyon uygulanır — küp sahnedeki dünyayı yansıtır).
     */
    _startViewCubeSync() {
        const activeCamera = this._getActiveCamera();
        const sync = () => {
            this._viewCubeRafId = requestAnimationFrame(sync);
            if (!this._viewCubeEl)
                return;
            // Kameranın quaternion'unu al ve tersini hesapla
            const q = activeCamera.quaternion.clone().invert();
            // CSS matrix3d ile CSS transform uygula
            const matrix = new THREE.Matrix4().makeRotationFromQuaternion(q);
            const e = matrix.elements;
            // Three.js matrix column-major, CSS transform row-major
            this._viewCubeEl.style.transform = `
        matrix3d(
          ${e[0]},  ${e[1]},  ${e[2]},  0,
          ${e[4]},  ${e[5]},  ${e[6]},  0,
          ${e[8]},  ${e[9]},  ${e[10]}, 0,
          0,        0,        0,        1
        )
      `;
        };
        this._viewCubeRafId = requestAnimationFrame(sync);
    }
}
//# sourceMappingURL=cameraPresets.js.map