import { EmptyState } from '../../ui/EmptyState.jsx'
import { Table } from '../../ui/Table.jsx'
import { formatMoney, formatDate } from '../../ui/format.js'
import { formatQuantity } from '../../lib/decimal.js'

const columns = [
  { key: 'id',       header: 'Ölçüm no',       render: row => row.measurement?.id ?? '—' },
  { key: 'qty',      header: 'Miktar',           numeric: true,
    render: row => `${formatQuantity(row.quantity)} ${row.measurement?.unit ?? ''}` },
  { key: 'amount',   header: 'Tutar',            numeric: true, render: row => formatMoney(row.amount) },
  { key: 'basis',    header: 'Dayanak',          render: row => row.measurement?.basis || '—' },
  { key: 'evidence', header: 'Belge kayıtları',  render: row => (row.measurement?.evidence_ids?.length ?? 0) > 0
    ? `${row.measurement.evidence_ids.length} belge`
    : '—'
  },
]

export function AllocationsTable({ allocations, loading }) {
  const total = allocations.reduce((s, a) => s + (Number(a.amount) || 0), 0)

  return (
    <Table
      columns={columns}
      rows={allocations.map((a, i) => ({ ...a, _key: i }))}
      loading={loading}
      emptyTitle="Ölçüm tahsisi yok"
      emptyDescription="Bu hakedişe henüz ölçüm tahsisi yapılmamış."
      footer={{ amount: formatMoney(total) }}
      caption="Hakediş ölçüm tahsisleri"
    />
  )
}
