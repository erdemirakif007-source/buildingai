import { useState, useRef } from 'react'
import { Camera, Wrench, ArrowRight } from 'lucide-react'

export default function AIInputBar({ onSend }) {
  const [value, setValue] = useState('')
  const inputRef = useRef(null)

  const handleSend = () => {
    const trimmed = value.trim()
    if (!trimmed) return
    onSend?.(trimmed)
    setValue('')
    inputRef.current?.focus()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div
      className="relative animate-fade-in"
      style={{ maxWidth: 860, animationDelay: '0.08s' }}
    >
      {/* Gradient border layer */}
      <div className="
        absolute inset-0 rounded-[14px] p-px pointer-events-none
        bg-gradient-to-r
          from-teal-500/30 via-violet-500/20 to-teal-400/15
      " />

      {/* Inner container */}
      <div className="
        relative flex items-center gap-3
        bg-[#080d1a]/90 backdrop-blur-xl
        rounded-[14px] px-3 py-[10px]
      ">
        {/* Action icons */}
        <div className="flex gap-1.5 flex-shrink-0">
          <button className="
            w-[34px] h-[34px] rounded-[9px]
            bg-violet-500/20 border border-violet-500/20
            flex items-center justify-center
            hover:bg-violet-500/30 hover:border-violet-400/35
            transition-all duration-150
          ">
            <Camera size={15} className="text-violet-300" strokeWidth={1.8} />
          </button>

          <button className="
            w-[34px] h-[34px] rounded-[9px]
            bg-sky-500/18 border border-sky-500/18
            flex items-center justify-center
            hover:bg-sky-500/28 hover:border-sky-400/32
            transition-all duration-150
          ">
            <Wrench size={15} className="text-sky-300" strokeWidth={1.8} />
          </button>
        </div>

        {/* Input area */}
        <div className="flex-1 min-w-0">
          <p className="text-[8.5px] text-[#162436] font-bold tracking-[0.9px] uppercase mb-[3px] select-none">
            AI Asistan
          </p>
          <input
            ref={inputRef}
            value={value}
            onChange={e => setValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Soru sor, hesap seç veya saha fotoğrafı yükle..."
            className="
              w-full bg-transparent
              text-[12.5px] text-gray-200
              placeholder-[#1e3452]
              outline-none caret-[#FF6200]
            "
          />
        </div>

        {/* Send button */}
        <button
          onClick={handleSend}
          className="
            w-[34px] h-[34px] rounded-[10px] flex-shrink-0
            bg-gradient-to-br from-[#FF6200] to-orange-600
            flex items-center justify-center
            shadow-lg shadow-orange-600/30
            hover:shadow-orange-500/50 hover:scale-105
            transition-all duration-150
          "
        >
          <ArrowRight size={15} className="text-white" strokeWidth={2.5} />
        </button>
      </div>
    </div>
  )
}
