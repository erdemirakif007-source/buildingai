import { useCallback, useEffect, useState } from 'react'
import { Building2, ClipboardList, Cuboid, FileText, Home, LogOut, Menu, X } from 'lucide-react'
import SecondaryPage from './SecondaryPage'
import './workspace.css'

const PAGES = ['portfolio', 'site', 'metraj', 'bim', 'hakedis', 'saha', 'kamera', 'rapor', 'stok', 'fiyat']
const LEGACY_PAGES = new Set(['metraj', 'hakedis', 'stok', 'fiyat'])
const LEGACY_MODULE = { metraj: 'hiyerarsi', hakedis: 'hakedis', stok: 'stok', fiyat: 'fiyat' }
const NAV = [
  ['portfolio', 'Portföy', Home],
  ['site', 'Şantiye', Building2],
  ['metraj', 'Metraj', ClipboardList],
  ['bim', 'BIM', Cuboid],
  ['hakedis', 'Hakediş', FileText],
  ['saha', 'Saha Kayıtları', ClipboardList],
  ['kamera', 'Kamera', Cuboid],
  ['rapor', 'Raporlar', FileText],
  ['stok', 'Stok', Building2],
  ['fiyat', 'Fiyatlar', FileText],
]
const money = value => new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY', maximumFractionDigits: 0 }).format(Number(value) || 0)

function readLocation() {
  const params = new URLSearchParams(window.location.search)
  const page = params.get('page')
  const siteId = Number(params.get('site')) || null
  return { page: PAGES.includes(page) ? page : 'portfolio', siteId }
}

async function api(path, token) {
  const response = await fetch(path, { headers: { Authorization: `Bearer ${token}` } })
  if (!response.ok) {
    let detail = `İstek başarısız (${response.status})`
    try { detail = (await response.json()).detail || detail } catch { /* response may not be JSON */ }
    throw new Error(detail)
  }
  return response.json()
}

function Notice({ children, kind = 'info' }) {
  return <div className={`ws-notice ws-notice--${kind}`} role={kind === 'error' ? 'alert' : undefined}>{children}</div>
}

