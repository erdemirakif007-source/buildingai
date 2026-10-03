import { useState } from 'react'
import {
  AlertTriangle, FileText, Search, FolderOpen,
  Mic, Download, Calendar, ChevronDown,
} from 'lucide-react'

const MAIN_ACTIONS = [
  {
    id: 'guvenlik',
    label: 'GÜVENLİK',
    icon: AlertTriangle,
    iconClass: 'text-red-400',
    bgGrad: 'from-red-900/35 to-red-900/10',
    border: 'border-red-800/30',
    hoverShadow: 'hover:shadow-red-900/25',
  },
  {
    id: 'raporlar',
    label: 'RAPORLAR',
    icon: FileText,
    iconClass: 'text-orange-400',
    bgGrad: 'from-orange-900/40 to-orange-900/10',
    border: 'border-orange-600/40',
    hoverShadow: 'hover:shadow-orange-900/30',
    hasDropdown: true,
    defaultActive: true,
  },
  {
    id: 'analiz',
    label: 'ANALİZ',
    icon: Search,
    iconClass: 'text-sky-400',
    bgGrad: 'from-sky-900/30 to-sky-900/5',
    border: 'border-sky-800/20',
    hoverShadow: 'hover:shadow-sky-900/20',
    hasDropdown: true,
  },
  {
    id: 'arsiv',
    label: 'ARŞİV',
    icon: FolderOpen,
    iconClass: 'text-yellow-400',
    bgGrad: 'from-yellow-900/25 to-yellow-900/5',
    border: 'border-yellow-800/20',
    hoverShadow: 'hover:shadow-yellow-900/15',
  },
]

const SUB_ITEMS = [
  { id: 'gunluk',   label: 'Günlük Rapor',  icon: FileText  },
  { id: 'sesli',    label: 'Sesli Rapor',   icon: Mic       },
  { id: 'pdf',      label: 'PDF İndir',     icon: Download  },
  { id: 'haftalik', label: 'Haftalık Rapor', icon: Calendar },
]

export default function QuickActions() {
  const [subOpen, setSubOpen] = useState(true)
  const [active, setActive] = useState('raporlar')

  return (
    <div className="space-y-2.5 animate-fade-in" style={{ maxWidth: 860 }}>

      {/* ── 4 main action cards ── */}
      <div className="grid grid-cols-4 gap-3">
        {MAIN_ACTIONS.map(action => {
          const Icon = action.icon
          const isActive = active === action.id

          return (
            <button
              key={action.id}
              onClick={() => {
                setActive(action.id)
                if (action.id === 'raporlar') setSubOpen(v => !v)
              }}
              className={`
                flex flex-col items-center justify-center gap-2
                py-4 px-3 rounded-[14px] cursor-pointer
                bg-gradient-to-br ${action.bgGrad}
                border ${action.border}
                backdrop-blur-md
                transition-all duration-200
                hover:scale-[1.025] hover:shadow-lg ${action.hoverShadow}
                ${isActive
                  ? 'border-orange-500/55 shadow-lg shadow-orange-900/20'
                  : ''}
              `}
            >
              <Icon
                size={26}
                strokeWidth={1.7}
                className={isActive ? 'text-orange-400' : action.iconClass}
              />
              <span className={`
                flex items-center gap-1
                text-[10px] font-bold tracking-widest
                ${isActive ? 'text-orange-400' : 'text-gray-300'}
              `}>
                {action.label}
                {action.hasDropdown && (
                  <ChevronDown
                    size={9}
                    className={`transition-transform duration-200 ${
                      action.id === 'raporlar' && subOpen ? 'rotate-180' : ''
                    }`}
                  />
                )}
              </span>
            </button>
          )
        })}
      </div>

      {/* ── Raporlar sub-menu ── */}
      {subOpen && (
        <div className="grid grid-cols-4 gap-2.5 animate-fade-in">
          {SUB_ITEMS.map(item => {
            const Icon = item.icon
            return (
              <button
                key={item.id}
                className="
                  flex items-center justify-center gap-1.5
                  py-2.5 px-3
                  bg-[#080d1c]/80 border border-white/[0.07]
                  rounded-[10px]
                  text-[10.5px] font-semibold text-sky-400
                  hover:border-orange-500/30 hover:text-orange-300
                  hover:bg-orange-500/[0.05]
                  transition-all duration-150
                "
              >
                <Icon size={12} strokeWidth={2} />
                {item.label}
              </button>
            )
          })}
        </div>
      )}
    </div>
  )
}
