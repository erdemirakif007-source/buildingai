/**
 * main.ts — BIM Viewer uygulama giriş noktası.
 *
 * Tüm UI ve 3D sahne yönetimi BIMViewer sınıfı tarafından yapılır.
 * Bu dosya sadece BIMViewer'ı başlatır.
 */

import './styles/main.css';
import { BIMViewer } from './viewer/BIMViewer';

async function main(): Promise<void> {
  console.log('🏗️  BuildingAI BIM Viewer v0.1.0');

  const viewer = new BIMViewer('bim-viewer-app');
  await viewer.initialize();

  // Debug: Browser console'dan erişim
  (window as Window & { __viewer?: BIMViewer }).__viewer = viewer;
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => { void main(); });
} else {
  void main();
}
