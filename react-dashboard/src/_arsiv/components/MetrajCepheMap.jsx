// MetrajCepheMap.jsx — Görsel Cephe İlerleme Haritası
// Dynamic building: floor count + per-floor shape (widthFactor, xOffsetFactor)
import React, { useState, useEffect, useMemo } from "react";

const T = {
  brand:       "var(--brand-orange, #FF6B2C)",
  brandHover:  "var(--brand-orange-hover, #E85B1E)",
  brandSoft:   "var(--brand-orange-soft, #FFF2EB)",
  brandBorder: "var(--brand-orange-border, #FFD9C2)",
  success:     "var(--success, #16A34A)",
  warning:     "var(--warning, #D97706)",
  bgCard:      "var(--bg-card, #FFFFFF)",
  bgCardAlt:   "var(--bg-card-alt, #FAFBFC)",
  bgSubtle:    "var(--bg-subtle, #F1F3F5)",
  border:      "var(--border-subtle, #EEF0F3)",
  borderD:     "var(--border-default, #E5E7EB)",
  textPri:     "var(--text-primary, #0F172A)",
  textSec:     "var(--text-secondary, #475569)",
  textTer:     "var(--text-tertiary, #94A3B8)",
  fontMono:    "var(--font-mono, ui-monospace, 'JetBrains Mono', monospace)",
  shadowSm:    "var(--shadow-sm, 0 1px 2px rgba(15,23,42,.04))",
};

const STYLE_ID = "mcm-styles";
function ensureStyles() {
  if (typeof document === "undefined" || document.getElementById(STYLE_ID)) return;
  const s = document.createElement("style");
  s.id = STYLE_ID;
  s.textContent = `
    @keyframes mcm-pulse { 0%,100%{opacity:.4} 50%{opacity:0} }
    .mcm-card { background:${T.bgCard}; border:1px solid ${T.border}; border-radius:12px; box-shadow:${T.shadowSm}; }
    .mcm-btn  { display:inline-flex; align-items:center; gap:6px; height:30px; padding:0 10px;
      border-radius:8px; border:1px solid ${T.borderD}; background:${T.bgCard}; color:${T.textPri};
      font:500 12px/1 inherit; cursor:pointer; transition:all .12s ease; font-family:inherit; }
    .mcm-btn:hover { background:${T.bgSubtle}; }
    .mcm-btn-ghost { border:0; background:transparent; color:${T.textSec}; }
    .mcm-btn-ghost:hover { background:${T.bgSubtle}; color:${T.textPri}; }
  `;
  document.head.appendChild(s);
}

const Icon = ({ name, size = 14, ...rest }) => {
  const paths = {
    building:     <><rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/></>,
    layers:       <><path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/><path d="M3 18l9 5 9-5"/></>,
    chevronRight: <><polyline points="9 6 15 12 9 18"/></>,
    info:         <><circle cx="12" cy="12" r="9"/><path d="M12 8v.5M12 11v5"/></>,
    plus:         <><path d="M12 5v14M5 12h14"/></>,
    expand:       <><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></>,
    moreH:        <><circle cx="6" cy="12" r="1.5" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.5" fill="currentColor" stroke="none"/><circle cx="18" cy="12" r="1.5" fill="currentColor" stroke="none"/></>,
    cube:         <><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></>,
  };
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size}
      viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" {...rest}>
      {paths[name]}
    </svg>
  );
};

const Progress = ({ value = 0, color = T.brand, height = 5 }) => (
  <div style={{ width:"100%", height, background:T.bgSubtle, borderRadius:999, overflow:"hidden" }}>
    <div style={{
      width:`${Math.min(100, Math.max(0, value))}%`, height:"100%",
      background:color, borderRadius:999, transition:"width .4s ease"
    }}/>
  </div>
);

const Donut = ({ value = 0, size = 34, stroke = 4, color = T.brand }) => {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const off = c - (Math.min(100, Math.max(0, value)) / 100) * c;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={T.bgSubtle} strokeWidth={stroke}/>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth={stroke}
        strokeDasharray={c} strokeDashoffset={off} strokeLinecap="round"
        transform={`rotate(-90 ${size/2} ${size/2})`}/>
      <text x={size/2} y={size/2+3} textAnchor="middle" fontSize={size*0.28}
        fontWeight="700" fill={T.textPri}>{value.toFixed(0)}%</text>
    </svg>
  );
};

