/**
 * sceneSetup.ts
 *
 * Three.js sahne kurulumundan sorumlu modül.
 *
 * Bu modül şunları oluşturur ve yapılandırır:
 *  - THREE.Scene          → sahne grafiği (model, ışıklar, yardımcı elemanlar)
 *  - THREE.PerspectiveCamera → perspektif kamera
 *  - THREE.WebGLRenderer  → GPU tabanlı render motoru (ACES tone mapping, sRGB)
 *  - OrbitControls        → fare/dokunmatik ekran ile kamera kontrolü
 *  - Işıklandırma         → ambient + directional (gölgeli) + hemisphere
 *  - GridHelper           → zemin ızgarası
 *  - AxesHelper           → X/Y/Z eksen göstergesi
 *
 * ─── RENDER KALİTE NOTLARI ───────────────────────────────────────────────
 *
 *  logarithmicDepthBuffer:
 *    BIM modellerinde binlerce yüzey aynı düzlemde üst üste gelebilir
 *    (örn. döşeme + duvar kesişimi). Standart doğrusal derinlik tamponu
 *    bu durumda "z-fighting" (titreşen piksel artefaktları) üretir.
 *    Logaritmik tampon, yakın ve uzak düzlemlerdeki hassasiyeti dengeler.
 *
 *  ACESFilmicToneMapping:
 *    Sinema kalitesi renk dönüşümü. HDR aydınlatma değerlerini (0'ın
 *    üzerindeki float) ekrana sığacak 0-1 aralığına doğal görünümlü
 *    şekilde eşler. Düz beyaz yerine yumuşak parlaklık rolloff sağlar.
 *
 *  SRGBColorSpace:
 *    Three.js r152+ varsayılanı. Renderer çıktısını sRGB renk uzayına
 *    dönüştürür — tarayıcı ve monitör beklentileriyle uyumlu.
 *
 *  PCFSoftShadowMap:
 *    Percentage Closer Filtering ile yumuşatılmış gölgeler.
 *    Hard shadow yerine daha gerçekçi kenar geçişi sağlar.
 *
 * ─── GELECEKTEKİ GELİŞTİRMELER ──────────────────────────────────────────
 *  - SSAO post-processing (ambient occlusion)
 *  - HDR PMREM environment map (EXR/HDR dosyası)
 *  - Bloom post-processing (parlak yüzeyler)
 *  - Kamera animasyonu (fly-to seçili eleman)
 *  - Ortografik projeksiyon modu (plan/kesit görünümü)
 */
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ─── 1. Sahne ─────────────────────────────────────────────────────────────────
/**
 * THREE.Scene oluşturur ve temel ayarları yapar.
 *
 * background: null → Arka plan CSS'den gelir (--color-bg-deep: #1a1a2e).
 * Bu sayede renderer ve HTML arka planı arasında renk uyumsuzluğu olmaz.
 * Opacity blending için alpha: true renderer ayarıyla birlikte kullanılır.
 */
function createScene() {
    const scene = new THREE.Scene();
    // Sahne arka planı CSS'e bırakılıyor (renderer alpha: true ile şeffaf)
    scene.background = null;
    // İsteğe bağlı: Sis efekti (büyük açık alan modellerde uzak elemanları gizler)
    // scene.fog = new THREE.FogExp2(0x1a1a2e, 0.002);
    return scene;
}
// ─── 2. Kamera ────────────────────────────────────────────────────────────────
/**
 * PerspectiveCamera oluşturur.
 *
 * FOV 60°: İnsan gözüne yakın görüş açısı. 45° dar (sıkışık), 75° geniş
 *          (balık gözü distorsiyonu). BIM için 60° ideal denge noktası.
 *
 * Near 0.1: Kameranın önündeki minimum görünür mesafe (metre cinsinden).
 *           Çok küçük değer (örn. 0.001) z-fighting'i artırır.
 *
 * Far 10000: BIM modelleri büyük yerleşke planları içerebilir.
 *            10km mesafeye kadar görünürlük sağlar.
 *
 * @param width  - Viewport genişliği (aspect ratio hesabı için)
 * @param height - Viewport yüksekliği
 */
