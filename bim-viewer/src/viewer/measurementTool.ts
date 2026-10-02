/**
 * measurementTool.ts — AutoDimensionTool
 *
 * AutoCAD Dimensions tarzı otomatik boyut ölçüm aracı.
 * Bir elemente tıklanınca bounding box'tan X/Y/Z boyut çizgileri otomatik oluşturulur.
 *
 * ─── MİMARİ GENEL BAKIŞ ──────────────────────────────────────────────────────
 *
 *  AutoDimensionTool
 *  ├── activate() / deactivate()       → Ölçüm modunu aç/kapat
 *  ├── Tıklama                         → Element tespiti → bounding box → 3 eksen boyutu
 *  ├── Hover (mouse move)              → Element highlight (Fragments API)
 *  ├── Shift+tıklama (iki element)     → Elementler arası mesafe çizgisi
 *  ├── clearDimension(id)              → Tek boyutu sil
 *  ├── clearAllDimensions()            → Tümünü sil
 *  └── dispose()                       → Kaynakları serbest bırak
 *
 * ─── RAYCASTING STRATEJİSİ ───────────────────────────────────────────────────
 *
 *  1. PRIMARY: @thatopen/fragments model.raycast() → model.getMergedBox([localId])
 *  2. FALLBACK: THREE.Raycaster → scene mesh traversal → geometry.boundingBox
 *
 * ─── BOYUT ÇİZGİSİ YAPISI ────────────────────────────────────────────────────
 *
 *  Her eksen için ONE THREE.LineSegments (5 segment = 10 nokta):
 *    - Extension line 1 (element köşesi → offset noktası)
 *    - Extension line 2 (diğer köşe → offset noktası)
 *    - Dimension line (iki offset noktası arası)
 *    - Tick 1 (dimension line başında dik işaret)
 *    - Tick 2 (dimension line sonunda dik işaret)
 *  + ONE CSS2DObject etiket (mesafe metni)
 */

import * as THREE from 'three';
import {
  CSS2DRenderer,
  CSS2DObject,
} from 'three/addons/renderers/CSS2DRenderer.js';
import type { FragmentsModel } from '@thatopen/fragments';
import type { ElementPicker } from './elementPicker';

// ─── Sabitler ──────────────────────────────────────────────────────────────────

const LINE_COLOR       = 0xe15a1f;  // Turuncu
const OFFSET           = 0.3;       // Boyut çizgilerinin elementten uzaklığı (m)
const TICK_SIZE        = 0.12;      // Uç çizgisi uzunluğu (m)
const MIN_SIZE         = 0.01;      // Bu boyuttan küçük eksenleri gösterme (m)
const MAX_DIMS         = 20;        // Aynı anda max aktif boyut sayısı
const HOVER_MS         = 16;        // Hover throttle (~60 fps)

// Fragments highlight için MaterialDefinition tipi
type MaterialDefinition = {
  color: THREE.Color;
  opacity: number;
  transparent: boolean;
  renderedFaces: number;
};

const HOVER_MAT: MaterialDefinition = {
  color:        new THREE.Color(0xe15a1f),
  opacity:      0.35,
  transparent:  true,
  renderedFaces: 2, // RenderedFaces.TwoSides
};

// ─── Tipler ────────────────────────────────────────────────────────────────────

/**
 * Tek bir boyut ölçümü.
 * Bir element tıklanınca oluşturulur; X/Y/Z eksenlerinde çizgiler + etiketler içerir.
 */
export interface AutoDimension {
  /** Benzersiz ID */
  id: string;
  /** Element adı (IFC Name veya fallback "Element-N") */
  elementName: string;
  /** Elementin 3D bounding box'ı */
  box: THREE.Box3;
  /** X boyutu (m) */
  sizeX: number;
  /** Y boyutu (m) */
  sizeY: number;
  /** Z boyutu (m) */
  sizeZ: number;
  /** Tüm 3D ve CSS2D elemanları içeren grup */
  group: THREE.Group;
  /** CSS2DObject etiketleri (dispose için) */
  labels: CSS2DObject[];
}

/** Boyut oluşturulduğunda tetiklenen callback */
export type DimensionAddedCallback = (dim: AutoDimension) => void;

// ─── Ana Sınıf ─────────────────────────────────────────────────────────────────