function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function submit(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    try {
      const response = await fetch('/login', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      const data = await response.json()
      if (!response.ok || !data.token) throw new Error(data.detail || 'Giriş yapılamadı.')
      localStorage.setItem('bai_token', data.token)
      onLogin(data.token)
    } catch (err) { setError(err.message) }
    finally { setBusy(false) }
  }

  return <main className="ws-login">
    <div className="ws-login-card">
      <img src="/static/buildingai-logo.svg" alt="" width="48" height="48" />
      <h1>BuildingAI</h1>
      <p>Şantiyelerinizin tek görünümü</p>
      <form onSubmit={submit}>
        <label>E-posta<input type="email" autoComplete="username" value={email} onChange={event => setEmail(event.target.value)} required /></label>
        <label>Şifre<input type="password" autoComplete="current-password" value={password} onChange={event => setPassword(event.target.value)} required /></label>
        {error && <Notice kind="error">{error}</Notice>}
        <button className="ws-primary" type="submit" disabled={busy}>{busy ? 'Giriş yapılıyor…' : 'Giriş yap'}</button>
      </form>
      <a href="/app">Google ile giriş ve hesap oluşturma</a>
    </div>
  </main>
}

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem('bai_token') || '')
  const [location, setLocation] = useState(readLocation)
  const [profile, setProfile] = useState(null)
  const [sites, setSites] = useState([])
  const [dashboard, setDashboard] = useState(null)
  const [data, setData] = useState({})
  const [selectedPayment, setSelectedPayment] = useState(null)
  const [selectedModelId, setSelectedModelId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [menuOpen, setMenuOpen] = useState(false)
  const site = sites.find(item => item.id === location.siteId) || null

  const navigate = useCallback((page, siteId = location.siteId) => {
    const resolvedSiteId = page !== 'portfolio' && !siteId && sites.length === 1 ? sites[0].id : siteId
    const next = { page, siteId: resolvedSiteId }
    const params = new URLSearchParams()
    params.set('page', page)
    if (resolvedSiteId) params.set('site', String(resolvedSiteId))
    window.history.pushState(next, '', `/workspace?${params}`)
    setLocation(next)
    setSelectedPayment(null)
    setSelectedModelId(null)
    setMenuOpen(false)
  }, [location.siteId, sites])

  useEffect(() => {
    const pop = () => { setLocation(readLocation()); setSelectedPayment(null) }
    window.addEventListener('popstate', pop)
    return () => window.removeEventListener('popstate', pop)
  }, [])

  useEffect(() => {
    if (!token) return
    let cancelled = false
    setLoading(true)
    setError('')
    Promise.all([api('/beni-tanı', token), api('/santiyeler', token), api('/api/dashboard/contractor', token)])
      .then(([user, siteResult, dashboardResult]) => {
        if (cancelled) return
        setProfile(user)
        setSites(siteResult.santiyeler || [])
        setDashboard(dashboardResult)
      })
      .catch(err => {
        if (cancelled) return
        if (/Token geçersiz|401/.test(err.message)) { localStorage.removeItem('bai_token'); setToken('') }
        else setError(err.message)
      })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [token])

  useEffect(() => {
    if (!token || !site || location.page === 'portfolio' || LEGACY_PAGES.has(location.page)) return
    let cancelled = false
    const id = site.id
    setData({})
    setSelectedModelId(null)
    setLoading(true)
    setError('')
    Promise.allSettled([
      api(`/api/v2/santiye/${id}/hiyerarsi`, token),
      api(`/api/metraj/ozet/${id}`, token),
      api(`/api/hakedis/liste/${id}`, token),
      api(`/api/bim/models?santiye_id=${id}`, token),
    ]).then(results => {
      if (cancelled) return
      const failures = results.filter(result => result.status === 'rejected')
      setData({
        hierarchy: results[0].status === 'fulfilled' ? results[0].value : null,
        metraj: results[1].status === 'fulfilled' ? results[1].value : null,
        payments: results[2].status === 'fulfilled' ? results[2].value.hakedisler : null,
        models: results[3].status === 'fulfilled' ? results[3].value.modeller : null,
      })
      if (failures.length) setError(`${failures.length} veri kaynağı yüklenemedi: ${failures[0].reason.message}`)
    }).finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [token, site?.id, location.page === 'portfolio'])

  async function logout() {
    await fetch("/logout", { method: "POST" })
    localStorage.removeItem('bai_token')
    localStorage.removeItem('bai_rol')
    setToken('')
    setProfile(null)
    setSites([])
  }

  async function openPayment(payment) {
    setSelectedPayment({ loading: true })
    try { setSelectedPayment(await api(`/api/hakedis/detay/${payment.id}`, token)) }
    catch (err) { setSelectedPayment({ error: err.message }) }
  }

  if (!token) return <Login onLogin={setToken} />

  return <div className="ws-app">
    <header className="ws-header">
      <button className="ws-menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-label="Menüyü aç">{menuOpen ? <X /> : <Menu />}</button>
      <a className="ws-brand" href="/workspace">Building<span>AI</span></a>
      <span className="ws-header-role">{profile?.full_name || profile?.email || 'Hesap'} · {profile?.role || 'Kullanıcı'}</span>
      <button className="ws-logout" onClick={logout}><LogOut size={16} /> Çıkış</button>
    </header>
    <div className="ws-body">
      <nav className={`ws-nav ${menuOpen ? 'ws-nav--open' : ''}`} aria-label="Ana gezinme">
        {NAV.map(([page, label, Icon]) => <button key={page} className={location.page === page ? 'active' : ''}
          onClick={() => navigate(page, page === 'portfolio' ? null : location.siteId)}><Icon size={18} />{label}</button>)}
        <div className="ws-nav-footer"><a href="/app">Diğer araçlar ve eski arayüz ↗</a></div>
      </nav>
      <main className="ws-main">
        <div className="ws-topline">
          <div><span className="ws-eyebrow">BUILDINGAI ÇALIŞMA ALANI</span><h1>{NAV.find(item => item[0] === location.page)?.[1]}</h1></div>
          <select aria-label="Aktif şantiye" value={site?.id || ''} onChange={event => navigate(event.target.value ? 'site' : 'portfolio', Number(event.target.value) || null)}>
            <option value="">Tüm şantiyeler</option>
            {sites.map(item => <option key={item.id} value={item.id}>{item.ad}</option>)}
          </select>
        </div>
        {error && <Notice kind="error">{error}</Notice>}
        {loading && <Notice>Veriler yükleniyor…</Notice>}
        {!loading && location.page !== 'portfolio' && !site && <Notice>Devam etmek için bir şantiye seçin.</Notice>}
        {location.page === 'portfolio' && <section>
          <div className="ws-kpis">{(dashboard?.kpis || []).map(kpi => <div className="ws-card" key={kpi.id}><span>{kpi.label}</span><strong>{kpi.value}</strong><small>{kpi.context}</small></div>)}</div>
          <h2>Şantiyeler</h2>
          {!loading && !sites.length && <Notice>Aktif şantiye bulunamadı.</Notice>}
          <div className="ws-site-grid">{sites.map(item => <button className="ws-site-card" key={item.id} onClick={() => navigate('site', item.id)}>
            <strong>{item.ad}</strong><span>{item.konum || 'Konum belirtilmedi'}</span><div className="ws-progress"><i style={{ width: `${Math.min(100, Math.max(0, item.ilerleme || 0))}%` }} /></div><small>%{item.ilerleme || 0} ilerleme · {item.isci_sayisi || 0} çalışan</small>
          </button>)}</div>
          <h2>Son onaylanan saha kayıtları</h2>
          <div className="ws-list">{(dashboard?.today_approved_feed || []).slice(0, 8).map(item => <div className="ws-list-row" key={item.id}><strong>{item.title}</strong><span>{sites.find(siteItem => siteItem.id === item.santiye_id)?.ad || 'Şantiye'}</span><small>{item.reviewed_at}</small></div>)}</div>
        </section>}
        {site && location.page === 'site' && <section>
          <div className="ws-hero"><span>AKTİF ŞANTİYE</span><h2>{site.ad}</h2><p>{site.konum || 'Konum belirtilmedi'}</p><div className="ws-progress"><i style={{ width: `${Math.min(100, Math.max(0, site.ilerleme || 0))}%` }} /></div><small>%{site.ilerleme || 0} ilerleme · {site.isci_sayisi || 0} çalışan · İSG: {site.isg_durumu || 'Bilinmiyor'}</small></div>
          <div className="ws-kpis"><div className="ws-card"><span>İş kalemi</span><strong>{data.metraj?.toplam_kalem ?? '—'}</strong></div><div className="ws-card"><span>Toplam metraj tutarı</span><strong>{data.metraj ? money(data.metraj.toplam_tutar) : '—'}</strong></div><div className="ws-card"><span>BIM modeli</span><strong>{data.models?.length ?? '—'}</strong></div><div className="ws-card"><span>Hakediş dönemi</span><strong>{data.payments?.length ?? '—'}</strong></div></div>
          <div className="ws-actions"><button onClick={() => navigate('metraj')}>Metrajı incele</button><button onClick={() => navigate('bim')}>BIM modelini aç</button><button onClick={() => navigate('hakedis')}>Hakedişleri incele</button></div>
        </section>}
        {site && LEGACY_PAGES.has(location.page) && <section className="ws-legacy-section">
          <div className="ws-section-head"><div><span className="ws-eyebrow">ALIŞTIĞINIZ ÇALIŞMA DÜZENİ</span><h2>{site.ad} · {NAV.find(item => item[0] === location.page)?.[1]}</h2></div><a className="ws-open-full" href={`/app?workspace_module=${LEGACY_MODULE[location.page]}&site=${site.id}`} target="_blank" rel="noopener noreferrer">Tam ekranda aç ↗</a></div>
          <iframe key={`${location.page}-${site.id}`} className="ws-legacy-frame" title={`${site.ad} ${location.page} çalışma ekranı`} src={`/app?workspace_module=${LEGACY_MODULE[location.page]}&site=${site.id}`} />
        </section>}
        {site && location.page === 'metraj-old' && <section>
          <div className="ws-section-head"><h2>{site.ad} · Metraj</h2><button onClick={() => navigate('bim')}>3D BIM ↗</button></div>
          {data.metraj && <div className="ws-kpis"><div className="ws-card"><span>Toplam kalem</span><strong>{data.metraj.toplam_kalem}</strong></div><div className="ws-card"><span>Tamamlanan</span><strong>{data.metraj.tamamlanan}</strong></div><div className="ws-card"><span>Devam eden</span><strong>{data.metraj.devam_eden}</strong></div><div className="ws-card"><span>Toplam tutar</span><strong>{money(data.metraj.toplam_tutar)}</strong></div></div>}
          {!loading && !data.hierarchy?.binalar?.length && <Notice>Bu şantiyede henüz yapı hiyerarşisi bulunmuyor.</Notice>}
          {(data.hierarchy?.binalar || []).map(bina => <div className="ws-card ws-building" key={bina.id}><h3>{bina.ad}</h3>{(bina.katlar || []).map(kat => <details key={kat.id}><summary>{kat.etiket || `Kat ${kat.kat_no}`}</summary>{(kat.mahaller || []).map(mahal => <div className="ws-mahal" key={mahal.id}><strong>{mahal.ad}</strong>{(mahal.is_kalemleri || []).map(kalem => <div className="ws-list-row" key={kalem.id}><span>{kalem.tanim}</span><span>{kalem.metraj} {kalem.birim}</span><strong>{money(kalem.toplam_fiyat_tl)}</strong></div>)}</div>)}</details>)}</div>)}
        </section>}
        {site && location.page === 'bim' && <section>
          <div className="ws-section-head"><h2>{site.ad} · BIM</h2><button onClick={() => navigate('metraj')}>Metraja dön</button></div>
          {!loading && !data.models?.length && <Notice>Bu şantiyeye bağlı BIM modeli yok. Model yükleme için mevcut metraj aracını açabilirsiniz: <a href="/app">Metraj aracı ↗</a></Notice>}
          {!!data.models?.length && <><div className="ws-model-list">{data.models.map(model => <button className={(selectedModelId || data.models[0].id) === model.id ? 'active' : ''} onClick={() => setSelectedModelId(model.id)} key={model.id}>{model.orijinal_dosya_adi || `Model ${model.id}`}</button>)}</div><iframe className="ws-bim-frame" title={`${site.ad} BIM modeli`} src={`/bim-viewer/?model_id=${selectedModelId || data.models[0].id}&santiye_id=${site.id}`} /></>}
        </section>}
        {site && location.page === 'hakedis-old' && <section>
          <h2>{site.ad} · Hakedişler</h2>
          {!loading && !data.payments?.length && <Notice>Bu şantiyede henüz hakediş dönemi yok.</Notice>}
          <div className="ws-payment-layout"><div className="ws-list">{(data.payments || []).map(payment => <button className="ws-payment" key={payment.id} onClick={() => openPayment(payment)}><strong>Hakediş #{payment.hakedis_no}</strong><small>{payment.donem_baslangic} – {payment.donem_bitis}</small><span>{money(payment.toplam_tutar)} · {payment.durum}</span></button>)}</div>
          <div className="ws-card ws-payment-detail">{selectedPayment?.loading ? 'Detay yükleniyor…' : selectedPayment?.error ? <Notice kind="error">{selectedPayment.error}</Notice> : selectedPayment?.hakedis ? <><h3>Hakediş #{selectedPayment.hakedis.hakedis_no}</h3><p>{selectedPayment.hakedis.durum} · {money(selectedPayment.hakedis.toplam_tutar)}</p><div className="ws-table-wrap"><table><thead><tr><th>İş kalemi</th><th>Bu dönem</th><th>Tutar</th></tr></thead><tbody>{selectedPayment.kalemler.map(kalem => <tr key={kalem.id}><td>{kalem.tanim}</td><td>{kalem.bu_donem_miktar} {kalem.birim}</td><td>{money(kalem.bu_donem_tutar)}</td></tr>)}</tbody></table></div></> : 'Dönem ayrıntısı için bir hakediş seçin.'}</div></div>
        </section>}
        {site && ['saha', 'kamera', 'rapor'].includes(location.page) && <SecondaryPage page={location.page} site={site} token={token} />}
      </main>
    </div>
  </div>
}
