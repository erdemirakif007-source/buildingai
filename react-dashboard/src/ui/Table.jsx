import { cn } from './cn'
import { EmptyState } from './EmptyState'
import { Spinner } from './Spinner'

export function Table({
  columns, rows, loading, onRowClick, footer, className,
  stickyHeader = false, maxHeight = '60vh',
  emptyTitle = 'Kayıt bulunamadı',
  emptyDescription = 'Bu tabloda gösterilecek veri yok.',
  emptyAction,
  caption,
}) {
  return (
    <div
      className={cn('overflow-x-auto rounded border border-border', className)}
      style={stickyHeader ? { maxHeight, overflowY: 'auto' } : undefined}
    >
      <table className="w-full min-w-[400px] border-collapse text-base">
        {caption && <caption className="sr-only">{caption}</caption>}
        <thead>
          <tr className="border-b border-border bg-surface-muted">
            {columns.map(col => (
              <th
                key={col.key}
                scope="col"
                className={cn(
                  'px-4 py-3 text-sm font-semibold text-text-muted whitespace-nowrap',
                  stickyHeader && 'sticky top-0 z-sticky bg-surface-muted',
                  (col.align === 'right' || col.numeric) ? 'text-right' : 'text-left'
                )}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {loading ? (
            Array.from({ length: 4 }).map((_, i) => (
              <tr key={i} className="border-b border-border">
                {columns.map(col => (
                  <td key={col.key} className="px-4 py-3">
                    <div className="h-4 rounded bg-surface-muted animate-pulse" />
                  </td>
                ))}
              </tr>
            ))
          ) : rows && rows.length > 0 ? (
            rows.map((row, i) => (
              <tr
                key={row.id ?? i}
                onClick={onRowClick ? () => onRowClick(row) : undefined}
                onKeyDown={onRowClick ? (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onRowClick(row) } } : undefined}
                tabIndex={onRowClick ? 0 : undefined}
                className={cn(
                  'border-b border-border last:border-0',
                  'hover:bg-surface-muted transition-colors duration-fast',
                  onRowClick && 'cursor-pointer focus-visible:outline-2 focus-visible:outline-focus-ring focus-visible:outline-offset-[-2px]'
                )}
              >
                {columns.map(col => (
                  <td
                    key={col.key}
                    className={cn(
                      'px-4 py-3 text-text',
                      (col.align === 'right' || col.numeric) && 'text-right tabular-nums'
                    )}
                  >
                    {col.render ? col.render(row) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={columns.length}>
                <EmptyState title={emptyTitle} description={emptyDescription} action={emptyAction} />
              </td>
            </tr>
          )}
        </tbody>
        {footer && (
          <tfoot>
            <tr className="border-t-2 border-border-strong bg-surface-muted font-semibold">
              {columns.map(col => (
                <td
                  key={col.key}
                  className={cn(
                    'px-4 py-3 text-text',
                    (col.align === 'right' || col.numeric) && 'text-right tabular-nums'
                  )}
                >
                  {footer[col.key] ?? ''}
                </td>
              ))}
            </tr>
          </tfoot>
        )}
      </table>
    </div>
  )
}