// ── Dynamic Building SVG ──────────────────────────────────────────────────────
// Each floor can have optional widthFactor (0-1, default 1) and
// xOffsetFactor (0-1, default 0 = left) to create stepped/tower/custom shapes.
// widthFactor=0.6, xOffsetFactor=0.2 centers a narrower floor, creating tower effect.
const BuildingSvg = ({ floors, selectedId, onSelect }) => {
  const SVG_W = 200;
  const FLOOR_H = 48;
  const ROOF_H  = 24;
  const GROUND_H = 28;
  const ANTENNA_H = 20;
  const MARGIN = 14; // left/right padding inside SVG

  const wallFloors = floors.filter(f => f.id !== "roof");
  const totalH = ANTENNA_H + ROOF_H + wallFloors.length * FLOOR_H + GROUND_H;
  const wallTop = ANTENNA_H + ROOF_H;
  const groundY = wallTop + wallFloors.length * FLOOR_H;

  // Compute per-floor rect: x1, x2 within [MARGIN, SVG_W - MARGIN]
  const innerW = SVG_W - MARGIN * 2;
  const floorRects = wallFloors.map(f => {
    const wf = Math.min(1, Math.max(0.2, f.widthFactor ?? 1));
    const xof = Math.min(1 - wf, Math.max(0, f.xOffsetFactor ?? 0));
    const x1 = MARGIN + xof * innerW;
    const x2 = x1 + wf * innerW;
    return { x1, x2, w: x2 - x1 };
  });

  // Building silhouette outline path (outermost contour, bottom to top, then back down)
  // Used just for visual shadow — actual floor rects drawn individually
  const maxX1 = Math.min(...floorRects.map(r => r.x1));
  const maxX2 = Math.max(...floorRects.map(r => r.x2));

  return (
    <svg width={SVG_W} height={totalH} viewBox={`0 0 ${SVG_W} ${totalH}`}
      style={{ display:"block" }}>
      <defs>
        <linearGradient id="mcm-wall" x1="0" x2="1" y1="0" y2="0">
          <stop offset="0%" stopColor="#FFFFFF"/>
          <stop offset="70%" stopColor="#F4F5F7"/>
          <stop offset="100%" stopColor="#E5E7EB"/>
        </linearGradient>
        <linearGradient id="mcm-wall-active" x1="0" x2="1" y1="0" y2="0">
          <stop offset="0%" stopColor="#FFF7F1"/>
          <stop offset="70%" stopColor="#FFEEDD"/>
          <stop offset="100%" stopColor="#FFD9C2"/>
        </linearGradient>
        <linearGradient id="mcm-roof" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor="#475569"/>
          <stop offset="100%" stopColor="#1E293B"/>
        </linearGradient>
        <linearGradient id="mcm-win-lit" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor="#FF6B2C"/>
          <stop offset="100%" stopColor="#E85B1E"/>
        </linearGradient>
        <pattern id="mcm-grid" width="8" height="8" patternUnits="userSpaceOnUse">
          <path d="M 8 0 L 0 0 0 8" stroke="#E5E7EB" strokeWidth=".4" fill="none"/>
        </pattern>
      </defs>

      <rect x="0" y="0" width={SVG_W} height={totalH} fill="url(#mcm-grid)" opacity=".5"/>

      {/* Ground shadow */}
      <ellipse cx={SVG_W/2} cy={groundY+2} rx={(maxX2 - maxX1) * 0.48} ry="3"
        fill="#0F172A" opacity=".07"/>

      {/* Antenna */}
      <line x1={SVG_W/2} y1="0" x2={SVG_W/2} y2={ANTENNA_H}
        stroke="#334155" strokeWidth="1.5" strokeLinecap="round"/>
      <circle cx={SVG_W/2} cy="3" r="2.5" fill="#FF6B2C"/>
      <circle cx={SVG_W/2} cy="3" r="5" fill="#FF6B2C" opacity=".2">
        <animate attributeName="r" values="3;7;3" dur="2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values=".4;0;.4" dur="2s" repeatCount="indefinite"/>
      </circle>

      {/* Roof — spans full building width */}
      {wallFloors.length > 0 && (() => {
        const topFloor = floorRects[0];
        return (
          <>
            <polygon
              points={`${topFloor.x1},${wallTop} ${topFloor.x2},${wallTop} ${topFloor.x2 - 12},${ANTENNA_H} ${topFloor.x1 + 12},${ANTENNA_H}`}
              fill="url(#mcm-roof)"/>
            <rect x={topFloor.x1} y={wallTop} width={topFloor.w} height="4" fill="#0F172A"/>
          </>
        );
      })()}

      {/* Floors */}
      {wallFloors.map((f, i) => {
        const { x1, x2, w } = floorRects[i];
        const y = wallTop + 4 + i * FLOOR_H;
        const isActive   = f.id === selectedId;
        const isComplete = f.status === "tamam";
        const isInProgress = f.status === "devam";
        const isGround = f.id === "zemin" || i === wallFloors.length - 1;

        const units = Math.max(f.units, 1);
        const winGap = 4;
        const winW = (w - 12 - winGap * (units - 1)) / units;
        const winH = FLOOR_H - 20;
        const winY = y + 8;

        // Stepped edge: draw connecting rect to next (wider) floor below
        const nextRect = floorRects[i + 1];
        const hasStep = nextRect && (nextRect.x1 < x1 || nextRect.x2 > x2);

        return (
          <g key={f.id} style={{ cursor:"pointer" }} onClick={() => onSelect(f.id)}>
            {/* Step connectors to wider floor below */}
            {hasStep && (
              <rect x={Math.min(x1, nextRect.x1)} y={y + FLOOR_H - 2}
                width={Math.max(x2, nextRect.x2) - Math.min(x1, nextRect.x1)}
                height={4} fill="#D1D5DB" opacity=".5"/>
            )}

            {/* Floor body */}
            <rect x={x1} y={y} width={w} height={FLOOR_H}
              fill={isActive ? "url(#mcm-wall-active)" : "url(#mcm-wall)"}
              stroke={isActive ? "#FF6B2C" : isComplete ? "#86EFAC" : "#D1D5DB"}
              strokeWidth={isActive ? 1.5 : 1}/>

            {isComplete && <rect x={x1} y={y} width={w} height={FLOOR_H} fill="#16A34A" opacity=".08"/>}
            {f.pct > 0 && f.pct < 100 && (
              <rect x={x1} y={y + FLOOR_H - (FLOOR_H * f.pct) / 100}
                width={w} height={(FLOOR_H * f.pct) / 100} fill="#FF6B2C" opacity=".12"/>
            )}

            {/* Windows */}
            {[...Array(units)].map((_, u) => {
              const wx = x1 + 6 + u * (winW + winGap);
              const ud = f.units_detail?.[u];
              const uPct = ud?.pct ?? (isComplete ? 100 : 0);
              const lit = isComplete || uPct >= 50;
              const partial = !lit && uPct > 0;
              return (
                <g key={u}>
                  <rect x={wx} y={winY} width={winW} height={winH} rx="1"
                    fill={lit ? "url(#mcm-win-lit)" : isActive ? "#FFF2EB" : "#CBD5E1"}
                    stroke={lit ? "#E85B1E" : isActive ? "#FFD9C2" : "#94A3B8"}
                    strokeWidth=".5" opacity={lit ? 1 : isActive ? 1 : .7}/>
                  {partial && (
                    <rect x={wx} y={winY + winH - winH*(uPct/100)} width={winW} height={winH*(uPct/100)}
                      fill="#FF6B2C" opacity=".55"/>
                  )}
                  <line x1={wx + winW/2} y1={winY+1.5} x2={wx + winW/2} y2={winY+winH-1.5}
                    stroke={lit?"#FFF":"#94A3B8"} strokeWidth=".4" opacity=".6"/>
                  <line x1={wx+1.5} y1={winY+winH/2} x2={wx+winW-1.5} y2={winY+winH/2}
                    stroke={lit?"#FFF":"#94A3B8"} strokeWidth=".4" opacity=".6"/>
                </g>
              );
            })}

            {/* Floor separator */}
            {i < wallFloors.length - 1 && !hasStep && (
              <line x1={x1} y1={y+FLOOR_H} x2={x2} y2={y+FLOOR_H} stroke="#94A3B8" strokeWidth=".4"/>
            )}

            {/* Active indicator bar */}
            {isActive && <rect x={x1-6} y={y+3} width="3" height={FLOOR_H-6} rx="1.5" fill="#FF6B2C"/>}
            {isActive && (
              <g>
                <line x1={x2} y1={y+FLOOR_H/2} x2={x2+5} y2={y+FLOOR_H/2} stroke="#FF6B2C" strokeWidth="1.2"/>
                <circle cx={x2+6} cy={y+FLOOR_H/2} r="1.5" fill="#FF6B2C"/>
              </g>
            )}

            {/* Status badge */}
            {isComplete && (
              <g>
                <circle cx={x2-8} cy={y+8} r="4.5" fill="#16A34A"/>
                <path d={`M ${x2-10} ${y+8} L ${x2-8.5} ${y+9.5} L ${x2-5.5} ${y+6.5}`}
                  stroke="#fff" strokeWidth="1.2" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
              </g>
            )}
            {isInProgress && (
              <g>
                <circle cx={x2-8} cy={y+8} r="4.5" fill="#D97706"/>
                <circle cx={x2-8} cy={y+8} r="6.5" fill="#D97706" opacity=".25">
                  <animate attributeName="r" values="4.5;8;4.5" dur="1.8s" repeatCount="indefinite"/>
                  <animate attributeName="opacity" values=".4;0;.4" dur="1.8s" repeatCount="indefinite"/>
                </circle>
              </g>
            )}

            {/* Ground floor door */}
            {isGround && (
              <g>
                <rect x={SVG_W/2-8} y={y+FLOOR_H-17} width="16" height="17" fill="#1E293B" stroke="#0F172A" strokeWidth=".5"/>
                <line x1={SVG_W/2} y1={y+FLOOR_H-15} x2={SVG_W/2} y2={y+FLOOR_H-2} stroke="#475569" strokeWidth=".5"/>
                <circle cx={SVG_W/2+5} cy={y+FLOOR_H-9} r=".9" fill="#FF6B2C"/>
                <rect x={SVG_W/2-11} y={y+FLOOR_H-21} width="22" height="4" fill="#FF6B2C" rx=".5"/>
              </g>
            )}
          </g>
        );
      })}

      {/* Ground */}
      <line x1="0" y1={groundY} x2={SVG_W} y2={groundY} stroke="#94A3B8" strokeWidth=".8"/>
      <rect x="0" y={groundY} width={SVG_W} height={GROUND_H} fill="#F1F3F5"/>
      {[1,2,3,4,5].map(i => (
        <line key={i} x1={(i*SVG_W)/6} y1={groundY+4} x2={(i*SVG_W)/6} y2={groundY+GROUND_H}
          stroke="#CBD5E1" strokeWidth=".5"/>
      ))}
      <text x="6" y={groundY+10} fontSize="7" fill="#94A3B8" letterSpacing=".08em">±0.00</text>
      <text x={SVG_W-6} y={groundY+10} fontSize="7" fill="#94A3B8" letterSpacing=".08em" textAnchor="end">N →</text>
    </svg>
  );
};

