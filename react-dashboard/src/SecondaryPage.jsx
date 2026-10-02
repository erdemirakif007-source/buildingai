import { useEffect, useState } from 'react'

const urls = {
  saha: site => `/api/saha-kayitlari?santiye_id=${site.id}`,
  kamera: site => `/api/camera-analyses?santiye_id=${site.id}`,
  rapor: site => `/daily-reports?santiye_id=${site.id}`,
  stok: site => `/stok?santiye_id=${site.id}`,
  fiyat: () => '/fiyatlar',
}

async function read(path, token) {
  const response = await fetch(path, { headers: { Authorization: `Bearer ${token}` } })
  if (!response.ok) {
    let detail = `Veri yüklenemedi (${response.status}).`
    try { detail = (await response.json()).detail || detail } catch { /* non-JSON response */ }
    throw new Error(detail)
  }
  return response.json()
}

export default function SecondaryPage({ page, site, token }) {
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!site) return
    let cancelled = false
    setLoading(true)
    setError('')
    setResult(null)
    read(urls[page](site), token)
      .then(data => { if (!cancelled) setResult(data) })
      .catch(err => { if (!cancelled) setError(err.message) })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [page, site?.id, token])

  if (!site) return null
  if (loading) return <div className="ws-notice">Veriler yükleniyor…</div>
  if (error) return <div className="ws-notice ws-notice--error" role="alert">{error}</div>

  if (page === 'saha' || page === 'kamera') {
    const rows = page === 'saha' ? result.kayitlar : result.analyses
    return <section><h2>{site.ad} · {page === 'saha' ? 'Saha kayıtları' : 'Kamera analizleri'}</h2>
      {!rows.length && <div className="ws-notice">Bu şantiyede kayıt bulunamadı.</div>}
      <div className="ws-feed">{rows.map(row => <article className="ws-card" key={row.id}>
        {row.thumbnail_url && <img className="ws-feed-image" src={row.thumbnail_url} alt="Saha kaydı" loading="lazy" />}
        <div><strong>{row.title || 'Saha kaydı'}</strong><p>{row.description || row.zone_label || 'Açıklama yok'}</p><small>{row.verification_status || 'Taslak'} · {row.created_at}</small></div>
      </article>)}</div><p className="ws-helper">Yeni kayıt ve inceleme işlemleri için <a href="/app">mevcut saha aracını açın ↗</a></p>
    </section>
  }
  if (page === 'rapor') {
    const rows = result.raporlar || []
    return <section><h2>{site.ad} · Günlük raporlar</h2>
      {!rows.length && <div className="ws-notice">Bu şantiyede günlük rapor bulunamadı.</div>}
      <div className="ws-feed">{rows.map(row => <article className="ws-card" key={row.id}><strong>{row.report_date}</strong><p>{row.summary || 'Özet eklenmemiş'}</p><small>{row.verification_status} · {row.items?.length || 0} kayıt</small></article>)}</div>
      <p className="ws-helper">Rapor oluşturma ve düzenleme için <a href="/app">mevcut rapor aracını açın ↗</a></p>
    </section>
  }
  if (page === 'stok') {
    return <section><h2>{site.ad} · Stok</h2><div className="ws-site-grid">{Object.entries(result.stok || {}).map(([name, item]) => <div className="ws-card" key={name}><span>{name}</span><strong>{item.mevcut}</strong><small>{item.bitis_gun ? `Tahmini ${item.bitis_gun} gün` : 'Tüketim tahmini yok'}</small></div>)}</div>
      {!!result.uyarilar?.length && <div className="ws-notice ws-notice--error">{result.uyarilar.length} stok uyarısı var.</div>}
      <p className="ws-helper">Stok hareketi eklemek için <a href="/app">mevcut stok aracını açın ↗</a></p>
    </section>
  }
  return <section><h2>Malzeme fiyatları</h2><div className="ws-site-grid">{Object.entries(result.fiyatlar || {}).map(([name, item]) => <div className="ws-card" key={name}><span>{name}</span><strong>{item.fiyat == null ? 'Veri yok' : new Intl.NumberFormat('tr-TR').format(item.fiyat) + ' ₺'}</strong><small>{item.birim || 'Birim belirtilmedi'} · {item.tarih || 'Tarih yok'}</small></div>)}</div>
    <p className="ws-helper">Geçmiş ve ayrıntılı analiz için <a href="/app">mevcut fiyat aracını açın ↗</a></p>
  </section>
}
