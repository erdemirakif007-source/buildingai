/**
 * statusbar.ts
 *
 * BIM Viewer alt bilgi çubuğu (statusbar) UI bileşeni.
 *
 * Statusbar, kullanıcıya anlık durum bilgileri sağlar:
 *
 *  [Sol] Durum Göstergesi
 *   - ● Hazır       — yeşil nokta, sistem boşta
 *   - ● Yükleniyor  — sarı/animasyonlu nokta, işlem var
 *   - ● Hata        — kırmızı nokta, bir sorun oluştu
 *
 *  [Orta] Dosya Bilgisi
 *   - Yüklü dosya adı
 *   - Eleman sayısı (IfcWall: 42, IfcSlab: 18, ...)
 *   - Dosya boyutu
 *
 *  [Sağ] Performans Metrikleri
 *   - FPS (Frames Per Second) — render hızı
 *   - Draw calls — GPU'ya gönderilen çizim komutları
 *   - Triangle count — sahnedeki toplam üçgen sayısı
 *   - Bellek kullanımı (MB)
 *
 * GELECEKTEKİ GELİŞTİRMELER:
 *  - Gerçek zamanlı FPS ölçümü (requestAnimationFrame timestamp farkı)
 *  - THREE.WebGLRenderer.info ile draw call / triangle sayısı
 *  - Kamera konumu (X, Y, Z koordinatları)
 *  - Koordinat sistemi (IFC: Z-up vs Three.js: Y-up dönüşümü notu)
 */
/**
 * Statusbar DOM yapısını oluşturur ve belirtilen container'a ekler.
 *
 * @param container - Statusbar'ın ekleneceği DOM elementi (genellikle #app)
 * @returns Statusbar elementi referansı (update fonksiyonu için)
 */
export function createStatusbar(container) {
    console.log('[statusbar] Statusbar oluşturuluyor...');
    const statusbar = document.createElement('div');
    statusbar.id = 'statusbar';
    statusbar.setAttribute('role', 'status');
    statusbar.setAttribute('aria-live', 'polite'); // Ekran okuyucular için
    // ── Durum Göstergesi (Sol) ───────────────────────────────────────────────
    const statusItem = document.createElement('div');
    statusItem.className = 'status-item';
    statusItem.innerHTML = `
    <span class="status-indicator" id="status-indicator" aria-hidden="true"></span>
    <span class="status-message" id="status-message">BIM Viewer hazır</span>
  `;
    // ── Ayırıcı ─────────────────────────────────────────────────────────────
    const sep1 = document.createElement('div');
    sep1.className = 'status-separator';
    sep1.setAttribute('aria-hidden', 'true');
    sep1.textContent = '|';
    // ── Dosya Bilgisi (Orta) ─────────────────────────────────────────────────
    const fileInfo = document.createElement('div');
    fileInfo.className = 'status-item';
    fileInfo.id = 'status-file-info';
    fileInfo.textContent = 'Dosya yüklenmedi';
    // ── Boşluk Doldurucu ─────────────────────────────────────────────────────
    const spacer = document.createElement('div');
    spacer.style.flex = '1';
    // ── Performans Metrikleri (Sağ) ──────────────────────────────────────────
    const perfInfo = document.createElement('div');
    perfInfo.className = 'status-item';
    perfInfo.id = 'status-perf-info';
    perfInfo.innerHTML = `
    <span id="status-fps">-- FPS</span>
    <span class="status-separator" aria-hidden="true">|</span>
    <span id="status-triangles">-- ▲</span>
  `;
    // Öğeleri statusbar'a ekle
    statusbar.appendChild(statusItem);
    statusbar.appendChild(sep1);
    statusbar.appendChild(fileInfo);
    statusbar.appendChild(spacer);
    statusbar.appendChild(perfInfo);
    // Statusbar'ı #app kapsayıcısına ekle
    container.appendChild(statusbar);
    console.log('[statusbar] Statusbar hazır.');
    return statusbar;
}
/**
 * Statusbar'ı verilen durum bilgisiyle günceller.
 * Render döngüsünden veya event handler'lardan çağrılır.
 *
 * @param statusbar - Güncellenecek statusbar elementi
 * @param state     - Yeni durum verileri
 */
export function updateStatusbar(statusbar, state) {
    // Durum göstergesi noktası
    const indicator = statusbar.querySelector('#status-indicator');
    const message = statusbar.querySelector('#status-message');
    const fileInfo = statusbar.querySelector('#status-file-info');
    const fpsEl = statusbar.querySelector('#status-fps');
    const trianglesEl = statusbar.querySelector('#status-triangles');
    // Durum türüne göre renk sınıfı güncelle
    if (state.type !== undefined && indicator) {
        indicator.className = 'status-indicator';
        if (state.type === 'loading')
            indicator.classList.add('loading');
        else if (state.type === 'error')
            indicator.style.background = 'var(--color-error)';
        else if (state.type === 'success')
            indicator.style.background = 'var(--color-success)';
    }
    if (state.message !== undefined && message) {
        message.textContent = state.message;
    }
    if (state.fileName !== undefined && fileInfo) {
        const count = state.elementCount !== undefined
            ? ` — ${state.elementCount.toLocaleString('tr-TR')} eleman`
            : '';
        fileInfo.textContent = `📄 ${state.fileName}${count}`;
    }
    if (state.fps !== undefined && fpsEl) {
        fpsEl.textContent = `${Math.round(state.fps)} FPS`;
    }
    // Üçgen sayacı — gelecekte THREE.WebGLRenderer.info.render.triangles ile doldurulacak
    if (trianglesEl && state.elementCount !== undefined) {
        trianglesEl.textContent = `${state.elementCount.toLocaleString('tr-TR')} ▲`;
    }
}
//# sourceMappingURL=statusbar.js.map