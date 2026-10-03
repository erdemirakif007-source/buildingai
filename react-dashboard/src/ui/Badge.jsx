import { cn } from './cn'

const toneClasses = {
  neutral: 'bg-surface-muted text-text-muted border-border',
  success: 'bg-success-bg text-success-fg border-success-border',
  danger:  'bg-danger-bg text-danger-fg border-danger-border',
  warning: 'bg-warning-bg text-warning-fg border-warning-border',
  info:    'bg-info-bg text-info-fg border-info-border',
  brand:   'bg-accent-soft text-link border-brand-200',
}

const dotColors = {
  neutral: 'bg-text-muted',
  success: 'bg-success-solid',
  danger:  'bg-danger-solid',
  warning: 'bg-warning-solid',
  info:    'bg-info-solid',
  brand:   'bg-primary',
}

export function Badge({ tone = 'neutral', dot = false, children, className }) {
  return (
    <span className={cn(
      'inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full border text-xs font-medium',
      toneClasses[tone],
      className
    )}>
      {dot && (
        <span
          aria-hidden
          className={cn('w-1.5 h-1.5 rounded-full flex-none', dotColors[tone])}
        />
      )}
      {children}
    </span>
  )
}