/**
 * AutoCAD tarzı otomatik boyutlandırma aracı.
 *
 * KULLANIM:
 * ```ts
 * const tool = new AutoDimensionTool(scene, camera, renderer, viewport, loadedModels);
 * tool.activate();
 * tool.onDimensionAdded = (d) => console.log(d.elementName, d.sizeX, d.sizeY, d.sizeZ);
 * ```
 */
export class AutoDimensionTool {

  // ── Durum ────────────────────────────────────────────────────────────────

  /** Araç aktif mi? */
  isActive = false;

  /** Aktif boyut ölçümleri listesi */
  dimensions: AutoDimension[] = [];

  // ── Callback'ler ─────────────────────────────────────────────────────────

  onDimensionAdded:   DimensionAddedCallback | null = null;
  onDimensionRemoved: (() => void) | null = null;

  // ── Bağımlılıklar ────────────────────────────────────────────────────────

  private readonly _scene:    THREE.Scene;
  private readonly _camera:   THREE.PerspectiveCamera;
  private readonly _renderer: THREE.WebGLRenderer;
  private readonly _viewport: HTMLElement;

  /** @thatopen/fragments model referansları — raycasting + getMergedBox için */
  private readonly _loadedModels: Map<string, FragmentsModel>;

  /** ElementPicker referansı — çalışan raycasting altyapısını yeniden kullanmak için */
  private readonly _elementPicker: ElementPicker | null;

  /** THREE.Raycaster fallback için hedef mesh'ler */
  private _targetObjects: THREE.Object3D[] = [];

  // ── CSS2DRenderer ────────────────────────────────────────────────────────

  private readonly _labelRenderer: CSS2DRenderer;

  // ── Raycasting ───────────────────────────────────────────────────────────

  private readonly _raycaster = new THREE.Raycaster();
  private readonly _mouse     = new THREE.Vector2();

  // ── Hover ────────────────────────────────────────────────────────────────

  private _hoveredElement: { modelId: string; localId: number } | null = null;
  private _hoverLastTime  = 0;

  // ── Shift seçimi (iki element arası mesafe) ──────────────────────────────

  private _shiftBox: { box: THREE.Box3; name: string } | null = null;

  // ── Sayaç ────────────────────────────────────────────────────────────────

  private _counter = 0;

  // ── Bound event handler'ları ─────────────────────────────────────────────

  private readonly _onClickBound:   (e: MouseEvent) => void;
  private readonly _onMoveBound:    (e: MouseEvent) => void;
  private readonly _onKeyDownBound: (e: KeyboardEvent) => void;

  // ─── Constructor ──────────────────────────────────────────────────────────

  constructor(
    scene:          THREE.Scene,
    camera:         THREE.PerspectiveCamera,
    renderer:       THREE.WebGLRenderer,
    viewport:       HTMLElement,
    loadedModels:   Map<string, FragmentsModel>,
    elementPicker?: ElementPicker,
  ) {
    this._scene          = scene;
    this._camera         = camera;
    this._renderer       = renderer;
    this._viewport       = viewport;
    this._loadedModels   = loadedModels;
    this._elementPicker  = elementPicker ?? null;

    this._labelRenderer = this._createLabelRenderer();

    this._onClickBound   = (e) => void this._handleClick(e);
    this._onMoveBound    = (e) => void this._handleMouseMove(e);
    this._onKeyDownBound = this._handleKeyDown.bind(this);

    console.log('[AutoDimensionTool] Başlatıldı.');
  }

  // ─── Public API ───────────────────────────────────────────────────────────

  /** Ölçüm modunu etkinleştirir. */
  activate(): void {
    if (this.isActive) return;
    this.isActive = true;
    this._renderer.domElement.style.cursor = 'crosshair';
    this._renderer.domElement.addEventListener('click',     this._onClickBound);
    this._renderer.domElement.addEventListener('mousemove', this._onMoveBound);
    document.addEventListener('keydown', this._onKeyDownBound);
    console.log('[AutoDimensionTool] Aktif — elemente tıklayın.');
  }

  /** Ölçüm modunu devre dışı bırakır. */
  deactivate(): void {
    if (!this.isActive) return;
    this.isActive = false;
    this._renderer.domElement.style.cursor = '';
    this._renderer.domElement.removeEventListener('click',     this._onClickBound);
    this._renderer.domElement.removeEventListener('mousemove', this._onMoveBound);
    document.removeEventListener('keydown', this._onKeyDownBound);
    void this._clearHover();
    this._shiftBox = null;
    console.log('[AutoDimensionTool] Deaktif.');
  }

