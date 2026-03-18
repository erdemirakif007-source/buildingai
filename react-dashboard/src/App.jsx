import { useState } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import QuickActions from './components/QuickActions'
import AIInputBar from './components/AIInputBar'
import EngineeringPanel from './components/EngineeringPanel'

export default function App() {
  const [activePage, setActivePage]   = useState('home')
  const [resultHtml, setResultHtml]   = useState(null)
  const [isLoading, setIsLoading]     = useState(false)

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
        <main className="flex-1 overflow-y-auto px-10 py-5 space-y-3">
          <QuickActions />
          <AIInputBar onSend={handleSend} />
          <EngineeringPanel resultHtml={resultHtml} />
        </main>

      </div>
    </div>
  )
}
