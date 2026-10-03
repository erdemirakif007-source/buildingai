import { cn } from './cn'

const paddingClasses = {
  none: '',
  sm:   'p-4',
  md:   'p-6',
}

export function Card({ title, description, action, children, padding = 'md', className }) {
  return (
    <div className={cn('bg-surface border border-border rounded shadow-sm', paddingClasses[padding], className)}>
      {(title || action) && (
        <div className="flex items-start justify-between gap-4 mb-4">
          <div>
            {title && <h3 className="text-base font-semibold text-text">{title}</h3>}
            {description && <p className="text-sm text-text-muted mt-0.5">{description}</p>}
          </div>
          {action && <div className="flex-none">{action}</div>}
        </div>
      )}
      {children}
    </div>
  )
}
