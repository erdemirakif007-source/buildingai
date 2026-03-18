/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'orange-prime': '#FF6200',
      },
      keyframes: {
        fadeInUp: {
          from: { opacity: '0', transform: 'translateY(8px)' },
          to:   { opacity: '1', transform: 'translateY(0)' },
        },
        blink: {
          '0%,100%': { opacity: '1' },
          '50%':      { opacity: '0.3' },
        },
      },
      animation: {
        'fade-in':   'fadeInUp 0.35s ease both',
        'blink-dot': 'blink 2s ease-in-out infinite',
      },
      boxShadow: {
        'glow-orange': '0 0 24px rgba(255,98,0,0.35)',
        'glow-teal':   '0 0 40px rgba(0,200,185,0.20)',
      },
    },
  },
  plugins: [],
}
