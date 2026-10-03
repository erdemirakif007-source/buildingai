import { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { X, CheckCircle2, AlertCircle, Info } from 'lucide-react'
import { cn } from './cn'

const ToastContext = createContext(null)

const toneClasses = {
  success: 'bg-success-bg border-success-border text-success-fg',
  danger:  'bg-danger-bg border-danger-border text-danger-fg',
  info:    'bg-surface border-border text-text',
}

const icons = {
  success: CheckCircle2,
  danger:  AlertCircle,
  info:    Info,
}

const DEFAULT_DURATION = { success: 4000, info: 4000, danger: 6000 }
const MAX_TOASTS = 3

function ToastItem({ id, message, tone = 'info', onRemove }) {
  const Icon = icons[tone]
  return (
    <div
      role="status"
      aria-live={tone === 'danger' ? 'assertive' : 'polite'}
      aria-atomic="true"
      className={cn(
        'flex items-start gap-3 w-full md:w-auto md:min-w-[280px] md:max-w-sm',
        'px-4 py-3 rounded border shadow-md',
        'animate-fade-in',
        toneClasses[tone]
      )}
    >
      {Icon && <Icon size={18} aria-hidden className="flex-none mt-0.5" />}
      <span className="flex-1 text-sm font-medium">{message}</span>
      <button
        type="button"
        onClick={() => onRemove(id)}
        className="flex-none p-0.5 rounded hover:opacity-70 transition-opacity focus-visible:outline-2 focus-visible:outline-current"
        aria-label="Bildirimi kapat"
      >
        <X size={14} aria-hidden />
      </button>
    </div>
  )
}

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])
  const timers = useRef({})

  const remove = useCallback((id) => {
    clearTimeout(timers.current[id])
    delete timers.current[id]
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  const add = useCallback(({ message, tone = 'info', duration }) => {
    const id = Date.now() + Math.random()
    setToasts(prev => {
      const next = [...prev, { id, message, tone }]
      return next.length > MAX_TOASTS ? next.slice(next.length - MAX_TOASTS) : next
    })
    const ms = duration ?? DEFAULT_DURATION[tone] ?? 4000
    timers.current[id] = setTimeout(() => remove(id), ms)
    return id
  }, [remove])

  useEffect(() => () => Object.values(timers.current).forEach(clearTimeout), [])

  return (
    <ToastContext.Provider value={add}>
      {children}
      {createPortal(
        <div className="fixed bottom-4 right-4 z-toast flex flex-col-reverse gap-2 w-full md:w-auto px-4 md:px-0 pointer-events-none">
          <div className="flex flex-col gap-2 pointer-events-auto">
            {toasts.map(t => (
              <ToastItem key={t.id} {...t} onRemove={remove} />
            ))}
          </div>
        </div>,
        document.body
      )}
    </ToastContext.Provider>
  )
}

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used within ToastProvider')
  return ctx
}
