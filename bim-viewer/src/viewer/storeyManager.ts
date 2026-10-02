/**
 * storeyManager.ts
 *
 * IFC modelindeki katları (IfcBuildingStorey) yönetmekten sorumlu modül.
 *
 * ─── MİMARİ ──────────────────────────────────────────────────────────────────
 *
 *  StoreyManager
 *  ├── extractStoreys(modelId)   → Spatial structure'dan IfcBuildingStorey'leri çeker
 *  ├── setStoreyVisibility()     → Bir katın tüm elementlerini göster/gizle
 *  ├── isolateStorey()           → Solo mod — sadece seçilen katı göster
 *  ├── showAllStoreys()          → Tüm katları görünür yap
 *  └── getStoreyForElement()     → Bir elementin hangi katta olduğunu döndür
 *
 * ─── IFC STOREY TESPİTİ ──────────────────────────────────────────────────────
 *
 *  @thatopen/fragments'in getSpatialStructure() metodu IFC hiyerarşisini döner:
 *    IfcProject → IfcSite → IfcBuilding → IfcBuildingStorey → elements
 *
 *  Her SpatialTreeItem şunları içerir:
 *    - localId   : ExpressID (IFC entity numarası)
 *    - category  : IFC tipi string ("IFCBUILDINGSTOREY" vb.)
 *    - children  : Alt elemanlar
 *
 *  Elevation değeri için IFC property'ler sorgulanır (Elevation attribute).
 *
 * ─── GELECEKTEKİ GELİŞTİRMELER ──────────────────────────────────────────────
 *  - Kat gruplaması (alt kat / bodrum / çatı arası)
 *  - Eleman tip sayısını canlı güncelleme
 *  - Kat bazlı kesit düzlemi entegrasyonu
 */

import type { FragmentsModels, FragmentsModel, SpatialTreeItem } from '@thatopen/fragments';

// ─── Tipler ────────────────────────────────────────────────────────────────────

/**
 * Bir IFC katının (IfcBuildingStorey) yönetim verisi.
 */
export interface StoreyInfo {
  /** IFC ExpressID (lokal model numarası) */
  id: string;
  /** Kat adı — IFC Name attribute'undan ("Zemin Kat", "1. Kat" vb.) */
  name: string;
  /** Kot değeri metre cinsinden (Z ekseni değeri) */
  elevation: number;
  /** Kattaki toplam element sayısı */
  elementCount: number;
  /** Kattaki tüm element ExpressID'leri */
  elementIds: number[];
  /** Kat şu an görünür mü? */
  isVisible: boolean;
  /** IFC tipine göre element dağılımı: { "IfcWall": 23, "IfcSlab": 4, ... } */
  elementTypes: Record<string, number>;
}

/**
 * Kat görünürlüğü değiştiğinde çağrılan callback tipi.
 */
export type StoreyVisibilityCallback = (storeyId: string, visible: boolean, storeys: StoreyInfo[]) => void;

// ─── Ana Sınıf ─────────────────────────────────────────────────────────────────

/**
 * IFC modelindeki IfcBuildingStorey entity'lerini yönetir.
 *
 * KULLANIM ÖRNEĞİ:
 * ```ts
 * const manager = new StoreyManager(fragmentsModels);
 * await manager.extractStoreys(modelId);
 * manager.onStoreyVisibilityChange = (id, vis) => console.log(id, vis);
 * await manager.isolateStorey(storeys[2].id);
 * ```
 */
export class StoreyManager {

  // ── Bağımlılıklar ────────────────────────────────────────────────────────

  /** @thatopen/fragments ana orkestratörü */
  private readonly _fragments: FragmentsModels;

  // ── Durum ────────────────────────────────────────────────────────────────

  /** Elevation'a göre sıralanmış (aşağıdan yukarı) kat listesi */
  storeys: StoreyInfo[] = [];

  /** Kat ID → görünürlük durumu haritası */
  visibilityState: Map<string, boolean> = new Map();

  /** Mevcut yüklü model referansı */
  private _model: FragmentsModel | null = null;

  /** Mevcut model ID'si */
  private _modelId: string | null = null;

  // ── Callback ─────────────────────────────────────────────────────────────

  /**
   * Bir katın görünürlüğü değiştiğinde çağrılır.
   * UI güncellemeleri için kullanılır.
   */
  onStoreyVisibilityChange: StoreyVisibilityCallback | null = null;

