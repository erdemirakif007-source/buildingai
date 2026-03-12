CSS_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

    /* ============================================
       DESIGN TOKENS — Single source of truth
    ============================================ */
    :root {
        /* Colors */
        --primary: #f97316;
        --primary-dark: #ea6c0a;
        --primary-light: rgba(249, 115, 22, 0.15);
        --primary-glow: rgba(249, 115, 22, 0.35);

        --bg: #080a0c;
        --bg-2: #0d1014;
        --bg-3: #12151a;

        --card: rgba(18, 21, 26, 0.85);
        --card-hover: rgba(24, 28, 34, 0.95);
        --card-border: rgba(255, 255, 255, 0.07);
        --card-border-hover: rgba(249, 115, 22, 0.3);

        --text: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #475569;

        --success: #22c55e;
        --success-light: rgba(34, 197, 94, 0.12);
        --danger: #ef4444;
        --danger-light: rgba(239, 68, 68, 0.12);
        --accent: #6366f1;
        --accent-light: rgba(99, 102, 241, 0.12);
        --warning: #f59e0b;

        /* Typography */
        --font: 'Inter', -apple-system, sans-serif;
        --font-mono: 'JetBrains Mono', monospace;

        /* Spacing */
        --radius-sm: 10px;
        --radius-md: 16px;
        --radius-lg: 22px;
        --radius-xl: 28px;
        --radius-2xl: 36px;

        /* Shadows */
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.3);
        --shadow-md: 0 8px 24px rgba(0,0,0,0.5);
        --shadow-lg: 0 20px 50px rgba(0,0,0,0.7);
        --shadow-glow: 0 0 30px var(--primary-glow);

        /* Transitions */
        --ease: cubic-bezier(0.19, 1, 0.22, 1);
        --ease-bounce: cubic-bezier(0.175, 0.885, 0.32, 1.275);
        --duration: 0.35s;
    }

    /* Light mode */
    body.light-mode {
        --bg: #f0f4f8;
        --bg-2: #e8edf3;
        --bg-3: #dde4ed;
        --card: rgba(255, 255, 255, 0.9);
        --card-hover: rgba(255, 255, 255, 0.98);
        --card-border: rgba(0, 0, 0, 0.08);
        --text: #0f172a;
        --text-secondary: #475569;
        --text-muted: #94a3b8;
    }

    /* ============================================
       RESET & BASE
    ============================================ */
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

    body {
        font-family: var(--font);
        background: var(--bg);
        color: var(--text);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow-x: hidden;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* Animated background */
    body::before {
        content: '';
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background:
            radial-gradient(ellipse 80% 60% at 70% -10%, rgba(249,115,22,0.08) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at -10% 80%, rgba(99,102,241,0.05) 0%, transparent 50%);
        pointer-events: none; z-index: 0;
        animation: bgPulse 8s ease-in-out infinite alternate;
    }

    @keyframes bgPulse {
        0% { opacity: 0.6; }
        100% { opacity: 1; }
    }

    /* ============================================
       TYPOGRAPHY SYSTEM
    ============================================ */
    .text-display { font-size: 2.2rem; font-weight: 900; letter-spacing: -2px; line-height: 1.1; }
    .text-heading { font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px; }
    .text-subheading { font-size: 1rem; font-weight: 600; letter-spacing: -0.2px; }
    .text-body { font-size: 0.95rem; font-weight: 400; line-height: 1.6; }
    .text-small { font-size: 0.8rem; font-weight: 500; }
    .text-label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; color: var(--text-muted); }
    .text-mono { font-family: var(--font-mono); font-size: 0.85rem; }
    .text-primary { color: var(--primary); }
    .text-secondary { color: var(--text-secondary); }
    .text-muted { color: var(--text-muted); }
    .text-success { color: var(--success); }
    .text-danger { color: var(--danger); }

    /* ============================================
       CARD SYSTEM
    ============================================ */
    .card {
        background: var(--card);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-lg);
        transition: border-color var(--duration) var(--ease), box-shadow var(--duration) var(--ease);
    }

    .card:hover {
        border-color: var(--card-border-hover);
    }

    .card-glass {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: var(--radius-lg);
    }

    .card-solid {
        background: var(--bg-3);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-lg);
    }

    .card-primary {
        background: var(--primary-light);
        border: 1px solid rgba(249,115,22,0.25);
        border-radius: var(--radius-lg);
    }

    /* ============================================
       BUTTON SYSTEM
    ============================================ */

    /* Base button */
    .btn {
        display: inline-flex; align-items: center; justify-content: center; gap: 8px;
        font-family: var(--font); font-weight: 700; font-size: 0.9rem;
        border: none; border-radius: var(--radius-md); cursor: pointer;
        transition: all var(--duration) var(--ease);
        position: relative; overflow: hidden; white-space: nowrap;
        -webkit-tap-highlight-color: transparent;
    }

    .btn::after {
        content: '';
        position: absolute; inset: 0;
        background: rgba(255,255,255,0.1);
        opacity: 0; transition: opacity 0.2s ease;
        border-radius: inherit;
    }

    .btn:hover::after { opacity: 1; }
    .btn:active { transform: scale(0.97); }

    /* Primary button */
    .btn-primary {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        padding: 13px 24px;
        box-shadow: 0 4px 15px var(--primary-glow);
    }
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px var(--primary-glow);
    }

    /* Secondary button */
    .btn-secondary {
        background: rgba(255,255,255,0.06);
        color: var(--text);
        border: 1px solid var(--card-border);
        padding: 13px 24px;
    }
    .btn-secondary:hover {
        background: rgba(255,255,255,0.1);
        border-color: rgba(255,255,255,0.15);
        transform: translateY(-1px);
    }

    /* Danger button */
    .btn-danger {
        background: var(--danger-light);
        color: var(--danger);
        border: 1px solid rgba(239,68,68,0.25);
        padding: 13px 24px;
    }
    .btn-danger:hover {
        background: rgba(239,68,68,0.2);
        transform: translateY(-1px);
    }

    /* Success button */
    .btn-success {
        background: var(--success-light);
        color: var(--success);
        border: 1px solid rgba(34,197,94,0.25);
        padding: 13px 24px;
    }
    .btn-success:hover {
        background: rgba(34,197,94,0.2);
        transform: translateY(-1px);
    }

    /* Ghost button */
    .btn-ghost {
        background: transparent;
        color: var(--text-secondary);
        border: 1px solid var(--card-border);
        padding: 13px 24px;
    }
    .btn-ghost:hover {
        color: var(--text);
        border-color: rgba(255,255,255,0.2);
    }

    /* Icon button */
    .btn-icon {
        width: 48px; height: 48px; padding: 0;
        border-radius: var(--radius-md);
    }

    /* Sizes */
    .btn-sm { padding: 8px 16px; font-size: 0.8rem; border-radius: var(--radius-sm); }
    .btn-lg { padding: 16px 32px; font-size: 1rem; border-radius: var(--radius-lg); }
    .btn-full { width: 100%; }

    /* Loading state */
    .btn.loading { pointer-events: none; opacity: 0.7; }
    .btn.loading::before {
        content: '';
        width: 16px; height: 16px;
        border: 2px solid rgba(255,255,255,0.3);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 0.7s linear infinite;
        margin-right: 8px;
    }

    /* ============================================
       SKELETON LOADING SYSTEM
    ============================================ */
    .skeleton {
        background: linear-gradient(90deg, var(--bg-3) 25%, rgba(255,255,255,0.05) 50%, var(--bg-3) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: var(--radius-sm);
    }

    .skeleton-text { height: 14px; width: 100%; margin-bottom: 8px; }
    .skeleton-text.w-75 { width: 75%; }
    .skeleton-text.w-50 { width: 50%; }
    .skeleton-title { height: 22px; width: 60%; margin-bottom: 16px; }
    .skeleton-card { height: 80px; width: 100%; border-radius: var(--radius-lg); }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    /* ============================================
       BADGE / CHIP SYSTEM
    ============================================ */
    .badge {
        display: inline-flex; align-items: center; gap: 5px;
        padding: 4px 12px; border-radius: 999px;
        font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px;
    }
    .badge-primary { background: var(--primary-light); color: var(--primary); border: 1px solid rgba(249,115,22,0.25); }
    .badge-success { background: var(--success-light); color: var(--success); border: 1px solid rgba(34,197,94,0.25); }
    .badge-danger { background: var(--danger-light); color: var(--danger); border: 1px solid rgba(239,68,68,0.25); }
    .badge-accent { background: var(--accent-light); color: var(--accent); border: 1px solid rgba(99,102,241,0.25); }
    .badge-muted { background: rgba(255,255,255,0.05); color: var(--text-muted); border: 1px solid var(--card-border); }

    /* ============================================
       MAIN CONTAINER
    ============================================ */
    .container {
        background: var(--card);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid var(--card-border);
        padding: 40px;
        border-radius: var(--radius-2xl);
        width: 92%;
        max-width: 880px;
        box-shadow: var(--shadow-lg), 0 0 0 1px rgba(255,255,255,0.02);
        position: relative;
        z-index: 1;
        animation: containerEntry 0.6s var(--ease-bounce) both;
    }

    @keyframes containerEntry {
        from { opacity: 0; transform: translateY(20px) scale(0.98); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* ============================================
       SIDEBAR OVERLAY
    ============================================ */
    .sidebar-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.6); backdrop-filter: blur(6px);
        display: none; z-index: 1500;
        animation: fadeIn 0.3s ease;
    }
    .sidebar-overlay.active { display: block; }

    /* ============================================
       HEADER
    ============================================ */
    .header-grid {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 32px;
        padding-bottom: 24px;
        border-bottom: 1px solid var(--card-border);
    }

    h1 {
        color: var(--primary);
        font-weight: 900;
        margin: 0;
        font-size: 1.8rem;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, var(--primary), #fb923c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ============================================
       WEATHER WIDGET
    ============================================ */
    .weather-widget {
        background: var(--primary-light);
        padding: 10px 20px;
        border-radius: var(--radius-lg);
        border: 1px solid rgba(249,115,22,0.2);
        text-align: right;
        transition: all var(--duration) var(--ease);
    }
    .weather-widget:hover {
        background: rgba(249,115,22,0.18);
        border-color: rgba(249,115,22,0.35);
    }

    .city-dropdown {
        background: transparent; color: var(--primary);
        border: 1px solid rgba(249,115,22,0.3); border-radius: 8px;
        padding: 4px 8px; font-weight: 700; cursor: pointer; outline: none;
        font-family: var(--font); font-size: 0.85rem;
        transition: border-color 0.2s;
    }
    .city-dropdown:focus { border-color: var(--primary); }
    .temp { font-size: 1.4rem; font-weight: 800; color: var(--primary); display: block; }
    .condition { font-size: 0.68rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 2px; }

    /* ============================================
       INPUT SYSTEM
    ============================================ */
    .input-wrapper {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-xl);
        padding: 8px;
        display: flex; gap: 10px;
        transition: border-color var(--duration) var(--ease), box-shadow var(--duration) var(--ease);
    }
    .input-wrapper:focus-within {
        border-color: rgba(249,115,22,0.4);
        box-shadow: 0 0 0 3px rgba(249,115,22,0.08);
    }

    input {
        flex: 1; background: transparent; border: none; color: var(--text);
        padding: 14px 16px; font-size: 1rem; outline: none; font-family: var(--font);
    }
    input::placeholder { color: var(--text-muted); }

    .btn-action {
        width: 50px; height: 50px;
        border-radius: var(--radius-md);
        border: none; cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem;
        transition: all var(--duration) var(--ease);
        flex-shrink: 0;
    }
    .btn-action:hover { transform: scale(1.08); filter: brightness(1.2); }
    .btn-action:active { transform: scale(0.95); }

    .mic-btn { background: linear-gradient(135deg, var(--accent), #4f46e5); color: white; box-shadow: 0 4px 12px rgba(99,102,241,0.3); }
    .send-btn { background: linear-gradient(135deg, var(--primary), var(--primary-dark)); color: white; box-shadow: 0 4px 12px var(--primary-glow); }
    .img-btn { background: linear-gradient(135deg, #8b5cf6, #7c3aed); color: white; box-shadow: 0 4px 12px rgba(139,92,246,0.3); }

    .mic-btn.recording { background: linear-gradient(135deg, #ef4444, #dc2626); animation: pulseBtn 1.5s infinite; }
    .img-btn.active-img { background: linear-gradient(135deg, var(--success), #16a34a); animation: pulseBtn 1.5s infinite; }

    /* ============================================
       RESULT PANEL
    ============================================ */
    #result {
        margin-top: 28px; padding: 28px;
        background: linear-gradient(145deg, var(--bg-3), var(--bg-2));
        border-radius: var(--radius-xl);
        min-height: 160px;
        border: 1px solid var(--card-border);
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
        display: flex; flex-direction: column; justify-content: center;
        position: relative; overflow: hidden;
        transition: border-color var(--duration) var(--ease);
    }
    #result:has(.res-title) { border-color: rgba(249,115,22,0.2); }

    #result::before {
        content: "● LIVE";
        position: absolute; top: 14px; right: 16px;
        font-size: 0.6rem; font-weight: 800; color: var(--success);
        letter-spacing: 1.5px; animation: blink 2.5s infinite;
        font-family: var(--font-mono);
    }

    .res-title { color: var(--primary); font-size: 1.2rem; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.3px; }
    .res-value { color: var(--text); font-size: 1.7rem; font-weight: 700; margin-bottom: 6px; }
    .res-detail { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.7; border-top: 1px solid var(--card-border); padding-top: 12px; margin-top: 4px; }

    /* ============================================
       FAB BUTTON
    ============================================ */
    .tool-fab {
        position: absolute; right: 32px; bottom: 32px;
        width: 68px; height: 68px;
        background: var(--bg-3);
        border: 2px solid var(--primary);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        cursor: pointer; font-size: 2rem;
        transition: all 0.5s var(--ease);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 0 0 var(--primary-glow);
        z-index: 1001;
    }
    .tool-fab:hover {
        transform: scale(1.12) rotate(18deg);
        background: var(--primary);
        box-shadow: 0 15px 35px rgba(0,0,0,0.5), var(--shadow-glow);
    }

    /* ============================================
       MODAL SYSTEM
    ============================================ */
    .modal-overlay {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.8); backdrop-filter: blur(12px);
        display: none; align-items: center; justify-content: center;
        z-index: 3000; opacity: 0; transition: opacity 0.3s ease;
    }
    .modal-overlay.active { display: flex; opacity: 1; }

    .modal-content {
        background: var(--card);
        border: 1px solid var(--card-border);
        border-radius: var(--radius-xl);
        padding: 35px; width: 90%; max-width: 440px;
        box-shadow: var(--shadow-lg);
        transform: translateY(30px) scale(0.97);
        transition: transform 0.4s var(--ease-bounce);
        border-top: 2px solid var(--primary);
    }
    .modal-overlay.active .modal-content { transform: translateY(0) scale(1); }

    .modal-header { color: var(--primary); font-weight: 800; margin-bottom: 24px; font-size: 1.2rem; text-align: center; letter-spacing: -0.3px; }

    .modal-input {
        width: 100%; background: rgba(255,255,255,0.04);
        border: 1px solid var(--card-border); border-radius: var(--radius-md);
        padding: 14px 16px; color: var(--text); font-size: 1rem;
        outline: none; margin-top: 8px; transition: all 0.25s ease;
        box-sizing: border-box; font-family: var(--font);
    }
    .modal-input:focus { border-color: var(--primary); background: var(--primary-light); box-shadow: 0 0 0 3px rgba(249,115,22,0.08); }

    .modal-footer { display: flex; gap: 12px; margin-top: 28px; }
    .modal-btn { flex: 1; padding: 14px; border-radius: var(--radius-md); border: none; cursor: pointer; font-weight: 800; font-size: 0.95rem; transition: all var(--duration) var(--ease); font-family: var(--font); }
    .btn-confirm { background: linear-gradient(135deg, var(--primary), var(--primary-dark)); color: white; box-shadow: 0 4px 15px var(--primary-glow); }
    .btn-confirm:hover { transform: translateY(-2px); box-shadow: 0 8px 20px var(--primary-glow); }
    .btn-cancel { background: rgba(255,255,255,0.06); color: var(--text-secondary); border: 1px solid var(--card-border); }
    .btn-cancel:hover { background: rgba(255,255,255,0.1); color: var(--text); }

    /* ============================================
       SIDEBAR
    ============================================ */
    .sidebar {
        position: fixed; right: -460px; top: 0;
        width: 420px; height: 100vh;
        background: rgba(8, 10, 12, 0.98);
        backdrop-filter: blur(40px);
        border-left: 1px solid var(--card-border);
        border-left-color: rgba(249,115,22,0.2);
        padding: 0;
        transition: right 0.7s var(--ease);
        z-index: 2000; overflow-y: auto;
        box-shadow: -20px 0 60px rgba(0,0,0,0.8);
    }
    .sidebar.active { right: 0; }

    .sidebar-header {
        padding: 28px 28px 20px;
        border-bottom: 1px solid var(--card-border);
        position: sticky; top: 0;
        background: rgba(8,10,12,0.95);
        backdrop-filter: blur(20px);
        z-index: 10;
    }

    .sidebar-body { padding: 20px 28px 40px; }

    .category-title {
        color: var(--text-muted);
        font-size: 0.68rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 3px;
        margin: 28px 0 12px;
    }

    .tool-card {
        background: rgba(255,255,255,0.03);
        border-radius: var(--radius-lg);
        padding: 16px 20px;
        margin-bottom: 8px;
        border: 1px solid rgba(255,255,255,0.05);
        cursor: pointer;
        transition: all var(--duration) var(--ease);
        display: flex; align-items: center; gap: 14px;
    }
    .tool-card:hover {
        transform: translateX(-6px);
        background: var(--primary-light);
        border-color: rgba(249,115,22,0.25);
    }
    .tool-card-icon { font-size: 1.4rem; flex-shrink: 0; }
    .tool-card-text { flex: 1; }
    .tool-card-title { font-weight: 600; font-size: 0.9rem; color: var(--text); }
    .tool-card-desc { font-size: 0.75rem; color: var(--text-muted); margin-top: 2px; }

    .stop-btn { border-color: var(--danger) !important; color: var(--danger) !important; }

    .btn-read {
        flex: 1; padding: 11px 18px;
        background: transparent;
        border: 1px solid var(--card-border);
        border-radius: var(--radius-md);
        color: var(--text-secondary);
        font-family: var(--font); font-weight: 700; font-size: 0.85rem;
        cursor: pointer; transition: all 0.25s var(--ease);
    }
    .btn-read:hover { background: rgba(255,255,255,0.06); color: var(--text); border-color: rgba(255,255,255,0.2); }

    /* ============================================
       AUTH OVERLAY
    ============================================ */
    #auth-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.92);
        display: flex; align-items: center; justify-content: center;
        z-index: 5000; backdrop-filter: blur(20px);
    }

    .auth-card {
        background: var(--card);
        border: 1px solid var(--card-border);
        border-top: 2px solid var(--primary);
        border-radius: var(--radius-2xl);
        padding: 45px; width: 90%; max-width: 400px;
        text-align: center;
        box-shadow: var(--shadow-lg);
        animation: containerEntry 0.5s var(--ease-bounce) both;
    }

    .auth-card h2 { color: var(--primary); margin-bottom: 8px; font-weight: 900; letter-spacing: -1px; font-size: 1.8rem; }
    .auth-card .auth-subtitle { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 30px; }

    .auth-input {
        width: 100%; background: rgba(255,255,255,0.04);
        border: 1px solid var(--card-border); border-radius: var(--radius-md);
        padding: 14px 16px; color: var(--text); font-size: 1rem;
        outline: none; margin-bottom: 12px; transition: all 0.25s ease;
        box-sizing: border-box; font-family: var(--font);
    }
    .auth-input:focus { border-color: var(--primary); background: var(--primary-light); box-shadow: 0 0 0 3px rgba(249,115,22,0.08); }

    .auth-btn {
        width: 100%; padding: 15px;
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white; border: none; border-radius: var(--radius-md);
        font-weight: 800; font-size: 1rem; cursor: pointer;
        transition: all var(--duration) var(--ease);
        font-family: var(--font);
        box-shadow: 0 4px 15px var(--primary-glow);
    }
    .auth-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px var(--primary-glow); }
    .auth-btn:active { transform: scale(0.98); }

    /* Message styles */
    .msg-success { background: var(--success-light); color: var(--success); border: 1px solid rgba(34,197,94,0.25); border-radius: var(--radius-sm); padding: 10px 16px; margin-top: 10px; font-size: 0.88rem; }
    .msg-error { background: var(--danger-light); color: var(--danger); border: 1px solid rgba(239,68,68,0.25); border-radius: var(--radius-sm); padding: 10px 16px; margin-top: 10px; font-size: 0.88rem; }

    /* ============================================
       DARK / LIGHT MODE TOGGLE
    ============================================ */
    .theme-toggle {
        width: 44px; height: 24px;
        background: var(--bg-3);
        border: 1px solid var(--card-border);
        border-radius: 999px; cursor: pointer;
        position: relative; transition: background 0.3s ease;
        flex-shrink: 0;
    }
    .theme-toggle::after {
        content: '';
        position: absolute; top: 3px; left: 3px;
        width: 16px; height: 16px;
        background: var(--text-muted);
        border-radius: 50%;
        transition: all 0.3s var(--ease);
    }
    body.light-mode .theme-toggle { background: var(--primary-light); border-color: var(--primary); }
    body.light-mode .theme-toggle::after { left: calc(100% - 19px); background: var(--primary); }

    /* ============================================
       ANIMATIONS
    ============================================ */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes fadeInDown { from { opacity: 0; transform: translateY(-16px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes scaleIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
    @keyframes slideInRight { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes pulseBtn { 0% { box-shadow: 0 0 0 0 var(--primary-glow); } 70% { box-shadow: 0 0 0 16px transparent; } 100% { box-shadow: 0 0 0 0 transparent; } }

    .animate-in { animation: fadeInUp 0.4s var(--ease) both; }
    .animate-scale { animation: scaleIn 0.35s var(--ease-bounce) both; }

    /* Stagger children */
    .stagger > *:nth-child(1) { animation-delay: 0.05s; }
    .stagger > *:nth-child(2) { animation-delay: 0.1s; }
    .stagger > *:nth-child(3) { animation-delay: 0.15s; }
    .stagger > *:nth-child(4) { animation-delay: 0.2s; }
    .stagger > *:nth-child(5) { animation-delay: 0.25s; }

    /* ============================================
       SCROLLBAR
    ============================================ */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-thumb { background: rgba(249,115,22,0.4); border-radius: 999px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--primary); }
    ::-webkit-scrollbar-track { background: transparent; }

    /* ============================================
       RESPONSIVE
    ============================================ */
    @media (max-width: 600px) {
        .container { padding: 24px 18px; border-radius: var(--radius-xl); width: 96%; }
        h1 { font-size: 1.4rem; }
        .sidebar { width: 100%; right: -100%; }
        .tool-fab { right: 20px; bottom: 20px; width: 58px; height: 58px; font-size: 1.7rem; }
    }

    /* ============================================
       APP SHELL LAYOUT
    ============================================ */
    body { display: block; }

    /* ============================================
       NAV SIDEBAR (left permanent)
    ============================================ */
    .nav-sidebar {
        position: fixed; top: 0; left: 0;
        width: 260px; height: 100vh;
        background: rgba(8, 10, 12, 0.97);
        backdrop-filter: blur(40px);
        border-right: 1px solid rgba(249,115,22,0.12);
        display: flex; flex-direction: column;
        transition: width 0.4s var(--ease), transform 0.4s var(--ease);
        z-index: 2500; overflow: hidden;
        box-shadow: 4px 0 30px rgba(0,0,0,0.4);
    }
    .nav-sidebar.collapsed { width: 64px; }

    .nav-logo {
        display: flex; align-items: center; gap: 12px;
        padding: 22px 18px 18px;
        border-bottom: 1px solid var(--card-border);
        color: var(--primary);
        font-weight: 900; font-size: 1rem;
        letter-spacing: -0.5px; white-space: nowrap;
        flex-shrink: 0; overflow: hidden;
    }
    .nav-logo-icon { font-size: 1.5rem; flex-shrink: 0; }
    .nav-logo-text { transition: opacity 0.3s ease; }
    .nav-sidebar.collapsed .nav-logo-text { opacity: 0; pointer-events: none; }

    .nav-links { flex: 1; padding: 10px 8px; overflow-y: auto; overflow-x: hidden; }

    .nav-item {
        display: flex; align-items: center; gap: 14px;
        padding: 11px 13px; border-radius: var(--radius-md);
        cursor: pointer; color: var(--text-secondary);
        white-space: nowrap; margin-bottom: 3px;
        transition: all 0.25s var(--ease);
        border: 1px solid transparent; overflow: hidden;
    }
    .nav-item:hover { background: var(--primary-light); color: var(--primary); }
    .nav-item.active { background: var(--primary-light); color: var(--primary); border-color: rgba(249,115,22,0.2); }

    .nav-icon { font-size: 1.2rem; flex-shrink: 0; width: 26px; text-align: center; }
    .nav-label { font-weight: 600; font-size: 0.88rem; transition: opacity 0.3s ease; }
    .nav-sidebar.collapsed .nav-label { opacity: 0; pointer-events: none; }

    .nav-bottom { padding: 10px 8px 16px; border-top: 1px solid var(--card-border); }

    /* ============================================
       TOP HEADER BAR
    ============================================ */
    .top-header {
        position: fixed; top: 0; left: 260px; right: 0;
        height: 62px;
        background: rgba(8, 10, 12, 0.95);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--card-border);
        display: flex; align-items: center; gap: 10px;
        padding: 0 20px 0 14px;
        z-index: 2000;
        transition: left 0.4s var(--ease);
    }
    .top-header.nav-collapsed { left: 64px; }

    .header-hamburger {
        display: none;
        background: none; border: none; color: var(--text);
        font-size: 1.3rem; cursor: pointer;
        padding: 6px 10px; border-radius: var(--radius-sm);
        transition: background 0.2s; flex-shrink: 0;
    }
    .header-hamburger:hover { background: rgba(255,255,255,0.08); }

    .header-collapse-btn {
        background: none; border: 1px solid var(--card-border);
        color: var(--text-muted); font-size: 0.85rem;
        cursor: pointer; padding: 5px 9px;
        border-radius: var(--radius-sm);
        transition: all 0.2s; flex-shrink: 0; line-height: 1;
    }
    .header-collapse-btn:hover { background: rgba(255,255,255,0.06); color: var(--text); border-color: rgba(255,255,255,0.15); }

    .header-title {
        flex: 1; font-weight: 700; font-size: 0.95rem;
        color: var(--text); letter-spacing: -0.2px;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .header-right { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }

    .header-profile-btn {
        width: 34px; height: 34px;
        background: var(--primary-light);
        border: 1px solid rgba(249,115,22,0.3);
        border-radius: 50%; cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        font-size: 1rem; transition: all 0.25s; flex-shrink: 0;
    }
    .header-profile-btn:hover { background: rgba(249,115,22,0.25); transform: scale(1.05); }

    /* ============================================
       MAIN CONTENT AREA
    ============================================ */
    .main-content {
        margin-left: 260px;
        padding-top: 62px;
        min-height: 100vh;
        display: flex; align-items: flex-start; justify-content: center;
        padding-bottom: 60px;
        padding-top: calc(62px + 40px);
        transition: margin-left 0.4s var(--ease);
    }
    .main-content.nav-collapsed { margin-left: 64px; }
    .main-content .container { animation: none; width: 92%; max-width: 880px; }

    /* Nav mobile overlay */
    .nav-overlay {
        display: none; position: fixed; inset: 0;
        background: rgba(0,0,0,0.65); backdrop-filter: blur(4px);
        z-index: 2400; animation: fadeIn 0.25s ease;
    }
    .nav-overlay.active { display: block; }

    /* History sidebar above nav */
    #historySidebar { z-index: 3000 !important; }

    /* ============================================
       QUICK ACTIONS GRID
    ============================================ */
    .quick-actions {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-top: 16px;
    }

    .qa-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 14px 8px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: all 0.25s var(--ease);
        color: var(--text-secondary);
        font-family: var(--font);
    }

    .qa-btn:hover {
        background: var(--primary-light);
        border-color: rgba(249,115,22,0.3);
        color: var(--primary);
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }

    .qa-btn:active { transform: translateY(0) scale(0.97); }

    .qa-btn.active {
        background: var(--danger-light);
        border-color: rgba(239,68,68,0.4);
        color: var(--danger);
        animation: pulseBtn 1.5s infinite;
    }

    .qa-icon { font-size: 1.4rem; line-height: 1; }

    .qa-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        text-transform: uppercase;
        white-space: nowrap;
    }

    /* ============================================
       WEATHER INLINE (header)
    ============================================ */
    .weather-inline {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(249,115,22,0.08);
        border: 1px solid rgba(249,115,22,0.18);
        border-radius: var(--radius-md);
        padding: 6px 12px;
    }

    .city-select-inline {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        font-size: 0.82rem;
        font-weight: 600;
        cursor: pointer;
        outline: none;
        font-family: var(--font);
        max-width: 100px;
    }

    .city-select-inline option { background: var(--bg-2); color: var(--text); }

    .weather-data { display: flex; flex-direction: column; align-items: flex-end; line-height: 1.1; }

    .weather-temp {
        font-size: 1.1rem;
        font-weight: 800;
        color: var(--primary);
        letter-spacing: -0.5px;
    }

    .weather-cond {
        font-size: 0.6rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        white-space: nowrap;
        max-width: 140px;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* ============================================
       READ CONTROLS
    ============================================ */
    .read-controls {
        display: flex;
        gap: 8px;
        margin-top: 14px;
    }

    .btn-read-new {
        flex: 2; padding: 10px 16px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: var(--radius-md);
        color: var(--text-secondary);
        font-family: var(--font); font-weight: 600; font-size: 0.85rem;
        cursor: pointer; transition: all 0.25s var(--ease);
        display: flex; align-items: center; justify-content: center; gap: 6px;
    }
    .btn-read-new:hover { background: rgba(255,255,255,0.08); color: var(--text); border-color: rgba(255,255,255,0.2); }

    .btn-stop-new {
        flex: 1; padding: 10px 16px;
        background: var(--danger-light);
        border: 1px solid rgba(239,68,68,0.2);
        border-radius: var(--radius-md);
        color: var(--danger); font-family: var(--font); font-weight: 600; font-size: 0.85rem;
        cursor: pointer; transition: all 0.25s var(--ease);
    }
    .btn-stop-new:hover { background: rgba(239,68,68,0.2); }

    .btn-save-new {
        flex: 1; padding: 10px 16px;
        background: var(--success-light);
        border: 1px solid rgba(34,197,94,0.2);
        border-radius: var(--radius-md);
        color: var(--success); font-family: var(--font); font-weight: 600; font-size: 0.85rem;
        cursor: pointer; transition: all 0.25s var(--ease);
    }
    .btn-save-new:hover { background: rgba(34,197,94,0.2); }

    /* ============================================
       CONTAINER MAX WIDTH UPGRADE
    ============================================ */
    .main-content .container { max-width: 960px; width: 94%; }

    /* ============================================
       MOBILE RESPONSIVE (sidebar layout)
    ============================================ */
    @media (max-width: 768px) {
        .nav-sidebar { transform: translateX(-100%); width: 260px !important; }
        .nav-sidebar.mobile-open { transform: translateX(0); }
        .top-header { left: 0 !important; }
        .header-hamburger { display: flex; align-items: center; justify-content: center; }
        .header-collapse-btn { display: none; }
        .main-content { margin-left: 0 !important; }
        .container { width: 96%; }
        .quick-actions { grid-template-columns: repeat(4, 1fr); gap: 8px; }
        .qa-icon { font-size: 1.2rem; }
        .qa-label { font-size: 0.65rem; }
        .weather-cond { display: none; }
        .city-select-inline { max-width: 70px; font-size: 0.75rem; }
        .weather-inline { padding: 5px 8px; gap: 6px; }
    }
</style>
"""