function createCamera(width, height) {
    const camera = new THREE.PerspectiveCamera(60, // FOV (derece) — dikey görüş açısı
    width / height, // Aspect ratio — viewport oranı
    0.1, // Near clipping plane (metre)
    10000 // Far clipping plane (metre)
    );
    // Başlangıç kamera konumu: modelin dışından izometrik görünüm
    // IFC modeli yüklenince kamera modele otomatik odaklanacak (fly-to)
    camera.position.set(30, 20, 30);
    camera.lookAt(0, 0, 0);
    return camera;
}
// ─── 3. Renderer ──────────────────────────────────────────────────────────────
/**
 * WebGLRenderer oluşturur ve yapılandırır.
 *
 * Kalite ve performans dengesi BIM görselleştirme için optimize edildi.
 *
 * @param width  - İlk render genişliği
 * @param height - İlk render yüksekliği
 */
function createRenderer(width, height) {
    const renderer = new THREE.WebGLRenderer({
        // Kenar yumuşatma — özellikle IFC çizgilerinde önemli
        antialias: true,
        // Şeffaf arka plan — CSS arka planı görünür
        alpha: true,
        // GPU güç tercihi: 'high-performance' dedike GPU kullanır (varsa)
        // Laptoplarda entegre/dedike GPU seçimi burada yapılır
        powerPreference: 'high-performance',
        // Logaritmik derinlik tamponu — BIM'de z-fighting'i önler
        // NOT: Bu ayar bazı post-processing efektleriyle çelişebilir
        logarithmicDepthBuffer: true,
    });
    // ── Boyut ve Piksel Oranı ──────────────────────────────────────────────
    renderer.setSize(width, height);
    // devicePixelRatio: Retina/HiDPI ekranlar için örnekleme oranı
    // 2 ile sınırlıyoruz: 3× ve üzeri oranlar performansı belirgin düşürür
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    // ── Renk Uzayı ────────────────────────────────────────────────────────
    // Three.js r152+ varsayılanı: sRGB çıktı.
    // IFC malzemeleri lineer renk uzayında tanımlanır, renderer sRGB'e çevirir.
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    // ── Ton Eşleme (Tone Mapping) ─────────────────────────────────────────
    // ACES Filmic: Sinema kalitesi HDR → LDR dönüşümü
    // Parlak yüzeylerde (cam, metal) gerçekçi parlaklık rolloff sağlar
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2; // Hafif parlak — kapalı mekan BIM için uygun
    // ── Gölgeler ──────────────────────────────────────────────────────────
    renderer.shadowMap.enabled = true;
    // PCFSoft: Yumuşak kenar geçişli gölgeler (en iyi kalite/performans dengesi)
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    return renderer;
}
// ─── 4. Işıklar ───────────────────────────────────────────────────────────────
/**
 * Sahne aydınlatma sistemini oluşturur.
 *
 * Üç katmanlı aydınlatma stratejisi:
 *  1. AmbientLight    → Gölgeli alanları aydınlatır (düz, yönsüz ışık)
 *  2. DirectionalLight → Ana ışık kaynağı, gölge üretir (güneş simülasyonu)
 *  3. HemisphereLight  → Gökyüzü/zemin renk gradyanı, doğal görünüm
 *
 * @param scene - Işıkların ekleneceği sahne
 */
