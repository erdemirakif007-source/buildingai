/**
 * scripts/copy-wasm.js
 *
 * Bu script, web-ifc paketinin içindeki WebAssembly (.wasm) dosyalarını
 * projenin public/ klasörüne kopyalar.
 *
 * NEDEN GEREKLİ?
 * web-ifc, IFC dosyalarını parse etmek için C++ ile yazılmış bir kütüphaneyi
 * WebAssembly olarak derler. Bu WASM dosyalarının tarayıcıdan doğrudan
 * erişilebilir olması gerekir (Vite bundle'ına dahil edilemezler).
 * Bu yüzden public/ klasörüne kopyalanırlar ve statik dosya olarak sunulurlar.
 *
 * KULLANIM:
 * Bu script package.json'daki "postinstall" hook'u ile otomatik çalışır.
 * Manuel çalıştırmak için: node scripts/copy-wasm.js
 */

import { copyFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

// ESM'de __dirname yok, bu yüzden import.meta.url'den türetiyoruz
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Proje kök dizini (scripts/ bir üst klasörün altında)
const rootDir = join(__dirname, '..');

// Kaynak: node_modules içindeki web-ifc WASM dosyaları
const wasmSourceDir = join(rootDir, 'node_modules', 'web-ifc');

// Hedef: public/ klasörü (Vite statik dosya sunucu kökü)
const publicDir = join(rootDir, 'public');

// Kopyalanacak WASM dosyaları listesi
const wasmFiles = [
  'web-ifc.wasm',        // Tekli iş parçacığı (single-thread) versiyonu
  'web-ifc-mt.wasm',     // Çoklu iş parçacığı (multi-thread) versiyonu
];

// public/ klasörü yoksa oluştur
if (!existsSync(publicDir)) {
  mkdirSync(publicDir, { recursive: true });
  console.log('[copy-wasm] public/ klasörü oluşturuldu.');
}

// Her WASM dosyasını kopyala
let copiedCount = 0;
for (const wasmFile of wasmFiles) {
  const sourcePath = join(wasmSourceDir, wasmFile);
  const destPath = join(publicDir, wasmFile);

  if (!existsSync(sourcePath)) {
    console.warn(`[copy-wasm] UYARI: ${wasmFile} bulunamadı: ${sourcePath}`);
    continue;
  }

  try {
    copyFileSync(sourcePath, destPath);
    console.log(`[copy-wasm] ✓ ${wasmFile} → public/${wasmFile}`);
    copiedCount++;
  } catch (err) {
    console.error(`[copy-wasm] HATA: ${wasmFile} kopyalanamadı:`, err);
  }
}

console.log(`[copy-wasm] Tamamlandı: ${copiedCount}/${wasmFiles.length} dosya kopyalandı.`);
