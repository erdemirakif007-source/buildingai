// Yalnızca rakam, nokta, virgül ve baştaki eksi işaretine izin ver.
const VALID_CHARS = /^-?[\d.,]+$/

/**
 * Türkçe yerel biçimli sayı dizisini float'a çevirir.
 *
 * Kurallar:
 *  - Boşlukları kırp; boş/null/undefined → NaN
 *  - Geçersiz karakter (VALID_CHARS dışı) → NaN
 *  - Birden fazla virgül → NaN
 *  - Virgül + nokta birlikte: nokta binlik, virgül ondalık ("1.234,5" → 1234.5)
 *  - Sadece virgül: virgül ondalık ("1234,5" → 1234.5)
 *  - Sadece nokta: /^\d{1,3}(\.\d{3})+$/ kalıbına uyuyorsa binlik ("1.234" → 1234),
 *    uymuyorsa ondalık ("1.5" → 1.5, "12.50" → 12.5)
 */
export function parseDecimalTR(str) {
  if (str === null || str === undefined) return NaN
  const s = String(str).trim()
  if (s === '') return NaN
  if (!VALID_CHARS.test(s)) return NaN

  const commaCount = (s.match(/,/g) || []).length
  if (commaCount > 1) return NaN

  if (s.includes(',') && s.includes('.')) {
    // TR format: 1.234,56 → nokta binlik, virgül ondalık
    return Number(s.replace(/\./g, '').replace(',', '.'))
  }

  if (s.includes(',')) {
    // Sadece virgül → ondalık
    return Number(s.replace(',', '.'))
  }

  if (s.includes('.')) {
    // Sadece nokta: binlik mi ondalık mı?
    const absS = s.startsWith('-') ? s.slice(1) : s
    if (/^\d{1,3}(\.\d{3})+$/.test(absS)) {
      // Binlik ayırıcı: 1.234 veya 12.345.678
      return Number((s.startsWith('-') ? '-' : '') + absS.replace(/\./g, ''))
    }
    return Number(s)
  }

  return Number(s)
}

/**
 * Sayıyı tr-TR yerel biçiminde, en fazla 3 ondalık ile formatlar.
 * NaN / null / undefined → boş dizi.
 */
export function formatQuantity(n) {
  const num = typeof n === 'number' ? n : Number(n)
  if (n === null || n === undefined || isNaN(num)) return ''
  return new Intl.NumberFormat('tr-TR', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 3,
  }).format(num)
}