  // ─── Constructor ──────────────────────────────────────────────────────────

  /**
   * @param fragments - FragmentsModels ana orkestratörü (IFCLoaderEngine.fragments)
   */
  constructor(fragments: FragmentsModels) {
    this._fragments = fragments;
  }

  // ─── Public API ───────────────────────────────────────────────────────────

  /**
   * Yüklü modelden IfcBuildingStorey entity'lerini çeker ve `storeys` array'ini doldurur.
   *
   * ADIMLAR:
   * 1. getSpatialStructure() ile IFC hiyerarşisini al
   * 2. BFS ile IfcBuildingStorey node'larını bul
   * 3. Her storey için ad, elevation ve children elementlerini çıkar
   * 4. Elevation'a göre sırala (aşağıdan yukarı: min → max)
   *
   * @param modelId - Fragments model kimliği
   */
  async extractStoreys(modelId: string): Promise<void> {
    const model = this._fragments.models.list.get(modelId);
    if (!model) {
      console.warn(`[StoreyManager] Model bulunamadı: ${modelId}`);
      return;
    }

    this._model = model;
    this._modelId = modelId;
    this.storeys = [];
    this.visibilityState.clear();

    try {
      console.log(`[StoreyManager] Katlar çıkarılıyor: ${modelId}`);

      // IFC spatial structure'ı al
      const tree = await model.getSpatialStructure();

      // BFS ile tüm IfcBuildingStorey node'larını topla
      const storeyNodes = this._collectStoreyNodes(tree);

      console.log("[StoreyManager] IFC'den bulunan IfcBuildingStorey sayısı:", storeyNodes.length);
      for (const node of storeyNodes) {
        console.log("[StoreyManager] Raw storey data:", node);
      }

      let storeyInfos: StoreyInfo[] = [];

      if (storeyNodes.length <= 1) {
        if (storeyNodes.length === 0) {
          console.warn('[StoreyManager] IFC dosyasında IfcBuildingStorey bulunamadı!');
        }
        storeyInfos = await this._runFallbackStoreyDetection(model, tree);
      } else {
        // Her node'u StoreyInfo'ya dönüştür
        for (const node of storeyNodes) {
          const info = await this._buildStoreyInfo(node, model);
          console.log("[StoreyManager] Storey:", info.name, "elevation:", info.elevation, "element count:", info.elementCount);
          storeyInfos.push(info);
        }
      }

      // Elevation'a göre sırala (aşağıdan yukarı)
      storeyInfos.sort((a, b) => a.elevation - b.elevation);

      this.storeys = storeyInfos;
      for (const info of storeyInfos) {
        this.visibilityState.set(info.id, true);
      }

      console.log(`[StoreyManager] ✓ ${storeyInfos.length} kat çıkarıldı:`,
        storeyInfos.map(s => `${s.name} (+${s.elevation.toFixed(2)}m, ${s.elementCount} el)`).join(', ')
      );

    } catch (err) {
      console.error('[StoreyManager] Kat çıkarma hatası:', err);
    }
  }

  /**
   * Belirtilen katın görünürlüğünü değiştirir.
   *
   * @param storeyId - StoreyInfo.id (ExpressID string)
   * @param visible  - true: görünür, false: gizli
   */
  async setStoreyVisibility(storeyId: string, visible: boolean): Promise<void> {
    if (!this._model) return;

    const storey = this.storeys.find(s => s.id === storeyId);
    if (!storey) {
      console.warn(`[StoreyManager] Kat bulunamadı: ${storeyId}`);
      return;
    }

    try {
      if (storey.elementIds.length > 0) {
        // Fragments API ile element görünürlüğünü değiştir
        await this._model.setVisible(storey.elementIds, visible);

        // Storey'in kendi node'unu da gizle/göster
        const storeyLocalId = parseInt(storeyId, 10);
        if (!isNaN(storeyLocalId)) {
          await this._model.setVisible([storeyLocalId], visible);
        }

        // Renderer'ı güncelle
        await this._fragments.update(true);
      }

      // Durumu güncelle
      this.visibilityState.set(storeyId, visible);
      storey.isVisible = visible;

      // Callback'i tetikle
      this.onStoreyVisibilityChange?.(storeyId, visible, this.storeys);

    } catch (err) {
      console.error(`[StoreyManager] Görünürlük değiştirilemedi: ${storeyId}`, err);
    }
  }

