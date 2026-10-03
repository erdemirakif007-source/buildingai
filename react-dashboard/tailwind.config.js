import { readFileSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const tokens = JSON.parse(readFileSync(resolve(__dirname, '../design/tokens.json'), 'utf8'))

function brandColors() {
  return Object.fromEntries(
    Object.keys(tokens.color.brand).map(k => [k, `var(--bai-color-brand-${k})`])
  )
}

function slateColors() {
  return Object.fromEntries(
    Object.keys(tokens.color.slate).map(k => [k, `var(--bai-color-slate-${k})`])
  )
}

function semanticColor(key) {
  return `var(--bai-${key})`
}

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}', '!./src/_arsiv/**'],
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      white: '#ffffff',
      black: '#000000',
      brand: brandColors(),
      slate: slateColors(),
      success: {
        fg:     'var(--bai-color-success-fg)',
        bg:     'var(--bai-color-success-bg)',
        border: 'var(--bai-color-success-border)',
        solid:  'var(--bai-color-success-solid)',
      },
      danger: {
        fg:     'var(--bai-color-danger-fg)',
        bg:     'var(--bai-color-danger-bg)',
        border: 'var(--bai-color-danger-border)',
        solid:  'var(--bai-color-danger-solid)',
      },
      warning: {
        fg:     'var(--bai-color-warning-fg)',
        bg:     'var(--bai-color-warning-bg)',
        border: 'var(--bai-color-warning-border)',
        solid:  'var(--bai-color-warning-solid)',
      },
      info: {
        fg:     'var(--bai-color-info-fg)',
        bg:     'var(--bai-color-info-bg)',
        border: 'var(--bai-color-info-border)',
        solid:  'var(--bai-color-info-solid)',
      },
      bg:               semanticColor('bg'),
      surface:          semanticColor('surface'),
      'surface-muted':  semanticColor('surface-muted'),
      border:           semanticColor('border'),
      'border-strong':  semanticColor('border-strong'),
      text:             semanticColor('text'),
      'text-muted':     semanticColor('text-muted'),
      'text-subtle':    semanticColor('text-subtle'),
      'text-disabled':  semanticColor('text-disabled'),
      primary:          semanticColor('primary'),
      'primary-hover':  semanticColor('primary-hover'),
      'primary-active': semanticColor('primary-active'),
      'on-primary':     semanticColor('on-primary'),
      accent:           semanticColor('accent'),
      'accent-soft':    semanticColor('accent-soft'),
      link:             semanticColor('link'),
      'focus-ring':      semanticColor('focus-ring'),
      'focus-ring-soft': semanticColor('focus-ring-soft'),
    },
    fontFamily: {
      sans: ['var(--bai-font-family)'],
      mono: ['var(--bai-font-family-mono)'],
    },
    fontSize: {
      xs:   ['var(--bai-font-size-xs)',   { lineHeight: '1.5' }],
      sm:   ['var(--bai-font-size-sm)',   { lineHeight: '1.5' }],
      md:   ['var(--bai-font-size-md)',   { lineHeight: '1.5' }],
      base: ['var(--bai-font-size-base)', { lineHeight: '1.5' }],
      lg:   ['var(--bai-font-size-lg)',   { lineHeight: '1.4' }],
      xl:   ['var(--bai-font-size-xl)',   { lineHeight: '1.4' }],
      '2xl':['var(--bai-font-size-2xl)',  { lineHeight: '1.3' }],
      '3xl':['var(--bai-font-size-3xl)',  { lineHeight: '1.25' }],
    },
    borderRadius: {
      none:    '0',
      sm:      'var(--bai-radius-sm)',
      DEFAULT: 'var(--bai-radius-md)',
      md:      'var(--bai-radius-md)',
      lg:      'var(--bai-radius-lg)',
      full:    'var(--bai-radius-pill)',
    },
    boxShadow: {
      none: 'none',
      sm:   'var(--bai-shadow-sm)',
      DEFAULT: 'var(--bai-shadow-md)',
      md:   'var(--bai-shadow-md)',
      lg:   'var(--bai-shadow-lg)',
    },
    zIndex: {
      auto:     'auto',
      0:        '0',
      10:       '10',
      20:       '20',
      30:       '30',
      dropdown: 'var(--bai-z-dropdown)',
      sticky:   'var(--bai-z-sticky)',
      drawer:   'var(--bai-z-drawer)',
      modal:    'var(--bai-z-modal)',
      toast:    'var(--bai-z-toast)',
    },
    transitionDuration: {
      DEFAULT: 'var(--bai-motion-base)',
      fast:    'var(--bai-motion-fast)',
      base:    'var(--bai-motion-base)',
      slow:    'var(--bai-motion-slow)',
    },
    screens: {
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px',
    },
    extend: {
      keyframes: {
        'modal-in': {
          from: { opacity: '0', transform: 'translateY(6px) scale(0.98)' },
          to:   { opacity: '1', transform: 'translateY(0) scale(1)' },
        },
        'sheet-in': {
          from: { transform: 'translateY(100%)' },
          to:   { transform: 'translateY(0)' },
        },
        'fade-in': {
          from: { opacity: '0' },
          to:   { opacity: '1' },
        },
      },
      animation: {
        'modal-in':  'modal-in var(--bai-motion-base) ease both',
        'sheet-in':  'sheet-in var(--bai-motion-base) ease both',
        'fade-in':   'fade-in var(--bai-motion-fast) ease both',
      },
    },
  },
  plugins: [],
}
