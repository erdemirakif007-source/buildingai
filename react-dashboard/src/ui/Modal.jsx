import { useEffect, useRef } from 'react'
import { createPortal } from 'react-dom'
import { X } from 'lucide-react'
import { cn } from './cn'

const sizeClasses = {
  sm: 'max-w-sm',
  md: 'max-w-lg',
  lg: 'max-w-2xl',
}

const FOCUSABLE = [
  'a[href]', 'button:not([disabled])', 'input:not([disabled])',
  'select:not([disabled])', 'textarea:not([disabled])',
  '[tabindex]:not([tabindex="-1"])',
].join(',')

export function Modal({ open, onClose, title, children, footer, size = 'md', closeOnOverlay = true }) {
  const dialogRef = useRef(null)
  const triggerRef = useRef(null)
  const mousedownTargetRef = useRef(null)

  useEffect(() => {
    if (open) {
      triggerRef.current = document.activeElement
      const el = dialogRef.current
      if (el) {
        const first = el.querySelectorAll(FOCUSABLE)[0]
        if (first) first.focus()
      }
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
      triggerRef.current?.focus()
    }
    return () => { document.body.style.overflow = '' }
  }, [open])

  useEffect(() => {
    if (!open) return
    function onKey(e) {
      if (e.key === 'Escape') { onClose(); return }
      if (e.key !== 'Tab') return
      const el = dialogRef.current
      if (!el) return
      const nodes = [...el.querySelectorAll(FOCUSABLE)]
      if (!nodes.length) return
      const first = nodes[0], last = nodes[nodes.length - 1]
      if (e.shiftKey ? document.activeElement === first : document.activeElement === last) {
        e.preventDefault()
        ;(e.shiftKey ? last : first).focus()
      }
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [open, onClose])

  if (!open) return null

  const titleId = 'modal-title-' + Math.random().toString(36).slice(2)

  return createPortal(
    <div
      className="fixed inset-0 z-modal flex items-end md:items-center justify-center p-0 md:p-4"
      style={{ background: 'var(--bai-overlay)' }}
      onMouseDown={closeOnOverlay ? (e) => { mousedownTargetRef.current = e.target } : undefined}
      onClick={closeOnOverlay ? (e) => { if (mousedownTargetRef.current === e.currentTarget && e.target === e.currentTarget) onClose() } : undefined}
    >
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        className={cn(
          'relative flex flex-col bg-surface shadow-lg',
          'w-full rounded-t-lg md:rounded-lg',
          'max-h-[90dvh] overflow-y-auto',
          'animate-sheet-in md:animate-modal-in',
          sizeClasses[size]
        )}
      >
        <div className="flex items-center justify-between gap-4 px-6 py-4 border-b border-border">
          <h2 id={titleId} className="text-lg font-semibold text-text">{title}</h2>
          <button
            type="button"
            onClick={onClose}
            className="p-2 rounded text-text-muted hover:text-text hover:bg-surface-muted transition-colors duration-fast focus-visible:outline-2 focus-visible:outline-focus-ring"
            aria-label="Kapat"
          >
            <X size={18} aria-hidden />
          </button>
        </div>
        <div className="flex-1 px-6 py-5 overflow-y-auto">{children}</div>
        {footer && (
          <div className="px-6 py-4 border-t border-border flex items-center justify-end gap-3">
            {footer}
          </div>
        )}
      </div>
    </div>,
    document.body
  )
}
