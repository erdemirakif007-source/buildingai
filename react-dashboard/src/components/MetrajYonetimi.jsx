// MetrajYonetimi.jsx — Metraj Yönetimi sayfası
// KPI kartları + görsel cephe haritası + iş kalemi tablosu
import { useState, useEffect, useMemo } from 'react'
import MetrajCepheMap from './MetrajCepheMap'
import { TrendingUp, Clock, Layers, BarChart2, ChevronRight, Plus, Upload, RefreshCw } from 'lucide-react'

const BASE = ''   // proxy ile localhost:8000 — vite.config.js'de /api tanımlı

// ── Helpers ──────────────────────────────────────────────────────────────────

function kisaltma(etiket) {
  if (!etiket) return '?'
  const e = etiket.trim()
  if (/çatı/i.test(e))  return 'ÇT'
  if (/bodrum/i.test(e)) return 'B' + (e.match(/\d+/) || [''])[0]
  if (/zemin/i.test(e))  return 'ZM'
  const m = e.match(/(\d+)/)
  if (m) return 'K' + m[1]
  return e.slice(0, 2).toUpperCase()
}

function durumHarita(durum) {
  if (durum === 'tamamlandi') return 'tamam'
  if (durum === 'devam_eden') return 'devam'
  return 'planli'
}

const RENK_PALETi = ['#FF6B2C','#2563EB','#16A34A','#7C3AED','#D97706','#0891B2','#DB2777']

function buildFloorsByBlock(binalar) {
  return Object.fromEntries(
    binalar.map(b => {
      const allKalemler = b.katlar.flatMap(k =>
        k.mahaller.flatMap(m => m.is_kalemleri)
      )
      const floors = b.katlar
        .slice()
        .sort((a, b) => b.kat_no - a.kat_no)  // yüksekten aşağı
        .map(k => {
          const kalemler = k.mahaller.flatMap(m => m.is_kalemleri)
          const pct = kalemler.length === 0 ? 0
            : kalemler.reduce((s, ik) => s + (ik.son_ilerleme_yuzde || 0), 0) / kalemler.length
          const durum = kalemler.every(ik => ik.durum === 'tamamlandi') ? 'tamam'
            : kalemler.some(ik => ik.durum === 'devam_eden') ? 'devam' : 'planli'

          const breakdown = kalemler.map((ik, i) => ({
            name:  ik.tanim.split('(')[0].trim(),
            pct:   Math.round(ik.son_ilerleme_yuzde || 0),
            color: RENK_PALETi[i % RENK_PALETi.length],
            qty:   `${ik.metraj} ${ik.birim}`,
          }))

          const daireSayisi = k.mahaller.filter(m =>
            /daire|konut|rezidans/i.test(m.mahal_tipi || m.ad)
          ).length || k.mahaller.length

          return {
            id:        String(k.id),
            label:     k.etiket || `Kat ${k.kat_no}`,
            short:     kisaltma(k.etiket || `Kat ${k.kat_no}`),
            units:     daireSayisi,
            pct:       Math.round(pct),
            status:    durum,
            breakdown: breakdown.length ? breakdown : null,
          }
        })
      return [String(b.id), floors]
    })
  )
}

// ── KPI Kart ─────────────────────────────────────────────────────────────────
function KpiKart({ icon: Icon, label, value, sub, accent }) {
  return (
    <div style={{
      background:'#fff', border:'1px solid #EEF0F3', borderRadius:12,
      padding:'14px 18px', display:'flex', alignItems:'flex-start', gap:12,
      boxShadow:'0 1px 2px rgba(15,23,42,.04)'
    }}>
      <div style={{
        width:36, height:36, borderRadius:9, display:'grid', placeItems:'center', flexShrink:0,
        background: accent + '14', color: accent
      }}>
        <Icon size={17} strokeWidth={1.8}/>
      </div>
      <div style={{ minWidth:0 }}>
        <div style={{ fontSize:10, color:'#94A3B8', textTransform:'uppercase',
          letterSpacing:'.07em', fontWeight:600, marginBottom:2 }}>{label}</div>
        <div style={{ fontSize:18, fontWeight:700, color:'#0F172A', lineHeight:1.2 }}>{value}</div>
        {sub && <div style={{ fontSize:11, color:'#94A3B8', marginTop:2 }}>{sub}</div>}
      </div>
    </div>
  )
}

