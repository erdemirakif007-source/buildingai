CSS_STYLE = """
<style>
/* ── DESIGN TOKENS ── */
:root {
  /* Premium dark theme — matches Landing page */
  --bg-base:      #030712;
  --bg-mid:       #060d1f;
  --bg-deep:      #080f24;
  --bg-panel:     rgba(6, 13, 31, 0.80);
  --bg-card:      rgba(8, 16, 36, 0.75);
  --bg-hover:     rgba(99,102,241,0.08);
  --border:       rgba(255,255,255,0.10);
  --border-lit:   rgba(255,255,255,0.22);
  --amber:        #f97316;
  --amber-glow:   rgba(249,115,22,0.22);
  --amber-shadow: rgba(249,115,22,0.30);
  --blue-accent:  #6366f1;
  --text-1:       #ffffff;
  --text-2:       #94a3b8;
  --text-3:       #475569;

  /* Legacy aliases — keeps existing JS working */
  --primary:           #f97316;
  --primary-dark:      #ea6c0a;
  --primary-light:     rgba(249,115,22,0.15);
  --primary-glow:      rgba(249,115,22,0.35);
  --bg:                #030712;
  --bg-2:              #060d1f;
  --bg-3:              #080f24;
  --sidebar-bg:        rgba(3, 7, 18, 0.85);
  --card:              rgba(8, 16, 36, 0.75);
  --card-border:       rgba(255,255,255,0.10);
  --card-border-hover: rgba(255,255,255,0.22);
  --text:              #ffffff;
  --text-secondary:    #94a3b8;
  --text-muted:        #475569;
  --success:           #22c55e;
  --success-light:     rgba(34,197,94,0.12);
  --danger:            #ef4444;
  --danger-light:      rgba(239,68,68,0.12);
  --accent:            #6366f1;
  --accent-light:      rgba(99,102,241,0.12);
  --warning:           #f59e0b;
  --font:              'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
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
  background: #F8FAFC !important;
  color: #0F172A !important;
  height: 100vh; min-height: 100vh;
  position: relative; overflow-x: hidden;
  letter-spacing: -0.01em;
}

body::before {
  content: '';
  position: fixed;
  inset: 0;
  background: transparent;
  z-index: 0;
  pointer-events: none;
}

/* ── BACKGROUND GLOWS / PATTERN ── */
#bgCanvas { position:fixed; inset:0; width:100%; height:100%; z-index:0; pointer-events:none; }

/* Indigo aurora glow — matches Landing */
.bg-glow-1 {
  position:fixed; width:70%; height:70%; top:-15%; left:-10%;
  background: radial-gradient(ellipse at 40% 40%,
    rgba(99,102,241,0.12) 0%,
    rgba(99,102,241,0.05) 45%,
    transparent 70%);
  filter: blur(60px);
  pointer-events:none; z-index:0;
  animation: dashBlob1 14s ease-in-out infinite alternate;
}
.bg-glow-2 {
  position:fixed; width:55%; height:60%; top:-10%; right:-5%;
  background: radial-gradient(ellipse at 60% 30%,
    rgba(139,92,246,0.09) 0%,
    rgba(99,102,241,0.05) 50%,
    transparent 70%);
  filter: blur(80px);
  pointer-events:none; z-index:0;
  animation: dashBlob2 18s ease-in-out infinite alternate;
}
.bg-glow-3 {
  position:fixed; width:45%; height:55%; bottom:-5%; left:5%;
  background: radial-gradient(ellipse at 35% 70%,
    rgba(249,115,22,0.07) 0%,
    transparent 65%);
  filter: blur(70px);
  pointer-events:none; z-index:0;
}
@keyframes dashBlob1 { from { transform: translate(0,0) scale(1); } to { transform: translate(20px,25px) scale(1.06); } }
@keyframes dashBlob2 { from { transform: translate(0,0) scale(1); } to { transform: translate(-15px,18px) scale(1.04); } }

/* Dot grid — devre dışı (light theme) */
body::before {
  content: '';
  position: fixed; inset: 0;
  background-image: none;
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
  background: rgba(3, 7, 18, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255,255,255,0.07);
  display: flex; align-items: center; padding: 0 22px;
  flex-shrink: 0; z-index: 10; justify-content: space-between; width: 100%;
  box-shadow: 0 1px 0 rgba(99,102,241,0.08);
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
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.09);
  color: #fff; border-radius: 8px; padding: 5px 10px;
  font-family: var(--font); font-size: 12px; font-weight: 500;
  cursor: pointer; outline: none;
}
.tb-city option { background: #060d1f; color: #fff; }
.tb-weather-block {
  display: flex; align-items: center; gap: 6px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px; padding: 5px 11px;
}
.tb-cond { font-size: 12px; }
.tb-temp { font-size: 13px; font-weight: 700; color: #fff; }
.tb-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, rgba(99,102,241,0.35), rgba(67,56,202,0.4));
  border: 1px solid rgba(99,102,241,0.30);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; color: #c7d2fe; font-weight: 700; cursor: pointer;
  box-shadow: 0 2px 12px rgba(99,102,241,0.20);
}

/* ── SIDEBAR ── */
#sidebar {
  width: 200px; flex-shrink: 0;
  background: rgba(8, 10, 16, 0.85) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
  display: flex; flex-direction: column;
  height: 100%; overflow-y: auto; overflow-x: hidden;
  box-shadow: 1px 0 0 rgba(99,102,241,0.06);
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
  font-size: 11px; font-weight: 600; color: rgba(255, 255, 255, 0.25);
  letter-spacing: 0.12em; text-transform: uppercase;
  padding: 10px 14px 4px;
}
.nav-item {
  display: flex; align-items: center; gap: 9px;
  margin: 2px 8px; padding: 9px 14px;
  font-size: 14px; font-weight: 500; color: var(--text-2);
  cursor: pointer; border-radius: 10px;
  border-left: none;
  transition: all 0.18s; user-select: none; white-space: nowrap;
  position: relative; z-index: 101; pointer-events: auto; cursor: pointer;
}
.nav-item:hover {
  color: #fff;
  background: rgba(99,102,241,0.10);
  box-shadow: inset 0 0 0 1px rgba(99,102,241,0.18);
}
.nav-item.active {
  color: #fff !important; font-weight: 600;
  background: rgba(249, 115, 22, 0.15) !important;
  border-radius: 8px !important;
  box-shadow: 0 4px 16px rgba(249,115,22,0.28), 0 0 0 1px rgba(249,115,22,0.20) !important;
}
.nav-item .nav-icon { font-size: 16px; width: 18px; text-align: center; flex-shrink: 0; }
.nav-item .nav-lock { margin-left: auto; font-size: 8px; opacity: 0.25; }
.nav-label { font-size: 12px; }
.sb-fill { flex: 1; }
.sb-foot { padding: 10px 10px 14px; flex-shrink: 0; }
.sb-user-card {
  background: rgba(99,102,241,0.06); border: 1px solid rgba(99,102,241,0.14);
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
  background: linear-gradient(135deg, rgba(249,115,22,0.15), rgba(99,102,241,0.15));
  border: 1px solid rgba(249,115,22,0.25);
  border-radius: 10px;
  padding: 10px 12px;
  cursor: pointer;
  transition: 0.2s;
}
.sb-upgrade:hover { border-color: rgba(139,92,246,0.40); transform: translateY(-1px); }
.sb-upgrade-title { font-size: 13px; font-weight: 600; color: #f97316; }
.sb-upgrade-sub { font-size: 11px; color: rgba(255,255,255,0.35); margin-top: 2px; }

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
  justify-content: center; gap: 9px; padding: 18px 10px;
  background: rgba(6, 13, 31, 0.60) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-top: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 16px !important;
  cursor: pointer; transition: all 0.22s ease; user-select: none;
  box-shadow: 0 4px 24px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.05) !important;
  position: relative; overflow: hidden;
}
.quick-btn::before {
  content: '';
  position: absolute; inset-x: 0; top: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(99,102,241,0.40), transparent);
  opacity: 0; transition: opacity 0.22s;
}
.quick-btn:hover {
  border-color: rgba(99,102,241,0.25) !important;
  border-top-color: rgba(99,102,241,0.35) !important;
  transform: translateY(-3px);
  box-shadow: 0 12px 36px rgba(0,0,0,0.40), 0 0 0 1px rgba(99,102,241,0.12), 0 -1px 0 rgba(99,102,241,0.25) inset !important;
  background: rgba(99,102,241,0.06) !important;
}
.quick-btn:hover::before { opacity: 1; }
.quick-btn.active {
  border: 1px solid rgba(249,115,22,0.35) !important;
  border-top: 1px solid rgba(249,115,22,0.55) !important;
  box-shadow: 0 0 28px rgba(249,115,22,0.18), 0 4px 24px rgba(0,0,0,0.35) !important;
  background: rgba(249,115,22,0.08) !important;
}
.quick-btn-icon {
  font-size: 22px; line-height: 1;
  background: #0D1117;
  border-radius: 10px;
  padding: 10px;
  filter: drop-shadow(0 0 8px rgba(249,115,22,0.30));
}
.quick-btn-label {
  font-size: 10px; font-weight: 700; letter-spacing: 0.8px;
  text-transform: uppercase; color: var(--text-2);
}
.quick-btn:hover .quick-btn-label { color: #c7d2fe; }
.quick-btn.active .quick-btn-label { color: var(--amber); }
.quick-btn.active .quick-btn-icon { filter: drop-shadow(0 0 10px rgba(249,115,22,0.50)); }

.quick-sub { display: none; gap: 10px; }
.quick-sub-btn {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: 7px;
  padding: 10px 8px;
  background: rgba(6, 13, 31, 0.60) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 16px !important;
  cursor: pointer; transition: all 0.2s;
  font-size: 11px; font-weight: 600; color: var(--text-2);
  box-shadow: 0 4px 20px rgba(0,0,0,0.30);
}
.quick-sub-btn:hover {
  border-color: rgba(99,102,241,0.25) !important;
  color: #fff; transform: translateY(-2px);
  background: rgba(99,102,241,0.07) !important;
  box-shadow: 0 8px 28px rgba(0,0,0,0.30);
}

/* ── SEARCH / AI INPUT BOX ── */
.search-wrap { position: relative; }
.search-border {
  position: absolute; inset: 0; border-radius: 16px; padding: 1px;
  background: linear-gradient(135deg,
    rgba(249,115,22,0.35),
    rgba(99,102,241,0.30),
    rgba(139,92,246,0.20));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none;
}
.search-box {
  background: rgba(6, 13, 31, 0.65) !important;
  backdrop-filter: blur(24px) !important;
  -webkit-backdrop-filter: blur(24px) !important;
  border: 1px solid rgba(255,255,255,0.09) !important;
  border-radius: 16px !important;
  display: flex; align-items: center; padding: 10px 13px; gap: 10px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.05) !important;
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
    rgba(99,102,241,0.30),
    rgba(139,92,246,0.18),
    transparent 60%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none;
}
.result-box {
  background: rgba(6, 13, 31, 0.65) !important;
  backdrop-filter: blur(24px) !important;
  -webkit-backdrop-filter: blur(24px) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 16px !important;
  padding: 16px 20px; min-height: 200px;
  display: flex; flex-direction: column; gap: 12px; overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.05) !important;
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

/* ── CHAT HUB PANEL ── */
.chat-header {
  display: flex; align-items: center; gap: 8px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  flex-shrink: 0;
}
.chat-header-title { font-size: 14px; font-weight: 600; color: #fff; flex: 1; }
.chat-kaynak {
  font-size: 9px; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase;
  color: #6366f1; background: rgba(99,102,241,0.12);
  border: 1px solid rgba(99,102,241,0.22); border-radius: 4px; padding: 2px 7px;
}

.chat-history {
  flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 14px;
  padding: 4px 0 8px;
}
.chat-history::-webkit-scrollbar { width: 3px; }
.chat-history::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.30); border-radius: 99px; }

/* User message (right) */
.chat-msg { display: flex; align-items: flex-end; gap: 10px; }
.chat-msg--user { justify-content: flex-end; }
.chat-msg--ai   { justify-content: flex-start; }

.chat-avatar {
  width: 30px; height: 30px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, rgba(99,102,241,0.35), rgba(67,56,202,0.5));
  border: 1px solid rgba(99,102,241,0.30);
  display: flex; align-items: center; justify-content: center; font-size: 14px;
}

.chat-bubble {
  max-width: 78%; padding: 10px 14px; border-radius: 14px;
  font-size: 12.5px; line-height: 1.75; position: relative;
  display: flex; flex-direction: column; gap: 5px;
}
.chat-bubble--user {
  background: linear-gradient(135deg, rgba(249,115,22,0.20), rgba(249,115,22,0.12));
  border: 1px solid rgba(249,115,22,0.28);
  border-bottom-right-radius: 4px;
  color: #fff;
}
.chat-bubble--ai {
  background: rgba(6, 13, 31, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(99,102,241,0.18);
  border-bottom-left-radius: 4px;
  color: var(--text-2);
}
.chat-bubble--thinking {
  display: flex; flex-direction: row; align-items: center;
  padding: 10px 16px;
}
.chat-text { color: inherit; }
.chat-text strong { color: #fff; }
.chat-text em { color: var(--text-2); }
.chat-text ul, .chat-text ol { padding-left: 18px; margin: 4px 0; }
.chat-text li { margin: 2px 0; }
.chat-time {
  font-size: 9.5px; color: var(--text-3); align-self: flex-end;
  letter-spacing: 0.3px; margin-top: 2px;
}

/* Typing dots animation */
.chat-dots { display: flex; gap: 4px; align-items: center; }
.chat-dots span {
  width: 6px; height: 6px; border-radius: 50%;
  background: rgba(99,102,241,0.70);
  animation: chatDotBounce 1.2s ease-in-out infinite;
}
.chat-dots span:nth-child(2) { animation-delay: 0.18s; }
.chat-dots span:nth-child(3) { animation-delay: 0.36s; }
@keyframes chatDotBounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
  40%           { transform: translateY(-5px); opacity: 1; }
}

/* Kritik uyarı şeridi */
.chat-uyari {
  display: flex; flex-direction: column; gap: 3px; margin-top: 6px;
  padding: 7px 10px;
  background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.18);
  border-radius: 8px;
}
.chat-uyari span { font-size: 11px; color: #fca5a5; }

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
@keyframes kpPulse        { 0%,100% { opacity:1; box-shadow:0 0 0 0 rgba(239,68,68,0.4); } 50% { opacity:0.7; box-shadow:0 0 0 5px rgba(239,68,68,0); } }
@keyframes kpSlideUp      { from { opacity:0; transform:translateY(16px) scale(0.97); } to { opacity:1; transform:translateY(0) scale(1); } }
@keyframes pulseBtn       { 0% { box-shadow: 0 0 0 0 var(--primary-glow); } 70% { box-shadow: 0 0 0 16px transparent; } 100% { box-shadow: 0 0 0 0 transparent; } }
@keyframes containerEntry { from { opacity:0; transform:translateY(20px) scale(0.98); } to { opacity:1; transform:translateY(0) scale(1); } }
@keyframes shimmer        { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }

.animate-in    { animation: fadeInUp 0.4s var(--ease) both; }
.animate-scale { animation: scaleIn 0.35s var(--ease-bounce) both; }

/* ══════════════════════════════════════════════════════
   PREMIUM AUTH OVERLAY — Dark SaaS (Linear / Vercel DNA)
   ══════════════════════════════════════════════════════ */
#auth-overlay {
  position: fixed; top:0; left:0; width:100vw; height:100vh;
  background: #030712;
  display: flex;
  z-index: 5000;
  overflow: hidden;
}

/* Grid background */
#auth-overlay::before {
  content: '';
  position: absolute; inset: 0; z-index: 0; pointer-events: none;
  background-image: radial-gradient(circle,rgba(255,255,255,0.055) 1px,transparent 1px);
  background-size: 28px 28px;
}

/* Aurora glow blobs */
.auth-glow-1 {
  position: absolute; z-index: 0; pointer-events: none; border-radius: 50%;
  width: 65vw; height: 55vw; top: -25%; left: -15%;
  background: radial-gradient(circle, rgba(99,102,241,0.16) 0%, transparent 70%);
  filter: blur(80px);
  animation: authBlob1 12s ease-in-out infinite alternate;
}
.auth-glow-2 {
  position: absolute; z-index: 0; pointer-events: none; border-radius: 50%;
  width: 50vw; height: 45vw; bottom: -15%; right: -10%;
  background: radial-gradient(circle, rgba(249,115,22,0.12) 0%, transparent 70%);
  filter: blur(80px);
  animation: authBlob2 10s ease-in-out infinite alternate;
}
@keyframes authBlob1 { from { transform: translate(0,0) scale(1); } to { transform: translate(30px,20px) scale(1.05); } }
@keyframes authBlob2 { from { transform: translate(0,0) scale(1); } to { transform: translate(-20px,15px) scale(1.08); } }

/* Brand panel (left half) */
.auth-brand-panel {
  flex: 1;
  display: flex; flex-direction: column; justify-content: center;
  padding: 60px 56px;
  position: relative; z-index: 1;
  border-right: 1px solid rgba(255,255,255,0.05);
}
.auth-logo {
  font-family: 'Poppins', sans-serif;
  font-size: 22px; font-weight: 900; letter-spacing: -0.5px;
  color: #fff; margin-bottom: 56px;
}
.auth-logo span { color: var(--amber); }
.auth-brand-h {
  font-size: clamp(28px, 3vw, 44px);
  font-weight: 800; color: #fff;
  letter-spacing: -1.5px; line-height: 1.15;
  margin-bottom: 16px;
}
.auth-brand-sub {
  font-size: 15px; color: var(--text-2);
  line-height: 1.7; max-width: 380px; margin-bottom: 48px;
}
.auth-brand-feats { display: flex; flex-direction: column; gap: 16px; margin-bottom: 56px; }
.auth-brand-feat {
  display: flex; align-items: flex-start; gap: 14px;
}
.auth-feat-check {
  width: 22px; height: 22px; flex-shrink: 0; margin-top: 1px;
  background: rgba(249,115,22,0.12);
  border: 1px solid rgba(249,115,22,0.25);
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  color: var(--amber); font-size: 12px; font-weight: 800;
}
.auth-feat-text { font-size: 14px; color: var(--text-2); line-height: 1.5; }
.auth-feat-text strong { color: var(--text-1); font-weight: 600; }
.auth-brand-mini-stats { display: flex; gap: 32px; }
.auth-mini-stat-val {
  font-size: 28px; font-weight: 800; color: #fff; line-height: 1;
}
.auth-mini-stat-val.amber { color: var(--amber); }
.auth-mini-stat-lbl { font-size: 11px; color: var(--text-3); margin-top: 4px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }

/* Form panel (right half) */
.auth-form-panel {
  flex: 1;
  display: flex; align-items: flex-start; justify-content: center;
  padding: 40px 48px;
  position: relative; z-index: 1;
  overflow-y: auto;
}
.auth-form-panel::-webkit-scrollbar { width: 4px; }
.auth-form-panel::-webkit-scrollbar-track { background: transparent; }
.auth-form-panel::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }

/* Glassmorphic Card */
.auth-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.055) 0%, rgba(255,255,255,0.02) 100%);
  backdrop-filter: blur(32px); -webkit-backdrop-filter: blur(32px);
  border: 1px solid rgba(255,255,255,0.08);
  border-top: 1px solid rgba(255,255,255,0.16);
  border-radius: 24px;
  padding: 48px 40px;
  width: 100%; max-width: 440px;
  margin-top: auto; margin-bottom: auto; align-self: center;
  box-shadow:
    0 40px 80px rgba(0,0,0,0.6),
    inset 0 1px 0 rgba(255,255,255,0.1),
    0 0 0 1px rgba(249,115,22,0.04);
  animation: authCardIn 0.7s cubic-bezier(0.16,1,0.3,1) both;
}
@keyframes authCardIn {
  from { opacity: 0; transform: translateY(28px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0)   scale(1); }
}
.auth-card h2 {
  color: #fff; margin-bottom: 6px; font-weight: 800;
  letter-spacing: -0.8px; font-size: 1.6rem; text-align: left;
}
.auth-card-sub { font-size: 14px; color: var(--text-2); margin-bottom: 28px; }

/* Premium Tabs */
.auth-tabs {
  display: flex; margin-bottom: 28px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px; padding: 4px; gap: 4px;
}
.auth-tab {
  flex: 1; padding: 10px 0;
  background: transparent; border: none; color: var(--text-2);
  cursor: pointer; font-weight: 600; font-size: 0.875rem;
  border-radius: 8px; transition: all 0.25s; font-family: var(--font);
}
.auth-tab.active {
  background: rgba(249,115,22,0.15);
  color: var(--amber);
  box-shadow: 0 0 0 1px rgba(249,115,22,0.2);
}

/* Premium Inputs */
.auth-input {
  width: 100%; background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px; padding: 13px 16px; color: #fff;
  font-size: 0.95rem; outline: none; margin-bottom: 12px;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
  box-sizing: border-box; font-family: var(--font);
}
.auth-input::placeholder { color: rgba(255,255,255,0.25); }
.auth-input:focus {
  border-color: rgba(249,115,22,0.5);
  background: rgba(249,115,22,0.04);
  box-shadow: 0 0 0 3px rgba(249,115,22,0.08);
}

/* Premium CTA Button */
.auth-btn {
  width: 100%; padding: 15px;
  background: var(--amber);
  color: #000; border: none; border-radius: 10px;
  font-weight: 700; font-size: 1rem; cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16,1,0.3,1);
  font-family: var(--font); letter-spacing: 0.01em;
  box-shadow: 0 0 28px rgba(249,115,22,0.38), 0 6px 18px rgba(0,0,0,0.25);
}
.auth-btn:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 0 44px rgba(249,115,22,0.58), 0 8px 24px rgba(0,0,0,0.3);
}
.auth-btn:active { transform: translateY(0) scale(0.99); }

/* Language Buttons */
.auth-lang-row { display: flex; justify-content: flex-end; gap: 6px; margin-bottom: 20px; }
.auth-lang-btn {
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px; padding: 5px 12px; color: var(--text-2);
  cursor: pointer; font-size: 0.8rem; font-weight: 700; transition: all 0.2s;
  font-family: var(--font);
}
.auth-lang-btn.active-lang {
  border-color: rgba(249,115,22,0.4); color: var(--amber);
  background: rgba(249,115,22,0.08);
}

/* Responsive: hide brand panel on small screens */
@media(max-width: 900px) {
  .auth-brand-panel { display: none; }
  .auth-form-panel { padding: 24px 20px; }
  .auth-card { padding: 36px 28px; }
  #auth-overlay { align-items: flex-start; overflow-y: auto; }
}
@media(max-width: 480px) {
  .auth-card { padding: 28px 20px; border-radius: 20px; }
}

.auth-btn { color: #000 !important; }

/* ── ORANGE HIGHLIGHT — Premium turuncu kelime vurgusu ── */
.orange-highlight {
  color: #F97316;
  text-shadow:
    0 0 32px rgba(249,115,22,0.50),
    0 0 64px rgba(249,115,22,0.22),
    0 0 100px rgba(249,115,22,0.10);
}

/* ── GOOGLE SIGN-IN BUTTON ── */
.google-btn {
  width: 100%;
  display: flex; align-items: center; justify-content: center; gap: 12px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 10px; padding: 13px 20px;
  color: #fff; font-size: 14px; font-weight: 600;
  cursor: pointer; letter-spacing: 0.01em;
  transition: all 0.25s cubic-bezier(0.16,1,0.3,1);
  font-family: var(--font); margin-bottom: 16px;
}
.google-btn:hover {
  background: rgba(255,255,255,0.08);
  border-color: rgba(255,255,255,0.26);
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.google-btn:active { transform: translateY(0); }

/* ── AUTH DIVIDER ── */
.auth-divider {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 20px; color: rgba(255,255,255,0.2);
  font-size: 12px; font-weight: 500;
}
.auth-divider::before, .auth-divider::after {
  content: ''; flex: 1; height: 1px;
  background: rgba(255,255,255,0.07);
}

/* ── FORGOT LINK ── */
.auth-forgot-link {
  font-size: 13px; color: rgba(255,255,255,0.35);
  text-decoration: none; cursor: pointer;
  transition: color 0.2s;
}
.auth-forgot-link:hover { color: var(--amber); }

/* ── PREMIUM PLAN CHIPS ── */
.plan-section-label {
  font-size: 11px; font-weight: 700; color: rgba(255,255,255,0.35);
  text-transform: uppercase; letter-spacing: 0.1em;
  margin: 20px 0 10px;
}
.plan-chips {
  display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px;
}
.plan-chip {
  display: flex; align-items: center; gap: 14px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px; padding: 14px 16px;
  cursor: pointer;
  transition: border-color 0.22s, background 0.22s, transform 0.2s;
  user-select: none;
}
.plan-chip:hover {
  border-color: rgba(249,115,22,0.22);
  background: rgba(249,115,22,0.04);
  transform: translateX(2px);
}
.plan-chip.selected {
  border-color: rgba(249,115,22,0.45);
  background: rgba(249,115,22,0.08);
  box-shadow: 0 0 0 1px rgba(249,115,22,0.1);
}
/* Radio dot */
.plan-chip-radio {
  width: 18px; height: 18px; border-radius: 50%; flex-shrink: 0;
  border: 2px solid rgba(255,255,255,0.18);
  position: relative; transition: border-color 0.2s;
}
.plan-chip.selected .plan-chip-radio { border-color: var(--amber); }
.plan-chip.selected .plan-chip-radio::after {
  content: ''; position: absolute; inset: 3px;
  background: var(--amber); border-radius: 50%;
}
/* Body */
.plan-chip-body { flex: 1; min-width: 0; }
.plan-chip-name {
  font-size: 14px; font-weight: 700; color: #fff;
  display: flex; align-items: center; gap: 8px; margin-bottom: 2px;
}
.plan-chip-desc { font-size: 11.5px; color: rgba(255,255,255,0.38); line-height: 1.4; }
.plan-chip-badge {
  font-size: 9.5px; font-weight: 700; color: var(--amber);
  background: rgba(249,115,22,0.12); border: 1px solid rgba(249,115,22,0.22);
  border-radius: 4px; padding: 1px 7px; text-transform: uppercase; letter-spacing: 0.08em;
}
/* Price */
.plan-chip-price {
  font-size: 15px; font-weight: 800; color: #fff; flex-shrink: 0; white-space: nowrap;
}
.plan-chip-price span { font-size: 11px; color: rgba(255,255,255,0.35); font-weight: 400; }
.plan-chip.selected .plan-chip-price { color: var(--amber); }

/* ── GSAP PANEL TRANSITION HELPERS ── */
.auth-panel-wrap { overflow: hidden; }
[id^="panel-"] { will-change: opacity, transform; }

/* ── MODAL SYSTEM ── */
.modal-overlay {
  position: fixed; top:0; left:0; width:100%; height:100%;
  background: rgba(15,23,42,0.7); backdrop-filter: blur(8px);
  display: none; align-items: center; justify-content: center;
  z-index: 3000; opacity:0; transition: opacity 0.25s ease;
  padding: 16px; box-sizing: border-box;
}
.modal-overlay.active { display: flex; opacity:1; }
.modal-content {
  background: #FFFFFF;
  border-radius: 20px; width: 100%; max-width: 440px;
  box-shadow: 0 24px 64px rgba(0,0,0,0.3); transform: translateY(24px) scale(0.97);
  transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1);
  overflow: hidden; display: flex; flex-direction: column;
  max-height: 92vh;
}
.modal-overlay.active .modal-content { transform: translateY(0) scale(1); }
.modal-header {
  background: #0D1117; padding: 16px 20px;
  display: flex; align-items: center; justify-content: space-between; flex-shrink: 0;
}
.modal-header-title { color: #F1F5F9; font-weight: 700; font-size: 1rem; }
.modal-header-close {
  background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
  color: #94A3B8; width: 30px; height: 30px; border-radius: 8px;
  cursor: pointer; font-size: 1rem; display: flex; align-items: center; justify-content: center;
  transition: background 0.15s;
}
.modal-header-close:hover { background: rgba(255,255,255,0.18); color: #fff; }
.modal-body { padding: 20px; overflow-y: auto; flex: 1; }
.modal-field-label {
  display: block; font-size: 0.78rem; font-weight: 600; color: #374151; margin-bottom: 6px; margin-top: 14px;
}
.modal-field-label:first-child { margin-top: 0; }
.modal-input {
  width: 100%; background: #F8FAFC; border: 1.5px solid #E2E8F0;
  border-radius: 10px; padding: 11px 14px; color: #0F172A;
  font-size: 0.95rem; outline: none; transition: all 0.2s ease;
  box-sizing: border-box; font-family: var(--font);
}
.modal-input:focus { border-color: #F97316; background: #FFF7ED; box-shadow: 0 0 0 3px rgba(249,115,22,0.1); }
.modal-result {
  display: none; background: #F8FAFC; border: 1.5px solid #E2E8F0;
  border-radius: 12px; padding: 16px; margin-top: 16px;
}
.modal-result.visible { display: block; }
.modal-result-value {
  font-size: 1.6rem; font-weight: 800; color: #0F172A; margin-bottom: 4px;
}
.modal-result-detail { font-size: 0.82rem; color: #64748B; line-height: 1.5; }
.modal-footer { display: flex; gap: 10px; padding: 16px 20px; background: #F8FAFC; border-top: 1px solid #E2E8F0; flex-shrink: 0; }
.modal-btn { flex:1; padding: 12px; border-radius: 10px; border: none; cursor: pointer; font-weight: 700; font-size: 0.9rem; transition: all 0.15s ease; font-family: var(--font); letter-spacing: 0.02em; }
.btn-confirm { background: #F97316; color: white; box-shadow: 0 2px 8px rgba(249,115,22,0.3); }
.btn-confirm:hover { background: #EA6C0A; transform: translateY(-1px); box-shadow: 0 4px 14px rgba(249,115,22,0.4); }
.btn-cancel { background: #F1F5F9; color: #64748B; border: 1px solid #E2E8F0; }
.btn-cancel:hover { background: #E2E8F0; color: #334155; }

/* ── MÜHENDİSLİK PANELİ SIDEBAR ── */
#sidebarPanel {
  position: fixed; right: -460px; top: 0;
  width: 400px; height: 100vh;
  background: #F8FAFC;
  border-left: 1px solid #E2E8F0;
  padding: 0;
  transition: right 0.35s cubic-bezier(0.4,0,0.2,1); z-index: 2000; overflow-y: auto;
  box-shadow: -8px 0 32px rgba(0,0,0,0.12);
  display: flex; flex-direction: column;
}
#sidebarPanel.active { right: 0; }
.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(15,23,42,0.4);
  z-index: 1999;
  pointer-events: none;
}
.sidebar-overlay.active { display: block; pointer-events: all; }

/* ── TOOL CARDS ── */
.category-title {
  color: #94A3B8; font-size: 0.68rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1.5px; margin: 20px 16px 8px; padding-left: 0;
}
.tool-card {
  background: #FFFFFF; border: 1px solid #E2E8F0;
  border-radius: 12px; padding: 14px 16px; margin: 0 16px 8px;
  cursor: pointer; transition: all 0.15s ease;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.tool-card:hover { border-color: #6366F1; background: #EEF2FF; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(99,102,241,0.12); }
.tool-card h4 { font-size: 0.9rem; margin:0 0 2px; color:#1E293B; font-weight:700; }
.tool-card small { font-size: 0.75rem; color:#64748B; margin:0; }

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
#santiyeFormModal > div {
  background: #FFFFFF !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  border: none !important;
  box-shadow: 0 24px 64px rgba(0,0,0,0.25) !important;
}
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
  background: rgba(255,255,255,0.03) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border-bottom: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 16px 16px 0 0 !important;
  padding: 22px 28px !important;
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
  background: rgba(255,255,255,0.03) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border-bottom: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 16px 16px 0 0 !important;
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

/* ── GÜVENLİK MODALI — LIGHT THEME ── */
.gv-tab {
  flex: 1;
  padding: 10px 4px 8px;
  border: none;
  background: transparent;
  color: #64748B;
  font-size: 10.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all .15s;
  font-family: var(--font);
  text-align: center;
  line-height: 1.5;
  min-width: 60px;
  white-space: nowrap;
}
.gv-tab:hover { background: #F1F5F9; }
.gv-tab.active { background: #0D1117; color: white; }

.gv-tab-content { display: block; }

.gv-check-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 0;
  border-bottom: 1px solid #F1F5F9;
  cursor: pointer;
  transition: opacity .15s;
}
.gv-check-item:last-child { border-bottom: none; }
.gv-check-item[data-checked="1"] { opacity: 0.65; }

.gv-item-icon {
  width: 34px; height: 34px;
  border-radius: 8px;
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.gv-item-body { flex: 1; min-width: 0; }
.gv-item-name { font-size: 12.5px; color: #0F172A; font-weight: 600; }
.gv-item-sub { font-size: 11px; color: #94A3B8; margin-top: 2px; }

.gv-ctrl-btn {
  background: #0D1117;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 5px 11px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
  font-family: var(--font);
  transition: background .15s;
  pointer-events: none;
}
.gv-ctrl-btn-ok { background: #16A34A !important; }

/* Legacy g-* classes kept for any older references */
.g-tab { display: none; }
.g-check-item { display: none; }
.g-tab-content { display: none; }

/* ── DASHBOARD KPI CARDS ── */
.dash-kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 18px;
}
.kpi-card {
  background: rgba(6, 13, 31, 0.65);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.08);
  border-top: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--radius-md);
  padding: 18px 16px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  transition: all 0.25s var(--ease);
  cursor: default;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(0,0,0,0.30), inset 0 1px 0 rgba(255,255,255,0.04);
}
.kpi-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 80% 60% at 10% 0%, var(--kc-a, rgba(249,115,22,0.05)) 0%, transparent 70%);
  pointer-events: none;
}
.kpi-card:hover {
  border-color: rgba(99,102,241,0.22);
  border-top-color: rgba(99,102,241,0.35);
  transform: translateY(-2px);
  box-shadow: 0 12px 36px rgba(0,0,0,0.40), 0 0 0 1px rgba(99,102,241,0.10);
}
.kpi-plan-card { cursor: pointer; }
.kpi-plan-card:hover { border-color: rgba(249,115,22,0.35); }
.kpi-icon-wrap {
  width: 40px; height: 40px;
  border-radius: 10px;
  background: #0D1117;
  border: 1px solid rgba(255,255,255,0.08);
  display: flex; align-items: center; justify-content: center;
  color: var(--kc, #f97316);
  flex-shrink: 0;
  padding: 8px;
}
.kpi-body { flex: 1; min-width: 0; }
.kpi-val {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-1);
  line-height: 1.1;
  margin-bottom: 4px;
  letter-spacing: -0.03em;
}
.kpi-lbl {
  font-size: 11px;
  color: var(--text-2);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.kpi-bar-wrap {
  height: 3px;
  background: rgba(255,255,255,0.06);
  border-radius: 2px;
  margin-top: 10px;
  overflow: hidden;
}
.kpi-bar {
  height: 100%;
  border-radius: 2px;
  transition: width 0.8s cubic-bezier(0.16,1,0.3,1);
}
@media(max-width:1100px) {
  .dash-kpi-grid { grid-template-columns: repeat(2,1fr); }
}
@media(max-width:600px) {
  .dash-kpi-grid { grid-template-columns: 1fr 1fr; gap:10px; }
  .kpi-val { font-size:1.2rem; }
}

/* ══════════════════════════════════════════════════════════════
   MOBİL UYUMLULUK — KAPSAMLI RESPONSIVE OVERRIDES
   Breakpoints: 900px (tablet), 600px (phone), 400px (small phone)
   ══════════════════════════════════════════════════════════════ */

/* ── AUTH MOBİL LOGO ── */
.auth-mobile-logo {
  display: none;
  text-align: center;
  font-size: 22px;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
  margin-bottom: 24px;
  padding-top: 8px;
}
.auth-mobile-logo span { color: var(--amber); }

@media(max-width: 900px) {
  /* Show mini logo, hide brand panel */
  .auth-mobile-logo { display: block; }

  /* Form panel takes full width */
  #auth-overlay {
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding: 32px 0 48px;
    overflow-y: auto;
  }
  .auth-form-panel {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0 24px;
  }
  .auth-card {
    width: 100%;
    max-width: 480px;
  }
}

@media(max-width: 600px) {
  .auth-form-panel { padding: 0 16px; }
  .auth-card {
    width: 95%;
    max-width: 100%;
    padding: 28px 20px;
    border-radius: 20px;
  }
  /* Plan chips — stack vertically, taller touch target */
  .plan-chips { gap: 8px; }
  .plan-chip {
    flex-direction: row;
    padding: 14px 14px;
    gap: 10px;
    min-height: 60px;
  }
  .plan-chip-body { flex: 1; }
  .plan-chip-name { font-size: 13px; }
  .plan-chip-desc { font-size: 11px; }
  .plan-chip-price { font-size: 15px; white-space: nowrap; }

  /* Touch-friendly input & button sizing */
  .auth-input {
    min-height: 50px;
    font-size: 16px; /* prevents iOS auto-zoom on focus */
    padding: 14px 16px;
  }
  .auth-btn {
    min-height: 52px;
    font-size: 15px;
    padding: 16px 24px;
  }
  .google-btn {
    min-height: 50px;
    font-size: 14px;
    padding: 14px 20px;
  }
  .auth-tabs { gap: 4px; padding: 4px; }
  .auth-tab { padding: 9px 16px; font-size: 13px; }
  .auth-mobile-logo { font-size: 20px; margin-bottom: 20px; }
}

@media(max-width: 400px) {
  .auth-card { padding: 22px 16px; border-radius: 16px; }
  .auth-mobile-logo { font-size: 18px; }
  .plan-chip { padding: 12px 12px; }
}

/* ── DASHBOARD PANEL MOBİL ── */
@media(max-width: 768px) {
  /* Ana butonlar için dokunma alanı */
  button, .btn, [role="button"] { min-height: 42px; }
  /* Modal içerikleri tam genişlik */
  .modal-content, .modal-inner {
    width: 95vw !important;
    max-width: 95vw !important;
    padding: 20px 16px !important;
  }
}

/* ── ŞANTİYELERİM KART & PROGRESS ── */
.s-kart {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 22px;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
  position: relative;
  overflow: hidden;
}
.s-kart::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, #6366f1, #f97316);
  opacity: 0;
  transition: opacity 0.25s ease;
}
.s-kart:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(99,102,241,0.15);
  border-color: rgba(99,102,241,0.30);
}
.s-kart:hover::before { opacity: 1; }

.s-progress-bar-track {
  height: 6px;
  background: rgba(255,255,255,0.08);
  border-radius: 99px;
  overflow: hidden;
  margin-top: 10px;
}
.s-progress-bar {
  height: 100%;
  border-radius: 99px;
  width: 0%;
  transition: width 1.1s cubic-bezier(0.4,0,0.2,1);
}

/* ── GSAP MOBİL PERFORMANS ── */
@media(max-width: 768px) and (prefers-reduced-motion: no-preference) {
  /* Animasyonlu elementlerin GPU katmanı hint'i */
  [id^="panel-"],
  .auth-card,
  .auth-mobile-logo {
    will-change: opacity, transform;
    backface-visibility: hidden;
  }
}
@media(prefers-reduced-motion: reduce) {
  /* Hareket hassasiyeti olan kullanıcılar için animasyonları kapat */
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* ── AI OMNI-COMMAND BAR ── */
#aiCommandInput::placeholder {
  color: rgba(255,255,255,0.25) !important;
}
#aiCommandInput:focus {
  color: #F1F5F9 !important;
}
@keyframes aiBounce {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-5px); }
}
/* mainArea flex düzeni: command bar + content */
#aiCommandBar {
  flex-shrink: 0;
}
/* content yüksekliğini flex'e bırak (command bar eklenince overflow önlenir) */
#mainArea > #content {
  height: auto !important;
  flex: 1;
}
/* Mobil: command bar input daralt */
@media (max-width: 600px) {
  #aiBarInner {
    padding: 6px 8px;
    gap: 6px;
  }
  #aiCommandInput {
    font-size: 13px;
  }
  #aiSendBtn {
    padding: 5px 8px;
  }
}

/* ══════════════════════════════════════
   DASHBOARD LIGHT THEME — SCREENSHOT MATCH
   ══════════════════════════════════════ */

/* 1) Glassmorphism sıfırla */
*, *::before, *::after {
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

/* 2) Body */
body {
  background-color: #F1F5F9 !important;
  background-image: none !important;
  color: #0F172A !important;
}
body::before { display: none !important; }
.bg-glow-1, .bg-glow-2, .bg-glow-3 { display: none !important; }
#bgCanvas { display: none !important; }

/* 3) Global topbar → tamamen gizle (logo sidebar'a taşındı) */
#topbar { display: none !important; }

/* 4) Layout: sidebar + mainArea full height (topbar olmadan) */
#app { flex-direction: row !important; height: 100vh !important; }
#bodyRow { flex: 1; display: flex; overflow: hidden; height: 100vh; }

/* 5) Sidebar — screenshot'taki gibi dark, clean */
#sidebar {
  width: 220px !important;
  background: #0D1117 !important;
  border-right: 1px solid #1E293B !important;
  display: flex; flex-direction: column;
  height: 100vh; overflow-y: auto; overflow-x: hidden;
  flex-shrink: 0;
  padding: 0 !important;
}
#sidebar::-webkit-scrollbar { width: 0; }

/* Sidebar logo header */
#sidebarLogoBar {
  padding: 20px 16px 14px;
  border-bottom: 1px solid #1E293B;
  flex-shrink: 0;
}
#sidebarLogoBar .sb-brand { font-size: 16px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.3px; }
#sidebarLogoBar .sb-brand-sub { font-size: 11px; color: #475569; margin-top: 2px; font-weight: 400; }

/* Nav items — screenshot style */
.nav-item {
  display: flex; align-items: center; gap: 10px;
  margin: 2px 10px; padding: 10px 12px;
  font-size: 13px; font-weight: 500; color: #64748B;
  cursor: pointer; border-radius: 10px;
  transition: all 0.15s; user-select: none; white-space: nowrap;
  border: none !important; box-shadow: none !important;
}
.nav-item:hover {
  color: #94A3B8 !important;
  background: #111827 !important;
  box-shadow: none !important;
}
.nav-item.active {
  color: #0F172A !important;
  background: #FFFFFF !important;
  font-weight: 600 !important;
  border-radius: 10px !important;
  box-shadow: 0 1px 4px rgba(0,0,0,0.15) !important;
}
.nav-item .nav-icon { font-size: 15px; width: 18px; text-align: center; flex-shrink: 0; }
.sb-section-title {
  font-size: 10px; font-weight: 600; color: #334155;
  letter-spacing: 0.1em; text-transform: uppercase;
  padding: 12px 16px 4px;
}
.sb-fill { flex: 1; }
.sb-foot { padding: 10px 10px 16px; flex-shrink: 0; border-top: 1px solid #1E293B; }
.sb-upgrade {
  background: #111827;
  border: 1px solid #1E293B;
  border-radius: 10px; padding: 10px 12px;
  cursor: pointer; transition: 0.2s;
}
.sb-upgrade:hover { background: #1E293B; }
.sb-upgrade-title { font-size: 12px; font-weight: 600; color: #F97316; }
.sb-upgrade-sub { font-size: 11px; color: #475569; margin-top: 2px; }

/* 6) mainArea */
#mainArea { flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #F1F5F9; }

/* 7) Content header — white bar inside mainArea */
#contentHeader {
  background: #FFFFFF;
  border-bottom: 1px solid #E2E8F0;
  padding: 16px 24px;
  display: flex; align-items: center; justify-content: space-between;
  flex-shrink: 0;
  min-height: 64px;
}

/* 8) AI Command Bar */
#aiCommandBar {
  background: #FFFFFF !important;
  border-bottom: 1px solid #E2E8F0 !important;
  padding: 12px 24px !important;
}
#aiBarInner {
  background: #F8FAFC !important;
  border: 1.5px solid #E2E8F0 !important;
  border-radius: 10px !important;
  max-width: 100% !important;
}
#aiBarInner:focus-within {
  border-color: #3B82F6 !important;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.10) !important;
}
#aiCommandInput { color: #0F172A !important; }
#aiCommandInput::placeholder { color: #94A3B8 !important; }
#aiQuickChips { margin-top: 8px !important; }
#aiResultBanner { background: #F8FAFC !important; border-color: #E2E8F0 !important; max-width: 100% !important; }
#aiQuickCommands { background: #FFFFFF !important; border-color: #E2E8F0 !important; box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important; max-width: 100% !important; }

/* 9) Content area */
#content {
  flex: 1; padding: 20px 24px !important;
  flex-direction: column !important;
  gap: 16px !important; overflow-y: auto;
  background: #F1F5F9 !important;
  height: auto !important;
}
#content::-webkit-scrollbar { width: 4px; }
#content::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 2px; }

/* Modal scrollbar — turuncu override sıfırla */
#santiyeFormModal ::-webkit-scrollbar { width: 4px; }
#santiyeFormModal ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
#santiyeFormModal ::-webkit-scrollbar-track { background: transparent; }
#santiyeModal ::-webkit-scrollbar { width: 4px; }
#santiyeModal ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }

/* 10) KPI kartlar */
.kpi-card {
  background: #FFFFFF !important;
  border: 1px solid #E2E8F0 !important;
  border-top: none !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
  color: #0F172A !important;
  transition: box-shadow 0.15s !important;
}
.kpi-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
  border-color: #CBD5E1 !important;
}
.kpi-val { color: inherit !important; }
.kpi-lbl { color: #64748B !important; }

/* 11) Legacy quick-btn */
.quick-btn, .quick-btn:hover { background: transparent !important; border: none !important; box-shadow: none !important; }
.quick-btn-label { color: #64748B !important; }
.quick-sub-btn { background: #F8FAFC !important; border: 1px solid #E2E8F0 !important; color: #475569 !important; }

/* 12) Saha günlüğü row hover */
.saha-row:hover { background: #F8FAFC !important; }

/* 13) Şantiye Sayfası Kartları */
.sp-kart-horiz {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 14px;
  display: flex;
  gap: 14px;
  cursor: pointer;
  transition: box-shadow 0.15s, transform 0.15s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.sp-kart-horiz:hover {
  box-shadow: 0 6px 20px rgba(0,0,0,0.10);
  transform: translateY(-1px);
}
.sp-kart-vert {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.15s, transform 0.15s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.sp-kart-vert:hover {
  box-shadow: 0 6px 20px rgba(0,0,0,0.10);
  transform: translateY(-2px);
}
.sp-img {
  border-radius: 8px;
  object-fit: cover;
  background: linear-gradient(135deg, #1E293B, #334155);
  display: flex; align-items: center; justify-content: center;
  font-size: 28px; color: rgba(255,255,255,0.5);
  flex-shrink: 0;
}
.sp-progress-bar {
  height: 5px;
  border-radius: 3px;
  background: #F1F5F9;
  overflow: hidden;
  margin: 8px 0 4px;
}
.sp-progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s ease;
}
.sp-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 20px;
  margin-top: 4px;
}

/* ── GÜNLÜK RAPOR MODAL — LIGHT THEME OVERRIDES ── */
#gunlukRaporModal input:not([type="checkbox"]):not([type="file"]):not([style*="display:none"]),
#gunlukRaporModal textarea,
#gunlukRaporModal select:not([style*="display:none"]) {
  color: #0F172A !important;
  background: #FFFFFF !important;
  border: 1.5px solid #CBD5E1 !important;
  border-radius: 10px !important;
}
#gunlukRaporModal input[type="date"],
#gunlukRaporModal input[type="number"] {
  border: none !important;
  border-radius: 0 !important;
  background: transparent !important;
}
#gunlukRaporModal input[type="checkbox"] {
  border: none !important;
  background: transparent !important;
}
#gunlukRaporModal input::placeholder,
#gunlukRaporModal textarea::placeholder { color: #94A3B8 !important; }
#gunlukRaporModal input:focus,
#gunlukRaporModal textarea:focus,
#gunlukRaporModal select:focus {
  border-color: #64748B !important;
  box-shadow: 0 0 0 3px rgba(100,116,139,0.1) !important;
  outline: none !important;
}
#gunlukRaporModal .gr-field-wrap {
  border: 1.5px solid #CBD5E1;
  border-radius: 10px;
  overflow: hidden;
  background: #FFFFFF;
  display: flex;
  align-items: center;
}
#gunlukRaporModal .gr-field-icon {
  padding: 0 12px;
  border-right: 1.5px solid #CBD5E1;
  color: #64748B;
  font-size: 1rem;
  height: 42px;
  display: flex;
  align-items: center;
  flex-shrink: 0;
  background: #F8FAFC;
}
#gunlukRaporModal textarea {
  min-height: 90px;
  resize: vertical;
  padding: 10px 12px !important;
  font-size: 0.85rem !important;
  line-height: 1.5;
  font-family: inherit !important;
  box-sizing: border-box;
  width: 100%;
}
#gunlukRaporModal label {
  color: #374151 !important;
}
#gunlukRaporModal ::-webkit-scrollbar-thumb { background: #CBD5E1; }

/* 14) Mobil */
@media (max-width: 768px) {
  #sidebar { width: 180px !important; }
  #content { padding: 14px !important; gap: 12px !important; }
  #dashKpiGrid { grid-template-columns: 1fr !important; }
  #contentHeader { padding: 12px 16px !important; }
  #santiyePageOzet { grid-template-columns: repeat(2,1fr) !important; }
  #santiyePageHoriz { grid-template-columns: 1fr !important; }
  #santiyePageGrid  { grid-template-columns: repeat(2,1fr) !important; }
}
</style>
"""
