import { useEffect, useRef, useState } from 'react'
import { fetchCaps, fetchDecisions, fetchAllocations, updateDurum, cancelHakedis, downloadPdf } from './api.js'
import { getMeta, allowedActions } from './status.js'
import { computeSummary } from './calc.js'
import { Badge } from '../../ui/Badge.jsx'
import { Button } from '../../ui/Button.jsx'
import { Card } from '../../ui/Card.jsx'
import { EmptyState } from '../../ui/EmptyState.jsx'
import { Field } from '../../ui/Field.jsx'
import { Modal } from '../../ui/Modal.jsx'
import { Spinner } from '../../ui/Spinner.jsx'
import { Tabs } from '../../ui/Tabs.jsx'
import { Textarea } from '../../ui/Field.jsx'
import { useToast } from '../../ui/Toast.jsx'
import { formatMoney, formatDate } from '../../ui/format.js'
import { KalemTable } from './KalemTable.jsx'
import { KalemCards } from './KalemCards.jsx'
import { DecisionTimeline } from './DecisionTimeline.jsx'
import { AllocationsTable } from './AllocationsTable.jsx'

export function HakedisDetail({ hakedis, kalemler, loading, error, token, profile, onStatusChanged, onKalemUpdated, onRetry }) {
  const [caps, setCaps]             = useState(null)
  const [capsLoading, setCapsLoading] = useState(false)
  const [decisions, setDecisions]   = useState([])
  const [allocations, setAllocations] = useState([])
  const [actionBusy, setActionBusy] = useState(false)
  const [rejectOpen, setRejectOpen] = useState(false)
  const [rejectReason, setRejectReason] = useState('')
  const [rejectError, setRejectError] = useState('')
  const [cancelOpen, setCancelOpen] = useState(false)
  const toast = useToast()
  const abortRef = useRef(null)

  useEffect(() => {
    if (!hakedis?.id) { setCaps(null); setDecisions([]); setAllocations([]); return }
    if (abortRef.current) abortRef.current.abort()
    const ac = new AbortController()
    abortRef.current = ac

    setCapsLoading(true)
    setCaps(null)
    setDecisions([])
    setAllocations([])

    Promise.all([
      fetchCaps(hakedis.id, token, ac.signal),
      fetchDecisions(hakedis.id, token, ac.signal),
    ]).then(([capsData, decData]) => {
      if (ac.signal.aborted) return
      setCaps(capsData)
      setDecisions(decData.decisions)
      if (capsData.contract_id) {
        fetchAllocations(hakedis.id, token, ac.signal)
          .then(a => { if (!ac.signal.aborted) setAllocations(a.allocations) })
          .catch(err => { if (err.name !== 'AbortError') {} })
      }
    }).catch(err => {
      if (err.name === 'AbortError') return
      // caps hatasında caps=null kalır → kalemler salt okunur gösterilir
    }).finally(() => { if (!ac.signal.aborted) setCapsLoading(false) })

    return () => ac.abort()
  }, [hakedis?.id, hakedis?.durum]) // eslint-disable-line react-hooks/exhaustive-deps

  async function doTransition(body, successMsg) {
    setActionBusy(true)
    try {
      await updateDurum(hakedis.id, body, token)
      toast({ message: successMsg, tone: 'success' })
      onStatusChanged()
    } catch (err) {
      toast({ message: err.message, tone: 'danger' })
    } finally {
      setActionBusy(false)
    }
  }

  async function handleRejectConfirm() {
    if (!rejectReason.trim()) { setRejectError('Gerekçe giriniz.'); return }
    setRejectOpen(false)
    await doTransition({ durum: 'reddedildi', reason: rejectReason.trim() }, 'Hakediş geri gönderildi.')
    setRejectReason('')
    setRejectError('')
  }

  async function handleCancel() {
    setCancelOpen(false)
    setActionBusy(true)
    try {
      await cancelHakedis(hakedis.id, token)
      toast({ message: 'Hakediş iptal edildi.', tone: 'success' })
      onStatusChanged()
    } catch (err) {
      toast({ message: err.message, tone: 'danger' })
    } finally {
      setActionBusy(false)
    }
  }

  async function handleDownload() {
    try {
      const blob = await downloadPdf(hakedis.id, token)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `hakedis-${hakedis.hakedis_no}.pdf`
      a.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      toast({ message: err.message, tone: 'danger' })
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-16">
        <Spinner size="lg" />
      </div>
    )
  }

  if (error) {
    return (
      <EmptyState
        title="Hakediş yüklenemedi"
        description={error}
        action={<Button variant="secondary" size="sm" onClick={onRetry}>Tekrar dene</Button>}
      />
    )
  }

  if (!hakedis) return null

  const meta    = getMeta(hakedis.durum)
  const actions = allowedActions(hakedis.durum, caps)
  const summary = computeSummary(hakedis, kalemler)
  const isSelfApprover = profile && hakedis.hazirlayan_id && profile.id === hakedis.hazirlayan_id

  const tabs = [
    {
      key: 'kalemler',
      label: 'İş kalemleri',
      content: (
        <>
          <div className="hidden md:block">
            <KalemTable
              kalemler={kalemler}
              loading={false}
              durum={hakedis.durum}
              caps={caps}
              capsLoading={capsLoading}
              token={token}
              onKalemUpdated={onKalemUpdated}
            />
          </div>
          <div className="block md:hidden">
            {hakedis.durum === 'taslak' && !caps?.contract_id && (
              <div role="note" className="text-sm text-text-muted bg-surface-muted border border-border rounded px-4 py-3 mb-3">
                Miktar düzenleme masaüstünden yapılır.
              </div>
            )}
            <KalemCards kalemler={kalemler} loading={false} />
          </div>
        </>
      ),
    },
    {
      key: 'tarihce',
      label: 'Onay geçmişi',
      content: <DecisionTimeline decisions={decisions} loading={capsLoading} />,
    },
    ...(caps?.contract_id ? [{
      key: 'tahsisler',
      label: 'Tahsisler',
      content: <AllocationsTable allocations={allocations} loading={capsLoading} />,
    }] : []),
  ]

  return (
    <div className="flex flex-col gap-4">
      {/* Başlık */}
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h2 className="text-xl font-bold text-text">Hakediş No. {hakedis.hakedis_no}</h2>
            <Badge tone={meta.tone} dot>{meta.label}</Badge>
          </div>
          <p className="text-sm text-text-muted mt-1">
            {formatDate(hakedis.donem_baslangic)} – {formatDate(hakedis.donem_bitis)}
          </p>
          <p className="text-sm text-text-muted">
            Hazırlayan: {hakedis.hazirlayan_ad || 'Belirtilmedi'}
            {hakedis.onaylayan_ad && ` · Onaylayan: ${hakedis.onaylayan_ad}`}
          </p>
        </div>

        {/* Aksiyon butonları */}
        <div className="flex flex-wrap gap-2">
          {/* Kendi hakedişine karar veremez notu */}
          {isSelfApprover && (actions.canApprove || actions.canReject) ? (
            <p className="text-sm text-text-muted self-center">
              Kendi hazırladığınız hakedişe karar veremezsiniz.
            </p>
          ) : (
            <>
              {actions.canApprove && (
                <Button loading={actionBusy} onClick={() => doTransition({ durum: 'onaylandi' }, 'Hakediş onaylandı.')}>
                  Onayla
                </Button>
              )}
              {actions.canReject && (
                <Button variant="danger" loading={actionBusy} onClick={() => { setRejectReason(''); setRejectError(''); setRejectOpen(true) }}>
                  Geri gönder
                </Button>
              )}
            </>
          )}
          {actions.canSubmit && (
            <Button loading={actionBusy} onClick={() => doTransition({ durum: 'onay_bekliyor' }, 'Onay için gönderildi.')}>
              Onaya gönder
            </Button>
          )}
          {actions.canRetract && (
            <Button variant="secondary" loading={actionBusy} onClick={() => doTransition({ durum: 'taslak' }, 'Taslağa geri alındı.')}>
              Geri çek
            </Button>
          )}
          {actions.canDraft && (
            <Button variant="secondary" loading={actionBusy} onClick={() => doTransition({ durum: 'taslak' }, 'Taslağa alındı.')}>
              Taslağa al
            </Button>
          )}
          {actions.canPdf && (
            <Button variant="secondary" onClick={handleDownload}>
              PDF indir
            </Button>
          )}
          {actions.canCancel && (
            <Button variant="ghost" onClick={() => setCancelOpen(true)}>
              Taslağı iptal et
            </Button>
          )}
        </div>
      </div>

      {/* Sözleşmeli bilgi notu */}
      {caps?.contract_id && (
        <div role="note" className="text-sm text-text-muted bg-surface-muted border border-border rounded px-4 py-3">
          Miktarlar kontrol edilmiş ölçümlerden gelir, elle düzenlenemez.
        </div>
      )}

      {/* Özet kartlar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <Card padding="sm">
          <p className="text-xs text-text-muted">Önceki onaylı toplam</p>
          <p className="text-base font-semibold text-text mt-1">{formatMoney(hakedis.onceki_toplam)}</p>
        </Card>
        <Card padding="sm">
          <p className="text-xs text-text-muted">Bu dönem</p>
          <p className="text-base font-semibold text-text mt-1">{formatMoney(summary.thisPeriod)}</p>
        </Card>
        <Card padding="sm">
          <p className="text-xs text-text-muted">Kümülatif</p>
          <p className="text-base font-semibold text-text mt-1">{formatMoney(summary.cumulative)}</p>
        </Card>
        <Card padding="sm">
          <p className="text-xs text-text-muted">Sözleşme gerçekleşme</p>
          <p className="text-base font-semibold text-text mt-1">
            {summary.contractTotal > 0
              ? `%${(summary.cumulative / summary.contractTotal * 100).toFixed(1)}`
              : '—'}
          </p>
        </Card>
      </div>

      {/* Tablar */}
      <Tabs tabs={tabs} defaultTab="kalemler" />

      {/* Geri gönder modal */}
      <Modal
        open={rejectOpen}
        onClose={() => setRejectOpen(false)}
        title="Hakedişi geri gönder"
        footer={
          <>
            <Button variant="secondary" onClick={() => setRejectOpen(false)}>Vazgeç</Button>
            <Button variant="danger" onClick={handleRejectConfirm}>Geri gönder</Button>
          </>
        }
      >
        <Field label="Gerekçe" required error={rejectError}>
          <Textarea
            value={rejectReason}
            onChange={e => { setRejectReason(e.target.value); setRejectError('') }}
            rows={3}
            placeholder="Neden geri gönderiliyor?"
          />
        </Field>
      </Modal>

      {/* İptal onay modal */}
      <Modal
        open={cancelOpen}
        onClose={() => setCancelOpen(false)}
        title="Taslağı iptal et"
        footer={
          <>
            <Button variant="secondary" onClick={() => setCancelOpen(false)}>Vazgeç</Button>
            <Button variant="danger" onClick={handleCancel}>İptal et</Button>
          </>
        }
      >
        <p className="text-sm text-text-muted">
          Hakediş iptal edilecek. Kalemler ve onay geçmişi korunur.
        </p>
      </Modal>
    </div>
  )
}