// ── Floor row ─────────────────────────────────────────────────────────────────
const STATUS_META = {
  tamam:  { label: "Tamamlandı",   dot: T.success, text: T.success },
  devam:  { label: "Devam ediyor", dot: T.warning, text: T.warning },
  planli: { label: "Planlı",       dot: T.textTer, text: T.textTer },
};

const FloorRow = ({ floor, active, onClick }) => {
  const s = STATUS_META[floor.status] || STATUS_META.planli;
  return (
    <button onClick={onClick} style={{
      display:"grid", gridTemplateColumns:"26px 1fr 64px 36px",
      alignItems:"center", gap:10, padding:"10px 14px",
      background: active ? T.brandSoft : "transparent",
      border:0, borderLeft: active ? `2px solid ${T.brand}` : "2px solid transparent",
      borderBottom:`1px solid ${T.border}`,
      cursor:"pointer", textAlign:"left", fontFamily:"inherit", width:"100%"
    }}>
      <span style={{
        width:22, height:22, borderRadius:5,
        background: active ? T.brand : T.bgSubtle,
        color: active ? "#fff" : T.textTer,
        display:"grid", placeItems:"center",
        fontSize:9.5, fontWeight:700, fontFamily:T.fontMono
      }}>{floor.short}</span>
      <div style={{ minWidth:0 }}>
        <div style={{ fontSize:12.5, fontWeight:600, color:T.textPri }}>{floor.label}</div>
        <div style={{ fontSize:10.5, color:s.text, fontWeight:500,
          display:"flex", alignItems:"center", gap:5, marginTop:1 }}>
          <span style={{ width:6, height:6, borderRadius:"50%", background:s.dot, display:"inline-block" }}/>
          {s.label}
          {floor.units > 0 && <span style={{ color:T.textTer }}>· {floor.units} daire</span>}
        </div>
      </div>
      <div style={{ display:"flex", flexDirection:"column", gap:3 }}>
        <Progress value={floor.pct} height={4} color={
          floor.status==="tamam" ? T.success :
          floor.status==="devam" ? T.brand : T.textTer
        }/>
        <div style={{ fontSize:10, color:T.textTer, textAlign:"right", fontFamily:T.fontMono }}>
          %{floor.pct}
        </div>
      </div>
      <Icon name="chevronRight" size={12} style={{ color: active ? T.brand : T.textTer }}/>
    </button>
  );
};

