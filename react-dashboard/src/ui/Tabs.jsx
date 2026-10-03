import { useState, useRef, useId } from 'react'
import { cn } from './cn'

export function Tabs({ tabs, defaultTab, value: controlledValue, onChange, children, className }) {
  const baseId = useId()
  const [internalValue, setInternalValue] = useState(defaultTab ?? tabs[0]?.key)
  const active = controlledValue ?? internalValue
  const listRef = useRef(null)

  function handleSelect(key) {
    if (onChange) onChange(key)
    else setInternalValue(key)
  }

  function handleKeyDown(e) {
    const keys = tabs.map(t => t.key)
    const idx = keys.indexOf(active)
    if (e.key === 'ArrowRight') { e.preventDefault(); handleSelect(keys[(idx + 1) % keys.length]) }
    if (e.key === 'ArrowLeft')  { e.preventDefault(); handleSelect(keys[(idx - 1 + keys.length) % keys.length]) }
    if (e.key === 'Home')       { e.preventDefault(); handleSelect(keys[0]) }
    if (e.key === 'End')        { e.preventDefault(); handleSelect(keys[keys.length - 1]) }
  }

  const panelContent = typeof children === 'function'
    ? children(active)
    : tabs.find(t => t.key === active)?.content

  return (
    <div className={className}>
      <div
        ref={listRef}
        role="tablist"
        onKeyDown={handleKeyDown}
        className="flex gap-1 border-b border-border"
      >
        {tabs.map(tab => {
          const isActive = tab.key === active
          return (
            <button
              key={tab.key}
              type="button"
              role="tab"
              id={`${baseId}-tab-${tab.key}`}
              aria-controls={`${baseId}-panel-${tab.key}`}
              aria-selected={isActive}
              tabIndex={isActive ? 0 : -1}
              onClick={() => handleSelect(tab.key)}
              className={cn(
                'px-4 py-2.5 text-sm font-medium rounded-t border-b-2 -mb-px',
                'transition-colors duration-fast focus-visible:outline-2 focus-visible:outline-focus-ring',
                isActive
                  ? 'border-primary text-primary'
                  : 'border-transparent text-text-muted hover:text-text hover:border-border-strong'
              )}
            >
              {tab.label}
            </button>
          )
        })}
      </div>
      <div
        role="tabpanel"
        id={`${baseId}-panel-${active}`}
        aria-labelledby={`${baseId}-tab-${active}`}
        tabIndex={0}
        className="pt-4 focus-visible:outline-none"
      >
        {panelContent}
      </div>
    </div>
  )
}