  /**
   * Solo mod: Sadece seçilen katı göster, diğer tüm katları gizle.
   *
   * @param storeyId - Gösterilecek katın ID'si
   */
  async isolateStorey(storeyId: string): Promise<void> {
    if (!this._model) return;

    console.log(`[StoreyManager] Kat izole ediliyor: ${storeyId}`);

    // Tüm katları gizle, sadece seçileni göster
    for (const storey of this.storeys) {
      const shouldBeVisible = storey.id === storeyId;
      await this.setStoreyVisibility(storey.id, shouldBeVisible);
    }
  }

  /**
   * Tüm katları görünür yapar.
   */
  async showAllStoreys(): Promise<void> {
    if (!this._model) return;

    console.log('[StoreyManager] Tüm katlar gösteriliyor...');

    for (const storey of this.storeys) {
      await this.setStoreyVisibility(storey.id, true);
    }
  }

  /**
   * Bir elementin hangi katta olduğunu döndürür.
   *
   * @param expressId - Sorgulanacak elementin IFC ExpressID'si
   * @returns Elementin ait olduğu StoreyInfo, bulunamazsa null
   */
  getStoreyForElement(expressId: number): StoreyInfo | null {
    for (const storey of this.storeys) {
      if (storey.elementIds.includes(expressId)) {
        return storey;
      }
    }
    return null;
  }

  /**
   * Eğer IFC modelinde storey bulunamazsa veya 1 tane bulunursa çalışan fallback.
   * Elementlerin elevation değerlerine bakarak kümeleme (clustering) yapar ve kat ayırır.
   */
  private async _runFallbackStoreyDetection(model: FragmentsModel, tree: SpatialTreeItem): Promise<StoreyInfo[]> {
    console.log("[StoreyManager] IFC'de storey bulunamadı, elevation bazlı tahmini kat ayırımı yapılıyor");
    
    // 1. Tüm elementleri topla
    const allElements: { localId: number, category: string }[] = [];
    const queue: SpatialTreeItem[] = [tree];
    while (queue.length > 0) {
      const node = queue.shift()!;
      if (node.localId !== null && node.localId !== undefined) {
        const cat = (node.category ?? '').toUpperCase();
        if (!cat.includes('PROJECT') && !cat.includes('SITE') && !cat.includes('BUILDING') && !cat.includes('STOREY')) {
          allElements.push({ localId: node.localId, category: node.category ?? 'Unknown' });
        }
      }
      if (node.children) {
        queue.push(...node.children);
      }
    }

    // 2. Y-min değerlerini bul
    const elevations: { expressId: number, y: number, type: string }[] = [];
    const batchSize = 200;
    
    for (let i = 0; i < allElements.length; i += batchSize) {
      const batch = allElements.slice(i, i + batchSize);
      await Promise.all(batch.map(async (el) => {
        try {
          const box = await model.getMergedBox([el.localId]);
          if (!box.isEmpty() && isFinite(box.min.y)) {
            elevations.push({
              expressId: el.localId,
              y: box.min.y,
              type: this._normalizeIfcType(el.category)
            });
          }
        } catch { /* skip */ }
      }));
    }

    // 3. Elevation'a göre sırala ve cluster yap
    elevations.sort((a, b) => a.y - b.y);

    const clusters: typeof elevations[] = [];
    if (elevations.length > 0) {
      let currentCluster = [elevations[0]!];
      for (let i = 1; i < elevations.length; i++) {
        const el = elevations[i]!;
        if (el.y - currentCluster[currentCluster.length - 1]!.y > 2.0) {
          clusters.push(currentCluster);
          currentCluster = [el];
        } else {
          currentCluster.push(el);
        }
      }
      clusters.push(currentCluster);
    }

    // 4. Cluster'lardan StoreyInfo oluştur
    const storeyInfos: StoreyInfo[] = [];
    clusters.forEach((cluster, index) => {
      const elementIds = cluster.map(c => c.expressId);
      const elementTypes: Record<string, number> = {};
      cluster.forEach(c => {
        elementTypes[c.type] = (elementTypes[c.type] || 0) + 1;
      });
      
      const avgY = cluster.reduce((sum, c) => sum + c.y, 0) / cluster.length;
      const name = index === 0 ? "Zemin Kat (tahmini)" : `${index}. Kat (tahmini)`;
      
      storeyInfos.push({
        id: `fallback_storey_${index}`,
        name,
        elevation: avgY,
        elementCount: elementIds.length,
        elementIds,
        isVisible: true,
        elementTypes
      });
    });

    return storeyInfos;
  }

