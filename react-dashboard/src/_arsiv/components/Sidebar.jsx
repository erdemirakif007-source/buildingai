import { useState } from 'react'
import {
  LayoutDashboard, Building2, Layers, FileText, Package,
  ShieldCheck, BarChart2, MapPin, Settings,
  Camera, Monitor, TrendingUp, Archive,
  Menu, X, Zap,
} from 'lucide-react'

const MAIN_ITEMS = [
  { id: 'home',        label: 'Ana Panel',        icon: LayoutDashboard },
  { id: 'santiye',     label: 'Şantiyerim',        icon: Building2,  badge: '3' },
  { id: 'metraj',      label: 'Metraj Yönetimi',   icon: Layers },
  { id: 'hakedis',     label: 'Hakediş',           icon: FileText },
  { id: 'stok',        label: 'Stok Takibi',       icon: Package },
  { id: 'isg',         label: 'ISG & Güvenlik',    icon: ShieldCheck },
  { id: 'raporlar',    label: 'Raporlar',          icon: BarChart2 },
  { id: 'saha',        label: 'Saha Kayıtları',    icon: MapPin },
  { id: 'ayarlar',     label: 'Ayarlar',           icon: Settings },
]

const AI_ITEMS = [
  { id: 'kamera',      label: 'Kamera Analizi',    icon: Camera,   aiTag: true },
  { id: 'muhendislik', label: 'Mühendislik',       icon: Monitor },
  { id: 'fiyat',       label: 'Fiyat Takibi',      icon: TrendingUp },
  { id: 'arsiv',       label: 'Arşiv',             icon: Archive },
]

function NavItem({ item, isActive, onClick }) {
  const Icon = item.icon
  return (
    <div className="px-2 py-[2px]">
      <div
        style={{
          borderRadius: 8,
          background: isActive ? '#ffffff' : 'transparent',
          transition: 'background 0.15s',
        }}
      >
        <button
          onClick={onClick}
          style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 10,
            padding: '11px 12px', background: 'none', border: 'none', cursor: 'pointer',
            textAlign: 'left', fontSize: 13, fontWeight: 500,
            color: isActive ? '#111827' : '#5a7a9a',
          }}
        >
          <Icon
            size={15}
            strokeWidth={isActive ? 2.2 : 1.7}
            style={{ flexShrink: 0, color: isActive ? '#FF6200' : 'currentColor' }}
          />
          <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {item.label}
          </span>
          {item.badge && (
            <span style={{ fontSize: 10, fontWeight: 600, background: '#1e3a5f',
              color: '#7ab3d4', padding: '2px 6px', borderRadius: 99 }}>
              {item.badge}
            </span>
          )}
          {item.aiTag && (
            <span style={{ fontSize: 9, fontWeight: 700, background: '#FF6200',
              color: 'white', padding: '2px 5px', borderRadius: 4 }}>
              AI
            </span>
          )}
        </button>
      </div>
    </div>
  )
}

export default function Sidebar({ active, setActive }) {
  const [mobileOpen, setMobileOpen] = useState(false)

  const handleClick = (id) => {
    setActive(id)
    setMobileOpen(false)
  }

  const content = (
    <div className="flex flex-col h-full overflow-y-auto pt-2 pb-2">

      {/* Main nav */}
      {MAIN_ITEMS.map(item => (
        <NavItem
          key={item.id}
          item={item}
          isActive={active === item.id}
          onClick={() => handleClick(item.id)}
        />
      ))}

      {/* AI section */}
      <div className="px-4 pt-4 pb-1">
        <span className="text-[10px] font-semibold tracking-widest text-[#2a4260] uppercase">
          AI Araçları
        </span>
      </div>
      {AI_ITEMS.map(item => (
        <NavItem
          key={item.id}
          item={item}
          isActive={active === item.id}
          onClick={() => handleClick(item.id)}
        />
      ))}

      <div className="flex-1 min-h-[16px]" />

      {/* CTA */}
      <div className="mx-2 mb-2">
        <button className="
          w-full p-3 text-left
          bg-gradient-to-br from-[#1a1a2e] to-[#16213e]
          border border-[#FF6200]/30 rounded-xl
          hover:border-[#FF6200]/60 transition-colors
        ">
          <div className="flex items-center gap-1.5 mb-0.5">
            <Zap size={11} className="text-[#FF6200]" />
            <span className="text-[11px] font-semibold text-white">Enterprise'a Geç</span>
          </div>
          <p className="text-[10px] text-[#3a5570]">Sınırsız şantiye, çoklu ekip</p>
        </button>
      </div>
    </div>
  )

  return (
    <>
      <button
        className="md:hidden fixed top-[60px] left-3 z-50 p-2 bg-gray-900/90 rounded-lg border border-white/10"
        onClick={() => setMobileOpen(v => !v)}
      >
        {mobileOpen
          ? <X size={16} className="text-gray-300" />
          : <Menu size={16} className="text-gray-300" />}
      </button>

      {mobileOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black/60 z-30"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <aside className={`
        fixed md:relative top-0 left-0 h-full z-40
        w-[200px] flex-shrink-0
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
