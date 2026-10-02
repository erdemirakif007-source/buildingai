/// <reference types="vite/client" />

/**
 * vite-env.d.ts
 *
 * Vite ortam değişkenleri ve özel modül tanımları.
 * Bu dosya Vite'ın yerleşik tip tanımlarını projeye dahil eder.
 *
 * CSS MODÜL BEYANNAMESI:
 * TypeScript, CSS/PNG/SVG gibi dosyaları modül olarak tanımaz.
 * Bu tanımlar sayesinde `import './styles/main.css'` gibi
 * side-effect import'lar hata vermez.
 */

// CSS dosyalarını side-effect modül olarak tanımla
declare module '*.css' {
  const css: string;
  export default css;
}

// WASM modüllerini URL string olarak tanımla
declare module '*.wasm' {
  const url: string;
  export default url;
}