function createLights(scene) {
    // ── 1. Ambient Light (Ortam Işığı) ────────────────────────────────────
    // Tüm yüzeyleri eşit aydınlatır, gölge üretmez.
    // Çok yüksek intensity tüm sahnei düzleştirir (derinlik kaybı).
    const ambientLight = new THREE.AmbientLight(0xffffff, // Beyaz renk
    0.6 // Intensity — yeterince aydınlık ama DirectionalLight'ı ezmez
    );
    scene.add(ambientLight);
    // ── 2. Directional Light (Yönlü Işık — Ana Güneş) ────────────────────
    // Paralel ışın huzmesi — güneşi simüle eder. Gölge üretir.
    // Konum: sağ üst köşe (50, 80, 50) — klasik 3/4 aydınlatma pozisyonu
    const directionalLight = new THREE.DirectionalLight(0xffffff, // Beyaz güneş ışığı
    1.0 // Ana ışık intensity
    );
    directionalLight.position.set(50, 80, 50);
    directionalLight.castShadow = true;
    // Gölge haritası çözünürlüğü: 2048×2048
    // 4096 daha keskin ama GPU belleği 4× artar; BIM için 2048 yeterli
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    // Gölge kamerası (ortografik projeksiyon) — sahnedeki modeli kapsamalı
    // Frustum çok geniş → gölge haritası piksel başına büyük alan = bulanık gölge
    // Frustum çok dar  → kapsam dışındaki objeler gölge üretemez
    const shadowCam = directionalLight.shadow.camera;
    shadowCam.left = -100;
    shadowCam.right = 100;
    shadowCam.top = 100;
    shadowCam.bottom = -100;
    shadowCam.near = 0.5;
    shadowCam.far = 500;
    // Gölge bias: "shadow acne" (yüzeyin kendi kendine gölgelenmesi) önleme
    // Negatif değer: yüzeyi biraz öne çeker, self-shadow artefaktlarını gizler
    directionalLight.shadow.bias = -0.0005;
    scene.add(directionalLight);
    // ── 3. Hemisphere Light (Gökyüzü/Zemin Gradyan Işığı) ─────────────────
    // Yukarıdan gelen mavi gökyüzü + aşağıdan gelen kahverengi zemin yansıması.
    // Outdoor ortamların doğal renk atmosferini simüle eder.
    const hemisphereLight = new THREE.HemisphereLight(0xb1e1ff, // Gökyüzü rengi: açık mavi
    0xb97a20, // Zemin rengi: toprak/kumsal sarısı
    0.3 // Düşük intensity — DirectionalLight'ın baskın kalması için
    );
    scene.add(hemisphereLight);
}
// ─── 5. Grid ve Eksen Yardımcıları ───────────────────────────────────────────
/**
 * Zemin ızgarası ve eksen göstergesi oluşturur.
 *
 * GridHelper: BIM modelinin oturduğu zemini gösterir.
 *             IFC'de Z ekseni yukarıdır ama Three.js Y-up kullanır.
 *             @thatopen/fragments bu dönüşümü otomatik yapar.
 *
 * AxesHelper: X (kırmızı) / Y (yeşil) / Z (mavi) eksenlerini gösterir.
 *             IFC koordinat sistemiyle karşılaştırma için faydalı.
 *
 * @param scene - Yardımcıların ekleneceği sahne
 */
function createGrid(scene) {
    // ── Zemin Izgarası ─────────────────────────────────────────────────────
    // size: 200 birim × 200 birim kare alan (metre → ~200m × 200m)
    // divisions: 50 → her 4 metrede bir çizgi
    const grid = new THREE.GridHelper(200, // Toplam ızgara boyutu (metre)
    50, // Bölme sayısı (denser = daha detaylı ızgara)
    0x888888, // Merkez çizgi rengi (daha parlak gri)
    0x444444 // Kenar çizgi rengi (koyu gri — arka plana karışsın)
    );
    // Izgarayı tam zemin düzeyine yerleştir
    grid.position.y = 0;
    // Izgara çizgileri kamera ile aynı derinlikte olduğunda z-fighting yapar.
    // Hafif negatif Y offset ile bu durumu önle:
    grid.position.y = -0.001;
    scene.add(grid);
    // ── Eksen Göstergesi ───────────────────────────────────────────────────
    // X = Kırmızı, Y = Yeşil (yukarı), Z = Mavi
    // size: 10 birim — yeterince görünür ama modeli engellemez
    const axesHelper = new THREE.AxesHelper(10);
    scene.add(axesHelper);
}
// ─── 6. OrbitControls ─────────────────────────────────────────────────────────
/**
 * OrbitControls oluşturur ve yapılandırır.
 *
 * OrbitControls, kameranın bir merkez noktası etrafında döndürülmesini,
 * yaklaştırılıp uzaklaştırılmasını ve kaydırılmasını sağlar.
 *
 * @param camera   - Kontrol edilecek kamera
 * @param renderer - Event listener'ların bağlandığı renderer (canvas)
 */