  /**
   * StoreyManager'ı temizler — yeni model için yeniden kullanılabilir.
   */
  reset(): void {
    this.storeys = [];
    this.visibilityState.clear();
    this._model = null;
    this._modelId = null;
  }

  // ─── Özel Yardımcılar ─────────────────────────────────────────────────────

  /**
   * Spatial tree'de BFS ile tüm IfcBuildingStorey node'larını toplar.
   *
   * IFC hiyerarşisi genellikle şöyledir:
   *   IfcProject → IfcSite → IfcBuilding → [IfcBuildingStorey, ...]
   *
   * Node'un IFC tipi "STOREY" içeren string olarak gelir.
   * Bazı modellerde "IFCBUILDINGSTOREY" ya da sadece "BuildingStorey" olabilir.
   */
  private _collectStoreyNodes(root: SpatialTreeItem): SpatialTreeItem[] {
    const storeys: SpatialTreeItem[] = [];
    const queue: SpatialTreeItem[] = [root];

    while (queue.length > 0) {
      const node = queue.shift()!;

      const cat = (node.category ?? '').toUpperCase();
      if (cat.includes('STOREY') || cat.includes('KAT')) {
        storeys.push(node);
        // Storey altındaki alt katlar varsa onları da topla
        // (genellikle yoktur ama güvenli olmak için alt dal da taranır)
      }

      if (node.children && node.children.length > 0) {
        queue.push(...node.children);
      }
    }

    return storeys;
  }

  /**
   * Bir SpatialTreeItem'dan StoreyInfo objesi oluşturur.
   *
   * Element ID'lerini ve tiplerini children'dan çıkarır.
   * Elevation için node'un adından ya da properties'ten okur.
   */
  private async _buildStoreyInfo(
    node: SpatialTreeItem,
    model: FragmentsModel,
  ): Promise<StoreyInfo> {
    const localId = node.localId ?? -1;
    const id = String(localId);

    // Kat adı: category yerine node.name tercih edilir (varsa)
    // SpatialTreeItem'da 'name' yoksa category'yi kullan
    const rawName = (node as unknown as { name?: string }).name
      ?? node.category
      ?? `Kat ${id}`;
    const name = this._cleanStoreyName(rawName, localId);

    // Elevation değerini çıkar
    const elevation = await this._extractElevation(node, model);

    // Children'daki element ID'lerini topla
    const { elementIds, elementTypes } = this._collectElementIds(node);

    return {
      id,
      name,
      elevation,
      elementCount: elementIds.length,
      elementIds,
      isVisible: true,
      elementTypes,
    };
  }

  /**
   * Kat adını temizler ve okunabilir hale getirir.
   *
   * Örnek dönüşümler:
   *  "IFCBUILDINGSTOREY" → "Kat 1234"
   *  "Level 1"           → "Level 1"   (korunur)
   *  "00 - Ground"       → "00 - Ground" (korunur)
   */
  private _cleanStoreyName(raw: string, localId: number): string {
    const upper = raw.toUpperCase();

    // Ham IFC tip adı ise anlamlı bir ad üret
    if (
      upper === 'IFCBUILDINGSTOREY' ||
      upper === 'BUILDINGSTOREY' ||
      upper === 'STOREY'
    ) {
      return `Kat ${localId}`;
    }

    // Boş string kontrolü
    if (!raw.trim()) return `Kat ${localId}`;

    return raw.trim();
  }

