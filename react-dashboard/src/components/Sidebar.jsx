import { useState } from 'react'
import {
  Home, Camera, Wrench, FileText, Mic, Archive,
  TrendingUp, Package, Activity, FileDown, BarChart2,
  Menu, X, Crown,
} from 'lucide-react'

const NAV_ITEMS = [
  { id: 'home',        label: 'Ana Sayfa',         icon: Home },
  { id: 'kamera',      label: 'Kamera Analizi',     icon: Camera },
  { id: 'muhendislik', label: 'Mühendislik Paneli', icon: Wrench },
  { id: 'gunluk',      label: 'Günlük Rapor',       icon: FileText },
  { id: 'sesli',       label: 'Sesli Rapor',        icon: Mic },
  { id: 'arsiv',       label: 'Arşiv',              icon: Archive },
  { id: 'fiyat',       label: 'Fiyat Takibi',       icon: TrendingUp },
  { id: 'stok',        label: 'Stok Takibi',        icon: Package },
  { id: 'deprem',      label: 'Deprem Analizi',     icon: Activity },
  { id: 'pdf',         label: 'PDF İndir',          icon: FileDown },
  { id: 'haftalik',    label: 'Haftalık Rapor',     icon: BarChart2 },
]

function NavItem({ item, isActive, onClick }) {
  const Icon = item.icon
  return (
    <button
      onClick={onClick}
      className={`
        group flex items-center gap-2.5 w-full text-left
        px-3.5 py-[8px] text-[12px] font-medium
        border-l-[3px] transition-all duration-120 select-none
        ${isActive
          ? 'border-[#FF6200] bg-gradient-to-r from-orange-600/[0.14] to-transparent text-white'
          : 'border-transparent text-[#2a4260] hover:text-[#6a9abb] hover:bg-white/[0.025]'
        }
      `}
    >
      <Icon
        size={13}
        strokeWidth={isActive ? 2.2 : 1.8}
        className={`flex-shrink-0 transition-colors ${isActive ? 'text-[#FF6200]' : 'text-current'}`}
      />
      <span className="truncate leading-none">{item.label}</span>
    </button>
  )
}

export default function Sidebar({ active, setActive }) {
  const [mobileOpen, setMobileOpen] = useState(false)

  const content = (
    <div className="flex flex-col h-full overflow-y-auto pt-1.5 pb-2">
      {NAV_ITEMS.map(item => (
        <NavItem
          key={item.id}
          item={item}
          isActive={active === item.id}
          onClick={() => { setActive(item.id); setMobileOpen(false) }}
        />
      ))}

      {/* Spacer */}
      <div className="flex-1 min-h-[16px]" />

      {/* Upgrade CTA */}
      <div className="mx-2.5 mb-2">
        <button className="
          w-full p-2.5 text-left
          bg-gradient-to-br from-violet-900/[0.18] to-violet-800/[0.08]
          border border-violet-700/[0.22] rounded-xl
          hover:border-violet-500/40 transition-colors
        ">
          <div className="flex items-center gap-1.5 mb-0.5">
            <Crown size={10} className="text-violet-400" />
            <span className="text-[10.5px] font-semibold text-violet-300">Max'e Geç</span>
          </div>
          <p className="text-[9px] text-[#243648]">Çoklu şantiye & stok</p>
        </button>
      </div>
    </div>
  )

  return (
    <>
      {/* Mobile hamburger button */}
      <button
        className="md:hidden fixed top-[60px] left-3 z-50 p-2 bg-gray-900/90 rounded-lg border border-white/10"
        onClick={() => setMobileOpen(v => !v)}
      >
        {mobileOpen
          ? <X size={16} className="text-gray-300" />
          : <Menu size={16} className="text-gray-300" />}
      </button>

      {/* Mobile backdrop */}
      {mobileOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black/60 z-30"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar panel */}
      <aside className={`
        fixed md:relative top-0 left-0 h-full z-40
        w-[158px] flex-shrink-0
        bg-[rgba(5,8,16,0.96)]
        border-r border-white/[0.045]
        transition-transform duration-300 ease-out
        ${mobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `}>
        {content}
      </aside>
    </>
  )
}
