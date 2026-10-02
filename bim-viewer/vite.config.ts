// vite.config.ts
// BIM Viewer için Vite yapılandırma dosyası.
// web-ifc paketi WASM (WebAssembly) dosyaları kullandığından,
// bu dosyaların Vite tarafından bundle edilmemesi gerekiyor.
// Aksi hâlde WASM binary'leri bozulabilir.

import { defineConfig, type Plugin } from 'vite';
import fs from 'fs';

// ─── web-ifc pthread worker URL düzeltmesi ─────────────────────────────────
//
// Problem:
//   web-ifc (emscripten/pthread), pthread worker'larını yüklemek için
//   kendi script URL'ini (_scriptName) kullanır. Tarayıcı ES modüllerinde
//   document.currentScript her zaman null olduğundan _scriptName = undefined
//   olur. Bu durumda new Worker(undefined) → http://localhost:5173/undefined
//   adresine istek gider ve HTML 404 sayfası döner →
//   "Unexpected token '<'" hatasına yol açar.
//
// Çözüm:
//   `load` hook ile web-ifc-api.js dosyasını doğrudan diskten okuyoruz
//   ve _scriptName fallback'ini '/web-ifc-api.js' olarak patch'liyoruz.
//   Bu yöntem Vite'ın pre-bundle cache'ini atlar.
//   public/web-ifc-api.js worker script olarak sunulur.
//
const fixWebIfcPthreadUrl: Plugin = {
  name: 'fix-web-ifc-pthread-url',

  // load hook: transform'dan önce çalışır, pre-bundle cache'i atlar.
  load(id) {
    // Sadece web-ifc-api.js dosyasını yakala
    if (!id.includes('web-ifc-api.js')) return null;
    // Query string'leri temizle (?v=... gibi)
    const cleanId = id.split('?')[0];
    if (!cleanId.endsWith('web-ifc-api.js')) return null;
    // Sadece node_modules içindekini patch'le (public/ ve diğerlerini değil)
    if (!cleanId.includes('node_modules')) return null;

    try {
      const raw = fs.readFileSync(cleanId, 'utf-8');
      const patched = raw.replaceAll(
        'var _scriptName = globalThis.document?.currentScript?.src;',
        "var _scriptName = globalThis.document?.currentScript?.src ?? '/bim-viewer/web-ifc-api.js';",
      );
      console.log('[vite-plugin] web-ifc-api.js patch uygulandı →', cleanId);
      return { code: patched, map: null };
    } catch {
      return null;
    }
  },
};

export default defineConfig({
  plugins: [fixWebIfcPthreadUrl],

  // Flask'ta /bim-viewer altında mount edildiğinden base path zorunlu
  base: '/bim-viewer/',

  // WASM dosyalarını statik asset olarak tanıt
  // (web-ifc.wasm ve web-ifc-mt.wasm public/ klasöründen sunulacak)
  assetsInclude: ['**/*.wasm'],

  optimizeDeps: {
    // web-ifc ve @thatopen paketlerini Vite'ın dependency pre-bundling'inden hariç tut.
    // @thatopen/fragments pre-bundle edilirse web-ifc-api.js'i içine alır ve
    // load hook'umuz çalışmaz → _scriptName = undefined kalır → worker patlar.
    exclude: ['web-ifc', '@thatopen/fragments', '@thatopen/components'],
  },

  server: {
    // Geliştirme sunucusu portu
    port: 5173,

    // WASM dosyaları için gerekli HTTP başlıkları
    // (SharedArrayBuffer / multi-thread desteği için COOP/COEP)
    headers: {
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'require-corp',
    },
  },
});
