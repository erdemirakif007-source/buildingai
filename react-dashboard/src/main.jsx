import React from 'react'
import ReactDOM from 'react-dom/client'
import '@fontsource/plus-jakarta-sans/400.css'
import '@fontsource/plus-jakarta-sans/500.css'
import '@fontsource/plus-jakarta-sans/600.css'
import '@fontsource/plus-jakarta-sans/700.css'
import App from './App.jsx'
import { ToastProvider } from './ui/Toast.jsx'
import './index.css'

async function mount() {
  let Root = App
  if (import.meta.env.DEV && new URLSearchParams(window.location.search).get('ui') === '1') {
    const { default: UiPreview } = await import('./ui/UiPreview.jsx')
    Root = UiPreview
  }
  ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
      <ToastProvider>
        <Root />
      </ToastProvider>
    </React.StrictMode>
  )
}

mount()
