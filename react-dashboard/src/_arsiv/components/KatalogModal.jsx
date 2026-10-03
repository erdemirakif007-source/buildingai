import { useState, useEffect } from 'react'
import { X, Search, ChevronDown, ChevronRight, Wrench, Layers, Plus } from 'lucide-react'

const trNorm = (s = '') =>
  s.toLowerCase()
    .replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ş/g, 's')
    .replace(/ı/g, 'i').replace(/ö/g, 'o').replace(/ç/g, 'c')

function useDebounce(value, delay) {
  const [deb, setDeb] = useState(value)
  useEffect(() => {
    const t = setTimeout(() => setDeb(value), delay)
    return () => clearTimeout(t)
  }, [value, delay])
  return deb
}

const BIRIM_SECENEKLERI = ['m²', 'm³', 'm', 'adet', 'ton', 'kg', 'lt', 'set']

export default function KatalogModal({ token, mahalId, santiyeId, onClose, onEklendi }) {
  const [mod, setMod] = useState('katalog')

  // Katalog modu state
  const [gruplar, setGruplar]             = useState([])
  const [secilenGrup, setSecilenGrup]     = useState(null)
  const [secilenAltGrup, setSecilenAltGrup] = useState(null)
  const [acikGruplar, setAcikGruplar]     = useState(new Set())
  const [isKalemleri, setIsKalemleri]     = useState([])
  const [secilenIk, setSecilenIk]         = useState(null)
  const [ikDetay, setIkDetay]             = useState(null)
  const [arama, setArama]                 = useState('')
  const [aramaResults, setAramaResults]   = useState(null)
  const [miktar, setMiktar]               = useState('')
  const [birimFiyat, setBirimFiyat]       = useState('')
  const [listLoading, setListLoading]     = useState(false)

  // Serbest giriş state
  const [sf, setSf] = useState({ tanim: '', birim: 'm²', poz_no: '', metraj: '', birim_fiyat_tl: '' })

  const [submitting, setSubmitting] = useState(false)
  const [hata, setHata]             = useState('')
  const debouncedArama              = useDebounce(arama, 300)

  const api = (path, opts = {}) =>
    fetch(path, {
      ...opts,
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...(opts.headers || {}),
      },
    }).then(r => r.json())

  // Grupları yükle
  useEffect(() => {
    api('/api/katalog/is-kalemi-gruplar').then(d => {
      const gs = d.gruplar || []
      setGruplar(gs)
      if (gs.length) {
        setSecilenGrup(gs[0].grup)
        setAcikGruplar(new Set([gs[0].grup]))
      }
    })
  }, [])

  // Grup değişince iş kalemlerini yükle
  useEffect(() => {
    if (!secilenGrup || aramaResults !== null) return
    setListLoading(true)
    const p = new URLSearchParams({ grup: secilenGrup })
    if (secilenAltGrup) p.set('alt_grup', secilenAltGrup)
    api(`/api/katalog/is-kalemleri?${p}`)
      .then(d => {
        setIsKalemleri(d.is_kalemleri || [])
        setSecilenIk(null)
        setIkDetay(null)
      })
      .finally(() => setListLoading(false))
  }, [secilenGrup, secilenAltGrup])

  // Arama debounce
  useEffect(() => {
    if (!debouncedArama.trim()) {
      setAramaResults(null)
      return
    }
    api(`/api/katalog/ara?q=${encodeURIComponent(debouncedArama)}&tip=is_kalemi`)
      .then(d => setAramaResults(d.sonuclar || []))
  }, [debouncedArama])

  // Seçilen iş kaleminin detayını yükle
  useEffect(() => {
    if (!secilenIk) { setIkDetay(null); return }
    api(`/api/katalog/is-kalemleri/${secilenIk.id}`).then(setIkDetay)
  }, [secilenIk?.id])

  const toggleGrup = (g) => {
    setSecilenGrup(g.grup)
    setSecilenAltGrup(null)
    setAcikGruplar(prev => {
      const next = new Set(prev)
      next.has(g.grup) ? next.delete(g.grup) : next.add(g.grup)
      return next
    })
  }

  const handleEkle = async () => {
    setHata('')
    setSubmitting(true)
    try {
      const url = mahalId
        ? `/api/v2/mahal/${mahalId}/is-kalemleri`
        : `/api/v2/santiye/${santiyeId}/is-kalemleri`

      let body
      if (mod === 'katalog') {
        if (!secilenIk || !miktar) { setHata('Miktar giriniz.'); return }
        body = {
          katalog_id: secilenIk.id,
          metraj: parseFloat(miktar),
          birim_fiyat_tl: birimFiyat ? parseFloat(birimFiyat) : 0,
        }
      } else {
        if (!sf.tanim.trim() || !sf.birim || !sf.metraj) {
          setHata('Ad, birim ve miktar zorunludur.')
          return
        }
        body = {
          tanim: sf.tanim.trim(),
          birim: sf.birim,
          poz_no: sf.poz_no || undefined,
          metraj: parseFloat(sf.metraj),
          birim_fiyat_tl: sf.birim_fiyat_tl ? parseFloat(sf.birim_fiyat_tl) : 0,
        }
      }

      const res = await api(url, { method: 'POST', body: JSON.stringify(body) })
      if (res.ok) {
        onEklendi?.(res.is_kalemi)
        onClose()
      } else {
        setHata(res.detail || 'Bir hata oluştu.')
      }
    } finally {
      setSubmitting(false)
    }
  }

  const displayList = aramaResults !== null ? aramaResults : isKalemleri
  const canEkle = mod === 'katalog'
    ? Boolean(secilenIk && miktar && parseFloat(miktar) > 0)
    : Boolean(sf.tanim.trim() && sf.birim && sf.metraj && parseFloat(sf.metraj) > 0)

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-2 sm:p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="
        relative w-full max-w-3xl flex flex-col
        bg-[#04070e] border border-white/[0.09]
        rounded-2xl shadow-2xl
        max-h-[90vh] sm:max-h-[85vh]
        overflow-hidden
      ">
        {/* ── Başlık ── */}
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-white/[0.07] flex-shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-6 h-6 rounded-lg bg-orange-500/10 border border-orange-500/20 flex items-center justify-center">
              <Layers size={12} className="text-orange-400" />
            </div>
            <h2 className="text-[13.5px] font-semibold text-gray-100">İş Kalemi Ekle</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-white/[0.06] text-gray-600 hover:text-gray-300 transition-colors"
          >
            <X size={14} />
          </button>
        </div>

        {/* ── Mod sekmeleri ── */}
        <div className="flex gap-0.5 px-5 pt-3 flex-shrink-0">
          {[['katalog', '📋 Katalogdan Seç'], ['serbest', '✏️ Serbest Giriş']].map(([m, label]) => (
            <button
              key={m}
              onClick={() => setMod(m)}
              className={`px-3.5 py-1.5 text-[11.5px] font-medium rounded-t-lg border-b-2 transition-all ${
                mod === m
                  ? 'border-orange-500 text-orange-400 bg-orange-500/[0.06]'
                  : 'border-transparent text-gray-600 hover:text-gray-400'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
        <div className="h-px bg-white/[0.06] mx-0" />

        {/* ── Gövde ── */}
        <div className="flex-1 overflow-hidden flex flex-col min-h-0">
          {mod === 'katalog' ? (
            <>
              {/* Arama */}
              <div className="px-5 py-3 flex-shrink-0">
                <div className="relative">
                  <Search size={13} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-600 pointer-events-none" />
                  <input
                    value={arama}
                    onChange={e => setArama(e.target.value)}
                    placeholder="Poz no veya iş kalemi adı ara… (ör: 16.003, C25/30, kalıp)"
                    className="w-full pl-9 pr-10 py-2.5 bg-[#080d1c] border border-white/[0.09] rounded-xl text-[11.5px] text-gray-200 placeholder-gray-600 focus:outline-none focus:border-orange-500/40 transition-colors"
                  />
                  {arama && (
                    <button
                      onClick={() => setArama('')}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-600 hover:text-gray-400 transition-colors"
                    >
                      <X size={12} />
                    </button>
                  )}
                </div>
              </div>

              {/* İki sütun */}
              <div className="flex flex-1 overflow-hidden min-h-0">
                {/* Sol: Grup ağacı */}
                {aramaResults === null && (
                  <div className="w-[172px] flex-shrink-0 overflow-y-auto border-r border-white/[0.06] py-1 px-1.5 space-y-0.5">
                    {gruplar.map(g => {
                      const expanded = acikGruplar.has(g.grup)
                      return (
                        <div key={g.grup}>
                          <button
                            onClick={() => toggleGrup(g)}
                            className={`w-full flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-[11px] font-medium transition-colors ${
                              secilenGrup === g.grup && !secilenAltGrup
                                ? 'bg-orange-500/[0.12] text-orange-300'
                                : 'text-gray-500 hover:text-gray-300 hover:bg-white/[0.04]'
                            }`}
                          >
                            {g.alt_gruplar?.length > 0 ? (
                              <ChevronDown
                                size={10}
                                className={`flex-shrink-0 transition-transform text-gray-600 ${expanded ? '' : '-rotate-90'}`}
                              />
                            ) : <span className="w-[10px] flex-shrink-0" />}
                            <span className="truncate flex-1 text-left">{g.grup}</span>
                            <span className="text-[9px] px-1 py-0.5 rounded bg-white/[0.05] text-gray-700 flex-shrink-0">
                              {g.is_kalemi_sayisi}
                            </span>
                          </button>

                          {expanded && g.alt_gruplar?.length > 0 && (
                            <div className="ml-3 mt-0.5 space-y-0.5">
                              {g.alt_gruplar.map(ag => (
                                <button
                                  key={ag}
                                  onClick={() => {
                                    setSecilenAltGrup(ag === secilenAltGrup ? null : ag)
                                    setSecilenGrup(g.grup)
                                  }}
                                  className={`w-full flex items-center gap-1.5 px-2 py-1 rounded-lg text-[10.5px] transition-colors ${
                                    secilenAltGrup === ag
                                      ? 'bg-orange-500/[0.08] text-orange-400'
                                      : 'text-gray-600 hover:text-gray-400 hover:bg-white/[0.03]'
                                  }`}
                                >
                                  <ChevronRight size={9} className="text-gray-700 flex-shrink-0" />
                                  <span className="truncate">{ag}</span>
                                </button>
                              ))}
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                )}

                {/* Sağ: İş kalemi listesi */}
                <div className="flex-1 overflow-y-auto px-3 py-1.5 space-y-0.5">
                  {listLoading ? (
                    <LoadingRows count={5} />
                  ) : displayList.length === 0 ? (
                    <EmptyState
                      icon={<Wrench size={22} className="text-gray-700" />}
                      text={arama ? 'Aramanızla eşleşen kayıt bulunamadı' : 'Bu grupta iş kalemi yok'}
                    />
                  ) : (
                    displayList.map(ik => (
                      <IsKalemiSatir
                        key={ik.id}
                        ik={ik}
                        selected={secilenIk?.id === ik.id}
                        detay={secilenIk?.id === ik.id ? ikDetay : null}
                        miktar={miktar}
                        birimFiyat={birimFiyat}
                        onSelect={() => {
                          if (secilenIk?.id === ik.id) {
                            setSecilenIk(null)
                          } else {
                            setSecilenIk(ik)
                            setMiktar('')
                            setBirimFiyat('')
                          }
                        }}
                        onMiktarChange={setMiktar}
                        onBirimFiyatChange={setBirimFiyat}
                      />
                    ))
                  )}
                </div>
              </div>
            </>
          ) : (
            /* ── Serbest giriş ── */
            <div className="px-5 py-4 space-y-3 overflow-y-auto">
              <div className="grid grid-cols-2 gap-3">
                <div className="col-span-2">
                  <Label>İş Kalemi Adı *</Label>
                  <input
                    value={sf.tanim}
                    onChange={e => setSf(p => ({ ...p, tanim: e.target.value }))}
                    placeholder="ör: Duvar boyası uygulaması"
                    className={inputCls}
                  />
                </div>
                <div>
                  <Label>Birim *</Label>
                  <div className="flex gap-1.5">
                    <input
                      value={sf.birim}
                      onChange={e => setSf(p => ({ ...p, birim: e.target.value }))}
                      placeholder="m², m³, adet…"
                      className={inputCls + ' flex-1'}
                    />
                    <div className="flex flex-wrap gap-1">
                      {BIRIM_SECENEKLERI.map(b => (
                        <button
                          key={b}
                          type="button"
                          onClick={() => setSf(p => ({ ...p, birim: b }))}
                          className={`text-[9.5px] px-1.5 py-1 rounded border transition-colors ${
                            sf.birim === b
                              ? 'border-orange-500/40 bg-orange-500/10 text-orange-400'
                              : 'border-white/[0.08] text-gray-600 hover:text-gray-400'
                          }`}
                        >
                          {b}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
                <div>
                  <Label>Poz No</Label>
                  <input
                    value={sf.poz_no}
                    onChange={e => setSf(p => ({ ...p, poz_no: e.target.value }))}
                    placeholder="ör: 16.003/1"
                    className={inputCls}
                  />
                </div>
                <div>
                  <Label>Miktar *</Label>
                  <input
                    type="number"
                    min="0"
                    value={sf.metraj}
                    onChange={e => setSf(p => ({ ...p, metraj: e.target.value }))}
                    placeholder="0"
                    className={inputCls}
                  />
                </div>
                <div>
                  <Label>Birim Fiyat (₺)</Label>
                  <input
                    type="number"
                    min="0"
                    value={sf.birim_fiyat_tl}
                    onChange={e => setSf(p => ({ ...p, birim_fiyat_tl: e.target.value }))}
                    placeholder="0"
                    className={inputCls}
                  />
                </div>
              </div>
              <p className="text-[10px] text-gray-700">
                💡 ÇŞB poz numarasıyla eşleştirmek için{' '}
                <button
                  onClick={() => setMod('katalog')}
                  className="text-orange-400/70 hover:text-orange-400 underline underline-offset-2"
                >
                  katalogdan seçin
                </button>
              </p>
            </div>
          )}
        </div>

        {/* ── Footer ── */}
        <div className="flex items-center justify-between px-5 py-3.5 border-t border-white/[0.07] flex-shrink-0 bg-[#030610]/60">
          <div>
            {hata && <p className="text-[10.5px] text-red-400">{hata}</p>}
          </div>
          <div className="flex items-center gap-2.5">
            <button
              onClick={onClose}
              className="px-4 py-2 text-[11.5px] text-gray-500 hover:text-gray-300 transition-colors"
            >
              İptal
            </button>
            <button
              onClick={handleEkle}
              disabled={submitting || !canEkle}
              className="flex items-center gap-1.5 px-4 py-2 bg-orange-600 hover:bg-orange-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-[11.5px] font-semibold rounded-xl transition-colors"
            >
              <Plus size={13} />
              {submitting ? 'Ekleniyor…' : 'İş Kalemi Ekle'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

/* ── İş kalemi satırı ── */
function IsKalemiSatir({ ik, selected, detay, miktar, birimFiyat, onSelect, onMiktarChange, onBirimFiyatChange }) {
  return (
    <div>
      <button
        onClick={onSelect}
        className={`w-full text-left px-3 py-2 rounded-xl border transition-all ${
          selected
            ? 'bg-orange-500/[0.10] border-orange-500/30'
            : 'bg-transparent border-transparent hover:bg-white/[0.03] hover:border-white/[0.06]'
        }`}
      >
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2 min-w-0">
            <span className="text-[9.5px] font-mono text-orange-400/60 flex-shrink-0 w-16 tabular-nums">{ik.poz_no}</span>
            <span className="text-[11.5px] text-gray-200 truncate">{ik.ad}</span>
          </div>
          <div className="flex items-center gap-1.5 flex-shrink-0">
            <span className="text-[9.5px] text-gray-600 bg-white/[0.05] px-1.5 py-0.5 rounded">{ik.birim}</span>
            <ChevronDown
              size={12}
              className={`text-gray-600 transition-transform ${selected ? 'rotate-180' : ''}`}
            />
          </div>
        </div>
      </button>

      {selected && (
        <div className="mx-1 mb-1.5 p-3 bg-[#080d1c] border border-white/[0.07] rounded-xl space-y-3">
          {/* Malzeme listesi */}
          {detay ? (
            detay.malzemeler?.length > 0 ? (
              <div>
                <p className="text-[9.5px] font-semibold text-gray-600 uppercase tracking-wider mb-1.5">
                  Bu iş kalemi şu malzemeleri gerektirir:
                </p>
                <div className="space-y-1">
                  {detay.malzemeler.map(m => (
                    <div key={m.malzeme_id} className="flex items-center justify-between gap-2 text-[10.5px]">
                      <div className="flex items-center gap-1.5 min-w-0">
                        <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${m.zorunlu ? 'bg-orange-400' : 'bg-gray-700'}`} />
                        <span className="text-[9.5px] font-mono text-gray-600">{m.poz_no}</span>
                        <span className="text-gray-400 truncate">{m.ad}</span>
                      </div>
                      <span className="text-gray-600 font-mono flex-shrink-0">{m.miktar} {m.birim}</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-[10.5px] text-gray-600 italic">Bu poz için malzeme tanımı yok.</p>
            )
          ) : (
            <div className="flex items-center gap-1.5 text-[10.5px] text-gray-600">
              <span className="animate-pulse">⏳</span> Malzemeler yükleniyor…
            </div>
          )}

          {/* Miktar & birim fiyat girişi */}
          <div className="pt-2.5 border-t border-white/[0.06] grid grid-cols-2 gap-2.5">
            <div>
              <Label>Miktar ({ik.birim}) *</Label>
              <input
                autoFocus
                type="number"
                min="0"
                value={miktar}
                onChange={e => onMiktarChange(e.target.value)}
                placeholder="0"
                className={inputCls}
              />
            </div>
            <div>
              <Label>Birim Fiyat (₺)</Label>
              <input
                type="number"
                min="0"
                value={birimFiyat}
                onChange={e => onBirimFiyatChange(e.target.value)}
                placeholder="0 — opsiyonel"
                className={inputCls}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

/* ── Yardımcı bileşenler ── */
const inputCls = 'w-full px-3 py-2 bg-[#040810] border border-white/[0.09] rounded-xl text-[11.5px] text-gray-200 placeholder-gray-600 focus:outline-none focus:border-orange-500/40 transition-colors'

function Label({ children }) {
  return <label className="block text-[10px] text-gray-600 mb-1">{children}</label>
}

function LoadingRows({ count = 4 }) {
  return (
    <div className="space-y-1 px-1 pt-1">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="h-8 rounded-xl bg-white/[0.03] animate-pulse"
          style={{ opacity: 1 - i * 0.18 }}
        />
      ))}
    </div>
  )
}

function EmptyState({ icon, text }) {
  return (
    <div className="flex flex-col items-center justify-center h-32 gap-2">
      {icon}
      <p className="text-[11px] text-gray-600">{text}</p>
    </div>
  )
}
