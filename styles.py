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
  position: relative;
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
.tb-logo-img {
  width: 38px; height: 38px; object-fit: contain;
}

/* ── BAI LOGO (global) ── */
.bai-logo {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
}
.bai-logo-icon {
  height: 48px;
  width: auto;
}
.bai-logo-text {
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 32px;
  letter-spacing: -0.5px;
  line-height: 1;
}
.bai-logo-text .building {
  color: #1a1a1a;
}
.bai-logo-text .ai {
  color: #e6743b;
}
[data-theme="dark"] .bai-logo-text .building,
.dark .bai-logo-text .building {
  color: #ffffff;
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
.sb-section { padding: 12px 13px 4px; }
.sb-section-title {
  font-size: 11px; font-weight: 600; color: rgba(255, 255, 255, 0.25);
  letter-spacing: 0.12em; text-transform: uppercase;
  padding: 10px 14px 4px;
}
.nav-item {
  display: flex; align-items: center; gap: 9px;
  margin: 2px 8px; padding: 6px 12px;
  font-size: 13px; font-weight: 500; color: var(--text-2);
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
.sb-foot { padding: 6px 8px 10px; flex-shrink: 0; }
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
  padding: 7px 10px;
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
  isolation: isolate;
  pointer-events: auto;
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
  display: inline-flex;
  align-items: center;
}
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
  position: relative; z-index: 2;
  overflow-y: auto;
  pointer-events: auto;
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
  position: relative; z-index: 10;
  pointer-events: auto;
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
  pointer-events: auto; position: relative; z-index: 1;
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
  pointer-events: auto; position: relative; z-index: 1;
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
  pointer-events: auto; position: relative; z-index: 1;
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
  font-family: var(--font); pointer-events: auto; position: relative; z-index: 1;
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
  pointer-events: auto; position: relative; z-index: 1;
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
#profesyonelModal > div,
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
#profesyonelModal,
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

/* Stok sayfası — datalist dropdown okunu gizle */
#stokPage input[list]::-webkit-calendar-picker-indicator,
#stokPage input[list]::-webkit-list-button {
  display: none !important;
  width: 0 !important;
  opacity: 0 !important;
}

/* Stok geçmiş listesi */
#stokGecmisListe > div {
  background: white !important;
  border-bottom: 1px solid #F9FAFB !important;
}

/* AI Bar */
#stokAiBarInput::placeholder {
  color: #9CA3AF;
}
#stokAiBarInput:focus {
  border-color: #E37A45;
  box-shadow: 0 0 0 3px rgba(227,122,69,0.1);
}

/* Stok tablo scroll */
#stokListeSatirlar::-webkit-scrollbar,
#stokGecmisListe::-webkit-scrollbar { width: 4px; }
#stokListeSatirlar::-webkit-scrollbar-thumb,
#stokGecmisListe::-webkit-scrollbar-thumb {
  background: #E5E7EB;
  border-radius: 999px;
}
#stokListeSatirlar::-webkit-scrollbar-thumb:hover,
#stokGecmisListe::-webkit-scrollbar-thumb:hover {
  background: #D1D5DB;
}

/* Excel modal scrollbar */
#excelModalIcerik::-webkit-scrollbar { width: 4px; }
#excelModalIcerik::-webkit-scrollbar-thumb {
  background: #E5E7EB;
  border-radius: 999px;
}
#excelModalIcerik::-webkit-scrollbar-thumb:hover {
  background: #D1D5DB;
}

/* Stok liste satir hover */
#stokListeSatirlar > div {
  transition: background 0.12s ease;
}
#stokListeSatirlar > div:hover {
  background: #F9FAFB !important;
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
#sidebarLogoBar .bai-logo-icon { height: 36px; width: auto; flex-shrink: 0; }
#sidebarLogoBar .bai-logo-text { font-size: 18px; }
#sidebarLogoBar .building { color: #ffffff; }
#sidebarOrgName {
  font-size: 11px; color: #94A3B8; font-weight: 600;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  margin: 6px 0 0 44px;
}

