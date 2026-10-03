import { useEffect, useRef, useState } from 'react'
import { fetchListe, fetchDetay } from './api.js'
import { defaultPeriod } from './calc.js'
import { HakedisList } from './HakedisList.jsx'
import { HakedisDetail } from './HakedisDetail.jsx'
import { NewHakedisModal } from './NewHakedisModal.jsx'
import { Button } from '../../ui/Button.jsx'
import { EmptyState } from '../../ui/EmptyState.jsx'

function readHakedisParam() {
  return Number(new URLSearchParams(window.location.search).get('hakedis')) || null
}

export default function HakedisPage({ site, token, profile }) {
  const [hakedisler, setHakedisler]   = useState([])
  const [listLoading, setListLoading] = useState(false)
  const [listError, setListError]     = useState('')
  const [selectedId, setSelectedId]   = useState(readHakedisParam)
  const [detay, setDetay]             = useState(null)
  const [detayLoading, setDetayLoading] = useState(false)
  const [detayError, setDetayError]   = useState('')
  const [showNewModal, setShowNewModal] = useState(false)

  const abortRef = useRef(null)

  function abortPending() {
    if (abortRef.current) {
      abortRef.current.abort()
      abortRef.current = null
    }
  }

  function loadListe(siteId, signal) {
    setListLoading(true)
    setListError('')
    fetchListe(siteId, token, signal)
      .then(data => {
        setHakedisler(data.hakedisler)
      })
      .catch(err => {
        if (err.name === 'AbortError') return
        setListError(err.message)
      })
      .finally(() => { if (!signal.aborted) setListLoading(false) })
  }

  function loadDetay(id, signal) {
    if (!id) return
    setDetayLoading(true)
    setDetayError('')
    fetchDetay(id, token, signal)
      .then(data => {
        setDetay(data)
      })
      .catch(err => {
        if (err.name === 'AbortError') return
        setDetayError(err.message)
        setDetay(null)
      })
      .finally(() => { if (!signal.aborted) setDetayLoading(false) })
  }

  // Site değişince: listeyi yenile, seçimi sıfırla
  useEffect(() => {
    abortPending()
    const ac = new AbortController()
    abortRef.current = ac
    setSelectedId(null)
    setDetay(null)
    loadListe(site.id, ac.signal)
    return () => ac.abort()
  }, [site.id]) // eslint-disable-line react-hooks/exhaustive-deps

  // Seçili hakediş değişince: detayı yükle, URL güncelle
  useEffect(() => {
    if (!selectedId) return
    abortPending()
    const ac = new AbortController()
    abortRef.current = ac

    // URL güncelle
    const params = new URLSearchParams(window.location.search)
    params.set('hakedis', selectedId)
    window.history.pushState(null, '', `?${params}`)

    loadDetay(selectedId, ac.signal)
    return () => ac.abort()
  }, [selectedId]) // eslint-disable-line react-hooks/exhaustive-deps

  function openDetail(id) {
    setSelectedId(id)
  }

  function handleCreated(newId) {
    setShowNewModal(false)
    // Hem listeyi hem detayı taze çek
    const ac = new AbortController()
    abortRef.current = ac
    fetchListe(site.id, token, ac.signal)
      .then(data => {
        setHakedisler(data.hakedisler)
        setSelectedId(newId)
      })
      .catch(err => { if (err.name !== 'AbortError') setListError(err.message) })
  }

  function handleStatusChanged() {
    const ac = new AbortController()
    loadListe(site.id, ac.signal)
    if (selectedId) loadDetay(selectedId, ac.signal)
  }

  function handleKalemUpdated(partial) {
    // partial: {id, kumulatif_miktar, bu_donem_tutar, kumulatif_tutar, hakedis_toplam_tutar, bu_donem_miktar?}
    setDetay(prev => {
      if (!prev) return prev
      return {
        ...prev,
        hakedis: { ...prev.hakedis, toplam_tutar: partial.hakedis_toplam_tutar ?? prev.hakedis.toplam_tutar },
        kalemler: prev.kalemler.map(k =>
          k.id === partial.id ? { ...k, ...partial } : k
        ),
      }
    })
    // Arka planda tam detayı yenile (onceki/kumulatif sunucuda hesaplanıyor)
    const ac = new AbortController()
    fetchDetay(selectedId, token, ac.signal)
      .then(data => setDetay(data))
      .catch(err => { if (err.name !== 'AbortError') {} })
  }

  // defaultPeriod için son onaylı hakedişin bitis tarihini bul
  const lastApproved = hakedisler.filter(h => h.durum === 'onaylandi').sort((a, b) => b.hakedis_no - a.hakedis_no)[0]
  const period = defaultPeriod(lastApproved?.donem_bitis)

  // Masaüstü: yan yana. Mobil: liste veya detay.
  const showBackButton = selectedId !== null

  return (
    <div className="flex flex-col gap-4">
      {listError && (
        <div role="alert" className="text-sm text-danger-fg bg-danger-bg border border-danger-border rounded px-4 py-3">
          {listError} <button className="underline ml-2" onClick={() => loadListe(site.id, new AbortController().signal)}>Tekrar dene</button>
        </div>
      )}

      {/* Mobil: detay görünümündeyken "Listeye dön" */}
      {showBackButton && (
        <div className="md:hidden">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              setSelectedId(null)
              const params = new URLSearchParams(window.location.search)
              params.delete('hakedis')
              window.history.pushState(null, '', `?${params}`)
            }}
          >
            ← Listeye dön
          </Button>
        </div>
      )}

      <div className="flex flex-col md:flex-row gap-6">
        {/* Liste — mobilde detay açıkken gizle */}
        <div className={`md:w-72 md:flex-none ${selectedId ? 'hidden md:block' : 'block'}`}>
          <HakedisList
            items={hakedisler}
            loading={listLoading}
            selectedId={selectedId}
            onSelect={openDetail}
            onNewClick={() => setShowNewModal(true)}
          />
        </div>

        {/* Detay — mobilde liste görünümündeyken gizle */}
        <div className={`flex-1 min-w-0 ${selectedId ? 'block' : 'hidden md:block'}`}>
          {selectedId ? (
            <HakedisDetail
              hakedis={detay?.hakedis ?? null}
              kalemler={detay?.kalemler ?? []}
              loading={detayLoading}
              error={detayError}
              token={token}
              profile={profile}
              onStatusChanged={handleStatusChanged}
              onKalemUpdated={handleKalemUpdated}
              onRetry={() => loadDetay(selectedId, new AbortController().signal)}
            />
          ) : (
            <div className="hidden md:flex items-center justify-center h-48 text-text-muted text-sm">
              Detay görmek için listeden bir hakediş seçin.
            </div>
          )}
        </div>
      </div>

      <NewHakedisModal
        open={showNewModal}
        onClose={() => setShowNewModal(false)}
        siteId={site.id}
        token={token}
        defaultStart={period.start}
        defaultEnd={period.end}
        onCreated={handleCreated}
      />
    </div>
  )
}
