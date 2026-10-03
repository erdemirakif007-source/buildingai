import { useState, useEffect, useRef } from 'react'
import {
  CreditCard, ArrowUp, ArrowDown, AlertTriangle,
  Search, ChevronDown, RefreshCw,
} from 'lucide-react'

function MalzemeCombobox({ value, onChange, options, placeholder, className, inputClassName }) {
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState(value || '')
  const ref = useRef(null)

  useEffect(() => { setQuery(value || '') }, [value])

  useEffect(() => {
    const handler = e => { if (ref.current && !ref.current.contains(e.target)) setOpen(false) }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const filtered = query.trim().length === 0
    ? options.slice(0, 50)
    : options.filter(o => o.toLowerCase().includes(query.toLowerCase())).slice(0, 50)

  return (
    <div ref={ref} className={`relative ${className || ''}`}>
      <input
        type="text"
        placeholder={placeholder}
        value={query}
        onChange={e => { setQuery(e.target.value); onChange(e.target.value); setOpen(true) }}
        onFocus={() => setOpen(true)}
        className={inputClassName}
      />
      {open && filtered.length > 0 && (
        <ul className="absolute z-50 left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto text-[12px]">
          {filtered.map(opt => (
            <li
              key={opt}
              onMouseDown={e => { e.preventDefault(); onChange(opt); setQuery(opt); setOpen(false) }}
              className={`px-3 py-1.5 cursor-pointer hover:bg-orange-50 hover:text-orange-600 transition-colors ${
                opt === value ? 'bg-orange-50 text-orange-600 font-medium' : 'text-gray-700'
              }`}
            >
              {opt}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

function StatusBadge({ days, level }) {
  const cfg = {
    ok:       'bg-green-100 text-green-700',
    low:      'bg-orange-100 text-orange-600',
    critical: 'bg-red-100 text-red-600',
  }
  const label = days != null ? `${days} g` : '—'
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold ${cfg[level]}`}>
      • {label}
    </span>
  )
}

const BIRIMLER = ['torba', 'm³', 'adet', 'm²', 'kg', 'lt', 'ton', 'mt']

export default function StokYonetimi({ token }) {
  const [malzemeler, setMalzemeler]   = useState([])
  const [hareketler, setHareketler]   = useState([])
  const [loading, setLoading]         = useState(true)
  const [error, setError]             = useState(null)
  const [aramaMetni, setAramaMetni]   = useState('')
  const [filtre, setFiltre]           = useState('hepsi')
  const [aktifTab, setAktifTab]       = useState('giris')
  const [kayitMesaj, setKayitMesaj]   = useState({ type: '', text: '' })

  // Giriş form
  const [malzemeAdi, setMalzemeAdi]   = useState('')
  const [miktar, setMiktar]           = useState('')
  const [birim, setBirim]             = useState('torba')
  const [tedarikci, setTedarikci]     = useState('')
  const [birimFiyat, setBirimFiyat]   = useState('')
  const [irsaliye, setIrsaliye]       = useState('')
  const [notlar, setNotlar]           = useState('')

  // Sarf form
  const [sarfMalzeme, setSarfMalzeme] = useState('')
  const [sarfMiktar, setSarfMiktar]   = useState('')
  const [sarfYer, setSarfYer]         = useState('')
  const [sarfNot, setSarfNot]         = useState('')

  // Eşik form
  const [kritikAd, setKritikAd]       = useState('')
  const [kritikMin, setKritikMin]     = useState('')

  const authHeaders = { Authorization: `Bearer ${token}` }

  useEffect(() => { fetchData() }, [])

  async function fetchData() {
    setLoading(true)
    setError(null)
    try {
      const [stokRes, hareketRes] = await Promise.all([
        fetch('/stok', { headers: authHeaders }),
        fetch('/stok-hareketler?limit=20', { headers: authHeaders }),
      ])

      if (!stokRes.ok) {
        const txt = await stokRes.text()
        if (txt.includes('PLAN_YETERSIZ')) throw new Error('Stok takibi Profesyonel plan gerektirir.')
        throw new Error(`Sunucu hatası: ${stokRes.status}`)
      }

      const stokData   = await stokRes.json()
      const hareketData = hareketRes.ok ? await hareketRes.json() : { hareketler: [] }

      const list = []
      const processGroup = (stokDict, santiyeAdi) => {
        for (const [key, val] of Object.entries(stokDict)) {
          list.push({
            key,
            ad:          val.malzeme_ad || key,
            santiye_adi: santiyeAdi || '',
            stok:        val.mevcut,
            birim:       val.birim || '',
            birimFiyat:  val.son_fiyat || 0,
            deger:       val.stok_degeri_tl || 0,
            gun:         val.bitis_gun,
            min:         val.min_esik || 0,
            uyari_mesaj: val.uyari_mesaj || null,
            level:       val.uyari
              ? 'critical'
              : (val.bitis_gun != null && val.bitis_gun <= 3 ? 'low' : 'ok'),
          })
        }
      }

      if (stokData.gruplar && stokData.gruplar.length > 0) {
        for (const grup of stokData.gruplar) processGroup(grup.stok, grup.santiye_adi)
      } else if (stokData.stok) {
        processGroup(stokData.stok, stokData.santiye_adi)
      }

      setMalzemeler(list)
      setHareketler(hareketData.hareketler || [])
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  function showMsg(type, text) {
    setKayitMesaj({ type, text })
    setTimeout(() => setKayitMesaj({ type: '', text: '' }), 3500)
  }

  function parseTR(val) { return parseFloat(String(val ?? '').replace(',', '.')) }

  async function handleGirisKaydet() {
    if (!malzemeAdi.trim() || !miktar) { showMsg('err', 'Malzeme adı ve miktar zorunludur.'); return }
    const miktarNum = parseTR(miktar)
    if (isNaN(miktarNum) || miktarNum <= 0) { showMsg('err', 'Miktar sıfırdan büyük bir sayı olmalıdır.'); return }
    try {
      const res = await fetch('/stok-ekle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token,
          malzeme:    malzemeAdi.trim().toLowerCase().replace(/\s+/g, '_'),
          malzeme_ad: malzemeAdi.trim(),
          miktar:     miktarNum,
          birim,
          tip:        'giris',
          tedarikci,
          fiyat:      birimFiyat ? parseTR(birimFiyat) : null,
          notlar:     [irsaliye ? `İrs:${irsaliye}` : '', notlar].filter(Boolean).join(' | '),
        }),
      })
      if (!res.ok) throw new Error(await res.text())
      showMsg('ok', 'Stok girişi kaydedildi.')
      setMalzemeAdi(''); setMiktar(''); setTedarikci('')
      setBirimFiyat(''); setIrsaliye(''); setNotlar('')
      fetchData()
    } catch (e) { showMsg('err', e.message) }
  }

  async function handleSarfKaydet() {
    if (!sarfMalzeme.trim() || !sarfMiktar) { showMsg('err', 'Malzeme ve miktar zorunludur.'); return }
    const sarfNum = parseTR(sarfMiktar)
    if (isNaN(sarfNum) || sarfNum <= 0) { showMsg('err', 'Miktar sıfırdan büyük bir sayı olmalıdır.'); return }
    try {
      const res = await fetch('/stok-sarf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token,
          malzeme:    sarfMalzeme.trim().toLowerCase().replace(/\s+/g, '_'),
          malzeme_ad: sarfMalzeme.trim(),
          miktar:     sarfNum,
          notlar:     [sarfYer ? `Yer:${sarfYer}` : '', sarfNot].filter(Boolean).join(' | '),
        }),
      })
      if (!res.ok) {
        const body = await res.json().catch(() => null)
        throw new Error(body?.detail || 'Sarf kaydedilemedi.')
      }
      showMsg('ok', 'Sarf kaydı eklendi.')
      setSarfMalzeme(''); setSarfMiktar(''); setSarfYer(''); setSarfNot('')
      fetchData()
    } catch (e) { showMsg('err', e.message) }
  }

  async function handleEsikKaydet() {
    if (!kritikAd.trim() || !kritikMin) return
    const minNum = parseTR(kritikMin)
    if (isNaN(minNum) || minNum < 0) { showMsg('err', 'Minimum miktar geçerli bir sayı olmalıdır.'); return }
    try {
      const res = await fetch('/stok-esik-ayarla', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token,
          malzeme:    kritikAd.trim().toLowerCase().replace(/\s+/g, '_'),
          malzeme_ad: kritikAd.trim(),
          min_miktar: minNum,
        }),
      })
      if (!res.ok) throw new Error(await res.text())
      showMsg('ok', 'Eşik kaydedildi.')
      setKritikAd(''); setKritikMin('')
    } catch (e) { showMsg('err', e.message) }
  }

  // Summary stats
  const toplamDeger  = malzemeler.reduce((s, m) => s + m.deger, 0)
  const kritikSayi   = malzemeler.filter(m => m.level === 'critical').length
  const buHaftaGiris = hareketler.filter(h => h.tip === 'giris').reduce((s, h) => s + (h.miktar || 0), 0)
  const buHaftaCikis = hareketler.filter(h => h.tip === 'cikis').reduce((s, h) => s + (h.miktar || 0), 0)
  const formatPara   = n => Math.round(n).toLocaleString('tr-TR') + ' ₺'

  const filtreliMalzeme = malzemeler.filter(m => {
    const aramaOk = m.ad.toLowerCase().includes(aramaMetni.toLowerCase())
    if (filtre === 'kritik') return aramaOk && m.level === 'critical'
    if (filtre === 'dusuk')  return aramaOk && (m.level === 'low' || m.level === 'critical')
    return aramaOk
  })

  // Mevcut malzeme adları (sarf formundaki datalist için)
  const mevcut_adlar = malzemeler.map(m => m.ad)

  if (loading) return (
    <div className="flex flex-1 items-center justify-center bg-[#f5f6fa]">
      <p className="text-gray-400 text-sm">Stok verileri yükleniyor…</p>
    </div>
  )

  if (error) return (
    <div className="flex flex-1 items-center justify-center bg-[#f5f6fa]">
      <div className="bg-white rounded-xl border border-red-100 shadow-sm p-6 text-center max-w-sm">
        <AlertTriangle size={24} className="text-red-400 mx-auto mb-2" />
        <p className="text-red-500 font-semibold text-sm mb-1">Yükleme Hatası</p>
        <p className="text-gray-500 text-xs mb-3">{error}</p>
        <button onClick={fetchData} className="px-4 py-2 bg-orange-500 text-white text-xs font-semibold rounded-lg hover:bg-orange-600">
          Tekrar Dene
        </button>
      </div>
    </div>
  )

  return (
    <div className="flex flex-col flex-1 min-h-0 bg-[#f5f6fa] overflow-hidden">

      {/* ── Top stat cards ── */}
      <div className="grid grid-cols-4 gap-3 px-5 pt-4 pb-3 flex-shrink-0">

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm px-4 py-3">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-wide mb-1">Toplam Değer</p>
              <p className="text-[22px] font-bold text-gray-800 leading-tight">{formatPara(toplamDeger)}</p>
              <p className="text-[11px] text-gray-400 mt-0.5">{malzemeler.length} malzeme</p>
            </div>
            <div className="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center flex-shrink-0">
              <CreditCard size={16} className="text-blue-400" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm px-4 py-3">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-wide mb-1">Bu Dönem Giriş</p>
              <p className="text-[22px] font-bold text-green-600 leading-tight">+{Math.round(buHaftaGiris).toLocaleString('tr-TR')}</p>
              <p className="text-[11px] text-gray-400 mt-0.5">{hareketler.filter(h => h.tip === 'giris').length} hareket</p>
            </div>
            <div className="w-8 h-8 bg-green-50 rounded-lg flex items-center justify-center flex-shrink-0">
              <ArrowUp size={16} className="text-green-500" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm px-4 py-3">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-wide mb-1">Bu Dönem Çıkış</p>
              <p className="text-[22px] font-bold text-blue-500 leading-tight">-{Math.round(buHaftaCikis).toLocaleString('tr-TR')}</p>
              <p className="text-[11px] text-gray-400 mt-0.5">{hareketler.filter(h => h.tip === 'cikis').length} hareket</p>
            </div>
            <div className="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center flex-shrink-0">
              <ArrowDown size={16} className="text-blue-400" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl border border-red-100 shadow-sm px-4 py-3">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-wide mb-1">Kritik</p>
              <p className="text-[22px] font-bold text-red-500 leading-tight">{kritikSayi}/{malzemeler.length}</p>
              <p className="text-[11px] text-red-400 mt-0.5">
                {kritikSayi > 0
                  ? malzemeler.find(m => m.level === 'critical')?.ad || ''
                  : 'Kritik yok'}
              </p>
            </div>
            <div className="w-8 h-8 bg-red-50 rounded-lg flex items-center justify-center flex-shrink-0">
              <AlertTriangle size={16} className="text-red-400" />
            </div>
          </div>
        </div>
      </div>

      {/* ── Body: table + form ── */}
      <div className="flex flex-1 gap-3 px-5 pb-5 overflow-hidden min-h-0">

        {/* ── Left: table ── */}
        <div className="flex-1 bg-white rounded-xl border border-gray-100 shadow-sm flex flex-col min-w-0 overflow-hidden">

          {/* Toolbar */}
          <div className="flex-shrink-0 flex items-center gap-3 px-4 py-3 border-b border-gray-100">
            <div className="flex items-center gap-2 flex-1 bg-gray-50 border border-gray-200 rounded-lg px-3 py-1.5">
              <Search size={13} className="text-gray-400 flex-shrink-0" />
              <input
                type="text"
                placeholder="Malzeme ara..."
                value={aramaMetni}
                onChange={e => setAramaMetni(e.target.value)}
                className="flex-1 bg-transparent text-[12px] text-gray-700 placeholder-gray-400 outline-none"
              />
            </div>
            <div className="flex gap-1.5">
              {[['hepsi','Hepsi'],['dusuk','Düşük'],['kritik','Kritik']].map(([key,label]) => (
                <button
                  key={key}
                  onClick={() => setFiltre(key)}
                  className={`px-3 py-1.5 rounded-lg text-[11px] font-semibold transition-colors ${
                    filtre === key ? 'bg-orange-500 text-white' : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                  }`}
                >{label}</button>
              ))}
            </div>
            <button
              onClick={fetchData}
              className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              title="Yenile"
            >
              <RefreshCw size={13} />
            </button>
          </div>

          {/* Table */}
          <div style={{ height: 'calc(100% - 94px)', overflowY: 'auto' }}>
            {filtreliMalzeme.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-gray-400 gap-2">
                <p className="text-sm">Kayıt bulunamadı</p>
                <p className="text-xs">Malzeme girişi yaparak stok takibini başlatın.</p>
              </div>
            ) : (
              <table className="w-full text-[12px]">
                <thead className="sticky top-0 bg-gray-50 z-10">
                  <tr>
                    <th className="text-left px-4 py-2.5 text-[10px] font-semibold text-gray-400 uppercase tracking-wide">Malzeme</th>
                    <th className="text-right px-3 py-2.5 text-[10px] font-semibold text-gray-400 uppercase tracking-wide">Stok</th>
                    <th className="text-right px-3 py-2.5 text-[10px] font-semibold text-gray-400 uppercase tracking-wide">Min Eşik</th>
                    <th className="text-right px-3 py-2.5 text-[10px] font-semibold text-gray-400 uppercase tracking-wide">Birim Fiyat</th>
                    <th className="text-right px-3 py-2.5 text-[10px] font-semibold text-gray-400 uppercase tracking-wide">Değer</th>
                    <th className="text-center px-4 py-2.5 text-[10px] font-semibold text-gray-400 uppercase tracking-wide">Bitiş</th>
                  </tr>
                </thead>
                <tbody>
                  {filtreliMalzeme.map(m => (
                    <tr key={`${m.key}-${m.santiye_adi}`} className="border-t border-gray-50 hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-2.5">
                        <p className="font-semibold text-gray-800 text-[12px]">{m.ad}</p>
                        {m.santiye_adi && <p className="text-[10px] text-gray-400">{m.santiye_adi}</p>}
                        {m.uyari_mesaj && <p className="text-[10px] text-red-400 mt-0.5 truncate max-w-[180px]" title={m.uyari_mesaj}>{m.uyari_mesaj}</p>}
                      </td>
                      <td className="px-3 py-2.5 text-right">
                        <span className={`font-bold ${m.level === 'critical' ? 'text-red-500' : m.level === 'low' ? 'text-orange-500' : 'text-gray-800'}`}>
                          {m.stok.toLocaleString('tr-TR')}
                        </span>
                        {m.birim && <span className="text-gray-400 ml-1">{m.birim}</span>}
                      </td>
                      <td className="px-3 py-2.5 text-right text-gray-500">{m.min > 0 ? m.min.toLocaleString('tr-TR') : '—'}</td>
                      <td className="px-3 py-2.5 text-right text-gray-700 font-medium">
                        {m.birimFiyat > 0 ? m.birimFiyat.toLocaleString('tr-TR') + ' ₺' : '—'}
                      </td>
                      <td className="px-3 py-2.5 text-right font-semibold text-gray-800">
                        {m.deger > 0 ? formatPara(m.deger) : '—'}
                      </td>
                      <td className="px-4 py-2.5 text-center">
                        <StatusBadge days={m.gun} level={m.level} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            <div className="h-4" />
          </div>

          {/* Son Hareketler footer */}
          <div className="flex-shrink-0 border-t border-gray-100 px-4 py-2.5">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[12px] font-semibold text-gray-700">Son Hareketler</span>
              <span className="text-[11px] text-gray-400">{hareketler.length} kayıt</span>
            </div>
            {hareketler.length > 0 && (
              <div className="flex gap-2 overflow-x-auto pb-0.5">
                {hareketler.slice(0, 5).map(h => (
                  <div key={h.id} className="flex-shrink-0 bg-gray-50 rounded-lg px-2.5 py-1.5 min-w-[110px]">
                    <p className="text-[10px] font-semibold text-gray-700 truncate">{h.malzeme_ad || h.malzeme}</p>
                    <p className={`text-[11px] font-bold ${h.tip === 'giris' ? 'text-green-600' : 'text-blue-500'}`}>
                      {h.tip === 'giris' ? '+' : '-'}{h.miktar?.toLocaleString('tr-TR')}
                    </p>
                    <p className="text-[9px] text-gray-400">{h.created_at?.slice(5, 16)}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* ── Right: form panel ── */}
        <div className="w-[270px] flex-shrink-0 bg-white rounded-xl border border-gray-100 shadow-sm flex flex-col overflow-hidden">

          {/* Tabs */}
          <div className="flex border-b border-gray-100 flex-shrink-0">
            {[['giris','📦','Malzeme Girişi'],['sarf','⚡','Sarf Kaydı']].map(([tab,icon,label]) => (
              <button
                key={tab}
                onClick={() => { setAktifTab(tab); setKayitMesaj({ type: '', text: '' }) }}
                className={`flex-1 flex items-center justify-center gap-1.5 py-3 text-[12px] font-semibold transition-colors ${
                  aktifTab === tab ? 'bg-orange-500 text-white' : 'text-gray-500 hover:bg-gray-50'
                }`}
              >
                <span className="text-base leading-none">{icon}</span>
                {label}
              </button>
            ))}
          </div>

          {/* Feedback message */}
          {kayitMesaj.text && (
            <div className={`mx-4 mt-3 px-3 py-2 rounded-lg text-[11px] font-semibold ${
              kayitMesaj.type === 'ok' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-600'
            }`}>
              {kayitMesaj.text}
            </div>
          )}

          {/* Form content */}
          <div className="flex-1 overflow-y-auto min-h-0 px-4 py-3 space-y-3">

            {aktifTab === 'giris' ? (
              <>
                <div>
                  <label className="block text-[10px] font-semibold text-gray-500 uppercase tracking-wide mb-1">Malzeme</label>
                  <MalzemeCombobox
                    value={malzemeAdi}
                    onChange={setMalzemeAdi}
                    options={mevcut_adlar}
                    placeholder="Malzeme adı..."
                    className="w-full"
                    inputClassName="w-full border border-gray-200 rounded-lg px-3 py-2 text-[12px] text-gray-700 placeholder-gray-300 outline-none focus:border-orange-400 transition-colors"
                  />
                </div>

                <div>
                  <div className="flex gap-1.5 mb-1">
                    <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide flex-1">Miktar</label>
                    <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide w-20">Birim</label>
                  </div>
                  <div className="flex gap-1.5">
                    <input
                      type="number"
                      placeholder="0"
                      value={miktar}
                      onChange={e => setMiktar(e.target.value)}
                      className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-[12px] text-gray-700 placeholder-gray-300 outline-none focus:border-orange-400 transition-colors"
                    />
                    <div className="relative w-20">
                      <select
                        value={birim}
                        onChange={e => setBirim(e.target.value)}
                        className="w-full appearance-none border border-gray-200 rounded-lg px-2 py-2 text-[12px] text-gray-700 outline-none focus:border-orange-400 bg-white pr-6 transition-colors"
                      >
                        {BIRIMLER.map(b => <option key={b} value={b}>{b}</option>)}
                      </select>
                      <ChevronDown size={10} className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
                    </div>
                  </div>
                </div>

                <div>
                  <label className="block text-[10px] font-semibold text-gray-500 uppercase tracking-wide mb-1">Tedarikçi <span className="normal-case font-normal text-gray-400">(Opsiyonel)</span></label>
                  <input
                    type="text"
                    placeholder="Akçansa, Vitra..."
                    value={tedarikci}
                    onChange={e => setTedarikci(e.target.value)}
                    className="w-full border border-gray-200 rounded-lg px-3 py-2 text-[12px] text-gray-700 placeholder-gray-300 outline-none focus:border-orange-400 transition-colors"
                  />
                </div>

                <div>
                  <div className="flex gap-1.5 mb-1">
                    <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide flex-1">Birim Fiyat</label>
                    <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide w-24">İrsaliye No</label>
                  </div>
                  <div className="flex gap-1.5">
                    <div className="flex-1 flex items-center border border-gray-200 rounded-lg overflow-hidden focus-within:border-orange-400 transition-colors">
                      <input
                        type="number"
                        placeholder="0,00"
                        value={birimFiyat}
                        onChange={e => setBirimFiyat(e.target.value)}
                        className="flex-1 px-3 py-2 text-[12px] text-gray-700 placeholder-gray-300 outline-none bg-white"
                      />
                      <span className="px-2 text-[12px] text-gray-400 bg-gray-50 border-l border-gray-200 py-2">₺</span>
                    </div>
                    <input
                      type="text"
                      placeholder="—"
                      value={irsaliye}
                      onChange={e => setIrsaliye(e.target.value)}
                      className="w-24 border border-gray-200 rounded-lg px-3 py-2 text-[12px] text-gray-700 placeholder-gray-400 outline-none focus:border-orange-400 transition-colors"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-[10px] font-semibold text-gray-500 uppercase tracking-wide mb-1">Notlar <span className="normal-case font-normal text-gray-400">(Opsiyonel)</span></label>
                  <textarea
                    placeholder="Açıklama..."
                    value={notlar}
                    onChange={e => setNotlar(e.target.value)}
                    rows={3}
                    className="w-full border border-gray-200 rounded-lg px-3 py-2 text-[12px] text-gray-700 placeholder-gray-300 outline-none focus:border-orange-400 transition-colors resize-none"
                  />
                </div>

                <button
                  onClick={handleGirisKaydet}
                  className="w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold text-[12px] py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                  <span className="text-sm">✓</span> Stok Girişi Kaydet
                </button>
              </>
            ) : (
              <>
                <div>
                  <label className="block text-[10px] font-semibold text-gray-500 uppercase tracking-wide mb-1">Malzeme</label>
                  <MalzemeCombobox
                    value={sarfMalzeme}
                    onChange={setSarfMalzeme}
                    options={mevcut_adlar}
                    placeholder="Malzeme adı..."
                    className="w-full"
                    inputClassName="w-full border border-gray-200 rounded-lg px-3 py-2 text-[12px] text-gray-700 placeholder-gray-300 outline-none focus:border-orange-400 transition-colors"
                  />
                </div>
                <div>
                  <div className="flex gap-1.5 mb-1">
                    <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide flex-1">Miktar</label>
                    <label className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide w-20">Birim</label>
                  </div>
                  <div className="flex gap-1.5">
                    <input
                      type="number"
                      placeholder="0"
                      value={sarfMiktar}
                      onChange={e => setSarfMiktar(e.target.value)}
                      className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-[12px] text-gray-700 placeholder-gray-300 outline-none focus:border-orange-400 transition-colors"
                    />
                    <div className="relative w-20">
                      <select className="w-full appearance-none border border-gray-200 rounded-lg px-2 py-2 text-[12px] text-gray-700 outline-none focus:border-orange-400 bg-white pr-6 transition-colors">
                        {BIRIMLER.map(b => <option key={b}>{b}</option>)}
                      </select>
                      <ChevronDown size={10} className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
                    </div>
                  </div>
                </div>
                <div>
                  <label className="block text-[10px] font-semibold text-gray-500 uppercase tracking-wide mb-1">Kullanım Yeri</label>
                  <input
                    type="text"
                    placeholder="Blok A, Zemin Kat..."
                    value={sarfYer}
                    onChange={e => setSarfYer(e.target.value)}
                    className="w-full border border-gray-200 rounded-lg px-3 py-2 text-[12px] text-gray-700 placeholder-gray-300 outline-none focus:border-orange-400 transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-semibold text-gray-500 uppercase tracking-wide mb-1">Notlar <span className="normal-case font-normal text-gray-400">(Opsiyonel)</span></label>
                  <textarea
                    rows={3}
                    placeholder="Açıklama..."
                    value={sarfNot}
                    onChange={e => setSarfNot(e.target.value)}
                    className="w-full border border-gray-200 rounded-lg px-3 py-2 text-[12px] text-gray-700 placeholder-gray-300 outline-none focus:border-orange-400 transition-colors resize-none"
                  />
                </div>
                <button
                  onClick={handleSarfKaydet}
                  className="w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold text-[12px] py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                  <span className="text-sm">✓</span> Sarf Kaydı Kaydet
                </button>
              </>
            )}
          </div>

          {/* Kritik Stok Eşiği */}
          <div className="border-t border-gray-100 px-4 py-3 flex-shrink-0">
            <p className="text-[10px] font-semibold text-gray-500 uppercase tracking-wide mb-2">Kritik Stok Eşiği</p>
            <div className="flex gap-1.5 mb-1.5">
              <MalzemeCombobox
                value={kritikAd}
                onChange={setKritikAd}
                options={mevcut_adlar}
                placeholder="Malzeme adı..."
                className="flex-1"
                inputClassName="w-full border border-gray-200 rounded-lg px-2.5 py-1.5 text-[11px] text-gray-700 placeholder-gray-300 outline-none focus:border-orange-400 transition-colors"
              />
              <input
                type="number"
                placeholder="Min"
                value={kritikMin}
                onChange={e => setKritikMin(e.target.value)}
                className="w-14 border border-gray-200 rounded-lg px-2 py-1.5 text-[11px] text-gray-700 placeholder-gray-300 outline-none focus:border-orange-400 transition-colors"
              />
              <button
                onClick={handleEsikKaydet}
                className="px-2.5 py-1.5 bg-gray-800 text-white text-[11px] font-semibold rounded-lg hover:bg-gray-700 transition-colors flex-shrink-0"
              >
                Kaydet
              </button>
            </div>
            <p className="text-[10px] text-gray-400 leading-snug">
              Bu miktarın altına düştüğünde otomatik uyarı oluşturulur.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