function createControls(camera, renderer) {
    const controls = new OrbitControls(camera, renderer.domElement);
    // ── Damping (İnertia / Momentum) ──────────────────────────────────────
    // Kullanıcı fare/dokunmayı bıraktığında kamera yavaşça durur.
    // dampingFactor: 0 = anında dur, 1 = hiç durmaz (0.05-0.15 doğal hissettir)
    controls.enableDamping = true;
    controls.dampingFactor = 0.1;
    // ── Zoom Limitleri ─────────────────────────────────────────────────────
    controls.minDistance = 1; // 1 metreye kadar yaklaşılabilir
    controls.maxDistance = 1000; // 1km uzağa kadar çıkılabilir
    // ── Açı Limitleri ──────────────────────────────────────────────────────
    // maxPolarAngle: Math.PI = zemine bakış (90°)
    // 0.9 × Math.PI = 162° → zemin altına biraz bakabilir (bodrum incelemesi için)
    controls.minPolarAngle = 0; // Tam yukarı bakış (düşey)
    controls.maxPolarAngle = Math.PI * 0.9; // Zemin altına hafif bakış
    // ── Fare Buton Atamaları ───────────────────────────────────────────────
    controls.mouseButtons = {
        LEFT: THREE.MOUSE.ROTATE, // Sol tık: döndür
        MIDDLE: THREE.MOUSE.DOLLY, // Orta tık / scroll: zoom
        RIGHT: THREE.MOUSE.PAN, // Sağ tık: kaydır (pan)
    };
    // ── Dokunmatik Ekran Hareketleri ──────────────────────────────────────
    controls.touches = {
        ONE: THREE.TOUCH.ROTATE, // Tek parmak: döndür
        TWO: THREE.TOUCH.DOLLY_PAN, // İki parmak: zoom + kaydır
    };
    // ── Ek Seçenekler ─────────────────────────────────────────────────────
    controls.enablePan = true; // Pan aktif
    controls.panSpeed = 1.0; // Pan hızı
    controls.zoomSpeed = 1.2; // Zoom hızı (biraz hızlı — büyük modeller için)
    controls.rotateSpeed = 0.8; // Döndürme hızı (biraz yavaş — hassas kontrol)
    controls.screenSpacePanning = false; // true: pan kameranın UP yönünde, false: world Y'de
    return controls;
}
// ─── 7. Ana Başlatma Fonksiyonu ───────────────────────────────────────────────
/**
 * Tüm sahne bileşenlerini oluşturur, container'a bağlar ve
 * animation loop ile resize handler'ı başlatır.
 *
 * ÇAĞRI SIRASI:
 *   1. createScene()         → THREE.Scene
 *   2. createCamera()        → THREE.PerspectiveCamera
 *   3. createRenderer()      → THREE.WebGLRenderer (canvas container'a eklenir)
 *   4. createLights()        → Sahneye 3 ışık eklenir
 *   5. createGrid()          → Izgara + eksen yardımcıları
 *   6. createControls()      → OrbitControls
 *   7. Animation loop başlar (requestAnimationFrame)
 *   8. ResizeObserver bağlanır
 *
 * @param container - Renderer canvas'ının mount edileceği DOM elementi
 * @returns SceneContext — tüm sahne bileşenlerine referanslar + dispose()
 */
