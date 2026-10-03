import { useRef, useState } from 'react'
import { updateKalem } from './api.js'
import { completionPercent } from './calc.js'
import { Badge } from '../../ui/Badge.jsx'
import { Field } from '../../ui/Field.jsx'
import { Input } from '../../ui/Field.jsx'
import { Spinner } from '../../ui/Spinner.jsx'
import { Table } from '../../ui/Table.jsx'
import { Toggle } from '../../ui/Toggle.jsx'
import { useToast } from '../../ui/Toast.jsx'
import { formatMoney, formatPercent } from '../../ui/format.js'
import { formatQuantity, parseDecimalTR } from '../../lib/decimal.js'
import { cn } from '../../ui/cn.js'

function KalemBadge({ kaynak }) {
  const isManuel = kaynak === 'manuel'
  return (
    <Badge
      tone={isManuel ? 'neutral' : 'info'}
      title={isManuel
        ? 'Elle girildi; ilerleme kayıtları bu değeri değiştirmez'
        : 'İlerleme kayıtlarından otomatik hesaplandı'}
    >
      {isManuel ? 'Elle' : 'İlerleme'}
    </Badge>
  )
}

function ProgressCell({ kalem }) {
  const pct = completionPercent(kalem)
  if (pct === null) return <span className="text-text-muted">—</span>
  const isComplete = pct >= 1
  return (
    <div className="flex flex-col gap-1 min-w-[80px]">
      <span className={cn('text-xs font-medium', isComplete ? 'text-success-fg' : 'text-text')}>
        {formatPercent(pct)}
      </span>
      <div className="h-1 rounded-full bg-surface-muted overflow-hidden">
        <div
          className={cn('h-full rounded-full', isComplete ? 'bg-success-solid' : 'bg-primary')}
          style={{ width: `${Math.min(100, pct * 100)}%` }}
        />
      </div>
    </div>
  )
}

function EditableCell({ kalem, token, onKalemUpdated }) {
  const [editing, setEditing] = useState(false)
  const [val, setVal]         = useState('')
  const [savedVal, setSavedVal] = useState(String(kalem.bu_donem_miktar))
  const [saving, setSaving]   = useState(false)
  const [saved, setSaved]     = useState(false)
  const [error, setError]     = useState('')
  const pendingRef = useRef(false)
  const toast = useToast()

  const kalan = (Number(kalem.sozlesme_metraj) || 0) - (Number(kalem.onceki_toplam_miktar) || 0)

  function validate(v) {
    const n = parseDecimalTR(v)
    if (v === '' || isNaN(n)) return 'Geçerli bir sayı girin.'
    if (n < 0) return 'Negatif değer girilmez.'
    if (n > kalan + 0.0001) return `En fazla: ${formatQuantity(kalan)} ${kalem.birim}`
    return ''
  }

  async function commit(v) {
    const n = parseDecimalTR(v)
    const err = validate(v)
    if (err) { setError(err); return }
    if (n === parseDecimalTR(savedVal)) { setEditing(false); return }
    if (pendingRef.current) return
    pendingRef.current = true
    setSaving(true)
    setError('')
    try {
      const result = await updateKalem({ hakedis_kalem_id: kalem.id, bu_donem_miktar: n }, token)
      setSavedVal(String(n))
      setSaved(true)
      setTimeout(() => setSaved(false), 1500)
      onKalemUpdated({ ...result.kalem, bu_donem_miktar: n })
      setEditing(false)
    } catch (err) {
      setError(err.message)
      toast({ message: err.message, tone: 'danger' })
    } finally {
      setSaving(false)
      pendingRef.current = false
    }
  }

  if (saving) return <Spinner size="sm" />
  if (saved) return <span className="text-success-fg text-sm">✓ {formatQuantity(parseDecimalTR(savedVal))}</span>

  if (!editing) {
    return (
      <button
        type="button"
        className="text-right tabular-nums text-sm hover:underline focus-visible:outline-1 focus-visible:outline-focus-ring rounded"
        onClick={() => { setVal(savedVal); setError(''); setEditing(true) }}
      >
        {formatQuantity(kalem.bu_donem_miktar)}
      </button>
    )
  }

  return (
    <div className="flex flex-col gap-1">
      <Input
        numeric
        autoFocus
        value={val}
        onChange={e => { setVal(e.target.value); setError('') }}
        onBlur={e => commit(e.target.value)}
        onKeyDown={e => {
          if (e.key === 'Enter') { e.preventDefault(); commit(val) }
          if (e.key === 'Escape') { setEditing(false); setError('') }
        }}
        className="w-28 h-8 text-sm"
        aria-invalid={error ? 'true' : undefined}
      />
      {!error && (
        <span className="text-xs text-text-subtle">
          En fazla: {formatQuantity(kalan)} {kalem.birim}
        </span>
      )}
      {error && <span className="text-xs text-danger-fg">{error}</span>}
    </div>
  )
}

