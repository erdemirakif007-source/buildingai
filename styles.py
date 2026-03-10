CSS_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    :root { 
        --primary: #e67e22; 
        --bg: #0f1113; 
        --card: rgba(30, 33, 37, 0.75); 
        --text: #f0f0f0;
        --text-gray: #a0a0a0;
        --accent: #2563eb;
    }

    body { 
        font-family: 'Inter', sans-serif; 
        background: radial-gradient(circle at top right, #1a1c20, #0f1113); 
        color: var(--text); 
        margin: 0; 
        min-height: 100vh;
        display: flex; 
        align-items: center; 
        justify-content: center;
        overflow-x: hidden;
    }

    .container { 
        background: var(--card); 
        backdrop-filter: blur(25px); 
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 45px; 
        border-radius: 32px; 
        width: 90%; 
        max-width: 850px; 
        box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.6);
        position: relative;
    }

    /* 🌑 SIDEBAR OVERLAY (Karartma Katmanı) */
    .sidebar-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(4px);
        display: none; z-index: 1500; transition: opacity 0.4s ease;
    }
    .sidebar-overlay.active { display: block; opacity: 1; }

    .header-grid { display: flex; justify-content: space-between; align-items: center; margin-bottom: 35px; }
    h1 { color: var(--primary); font-weight: 700; margin: 0; font-size: 1.9rem; letter-spacing: -1.5px; }

    .weather-widget { 
        background: rgba(230, 126, 34, 0.1); padding: 12px 24px; 
        border-radius: 20px; border: 1px solid rgba(230, 126, 34, 0.25); text-align: right;
    }
    .city-dropdown { background: transparent; color: var(--primary); border: 1px solid rgba(230, 126, 34, 0.4); border-radius: 10px; padding: 5px; font-weight: 700; cursor: pointer; outline: none; }
    .temp { font-size: 1.5rem; font-weight: 800; color: var(--primary); display: block; }
    .condition { font-size: 0.75rem; color: var(--text-gray); text-transform: uppercase; letter-spacing: 1.5px; }

    /* 🎙️ GİRİŞ ALANI VE BUTONLAR */
    .input-wrapper { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 22px; padding: 10px; display: flex; gap: 12px; }
    input { flex: 1; background: transparent; border: none; color: white; padding: 15px; font-size: 1.05rem; outline: none; }
    .btn-action { width: 52px; height: 52px; border-radius: 18px; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.4s; }
    
    .mic-btn { background: var(--accent); color: white; }
    .send-btn { background: var(--primary); color: white; }
    .mic-btn.recording { background: #dc2626; animation: pulse 1.5s infinite; }
    
    /* 📸 FOTOĞRAF BUTONU STİLLERİ (YENİ EKLENDİ) */
    .img-btn { background: #8b5cf6; color: white; }
    .img-btn.active-img { background: #2ecc71; animation: pulse 1.5s infinite; }

    #result { 
        margin-top: 35px; padding: 30px; background: linear-gradient(145deg, #14171a, #0b0d0e); 
        border-radius: 28px; min-height: 180px; border: 2px solid rgba(230, 126, 34, 0.15);
        box-shadow: inset 0 4px 15px rgba(0,0,0,0.8), 0 10px 30px rgba(0,0,0,0.4);
        display: flex; flex-direction: column; justify-content: center; position: relative; overflow: hidden;
    }
    #result::before {
        content: "● LIVE DATA"; position: absolute; top: 15px; left: 20px;
        font-size: 0.65rem; font-weight: 800; color: #2ecc71; letter-spacing: 1px; animation: blink 2s infinite;
    }

    .res-title { color: var(--primary); font-size: 1.4rem; font-weight: 800; margin-bottom: 10px; }
    .res-value { color: #fff; font-size: 1.8rem; font-weight: 700; margin-bottom: 5px; }
    .res-detail { color: var(--text-gray); font-size: 0.95rem; font-style: italic; border-top: 1px solid #333; padding-top: 10px; }

    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

    .tool-fab {
        position: absolute; right: 35px; bottom: 35px; width: 75px; height: 75px;
        background: var(--bg); border: 4px solid var(--primary); border-radius: 50%;
        display: flex; align-items: center; justify-content: center; cursor: pointer;
        font-size: 2.2rem; transition: 0.5s cubic-bezier(0.19, 1, 0.22, 1); box-shadow: 0 15px 35px rgba(0,0,0,0.7); z-index: 1001;
    }
    .tool-fab:hover { transform: scale(1.1) rotate(18deg); background: var(--primary); box-shadow: 0 0 30px rgba(230, 126, 34, 0.5); }

    .modal-overlay {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(10px);
        display: none; align-items: center; justify-content: center; z-index: 3000; opacity: 0; transition: opacity 0.3s ease;
    }
    .modal-overlay.active { display: flex; opacity: 1; }
    .modal-content {
        background: var(--card); border: 2px solid var(--primary); border-radius: 28px; padding: 35px; width: 90%; max-width: 420px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.8); transform: translateY(30px); transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .modal-overlay.active .modal-content { transform: translateY(0); }
    .modal-header { color: var(--primary); font-weight: 800; margin-bottom: 25px; font-size: 1.3rem; text-align: center; letter-spacing: 1px; }
    .modal-input {
        width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15);
        border-radius: 14px; padding: 15px; color: white; font-size: 1rem; outline: none; margin-top: 10px; transition: 0.3s; box-sizing: border-box;
    }
    .modal-input:focus { border-color: var(--primary); background: rgba(230, 126, 34, 0.08); }
    .modal-footer { display: flex; gap: 15px; margin-top: 30px; }
    .modal-btn { flex: 1; padding: 15px; border-radius: 15px; border: none; cursor: pointer; font-weight: 800; transition: 0.3s; }
    .btn-confirm { background: var(--primary); color: white; }
    .btn-cancel { background: rgba(255,255,255,0.1); color: white; }

    .sidebar {
        position: fixed; right: -450px; top: 0; width: 400px; height: 100vh;
        background: rgba(10, 12, 14, 0.99); backdrop-filter: blur(40px); border-left: 3px solid var(--primary); padding: 35px;
        transition: 0.7s cubic-bezier(0.19, 1, 0.22, 1); z-index: 2000; overflow-y: auto; box-shadow: -20px 0 60px rgba(0,0,0,0.8);
    }
    .sidebar.active { right: 0; }
    .category-title { color: var(--primary); font-size: 0.8rem; font-weight: 800; text-transform: uppercase; letter-spacing: 3px; margin: 35px 0 15px 5px; border-bottom: 2px solid rgba(255,255,255,0.08); padding-bottom: 8px; }
    .tool-card { background: rgba(255,255,255,0.04); border-radius: 20px; padding: 20px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.07); cursor: pointer; transition: 0.3s; }
    .tool-card:hover { transform: translateX(-10px); background: rgba(230, 126, 34, 0.15); border-color: var(--primary); }
    
    .stop-btn { border-color: #dc2626 !important; color: #dc2626 !important; }

    /* 🧱 ŞEFİM, BURADAN AŞAĞISI SAAS GİRİŞ PANELİ İÇİN EKLENEN KISIMLARDIR */
    #auth-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0, 0, 0, 0.9); display: flex; align-items: center; justify-content: center;
        z-index: 5000; backdrop-filter: blur(15px);
    }
    .auth-card {
        background: var(--card); border: 2px solid var(--primary); border-radius: 32px; 
        padding: 45px; width: 90%; max-width: 400px; text-align: center;
        box-shadow: 0 30px 60px rgba(0,0,0,0.8);
    }
    .auth-card h2 { color: var(--primary); margin-bottom: 25px; font-weight: 800; letter-spacing: -1px; }
    .auth-input {
        width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15);
        border-radius: 14px; padding: 15px; color: white; font-size: 1rem; outline: none; 
        margin-bottom: 15px; transition: 0.3s; box-sizing: border-box;
    }
    .auth-input:focus { border-color: var(--primary); background: rgba(230, 126, 34, 0.08); }
    .auth-btn {
        width: 100%; padding: 15px; background: var(--primary); color: white; 
        border: none; border-radius: 14px; font-weight: 800; cursor: pointer; transition: 0.4s;
    }
    .auth-btn:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(230, 126, 34, 0.4); }

    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.5); } 70% { box-shadow: 0 0 0 20px rgba(46, 204, 113, 0); } 100% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); } }

    /* Modern Scrollbar */
    .sidebar::-webkit-scrollbar { width: 8px; }
    .sidebar::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 10px; }
    .sidebar::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
</style>
"""