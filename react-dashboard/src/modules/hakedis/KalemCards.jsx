import { useState } from 'react'
import { completionPercent } from './calc.js'
import { Badge } from '../../ui/Badge.jsx'
import { Spinner } from '../../ui/Spinner.jsx'
import { formatMoney, formatPercent } from '../../ui/format.js'
import { formatQuantity } from '../../lib/decimal.js'
import { cn } from '../../ui/cn.js'

function ProgressBar({ kalem }) {
  const pct = completionPercent(kalem)
  if (pct === null) return null
  const isComplete = pct >= 1
  return (
    <div className="flex items-center gap-2 mt-2">
      <div className="flex-1 h-1.5 rounded-full bg-surface-muted overflow-hidden">
        <div
          className={cn('h-full rounded-full', isComplete ? 'bg-success-solid' : 'bg-primary')}
          style={{ width: `${Math.min(100, pct * 100)}%` }}
        />
      </div>
      <span className={cn('text-xs font-medium flex-none', isComplete ? 'text-success-fg' : 'text-text-muted')}>
        {formatPercent(pct)}
      </span>
    </div>
  )
}

function KalemCard({ kalem }) {
  const [open, setOpen] = useState(false)
  const isManuel = kalem.kaynak === 'manuel'

  return (
    <div className="bg-surface border border-border rounded p-4">
      <div className="flex items-start justify-between gap-2">
        <div>
          <p className="text-sm font-semibold text-text">{kalem.tanim}</p>
          <p className="text-xs text-text-muted">{kalem.poz_no || '—'} · {kalem.birim}</p>
        </div>
        <Badge tone={isManuel ? 'neutral' : 'info'}>
          {isManuel ? 'Elle' : 'İlerleme'}
        </Badge>
      </div>

      <ProgressBar kalem={kalem} />

      <div className="grid grid-cols-2 gap-x-4 gap-y-1 mt-3 text-sm">
        <span className="text-text-muted">Bu dönem</span>
        <span className="font-medium text-text text-right tabular-nums">
          {formatQuantity(kalem.bu_donem_miktar)} {kalem.birim}
        </span>
        <span className="text-text-muted">Dönem tutarı</span>
        <span className="font-medium text-text text-right tabular-nums">
          {formatMoney(kalem.bu_donem_tutar)}
        </span>
      </div>

      <button
        type="button"
        onClick={() => setOpen(v => !v)}
        className="mt-3 text-xs text-link hover:underline focus-visible:outline-1 focus-visible:outline-focus-ring rounded"
      >
        {open ? 'Daha az göster' : 'Detayları göster'}
      </button>

      {open && (
        <div className="grid grid-cols-2 gap-x-4 gap-y-1 mt-2 text-sm border-t border-border pt-2">
          <span className="text-text-muted">Sözleşme</span>
          <span className="text-right tabular-nums">{formatQuantity(kalem.sozlesme_metraj)} {kalem.birim}</span>
          <span className="text-text-muted">Önceki</span>
          <span className="text-right tabular-nums">{formatQuantity(kalem.onceki_toplam_miktar)}</span>
          <span className="text-text-muted">Kümülatif</span>
          <span className="text-right tabular-nums">{formatQuantity(kalem.kumulatif_miktar)}</span>
          <span className="text-text-muted">Birim fiyat</span>
          <span className="text-right tabular-nums">{formatMoney(kalem.birim_fiyat)}</span>
          <span className="text-text-muted">Kümülatif tutar</span>
          <span className="text-right tabular-nums">{formatMoney(kalem.kumulatif_tutar)}</span>
        </div>
      )}
    </div>
  )
}

export function KalemCards({ kalemler, loading }) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Spinner />
      </div>
    )
  }

  if (!kalemler.length) {
    return <p className="text-sm text-text-muted text-center py-8">Bu hakedişte iş kalemi yok.</p>
  }

  return (
    <ul className="flex flex-col gap-3">
      {kalemler.map(k => (
        <li key={k.id}>
          <KalemCard kalem={k} />
        </li>
      ))}
    </ul>
  )
}
