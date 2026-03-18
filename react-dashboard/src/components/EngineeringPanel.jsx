import { useState } from 'react'

/* ── Small stat chip ── */
function StatChip({ emoji, label, value, variant = 'gray', progress }) {
  const variants = {
    orange: 'bg-orange-500/10 border-orange-500/24 text-orange-400',
    blue:   'bg-sky-500/10  border-sky-500/24  text-sky-400',
    gray:   'bg-white/[0.04] border-white/[0.08] text-gray-400',
  }

  return (
    <div className={`
      flex items-center gap-2 px-3 py-[9px]
      border rounded-xl
      text-[10.5px] font-semibold
      cursor-default select-none
      hover:scale-[1.04] transition-transform duration-150
      ${variants[variant]}
    `}>
      <span className="text-[13px] leading-none">{emoji}</span>
      <span className="text-gray-500">{label}:</span>
      <span>{value}</span>

      {/* Optional progress bar */}
      {progress !== undefined && (
        <div className="w-16 h-[3px] bg-white/[0.08] rounded-full overflow-hidden ml-1">
          <div
            className="h-full bg-gradient-to-r from-sky-500 to-orange-500 rounded-full"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  )
}

/* ── Result body (shown after AI responds) ── */
export default function EngineeringPanel({ resultHtml }) {
  return (
    <div
      className="relative animate-fade-in"
      style={{ maxWidth: 860, animationDelay: '0.12s' }}
    >
      {/* Gradient border */}
      <div className="
        absolute inset-0 rounded-[14px] p-px pointer-events-none
        bg-gradient-to-br from-teal-500/20 via-teal-400/10 to-transparent
      " />

      <div className="
        relative glass-card rounded-[14px]
        px-5 py-4
        flex flex-col gap-3
      ">
        {/* Header row */}
        <div className="flex items-center gap-2.5">
          {/* Live dot */}
          <span className="
            w-[7px] h-[7px] rounded-full flex-shrink-0
            bg-green-500
            shadow-[0_0_10px_rgba(34,197,94,0.75)]
            animate-blink-dot
          " />

          <h2 className="text-[14px] font-semibold text-gray-100">
            🏗️ Mühendislik Paneli Hazır
          </h2>

          {/* LIVE badge */}
          <span className="
            text-[8px] font-bold text-green-400 tracking-wider
            bg-green-500/[0.09] border border-green-500/[0.20]
            rounded px-1.5 py-[2px]
          ">
            LIVE
          </span>
        </div>

        {/* Body text or AI response */}
        <div
          className="text-[12px] text-[#5a8aaa] leading-[1.80]"
          dangerouslySetInnerHTML={
            resultHtml
              ? { __html: resultHtml }
              : {
                  __html:
                    'Kamera analizi, mühendislik hesapları ve raporlama araçlarına hazırsınız. ' +
                    'Soru sorabilir, fotoğraf yükleyebilir veya bir hesaplama başlatabilirsiniz.',
                }
          }
        />

        {/* Stat chips */}
        <div className="flex gap-2.5 flex-wrap">
          <StatChip emoji="🔥" label="Aktif Kamera"     value="12"  variant="orange" />
          <StatChip emoji="📊" label="Günlük İlerleme"  value="%87" variant="blue" progress={87} />
          <StatChip emoji="⚠️"  label="Güvenlik Uyarısı" value="0"  variant="gray" />
        </div>
      </div>
    </div>
  )
}