  /**
   * Fallback raycasting hedef nesnelerini günceller.
   * Model yüklendiğinde BIMViewer tarafından çağrılır.
   */
  setTargetObjects(objects: THREE.Object3D[]): void {
    this._targetObjects = objects;
  }

  /** ID'ye göre tek bir boyutu siler. */
  clearDimension(id: string): void {
    const idx = this.dimensions.findIndex(d => d.id === id);
    if (idx === -1) return;
    this._removeDimensionFromScene(this.dimensions[idx]!);
    this.dimensions.splice(idx, 1);
    this.onDimensionRemoved?.();
    console.log(`[AutoDimensionTool] Boyut silindi: ${id}`);
  }

  /** Tüm boyutları siler. */
  clearAllDimensions(): void {
    for (const dim of this.dimensions) this._removeDimensionFromScene(dim);
    this.dimensions = [];
    this.onDimensionRemoved?.();
    console.log('[AutoDimensionTool] Tüm boyutlar silindi.');
  }

  /**
   * Animation loop'ta çağrılmalı — CSS2DRenderer'ı günceller.
   */
  updateRenderer(): void {
    for (const dim of this.dimensions) {
      for (const label of dim.labels) {
        const dist = this._camera.position.distanceTo(label.position);
        let fontSize = 14 - (dist / 10);
        if (fontSize < 8) fontSize = 8;
        if (fontSize > 14) fontSize = 14;
        label.element.style.fontSize = `${fontSize}px`;
      }
    }
    this._labelRenderer.render(this._scene, this._camera);
  }

  /** Tüm kaynakları serbest bırakır. */
  dispose(): void {
    this.deactivate();
    this.clearAllDimensions();
    this._labelRenderer.domElement.remove();
    console.log('[AutoDimensionTool] Dispose edildi.');
  }

  // ─── Event Handler'ları ───────────────────────────────────────────────────

  private async _handleClick(e: MouseEvent): Promise<void> {
    if (!this.isActive || e.button !== 0) return;

    this._updateMouseCoords(e);

    console.log('[AutoDim] click — NDC:', this._mouse.x.toFixed(3), this._mouse.y.toFixed(3),
      '| models:', this._loadedModels.size, '| targets:', this._targetObjects.length);

    try {
      const result = await this._getElementAndBox();

      if (!result) {
        console.warn('[AutoDim] Tıklanan noktada element bulunamadı.');
        return;
      }

      const sz = result.box.getSize(new THREE.Vector3());
      console.log('[AutoDim] Sonuç:', result.name, `→ ${sz.x.toFixed(2)}m × ${sz.y.toFixed(2)}m × ${sz.z.toFixed(2)}m`);

      const { box, name } = result;

      // Shift+tık: iki element arası mesafe
      if (e.shiftKey) {
        if (this._shiftBox) {
          this._showInterDistance(this._shiftBox.box, this._shiftBox.name, box, name);
          this._shiftBox = null;
        } else {
          this._shiftBox = { box, name };
          console.log('[AutoDim] Shift: ilk element seçildi →', name);
        }
        return;
      }

      // Normal tık: boyut ekle
      this._addDimension(box, name);

    } catch (err) {
      console.error('[AutoDim] handleClick hatası:', err);
    }
  }

  private async _handleMouseMove(e: MouseEvent): Promise<void> {
    if (!this.isActive) return;
    const now = performance.now();
    if (now - this._hoverLastTime < HOVER_MS) return;
    this._hoverLastTime = now;

    this._updateMouseCoords(e);

    // Fragments hover: sadece models varsa ve önceki hover temizlenmemişse dene
    // model.raycast genellikle null döndürdüğü için mesh hover da çalıştır
    if (this._loadedModels.size > 0) {
      void this._doFragmentsHover();
    }
    this._doMeshHover();
  }

  private _handleKeyDown(e: KeyboardEvent): void {
    if (!this.isActive) return;
    if (e.key === 'Escape') {
      void this._clearHover();
      this._shiftBox = null;
      // BIMViewer kendi ESC handler'ında deactivate + clearAll çağırır
    }
  }

  // ─── Koordinat Güncelleme ─────────────────────────────────────────────────