export function initScene(container) {
    console.log('[sceneSetup] Three.js sahnesi başlatılıyor...');
    // ── Mevcut boyutu al ───────────────────────────────────────────────────
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;
    // ── Bileşenleri oluştur ────────────────────────────────────────────────
    const scene = createScene();
    const camera = createCamera(width, height);
    const renderer = createRenderer(width, height);
    createLights(scene);
    createGrid(scene);
    const controls = createControls(camera, renderer);
    // ── Renderer canvas'ını container'a ekle ──────────────────────────────
    // domElement: WebGLRenderer'ın oluşturduğu <canvas> elementi
    renderer.domElement.style.display = 'block';
    container.appendChild(renderer.domElement);
    // ── Animation Loop ────────────────────────────────────────────────────
    // requestAnimationFrame: tarayıcının vsync döngüsüne bağlı (~60fps / 120fps)
    // NOT: Sadece controls.update() ve renderer.render() çağrılır.
    //      Gereksiz hesaplamalar buraya eklenmemeli — her kare çalışır!
    let animationFrameId;
    let isDisposed = false;
    /** Ek render callback'leri (CSS2DRenderer vb. için) */
    const onRenderCallbacks = [];
    /** Resize callback'leri (fragments LOD güncellemesi vb. için) */
    const onResizeCallbacks = [];
    function animate() {
        // Dispose edildikten sonra döngüyü durdur
        if (isDisposed)
            return;
        animationFrameId = requestAnimationFrame(animate);
        // Damping animasyonu için controls her karede güncellenmeli
        controls.update();
        // Sahneyi kameranın bakış açısından render et
        renderer.render(scene, camera);
        // Ek renderer'lar (CSS2DRenderer gibi) — her kare çağrılır
        for (const cb of onRenderCallbacks)
            cb();
    }
    // İlk kareyi başlat
    animate();
    console.log('[sceneSetup] Animation loop başlatıldı.');
    // ── Resize Handler ────────────────────────────────────────────────────
    // ResizeObserver: window.resize yerine container boyutunu izler.
    // Bu sayede sidebar açılıp kapandığında canvas doğru boyutlanır.
    const resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
            const { width: newWidth, height: newHeight } = entry.contentRect;
            if (newWidth === 0 || newHeight === 0)
                continue;
            // Kamera aspect ratio güncelle
            camera.aspect = newWidth / newHeight;
            camera.updateProjectionMatrix();
            // Renderer boyutunu güncelle
            renderer.setSize(newWidth, newHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            // Dış callback'leri tetikle (örn. fragments LOD güncellemesi)
            for (const cb of onResizeCallbacks)
                cb(newWidth, newHeight);
            console.log(`[sceneSetup] Yeniden boyutlandırıldı: ${Math.round(newWidth)}×${Math.round(newHeight)}px`);
        }
    });
    resizeObserver.observe(container);
    // ── Dispose Fonksiyonu ────────────────────────────────────────────────
    /**
     * Tüm Three.js kaynaklarını serbest bırakır.
     *
     * Memory leak önleme sırası (bağımlılık sırasına göre):
     *  1. Animation loop durdur
     *  2. ResizeObserver bağlantısını kes
     *  3. OrbitControls event listener'larını temizle
     *  4. Sahne grafiğini traverse ederek geometri + materyal dispose et
     *  5. Renderer'ı dispose et (WebGL context'i serbest bırak)
     *  6. Canvas'ı DOM'dan kaldır
     */
    function dispose() {
        console.log('[sceneSetup] Kaynaklar serbest bırakılıyor...');
        isDisposed = true;
        // 1. Animation loop'u durdur
        cancelAnimationFrame(animationFrameId);
        // 2. Resize observer'ı durdur
        resizeObserver.disconnect();
        // 3. OrbitControls event listener'larını temizle
        controls.dispose();
        // 4. Sahne grafiğini traverse et ve dispose et
        //    Three.js'de geometri ve materyaller GPU belleğinde tutulur.
        //    Manuel dispose çağrısı yapılmazsa memory leak oluşur.
        scene.traverse((object) => {
            if (object instanceof THREE.Mesh) {
                // Geometriyi serbest bırak (vertex buffer, index buffer)
                object.geometry.dispose();
                // Materyali serbest bırak (texture, shader)
                const materials = Array.isArray(object.material)
                    ? object.material
                    : [object.material];
                for (const material of materials) {
                    // Tüm texture map'leri dispose et
                    disposeTexturesFromMaterial(material);
                    material.dispose();
                }
            }
        });
        // Sahneyi temizle
        scene.clear();
        // 5. Renderer ve WebGL context'i serbest bırak
        renderer.dispose();
        // 6. Canvas'ı DOM'dan kaldır
        if (renderer.domElement.parentNode) {
            renderer.domElement.parentNode.removeChild(renderer.domElement);
        }
        console.log('[sceneSetup] ✓ Tüm kaynaklar serbest bırakıldı.');
    }
    console.log('[sceneSetup] ✓ Sahne başarıyla kuruldu.');
    return { scene, camera, renderer, controls, dispose, onRenderCallbacks, onResizeCallbacks };
}
// ─── 8. Yardımcı Fonksiyonlar ─────────────────────────────────────────────────
/**
 * Bir materyaldeki tüm texture map'leri dispose eder.
 *
 * Three.js materyalleri map, normalMap, roughnessMap gibi
 * çeşitli texture referansları tutabilir. Her biri GPU belleğinde
 * ayrı yer kaplar ve ayrıca dispose edilmesi gerekir.
 *
 * @param material - Dispose edilecek materyal
 */
