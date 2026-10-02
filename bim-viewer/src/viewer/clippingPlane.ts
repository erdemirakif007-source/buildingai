/**
 * clippingPlane.ts
 *
 * BIM Viewer için kesit düzlemi (clipping plane) yöneticisi.
 *
 * ─── MİMARİ GENEL BAKIŞ ──────────────────────────────────────────────────────
 *
 *  ClippingPlaneManager
 *  ├── addClippingPlane(axis, position?)   → THREE.Plane oluştur, renderer'a ekle
 *  ├── removeClippingPlane(id)             → Belirli düzlemi kaldır
 *  ├── removeAllClippingPlanes()           → Tüm düzlemleri kaldır
 *  ├── flipPlane(id)                       → Düzlem normalini tersine çevir
 *  ├── setPlanePosition(id, pos)           → Düzlem pozisyonunu güncelle
 *  └── dispose()                           → Tüm kaynakları serbest bırak
 *
 * ─── CLIPPING TEKNİĞİ ────────────────────────────────────────────────────────
 *
 *  WebGL renderer'da globalClippingPlanes veya material.clippingPlanes kullanılır.
 *  Bu implementasyon renderer.clippingPlanes (global) yaklaşımını kullanır:
 *    renderer.localClippingEnabled = true
 *    renderer.clippingPlanes = [plane1, plane2, ...]
 *
 *  Görsel yardımcı (helper): Yarı-saydam MeshBasicMaterial ile düzlem mesh'i
 *  kullanıcıya düzlemin konumunu gösterir.
 *
 *  Mouse Drag:
 *    - Sol sürükleme: düzlemi ileri/geri kaydır
 *    - Shift + sürükleme: düzlemi döndür
 *
 * ─── STENCIL BUFFER NOTU ─────────────────────────────────────────────────────
 *
 *  Renderer stencil: true ile oluşturulmalı (sceneSetup.ts'de).
 *  Aşama 5'te kesit çizgisi efekti (caps) stencil tekniğiyle eklenecek.
 *  Şu an sadece düzlem ile kesim yapılıyor.
 *
 * ─── GELECEKTEKİ GELİŞTİRMELER ──────────────────────────────────────────────
 *  - Stencil buffer ile kesit yüzeyi renklendirme (caps)
 *  - Çoklu düzlem kombinasyonu (kutu kesit)
 *  - Düzlem kilidleme (sürüklemeyi devre dışı bırak)
 *  - Undo/redo desteği
 */

