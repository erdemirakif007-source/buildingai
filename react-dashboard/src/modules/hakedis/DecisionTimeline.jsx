import { getMeta } from './status.js'
import { EmptyState } from '../../ui/EmptyState.jsx'
import { formatDate } from '../../ui/format.js'
import { cn } from '../../ui/cn.js'

const dotClass = {
  onaylandi:     'bg-success-solid',
  reddedildi:    'bg-danger-solid',
  onay_bekliyor: 'bg-warning-solid',
  taslak:        'bg-border-strong',
}

function Skeleton() {
  return (
    <div className="flex flex-col gap-4">
      {[0, 1].map(i => (
        <div key={i} className="flex gap-4 animate-pulse">
          <div className="flex flex-col items-center">
            <div className="w-2.5 h-2.5 rounded-full bg-surface-muted mt-1 flex-none" />
            {i === 0 && <div className="w-px flex-1 bg-surface-muted mt-1" />}
          </div>
          <div className="pb-4 flex-1">
            <div className="h-4 w-32 rounded bg-surface-muted mb-1" />
            <div className="h-3 w-48 rounded bg-surface-muted" />
          </div>
        </div>
      ))}
    </div>
  )
}

export function DecisionTimeline({ decisions, loading }) {
  if (loading) return <Skeleton />

  if (!decisions.length) {
    return (
      <EmptyState
        title="Henüz karar alınmadı"
        description="Hakediş onay süreci başladığında burada görünecek."
      />
    )
  }

  return (
    <ol className="flex flex-col gap-0">
      {decisions.map((d, i) => {
        const meta = getMeta(d.new_status)
        return (
          <li key={i} className="flex gap-4">
            <div className="flex flex-col items-center flex-none">
              <span className={cn(
                'w-2.5 h-2.5 rounded-full mt-1 flex-none',
                dotClass[d.new_status] ?? 'bg-border-strong'
              )} />
              {i < decisions.length - 1 && (
                <span className="w-px flex-1 bg-border mt-1" />
              )}
            </div>
            <div className="pb-5">
              <p className="text-sm font-medium text-text">{meta.label}</p>
              <p className="text-xs text-text-muted">
                {d.actor_ad ?? `Kullanıcı #${d.actor_id}`} · {formatDate(d.created_at)}
              </p>
              {d.reason && (
                <blockquote className="mt-1 text-sm text-text-subtle italic border-l-2 border-border pl-3">
                  "{d.reason}"
                </blockquote>
              )}
            </div>
          </li>
        )
      })}
    </ol>
  )
}