function disposeTexturesFromMaterial(material) {
    // THREE.Material'ın bilinen texture property isimleri
    const textureKeys = [
        'map', 'lightMap', 'bumpMap', 'normalMap',
        'envMap', 'alphaMap', 'aoMap', 'displacementMap',
        'roughnessMap', 'metalnessMap', 'emissiveMap',
    ];
    for (const key of textureKeys) {
        const value = material[key];
        if (value instanceof THREE.Texture) {
            value.dispose();
        }
    }
}
/**
 * Sahneye verilen pozisyona kamerayı yönlendirir (fly-to animasyonu).
 *
 * IFC modeli yüklendikten sonra bounding box hesaplanır ve bu fonksiyon
 * ile kamera modeli tam çerçeveleyecek konuma getirilir.
 *
 * Kamera near/far ve OrbitControls min/maxDistance değerleri model boyutuna
 * göre dinamik olarak ayarlanır — bu sayede yakın zoom'da model kaybolmaz.
 *
 * @param camera   - Konumlandırılacak kamera
 * @param controls - Hedef noktasını güncellemek için
 * @param box      - Modelin bounding box'ı
 */
export function fitCameraToBox(camera, controls, box) {
    // Bounding box merkezi ve boyutu
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    // En büyük boyut (genişlik, yükseklik veya derinlik)
    const maxDim = Math.max(size.x, size.y, size.z);
    // FOV'a göre kameranın kaç birim uzakta durması gerektiği
    const fovRad = THREE.MathUtils.degToRad(camera.fov);
    const distance = (maxDim / 2) / Math.tan(fovRad / 2) * 1.5; // 1.5 = kenar boşluğu
    // ── Dinamik near/far ayarı ─────────────────────────────────────────────
    // Near çok küçük + far çok büyük → derinlik hassasiyeti bozulur ve
    // büyük IFC modellerinde yakın zoom'da yüzeyler yok olur.
    // Model boyutuna orantılı near/far: near = maxDim/1000, far = maxDim×200
    const dynNear = Math.max(0.01, maxDim * 0.001);
    const dynFar = Math.max(10000, maxDim * 200);
    camera.near = dynNear;
    camera.far = dynFar;
    camera.updateProjectionMatrix();
    // OrbitControls zoom limitleri de model boyutuna uyarlanır:
    // minDistance: modelin en küçük boyutunun %1'i kadar yaklaşılabilir
    // maxDistance: modelin en büyük boyutunun 20 katı uzağa çıkılabilir
    controls.minDistance = Math.max(0.1, maxDim * 0.01);
    controls.maxDistance = Math.max(1000, maxDim * 20);
    // Kamerayı modelin üst-sağ köşesine konumlandır
    const direction = new THREE.Vector3(1, 0.8, 1).normalize();
    camera.position.copy(center).addScaledVector(direction, distance);
    // Controls hedefini modelin merkezine al
    controls.target.copy(center);
    controls.update();
    console.log(`[sceneSetup] Kamera modele odaklandı: merkez ${center.toArray().map(v => v.toFixed(1)).join(', ')}, uzaklık ${distance.toFixed(1)}, near=${dynNear.toFixed(4)}, far=${dynFar.toFixed(0)}`);
}
//# sourceMappingURL=sceneSetup.js.map