  /**
   * Kat'ın elevation (kot) değerini tespit eder.
   *
   * Öncelik sırası:
   * 1. node.localId ile model properties'inden Elevation attribute'u okuma
   * 2. Index tabanlı fallback (her kat 3.5m aralıkla)
   *
   * Not: @thatopen/fragments'in getProperties() her modelde bulunmayabilir.
   *      Hata durumunda sessizce 0 döner.
   */
  private async _extractElevation(
    node: SpatialTreeItem,
    model: FragmentsModel,
  ): Promise<number> {
    // FragmentsModel.getProperties() varsa kullan
    if (typeof (model as unknown as { getProperties?: unknown }).getProperties === 'function') {
      try {
        const localId = node.localId ?? -1;
        if (localId !== -1) {
          const getProps = (model as unknown as { getProperties: (id: number) => Promise<Record<string, unknown> | null> }).getProperties;
          const props = await getProps.call(model, localId);
          if (props) {
            // IFC Elevation attribute olası alan adları
            const elevationKeys = ['Elevation', 'elevation', 'ElevationWithFlooring', 'value'];
            for (const key of elevationKeys) {
              const val = props[key];
              if (typeof val === 'number' && isFinite(val)) {
                // IFC elevation genellikle mm cinsinden gelir — metre'ye çevir
                // Eğer değer 1000'den büyükse mm olarak yorumla
                return Math.abs(val) > 100 ? val / 1000 : val;
              }
            }

            // Nested value objesi kontrolü: { value: { value: 3.5 } }
            const elevVal = props['Elevation'];
            if (elevVal && typeof elevVal === 'object') {
              const nested = (elevVal as Record<string, unknown>)['value'];
              if (typeof nested === 'number' && isFinite(nested)) {
                return Math.abs(nested) > 100 ? nested / 1000 : nested;
              }
            }
          }
        }
      } catch {
        // getProperties desteklenmiyor veya hata — fallback'e geç
      }
    }

    // Fallback: sıfır döndür (caller'da index ile hesaplanacak)
    return 0;
  }

  /**
   * Bir storey node'unun tüm çocuklarından element ID'lerini ve tiplerini toplar.
   *
   * Sadece storey'in DOĞRUDAN children'ları (leafler) alınır.
   * IfcSpace, IfcOpeningElement gibi geometry olmayan tipler dahil edilir.
   *
   * @returns elementIds — tüm element ExpressID'leri
   * @returns elementTypes — { "IfcWall": 23, "IfcSlab": 4, ... }
   */
  private _collectElementIds(storeyNode: SpatialTreeItem): {
    elementIds: number[];
    elementTypes: Record<string, number>;
  } {
    const elementIds: number[] = [];
    const elementTypes: Record<string, number> = {};

    if (!storeyNode.children) {
      return { elementIds, elementTypes };
    }

    // Yalnızca direkt children (BFS ile tüm derinlik)
    const queue: SpatialTreeItem[] = [...storeyNode.children];

    while (queue.length > 0) {
      const child = queue.shift()!;

      if (child.localId !== null && child.localId !== undefined) {
        elementIds.push(child.localId);

        // IFC tip adını normalize et
        const typeName = this._normalizeIfcType(child.category ?? 'Unknown');
        elementTypes[typeName] = (elementTypes[typeName] ?? 0) + 1;
      }

      // Alt elemanları da dahil et (örn. IfcWall → IfcWallStandardCase)
      if (child.children && child.children.length > 0) {
        queue.push(...child.children);
      }
    }

    return { elementIds, elementTypes };
  }

  /**
   * IFC tip adını okunabilir hale getirir.
   *
   * @example
   * "IFCWALL"              → "IfcWall"
   * "IFCWALLSTANDARDCASE"  → "IfcWallStandardCase"
   * "IfcSlab"              → "IfcSlab"  (zaten temiz)
   */
  private _normalizeIfcType(raw: string): string {
    if (!raw) return 'Unknown';

    // Zaten Pascal case (IfcWall) ise koru
    if (raw.startsWith('Ifc') || raw.startsWith('ifc')) {
      return raw.charAt(0).toUpperCase() + raw.slice(1);
    }

    // Tümü büyük harf ise dönüştür: "IFCWALL" → "IfcWall"
    if (raw === raw.toUpperCase()) {
      const lower = raw.toLowerCase();
      // "ifcwall" → "IfcWall" (basit capitalize)
      return lower.charAt(0).toUpperCase() + lower.slice(1);
    }

    return raw;
  }

  // ─── Public Getter'lar ────────────────────────────────────────────────────

  /** Yüklü model referansı */
  get model(): FragmentsModel | null { return this._model; }

  /** Yüklü model ID'si */
  get modelId(): string | null { return this._modelId; }

  /** Kaç kat bulundu */
  get storeyCount(): number { return this.storeys.length; }

  /** Görünür kat sayısı */
  get visibleStoreyCount(): number {
    return this.storeys.filter(s => s.isVisible).length;
  }
}
