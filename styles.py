CSS_STYLE = """
<style>
/* ── DESIGN TOKENS ── */
:root {
  /* Teal dark theme */
  --bg-base:      #0a1628;
  --bg-mid:       #0d2137;
  --bg-deep:      #0f2a3d;
  --bg-panel:     rgba(13, 31, 53, 0.88);
  --bg-card:      rgba(13, 33, 55, 0.85);
  --bg-hover:     rgba(255,255,255,0.06);
  --border:       rgba(255,255,255,0.12);
  --border-lit:   rgba(255,255,255,0.25);
  --amber:        #f97316;
  --amber-glow:   rgba(249,115,22,0.22);
  --amber-shadow: rgba(249,115,22,0.30);
  --blue-accent:  #38bdf8;
  --text-1:       #ffffff;
  --text-2:       #a8c4d8;
  --text-3:       #4a6580;

  /* Legacy aliases — keeps existing JS working */
  --primary:           #f97316;
  --primary-dark:      #ea6c0a;
  --primary-light:     rgba(249,115,22,0.15);
  --primary-glow:      rgba(249,115,22,0.35);
  --bg:                #0a1628;
  --bg-2:              #0d2137;
  --bg-3:              #0f2a3d;
  --sidebar-bg:        rgba(13, 31, 53, 0.88);
  --card:              rgba(13, 33, 55, 0.85);
  --card-border:       rgba(255,255,255,0.12);
  --card-border-hover: rgba(255,255,255,0.25);
  --text:              #ffffff;
  --text-secondary:    #a8c4d8;
  --text-muted:        #4a6580;
  --success:           #22c55e;
  --success-light:     rgba(34,197,94,0.12);
  --danger:            #ef4444;
  --danger-light:      rgba(239,68,68,0.12);
  --accent:            #6366f1;
  --accent-light:      rgba(99,102,241,0.12);
  --warning:           #f59e0b;
  --font:              'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
  --radius-sm:         8px;
  --radius-md:         12px;
  --radius-lg:         16px;
  --radius-xl:         20px;
  --radius-2xl:        28px;
  --shadow:            0 8px 32px rgba(0,0,0,0.3);
  --shadow-md:         0 8px 24px rgba(0,0,0,0.5);
  --shadow-lg:         0 20px 50px rgba(0,0,0,0.7);
  --ease:              cubic-bezier(0.19,1,0.22,1);
  --ease-bounce:       cubic-bezier(0.175,0.885,0.32,1.275);
  --duration:          0.3s;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

/* ── BODY & BASE ── */
body {
  font-family: var(--font);
  background:
    linear-gradient(135deg, rgba(6,18,32,0.88) 0%, rgba(8,30,52,0.85) 35%, rgba(6,40,42,0.87) 70%, rgba(8,24,38,0.90) 100%),
    url('/static/santiye_bg.jpg') center center / cover no-repeat fixed !important;
  background-attachment: fixed;
  color: var(--text-1);
  height: 100vh; min-height: 100vh;
  position: relative; overflow-x: hidden;
}

/* ── BACKGROUND GLOWS / PATTERN ── */
#bgCanvas { position:fixed; inset:0; width:100%; height:100%; z-index:0; pointer-events:none; }

.bg-glow-1 {
  position:fixed; width:80%; height:90%; top:5%; left:20%;
  background: radial-gradient(ellipse at 50% 45%,
    rgba(0,210,190,0.32) 0%,
    rgba(0,130,200,0.22) 40%,
    transparent 70%);
  pointer-events:none; z-index:0;
}
.bg-glow-2 {
  position:fixed; width:50%; height:60%; top:-10%; right:-5%;
  background: radial-gradient(ellipse at 65% 35%,
    rgba(0,160,220,0.26) 0%, transparent 60%);
  pointer-events:none; z-index:0;
}
.bg-glow-3 {
  position:fixed; width:40%; height:50%; bottom:0; left:10%;
  background: radial-gradient(ellipse at 35% 75%,
    rgba(0,120,140,0.10) 0%, transparent 65%);
  pointer-events:none; z-index:0;
}

/* Blueprint grid pattern */
body::before {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(0,180,180,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,180,180,0.04) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none; z-index: 0;
}

/* ── LAYOUT ── */
#app {
  position: relative; z-index: 1;
  display: flex; flex-direction: column; height: 100vh; overflow: hidden;
}
#bodyRow { flex: 1; display: flex; overflow: hidden; }

/* ── TOPBAR ── */
#topbar {
  height: 54px;
  background: rgba(10, 22, 40, 0.80);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-bottom: 1px solid rgba(255,255,255,0.08);
  display: flex; align-items: center; padding: 0 22px;
  flex-shrink: 0; z-index: 10; justify-content: space-between; width: 100%;
  box-shadow: 0 2px 20px rgba(0,0,0,0.25);
}
.tb-logo {
  display: flex; align-items: center; gap: 10px;
  font-size: 16px; font-weight: 700; color: #fff; letter-spacing: -0.3px;
  user-select: none;
}
.tb-logo em { color: var(--amber); font-style: normal; font-size: 13px; font-weight: 600; margin-left: 1px; }
.tb-logo-icon {
  width: 30px; height: 30px; border-radius: 8px;
  background: linear-gradient(135deg, var(--amber), #ea6010);
  display: flex; align-items: center; justify-content: center;
  font-size: 15px; box-shadow: 0 2px 10px var(--amber-shadow);
}
.tb-right { display: flex; align-items: center; gap: 10px; }
.tb-city {
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.12);
  color: #fff; border-radius: 8px; padding: 5px 10px;
  font-family: var(--font); font-size: 12px; font-weight: 500;
  cursor: pointer; outline: none;
}
.tb-city option { background: #0d2137; color: #fff; }
.tb-weather-block {
  display: flex; align-items: center; gap: 6px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 8px; padding: 5px 11px;
}
.tb-cond { font-size: 12px; }
.tb-temp { font-size: 13px; font-weight: 700; color: #fff; }
.tb-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, #1a4060, #0d2137);
  border: 2px solid rgba(255,255,255,0.15);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; color: #a8c4d8; font-weight: 700; cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

/* ── SIDEBAR ── */
#sidebar {
  width: 180px; flex-shrink: 0;
  background: rgba(8, 20, 45, 0.65) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border-right: none;
  display: flex; flex-direction: column;
  height: 100%; overflow-y: auto; overflow-x: hidden;
  box-shadow: 2px 0 20px rgba(0,0,0,0.2);
}
#sidebar::-webkit-scrollbar { width: 0; }

.sb-top {
  padding: 14px 14px 11px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  display: flex; align-items: center; gap: 8px; flex-shrink: 0;
}
.sb-logo { font-size: 13px; font-weight: 700; color: #fff; letter-spacing: -0.2px; }
.sb-logo em { color: var(--amber); font-style: normal; }
.sb-section { padding: 12px 13px 4px; }
.sb-section-title {
  font-size: 9px; font-weight: 600; color: var(--text-3);
  letter-spacing: 1.5px; text-transform: uppercase;
}
.nav-item {
  display: flex; align-items: center; gap: 9px;
  margin: 2px 8px; padding: 7px 10px;
  font-size: 12px; font-weight: 500; color: var(--text-2);
  cursor: pointer; border-radius: 10px;
  border-left: none;
  transition: all 0.18s; user-select: none; white-space: nowrap;
  position: relative; z-index: 101; pointer-events: auto; cursor: pointer;
}
.nav-item:hover { color: #fff; background: var(--bg-hover); }
.nav-item.active {
  color: #fff !important; font-weight: 600;
  background: #f97316 !important;
  border-radius: 10px !important;
  box-shadow: 0 4px 16px var(--amber-shadow);
}
.nav-item .nav-icon { font-size: 13px; width: 16px; text-align: center; flex-shrink: 0; }
.nav-item .nav-lock { margin-left: auto; font-size: 8px; opacity: 0.25; }
.nav-label { font-size: 12px; }
.sb-fill { flex: 1; }
.sb-foot { padding: 10px 10px 14px; flex-shrink: 0; }
.sb-user-card {
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.09);
  border-radius: 12px; padding: 10px 11px;
  display: flex; align-items: center; gap: 9px;
}
.sb-user-avatar {
  width: 28px; height: 28px; border-radius: 50%;
  background: linear-gradient(135deg, var(--amber), #ea6010);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; color: #fff; font-weight: 700; flex-shrink: 0;
}
.sb-user-name { font-size: 11px; font-weight: 600; color: #fff; }
.sb-user-role { font-size: 9px; color: var(--text-3); margin-top: 1px; }
.sb-upgrade {
  background: linear-gradient(135deg, rgba(139,92,246,0.14), rgba(99,60,200,0.08));
  border: 1px solid rgba(139,92,246,0.22); border-radius: 10px;
  padding: 9px 11px; cursor: pointer; transition: 0.2s;
}
.sb-upgrade:hover { border-color: rgba(139,92,246,0.40); transform: translateY(-1px); }
.sb-upgrade-title { font-size: 11px; font-weight: 600; color: #b49cff; }
.sb-upgrade-sub { font-size: 9.5px; color: var(--text-3); margin-top: 2px; }

/* ── MAIN AREA ── */
#mainArea { flex: 1; display: flex; flex-direction: column; overflow: hidden; }

/* ── CONTENT ── */
#content {
  flex: 1; padding: 18px 20px;
  display: flex; flex-direction: column; gap: 10px; overflow-y: auto; padding-bottom: 40px;
  height: calc(100vh - 54px);
}
#content::-webkit-scrollbar { width: 0; }

/* ── QUICK ACTION CARDS ── */
.quick-actions { display: flex; gap: 12px; }
.quick-btn {
  flex: 1; display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 9px; padding: 16px 10px;
  background: rgba(8, 25, 55, 0.45) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 16px !important;
  cursor: pointer; transition: all 0.2s ease; user-select: none;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06) !important;
}
.quick-btn:hover {
  border-color: rgba(255,255,255,0.25) !important;
  transform: translateY(-3px);
  box-shadow: 0 12px 36px rgba(0,0,0,0.40) !important;
}
.quick-btn.active {
  border: 2px solid #f97316 !important;
  box-shadow: 0 0 24px rgba(249,115,22,0.25) !important;
  background: rgba(249,115,22,0.10) !important;
}
.quick-btn-icon { font-size: 26px; line-height: 1; }
.quick-btn-label {
  font-size: 10px; font-weight: 700; letter-spacing: 1.2px;
  text-transform: uppercase; color: var(--text-2);
}
.quick-btn.active .quick-btn-label { color: var(--amber); }

.quick-sub { display: none; gap: 10px; }
.quick-sub-btn {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: 7px;
  padding: 10px 8px;
  background: rgba(8, 25, 55, 0.45) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 16px !important;
  cursor: pointer; transition: all 0.2s;
  font-size: 11px; font-weight: 600; color: var(--text-2);
  box-shadow: var(--shadow);
}
.quick-sub-btn:hover {
  border-color: var(--border-lit);
  color: #fff; transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(0,0,0,0.30);
}

/* ── SEARCH / AI INPUT BOX ── */
.search-wrap { position: relative; }
.search-border {
  position: absolute; inset: 0; border-radius: 14px; padding: 1px;
  background: linear-gradient(135deg,
    rgba(249,115,22,0.40),
    rgba(99,102,241,0.28),
    rgba(0,180,200,0.18));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none;
}
.search-box {
  background: rgba(8, 25, 55, 0.45) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 16px !important;
  display: flex; align-items: center; padding: 10px 13px; gap: 10px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06) !important;
}
.search-icons { display: flex; gap: 6px; }
.search-icon {
  width: 34px; height: 34px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; cursor: pointer; flex-shrink: 0; transition: 0.18s;
}
.search-icon:hover { transform: scale(1.10); }
.search-icon.cam  { background: rgba(139,92,246,0.30); border: 1px solid rgba(139,92,246,0.35); }
.search-icon.tool { background: rgba(249,115,22,0.25); border: 1px solid rgba(249,115,22,0.30); }
.search-mid { flex: 1; }
.search-label {
  font-size: 8.5px; color: rgba(168,196,216,0.55); font-weight: 600;
  letter-spacing: 1px; text-transform: uppercase; margin-bottom: 3px;
}
.search-input-real {
  background: none; border: none; outline: none;
  font-family: var(--font); font-size: 13px; color: #fff; width: 100%; caret-color: var(--amber);
}
.search-input-real::placeholder { color: rgba(168,196,216,0.35); }
.search-send {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, var(--amber), #ea6010);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 15px; color: #fff; cursor: pointer; flex-shrink: 0;
  box-shadow: 0 3px 16px var(--amber-shadow); border: none; transition: 0.2s;
}
.search-send:hover { transform: scale(1.10); box-shadow: 0 5px 22px rgba(249,115,22,0.50); }

/* ── RESULT / ENGINEERING PANEL ── */
.result-wrap { flex: 1; position: relative; min-height: 320px; height: auto; }
.result-border {
  position: absolute; inset: 0; border-radius: 16px; padding: 1px;
  background: linear-gradient(150deg,
    rgba(0,200,190,0.28),
    rgba(0,140,200,0.18),
    transparent 60%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none;
}
.result-box {
  background: rgba(8, 25, 55, 0.45) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 16px !important;
  padding: 16px 20px; min-height: 200px;
  display: flex; flex-direction: column; gap: 12px; overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06) !important;
}
.result-box::-webkit-scrollbar { width: 3px; }
.result-box::-webkit-scrollbar-thumb { background: rgba(249,115,22,0.35); border-radius: 999px; }
.result-header { display: flex; align-items: center; gap: 9px; }
.result-live-dot {
  width: 7px; height: 7px; border-radius: 50%; background: #22c55e; flex-shrink: 0;
  box-shadow: 0 0 10px rgba(34,197,94,0.75);
  animation: blinkDot 2s ease-in-out infinite;
}
@keyframes blinkDot {
  0%, 100% { opacity: 1; box-shadow: 0 0 10px rgba(34,197,94,0.75); }
  50%       { opacity: 0.4; box-shadow: 0 0 4px rgba(34,197,94,0.3); }
}
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.5; } }
@keyframes livepulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(1.3)} }
.result-title { font-size: 14px; font-weight: 600; color: #fff; }
.result-live-tag {
  font-size: 8.5px; font-weight: 700; color: #22c55e;
  background: rgba(34,197,94,0.10); border: 1px solid rgba(34,197,94,0.22);
  border-radius: 4px; padding: 2px 6px; letter-spacing: 1px;
}
.result-body { font-size: 12.5px; color: var(--text-2); line-height: 1.80; }

/* ── STAT CHIPS ── */
.result-stats { display: flex; gap: 8px; flex-wrap: wrap; }
.stat-chip {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 13px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 20px;
  font-size: 10.5px; font-weight: 600; color: var(--text-2);
}
.stat-chip.orange {
  background: rgba(249,115,22,0.14);
  border-color: rgba(249,115,22,0.32);
  color: #ffb07c;
}
.stat-chip.blue {
  background: rgba(56,189,248,0.12);
  border-color: rgba(56,189,248,0.28);
  color: #7dd3f8;
}

/* ── FADE-IN ANIMATIONS (staggered) ── */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeInUp 0.45s var(--ease) both; }
.fade-in:nth-child(1) { animation-delay: 0.00s; }
.fade-in:nth-child(2) { animation-delay: 0.06s; }
.fade-in:nth-child(3) { animation-delay: 0.12s; }
.fade-in:nth-child(4) { animation-delay: 0.18s; }

/* ══════════════════════════════════════════
   LEGACY COMPONENT STYLES
   ══════════════════════════════════════════ */

@keyframes fadeIn         { from { opacity: 0; } to { opacity: 1; } }
@keyframes fadeInDown     { from { opacity: 0; transform: translateY(-16px); } to { opacity: 1; transform: translateY(0); } }
@keyframes scaleIn        { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
@keyframes blink          { 0%,100% { opacity:1; } 50% { opacity:0.2; } }
@keyframes spin           { to { transform: rotate(360deg); } }
@keyframes pulseBtn       { 0% { box-shadow: 0 0 0 0 var(--primary-glow); } 70% { box-shadow: 0 0 0 16px transparent; } 100% { box-shadow: 0 0 0 0 transparent; } }
@keyframes containerEntry { from { opacity:0; transform:translateY(20px) scale(0.98); } to { opacity:1; transform:translateY(0) scale(1); } }
@keyframes shimmer        { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }

.animate-in    { animation: fadeInUp 0.4s var(--ease) both; }
.animate-scale { animation: scaleIn 0.35s var(--ease-bounce) both; }

/* ── AUTH OVERLAY ── */
#auth-overlay {
  position: fixed; top:0; left:0; width:100vw; height:100vh;
  background: rgba(0,0,0,0.88);
  display: flex; align-items: flex-start; justify-content: center;
  z-index: 5000; backdrop-filter: blur(20px);
  overflow-y: auto;
  padding: 20px 0;
}
.auth-card {
  background: rgba(13, 33, 55, 0.95);
  border: 1px solid rgba(255,255,255,0.12);
  border-top: 2px solid var(--amber);
  border-radius: var(--radius-2xl);
  padding: 45px; width: 90%; max-width: 400px; text-align: center;
  box-shadow: 0 24px 60px rgba(0,0,0,0.6); animation: containerEntry 0.5s var(--ease-bounce) both;
  backdrop-filter: blur(16px);
  max-height: none; overflow-y: visible;
}
.auth-card h2 { color: var(--amber); margin-bottom: 8px; font-weight: 800; letter-spacing: -0.5px; font-size: 1.8rem; }
.auth-input {
  width: 100%; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--radius-md); padding: 14px 16px; color: #fff;
  font-size: 1rem; outline: none; margin-bottom: 12px; transition: all 0.25s ease;
  box-sizing: border-box; font-family: var(--font);
}
.auth-input:focus { border-color: var(--amber); background: rgba(249,115,22,0.08); box-shadow: 0 0 0 3px rgba(249,115,22,0.08); }
.auth-btn {
  width: 100%; padding: 15px;
  background: linear-gradient(135deg, var(--amber), var(--primary-dark));
  color: white; border: none; border-radius: var(--radius-md);
  font-weight: 700; font-size: 1rem; cursor: pointer;
  transition: all var(--duration) var(--ease); font-family: var(--font);
  box-shadow: 0 4px 18px var(--amber-shadow);
}
.auth-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 28px var(--amber-shadow); }

/* ── MODAL SYSTEM ── */
.modal-overlay {
  position: fixed; top:0; left:0; width:100%; height:100%;
  background: rgba(0,0,0,0.75); backdrop-filter: blur(12px);
  display: none; align-items: center; justify-content: center;
  z-index: 3000; opacity:0; transition: opacity 0.3s ease;
}
.modal-overlay.active { display: flex; opacity:1; }
.modal-content {
  background: rgba(13, 33, 55, 0.96);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--radius-xl); padding: 35px; width: 90%; max-width: 440px;
  box-shadow: 0 24px 60px rgba(0,0,0,0.6); transform: translateY(30px) scale(0.97);
  transition: transform 0.4s var(--ease-bounce); border-top: 2px solid var(--amber);
  backdrop-filter: blur(16px);
}
.modal-overlay.active .modal-content { transform: translateY(0) scale(1); }
.modal-header { color: var(--amber); font-weight: 800; margin-bottom: 24px; font-size: 1.2rem; text-align: center; }
.modal-input {
  width: 100%; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--radius-md); padding: 14px 16px; color: #fff;
  font-size: 1rem; outline: none; margin-top: 8px; transition: all 0.25s ease;
  box-sizing: border-box; font-family: var(--font);
}
.modal-input:focus { border-color: var(--amber); background: rgba(249,115,22,0.08); }
.modal-footer { display: flex; gap: 12px; margin-top: 28px; }
.modal-btn { flex:1; padding: 14px; border-radius: var(--radius-md); border: none; cursor: pointer; font-weight: 700; font-size: 0.95rem; transition: all var(--duration) var(--ease); font-family: var(--font); }
.btn-confirm { background: linear-gradient(135deg, var(--amber), var(--primary-dark)); color: white; box-shadow: 0 4px 15px var(--amber-shadow); }
.btn-confirm:hover { transform: translateY(-2px); }
.btn-cancel { background: rgba(255,255,255,0.07); color: var(--text-2); border: 1px solid rgba(255,255,255,0.12); }
.btn-cancel:hover { background: rgba(255,255,255,0.12); color: #fff; }

/* ── MÜHENDİSLİK PANELİ SIDEBAR ── */
#sidebarPanel {
  position: fixed; right: -460px; top: 0;
  width: 420px; height: 100vh;
  background: rgba(10, 22, 40, 0.98); backdrop-filter: blur(12px);
  border-left: 1px solid rgba(249,115,22,0.2);
  padding: 28px 28px 40px;
  transition: right 0.7s var(--ease); z-index: 2000; overflow-y: auto;
  box-shadow: -20px 0 60px rgba(0,0,0,0.8);
}
#sidebarPanel.active { right: 0; }
.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 50;
  pointer-events: none;
}
.sidebar-overlay.active { display: none; pointer-events: none; }

/* ── TOOL CARDS ── */
.category-title {
  color: var(--text-3); font-size: 0.68rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1.5px; margin: 20px 0 8px; padding-left: 4px;
}
.tool-card {
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.10);
  border-radius: 14px; padding: 14px 16px; margin-bottom: 8px;
  cursor: pointer; transition: all 0.2s ease;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}
.tool-card:hover { border-color: rgba(255,255,255,0.22); background: rgba(255,255,255,0.07); transform: translateY(-2px); }
.tool-card h4 { font-size: 0.9rem; margin:0; color:#fff; font-weight:700; }
.tool-card small { font-size: 0.75rem; color: var(--text-2); margin:0; }

.btn-read {
  flex:1; padding: 11px 18px; background: transparent;
  border: 1px solid rgba(255,255,255,0.12); border-radius: var(--radius-md);
  color: var(--text-2); font-family: var(--font); font-weight: 600;
  font-size: 0.85rem; cursor: pointer; transition: all 0.25s var(--ease);
}
.btn-read:hover { background: rgba(255,255,255,0.07); color: #fff; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-thumb { background: rgba(249,115,22,0.4); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: var(--amber); }
::-webkit-scrollbar-track { background: transparent; }

/* ── THEME TOGGLE ── */
.theme-toggle {
  width: 44px; height: 24px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 999px; cursor: pointer; position: relative; transition: background 0.3s ease; flex-shrink: 0;
}
.theme-toggle::after {
  content: ''; position: absolute; top: 3px; left: 3px; width: 16px; height: 16px;
  background: var(--text-2); border-radius: 50%; transition: all 0.3s var(--ease);
}

/* ── LEGACY RESULT ── */
.res-title  { color: var(--amber); font-size: 1rem; font-weight: 800; margin-bottom: 8px; }
.res-detail { color: var(--text-2); font-size: 0.9rem; line-height: 1.7; }
.res-value  { color: #fff; font-size: 1.4rem; font-weight: 700; margin-bottom: 6px; }
#result { overflow-y: auto; }

/* ── WEATHER INLINE (compat) ── */
.weather-inline { display: flex; align-items: center; gap: 10px; }
.city-select-inline { background: transparent; border: none; color: var(--text-2); font-size: 0.82rem; font-weight: 600; cursor: pointer; outline: none; font-family: var(--font); max-width: 100px; }
.weather-data { display: flex; flex-direction: column; align-items: flex-end; line-height: 1.1; }
.weather-temp { font-size: 1.1rem; font-weight: 800; color: var(--amber); }
.weather-cond { font-size: 0.6rem; color: var(--text-3); text-transform: uppercase; letter-spacing: 1.5px; }

/* ── MISC LEGACY ── */
.divider    { border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 20px 0; }
.auth-link  { color: var(--amber); cursor: pointer; font-size: 0.85rem; text-align: center; margin-top: 15px; display: block; }
.auth-link:hover { text-decoration: underline; }
.active-lang { background: rgba(249,115,22,0.28) !important; border-color: var(--amber) !important; color: white !important; }
.msg-success { background: var(--success-light); color: var(--success); border: 1px solid rgba(34,197,94,0.25); border-radius: var(--radius-sm); padding: 10px 16px; margin-top: 10px; font-size: 0.88rem; }
.msg-error   { background: var(--danger-light);  color: var(--danger);  border: 1px solid rgba(239,68,68,0.25);  border-radius: var(--radius-sm); padding: 10px 16px; margin-top: 10px; font-size: 0.88rem; }
.btn-action  { width:50px; height:50px; border-radius: var(--radius-md); border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; font-size:1.2rem; transition: all var(--duration) var(--ease); flex-shrink:0; }
.btn-action:hover { transform: scale(1.08); filter: brightness(1.15); }
.mic-btn  { background: linear-gradient(135deg, var(--accent), #4f46e5); color: white; }
.send-btn { background: linear-gradient(135deg, var(--amber), var(--primary-dark)); color: white; }
.img-btn  { background: linear-gradient(135deg, #8b5cf6, #7c3aed); color: white; }
.mic-btn.recording  { background: linear-gradient(135deg, #ef4444, #dc2626); animation: pulseBtn 1.5s infinite; }
.img-btn.active-img { background: linear-gradient(135deg, var(--success), #16a34a); animation: pulseBtn 1.5s infinite; }

/* ── HAMBURGER BUTTON ── */
#hamburger-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 36px;
  height: 36px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 8px;
  cursor: pointer;
  margin-right: 10px;
  flex-shrink: 0;
}

#hamburger-btn span {
  display: block;
  width: 18px;
  height: 2px;
  background: #fff;
  border-radius: 2px;
  transition: all 0.3s;
}

#hamburger-btn.open span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}
#hamburger-btn.open span:nth-child(2) {
  opacity: 0;
}
#hamburger-btn.open span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* ── MOBILE ── */
@media (max-width: 768px) {
  #app { height: 100dvh; overflow: hidden; }

  #topbar {
    padding: 0 12px !important;
    height: 54px !important;
    position: relative;
    z-index: 100;
  }

  .tb-weather-block { display: none !important; visibility: hidden !important; }
  .tb-hide-mobile { display: none !important; }
  .tb-city { display: none !important; }
  select#citySelect { display: none !important; }
  #condition { display: none !important; }
  #temp { display: none !important; }

  .tb-cond {
    display: none !important;
  }

  #hamburger-btn {
    display: flex !important;
  }

  #mobile-overlay {
    display: none !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    background: rgba(0,0,0,0.7) !important;
    z-index: 100 !important;
  }

  #mobile-overlay.active {
    display: block !important;
  }

  #sidebar {
    position: fixed !important;
    top: 0 !important;
    left: -100% !important;
    width: 80% !important;
    max-width: 280px !important;
    height: 100dvh !important;
    z-index: 200 !important;
    background: rgba(8, 18, 40, 0.98) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(255,255,255,0.10) !important;
    transition: left 0.3s ease !important;
    overflow-y: auto !important;
    flex-direction: column !important;
    padding-top: 20px !important;
    display: flex !important;
  }

  #sidebar.mobile-open {
    left: 0 !important;
    z-index: 200 !important;
  }

  #sidebar * {
    position: relative !important;
    z-index: 201 !important;
    pointer-events: auto !important;
  }

  .nav-item {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding: 14px 20px !important;
    font-size: 14px !important;
    margin: 2px 10px !important;
    white-space: nowrap !important;
    border-radius: 12px !important;
  }

  .nav-icon { font-size: 18px !important; }

  .sb-section-title {
    padding: 14px 20px 4px !important;
    display: block !important;
  }

  .sb-fill { flex: 1 !important; }

  .sb-foot {
    display: block !important;
    padding: 10px !important;
  }

  #bodyRow {
    flex-direction: row !important;
    height: calc(100dvh - 54px) !important;
    overflow: hidden !important;
    position: relative !important;
  }

  #mainArea {
    flex: 1 !important;
    width: 100% !important;
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch !important;
    position: relative !important;
    z-index: 1 !important;
  }

  #content {
    padding: 10px !important;
    gap: 8px !important;
    padding-bottom: 20px !important;
  }

  .quick-actions {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 8px !important;
  }

  .quick-btn {
    flex: unset !important;
    padding: 12px 8px !important;
    min-width: unset !important;
  }

  .quick-sub {
    flex-wrap: wrap !important;
    gap: 6px !important;
  }

  .quick-sub-btn {
    flex: unset !important;
    min-width: calc(50% - 3px) !important;
    font-size: 12px !important;
  }

  .search-box { padding: 8px 10px !important; }

  #planLabel {
    font-size: 11px !important;
    font-weight: 500 !important;
    padding: 2px 7px !important;
    background: rgba(239,68,68,0.15) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-radius: 8px !important;
    vertical-align: middle !important;
  }

  .tb-logo {
    font-size: 13px !important;
  }
  .result-box { padding: 12px 14px !important; }

  #mainArea, #content, .quick-actions, .quick-btn,
  .quick-sub, .quick-sub-btn, .search-wrap, .result-wrap {
    pointer-events: auto !important;
    position: relative !important;
    z-index: 1 !important;
  }
}

/* ── FİYAT TAKİBİ MODALİ ── */
#fiyatModal > div {
  background: rgba(8, 20, 45, 0.92) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-top: 2px solid var(--amber) !important;
  box-shadow: 0 24px 60px rgba(0,0,0,0.6) !important;
}

/* Uyarı satırları (demir düştü vb.) */
#uyarilar > div {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 10px !important;
  padding: 10px 14px !important;
  margin-bottom: 8px !important;
  font-size: 13px !important;
}

/* Fiyat kartları */
#fiyatKartlari > div {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 14px !important;
  backdrop-filter: blur(10px) !important;
  transition: all 0.2s !important;
}
#fiyatKartlari > div:hover {
  border-color: rgba(249,115,22,0.35) !important;
  transform: translateY(-2px) !important;
}

/* Grafik alanı */
#fiyatModal canvas {
  border-radius: 10px !important;
}

/* Select ve input'lar */
#fiyatModal select,
#fiyatModal input[type="number"] {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  border-radius: 10px !important;
  color: white !important;
  padding: 10px 12px !important;
}
#fiyatModal select:focus,
#fiyatModal input:focus {
  border-color: var(--amber) !important;
  outline: none !important;
}

/* Bölüm başlıkları */
#fiyatModal .div[style*="color:var(--primary)"],
#fiyatModal div[style*="color: var(--primary)"] {
  font-size: 13px !important;
  letter-spacing: 0.5px !important;
}

/* Scrollbar */
#fiyatModal ::-webkit-scrollbar { width: 4px; }
#fiyatModal ::-webkit-scrollbar-thumb {
  background: rgba(249,115,22,0.4);
  border-radius: 999px;
}

/* ── TÜM MODALLER — GENEL GLASSMORPHİSM ── */
#stokModal > div,
#depremModal > div,
#gunlukRaporModal > div,
#arsivModal > div,
#proModal > div,
#profileModal > div,
#kameraModal > div,
#santiyeModal > div,
#santiyeFormModal > div,
#odemeModal > div {
  background: rgba(8, 20, 45, 0.92) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-top: 2px solid var(--amber) !important;
  box-shadow: 0 24px 60px rgba(0,0,0,0.6) !important;
}

/* Modal arka plan overlay */
#stokModal,
#depremModal,
#gunlukRaporModal,
#arsivModal,
#proModal,
#kameraModal {
  background: rgba(0,0,0,0.75) !important;
  backdrop-filter: blur(8px) !important;
}

/* Modal içi kartlar */
#stokModal div[style*="background:rgba(255,255,255,0.04)"],
#depremModal div[style*="background:rgba(255,255,255,0.04)"],
#gunlukRaporModal div[style*="background:rgba(255,255,255,0.04)"] {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 14px !important;
}

/* Tüm modal select ve input'lar */
#stokModal select, #stokModal input,
#depremModal select, #depremModal input,
#gunlukRaporModal select, #gunlukRaporModal input,
#gunlukRaporModal textarea {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  border-radius: 10px !important;
  color: white !important;
}
#stokModal select:focus, #stokModal input:focus,
#depremModal input:focus,
#gunlukRaporModal textarea:focus,
#gunlukRaporModal select:focus {
  border-color: var(--amber) !important;
  outline: none !important;
}

/* Stok geçmiş listesi */
#stokGecmisListe > div {
  background: rgba(255,255,255,0.03) !important;
  border-bottom: 1px solid rgba(255,255,255,0.06) !important;
  padding: 8px 4px !important;
}

/* Deprem harita border */
#depremHarita {
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 14px !important;
  overflow: hidden !important;
}

/* Arşiv içerik */
#arsivIcerik > div {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 12px !important;
  margin-bottom: 10px !important;
  padding: 12px 16px !important;
}

/* ── SONUÇ ALANI BUTONLARI ── */
#result button,
#result a[style*="background"] {
  background: rgba(255,255,255,0.07) !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  border-radius: 12px !important;
  color: #e2e8f0 !important;
  backdrop-filter: blur(10px) !important;
  font-weight: 600 !important;
  transition: all 0.2s !important;
  padding: 12px 20px !important;
}
#result button:hover {
  background: rgba(249,115,22,0.15) !important;
  border-color: rgba(249,115,22,0.4) !important;
  color: white !important;
  transform: translateY(-1px) !important;
}

/* ── ŞANTİYE DASHBOARD MODALİ ── */
#santiyeModal {
  background: rgba(0,0,0,0.75) !important;
  backdrop-filter: blur(8px) !important;
  padding: 20px !important;
  overflow-y: auto !important;
}

#santiyeModal > div {
  background: rgba(8, 20, 45, 0.95) !important;
  backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 24px !important;
  box-shadow: 0 24px 60px rgba(0,0,0,0.6) !important;
  overflow: hidden !important;
}

/* Header */
#santiyeModal > div > div:first-child {
  background: linear-gradient(135deg, #f97316, #ea6010) !important;
  padding: 22px 28px !important;
  border-radius: 0 !important;
}

/* Özet kartları */
#santiyeOzet > div {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 14px !important;
  padding: 16px !important;
  text-align: center !important;
  transition: all 0.2s !important;
}
#santiyeOzet > div:hover {
  border-color: rgba(249,115,22,0.35) !important;
  transform: translateY(-2px) !important;
}

/* Harita container */
#santiyeHarita {
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 14px !important;
  overflow: hidden !important;
  background: rgba(255,255,255,0.03) !important;
}

/* Tablo */
#santiyeTablo {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 14px !important;
  padding: 12px !important;
}

/* Şantiye kartları */
#santiyeKartlar > div {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 16px !important;
  padding: 18px !important;
  transition: all 0.2s !important;
  cursor: pointer !important;
}
#santiyeKartlar > div:hover {
  border-color: rgba(249,115,22,0.35) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 12px 32px rgba(0,0,0,0.3) !important;
}

/* Section başlıkları */
#santiyeModal [style*="text-transform:uppercase"],
#santiyeModal [style*="text-transform: uppercase"] {
  color: rgba(168,196,216,0.6) !important;
  font-size: 10px !important;
  letter-spacing: 2px !important;
}

/* + Yeni Şantiye butonu */
#santiyeModal button[onclick*="santiyeEkleModalAc"] {
  background: rgba(255,255,255,0.15) !important;
  border: 1px solid rgba(255,255,255,0.25) !important;
  border-radius: 10px !important;
  color: white !important;
  font-weight: 700 !important;
  transition: all 0.2s !important;
}
#santiyeModal button[onclick*="santiyeEkleModalAc"]:hover {
  background: rgba(255,255,255,0.25) !important;
}

/* ── ŞANTİYE DASHBOARD — TAM YENİDEN ── */
#santiyeModal {
  background: rgba(0,0,0,0.80) !important;
  backdrop-filter: blur(12px) !important;
  align-items: flex-start !important;
  justify-content: center !important;
  padding: 30px 20px !important;
  overflow-y: auto !important;
}
#santiyeModal > div {
  background: rgba(8, 18, 40, 0.97) !important;
  backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 24px !important;
  box-shadow: 0 30px 80px rgba(0,0,0,0.7) !important;
  overflow: hidden !important;
  max-width: 1100px !important;
  width: 100% !important;
  margin: auto !important;
}

/* Header gradient */
#santiyeModal > div > div:first-child {
  background: linear-gradient(135deg, #f97316 0%, #c2500e 100%) !important;
  padding: 22px 28px !important;
}

/* İç padding alanı */
#santiyeModal > div > div:nth-child(2) {
  padding: 24px !important;
}

/* Özet stat kartları */
#santiyeOzet {
  display: grid !important;
  grid-template-columns: repeat(4, 1fr) !important;
  gap: 12px !important;
  margin-bottom: 20px !important;
}
#santiyeOzet > div {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 14px !important;
  padding: 16px 18px !important;
  transition: all 0.2s !important;
}
#santiyeOzet > div:hover {
  border-color: rgba(249,115,22,0.4) !important;
  transform: translateY(-2px) !important;
  background: rgba(249,115,22,0.08) !important;
}

/* Grid layout düzelt */
#santiyeModal div[style*="grid-template-columns:1fr 1fr"] {
  gap: 20px !important;
}

/* Harita */
#santiyeHarita {
  height: 280px !important;
  border-radius: 14px !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  overflow: hidden !important;
}

/* Tablo alanı */
#santiyeTablo {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 14px !important;
  padding: 14px !important;
  min-height: 280px !important;
}

/* Şantiye kartları */
#santiyeKartlar {
  display: grid !important;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)) !important;
  gap: 14px !important;
  margin-top: 16px !important;
}
#santiyeKartlar > div {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 16px !important;
  padding: 18px !important;
  transition: all 0.2s !important;
  cursor: pointer !important;
}
#santiyeKartlar > div:hover {
  border-color: rgba(249,115,22,0.40) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 12px 32px rgba(0,0,0,0.35) !important;
  background: rgba(249,115,22,0.06) !important;
}

/* Section label */
#santiyeModal div[style*="color:#aaa"][style*="uppercase"] {
  color: rgba(168,196,216,0.55) !important;
  font-size: 10px !important;
  letter-spacing: 2px !important;
  margin-bottom: 12px !important;
}

/* + Yeni Şantiye butonu */
#santiyeModal button[onclick*="santiyeEkleModalAc(null)"] {
  background: rgba(255,255,255,0.18) !important;
  border: 1px solid rgba(255,255,255,0.3) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(6px) !important;
  transition: all 0.2s !important;
}
#santiyeModal button[onclick*="santiyeEkleModalAc(null)"]:hover {
  background: rgba(255,255,255,0.28) !important;
}

/* ── GÜVENLİK MODALI ── */
.g-tab {
  padding: 7px 16px;
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.12);
  background: transparent;
  color: #aaa;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all .15s;
  font-family: var(--font);
}
.g-tab:hover { background: rgba(255,255,255,0.08); color: white; }
.g-tab.active { background: #dc2626; border-color: #dc2626; color: white; }

.g-check-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  cursor: pointer;
  transition: all .15s;
  border-radius: 8px;
}
.g-check-item:hover { background: rgba(255,255,255,0.03); padding-left: 8px; }
.g-check-item:last-child { border-bottom: none; }

.g-checkbox {
  width: 24px; height: 24px;
  border-radius: 8px;
  border: 2px solid rgba(255,255,255,0.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700;
  flex-shrink: 0;
  transition: all .15s;
  color: #aaa;
}
.g-checkbox.checked { background: #22c55e; border-color: #22c55e; color: white; }

.g-check-label { font-size: 14px; color: white; font-weight: 500; }
.g-check-sub { font-size: 12px; color: #aaa; margin-top: 2px; }

.g-badge {
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 10px;
  font-weight: 600;
  white-space: nowrap;
  margin-left: auto;
  flex-shrink: 0;
}
.g-badge-ok { background: rgba(34,197,94,0.15); color: #22c55e; border: 1px solid rgba(34,197,94,0.2); }
.g-badge-warn { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.2); }
</style>
"""
