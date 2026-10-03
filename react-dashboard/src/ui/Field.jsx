import { cloneElement, isValidElement, useId } from 'react'
import { ChevronDown } from 'lucide-react'
import { cn } from './cn'

const baseInput = [
  'block w-full rounded border border-border bg-surface text-text',
  'px-3 placeholder:text-text-disabled',
  'transition-colors duration-fast',
  'focus-visible:outline-none focus-visible:border-focus-ring focus-visible:ring-2 focus-visible:ring-focus-ring-soft',
  'disabled:opacity-40 disabled:cursor-not-allowed',
  'aria-[invalid=true]:border-danger-solid aria-[invalid=true]:ring-1 aria-[invalid=true]:ring-danger-solid',
].join(' ')

export function Input({ numeric, className, ...props }) {
  return (
    <input
      className={cn(
        baseInput,
        'h-control-lg text-lg md:h-control-md md:text-base',
        numeric && 'text-right tabular-nums',
        className
      )}
      inputMode={numeric ? 'decimal' : undefined}
      {...props}
    />
  )
}

export function Select({ className, children, ...props }) {
  return (
    <div className="relative">
      <select
        className={cn(baseInput, 'h-control-lg text-lg md:h-control-md md:text-base appearance-none pr-10 cursor-pointer', className)}
        {...props}
      >
        {children}
      </select>
      <ChevronDown
        size={16}
        aria-hidden
        className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-text-muted"
      />
    </div>
  )
}

export function Textarea({ className, ...props }) {
  return (
    <textarea
      className={cn(baseInput, 'py-2 text-lg md:text-base min-h-textarea resize-y', className)}
      {...props}
    />
  )
}

export function Field({ label, hint, error, required, children, className }) {
  const id = useId()
  const hintId = hint ? `${id}-hint` : undefined
  const errorId = error ? `${id}-error` : undefined
  const describedBy = [hintId, errorId].filter(Boolean).join(' ') || undefined

  const accessibilityProps = {
    'aria-describedby': describedBy,
    'aria-invalid': error ? 'true' : undefined,
    'aria-required': required,
  }

  let child
  if (typeof children === 'function') {
    child = children({ id, ...accessibilityProps })
  } else if (isValidElement(children)) {
    const childId = children.props.id || id
    child = cloneElement(children, { id: childId, ...accessibilityProps })
  } else {
    child = children
  }

  const labelTarget = isValidElement(children) && children.props.id
    ? children.props.id
    : id

  return (
    <div className={cn('flex flex-col gap-1', className)}>
      {label && (
        <label htmlFor={labelTarget} className="text-sm font-medium text-text">
          {label}
          {required && <span className="text-danger-fg ml-0.5" aria-hidden>*</span>}
        </label>
      )}
      {child}
      {hint && !error && <p id={hintId} className="text-sm text-text-subtle">{hint}</p>}
      {error && <p id={errorId} role="alert" className="text-sm text-danger-fg">{error}</p>}
    </div>
  )
}