  private _updateMouseCoords(e: MouseEvent): void {
    const rect = this._renderer.domElement.getBoundingClientRect();
    this._mouse.set(
      ((e.clientX - rect.left) / rect.width)  *  2 - 1,
      ((e.clientY - rect.top)  / rect.height) * -2 + 1,
    );
  }

  // ─── Raycasting & Element Tespiti ────────────────────────────────────────

  /**
   * Mouse pozisyonundaki elementi ve bounding box'ını döndürür.
   *
   * Strateji (sırayla):
   * 1. Fragments model.raycast() → getMergedBox([localId])  (IFC element bazında, doğru)
   * 2. THREE.Raycaster → isabet eden mesh → Box3.setFromObject  (genel fallback)
   * 3. THREE.Raycaster hit point → sabit boyutlu sentetik kutu  (son çare)
   */
  private async _getElementAndBox(): Promise<{
    box:      THREE.Box3;
    name:     string;
    modelId?: string;
    localId?: number;
  } | null> {

    // ── 1. Fragments raycasting ────────────────────────────────────────────
    if (this._loadedModels.size > 0) {
      const hit = await this._fragmentsRaycast(true);
      console.log('[AutoDim] Fragments hit:', hit ? { localId: hit.localId } : null);

      if (hit) {
        try {
          const box = await hit.model.getMergedBox([hit.localId]);
          const sz  = box.getSize(new THREE.Vector3());
          console.log('[AutoDim] getMergedBox:', { min: box.min, max: box.max, isEmpty: box.isEmpty(), sz });

          if (!box.isEmpty() && isFinite(box.min.x) && sz.length() > 0) {
            const name = await this._fetchElementName(hit.model, hit.localId);
            return { box, name, modelId: hit.model.modelId, localId: hit.localId };
          }
        } catch (err) {
          console.warn('[AutoDim] getMergedBox hatası:', err);
        }
      }
    }

    // ── 2. THREE.Raycaster fallback ────────────────────────────────────────
    return this._meshRaycastAndBox();
  }

  /**
   * @thatopen/fragments built-in raycasting — en yakın model hit'ini döndürür.
   *
   * ElementPicker mevcutsa onun performRaycast() metodunu kullanır; bu yol
   * zaten çalıştığı kanıtlanmıştır. ElementPicker yoksa kendi implementasyonunu
   * çalıştırır (fallback).
   */
  private async _fragmentsRaycast(log = false): Promise<{
    model:   FragmentsModel;
    localId: number;
  } | null> {
    // ElementPicker'ın çalışan raycasting altyapısını kullan
    if (this._elementPicker) {
      const result = await this._elementPicker.performRaycast(this._mouse);
      if (log) console.log('[AutoDim] ElementPicker raycast:', result ? { localId: result.localId } : null);
      return result;
    }

    // Fallback: kendi model.raycast() çağrısı
    const canvas = this._renderer.domElement;
    let closestDist = Infinity;
    let closest: { model: FragmentsModel; localId: number } | null = null;

    for (const [modelId, model] of this._loadedModels) {
      try {
        const result = await model.raycast({
          camera: this._camera,
          mouse:  this._mouse,
          dom:    canvas,
        });
        if (log) console.log('[AutoDim] model.raycast:', modelId, result ? { localId: result.localId, dist: result.distance } : null);
        if (result && result.distance < closestDist) {
          closestDist = result.distance;
          closest = { model, localId: result.localId };
        }
      } catch (err) {
        if (log) console.warn('[AutoDim] model.raycast hatası:', err);
      }
    }
    return closest;
  }