export function KalemTable({ kalemler, loading, durum, caps, capsLoading, token, onKalemUpdated }) {
  const [search, setSearch]         = useState('')
  const [onlyActive, setOnlyActive] = useState(false)
  const toast = useToast()

  const canEdit = durum === 'taslak' && !caps?.contract_id && !!caps?.can_submit && !capsLoading

  const filtered = kalemler.filter(k => {
    const q = search.toLowerCase()
    const matchSearch = !q || k.poz_no?.toLowerCase().includes(q) || k.tanim?.toLowerCase().includes(q)
    const matchActive = !onlyActive || Number(k.bu_donem_miktar) > 0
    return matchSearch && matchActive
  })

  const totalThisPeriod  = kalemler.reduce((s, k) => s + (Number(k.bu_donem_tutar) || 0), 0)
  const totalKumulatif   = kalemler.reduce((s, k) => s + (Number(k.kumulatif_tutar) || 0), 0)

  const columns = [
    { key: 'poz_no',            header: 'Poz',           render: k => k.poz_no || '—' },
    { key: 'tanim',             header: 'Tanım' },
    { key: 'birim',             header: 'Birim' },
    { key: 'sozlesme_metraj',   header: 'Sözleşme',      numeric: true, render: k => formatQuantity(k.sozlesme_metraj) },
    { key: 'onceki_toplam_miktar', header: 'Önceki',     numeric: true, render: k => formatQuantity(k.onceki_toplam_miktar) },
    {
      key: 'bu_donem_miktar',
      header: 'Bu dönem',
      numeric: true,
      render: k => canEdit
        ? <EditableCell kalem={k} token={token} onKalemUpdated={onKalemUpdated} />
        : formatQuantity(k.bu_donem_miktar),
    },
    { key: 'kumulatif_miktar',  header: 'Kümülatif',     numeric: true, render: k => formatQuantity(k.kumulatif_miktar) },
    { key: 'ilerleme',          header: 'İlerleme',      render: k => <ProgressCell kalem={k} /> },
    { key: 'kaynak',            header: 'Kaynak',        render: k => <KalemBadge kaynak={k.kaynak} /> },
    { key: 'birim_fiyat',       header: 'Birim fiyat',   numeric: true, render: k => formatMoney(k.birim_fiyat) },
    { key: 'bu_donem_tutar',    header: 'Dönem tutarı',  numeric: true, render: k => formatMoney(k.bu_donem_tutar) },
    { key: 'kumulatif_tutar',   header: 'Kümülatif tutar', numeric: true, render: k => formatMoney(k.kumulatif_tutar) },
  ]

  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-wrap items-center gap-3">
        <input
          type="search"
          placeholder="Poz no veya tanım ara…"
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="h-9 rounded border border-border bg-surface text-sm px-3 focus-visible:outline-none focus-visible:border-focus-ring focus-visible:ring-1 focus-visible:ring-focus-ring-soft w-56"
        />
        <Toggle
          checked={onlyActive}
          onChange={setOnlyActive}
          label="Sadece bu dönem hareketi olanlar"
        />
        <span className="text-xs text-text-muted ml-auto">{filtered.length} kalem</span>
      </div>

      <Table
        columns={columns}
        rows={filtered}
        loading={loading}
        stickyHeader
        caption={`Hakediş iş kalemleri — ${kalemler.length} satır`}
        footer={{
          bu_donem_tutar:  formatMoney(totalThisPeriod),
          kumulatif_tutar: formatMoney(totalKumulatif),
        }}
        emptyTitle="Kalem bulunamadı"
        emptyDescription={search || onlyActive ? 'Arama veya filtreyi temizleyin.' : 'Bu hakedişte iş kalemi yok.'}
      />
    </div>
  )
}
