import { cn } from './cn'

export function EmptyState({ icon: Icon, title, description, action, className }) {
  return (
    <div className={cn('flex flex-col items-center justify-center py-12 px-6 text-center gap-3', className)}>
      {Icon && (
        <div className="w-12 h-12 rounded-full bg-surface-muted flex items-center justify-center text-text-subtle" aria-hidden>
          <Icon size={22} />
        </div>
      )}
      {title && <p className="text-base font-semibold text-text">{title}</p>}
      {description && <p className="text-sm text-text-muted max-w-xs">{description}</p>}
      {action && <div className="mt-2">{action}</div>}
    </div>
  )
}