// ── Main component ────────────────────────────────────────────────────────────
export default function MetrajCepheMap({
  blocks = [],
  initialBlockId,
  floorsByBlock = {},
  projectName = "",
  onFloorSelect,
  onShow3D,
  onAddFloor,
}) {
  useEffect(ensureStyles, []);

  const [blockId, setBlockId] = useState(
    initialBlockId || blocks.find(b => !b.disabled)?.id || blocks[0]?.id
  );
  const floors = floorsByBlock[blockId] || [];

  const defaultSelected =
    floors.find(f => f.status === "devam")?.id ||
    floors.find(f => f.id !== "roof")?.id || null;
  const [selectedId, setSelectedId] = useState(defaultSelected);

  useEffect(() => {
    const fs = floorsByBlock[blockId] || [];
    setSelectedId(
      fs.find(f => f.status === "devam")?.id ||
      fs.find(f => f.id !== "roof")?.id || null
    );
  }, [blockId, floorsByBlock]);

  const handleSelect = (id) => {
    setSelectedId(id);
    const f = floors.find(x => x.id === id);
    if (f) onFloorSelect?.(f, blockId);
  };

  const selected = floors.find(f => f.id === selectedId);
  const counts = useMemo(() => ({
    tamam:  floors.filter(f => f.status === "tamam").length,
    devam:  floors.filter(f => f.status === "devam").length,
    planli: floors.filter(f => f.status === "planli" && f.id !== "roof").length,
  }), [floors]);
  const totalPct = useMemo(() => {
    const ws = floors.filter(f => f.id !== "roof");
    if (!ws.length) return 0;
    return ws.reduce((s, f) => s + f.pct, 0) / ws.length;
  }, [floors]);

  return (
    <div className="mcm-card" style={{ padding:0, overflow:"hidden", display:"flex", flexDirection:"column" }}>

      {/* Header */}
      <div style={{ padding:"16px 20px 14px", borderBottom:`1px solid ${T.border}` }}>
        <div style={{ display:"flex", alignItems:"flex-start", justifyContent:"space-between", gap:12, marginBottom:12 }}>
          <div>
            <div style={{ display:"flex", alignItems:"center", gap:8 }}>
              <h2 style={{ margin:0, fontSize:15, fontWeight:600, letterSpacing:"-0.01em" }}>İlerleme Haritası</h2>
              <span style={{
                display:"inline-flex", alignItems:"center", gap:6,
                height:22, padding:"0 8px", borderRadius:999,
                fontSize:11, fontWeight:500,
                background:T.brandSoft, color:T.brand, border:`1px solid ${T.brandBorder}`
              }}>
                <span style={{
                  width:6, height:6, borderRadius:"50%", background:"#DC2626",
                  boxShadow:"0 0 0 0 rgba(220,38,38,.6)", animation:"mcm-pulse 2s infinite"
                }}/>
                Canlı
              </span>
            </div>
            <div style={{ fontSize:12, color:T.textTer, marginTop:3 }}>
              Kat ve daire bazında imalat tamamlanması{projectName && ` · ${projectName}`}
            </div>
          </div>
          <div style={{ display:"flex", gap:6 }}>
            {onShow3D && (
              <button className="mcm-btn" onClick={onShow3D}
                style={{ background:"#0F172A", color:"#94A3B8", borderColor:"#334155" }}
                onMouseEnter={e => { e.currentTarget.style.background="#1E293B"; e.currentTarget.style.color="#FF6B2C"; }}
                onMouseLeave={e => { e.currentTarget.style.background="#0F172A"; e.currentTarget.style.color="#94A3B8"; }}>
                <Icon name="cube" size={12}/> 3D BIM
              </button>
            )}
            <button className="mcm-btn mcm-btn-ghost" style={{ width:30, padding:0 }}>
              <Icon name="moreH" size={14}/>
            </button>
          </div>
        </div>

        {/* Block selector + summary */}
        <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between", gap:10 }}>
          <div style={{
            display:"inline-flex", padding:3, gap:2,
            background:T.bgSubtle, borderRadius:7, border:`1px solid ${T.border}`
          }}>
            {blocks.map(b => (
              <button key={b.id}
                onClick={() => !b.disabled && setBlockId(b.id)}
                disabled={b.disabled}
                style={{
                  display:"flex", alignItems:"center", gap:6,
                  padding:"5px 11px", borderRadius:5, border:0,
                  fontSize:11.5, fontWeight:600, fontFamily:"inherit",
                  cursor:b.disabled?"not-allowed":"pointer",
                  background: blockId===b.id ? T.bgCard : "transparent",
                  color: b.disabled ? T.textTer : blockId===b.id ? T.textPri : T.textSec,
                  boxShadow: blockId===b.id ? T.shadowSm : "none",
                  opacity: b.disabled ? .55 : 1
                }}>
                <Icon name="building" size={11}/>
                {b.label}
                {b.count != null && (
                  <span style={{
                    fontSize:9.5, padding:"0 5px", borderRadius:3,
                    background: blockId===b.id ? T.brandSoft : T.bgCard,
                    color: blockId===b.id ? T.brand : T.textTer,
                    fontFamily:T.fontMono, fontWeight:700, border:`1px solid ${T.border}`
                  }}>{b.count}</span>
                )}
              </button>
            ))}
          </div>
          <div style={{ display:"flex", alignItems:"center", gap:10 }}>
            <div style={{ textAlign:"right" }}>
              <div style={{ fontSize:9.5, color:T.textTer, letterSpacing:"0.06em",
                textTransform:"uppercase", fontWeight:600 }}>Blok Σ</div>
              <div style={{ fontSize:14, fontWeight:700, color:T.brand, fontFamily:T.fontMono }}>
                %{totalPct.toFixed(1)}
              </div>
            </div>
            <Donut value={totalPct} size={36} stroke={4} color={T.brand}/>
          </div>
        </div>
      </div>

      {/* Main: building + floor list */}
      <div style={{ display:"grid", gridTemplateColumns:"minmax(0,230px) 1fr", flex:1 }}>
        <div style={{
          background:"linear-gradient(180deg,#FAFBFC 0%,#F1F3F5 60%,#E9ECEF 100%)",
          borderRight:`1px solid ${T.border}`, padding:"16px 8px 0",
          display:"flex", justifyContent:"center", alignItems:"flex-start",
          position:"relative", overflowX:"hidden"
        }}>
          {/* Height scale */}
          <div style={{
            position:"absolute", left:6, top:24, bottom:14,
            display:"flex", flexDirection:"column", justifyContent:"space-between",
            fontSize:7.5, color:T.textTer, fontFamily:T.fontMono,
            letterSpacing:".05em", textAlign:"right",
            paddingRight:4, borderRight:"1px dashed #CBD5E1"
          }}>
            {floors.filter(f=>f.id!=="roof").slice(0,4).map((_, i) => (
              <span key={i}>+{(floors.filter(f=>f.id!=="roof").length - i) * 3}m</span>
            ))}
            <span>±0</span>
          </div>
          <BuildingSvg floors={floors} selectedId={selectedId} onSelect={handleSelect}/>
        </div>

        <div style={{ display:"flex", flexDirection:"column", minWidth:0 }}>
          <div style={{
            padding:"8px 14px", background:T.bgCardAlt,
            borderBottom:`1px solid ${T.border}`,
            fontSize:9.5, color:T.textTer, letterSpacing:".08em",
            textTransform:"uppercase", fontWeight:600,
            display:"grid", gridTemplateColumns:"26px 1fr 64px 36px", gap:10, alignItems:"center"
          }}>
            <span>Kat</span><span>Durum</span>
            <span style={{ textAlign:"right" }}>İlerleme</span><span/>
          </div>
          {floors.length === 0 ? (
            <div style={{ padding:"40px 20px", textAlign:"center", color:T.textTer,
              display:"flex", flexDirection:"column", alignItems:"center", gap:8 }}>
              <Icon name="building" size={22} style={{ color:T.textTer }}/>
              <div style={{ fontSize:13 }}>Bu blokta henüz iş kalemi yok</div>
              {onAddFloor && (
                <button className="mcm-btn" style={{ marginTop:6 }} onClick={onAddFloor}>
                  <Icon name="plus" size={11}/> Kat ekle
                </button>
              )}
            </div>
          ) : (
            floors.map(f => (
              <FloorRow key={f.id} floor={f} active={f.id===selectedId}
                onClick={() => handleSelect(f.id)}/>
            ))
          )}
        </div>
      </div>

      {/* Footer: selected floor breakdown */}
      {selected && selected.id !== "roof" && (
        <div style={{ padding:"14px 18px 16px", borderTop:`1px solid ${T.border}`, background:T.bgCardAlt }}>
          <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between", marginBottom:10, gap:10 }}>
            <div style={{ display:"flex", alignItems:"center", gap:8, minWidth:0 }}>
              <div style={{ width:26, height:26, borderRadius:6, background:T.brandSoft, color:T.brand,
                display:"grid", placeItems:"center", flexShrink:0 }}>
                <Icon name="layers" size={13}/>
              </div>
              <div style={{ minWidth:0 }}>
                <div style={{ fontSize:12.5, fontWeight:600, display:"flex", alignItems:"center", gap:6 }}>
                  {selected.label}
                  <span style={{ color:T.textTer, fontWeight:500, fontSize:11 }}>· disiplin kırılımı</span>
                </div>
                <div style={{ fontSize:10.5, color:T.textTer, marginTop:1 }}>
                  {selected.date}{selected.workers ? ` · ${selected.workers} işçi sahada` : ""}
                </div>
              </div>
            </div>
            <button className="mcm-btn mcm-btn-ghost" style={{ flexShrink:0 }}>
              Detay <Icon name="chevronRight" size={11}/>
            </button>
          </div>

          {selected.breakdown ? (
            <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"8px 16px" }}>
              {selected.breakdown.map(d => (
                <div key={d.name} style={{ display:"flex", alignItems:"center", gap:8, minWidth:0 }}>
                  <span style={{ width:6, height:6, borderRadius:2, background:d.color, flexShrink:0 }}/>
                  <div style={{ minWidth:0, flex:1 }}>
                    <div style={{ display:"flex", alignItems:"baseline", justifyContent:"space-between", gap:6 }}>
                      <span style={{ fontSize:11.5, fontWeight:500, color:T.textPri,
                        whiteSpace:"nowrap", overflow:"hidden", textOverflow:"ellipsis" }}>{d.name}</span>
                      <span style={{ fontSize:11, fontWeight:600, color:T.textSec,
                        flexShrink:0, fontFamily:T.fontMono }}>%{d.pct}</span>
                    </div>
                    <div style={{ display:"flex", alignItems:"center", gap:6, marginTop:3 }}>
                      <div style={{ flex:1 }}><Progress value={d.pct} color={d.color} height={3}/></div>
                      <span style={{ fontSize:9.5, color:T.textTer, flexShrink:0, fontFamily:T.fontMono }}>{d.qty}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ fontSize:11.5, color:T.textTer, padding:"8px 0", display:"flex", alignItems:"center", gap:8 }}>
              <Icon name="info" size={12}/>
              Bu kat için planlama henüz yapılmadı.
            </div>
          )}
        </div>
      )}

      {/* Legend */}
      <div style={{ padding:"10px 18px", borderTop:`1px solid ${T.border}`,
        display:"flex", alignItems:"center", justifyContent:"space-between",
        gap:10, flexWrap:"wrap", fontSize:11 }}>
        <div style={{ display:"flex", alignItems:"center", gap:14, color:T.textSec }}>
          {[
            { label:"Tamamlanan", val:counts.tamam,  dot:T.success },
            { label:"Devam eden", val:counts.devam,  dot:T.warning },
            { label:"Planlı",     val:counts.planli, dot:T.textTer },
          ].map(({ label, val, dot }) => (
            <span key={label} style={{ display:"inline-flex", alignItems:"center", gap:5 }}>
              <span style={{ width:6, height:6, borderRadius:"50%", background:dot }}/>
              {label} <b style={{ color:T.textPri, fontFamily:T.fontMono }}>{val}</b>
            </span>
          ))}
        </div>
        <div style={{ display:"flex", alignItems:"center", gap:4, color:T.textTer, fontSize:10.5 }}>
          <Icon name="info" size={11}/>
          Pencereler = daireler · turuncu = imalat tamam
        </div>
      </div>
    </div>
  );
}