// ── İş Kalemi Tablosu ─────────────────────────────────────────────────────────
function IsKalemiTablosu({ kalemler, loading }) {
  const fmt = (n) => new Intl.NumberFormat('tr-TR', { minimumFractionDigits:2 }).format(n)

  if (loading) return (
    <div style={{ padding:'40px 0', textAlign:'center', color:'#94A3B8', fontSize:13 }}>
      <RefreshCw size={18} style={{ animation:'spin 1s linear infinite', display:'inline-block', marginBottom:8 }}/>
      <div>Yükleniyor…</div>
    </div>
  )

  if (!kalemler.length) return (
    <div style={{ padding:'40px 0', textAlign:'center', color:'#94A3B8', fontSize:13 }}>
      Seçili katta iş kalemi yok
    </div>
  )

  const durumBadge = (d) => {
    const meta = {
      tamamlandi: { label:'Tamamlandı', bg:'#F0FDF4', color:'#16A34A' },
      devam_eden: { label:'Devam',       bg:'#FFFBEB', color:'#D97706' },
      planli:     { label:'Planlı',      bg:'#F8FAFC', color:'#94A3B8' },
      iptal:      { label:'İptal',       bg:'#FFF1F2', color:'#E11D48' },
    }
    const m = meta[d] || meta.planli
    return (
      <span style={{ fontSize:10.5, fontWeight:600, padding:'3px 8px', borderRadius:6,
        background:m.bg, color:m.color }}>{m.label}</span>
    )
  }

  const cols = [
    { key:'poz_no',         label:'Poz No',      w:'10%' },
    { key:'tanim',          label:'Tanım',        w:'30%' },
    { key:'birim',          label:'Birim',        w:'7%'  },
    { key:'metraj',         label:'Metraj',       w:'10%' },
    { key:'birim_fiyat_tl', label:'Birim Fiyat',  w:'12%' },
    { key:'toplam_fiyat_tl',label:'Toplam',       w:'13%' },
    { key:'son_ilerleme_yuzde', label:'İlerleme', w:'10%' },
    { key:'durum',          label:'Durum',        w:'8%'  },
  ]

  return (
    <div style={{ overflowX:'auto' }}>
      <table style={{ width:'100%', borderCollapse:'collapse', fontSize:12 }}>
        <thead>
          <tr style={{ background:'#F8FAFC', borderBottom:'1px solid #EEF0F3' }}>
            {cols.map(c => (
              <th key={c.key} style={{ padding:'8px 12px', textAlign:'left', fontWeight:600,
                color:'#94A3B8', fontSize:10, letterSpacing:'.07em', textTransform:'uppercase',
                width:c.w }}>{c.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {kalemler.map((ik, i) => (
            <tr key={ik.id} style={{
              borderBottom:'1px solid #EEF0F3',
              background: i % 2 === 0 ? '#fff' : '#FAFBFC'
            }}>
              <td style={{ padding:'10px 12px', color:'#2563EB', fontFamily:'monospace', fontSize:11 }}>
                {ik.poz_no || '—'}
              </td>
              <td style={{ padding:'10px 12px', color:'#0F172A', fontWeight:500 }}>{ik.tanim}</td>
              <td style={{ padding:'10px 12px', color:'#475569' }}>{ik.birim}</td>
              <td style={{ padding:'10px 12px', color:'#475569', fontFamily:'monospace' }}>
                {fmt(ik.metraj)}
              </td>
              <td style={{ padding:'10px 12px', color:'#475569', fontFamily:'monospace' }}>
                {fmt(ik.birim_fiyat_tl)} ₺
              </td>
              <td style={{ padding:'10px 12px', color:'#0F172A', fontWeight:600, fontFamily:'monospace' }}>
                {fmt(ik.toplam_fiyat_tl)} ₺
              </td>
              <td style={{ padding:'10px 12px' }}>
                <div style={{ display:'flex', alignItems:'center', gap:6 }}>
                  <div style={{ flex:1, height:4, background:'#F1F3F5', borderRadius:99, overflow:'hidden' }}>
                    <div style={{
                      width:`${ik.son_ilerleme_yuzde || 0}%`, height:'100%',
                      background: ik.son_ilerleme_yuzde >= 100 ? '#16A34A' : '#FF6B2C',
                      borderRadius:99
                    }}/>
                  </div>
                  <span style={{ fontSize:10.5, color:'#475569', fontFamily:'monospace', flexShrink:0 }}>
                    %{Math.round(ik.son_ilerleme_yuzde || 0)}
                  </span>
                </div>
              </td>
              <td style={{ padding:'10px 12px' }}>{durumBadge(ik.durum)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

// ── Sağ panel: İş Kalemi Dağılımı ────────────────────────────────────────────
function IsKalemiDagilimi({ kalemler }) {
  const fmt = (n) => new Intl.NumberFormat('tr-TR', { minimumFractionDigits:2 }).format(n)
  const toplam = kalemler.reduce((s, k) => s + (k.toplam_fiyat_tl || 0), 0)

  return (
    <div style={{ background:'#fff', border:'1px solid #EEF0F3', borderRadius:12,
      boxShadow:'0 1px 2px rgba(15,23,42,.04)', display:'flex', flexDirection:'column', height:'100%' }}>
      <div style={{ padding:'14px 18px 12px', borderBottom:'1px solid #EEF0F3',
        display:'flex', alignItems:'center', justifyContent:'space-between' }}>
        <div>
          <div style={{ fontSize:14, fontWeight:600, color:'#0F172A' }}>İş Kalemi Dağılımı</div>
          <div style={{ fontSize:11, color:'#94A3B8', marginTop:1 }}>Bütçeye göre</div>
        </div>
        <button style={{ fontSize:11, fontWeight:600, color:'#FF6B2C', background:'transparent',
          border:'none', cursor:'pointer', display:'flex', alignItems:'center', gap:4 }}>
          Detay <ChevronRight size={12}/>
        </button>
      </div>
      <div style={{ flex:1, overflowY:'auto', padding:'8px 0' }}>
        {kalemler.length === 0 && (
          <div style={{ padding:'32px 18px', textAlign:'center', color:'#94A3B8', fontSize:12 }}>
            Seçili kat için iş kalemi yok
          </div>
        )}
        {kalemler.map((ik, i) => {
          const pct = toplam > 0 ? (ik.toplam_fiyat_tl / toplam) * 100 : 0
          const color = RENK_PALETi[i % RENK_PALETi.length]
          return (
            <div key={ik.id} style={{ padding:'10px 18px', borderBottom:'1px solid #EEF0F3' }}>
              <div style={{ display:'flex', alignItems:'flex-start', justifyContent:'space-between', marginBottom:6 }}>
                <div style={{ display:'flex', alignItems:'center', gap:8, flex:1, minWidth:0 }}>
                  <span style={{ width:10, height:10, borderRadius:3, background:color, flexShrink:0 }}/>
                  <span style={{ fontSize:12, fontWeight:500, color:'#0F172A',
                    whiteSpace:'nowrap', overflow:'hidden', textOverflow:'ellipsis' }}>{ik.tanim}</span>
                </div>
                <span style={{ fontSize:12, fontWeight:700, color:'#0F172A',
                  flexShrink:0, marginLeft:8, fontFamily:'monospace' }}>
                  {fmt(ik.toplam_fiyat_tl)} ₺
                </span>
              </div>
              <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                <div style={{ flex:1, height:4, background:'#F1F3F5', borderRadius:99, overflow:'hidden' }}>
                  <div style={{ width:`${pct}%`, height:'100%', background:color, borderRadius:99,
                    transition:'width .4s ease' }}/>
                </div>
                <span style={{ fontSize:10.5, color:'#94A3B8', flexShrink:0, fontFamily:'monospace' }}>
                  %{pct.toFixed(1)}
                </span>
              </div>
              <div style={{ fontSize:10.5, color:'#94A3B8', marginTop:3 }}>
                {ik.metraj} {ik.birim} × {fmt(ik.birim_fiyat_tl)} ₺
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ── Ana sayfa ─────────────────────────────────────────────────────────────────
export default function MetrajYonetimi({ token, santiyeId, santiyeAdi, onShow3D }) {
  const [view, setView]             = useState('gorsel')   // 'gorsel' | 'klasik'
  const [hiyerarsi, setHiyerarsi]   = useState(null)
  const [ozet, setOzet]             = useState(null)
  const [loading, setLoading]       = useState(true)
  const [error, setError]           = useState(null)
  const [selectedFloor, setSelectedFloor] = useState(null)
  const [selectedBinaId, setSelectedBinaId] = useState(null)

  useEffect(() => {
    if (!santiyeId) return
    setLoading(true)
    setError(null)
    const hdrs = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }

    Promise.all([
      fetch(`${BASE}/api/v2/santiye/${santiyeId}/hiyerarsi`, { headers: hdrs }).then(r => r.json()),
      fetch(`${BASE}/api/metraj/ozet/${santiyeId}`, { headers: hdrs }).then(r => r.json()),
    ]).then(([h, o]) => {
      setHiyerarsi(h)
      setOzet(o)
      if (h.binalar?.length) setSelectedBinaId(String(h.binalar[0].id))
      setLoading(false)
    }).catch(e => {
      setError(e.message)
      setLoading(false)
    })
  }, [santiyeId, token])

  // Metraj haritası için blok ve kat verileri
  const blocks = useMemo(() => {
    if (!hiyerarsi?.binalar) return []
    return hiyerarsi.binalar.map(b => ({
      id:    String(b.id),
      label: b.ad,
      count: b.katlar?.length ?? 0,
    }))
  }, [hiyerarsi])

  const floorsByBlock = useMemo(() => {
    if (!hiyerarsi?.binalar) return {}
    return buildFloorsByBlock(hiyerarsi.binalar)
  }, [hiyerarsi])

  // Seçili kata ait iş kalemleri
  const selectedKalemler = useMemo(() => {
    if (!hiyerarsi?.binalar || !selectedFloor || !selectedBinaId) return []
    const bina = hiyerarsi.binalar.find(b => String(b.id) === selectedBinaId)
    if (!bina) return []
    const kat = bina.katlar.find(k => String(k.id) === selectedFloor.id)
    if (!kat) return []
    return kat.mahaller.flatMap(m => m.is_kalemleri)
  }, [hiyerarsi, selectedFloor, selectedBinaId])

  // KPI hesapları
  const kpiData = useMemo(() => {
    if (!hiyerarsi?.binalar || !ozet) return null
    const allKalemler = hiyerarsi.binalar.flatMap(b =>
      b.katlar.flatMap(k => k.mahaller.flatMap(m => m.is_kalemleri))
    )
    const toplam_butce = allKalemler.reduce((s, k) => s + (k.toplam_fiyat_tl || 0), 0)
    const genel_pct = allKalemler.length === 0 ? 0
      : allKalemler.reduce((s, k) => s + (k.son_ilerleme_yuzde || 0), 0) / allKalemler.length
    return { toplam_butce, genel_pct, ...ozet }
  }, [hiyerarsi, ozet])

  const fmtTL = (n) => new Intl.NumberFormat('tr-TR', { minimumFractionDigits:0, maximumFractionDigits:0 }).format(n) + ' ₺'

  if (loading) return (
    <div style={{ display:'flex', alignItems:'center', justifyContent:'center', height:'100%',
      color:'#94A3B8', fontSize:13, gap:10 }}>
      <RefreshCw size={18} style={{ animation:'spin 1s linear infinite' }}/>
      Metraj verileri yükleniyor…
    </div>
  )

  if (error) return (
    <div style={{ padding:32, color:'#E11D48', fontSize:13 }}>
      Veri yüklenemedi: {error}
    </div>
  )

  return (
    <div style={{ padding:'16px 24px', display:'flex', flexDirection:'column', gap:16,
      fontFamily:"Inter, system-ui, sans-serif", color:'#0F172A' }}>

      {/* Page title + actions */}
      <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', gap:12 }}>
        <div>
          <h1 style={{ margin:0, fontSize:20, fontWeight:700, color:'#0F172A' }}>Metraj Yönetimi</h1>
          <div style={{ fontSize:12, color:'#94A3B8', marginTop:2 }}>
            {santiyeAdi}
            {selectedFloor && ` › ${hiyerarsi?.binalar?.find(b => String(b.id) === selectedBinaId)?.ad} › ${selectedFloor.label}`}
          </div>
        </div>
        <div style={{ display:'flex', gap:8 }}>
          <button style={{
            display:'flex', alignItems:'center', gap:6, height:34, padding:'0 14px',
            borderRadius:9, border:'1px solid #E5E7EB', background:'#fff', color:'#475569',
            fontSize:12, fontWeight:500, cursor:'pointer'
          }}>
            <Upload size={13}/> Excel'den Yükle
          </button>
          <button style={{
            display:'flex', alignItems:'center', gap:6, height:34, padding:'0 14px',
            borderRadius:9, border:'none', background:'#FF6B2C', color:'#fff',
            fontSize:12, fontWeight:600, cursor:'pointer'
          }}>
            <Plus size={13}/> İş Kalemi Ekle
          </button>
        </div>
      </div>

      {/* KPI kartları */}
      {kpiData && (
        <div style={{ display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap:12 }}>
          <KpiKart icon={BarChart2} label="Toplam Bütçe"
            value={fmtTL(kpiData.toplam_butce)}
            sub={`${kpiData.toplam_kalem} iş kalemi`}
            accent="#FF6B2C"/>
          <KpiKart icon={Clock} label="Aktif İş Kalemi"
            value={kpiData.devam_eden}
            sub={`${kpiData.baslanmamis} planlı`}
            accent="#2563EB"/>
          <KpiKart icon={Layers} label="Tamamlanan"
            value={kpiData.tamamlanan}
            sub={`${kpiData.toplam_kalem} toplam kalem`}
            accent="#16A34A"/>
          <KpiKart icon={TrendingUp} label="Genel İlerleme"
            value={`%${kpiData.genel_pct?.toFixed(1) ?? 0}`}
            sub="tüm katlara göre ağırlıklı"
            accent="#7C3AED"/>
        </div>
      )}

      {/* Varyasyon toggle */}
      <div style={{ display:'flex', alignItems:'center', gap:10 }}>
        <span style={{ fontSize:10.5, color:'#94A3B8', fontWeight:600,
          textTransform:'uppercase', letterSpacing:'.07em' }}>VARYASYON</span>
        <div style={{ display:'inline-flex', background:'#F1F3F5', borderRadius:8,
          border:'1px solid #EEF0F3', padding:3, gap:2 }}>
          {[
            { id:'klasik', label:'Klasik · ağaç + tablo' },
            { id:'gorsel', label:'Görsel · ilerleme haritası' },
          ].map(v => (
            <button key={v.id} onClick={() => setView(v.id)} style={{
              padding:'5px 14px', borderRadius:6, border:'none', fontSize:12, fontWeight:500,
              fontFamily:'inherit', cursor:'pointer',
              background: view===v.id ? '#fff' : 'transparent',
              color: view===v.id ? '#0F172A' : '#94A3B8',
              boxShadow: view===v.id ? '0 1px 2px rgba(15,23,42,.06)' : 'none',
            }}>{v.label}</button>
          ))}
        </div>
        <span style={{ fontSize:10.5, color:'#94A3B8' }}>
          2 varyasyon · sağ alttaki Tweaks panelinden de geçiş yapabilirsin
        </span>
      </div>

      {/* Görsel mod: harita + dağılım yan yana */}
      {view === 'gorsel' && (
        <div style={{ display:'grid', gridTemplateColumns:'1fr 340px', gap:16, alignItems:'start' }}>
          <MetrajCepheMap
            blocks={blocks}
            initialBlockId={selectedBinaId}
            floorsByBlock={floorsByBlock}
            projectName={santiyeAdi}
            onFloorSelect={(floor, binaId) => {
              setSelectedFloor(floor)
              setSelectedBinaId(binaId)
            }}
            onShow3D={onShow3D}
          />
          <IsKalemiDagilimi kalemler={selectedKalemler}/>
        </div>
      )}

      {/* İş kalemi tablosu (her iki modda görünür) */}
      <div style={{ background:'#fff', border:'1px solid #EEF0F3', borderRadius:12,
        boxShadow:'0 1px 2px rgba(15,23,42,.04)', overflow:'hidden' }}>
        <div style={{ padding:'12px 18px', borderBottom:'1px solid #EEF0F3',
          display:'flex', alignItems:'center', justifyContent:'space-between' }}>
          <div style={{ display:'flex', alignItems:'center', gap:6, fontSize:12, color:'#94A3B8' }}>
            {santiyeAdi && (
              <>
                <span style={{ color:'#475569', fontWeight:500 }}>{santiyeAdi}</span>
                <ChevronRight size={12}/>
              </>
            )}
            {selectedBinaId && hiyerarsi?.binalar && (
              <>
                <span style={{ color:'#475569', fontWeight:500 }}>
                  {hiyerarsi.binalar.find(b => String(b.id) === selectedBinaId)?.ad}
                </span>
                <ChevronRight size={12}/>
              </>
            )}
            {selectedFloor && (
              <span style={{ color:'#FF6B2C', fontWeight:600 }}>{selectedFloor.label}</span>
            )}
            {!selectedFloor && <span style={{ color:'#94A3B8' }}>Tüm katlar</span>}
          </div>
          <div style={{ fontSize:11, color:'#94A3B8' }}>
            {selectedKalemler.length} iş kalemi
          </div>
        </div>
        <IsKalemiTablosu kalemler={selectedKalemler} loading={false}/>
      </div>
    </div>
  )
}