  /**
   * THREE.Raycaster ile mesh/InstancedMesh tespiti ve bounding box hesabı.
   *
   * @thatopen/fragments InstancedMesh'lerinin instanceMatrix buffer'ı
   * bazen null/uninitialized olduğundan `intersectObjects(arr, true)` crash verir.
   * Her objeyi ayrı ayrı try-catch içinde `intersectObject` ile test ederiz.
   *
   * InstancedMesh hit: instanceId + getMatrixAt → element bazında doğru bbox.
   * Normal mesh hit:   Box3.setFromObject → mesh bbox.
   * Geçersiz / çok büyük bbox: hit point etrafında sentetik 2×3×0.25 m kutu.
   */
  private _meshRaycastAndBox(): { box: THREE.Box3; name: string } | null {
    this._raycaster.setFromCamera(this._mouse, this._camera);

    const castTargets: THREE.Object3D[] =
      this._targetObjects.length > 0
        ? this._targetObjects
        : this._scene.children.filter(c => !c.userData['isHelper']);

    console.log('[AutoDim] mesh fallback targets:', castTargets.length);

    // ── Her objeyi ayrı ayrı raycast et (crash-safe) ──────────────────────
    const hits: THREE.Intersection[] = [];
    for (const target of castTargets) {
      try {
        this._raycaster.intersectObject(target, true, hits);
      } catch { /* instanceMatrix null olan Fragments tile'ları atla */ }
    }
    hits.sort((a, b) => a.distance - b.distance);

    console.log('[AutoDim] mesh hits:', hits.length);
    if (hits.length === 0) return null;

    let finalBox: THREE.Box3 | null = null;
    let finalName = '';
    let finalHitPoint = hits[0]!.point;

    for (const hit of hits) {
      const hitObject = hit.object;
      finalHitPoint = hit.point;

      if (hitObject instanceof THREE.InstancedMesh && hit.instanceId !== undefined) {
        try {
          const instMat = new THREE.Matrix4();
          hitObject.getMatrixAt(hit.instanceId, instMat);
          const worldMat = hitObject.matrixWorld.clone().multiply(instMat);

          hitObject.geometry.computeBoundingBox();
          const localBox = hitObject.geometry.boundingBox;

          if (localBox && !localBox.isEmpty()) {
            const box = localBox.clone().applyMatrix4(worldMat);
            const sz  = box.getSize(new THREE.Vector3());
            if (sz.length() > 0 && Math.max(sz.x, sz.y, sz.z) < 200) {
              finalBox = box;
              finalName = hitObject.name || `Element-${this._counter + 1}`;
            }
          }
        } catch (err) {
          console.warn('[AutoDim] InstancedMesh bbox hatası:', err);
        }
      } else {
        const box = new THREE.Box3().setFromObject(hitObject);
        const size = box.getSize(new THREE.Vector3());
        
        if (!box.isEmpty() && isFinite(box.min.x)) {
          // Çok büyük kapsayıcı nesneleri filtrele (örn. 15m'den büyük)
          if (size.x > 15 && size.y > 15 && size.z > 5) {
            console.log('[AutoDim] Container obje atlandı:', hitObject.name, size);
            continue;
          }
          finalBox = box;
          finalName = hitObject.name || hitObject.parent?.name || `Element-${this._counter + 1}`;
        }
      }

      if (finalBox) {
        break; // İlk uygun valid box'ı bulduk
      }
    }

    if (!finalBox) {
      console.log('[AutoDim] Sentetik kutu — hitPoint:', finalHitPoint.x.toFixed(2), finalHitPoint.y.toFixed(2), finalHitPoint.z.toFixed(2));
      const half = new THREE.Vector3(1.0, 1.5, 0.125);
      finalBox = new THREE.Box3(finalHitPoint.clone().sub(half), finalHitPoint.clone().add(half));
      finalName = `Element-${this._counter + 1}`;
    }

    return { box: finalBox, name: finalName };
  }

  /**
   * Fragments getItemsData'dan element adını getirir.
   * Hata durumunda fallback isim döner.
   */
  private async _fetchElementName(model: FragmentsModel, localId: number): Promise<string> {
    try {
      const [data] = await model.getItemsData([localId], { attributesDefault: true });
      const n = (data?.['Name'] as { value?: unknown } | undefined)?.value;
      if (n && String(n).trim()) return String(n).trim();
    } catch { /* skip */ }
    return `Element-${this._counter + 1}`;
  }

  // ─── Hover ───────────────────────────────────────────────────────────────

  /**
   * Fragments highlight API ile hover efekti.
   * Önceki hover'ı temizleyip yeni elementi highlight eder.
   */
  private async _doFragmentsHover(): Promise<void> {
    const hit = await this._fragmentsRaycast();

    if (!hit) {
      if (this._hoveredElement) await this._clearHover();
      return;
    }

    // Aynı element hover'daysa gereksiz işlem yapma
    if (
      this._hoveredElement?.modelId === hit.model.modelId &&
      this._hoveredElement?.localId === hit.localId
    ) return;

    await this._clearHover();

    try {
      await hit.model.highlight([hit.localId], HOVER_MAT as any);
      this._hoveredElement = { modelId: hit.model.modelId, localId: hit.localId };
    } catch { /* skip */ }
  }

