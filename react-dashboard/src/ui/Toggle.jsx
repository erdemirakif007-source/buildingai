import { useId } from 'react'
import { cn } from './cn'

export function Toggle({ label, checked, onChange, disabled, className }) {
  const id = useId()
  return (
    <label
      htmlFor={id}
      className={cn(
        'inline-flex items-center gap-3 cursor-pointer select-none',
        disabled && 'opacity-40 cursor-not-allowed',
        className
      )}
    >
      <button
        type="button"
        role="switch"
        id={id}
        aria-checked={checked}
        disabled={disabled}
        onClick={() => !disabled && onChange(!checked)}
        className={cn(
          'relative inline-flex w-10 h-6 rounded-full border-2 border-transparent',
          'transition-colors duration-fast focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus-ring',
          checked ? 'bg-primary' : 'bg-border-strong'
        )}
      >
        <span
          aria-hidden
          className={cn(
            'inline-block w-4 h-4 rounded-full bg-white shadow-sm',
            'transition-transform duration-fast',
            checked ? 'translate-x-4' : 'translate-x-0.5'
          )}
          style={{ marginTop: '2px' }}
        />
      </button>
      {label && <span className="text-base text-text">{label}</span>}
    </label>
  )
}
