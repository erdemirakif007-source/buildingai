export function computeSummary(hakedis, kalemler = []) {
  const thisPeriod   = kalemler.reduce((s, k) => s + (Number(k.bu_donem_tutar)   || 0), 0)
  const cumulative   = kalemler.reduce((s, k) => s + (Number(k.kumulatif_tutar)  || 0), 0)
  const contractTotal= kalemler.reduce((s, k) => s + (Number(k.sozlesme_metraj)  || 0) * (Number(k.birim_fiyat) || 0), 0)
  const prevTotal    = Number(hakedis?.onceki_toplam) || 0
  return { thisPeriod, cumulative, contractTotal, prevTotal }
}

export function completionPercent(kalem) {
  const contract = Number(kalem?.sozlesme_metraj) || 0
  if (contract === 0) return null
  return Math.min(1, (Number(kalem?.kumulatif_miktar) || 0) / contract)
}

export function defaultPeriod(lastApprovedBitis) {
  const today = new Date()
  let start, end

  if (lastApprovedBitis) {
    const prev = new Date(lastApprovedBitis)
    start = new Date(prev.getFullYear(), prev.getMonth(), prev.getDate() + 1)
  } else {
    start = new Date(today.getFullYear(), today.getMonth(), 1)
  }

  end = new Date(start.getFullYear(), start.getMonth() + 1, 0)

  const fmt = d => d.toISOString().slice(0, 10)
  return { start: fmt(start), end: fmt(end) }
}
