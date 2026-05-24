import { useState } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import QuickActions from './components/QuickActions'
import AIInputBar from './components/AIInputBar'
import EngineeringPanel from './components/EngineeringPanel'
import KatalogTarayici from './components/KatalogTarayici'
import StokYonetimi from './components/StokYonetimi'
import MetrajYonetimi from './components/MetrajYonetimi'

function getToken() {
  return localStorage.getItem('bai_token') || ''
}

// BIM viewer iframe — served by Flask at /bim-viewer
function BimViewer({ onBack, santiyeId }) {
  const src = santiyeId
    ? `/bim-viewer/?auto_load=true&santiye_id=${santiyeId}`
    : '/bim-viewer/'
  return (
    <div style={{ position:'relative', width:'100%', height:'100%', display:'flex', flexDirection:'column' }}>
      <div style={{
        padding:'8px 16px', background:'rgba(5,8,16,0.96)',
        borderBottom:'1px solid rgba(255,255,255,0.06)',
        display:'flex', alignItems:'center', gap:12, flexShrink:0
      }}>
        <button onClick={onBack} style={{
          display:'flex', alignItems:'center', gap:6,
          background:'rgba(255,255,255,0.06)', border:'1px solid rgba(255,255,255,0.1)',
          color:'#94A3B8', borderRadius:8, padding:'6px 12px', fontSize:12,
          cursor:'pointer', fontFamily:'inherit'
        }}>
          ← Metraj'a Dön
        </button>
        <span style={{ fontSize:12, color:'#475569' }}>BIM Görüntüleyici</span>
      </div>
      <iframe
        src={src}
        title="BIM Viewer"
        style={{ flex:1, border:'none', width:'100%' }}
        allow="fullscreen"
      />
    </div>
  )
}

export default function App() {
  const [activePage, setActivePage]   = useState('home')
  const [resultHtml, setResultHtml]   = useState(null)
  const [isLoading, setIsLoading]     = useState(false)
  const [bimSantiyeId, setBimSantiyeId] = useState(null)

  // Simulate AI response (wire to real API later)
  const handleSend = async (soru) => {
    setIsLoading(true)
    setResultHtml(`<i style="color:#5a8aaa">⏳ Yanıt hazırlanıyor…</i>`)
    await new Promise(r => setTimeout(r, 800))
    setResultHtml(
      `<b style="color:#dce8f5">"${soru}"</b><br/><br/>` +
      `<span>AI yanıtı burada görünecek. Backend'i <code style="color:#FF6200">app.py /sor</code> endpoint'ine bağlayın.</span>`
    )
    setIsLoading(false)
  }

  return (
    /* dark class enables dark-mode Tailwind variants */
    <div className="dark h-screen flex flex-col bg-[#060a14] overflow-hidden">

      {/* ── Background layers ── */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        {/* Blueprint grid */}
        <div className="absolute inset-0 blueprint-grid" />
        {/* Construction silhouette */}
        <div className="absolute inset-0 construction-bg opacity-100" />
        {/* Teal radial glow */}
        <div
          className="absolute inset-0"
          style={{
            background:
              'radial-gradient(ellipse 85% 65% at 62% 45%, rgba(13,200,185,0.22) 0%, rgba(6,100,160,0.14) 38%, transparent 68%)',
          }}
        />
        {/* Top-right accent */}
        <div
          className="absolute inset-0"
          style={{
            background:
              'radial-gradient(ellipse 55% 60% at 90% 10%, rgba(0,210,230,0.14) 0%, transparent 55%)',
          }}
        />
      </div>

      {/* ── Header ── */}
      <div className="relative z-10 flex-shrink-0">
        <Header />
      </div>

      {/* ── Body row ── */}
      <div className="relative z-10 flex flex-1 overflow-hidden">

        {/* Sidebar */}
        <Sidebar active={activePage} setActive={setActivePage} />

        {/* Main content */}
        <main className={`flex-1 overflow-hidden ${
          activePage === 'katalog' || activePage === 'stok' || activePage === 'metraj' || activePage === 'bim'
            ? 'flex flex-col'
            : 'overflow-y-auto px-10 py-5 space-y-3'
        }`}>
          {activePage === 'katalog' ? (
            <KatalogTarayici token={getToken()} />
          ) : activePage === 'stok' ? (
            <StokYonetimi token={getToken()} />
          ) : activePage === 'metraj' ? (
            <div style={{ flex:1, overflowY:'auto' }}>
              <MetrajYonetimi
                token={getToken()}
                santiyeId={1}
                santiyeAdi="İstanbul Kartal"
                onShow3D={() => { setBimSantiyeId(1); setActivePage('bim'); }}
              />
            </div>
          ) : activePage === 'bim' ? (
            <BimViewer onBack={() => setActivePage('metraj')} santiyeId={bimSantiyeId} />
          ) : (
            <>
              <QuickActions />
              <AIInputBar onSend={handleSend} />
              <EngineeringPanel resultHtml={resultHtml} />
            </>
          )}
        </main>

      </div>
    </div>
  )
}