  /**
   * Fallback hover: mesh varsa cursor'ı pointer yap.
   */
  private _doMeshHover(): void {
    const targets: THREE.Object3D[] = this._targetObjects.length > 0
      ? this._targetObjects
      : this._scene.children.filter(c => !c.userData['isHelper']);

    this._raycaster.setFromCamera(this._mouse, this._camera);
    const hits: THREE.Intersection[] = [];
    for (const t of targets) {
      try { this._raycaster.intersectObject(t, true, hits); } catch { /* skip */ }
    }
    this._renderer.domElement.style.cursor = hits.length > 0 ? 'pointer' : 'crosshair';
  }

  /** Mevcut hover highlight'ı temizler. */
  private async _clearHover(): Promise<void> {
    if (!this._hoveredElement) return;
    const { modelId, localId } = this._hoveredElement;
    const model = this._loadedModels.get(modelId);
    if (model) {
      try { await model.resetHighlight([localId]); } catch { /* skip */ }
    }
    this._hoveredElement = null;
  }

  // ─── Boyut Oluşturma ─────────────────────────────────────────────────────

  /**
   * Verilen bounding box için X/Y/Z boyut çizgilerini sahneye ekler.
   */
  private _addDimension(box: THREE.Box3, name: string): void {
    const size = new THREE.Vector3();
    box.getSize(size);

    const sizeX = size.x;
    const sizeY = size.y;
    const sizeZ = size.z;

    const id    = `dim-${Date.now()}-${this._counter++}`;
    const group = new THREE.Group();
    group.userData['dimensionId'] = id;
    group.renderOrder = 999;

    const labels: CSS2DObject[] = [];

    // X boyutu — elementin üstüne yatay çizgi
    if (sizeX >= MIN_SIZE) {
      const [ls, lbl] = this._buildXDim(box, sizeX);
      group.add(ls, lbl);
      labels.push(lbl);
    }

    // Y boyutu — elementin sağına dikey çizgi
    if (sizeY >= MIN_SIZE) {
      const [ls, lbl] = this._buildYDim(box, sizeY);
      group.add(ls, lbl);
      labels.push(lbl);
    }

    // Z boyutu — elementin önüne yatay çizgi
    if (sizeZ >= MIN_SIZE) {
      const [ls, lbl] = this._buildZDim(box, sizeZ);
      group.add(ls, lbl);
      labels.push(lbl);
    }

    this._scene.add(group);

    const dim: AutoDimension = { id, elementName: name, box, sizeX, sizeY, sizeZ, group, labels };

    // Max limit aşılırsa en eskiyi kaldır
    if (this.dimensions.length >= MAX_DIMS) {
      this._removeDimensionFromScene(this.dimensions[0]!);
      this.dimensions.shift();
    }

    this.dimensions.push(dim);
    this.onDimensionAdded?.(dim);

    console.log(`[AutoDimensionTool] Boyut eklendi: ${id} — ${name} (${sizeX.toFixed(2)} × ${sizeY.toFixed(2)} × ${sizeZ.toFixed(2)} m)`);
  }

  // ─── Boyut Çizgisi Builder'ları ───────────────────────────────────────────

  /**
   * X boyutu (genişlik) — elementin üstünde yatay.
   *
   * Yerleşim:
   *   y_offset = max.y + OFFSET
   *   Extension lines: köşelerden yukarı
   *   Dimension line: min.x → max.x (y_offset yüksekliğinde)
   */
  private _buildXDim(box: THREE.Box3, size: number): [THREE.LineSegments, CSS2DObject] {
    const { min, max } = box;
    const midZ = (min.z + max.z) / 2;
    const y    = max.y + OFFSET;

    const pts = [
      // Extension line 1
      min.x, max.y, midZ,           min.x, y, midZ,
      // Extension line 2
      max.x, max.y, midZ,           max.x, y, midZ,
      // Dimension line
      min.x, y, midZ,               max.x, y, midZ,
      // Tick 1 (left end)
      min.x, y - TICK_SIZE / 2, midZ,   min.x, y + TICK_SIZE / 2, midZ,
      // Tick 2 (right end)
      max.x, y - TICK_SIZE / 2, midZ,   max.x, y + TICK_SIZE / 2, midZ,
    ];

    const ls  = this._makeLineSegments(pts);
    const lbl = this._makeLabel(
      `${size.toFixed(2)} m`,
      new THREE.Vector3((min.x + max.x) / 2, y, midZ),
    );
    return [ls, lbl];
  }

