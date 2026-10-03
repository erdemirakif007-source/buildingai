import { describe, it, expect } from 'vitest'
import { parseDecimalTR, formatQuantity } from './decimal.js'

describe('parseDecimalTR', () => {
  // TR format: nokta binlik, virgül ondalık
  it('TR format: 1.234,5 → 1234.5', () => { expect(parseDecimalTR('1.234,5')).toBe(1234.5) })
  it('TR format: 1.234,56 → 1234.56', () => { expect(parseDecimalTR('1.234,56')).toBe(1234.56) })
  it('TR format: 12.345.678,9 → 12345678.9', () => { expect(parseDecimalTR('12.345.678,9')).toBe(12345678.9) })

  // Sadece virgül → ondalık
  it('Sadece virgül: 12,5 → 12.5', () => { expect(parseDecimalTR('12,5')).toBe(12.5) })
  it('Sadece virgül: 1234,56 → 1234.56', () => { expect(parseDecimalTR('1234,56')).toBe(1234.56) })

  // Sadece nokta: binlik kalıbı
  it('Binlik nokta: 1.234 → 1234', () => { expect(parseDecimalTR('1.234')).toBe(1234) })
  it('Binlik nokta: 12.345.678 → 12345678', () => { expect(parseDecimalTR('12.345.678')).toBe(12345678) })

  // Sadece nokta: ondalık (binlik kalıbına uymayan)
  it('Ondalık nokta: 1.5 → 1.5', () => { expect(parseDecimalTR('1.5')).toBe(1.5) })
  it('Ondalık nokta: 12.50 → 12.5', () => { expect(parseDecimalTR('12.50')).toBe(12.5) })
  it('Ondalık nokta: 12.5 → 12.5', () => { expect(parseDecimalTR('12.5')).toBe(12.5) })

  // Integer
  it('Tam sayı: 100 → 100', () => { expect(parseDecimalTR('100')).toBe(100) })
  it('Tam sayı: 0 → 0', () => { expect(parseDecimalTR('0')).toBe(0) })

  // Negatif
  it('Negatif: -1.234,5 → -1234.5', () => { expect(parseDecimalTR('-1.234,5')).toBe(-1234.5) })
  it('Negatif: -12,5 → -12.5', () => { expect(parseDecimalTR('-12,5')).toBe(-12.5) })

  // Boş / null / undefined
  it('Boş string → NaN', () => { expect(parseDecimalTR('')).toBeNaN() })
  it('Sadece boşluk → NaN', () => { expect(parseDecimalTR('   ')).toBeNaN() })
  it('null → NaN', () => { expect(parseDecimalTR(null)).toBeNaN() })
  it('undefined → NaN', () => { expect(parseDecimalTR(undefined)).toBeNaN() })

  // Geçersiz karakter
  it('Harf içeren → NaN', () => { expect(parseDecimalTR('abc')).toBeNaN() })
  it('Karışık: 12abc → NaN', () => { expect(parseDecimalTR('12abc')).toBeNaN() })
  it('Türkçe karakter: 1,2m → NaN', () => { expect(parseDecimalTR('1,2m')).toBeNaN() })

  // Birden fazla virgül
  it('Çift virgül: 1,2,3 → NaN', () => { expect(parseDecimalTR('1,2,3')).toBeNaN() })

  // Boşluk kırpma
  it('Baştaki boşluk kırpılır: " 12,5" → 12.5', () => { expect(parseDecimalTR(' 12,5')).toBe(12.5) })
  it('Sondaki boşluk kırpılır: "12,5 " → 12.5', () => { expect(parseDecimalTR('12,5 ')).toBe(12.5) })
})

describe('formatQuantity', () => {
  it('Tam sayı: 100 → "100"', () => { expect(formatQuantity(100)).toBe('100') })
  it('Ondalık tr-TR: 1.5 → "1,5"', () => { expect(formatQuantity(1.5)).toBe('1,5') })
  it('3 ondalık: 1.234 → "1,234"', () => { expect(formatQuantity(1.234)).toBe('1,234') })
  it('4. ondalık yuvarlanır: 1.2345 → "1,235"', () => { expect(formatQuantity(1.2345)).toBe('1,235') })
  it('NaN → boş string', () => { expect(formatQuantity(NaN)).toBe('') })
  it('null → boş string', () => { expect(formatQuantity(null)).toBe('') })
  it('undefined → boş string', () => { expect(formatQuantity(undefined)).toBe('') })
  it('0 → "0"', () => { expect(formatQuantity(0)).toBe('0') })
})
