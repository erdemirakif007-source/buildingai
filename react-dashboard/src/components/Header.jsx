import { useState, useRef, useEffect } from 'react'
import { ChevronDown, Cloud, UserCircle2, Building2 } from 'lucide-react'

const CITIES = [
  'Adana','Ankara','Antalya','Bursa','Diyarbakır','Erzurum',
  'Eskişehir','Gaziantep','İstanbul','İzmir','Kayseri',
  'Konya','Malatya','Mersin','Samsun','Sivas','Trabzon',
]

export default function Header() {
  const [city, setCity] = useState('Sivas')
  const [dropOpen, setDropOpen] = useState(false)
  const dropRef = useRef(null)

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => {
      if (dropRef.current && !dropRef.current.contains(e.target)) setDropOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <header className="
      h-[50px] flex items-center justify-between px-5
      bg-[#04070e]/96 border-b border-white/[0.055]
      backdrop-blur-xl flex-shrink-0 z-20
    ">
      {/* ── Logo ── */}
      <div className="flex items-center gap-2.5 select-none">
        <div className="
          w-[34px] h-[34px] rounded-xl
          bg-gradient-to-br from-orange-500 to-red-600
          flex items-center justify-center
          shadow-lg shadow-orange-600/30
        ">
          <Building2 size={17} className="text-white" strokeWidth={2.2} />
        </div>
        <span className="text-[15px] font-bold tracking-tight text-white">
          BuildingAI<span className="text-[#FF6200]">Pro</span>
        </span>
      </div>

      {/* ── Right controls ── */}
      <div className="flex items-center gap-2.5">

        {/* City dropdown */}
        <div className="relative" ref={dropRef}>
          <button
            onClick={() => setDropOpen(v => !v)}
            className="
              flex items-center gap-1.5 px-3 py-1.5
              bg-white/[0.055] border border-white/[0.10]
              rounded-lg text-[12.5px] font-semibold text-gray-200
              hover:bg-white/[0.09] hover:border-white/[0.18]
              transition-all duration-150 select-none
            "
          >
            {city}
            <ChevronDown size={11} className={`transition-transform duration-200 ${dropOpen ? 'rotate-180' : ''}`} />
          </button>

          {dropOpen && (
            <div className="
              absolute right-0 top-full mt-1.5 z-50
              bg-[#090e1c] border border-white/[0.09]
              rounded-xl shadow-2xl py-1
              max-h-56 overflow-y-auto min-w-[130px]
              animate-fade-in
            ">
              {CITIES.map(c => (
                <button
                  key={c}
                  onClick={() => { setCity(c); setDropOpen(false) }}
                  className={`
                    w-full text-left px-3.5 py-2 text-[12px] transition-colors
                    ${c === city
                      ? 'text-[#FF6200] bg-orange-500/10'
                      : 'text-gray-400 hover:text-gray-100 hover:bg-white/[0.06]'}
                  `}
                >
                  {c}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Weather widget */}
        <div className="
          flex items-center gap-2
          bg-white/[0.04] border border-white/[0.07]
          rounded-lg px-3 py-1.5
        ">
          <Cloud size={14} className="text-sky-400 flex-shrink-0" />
          <span className="text-[10px] text-sky-600 uppercase tracking-wider font-semibold hidden sm:block">
            PARÇALI BULUTLU
          </span>
          <span className="text-[13px] font-bold text-gray-100">6°C</span>
        </div>

        {/* Theme toggle */}
        <button className="
          relative w-11 h-[22px]
          bg-[#0e1526] border border-white/[0.09]
          rounded-full transition-colors flex-shrink-0
          hover:border-white/20
        ">
          <span className="
            absolute top-[3px] left-[3px]
            w-4 h-4 rounded-full
            bg-gray-600
          " />
        </button>

        {/* Avatar */}
        <button className="
          w-[32px] h-[32px] rounded-full
          bg-[#0d1b2e] border border-sky-900/40
          flex items-center justify-content-center
          hover:border-[#FF6200]/50 transition-colors
          flex-shrink-0 flex items-center justify-center
        ">
          <UserCircle2 size={18} className="text-sky-700" />
        </button>
      </div>
    </header>
  )
}
