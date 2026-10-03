import { getMeta } from './status.js'
import { Badge } from '../../ui/Badge.jsx'
import { Button } from '../../ui/Button.jsx'
import { EmptyState } from '../../ui/EmptyState.jsx'
import { Spinner } from '../../ui/Spinner.jsx'
import { formatMoney, formatDate } from '../../ui/format.js'
import { cn } from '../../ui/cn.js'

const OPEN_STATUSES = new Set(['taslak', 'onay_bekliyor', 'reddedildi'])

export function HakedisList({ items, loading, selectedId, onSelect, onNewClick }) {
  const hasOpen = items.some(h => OPEN_STATUSES.has(h.durum))

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between gap-2">
        <h3 className="text-base font-semibold text-text">Hakediş listesi</h3>
        <div className="flex flex-col items-end gap-1">
          <Button
            size="sm"
            variant="secondary"
            onClick={onNewClick}
            disabled={hasOpen}
          >
            Yeni hakediş
          </Button>
          {hasOpen && (
            <p className="text-xs text-text-muted text-right max-w-[200px]">
              Açık hakediş sonuçlanmadan yenisi oluşturulamaz.
            </p>
          )}
        </div>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-8">
          <Spinner />
        </div>
      )}

      {!loading && items.length === 0 && (
        <EmptyState
          title="Bu şantiyede henüz hakediş yok"
          description="İlk hakedişi oluşturmak için Yeni hakediş butonunu kullanın."
          action={<Button size="sm" onClick={onNewClick}>Yeni hakediş</Button>}
        />
      )}

      {!loading && items.length > 0 && (
        <ul className="flex flex-col gap-2">
          {items.map(h => {
            const meta = getMeta(h.durum)
            const isSelected = h.id === selectedId
            return (
              <li key={h.id}>
                <button
                  type="button"
                  aria-current={isSelected ? 'true' : undefined}
                  onClick={() => onSelect(h.id)}
                  className={cn(
                    'w-full text-left rounded border px-4 py-3 transition-colors duration-fast',
                    'focus-visible:outline-2 focus-visible:outline-focus-ring focus-visible:outline-offset-1',
                    isSelected
                      ? 'border-primary bg-accent-soft'
                      : 'border-border bg-surface hover:bg-surface-muted'
                  )}
                >
                  <div className="flex items-center justify-between gap-2 flex-wrap">
                    <span className="text-sm font-semibold text-text">
                      Hakediş No. {h.hakedis_no}
                    </span>
                    <Badge tone={meta.tone} dot>{meta.label}</Badge>
                  </div>
                  <p className="text-xs text-text-muted mt-1">
                    {formatDate(h.donem_baslangic)} – {formatDate(h.donem_bitis)}
                  </p>
                  <p className="text-sm font-medium text-text mt-1">
                    {formatMoney(h.toplam_tutar)}
                  </p>
                </button>
              </li>
            )
          })}
        </ul>
      )}
    </div>
  )
}