import * as THREE from 'three';
import type { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// ─── Tipler ────────────────────────────────────────────────────────────────────

/** Kesit düzleminin hangi eksende çalıştığı */
export type ClippingAxis = 'x' | 'y' | 'z';

/**
 * Tek bir kesit düzleminin tam yönetim verisi.
 */
export interface ClippingPlaneInfo {
  /** Benzersiz kimlik (örn. "cp-x-1716000000000") */
  id: string;
  /** Hangi eksende kesim yapıyor */
  axis: ClippingAxis;
  /** THREE.Plane nesnesi (normal + constant) */
  plane: THREE.Plane;
  /** Düzlemin konumu dünya koordinatında */
  position: number;
  /** Düzlem tersine çevrildi mi? */
  flipped: boolean;
  /** Görsel yardımcı (yarı-saydam mesh) */
  helperMesh: THREE.Mesh | null;
  /** Yardımcı görünür mü? */
  helperVisible: boolean;
}

/**
 * Düzlem eklendiğinde / kaldırıldığında tetiklenen callback.
 */
export type ClippingPlaneChangeCallback = (planes: ClippingPlaneInfo[]) => void;

// ─── Sabitler ──────────────────────────────────────────────────────────────────

/** Eksenlerin normal vektörleri (flipped: false durumu için) */
const AXIS_NORMALS: Record<ClippingAxis, THREE.Vector3> = {
  x: new THREE.Vector3(-1, 0, 0),
  y: new THREE.Vector3(0, -1, 0),
  z: new THREE.Vector3(0, 0, -1),
};

/** Helper mesh boyutu (metre) */
const HELPER_SIZE = 50;

/** Helper mesh opaklığı */
const HELPER_OPACITY = 0.18;

/** Sürükleme hassasiyeti (piksel başına birim) */
const DRAG_SENSITIVITY = 0.05;

/** Döndürme hassasiyeti (piksel başına radyan) */
const ROTATE_SENSITIVITY = 0.005;

// ─── Ana Sınıf ─────────────────────────────────────────────────────────────────

/**
 * BIM modelini kesmek için düzlem aracı.
 *
 * Kullanım:
 * ```ts
 * const mgr = new ClippingPlaneManager(scene, renderer, camera, controls);
 * mgr.addClippingPlane('y', 3.5);  // Y ekseninde, 3.5m'de
 * mgr.onPlanesChanged = (planes) => updateUI(planes);
 * ```
 */
export class ClippingPlaneManager {

  // ── Bağımlılıklar ────────────────────────────────────────────────────────

  private readonly _scene:    THREE.Scene;
  private readonly _renderer: THREE.WebGLRenderer;
  private readonly _camera:   THREE.PerspectiveCamera;
  private readonly _controls: OrbitControls;

  // ── Durum ────────────────────────────────────────────────────────────────

  /** Mevcut tüm kesit düzlemleri */
  private _planes: Map<string, ClippingPlaneInfo> = new Map();

  /** Kaç düzlem oluşturuldu (ID üretimi için) */
  private _counter = 0;

  // ── Sürükleme Durumu ─────────────────────────────────────────────────────

  private _isDragging    = false;
  private _dragPlaneId:   string | null = null;
  private _dragStartPos:  THREE.Vector2 = new THREE.Vector2();
  private _dragStartConst: number = 0;
  private _dragStartNormal: THREE.Vector3 = new THREE.Vector3();
  private _isShiftDrag   = false;

  // ── Raycaster (helper seçimi için) ───────────────────────────────────────

  private readonly _raycaster = new THREE.Raycaster();
  private readonly _mouse     = new THREE.Vector2();

  // ── Callback ─────────────────────────────────────────────────────────────

  /**
   * Herhangi bir düzlem eklendiğinde, kaldırıldığında veya değiştiğinde çağrılır.
   * UI güncellemesi için kullanılır.
   */
  onPlanesChanged: ClippingPlaneChangeCallback | null = null;

  // ── Event Handler Referansları ───────────────────────────────────────────

  private _onMouseDown: (e: MouseEvent) => void;
  private _onMouseMove: (e: MouseEvent) => void;
  private _onMouseUp:   (e: MouseEvent) => void;

  // ─── Constructor ──────────────────────────────────────────────────────────

  /**
   * @param scene    - Three.js sahne (helper mesh'ler buraya eklenir)
   * @param renderer - WebGL renderer (clippingPlanes ve stencil ayarı)
   * @param camera   - Perspektif kamera (raycasting için)
   * @param controls - OrbitControls (drag sırasında devre dışı bırakılır)
   */
  constructor(
    scene:    THREE.Scene,
    renderer: THREE.WebGLRenderer,
    camera:   THREE.PerspectiveCamera,
    controls: OrbitControls,
  ) {
    this._scene    = scene;
    this._renderer = renderer;
    this._camera   = camera;
    this._controls = controls;

    // Renderer ayarları
    this._renderer.localClippingEnabled = true;

    // Event handler'larını bağla
    this._onMouseDown = this._handleMouseDown.bind(this);
    this._onMouseMove = this._handleMouseMove.bind(this);
    this._onMouseUp   = this._handleMouseUp.bind(this);

    this._renderer.domElement.addEventListener('mousedown', this._onMouseDown);
    this._renderer.domElement.addEventListener('mousemove', this._onMouseMove);
    window.addEventListener('mouseup', this._onMouseUp);

    console.log('[ClippingPlaneManager] Başlatıldı. localClippingEnabled = true');
  }

  // ─── Public API ───────────────────────────────────────────────────────────

  /**
   * Yeni bir kesit düzlemi ekler.
   *
   * @param axis     - Kesim ekseni: 'x' | 'y' | 'z'
   * @param position - Düzlemin dünya koordinatındaki konumu (varsayılan: 0)
   * @returns Oluşturulan düzlemin ID'si
   */
  addClippingPlane(axis: ClippingAxis, position = 0): string {
    const id = `cp-${axis}-${Date.now()}-${this._counter++}`;

    // ── THREE.Plane oluştur ────────────────────────────────────────────────
    // THREE.Plane: normal * x + constant = 0
    // Kesen taraf: normal yönünde kalan objeler görünür
    const normal   = AXIS_NORMALS[axis].clone();
    const constant = position; // plane.constant = -dot(normal, point)
    const plane    = new THREE.Plane(normal, constant);

    // ── Renderer'a ekle ───────────────────────────────────────────────────
    this._renderer.clippingPlanes.push(plane);

    // ── Görsel helper oluştur ─────────────────────────────────────────────
    const helperMesh = this._createHelperMesh(axis, position);

    // Helper'a ID ata (raycasting ile tanımlama için)
    helperMesh.userData['clippingPlaneId'] = id;

    // ── PlaneInfo kaydet ──────────────────────────────────────────────────
    const info: ClippingPlaneInfo = {
      id,
      axis,
      plane,
      position,
      flipped: false,
      helperMesh,
      helperVisible: true,
    };

    this._planes.set(id, info);
    this._notifyChange();

    console.log(`[ClippingPlaneManager] Düzlem eklendi: ${id} (${axis} ekseni, pozisyon: ${position})`);
    return id;
  }

  /**
   * Belirtilen ID'li kesit düzlemini kaldırır.
   *
   * @param id - addClippingPlane() tarafından döndürülen ID
   */
  removeClippingPlane(id: string): void {
    const info = this._planes.get(id);
    if (!info) {
      console.warn(`[ClippingPlaneManager] Düzlem bulunamadı: ${id}`);
      return;
    }

    // Renderer'dan kaldır
    const idx = this._renderer.clippingPlanes.indexOf(info.plane);
    if (idx !== -1) {
      this._renderer.clippingPlanes.splice(idx, 1);
    }

    // Helper mesh'i sahneden kaldır
    this._removeHelperMesh(info);

    this._planes.delete(id);
    this._notifyChange();

    console.log(`[ClippingPlaneManager] Düzlem kaldırıldı: ${id}`);
  }

  /**
   * Tüm kesit düzlemlerini kaldırır.
   */
  removeAllClippingPlanes(): void {
    for (const id of this._planes.keys()) {
      const info = this._planes.get(id)!;
      const idx = this._renderer.clippingPlanes.indexOf(info.plane);
      if (idx !== -1) this._renderer.clippingPlanes.splice(idx, 1);
      this._removeHelperMesh(info);
    }

    this._planes.clear();
    this._notifyChange();

    console.log('[ClippingPlaneManager] Tüm düzlemler kaldırıldı.');
  }

  /**
   * Belirtilen düzlemi tersine çevirir (hangi tarafı kestiği değişir).
   *
   * @param id - Tersine çevrilecek düzlemin ID'si
   */
  flipPlane(id: string): void {
    const info = this._planes.get(id);
    if (!info) return;

    // Normali tersine çevir
    info.plane.normal.negate();
    info.plane.constant = -info.plane.constant;
    info.flipped = !info.flipped;

    // Helper rengini güncelle (tersine çevrilmiş düzlemler farklı renk göster)
    this._updateHelperColor(info);

    this._notifyChange();
    console.log(`[ClippingPlaneManager] Düzlem tersine çevrildi: ${id}`);
  }

  /**
   * Düzlemin pozisyonunu programatik olarak günceller.
   *
   * @param id       - Güncellenecek düzlemin ID'si
   * @param position - Yeni pozisyon (dünya koordinatında)
   */
  setPlanePosition(id: string, position: number): void {
    const info = this._planes.get(id);
    if (!info) return;

    info.position = position;
    this._applyPosition(info, position);
    this._notifyChange();
  }

  /**
   * Düzlem helper'ının görünürlüğünü toggle eder.
   *
   * @param id - Düzlemin ID'si
   */
  toggleHelperVisibility(id: string): void {
    const info = this._planes.get(id);
    if (!info || !info.helperMesh) return;

    info.helperVisible = !info.helperVisible;
    info.helperMesh.visible = info.helperVisible;
    this._notifyChange();
  }

  /**
   * Kat kesiti modu: Y ekseninde verilen elevation'da düzlem ekler
   * veya mevcut Y düzlemini günceller.
   *
   * @param elevation - Kat kot değeri (metre)
   * @param existingId - Güncellenecek mevcut düzlem ID'si (varsa)
   * @returns Düzlem ID'si
   */
  setFloorSection(elevation: number, existingId?: string): string {
    if (existingId && this._planes.has(existingId)) {
      this.setPlanePosition(existingId, elevation);
      return existingId;
    }
    return this.addClippingPlane('y', elevation);
  }

  // ─── Getter'lar ───────────────────────────────────────────────────────────

  /** Tüm aktif düzlemlerin listesi (kopyası) */
  get planes(): ClippingPlaneInfo[] {
    return Array.from(this._planes.values());
  }

  /** Aktif düzlem sayısı */
  get planeCount(): number {
    return this._planes.size;
  }

  /**
   * Tüm kaynakları serbest bırakır (event listener'lar, mesh'ler, düzlemler).
   */
  dispose(): void {
    this.removeAllClippingPlanes();

    this._renderer.domElement.removeEventListener('mousedown', this._onMouseDown);
    this._renderer.domElement.removeEventListener('mousemove', this._onMouseMove);
    window.removeEventListener('mouseup', this._onMouseUp);

    this._renderer.localClippingEnabled = false;
    console.log('[ClippingPlaneManager] Dispose edildi.');
  }

  // ─── Özel: Helper Mesh ────────────────────────────────────────────────────

  /**
   * Düzlem için yarı-saydam görsel yardımcı mesh oluşturur.
   *
   * Eksene göre döndürülmüş kare düzlem:
   *  X ekseni → YZ düzleminde (90° Y döndürme)
   *  Y ekseni → XZ düzleminde (varsayılan yatay)
   *  Z ekseni → XY düzleminde (90° X döndürme)
   */
  private _createHelperMesh(axis: ClippingAxis, position: number): THREE.Mesh {
    const geo = new THREE.PlaneGeometry(HELPER_SIZE, HELPER_SIZE, 1, 1);
    const mat = new THREE.MeshBasicMaterial({
      color:       this._getAxisColor(axis),
      transparent: true,
      opacity:     HELPER_OPACITY,
      side:        THREE.DoubleSide,
      depthWrite:  false,
    });

    const mesh = new THREE.Mesh(geo, mat);
    mesh.name = `clipping-helper-${axis}`;

    // Eksene göre döndür ve konumlandır
    this._positionHelperMesh(mesh, axis, position);

    this._scene.add(mesh);
    return mesh;
  }

  /**
   * Helper mesh'i eksen ve pozisyona göre döndürür ve konumlandırır.
   */
  private _positionHelperMesh(
    mesh: THREE.Mesh,
    axis: ClippingAxis,
    position: number,
  ): void {
    mesh.rotation.set(0, 0, 0);
    mesh.position.set(0, 0, 0);

    switch (axis) {
      case 'x':
        // PlaneGeometry varsayılan XY düzleminde → YZ için 90° Y döndür
        mesh.rotation.y = Math.PI / 2;
        mesh.position.x = -position; // normal -X, constant = pos → world x = -pos
        break;

      case 'y':
        // PlaneGeometry varsayılan XY düzleminde → XZ için 90° X döndür
        mesh.rotation.x = -Math.PI / 2;
        mesh.position.y = -position;
        break;

      case 'z':
        // PlaneGeometry varsayılan XY düzleminde → XY olduğu gibi, Z konumlandır
        mesh.position.z = -position;
        break;
    }
  }

  /**
   * Mevcut bir düzlemin pozisyonunu günceller (hem THREE.Plane hem helper).
   */
  private _applyPosition(info: ClippingPlaneInfo, position: number): void {
    // THREE.Plane constant güncelle
    // Normal flipped değilse: normal yönünde constant = position
    // Flipped ise constant ters işaretli
    const sign = info.flipped ? -1 : 1;
    info.plane.constant = sign * position;

    // Helper mesh'i taşı
    if (info.helperMesh) {
      this._positionHelperMesh(info.helperMesh, info.axis, position);
    }
  }

  /**
   * Helper mesh'i sahneden kaldırır ve kaynaklarını serbest bırakır.
   */
  private _removeHelperMesh(info: ClippingPlaneInfo): void {
    if (info.helperMesh) {
      this._scene.remove(info.helperMesh);
      info.helperMesh.geometry.dispose();
      (info.helperMesh.material as THREE.Material).dispose();
      info.helperMesh = null;
    }
  }

  /**
   * Helper materyalinin rengini günceller (flipped durumu yansıtır).
   */
  private _updateHelperColor(info: ClippingPlaneInfo): void {
    if (!info.helperMesh) return;
    const mat = info.helperMesh.material as THREE.MeshBasicMaterial;
    // Flipped düzlemler biraz daha soluk renk
    const baseColor = this._getAxisColor(info.axis);
    mat.color.set(baseColor);
    mat.opacity = info.flipped ? HELPER_OPACITY * 0.7 : HELPER_OPACITY;
  }

  /**
   * Eksene göre helper rengi döndürür.
   *  X → kırmızımsı
   *  Y → yeşilimsi
   *  Z → mavimsi
   */
  private _getAxisColor(axis: ClippingAxis): number {
    switch (axis) {
      case 'x': return 0xff4444;
      case 'y': return 0x44ff44;
      case 'z': return 0x4488ff;
    }
  }

  // ─── Özel: Mouse Sürükleme ────────────────────────────────────────────────

  /**
   * Mousedown: hangi helper'a tıklandığını tespit et, sürüklemeyi başlat.
   */
  private _handleMouseDown(e: MouseEvent): void {
    if (e.button !== 0) return; // Sadece sol tık

    const canvas   = this._renderer.domElement;
    const rect     = canvas.getBoundingClientRect();
    this._mouse.set(
      ((e.clientX - rect.left) / rect.width)  * 2 - 1,
      -((e.clientY - rect.top)  / rect.height) * 2 + 1,
    );

    this._raycaster.setFromCamera(this._mouse, this._camera);

    // Tüm helper mesh'lerle raycasting yap
    const helperMeshes: THREE.Object3D[] = [];
    for (const info of this._planes.values()) {
      if (info.helperMesh && info.helperVisible) {
        helperMeshes.push(info.helperMesh);
      }
    }

    if (helperMeshes.length === 0) return;

    const intersects = this._raycaster.intersectObjects(helperMeshes, false);
    if (intersects.length === 0) return;

    // En yakın helper'ı bul
    const hitMesh = intersects[0]!.object as THREE.Mesh;
    const planeId = hitMesh.userData['clippingPlaneId'] as string | undefined;
    if (!planeId) return;

    const info = this._planes.get(planeId);
    if (!info) return;

    // Sürüklemeyi başlat
    this._isDragging    = true;
    this._dragPlaneId   = planeId;
    this._dragStartPos.set(e.clientX, e.clientY);
    this._dragStartConst  = info.plane.constant;
    this._dragStartNormal = info.plane.normal.clone();
    this._isShiftDrag   = e.shiftKey;

    // OrbitControls'ü devre dışı bırak (çakışmayı önle)
    this._controls.enabled = false;

    e.stopPropagation();
  }

  /**
   * Mousemove: sürükleme devam ediyorsa düzlemi taşı veya döndür.
   */
  private _handleMouseMove(e: MouseEvent): void {
    if (!this._isDragging || !this._dragPlaneId) return;

    const info = this._planes.get(this._dragPlaneId);
    if (!info) return;

    const dx = e.clientX - this._dragStartPos.x;
    const dy = e.clientY - this._dragStartPos.y;

    if (this._isShiftDrag) {
      // ── Döndürme modu ──────────────────────────────────────────────────
      // Fareyi X hareket ettirince yatay döndür, Y hareket ettirince dikey
      const rotX = -dy * ROTATE_SENSITIVITY;
      const rotY =  dx * ROTATE_SENSITIVITY;

      const newNormal = this._dragStartNormal.clone();

      // Kamera sağ vektörü etrafında döndür (X hareketi)
      const camRight = new THREE.Vector3();
      camRight.crossVectors(this._camera.getWorldDirection(new THREE.Vector3()), this._camera.up).normalize();
      const qX = new THREE.Quaternion().setFromAxisAngle(camRight, rotX);
      newNormal.applyQuaternion(qX);

      // Kamera up vektörü etrafında döndür (Y hareketi)
      const qY = new THREE.Quaternion().setFromAxisAngle(this._camera.up, rotY);
      newNormal.applyQuaternion(qY);

      newNormal.normalize();
      info.plane.normal.copy(newNormal);

    } else {
      // ── Kaydırma modu ─────────────────────────────────────────────────
      // Fare hareketi → düzlemi eksen boyunca taşı
      // Kameraya göre projelendirme ile "doğal" hissettir:
      // Fare yukarı gidince model daha fazla kesilir (düzlem ileriye gider)
      const delta = (-dy + dx) * DRAG_SENSITIVITY;
      const newConst = this._dragStartConst + delta;

      info.plane.constant = newConst;
      info.position = -newConst; // constant = -(normal · point) kuralı

      // Helper mesh'i taşı
      if (info.helperMesh) {
        this._positionHelperMesh(info.helperMesh, info.axis, info.position);
      }
    }

    this._notifyChange();
  }

  /**
   * Mouseup: sürüklemeyi sonlandır, OrbitControls'ü etkinleştir.
   */
  private _handleMouseUp(_e: MouseEvent): void {
    if (!this._isDragging) return;

    this._isDragging  = false;
    this._dragPlaneId = null;
    this._controls.enabled = true;
  }

  // ─── Özel: Callback ───────────────────────────────────────────────────────

  private _notifyChange(): void {
    this.onPlanesChanged?.(this.planes);
  }
}