  /**
   * Y boyutu (yükseklik) — elementin sağında dikey.
   *
   * Yerleşim:
   *   x_offset = max.x + OFFSET
   *   Extension lines: üst ve alt köşelerden sağa
   *   Dimension line: min.y → max.y (x_offset mesafesinde)
   */
  private _buildYDim(box: THREE.Box3, size: number): [THREE.LineSegments, CSS2DObject] {
    const { min, max } = box;
    const midZ = (min.z + max.z) / 2;
    const x    = max.x + OFFSET;

    const pts = [
      // Extension line 1 (bottom)
      max.x, min.y, midZ,           x, min.y, midZ,
      // Extension line 2 (top)
      max.x, max.y, midZ,           x, max.y, midZ,
      // Dimension line
      x, min.y, midZ,               x, max.y, midZ,
      // Tick 1 (bottom end)
      x - TICK_SIZE / 2, min.y, midZ,   x + TICK_SIZE / 2, min.y, midZ,
      // Tick 2 (top end)
      x - TICK_SIZE / 2, max.y, midZ,   x + TICK_SIZE / 2, max.y, midZ,
    ];

    const ls  = this._makeLineSegments(pts);
    const lbl = this._makeLabel(
      `${size.toFixed(2)} m`,
      new THREE.Vector3(x, (min.y + max.y) / 2, midZ),
    );
    return [ls, lbl];
  }

  /**
   * Z boyutu (derinlik) — elementin önünde yatay.
   *
   * Yerleşim:
   *   z_offset = min.z - OFFSET
   *   Extension lines: ön köşelerden öne
   *   Dimension line: min.x → max.x (z_offset derinliğinde)
   */
  private _buildZDim(box: THREE.Box3, size: number): [THREE.LineSegments, CSS2DObject] {
    const { min, max } = box;
    const midY = (min.y + max.y) / 2;
    const z    = min.z - OFFSET;

    const pts = [
      // Extension line 1 (left)
      min.x, midY, min.z,           min.x, midY, z,
      // Extension line 2 (right)
      max.x, midY, min.z,           max.x, midY, z,
      // Dimension line
      min.x, midY, z,               max.x, midY, z,
      // Tick 1 (left end)
      min.x, midY - TICK_SIZE / 2, z,   min.x, midY + TICK_SIZE / 2, z,
      // Tick 2 (right end)
      max.x, midY - TICK_SIZE / 2, z,   max.x, midY + TICK_SIZE / 2, z,
    ];

    const ls  = this._makeLineSegments(pts);
    const lbl = this._makeLabel(
      `${size.toFixed(2)} m`,
      new THREE.Vector3((min.x + max.x) / 2, midY, z),
    );
    return [ls, lbl];
  }

  // ─── İki Element Arası Mesafe ─────────────────────────────────────────────

  /**
   * İki elementin bounding box'ları arasındaki en kısa mesafeyi gösteren çizgi.
   * Bağlantı noktaları: her kutunun merkezini diğer kutunun sınırına kısıtla.
   */
  private _showInterDistance(
    boxA: THREE.Box3,
    nameA: string,
    boxB: THREE.Box3,
    nameB: string,
  ): void {
    const centerA  = boxA.getCenter(new THREE.Vector3());
    const centerB  = boxB.getCenter(new THREE.Vector3());
    const closestA = centerB.clone().clamp(boxA.min, boxA.max);
    const closestB = centerA.clone().clamp(boxB.min, boxB.max);
    const dist     = closestA.distanceTo(closestB);

    const id    = `dim-dist-${Date.now()}-${this._counter++}`;
    const group = new THREE.Group();
    group.userData['dimensionId'] = id;
    group.renderOrder = 999;

    const ls = this._makeLineSegments([
      closestA.x, closestA.y, closestA.z,
      closestB.x, closestB.y, closestB.z,
    ]);
    group.add(ls);

    const mid = new THREE.Vector3().addVectors(closestA, closestB).multiplyScalar(0.5);
    const lbl = this._makeLabel(`${nameA} ↔ ${nameB}: ${dist.toFixed(2)} m`, mid);
    group.add(lbl);

    this._scene.add(group);

    const dim: AutoDimension = {
      id,
      elementName: `${nameA} ↔ ${nameB}`,
      box:         new THREE.Box3(),
      sizeX:       dist,
      sizeY:       0,
      sizeZ:       0,
      group,
      labels:      [lbl],
    };

    if (this.dimensions.length >= MAX_DIMS) {
      this._removeDimensionFromScene(this.dimensions[0]!);
      this.dimensions.shift();
    }
    this.dimensions.push(dim);
    this.onDimensionAdded?.(dim);

    console.log(`[AutoDimensionTool] İki element arası mesafe: ${dist.toFixed(3)} m`);
  }

