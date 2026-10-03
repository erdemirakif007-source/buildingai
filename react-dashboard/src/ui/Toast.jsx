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

function ToastItem({ id, message, tone = 'info', duration, onRemove }) {
  const Icon = icons[tone]
  const startRef = useRef(null)
  const remainingRef = useRef(duration)
  const timerRef = useRef(null)

  const pause = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current)
      timerRef.current = null
      remainingRef.current -= Date.now() - startRef.current
    }
  }, [])

  const resume = useCallback(() => {
    startRef.current = Date.now()
    timerRef.current = setTimeout(() => onRemove(id), remainingRef.current)
  }, [id, onRemove])

  useEffect(() => {
    resume()
    return () => clearTimeout(timerRef.current)
  }, [resume])

  return (
    <div
      className={cn(
        'flex items-start gap-3',
        'px-4 py-3 rounded border shadow-md',
        'animate-fade-in',
        toneClasses[tone]
      )}
      onMouseEnter={pause}
      onMouseLeave={resume}
      onFocusCapture={pause}
      onBlurCapture={resume}
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
    const ms = duration ?? DEFAULT_DURATION[tone] ?? 4000
    setToasts(prev => {
      if (prev.length >= MAX_TOASTS) {
        const dropped = prev[0]
        clearTimeout(timers.current[dropped.id])
        delete timers.current[dropped.id]
        return [...prev.slice(1), { id, message, tone, duration: ms }]
      }
      return [...prev, { id, message, tone, duration: ms }]
    })
    return id
  }, [])

  useEffect(() => () => Object.values(timers.current).forEach(clearTimeout), [])

  const politeToasts = toasts.filter(t => t.tone !== 'danger')
  const urgentToasts = toasts.filter(t => t.tone === 'danger')

  return (
    <ToastContext.Provider value={add}>
      {children}
      {createPortal(
        <>
          <div
            aria-live="polite"
            aria-atomic="false"
            className="sr-only"
          >
            {politeToasts.map(t => <span key={t.id}>{t.message}</span>)}
          </div>
          <div
            role="alert"
            aria-atomic="false"
            className="sr-only"
          >
            {urgentToasts.map(t => <span key={t.id}>{t.message}</span>)}
          </div>
          <div
            className="fixed z-toast flex flex-col-reverse gap-2 pointer-events-none"
            style={{
              bottom: 'max(1rem, env(safe-area-inset-bottom, 1rem))',
              right: '1rem',
              left: '1rem',
            }}
          >
            <div className="flex flex-col gap-2 pointer-events-auto md:items-end">
              {toasts.map(t => (
                <ToastItem key={t.id} {...t} onRemove={remove} />
              ))}
            </div>
          </div>
        </>,
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