/* Nav items — screenshot style */
.nav-item {
  display: flex; align-items: center; gap: 10px;
  margin: 2px 8px; padding: 6px 12px;
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
.sb-foot { padding: 6px 8px 10px; flex-shrink: 0; border-top: 1px solid #1E293B; }
.sb-upgrade {
  background: #111827;
  border: 1px solid #1E293B;
  border-radius: 10px; padding: 7px 10px;
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

/* 14) Engineer Dashboard */
.engineer-dashboard {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 18px;
  align-items: start;
  min-height: 100%;
}
.engineer-dashboard__main {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.engineer-stat-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}
.engineer-stat-card {
  appearance: none;
  border: 1px solid #1E293B;
  background:
    radial-gradient(circle at top right, rgba(249,115,22,0.14), transparent 42%),
    linear-gradient(180deg, #111827 0%, #0F172A 100%);
  border-radius: 18px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  color: #F8FAFC;
  text-align: left;
  cursor: pointer;
  transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 18px 40px rgba(2,6,23,0.18);
}
.engineer-stat-card:hover {
  transform: translateY(-2px);
  border-color: rgba(249,115,22,0.28);
  box-shadow: 0 24px 50px rgba(2,6,23,0.24);
}
.engineer-stat-card__icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
}
.engineer-stat-card__icon svg {
  width: 20px;
  height: 20px;
}
.engineer-stat-card__label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #94A3B8;
}
.engineer-stat-card__value {
  font-size: 36px;
  line-height: 1;
  font-weight: 800;
  letter-spacing: -0.04em;
}
.engineer-stat-card[data-tone="success"] .engineer-stat-card__value,
.engineer-stat-card[data-tone="success"] .engineer-stat-card__icon {
  color: #22C55E;
}
.engineer-stat-card[data-tone="warning"] .engineer-stat-card__value,
.engineer-stat-card[data-tone="warning"] .engineer-stat-card__icon {
  color: #F59E0B;
}
.engineer-panel,
.engineer-assistant__surface {
  border: 1px solid #1E293B;
  background: linear-gradient(180deg, rgba(15,23,42,0.98) 0%, rgba(10,15,29,0.98) 100%);
  border-radius: 20px;
  box-shadow: 0 22px 50px rgba(2,6,23,0.22);
}
.engineer-panel {
  overflow: hidden;
}
.engineer-panel__header {
  padding: 18px 20px 16px;
  border-bottom: 1px solid rgba(148,163,184,0.12);
}
.engineer-panel__title {
  font-size: 17px;
  font-weight: 800;
  color: #F8FAFC;
  letter-spacing: -0.02em;
}
.engineer-panel__subtitle {
  margin-top: 5px;
  font-size: 12px;
  color: #64748B;
}
.engineer-open-loops {
  padding: 10px 12px 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.engineer-loop-row {
  display: grid;
  grid-template-columns: auto minmax(0, 1.4fr) minmax(120px, 0.8fr) minmax(100px, 0.7fr) auto auto;
  gap: 12px;
  align-items: center;
  padding: 14px;
  border: 1px solid rgba(148,163,184,0.12);
  border-radius: 16px;
  background: rgba(15,23,42,0.72);
}
.engineer-loop-row__icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #F8FAFC;
  background: rgba(51,65,85,0.55);
  border: 1px solid rgba(148,163,184,0.14);
}
.engineer-loop-row__icon svg {
  width: 18px;
  height: 18px;
}
.engineer-loop-row__title {
  min-width: 0;
}
.engineer-loop-row__title strong {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: #F8FAFC;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.engineer-loop-row__title span,
.engineer-loop-row__meta {
  font-size: 12px;
  color: #64748B;
}
.engineer-loop-row__meta {
  white-space: nowrap;
}
.engineer-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
  border: 1px solid transparent;
}
.engineer-badge[data-tone="warning"] {
  background: rgba(245,158,11,0.12);
  color: #FBBF24;
  border-color: rgba(245,158,11,0.24);
}
.engineer-badge[data-tone="danger"] {
  background: rgba(239,68,68,0.12);
  color: #FCA5A5;
  border-color: rgba(239,68,68,0.24);
}
.engineer-badge[data-tone="success"] {
  background: rgba(34,197,94,0.12);
  color: #86EFAC;
  border-color: rgba(34,197,94,0.24);
}
.engineer-badge[data-tone="info"] {
  background: rgba(59,130,246,0.12);
  color: #93C5FD;
  border-color: rgba(59,130,246,0.24);
}
.engineer-loop-row__action,
.engineer-evidence-card__action,
.engineer-assistant__send,
.engineer-quick-action-btn {
  border: 1px solid transparent;
  border-radius: 12px;
  font-family: inherit;
  cursor: pointer;
  transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease, color 0.18s ease;
}
.engineer-loop-row__action,
.engineer-evidence-card__action {
  background: rgba(99,102,241,0.14);
  color: #C7D2FE;
  border-color: rgba(99,102,241,0.24);
  font-size: 12px;
  font-weight: 700;
  padding: 9px 12px;
  white-space: nowrap;
}
.engineer-loop-row__action:hover,
.engineer-evidence-card__action:hover,
.engineer-assistant__send:hover,
.engineer-quick-action-btn:hover {
  transform: translateY(-1px);
}
.engineer-evidence-grid {
  padding: 14px 18px 18px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}
.engineer-evidence-card {
  border: 1px solid rgba(148,163,184,0.12);
  border-radius: 18px;
  overflow: hidden;
  background: rgba(15,23,42,0.72);
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.engineer-evidence-thumb {
  aspect-ratio: 1.45 / 1;
  background: linear-gradient(135deg, rgba(30,41,59,0.95), rgba(15,23,42,0.92));
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.engineer-evidence-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.engineer-evidence-thumb.is-placeholder::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at top left, rgba(249,115,22,0.20), transparent 42%),
    linear-gradient(135deg, rgba(30,41,59,0.96), rgba(15,23,42,0.92));
}
.engineer-evidence-thumb__placeholder {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #64748B;
  font-size: 12px;
  font-weight: 600;
}
.engineer-evidence-thumb__placeholder svg {
  width: 22px;
  height: 22px;
}
.engineer-evidence-card__body {
  padding: 12px 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.engineer-evidence-card__meta strong {
  display: block;
  color: #F8FAFC;
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.engineer-evidence-card__meta span {
  display: block;
  margin-top: 4px;
  color: #64748B;
  font-size: 11px;
}
.engineer-evidence-card__action {
  align-self: flex-start;
  background: rgba(249,115,22,0.14);
  color: #FDBA74;
  border-color: rgba(249,115,22,0.24);
  padding: 8px 11px;
}
.engineer-assistant {
  position: sticky;
  top: 0;
  align-self: start;
}
.engineer-assistant__surface {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.engineer-assistant__eyebrow,
.engineer-quick-actions__title {
  font-size: 15px;
  font-weight: 800;
  color: #F8FAFC;
  letter-spacing: -0.02em;
}
.engineer-chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.engineer-chip {
  border: 1px solid rgba(148,163,184,0.16);
  background: rgba(15,23,42,0.78);
  color: #CBD5E1;
  font-size: 12px;
  font-weight: 600;
  border-radius: 999px;
  padding: 8px 12px;
  cursor: pointer;
  transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease;
}
.engineer-chip:hover {
  background: rgba(99,102,241,0.12);
  border-color: rgba(99,102,241,0.28);
  color: #E2E8F0;
}
.engineer-assistant__composer {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.engineer-assistant__input {
  width: 100%;
  min-height: 118px;
  resize: vertical;
  border-radius: 16px;
  border: 1px solid rgba(148,163,184,0.16);
  background: rgba(15,23,42,0.78);
  color: #F8FAFC;
  padding: 14px 15px;
  font-size: 13px;
  line-height: 1.6;
  outline: none;
  font-family: inherit;
}
.engineer-assistant__input::placeholder {
  color: #64748B;
}
.engineer-assistant__input:focus {
  border-color: rgba(249,115,22,0.32);
  box-shadow: 0 0 0 3px rgba(249,115,22,0.08);
}
.engineer-assistant__send {
  align-self: flex-start;
  background: linear-gradient(135deg, #F97316, #EA580C);
  color: #FFF7ED;
  font-size: 13px;
  font-weight: 800;
  padding: 10px 16px;
}
.engineer-assistant__response {
  min-height: 168px;
  border-radius: 16px;
  border: 1px solid rgba(148,163,184,0.12);
  background: rgba(15,23,42,0.74);
  padding: 14px 15px;
  color: #CBD5E1;
  font-size: 13px;
  line-height: 1.7;
  white-space: normal;
}
.engineer-assistant__response.is-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: transparent;
  font-size: 0;
}
.engineer-assistant__response.is-loading {
  color: #94A3B8;
}
.engineer-assistant__divider {
  height: 1px;
  background: rgba(148,163,184,0.12);
}
.engineer-quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.engineer-quick-action-btn {
  width: 100%;
  text-align: left;
  padding: 12px 14px;
  background: rgba(15,23,42,0.78);
  border-color: rgba(148,163,184,0.16);
  color: #E2E8F0;
  font-size: 13px;
  font-weight: 700;
}
.engineer-quick-action-btn:hover {
  background: rgba(99,102,241,0.12);
  border-color: rgba(99,102,241,0.28);
}
.engineer-empty-state,
.engineer-error-state {
  border: 1px dashed rgba(148,163,184,0.18);
  border-radius: 16px;
  padding: 26px 18px;
  text-align: center;
  color: #64748B;
  font-size: 13px;
}
.engineer-error-state {
  color: #FCA5A5;
  background: rgba(127,29,29,0.10);
  border-color: rgba(239,68,68,0.18);
}
.engineer-skeleton {
  position: relative;
  overflow: hidden;
}
.engineer-skeleton::after {
  content: '';
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
  animation: engineerShimmer 1.5s infinite;
}
.engineer-skeleton-row {
  height: 82px;
  border-radius: 16px;
  background: rgba(15,23,42,0.74);
  border: 1px solid rgba(148,163,184,0.10);
}
.engineer-skeleton-card {
  aspect-ratio: 1.45 / 1.18;
  border-radius: 18px;
  background: rgba(15,23,42,0.74);
  border: 1px solid rgba(148,163,184,0.10);
}
.engineer-bottleneck-panel {
  background:
    radial-gradient(circle at top right, rgba(249,115,22,0.18), transparent 32%),
    linear-gradient(135deg, rgba(255,255,255,0.88), rgba(241,245,249,0.94) 56%, rgba(226,232,240,0.92));
  border: 1px solid rgba(226,232,240,0.9);
  box-shadow: 0 26px 60px rgba(15,23,42,0.16);
}
.engineer-bottleneck-panel__top {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  padding: 22px 24px 14px;
}
.engineer-bottleneck-panel__eyebrow {
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #EA580C;
}
.engineer-bottleneck-panel__title {
  margin-top: 8px;
  font-size: 28px;
  line-height: 1.1;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: #0F172A;
}
.engineer-bottleneck-panel__body {
  padding: 0 24px 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.engineer-bottleneck-panel__summary {
  margin: 0;
  color: #334155;
  font-size: 15px;
  line-height: 1.7;
  max-width: 900px;
}
.engineer-close-meter {
  min-width: 174px;
  border-radius: 18px;
  padding: 14px 16px;
  background: rgba(15,23,42,0.92);
  color: #F8FAFC;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
}
.engineer-close-meter__label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #94A3B8;
}
.engineer-close-meter strong {
  font-size: 34px;
  line-height: 1;
  letter-spacing: -0.05em;
  color: #F97316;
}
.engineer-bottleneck-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}
.engineer-bottleneck-metric {
  border-radius: 18px;
  border: 1px solid rgba(148,163,184,0.18);
  background: rgba(255,255,255,0.72);
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.engineer-bottleneck-metric__label {
  font-size: 12px;
  font-weight: 700;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.engineer-bottleneck-metric__value {
  font-size: 30px;
  line-height: 1;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: #0F172A;
}
.engineer-bottleneck-metric[data-tone="warning"] .engineer-bottleneck-metric__value {
  color: #B45309;
}
.engineer-bottleneck-metric[data-tone="success"] .engineer-bottleneck-metric__value {
  color: #15803D;
}
.engineer-action-panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
/* --- KARAR TERMİNALİ — section override (light panel) --- */
.engineer-action-panel {
  background: #FFFFFF !important;
  border: 1px solid #E5E7EB !important;
  box-shadow: 0 4px 16px rgba(0,0,0,0.06) !important;
}
.engineer-action-panel .engineer-panel__header {
  background: transparent;
  border-bottom: 1px solid #F0F2F5;
}
.engineer-action-panel .engineer-panel__title {
  color: #111827;
}
.engineer-action-panel .engineer-panel__subtitle {
  color: #6B7280;
}
/* --- KARAR TERMİNALİ --- */
.karar-badge {
  display: inline-flex;
  align-items: center;
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  background: #EEF2FF;
  color: #4F46E5;
  border: 1px solid #DDE3FF;
}
.karar-terminal {
  display: grid;
  grid-template-columns: 296px minmax(0,1fr);
  min-height: 440px;
  border-top: 1px solid #E5E7EB;
  background: #FFFFFF;
}
.karar-terminal__list {
  overflow-y: auto;
  max-height: 540px;
  border-right: 1px solid #E5E7EB;
  padding: 6px 0;
  background:
    linear-gradient(180deg, rgba(248,250,252,0.88) 0%, rgba(255,255,255,0.98) 16%, #FFFFFF 100%);
}
.karar-terminal__detail {
  padding: 14px 18px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  max-height: 540px;
  background: linear-gradient(180deg, #FFFFFF 0%, #FAFBFC 100%);
}
.karar-list-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  border-bottom: 1px solid #F1F5F9;
  transition: background 0.15s ease, box-shadow 0.15s ease;
  position: relative;
}
.karar-list-item:hover { background: #F8FAFC; }
.karar-list-item.is-active {
  background: linear-gradient(90deg, rgba(59,130,246,0.08) 0%, rgba(59,130,246,0.03) 100%);
  box-shadow: inset 3px 0 0 #60A5FA;
}
.karar-list-item__tag {
  width: 34px;
  height: 34px;
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.04em;
  flex-shrink: 0;
  border: 1px solid transparent;
  margin-top: 2px;
}
.karar-list-item__tag[data-type="ISG"] { background: #FFF1F2; color: #DC2626; border-color: #FECACA; }
.karar-list-item__tag[data-type="STK"] { background: #FEF3C7; color: #B45309; border-color: #FDE68A; }
.karar-list-item__tag[data-type="RPR"] { background: #E8F5E9; color: #2E7D32; border-color: #C8E6C9; }
.karar-list-item__body { flex: 1; min-width: 0; }
.karar-list-item__title {
  font-size: 14px;
  font-weight: 700;
  color: #111827;
  line-height: 1.35;
}
.karar-list-item__meta {
  font-size: 12px;
  color: #6B7280;
  margin-top: 4px;
  line-height: 1.35;
}
.karar-list-item__right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
  flex-shrink: 0;
  min-width: 68px;
}
.karar-list-item__change {
  font-size: 18px;
  font-weight: 700;
  line-height: 1;
}
.karar-list-item__change.up { color: #16A34A; }
.karar-list-item__change.down { color: #DC2626; }
.karar-list-item__type-badge {
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: #F3F4F6;
  color: #6B7280;
  border: 1px solid #E5E7EB;
}
.karar-detail__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.karar-detail__record-type {
  font-size: 12px;
  font-weight: 800;
  color: #374151;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}
.karar-detail__record-time {
  font-size: 12px;
  color: #6B7280;
}
.karar-detail__image {
  border-radius: 14px;
  overflow: hidden;
  background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
  height: 188px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid #E5E7EB;
}
.karar-detail__image img { width: 100%; height: 100%; object-fit: cover; }
.karar-detail__image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #9CA3AF;
  font-size: 13px;
}
.karar-detail__title {
  font-size: 28px;
  font-weight: 700;
  color: #1F2937;
  margin: 0;
  line-height: 1.2;
}
.karar-detail__analysis-label {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #64748B;
  margin-bottom: 6px;
}
.karar-detail__analysis-text {
  font-size: 14px;
  color: #334155;
  line-height: 1.6;
  background: #EAF3FF;
  border-radius: 12px;
  padding: 14px 15px;
  border: 1px solid #D7E7FB;
}
.karar-detail__meta-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
.karar-detail__meta-cell {
  background: #F3F4F6;
  border-radius: 12px;
  padding: 11px 12px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  border: 1px solid #E5E7EB;
}
.karar-detail__meta-cell__label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #9CA3AF;
  font-weight: 700;
}
.karar-detail__meta-cell__value {
  font-size: 15px;
  font-weight: 700;
  color: #1F2937;
}
.karar-detail__actions {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
  margin-top: auto;
  padding-top: 6px;
}
.karar-btn-approve, .karar-btn-reject, .karar-btn-edit {
  appearance: none;
  border-radius: 10px;
  padding: 12px 8px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.15s ease, opacity 0.15s ease, box-shadow 0.15s ease;
}
.karar-btn-approve {
  border: none;
  background: linear-gradient(135deg, #16A34A 0%, #15803D 100%);
  color: #FFFFFF;
  box-shadow: 0 8px 18px rgba(22,163,74,0.22);
}
.karar-btn-reject {
  border: 2px solid #DC2626;
  background: transparent;
  color: #DC2626;
}
.karar-btn-edit {
  border: 2px solid #D1D5DB;
  background: transparent;
  color: #6B7280;
}
.karar-btn-approve:hover, .karar-btn-reject:hover, .karar-btn-edit:hover {
  transform: translateY(-1px);
  opacity: 0.96;
}
.karar-btn-approve:disabled, .karar-btn-reject:disabled, .karar-btn-edit:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}
.karar-detail__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #94A3B8;
  font-size: 14px;
  gap: 8px;
  min-height: 280px;
}
.karar-terminal__list-empty {
  padding: 48px 20px;
  text-align: center;
  color: #94A3B8;
  font-size: 14px;
}
.karar-skeleton-row {
  height: 74px;
  border-radius: 14px;
  background: linear-gradient(90deg, #F3F4F6 0%, #E5E7EB 50%, #F3F4F6 100%);
  margin: 8px 12px;
  animation: engineerPulse 1.6s ease-in-out infinite;
}
@media (max-width: 768px) {
  .karar-terminal { grid-template-columns: 1fr; }
  .karar-terminal__list { border-right: none; border-bottom: 1px solid #E5E7EB; max-height: 300px; }
  .karar-detail__top { align-items: flex-start; flex-direction: column; }
  .karar-detail__title { font-size: 22px; }
  .karar-detail__meta-grid { grid-template-columns: repeat(2,1fr); }
  .karar-detail__actions { grid-template-columns: 1fr; }
}
.engineer-batch-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}
.engineer-batch-bar__status {
  font-size: 12px;
  font-weight: 700;
  color: #94A3B8;
}
.engineer-batch-bar__button {
  appearance: none;
  border: 1px solid rgba(34,197,94,0.24);
  background: linear-gradient(135deg, #22C55E, #15803D);
  color: #F0FDF4;
  padding: 11px 16px;
  border-radius: 14px;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
  transition: transform 0.18s ease, opacity 0.18s ease, box-shadow 0.18s ease;
  box-shadow: 0 16px 32px rgba(21,128,61,0.24);
}
.engineer-batch-bar__button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  box-shadow: none;
}
.engineer-batch-bar__button:not(:disabled):hover {
  transform: translateY(-1px);
}
.engineer-action-grid {
  padding: 16px 18px 18px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}
.engineer-action-card {
  border: 1px solid rgba(148,163,184,0.12);
  border-radius: 22px;
  background:
    radial-gradient(circle at top right, rgba(249,115,22,0.12), transparent 34%),
    rgba(15,23,42,0.84);
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  cursor: pointer;
  transition: transform 0.18s ease, border-color 0.18s ease, opacity 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
}
.engineer-action-card:hover {
  transform: translateY(-2px);
  border-color: rgba(249,115,22,0.24);
  box-shadow: 0 20px 44px rgba(2,6,23,0.22);
}
.engineer-action-card.is-focused {
  border-color: rgba(249,115,22,0.38);
  box-shadow: 0 24px 52px rgba(2,6,23,0.26);
}
.engineer-action-card.is-dimmed {
  opacity: 0.44;
  filter: saturate(0.7);
}
.engineer-action-card[data-status="approved"] {
  border-color: rgba(34,197,94,0.26);
}
.engineer-action-card[data-status="rejected"] {
  border-color: rgba(239,68,68,0.26);
}
.engineer-action-card__select {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}
.engineer-action-card__check {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #CBD5E1;
  font-size: 12px;
  font-weight: 700;
}
.engineer-action-card__check input {
  accent-color: #22C55E;
}
.engineer-action-card__content {
  display: grid;
  grid-template-columns: 148px minmax(0, 1fr);
  gap: 14px;
}
.engineer-action-card__media .engineer-evidence-thumb {
  height: 100%;
  min-height: 168px;
  border-radius: 18px;
  overflow: hidden;
}
.engineer-action-card__body {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.engineer-action-card__header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}
.engineer-action-card__header h3 {
  margin: 0;
  font-size: 17px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #F8FAFC;
}
.engineer-action-card__header p {
  margin: 4px 0 0;
  font-size: 12px;
  color: #94A3B8;
}
.engineer-action-card__time {
  white-space: nowrap;
  color: #64748B;
  font-size: 11px;
  font-weight: 700;
}
.engineer-action-card__summary {
  border-radius: 16px;
  padding: 12px 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(148,163,184,0.10);
  color: #E2E8F0;
  font-size: 13px;
  line-height: 1.6;
}
.engineer-action-card__rows {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}
.engineer-action-card__row {
  border-radius: 14px;
  background: rgba(30,41,59,0.64);
  border: 1px solid rgba(148,163,184,0.08);
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.engineer-action-card__row span {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #64748B;
}
.engineer-action-card__row strong {
  color: #F8FAFC;
  font-size: 13px;
  font-weight: 700;
}
.engineer-action-card__footer {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-top: auto;
}
.engineer-action-card__approve,
.engineer-action-card__reject {
  appearance: none;
  border-radius: 14px;
  padding: 13px 14px;
  border: 1px solid transparent;
  font-size: 13px;
  font-weight: 900;
  letter-spacing: 0.04em;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.engineer-action-card__approve {
  background: linear-gradient(135deg, #22C55E, #15803D);
  color: #F0FDF4;
  box-shadow: 0 16px 30px rgba(21,128,61,0.22);
}
.engineer-action-card__reject {
  background: rgba(239,68,68,0.10);
  color: #FCA5A5;
  border-color: rgba(239,68,68,0.18);
}
.engineer-action-card__approve:hover,
.engineer-action-card__reject:hover {
  transform: translateY(-1px);
}
.engineer-secretary-rail__surface {
  min-height: 100%;
  background:
    radial-gradient(circle at top, rgba(249,115,22,0.16), transparent 24%),
    linear-gradient(180deg, #111827 0%, #0B1120 100%);
}
.engineer-secretary-rail__top {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.engineer-secretary-rail__sub {
  color: #94A3B8;
  font-size: 13px;
  line-height: 1.5;
}
.engineer-assistant__response.is-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #94A3B8;
  font-size: 13px;
}
.engineer-secretary-draft {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.engineer-secretary-draft__meta {
  font-size: 11px;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.engineer-secretary-draft__text {
  color: #E2E8F0;
  font-size: 13px;
  line-height: 1.7;
}
.engineer-secretary-note {
  border-radius: 14px;
  padding: 10px 12px;
  background: rgba(34,197,94,0.10);
  border: 1px solid rgba(34,197,94,0.18);
  color: #86EFAC;
  font-size: 12px;
  line-height: 1.6;
}
@keyframes engineerShimmer {
  100% { transform: translateX(100%); }
}

.contractor-dashboard {
  min-height: 100%;
}
.contractor-dashboard .engineer-dashboard__main {
  gap: 18px;
}
.contractor-summary-panel {
  order: -2;
  overflow: hidden;
}
.contractor-metric-grid {
  display: none !important;
  order: -1;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}
.contractor-metric-card {
  appearance: none;
  border: 1px solid #D7DEE8;
  border-radius: 16px;
  background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
  box-shadow: 0 8px 24px rgba(148,163,184,0.12);
  padding: 14px 16px 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 6px;
  text-align: left;
  cursor: default;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  min-height: 100px;
}
.contractor-metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 22px 46px rgba(148,163,184,0.2);
}
.contractor-metric-card__label {
  order: 2;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: none;
  color: #64748B;
}
.contractor-metric-card__value {
  order: 1;
  font-size: 36px;
  line-height: 1;
  letter-spacing: -0.04em;
  font-weight: 900;
  color: #0F172A;
}
.contractor-metric-card__context {
  display: none;
}
.contractor-metric-card__note {
  display: none;
}
.contractor-metric-card[data-tone="critical"] {
  border-color: rgba(239,68,68,0.28);
  background: linear-gradient(180deg, #FFFFFF 0%, #FEF2F2 100%);
}
.contractor-metric-card[data-tone="critical"] .contractor-metric-card__value {
  color: #B91C1C;
}
.contractor-metric-card[data-tone="warning"] {
  border-color: rgba(245,158,11,0.32);
  background: linear-gradient(180deg, #FFFFFF 0%, #FFF7ED 100%);
}
.contractor-metric-card[data-tone="warning"] .contractor-metric-card__value {
  color: #C2410C;
}
.contractor-metric-card[data-tone="success"] {
  border-color: rgba(16,185,129,0.28);
  background: linear-gradient(180deg, #FFFFFF 0%, #F0FDF4 100%);
}
.contractor-metric-card[data-tone="success"] .contractor-metric-card__value {
  color: #047857;
}
.contractor-metric-card[data-tone="info"] {
  border-color: rgba(14,165,233,0.28);
  background: linear-gradient(180deg, #FFFFFF 0%, #F0F9FF 100%);
}
.contractor-metric-card[data-tone="info"] .contractor-metric-card__value {
  color: #0369A1;
}
.contractor-panel--light {
  border-color: #D7DEE8;
  background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
  box-shadow: 0 18px 44px rgba(148,163,184,0.16);
}
.contractor-panel__header {
  border-bottom-color: rgba(203,213,225,0.8);
}
.contractor-panel__title {
  color: #0F172A;
}
.contractor-panel__subtitle {
  color: #64748B;
}
.contractor-summary-panel__body {
  padding: 18px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.contractor-summary-panel__composer {
  max-width: 420px;
}
.contractor-summary-panel .contractor-insight-list {
  grid-template-columns: 1fr;
}
.contractor-summary-hero-card {
  border: 1px solid rgba(203,213,225,0.9);
  border-radius: 18px;
  background:
    radial-gradient(circle at top right, rgba(249,115,22,0.08), transparent 28%),
    linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
  padding: 14px 18px 16px;
}
.contractor-summary-hero-card__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}
.contractor-summary-hero-card__eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #64748B;
}
.contractor-summary-hero-card__eyebrow::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #0F766E;
}
.contractor-summary-hero-card__role {
  border: 1px solid rgba(203,213,225,0.9);
  border-radius: 999px;
  background: #FFFFFF;
  color: #0F172A;
  font-size: 11px;
  font-weight: 800;
  padding: 7px 12px;
  white-space: nowrap;
}
.contractor-summary-hero-card__title {
  margin-top: 8px;
  color: #0F172A;
  font-size: 18px;
  line-height: 1.4;
  letter-spacing: -0.02em;
  font-weight: 800;
}
.contractor-summary-hero-card__footer {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.contractor-summary-hero-card__pill {
  border-radius: 999px;
  background: #FFFFFF;
  border: 1px solid rgba(203,213,225,0.9);
  color: #334155;
  font-size: 11px;
  font-weight: 700;
  padding: 8px 12px;
}
.contractor-summary-hero-card__pill[data-tone="warning"] {
  color: #C2410C;
}
.contractor-summary-hero-card__pill[data-tone="critical"] {
  color: #B91C1C;
}
.contractor-summary-hero-card__pill[data-tone="success"] {
  color: #047857;
}
.contractor-summary-hero-card__pill[data-tone="info"] {
  color: #0369A1;
}
.contractor-summary-hero-card[data-tone="warning"] .contractor-summary-hero-card__eyebrow::before {
  background: #F97316;
}
.contractor-summary-hero-card[data-tone="critical"] .contractor-summary-hero-card__eyebrow::before {
  background: #DC2626;
}
.contractor-summary-hero-card[data-tone="critical"] .contractor-summary-hero-card__title {
  color: #7F1D1D;
}
.contractor-summary-hero-card[data-tone="warning"] .contractor-summary-hero-card__title {
  color: #9A3412;
}
.contractor-content-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}
.contractor-command-rail {
  position: sticky;
  top: 0;
  align-self: start;
}
.contractor-command-rail__surface {
  min-height: calc(100vh - 150px);
  background:
    radial-gradient(circle at top, rgba(249,115,22,0.18), transparent 24%),
    linear-gradient(180deg, #111827 0%, #0B1220 100%);
  border-color: rgba(51,65,85,0.95);
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.contractor-command-rail__top {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.contractor-command-rail__eyebrow {
  font-size: 15px;
  font-weight: 800;
  color: #F8FAFC;
}
.contractor-command-rail__sub {
  font-size: 12px;
  line-height: 1.6;
  color: #94A3B8;
}
.contractor-command-rail__center {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
  gap: 14px;
  text-align: left;
}
.contractor-command-rail__status {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
}
.contractor-command-rail__status-orb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background:
    radial-gradient(circle at 30% 30%, rgba(251,146,60,0.95), rgba(234,88,12,0.18) 38%, rgba(15,23,42,0.08) 72%),
    #1E293B;
  box-shadow: 0 0 18px rgba(249,115,22,0.28);
}
.contractor-command-rail__status-text {
  color: #F8FAFC;
  font-size: 14px;
  font-weight: 800;
}
.contractor-command-rail__hint {
  max-width: none;
  color: #94A3B8;
  font-size: 12px;
  line-height: 1.7;
}
.contractor-action-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.contractor-action-card {
  border: 1px solid rgba(148,163,184,0.14);
  border-radius: 18px;
  background: rgba(255,255,255,0.05);
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.contractor-action-card__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}
.contractor-action-card__title {
  color: #F8FAFC;
  font-size: 13px;
  font-weight: 800;
  line-height: 1.5;
}
.contractor-action-card__mode {
  border-radius: 999px;
  padding: 5px 9px;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  background: rgba(255,255,255,0.08);
  color: #CBD5E1;
  white-space: nowrap;
}
.contractor-action-card__body {
  color: #CBD5E1;
  font-size: 12px;
  line-height: 1.7;
}
.contractor-action-card__cta {
  align-self: flex-start;
  border: 1px solid rgba(148,163,184,0.16);
  border-radius: 999px;
  background: rgba(255,255,255,0.08);
  color: #F8FAFC;
  font-size: 11px;
  font-weight: 800;
  padding: 8px 12px;
}
.contractor-action-card[data-tone="warning"] {
  border-color: rgba(249,115,22,0.28);
  background: rgba(154,52,18,0.14);
}
.contractor-action-card[data-tone="critical"] {
  border-color: rgba(239,68,68,0.28);
  background: rgba(127,29,29,0.18);
}
.contractor-action-card[data-tone="success"] {
  border-color: rgba(16,185,129,0.24);
}
.contractor-action-card[data-tone="info"] {
  border-color: rgba(56,189,248,0.24);
}
/* ── Contractor Feed Detail Drawer ─────────────────────────────── */
.contractor-feed-drawer {
  position: fixed;
  inset: 0;
  z-index: 1200;
  display: flex;
  justify-content: flex-end;
  pointer-events: none;
  visibility: hidden;
}
.contractor-feed-drawer.is-open {
  pointer-events: auto;
  visibility: visible;
}
.contractor-feed-drawer__backdrop {
  position: absolute;
  inset: 0;
  background: rgba(15,23,42,0.45);
  opacity: 0;
  transition: opacity 0.22s ease;
}
.contractor-feed-drawer.is-open .contractor-feed-drawer__backdrop {
  opacity: 1;
}
.contractor-feed-drawer__panel {
  position: relative;
  width: min(480px, 100vw);
  height: 100%;
  overflow-y: auto;
  background: #FFFFFF;
  display: flex;
  flex-direction: column;
  transform: translateX(100%);
  transition: transform 0.26s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: -8px 0 40px rgba(15,23,42,0.14);
}
.contractor-feed-drawer.is-open .contractor-feed-drawer__panel {
  transform: translateX(0);
}
.contractor-feed-drawer__header {
  position: sticky;
  top: 0;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 20px;
  background: #FFFFFF;
  border-bottom: 1px solid #F1F5F9;
}
.contractor-feed-drawer__eyebrow {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: #64748B;
}
.contractor-feed-drawer__close {
  appearance: none;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  background: #F8FAFC;
  color: #64748B;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.15s ease;
  flex-shrink: 0;
}
.contractor-feed-drawer__close:hover { background: #F1F5F9; }
.contractor-feed-drawer__body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  flex: 1;
}
.contractor-feed-drawer__status-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.contractor-feed-drawer__badge {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 800;
  background: #F0FDF4;
  border: 1px solid #BBF7D0;
  color: #15803D;
}
.contractor-feed-drawer__badge[data-tone="warning"] {
  background: #FFF7ED; border-color: #FED7AA; color: #C2410C;
}
.contractor-feed-drawer__badge[data-tone="info"] {
  background: #F0F9FF; border-color: #BAE6FD; color: #0369A1;
}
.contractor-feed-drawer__title {
  font-size: 20px;
  font-weight: 800;
  line-height: 1.35;
  letter-spacing: -0.02em;
  color: #0F172A;
}
.contractor-feed-drawer__meta {
  font-size: 12px;
  color: #64748B;
  line-height: 1.6;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.contractor-feed-drawer__meta strong {
  color: #334155;
}
.contractor-feed-drawer__section-label {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #94A3B8;
  margin-bottom: 6px;
}
.contractor-feed-drawer__summary {
  font-size: 14px;
  color: #334155;
  line-height: 1.65;
  padding: 12px 14px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
}
.contractor-feed-drawer__note {
  font-size: 13px;
  color: #475569;
  line-height: 1.6;
  padding: 10px 12px;
  background: #FFF7ED;
  border: 1px solid #FED7AA;
  border-radius: 10px;
}
.contractor-feed-drawer__image {
  border-radius: 12px;
  overflow: hidden;
  background: #F1F5F9;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.contractor-feed-drawer__image img {
  width: 100%;
  height: auto;
  display: block;
  max-height: 280px;
  object-fit: cover;
}
.contractor-feed-drawer__image-placeholder {
  color: #94A3B8;
  font-size: 12px;
  padding: 24px;
  text-align: center;
}
.contractor-feed-drawer__delta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  color: #0F172A;
  padding: 8px 12px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
}
@media (max-width: 640px) {
  .contractor-feed-drawer__panel { width: 100vw; }
}
/* ── Contractor Feed Detail Drawer — extended slots ────────────── */
.contractor-feed-drawer__gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
.contractor-feed-drawer__gallery-item {
  aspect-ratio: 1;
  border-radius: 10px;
  overflow: hidden;
  background: #F1F5F9;
  cursor: pointer;
}
.contractor-feed-drawer__gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.2s ease;
}
.contractor-feed-drawer__gallery-item:hover img { transform: scale(1.04); }
.contractor-feed-drawer__section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.contractor-feed-drawer__tech-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px 16px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
}
.contractor-feed-drawer__tech-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
  font-size: 13px;
  line-height: 1.5;
}
.contractor-feed-drawer__tech-key {
  flex-shrink: 0;
  width: 110px;
  font-weight: 600;
  color: #64748B;
  font-size: 12px;
}
.contractor-feed-drawer__tech-value {
  flex: 1;
  color: #0F172A;
  font-weight: 500;
  word-break: break-word;
}
.contractor-feed-drawer__thread {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.contractor-feed-drawer__thread-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 10px 14px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
}
.contractor-feed-drawer__thread-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.contractor-feed-drawer__thread-role {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: #0F172A;
  color: #FFFFFF;
}
.contractor-feed-drawer__thread-role[data-role="engineer"] { background: #2563EB; }
.contractor-feed-drawer__thread-role[data-role="contractor"] { background: #0F172A; }
.contractor-feed-drawer__thread-role[data-role="ai"] { background: #7C3AED; }
.contractor-feed-drawer__thread-role--muhendis {
  background: rgba(59, 130, 246, 0.12);
  color: #1D4ED8;
}
.contractor-feed-drawer__thread-role--muteahhit {
  background: rgba(234, 88, 12, 0.12);
  color: #C2410C;
}
.contractor-feed-drawer__thread-role--santi_sefi {
  background: rgba(16, 185, 129, 0.12);
  color: #047857;
}
.contractor-feed-drawer__thread-role--yonetici,
.contractor-feed-drawer__thread-role--admin,
.contractor-feed-drawer__thread-role--default {
  background: rgba(100, 116, 139, 0.12);
  color: #475569;
}
.contractor-feed-drawer__thread-time {
  font-size: 11px;
  color: #94A3B8;
  font-weight: 500;
}
.contractor-feed-drawer__thread-body {
  font-size: 13px;
  color: #334155;
  line-height: 1.6;
}
.contractor-feed-drawer__thread-input {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 10px 14px;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  background: #FFFFFF;
}
.contractor-feed-drawer__thread-input input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 13px;
  color: #0F172A;
  background: transparent;
  font-family: inherit;
}
.contractor-feed-drawer__thread-input input::placeholder { color: #94A3B8; }
.contractor-feed-drawer__thread-send {
  appearance: none;
  border: none;
  border-radius: 8px;
  background: #0F172A;
  color: #FFFFFF;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.15s;
}
.contractor-feed-drawer__thread-send:hover { background: #1E293B; }
.contractor-feed-drawer__action-bar {
  position: sticky;
  bottom: 0;
  z-index: 1;
  display: flex;
  gap: 10px;
  padding: 16px 24px;
  background: #FFFFFF;
  border-top: 1px solid #E2E8F0;
  flex-shrink: 0;
}
.contractor-feed-drawer__action-btn {
  appearance: none;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  padding: 10px 20px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
  background: #F8FAFC;
  color: #0F172A;
}
.contractor-feed-drawer__action-btn:hover { background: #F1F5F9; }
.contractor-feed-drawer__action-btn[data-variant="primary"] {
  background: #0F172A;
  color: #FFFFFF;
  border-color: #0F172A;
}
.contractor-feed-drawer__action-btn[data-variant="primary"]:hover { background: #1E293B; }
/* ── /Contractor Feed Detail Drawer ────────────────────────────── */
.contractor-command-rail__composer {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.contractor-command-rail__composer::before {
  content: 'Derin analiz / komut';
  color: #E2E8F0;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.contractor-command-rail__composer-box {
  gap: 10px;
}
.contractor-trend-body {
  padding: 18px 20px 20px;
}
.contractor-trend-chart {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 10px;
  align-items: end;
}
.contractor-trend-bar {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}
.contractor-trend-bar__column {
  width: 100%;
  min-height: 120px;
  border-radius: 14px;
  background: linear-gradient(180deg, #E2E8F0 0%, #F8FAFC 100%);
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}
.contractor-trend-bar__fill {
  width: 100%;
  min-height: 10px;
  border-radius: 14px;
  background: linear-gradient(180deg, #0F766E 0%, #0F172A 100%);
}
.contractor-trend-bar__value {
  font-size: 11px;
  font-weight: 800;
  color: #0F172A;
}
.contractor-trend-bar__date {
  font-size: 10px;
  color: #64748B;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.contractor-trend-summary {
  border: 1px solid rgba(203,213,225,0.9);
  border-radius: 18px;
  background: #FFFFFF;
  padding: 16px 18px;
  color: #334155;
  font-size: 13px;
  line-height: 1.7;
}
.contractor-trend-summary strong {
  display: block;
  margin-bottom: 6px;
  color: #0F172A;
  font-size: 13px;
}
.contractor-field-grid {
  padding: 16px 18px 18px;
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}
.contractor-field-card {
  border: 1px solid rgba(203,213,225,0.9);
  border-radius: 18px;
  background: #FFFFFF;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.contractor-field-card__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}
.contractor-field-card__site strong {
  display: block;
  color: #0F172A;
  font-size: 15px;
  font-weight: 800;
}
.contractor-field-card__site span {
  display: block;
  margin-top: 5px;
  color: #64748B;
  font-size: 12px;
}
.contractor-field-card__count {
  min-width: 68px;
  border-radius: 16px;
  background: #0F172A;
  color: #F8FAFC;
  padding: 10px 12px;
  text-align: center;
}
.contractor-field-card__count strong {
  display: block;
  font-size: 22px;
  line-height: 1;
  letter-spacing: -0.04em;
}
.contractor-field-card__count span {
  display: block;
  margin-top: 4px;
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(248,250,252,0.72);
}
.contractor-field-card__zone {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 10px;
  border-radius: 999px;
  background: #F1F5F9;
  color: #0F172A;
  font-size: 11px;
  font-weight: 800;
}
.contractor-field-card__zone.is-repeated {
  background: #FFF7ED;
  color: #C2410C;
}
.contractor-field-card__summary {
  color: #475569;
  font-size: 13px;
  line-height: 1.65;
}
.contractor-field-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  color: #64748B;
  font-size: 11px;
}
.contractor-field-card__footer strong {
  color: #0F172A;
}
.contractor-insight-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}
.contractor-insight-card {
  border: 1px solid rgba(203,213,225,0.9);
  border-radius: 18px;
  background: #FFFFFF;
  padding: 14px 14px 15px;
}
.contractor-insight-card__title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  color: #0F172A;
  font-size: 13px;
  font-weight: 800;
}
.contractor-insight-card__body {
  margin-top: 8px;
  color: #475569;
  font-size: 12px;
  line-height: 1.7;
}
.contractor-insight-card[data-tone="warning"] {
  border-color: rgba(245,158,11,0.24);
}
.contractor-insight-card[data-tone="warning"] .contractor-insight-card__title {
  color: #FBBF24;
}
.contractor-insight-card[data-tone="success"] {
  border-color: rgba(16,185,129,0.24);
}
.contractor-insight-card[data-tone="success"] .contractor-insight-card__title {
  color: #86EFAC;
}
.contractor-insight-card[data-tone="info"] {
  border-color: rgba(14,165,233,0.24);
}
.contractor-insight-card[data-tone="info"] .contractor-insight-card__title {
  color: #7DD3FC;
}
.contractor-chip-row {
  gap: 8px;
}
.contractor-chip {
  border: 1px solid rgba(203,213,225,0.9);
  background: #FFFFFF;
  color: #334155;
}
.contractor-chip.is-static {
  cursor: default;
}
.contractor-chip[data-tone="warning"] {
  color: #C2410C;
}
.contractor-chip[data-tone="critical"] {
  color: #B91C1C;
}
.contractor-chip[data-tone="success"] {
  color: #047857;
}
.contractor-chip[data-tone="info"] {
  color: #0369A1;
}
.contractor-assistant__composer {
  gap: 10px;
}
.contractor-assistant__input {
  min-height: 86px;
  background: rgba(255,255,255,0.06);
  color: #F8FAFC;
  border-color: rgba(148,163,184,0.16);
}
.contractor-assistant__send {
  align-self: flex-start;
}
.contractor-assistant__response {
  min-height: 72px;
  max-height: 220px;
  overflow-y: auto;
  background: rgba(255,255,255,0.06);
  color: #CBD5E1;
  border-color: rgba(148,163,184,0.16);
}
.contractor-quick-actions__title {
  color: #0F172A;
}
.contractor-quick-action-btn {
  background: #FFFFFF;
  color: #0F172A;
  border-color: rgba(203,213,225,0.9);
}
.contractor-quick-actions {
  border: 1px solid rgba(203,213,225,0.9);
  border-radius: 20px;
  background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
  box-shadow: 0 18px 44px rgba(148,163,184,0.16);
  padding: 18px 20px 20px;
}
.contractor-quick-actions--inline {
  margin-top: 2px;
}
.contractor-quick-actions__row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.contractor-quick-actions__row .contractor-quick-action-btn {
  width: auto;
}
.contractor-command-rail__footer {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.contractor-command-rail__footer .contractor-quick-actions__title {
  color: #F8FAFC;
}
.contractor-command-rail__footer-links {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.contractor-command-rail__footer-links .contractor-quick-action-btn {
  width: 100%;
  background: rgba(255,255,255,0.06);
  color: #E2E8F0;
  border-color: rgba(148,163,184,0.16);
  text-align: left;
}
.contractor-summary-hero-card__footer {
  margin-top: 18px;
  padding-top: 4px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.contractor-summary-hero-card__pill {
  background: #F1F5F9;
  border-color: rgba(203,213,225,0.92);
  color: #475569 !important;
  font-weight: 700;
}
.contractor-action-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-top: 2px;
}
.contractor-action-card__ghost {
  border: 1px solid rgba(148,163,184,0.16);
  border-radius: 999px;
  background: transparent;
  color: #CBD5E1;
  font-size: 11px;
  font-weight: 700;
  padding: 8px 12px;
}
.contractor-action-card__ghost:hover {
  background: rgba(255,255,255,0.06);
  color: #F8FAFC;
}
.contractor-action-card__evidence {
  margin-top: 2px;
  border-top: 1px solid rgba(148,163,184,0.14);
  padding-top: 12px;
}
.contractor-action-card__evidence-title {
  color: #E2E8F0;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.contractor-action-card__evidence-list {
  margin: 0;
  padding-left: 18px;
  color: #CBD5E1;
  font-size: 12px;
  line-height: 1.7;
}
.contractor-action-card__evidence-list li + li {
  margin-top: 6px;
}
.contractor-action-card__evidence-list strong {
  color: #F8FAFC;
}
.contractor-empty-state,
.contractor-error-state,
.contractor-locked-state {
  border: 1px dashed rgba(148,163,184,0.26);
  border-radius: 18px;
  padding: 22px 18px;
  text-align: center;
  font-size: 13px;
  line-height: 1.7;
}
.contractor-empty-state {
  color: #64748B;
  background: #FFFFFF;
}
.contractor-error-state,
.contractor-locked-state {
  color: #FCA5A5;
  background: rgba(127,29,29,0.12);
  border-color: rgba(239,68,68,0.22);
}

.engineer-workspace-panel {
  box-shadow: 0 14px 36px rgba(15,23,42,0.08);
}
.engineer-workspace-panel__top {
  padding: 18px 22px 10px;
  align-items: center;
}
.engineer-workspace-panel__title {
  margin-top: 6px;
  font-size: 24px;
}
.engineer-workspace-panel__body {
  padding: 0 22px 18px;
  gap: 14px;
}
.engineer-workspace-metrics .engineer-bottleneck-metric {
  min-height: 112px;
}
.karar-header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
.dashboard-rail-toggle,
.dashboard-rail-close {
  appearance: none;
  border: 1px solid #D6DCE5;
  background: #FFFFFF;
  color: #334155;
  border-radius: 999px;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}
.dashboard-rail-toggle--dark {
  background: #0F172A;
  border-color: #0F172A;
  color: #F8FAFC;
}
.dashboard-rail-close {
  background: rgba(255,255,255,0.08);
  border-color: rgba(148,163,184,0.18);
  color: #CBD5E1;
}
.dashboard-rail-close--light {
  background: rgba(255,255,255,0.08);
  border-color: rgba(148,163,184,0.18);
  color: #F8FAFC;
}
/* Müteahhit: mobile-only AI Paneli butonu */
.dashboard-rail-toggle--compact { display: none; }
@media (max-width: 1023px) {
  .dashboard-rail-toggle--compact { display: inline-flex; align-items: center; }
  /* FAB olduğu için header butonu mobile'da gizlenir */
  #contractorRailToggleMobile { display: none !important; }
}
.karar-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 0 20px 16px;
  border-bottom: 1px solid #F1F5F9;
  flex-wrap: wrap;
}
.karar-filter-group {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.karar-filter-btn {
  appearance: none;
  border: 1px solid #D6DCE5;
  background: #FFFFFF;
  color: #64748B;
  border-radius: 999px;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.16s ease;
}
.karar-filter-btn.is-active {
  background: #0F172A;
  border-color: #0F172A;
  color: #FFFFFF;
}
.karar-toolbar__note {
  font-size: 12px;
  color: #64748B;
}
.karar-terminal {
  min-height: 480px;
  grid-template-columns: 296px minmax(0,1fr);
}
.karar-detail__record-subline,
.karar-detail__supporting {
  font-size: 12px;
  color: #64748B;
  line-height: 1.5;
}
.karar-detail__heading-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
}
.karar-detail__status-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 800;
  white-space: nowrap;
  border: 1px solid #E2E8F0;
  background: #F8FAFC;
  color: #475569;
}
.karar-detail__status-badge[data-tone="success"] {
  background: #F0FDF4;
  border-color: #BBF7D0;
  color: #15803D;
}
.karar-detail__status-badge[data-tone="critical"] {
  background: #FEF2F2;
  border-color: #FECACA;
  color: #B91C1C;
}
.karar-detail__status-badge[data-tone="warning"] {
  background: #FFF7ED;
  border-color: #FED7AA;
  color: #C2410C;
}
.karar-detail__analysis-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}
.karar-detail__expand-btn {
  appearance: none;
  border: none;
  background: transparent;
  color: #2563EB;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}
.karar-detail__analysis-text[data-expanded="true"] {
  white-space: pre-wrap;
}
.karar-detail__fact-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}
.karar-detail__fact {
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 11px 12px;
  background: #FFFFFF;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.karar-detail__fact-label {
  font-size: 10px;
  font-weight: 700;
  color: #94A3B8;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.karar-detail__fact-value {
  font-size: 14px;
  color: #0F172A;
  font-weight: 700;
  line-height: 1.4;
}
.karar-detail__note-box {
  border: 1px solid #E5E7EB;
  border-radius: 14px;
  background: #F8FAFC;
  padding: 14px;
}
.karar-detail__note-help {
  font-size: 11px;
  color: #64748B;
}
.karar-detail__note-input {
  width: 100%;
  min-height: 100px;
  resize: vertical;
  border: 1px solid #D6DCE5;
  border-radius: 12px;
  background: #FFFFFF;
  color: #0F172A;
  padding: 12px 13px;
  font-size: 13px;
  line-height: 1.6;
  font-family: inherit;
  outline: none;
  box-sizing: border-box;
}
.karar-detail__note-input:focus {
  border-color: #93C5FD;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.08);
}
.engineer-secretary-rail__head,
.contractor-command-rail__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}
.engineer-secretary-rail.is-collapsed,
.contractor-command-rail.is-collapsed {
  display: none;
}
.contractor-metric-grid {
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}
.contractor-summary-lines {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.contractor-summary-line {
  border: 1px solid rgba(203,213,225,0.86);
  border-radius: 14px;
  background: rgba(255,255,255,0.86);
  padding: 12px 14px;
  color: #334155;
  font-size: 13px;
  line-height: 1.6;
}
/* ── Bugün Onaylananlar — horizontal media card ─────────────────── */
.contractor-approved-feed {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.contractor-approved-card {
  border: 1px solid rgba(203,213,225,0.9);
  border-radius: 16px;
  background: #FFFFFF;
  display: grid;
  grid-template-columns: 80px minmax(0, 1fr) auto;
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.18s ease, border-color 0.18s ease, transform 0.12s ease;
  min-height: 80px;
  position: relative;
}
.contractor-approved-card:hover {
  border-color: rgba(99,102,241,0.38);
  box-shadow: 0 6px 20px rgba(99,102,241,0.11);
  transform: translateY(-1px);
}
.contractor-approved-card:focus-visible {
  outline: 2px solid #6366F1;
  outline-offset: 2px;
}
/* Thumbnail column */
.contractor-approved-card__thumb {
  position: relative;
  overflow: hidden;
  border-right: 1px solid rgba(203,213,225,0.6);
  flex-shrink: 0;
}
.contractor-approved-card__thumb img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  z-index: 1;
}
.contractor-approved-card__thumb-ph {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  background: linear-gradient(135deg, #F8FAFC, #E2E8F0);
  color: #64748B;
  padding: 8px;
}
.contractor-approved-card__thumb-ph[data-cat="ISG"] {
  background: linear-gradient(135deg, #FEF2F2, #FEE2E2);
  color: #DC2626;
}
.contractor-approved-card__thumb-ph[data-cat="Stok"] {
  background: linear-gradient(135deg, #FFFBEB, #FEF3C7);
  color: #B45309;
}
.contractor-approved-card__thumb-ph[data-cat="Rapor"] {
  background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
  color: #1D4ED8;
}
.contractor-approved-card__thumb-ph svg {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}
.contractor-approved-card__thumb-ph span {
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  text-align: center;
  line-height: 1.2;
}
/* Content column */
.contractor-approved-card__content {
  padding: 12px 12px 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
  justify-content: center;
}
.contractor-approved-card__badges {
  display: flex;
  align-items: center;
  gap: 5px;
  flex-wrap: wrap;
  margin-bottom: 2px;
}
.contractor-approved-card__type-badge {
  font-size: 10px;
  font-weight: 800;
  border-radius: 5px;
  padding: 2px 7px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  background: #F1F5F9;
  color: #475569;
}
.contractor-approved-card__type-badge[data-cat="ISG"] {
  background: #FEE2E2;
  color: #DC2626;
}
.contractor-approved-card__type-badge[data-cat="Stok"] {
  background: #FEF3C7;
  color: #B45309;
}
.contractor-approved-card__type-badge[data-cat="Rapor"] {
  background: #DBEAFE;
  color: #1D4ED8;
}
.contractor-approved-card__status-badge {
  font-size: 10px;
  font-weight: 700;
  border-radius: 999px;
  padding: 2px 8px;
  background: #F8FAFC;
  color: #64748B;
  border: 1px solid #E2E8F0;
}
.contractor-approved-card__status-badge[data-status="approved"] {
  background: #F0FDF4;
  color: #15803D;
  border-color: #BBF7D0;
}
.contractor-approved-card__status-badge[data-status="correction"] {
  background: #FFFBEB;
  color: #B45309;
  border-color: #FDE68A;
}
.contractor-approved-card__status-badge[data-status="rejected"] {
  background: #FEF2F2;
  color: #DC2626;
  border-color: #FECACA;
}
.contractor-approved-card__title {
  font-size: 14px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.contractor-approved-card__meta {
  font-size: 11px;
  color: #64748B;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.contractor-approved-card__summary {
  font-size: 12px;
  color: #475569;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-top: 2px;
}
/* CTA column */
.contractor-approved-card__cta {
  display: flex;
  align-items: center;
  padding: 12px 14px 12px 0;
  flex-shrink: 0;
}
.contractor-approved-card__incele {
  font-size: 12px;
  font-weight: 800;
  color: #6366F1;
  background: rgba(99,102,241,0.07);
  border: 1px solid rgba(99,102,241,0.18);
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s ease;
  letter-spacing: 0.01em;
  pointer-events: none;
}
.contractor-approved-card:hover .contractor-approved-card__incele {
  background: rgba(99,102,241,0.14);
}
/* ── /Bugün Onaylananlar ─────────────────────────────────────────── */
.contractor-field-grid {
  grid-template-columns: 1fr;
}
.contractor-field-brief-card {
  border: 1px solid rgba(203,213,225,0.92);
  border-radius: 18px;
  background: #FFFFFF;
  padding: 16px;
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr);
  gap: 12px;
  align-items: start;
}
.contractor-field-brief-card__index {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  background: #0F172A;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 800;
}
.contractor-field-brief-card__text {
  color: #334155;
  font-size: 13px;
  line-height: 1.7;
}
.contractor-action-card__evidence.is-open {
  display: block;
}
.contractor-action-card__footer {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

/* 14) Mobil */
@media (max-width: 768px) {
  #sidebar { width: 180px !important; }
  #content { padding: 14px !important; gap: 12px !important; }
  #dashKpiGrid { grid-template-columns: 1fr !important; }
  #contentHeader { padding: 12px 16px !important; }
  #santiyePageOzet { grid-template-columns: repeat(2,1fr) !important; }
  #santiyePageHoriz { grid-template-columns: 1fr !important; }
  #santiyePageGrid  { grid-template-columns: repeat(2,1fr) !important; }
  .engineer-dashboard { grid-template-columns: 1fr; }
  .engineer-bottleneck-panel__top,
  .engineer-action-panel__header,
  .engineer-batch-bar,
  .engineer-action-card__header { flex-direction: column; align-items: flex-start; }
  .karar-header-actions,
  .karar-toolbar,
  .karar-detail__heading-row,
  .engineer-secretary-rail__head,
  .contractor-command-rail__head { width: 100%; }
  .engineer-bottleneck-metrics,
  .engineer-action-grid,
  .engineer-action-card__rows,
  .engineer-action-card__footer,
  .karar-detail__fact-grid { grid-template-columns: 1fr; }
  .engineer-action-card__content { grid-template-columns: 1fr; }
  .engineer-assistant { position: static; }
  .engineer-loop-row {
    grid-template-columns: auto minmax(0, 1fr);
    align-items: start;
  }
  .engineer-loop-row__meta,
  .engineer-loop-row .engineer-badge,
  .engineer-loop-row__action {
    grid-column: 2;
  }
  .contractor-command-rail { position: static; }
  .contractor-command-rail__surface { min-height: auto; }
  .contractor-content-grid,
  .contractor-field-card__top,
  .contractor-field-card__footer { flex-direction: column; align-items: flex-start; }
  .contractor-metric-grid,
  .contractor-field-grid { grid-template-columns: 1fr; }
  .contractor-insight-list { display: grid; grid-template-columns: 1fr; }
  .contractor-trend-chart { gap: 8px; }
  .contractor-approved-card {
    grid-template-columns: 68px minmax(0, 1fr);
  }
  .contractor-approved-card__cta { display: none; }
  .contractor-field-brief-card { min-height: auto; }
}
@media (max-width: 1200px) and (min-width: 769px) {
  .engineer-dashboard { grid-template-columns: minmax(0, 1fr) 288px; }
  .engineer-action-grid { grid-template-columns: 1fr; }
  .engineer-loop-row {
    grid-template-columns: auto minmax(0, 1fr) minmax(100px, 0.7fr) auto;
  }
  .engineer-loop-row__meta:first-of-type { display: none; }
  .contractor-field-grid { grid-template-columns: 1fr; }
  .contractor-metric-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .contractor-insight-list { grid-template-columns: 1fr; }
  .contractor-content-grid { grid-template-columns: 1fr; }
  .contractor-command-rail__surface { min-height: 760px; }
}
@media (max-width: 1024px) {
  .engineer-dashboard {
    grid-template-columns: 1fr;
  }
  .engineer-assistant,
  .contractor-command-rail {
    position: static;
  }
  .karar-terminal {
    grid-template-columns: 1fr;
    min-height: 0;
  }
  .karar-terminal__list {
    border-right: none;
    border-bottom: 1px solid #E5E7EB;
    max-height: 320px;
  }
  .contractor-dashboard {
    grid-template-columns: 1fr;
  }
  .contractor-metric-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* ── Müteahhit AI Paneli FAB — sadece mobile ── */
.contractor-fab {
  display: none; /* Desktop'ta daima gizli */
}

@media (max-width: 1023px) {
  .contractor-fab {
    display: flex;
    position: fixed;
    bottom: calc(env(safe-area-inset-bottom, 0px) + 20px);
    right: 20px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border: 1px solid rgba(20, 184, 166, 0.4);
    color: #5EEAD4;
    font-size: 24px;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35),
                0 0 0 1px rgba(20, 184, 166, 0.15),
                0 0 20px rgba(20, 184, 166, 0.2);
    z-index: 998;
    transition: transform 0.2s ease-out, opacity 0.2s ease-out;
    -webkit-tap-highlight-color: transparent;
  }

  .contractor-fab:active {
    transform: scale(0.92);
  }

  .contractor-fab[data-hidden="true"] {
    opacity: 0;
    pointer-events: none;
    transform: scale(0.8);
  }

  .contractor-fab__icon {
    display: block;
    line-height: 1;
  }
}

/* ── Müteahhit Rail — Mobile full-screen davranışı ── */
.contractor-rail-overlay {
  display: none;
}

@media (max-width: 1023px) {
  /* Rail mobile'da is-collapsed'ın display:none'ını ezip transform kullanır */
  #contractorAssistantRail,
  #contractorAssistantRail.is-collapsed {
    display: flex !important;
    position: fixed !important;
    top: var(--contractor-header-height, 140px);
    right: 0;
    bottom: 0;
    width: 100vw !important;
    max-width: 100vw !important;
    height: auto !important;
    transform: translateX(100%);
    transition: transform 280ms cubic-bezier(0.32, 0.72, 0, 1);
    z-index: 1000;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
  }

  #contractorAssistantRail[data-open="true"] {
    transform: translateX(0);
  }

  /* Overlay — rail açıkken arka planı karartır */
  .contractor-rail-overlay {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0);
    pointer-events: none;
    transition: background 280ms ease-out;
    z-index: 999;
  }

  .contractor-rail-overlay[data-visible="true"] {
    background: rgba(0, 0, 0, 0.5);
    pointer-events: auto;
  }

  /* Body scroll lock rail açıkken */
  body[data-rail-open="true"] {
    overflow: hidden;
  }
}

/* ── HAKEDİŞ MODÜLÜ ──────────────────────────────────────── */
.hkd-kart {
  transition: border-color .15s, box-shadow .15s;
}
.hkd-kart:hover {
  border-color: #94A3B8 !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.hkd-kart-aktif {
  border-color: #0F172A !important;
  background: #F8FAFC !important;
}
#hakedisKalemTable input[type="number"] {
  outline: none;
  transition: border-color .15s;
}
#hakedisKalemTable input[type="number"]:focus {
  border-color: #0F172A;
  box-shadow: 0 0 0 2px rgba(15,23,42,.08);
}
#hakedisKalemTable tbody tr:hover {
  background: #F8FAFC;
}

@media (max-width: 639px) {
  #hakedisListPanel {
    width: 100% !important;
    min-width: 0 !important;
    border-right: none !important;
  }
  #hakedisDetayPanel {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 10;
    background: #F1F5F9;
  }
  #hakedisModal > div {
    width: 92vw !important;
  }
}

/* Metraj özeti */
.metraj-ozet-wrap {
  flex-shrink: 0;
  padding: 14px 18px 0;
  background: #F1F5F9;
}

.metraj-ozet-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.metraj-ozet-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 14px 16px;
  min-width: 0;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}

.metraj-ozet-label {
  color: #64748B;
  font-size: 11px;
  font-weight: 700;
  margin-bottom: 6px;
  text-transform: uppercase;
}

.metraj-ozet-value {
  color: #0F172A;
  font-size: 19px;
  font-weight: 800;
  line-height: 1.2;
}

.metraj-ozet-sub {
  color: #64748B;
  font-size: 11px;
  margin-top: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.metraj-ozet-progress {
  height: 7px;
  background: #E2E8F0;
  border-radius: 999px;
  overflow: hidden;
  margin-top: 10px;
}

.metraj-ozet-progress span {
  display: block;
  height: 100%;
  background: #16A34A;
  border-radius: inherit;
}

.metraj-ozet-loading {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  color: #64748B;
  font-size: 13px;
  padding: 14px 16px;
}

.metraj-ozet-loading.error {
  color: #DC2626;
}

@media (max-width: 1100px) {
  .metraj-ozet-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .metraj-ozet-wrap {
    padding: 12px 12px 0;
  }

  .metraj-ozet-grid {
    grid-template-columns: 1fr;
  }
}
</style>
"""