  // ─── Yardımcı: 3D Elemanlar ───────────────────────────────────────────────

  /**
   * Verilen düz koordinat listesinden (ikişerli segment çiftleri) LineSegments oluşturur.
   *
   * @param pts - Düz sayı dizisi: [x1,y1,z1, x2,y2,z2, ...] (çift sayı nokta)
   */
  private _makeLineSegments(pts: number[]): THREE.LineSegments {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
    const mat = new THREE.LineBasicMaterial({ color: LINE_COLOR, linewidth: 1 });
    const ls  = new THREE.LineSegments(geo, mat);
    ls.renderOrder = 999;
    return ls;
  }

  /**
   * AutoCAD tarzı boyut etiketi (CSS2DObject).
   *
   * Stil: koyu arka plan (#1B1612), beyaz yazı, turuncu kenarlık.
   * pointer-events: none → tıklamaları engelleme.
   */
  private _makeLabel(text: string, position: THREE.Vector3): CSS2DObject {
    const div = document.createElement('div');
    div.className   = 'bv-autodim-label';
    div.textContent = text;

    Object.assign(div.style, {
      background:    'rgba(27, 22, 18, 0.85)',
      color:         '#ffffff',
      fontSize:      '12px',
      fontFamily:    "'Inter', 'Segoe UI', sans-serif",
      fontWeight:    '600',
      padding:       '4px 10px',
      margin:        '5px',
      borderRadius:  '4px',
      border:        '1px solid #E15A1F',
      pointerEvents: 'auto',
      userSelect:    'none',
      whiteSpace:    'nowrap',
      letterSpacing: '0.3px',
      boxShadow:     '0 1px 4px rgba(0,0,0,0.6)',
      transition:    'all 0.2s ease',
    });

    div.addEventListener('mouseenter', () => {
      div.style.zIndex = '999';
      div.style.transform = 'scale(1.1)';
      div.style.background = 'rgba(27, 22, 18, 1)';
    });
    div.addEventListener('mouseleave', () => {
      div.style.zIndex = '';
      div.style.transform = 'scale(1)';
      div.style.background = 'rgba(27, 22, 18, 0.85)';
    });

    const label = new CSS2DObject(div);
    label.position.copy(position);
    return label;
  }

  // ─── Temizlik ─────────────────────────────────────────────────────────────

  /** Tek bir boyutun tüm 3D ve CSS2D elemanlarını sahneden kaldırır. */
  private _removeDimensionFromScene(dim: AutoDimension): void {
    this._scene.remove(dim.group);
    dim.group.traverse((child) => {
      if (child instanceof THREE.LineSegments) {
        child.geometry.dispose();
        (child.material as THREE.Material).dispose();
      }
    });
  }

  // ─── CSS2DRenderer Kurulumu ───────────────────────────────────────────────

  private _createLabelRenderer(): CSS2DRenderer {
    const lr = new CSS2DRenderer();

    const { width, height } = this._renderer.domElement.getBoundingClientRect();
    lr.setSize(
      width  || this._viewport.clientWidth,
      height || this._viewport.clientHeight,
    );

    const dom = lr.domElement;
    dom.style.position      = 'absolute';
    dom.style.top           = '0';
    dom.style.left          = '0';
    dom.style.width         = '100%';
    dom.style.height        = '100%';
    dom.style.pointerEvents = 'none';
    dom.style.overflow      = 'hidden';
    dom.style.zIndex        = '10';

    this._viewport.style.position = 'relative';
    this._viewport.appendChild(dom);

    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width: w, height: h } = entry.contentRect;
        if (w > 0 && h > 0) lr.setSize(w, h);
      }
    });
    ro.observe(this._viewport);

    console.log('[AutoDimensionTool] CSS2DRenderer kuruldu.');
    return lr;
  }
}
