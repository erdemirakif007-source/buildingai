ADMIN_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BuildingAI Pro — Admin</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;color:#f0f0f0;font-family:Arial,sans-serif;min-height:100vh}
.header{background:#161b22;border-bottom:2px solid #e67e22;padding:20px 30px;display:flex;justify-content:space-between;align-items:center}
.header h1{color:#e67e22;font-size:1.4rem}
.login-screen{display:flex;align-items:center;justify-content:center;min-height:100vh}
.login-box{background:#161b22;border:1px solid #e67e22;border-radius:20px;padding:40px;width:90%;max-width:400px;text-align:center}
.login-box h2{color:#e67e22;margin-bottom:25px}
.input{width:100%;background:rgba(255,255,255,0.05);border:1px solid #333;color:white;padding:12px 16px;border-radius:10px;font-size:1rem;margin-bottom:12px;outline:none}
.input:focus{border-color:#e67e22}
.btn{width:100%;padding:13px;background:#e67e22;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;font-size:1rem}
.btn:hover{background:#d35400}
.btn-green{background:#2ecc71}.btn-green:hover{background:#27ae60}
.btn-red{background:#e74c3c}.btn-red:hover{background:#c0392b}
.btn-small{width:auto;padding:6px 14px;font-size:0.85rem;border-radius:8px}
.container{padding:30px;max-width:1200px;margin:0 auto}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-bottom:30px}
.stat-card{background:#161b22;border:1px solid #30363d;border-radius:14px;padding:20px;text-align:center}
.stat-card .num{font-size:2rem;font-weight:800;color:#e67e22}
.stat-card .label{color:#aaa;font-size:0.85rem;margin-top:5px}
.stat-card.green .num{color:#2ecc71}
.stat-card.blue .num{color:#3498db}
.section{background:#161b22;border:1px solid #30363d;border-radius:16px;padding:25px;margin-bottom:25px}
.section h2{color:#e67e22;margin-bottom:20px;font-size:1.1rem}
.table{width:100%;border-collapse:collapse}
.table th{color:#aaa;font-size:0.85rem;padding:10px 12px;text-align:left;border-bottom:1px solid #30363d}
.table td{padding:12px;border-bottom:1px solid #1a1d21;font-size:0.9rem;vertical-align:middle}
.table tr:hover td{background:rgba(255,255,255,0.02)}
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:0.78rem;font-weight:bold}
.badge-pro{background:rgba(46,204,113,0.15);color:#2ecc71;border:1px solid #2ecc71}
.badge-free{background:rgba(230,126,34,0.1);color:#e67e22;border:1px solid #e67e22}
.badge-admin{background:rgba(52,152,219,0.15);color:#3498db;border:1px solid #3498db}
.msg{padding:10px 16px;border-radius:8px;margin-top:10px;font-size:0.9rem}
.msg-success{background:rgba(46,204,113,0.1);color:#2ecc71;border:1px solid #2ecc71}
.msg-error{background:rgba(231,76,60,0.1);color:#e74c3c;border:1px solid #e74c3c}
.nav{display:flex;gap:10px;margin-bottom:25px;flex-wrap:wrap}
.nav-btn{padding:8px 18px;background:#1a1d21;border:1px solid #333;color:#aaa;border-radius:8px;cursor:pointer;font-size:0.9rem}
.nav-btn.active{background:rgba(230,126,34,0.15);border-color:#e67e22;color:#e67e22}
#loginScreen{display:flex}
#mainPanel{display:none}
</style>
</head>
<body>

<div id="loginScreen" class="login-screen">
  <div class="login-box">
    <div style="font-size:2.5rem;margin-bottom:10px">🏗️</div>
    <h2>Admin Panel</h2>
    <p style="color:#aaa;margin-bottom:25px;font-size:0.9rem">BuildingAI Pro</p>
    <input type="email" id="adminEmail" class="input" placeholder="Admin email">
    <input type="password" id="adminPass" class="input" placeholder="Şifre">
    <button class="btn" onclick="adminGiris()">Giriş Yap</button>
    <div id="loginMsg"></div>
  </div>
</div>

<div id="mainPanel">
  <div class="header">
    <h1>🏗️ BuildingAI Pro — Admin</h1>
    <div style="display:flex;align-items:center;gap:15px">
      <span id="adminWelcome" style="color:#aaa;font-size:0.9rem"></span>
      <button onclick="adminCikis()" style="background:none;border:1px solid #555;color:#aaa;padding:6px 14px;border-radius:8px;cursor:pointer;font-size:0.85rem">Çıkış</button>
    </div>
  </div>
  <div class="container">
    <div class="nav">
      <button class="nav-btn active" onclick="sekmeAc('istatistik',this)">📊 İstatistikler</button>
      <button class="nav-btn" onclick="sekmeAc('kullanicilar',this)">👥 Kullanıcılar</button>
    </div>

    <div id="sekme-istatistik">
      <div class="stats-grid" id="statsGrid"><div class="stat-card"><div class="num">...</div><div class="label">Yükleniyor</div></div></div>
      <div class="section"><h2>💰 Gelir Özeti</h2><div id="gelirOzet" style="color:#aaa">Yükleniyor...</div></div>
    </div>

    <div id="sekme-kullanicilar" style="display:none">
      <div class="section">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;flex-wrap:wrap;gap:10px">
          <h2 style="margin:0">👥 Kullanıcılar</h2>
          <input type="text" id="searchInput" class="input" style="width:220px;margin:0" placeholder="Email ara..." oninput="kullanicilariFiltrele()">
        </div>
        <div style="overflow-x:auto">
          <table class="table">
            <thead><tr><th>ID</th><th>Ad Soyad</th><th>Email</th><th>Plan</th><th>Kayıt</th><th>İşlemler</th></tr></thead>
            <tbody id="kullaniciTablosu"></tbody>
          </table>
        </div>
      </div>
    </div>

    <div id="islemMsg"></div>
  </div>
</div>

<script>
let adminToken = localStorage.getItem('admin_token');
let tumKullanicilar = [];

window.onload = () => { if(adminToken) panelYukle(); };

async function adminGiris() {
  const email = document.getElementById('adminEmail').value;
  const pass = document.getElementById('adminPass').value;
  try {
    const res = await fetch('/login', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password:pass})});
    const data = await res.json();
    if(res.ok && data.token) {
      const check = await fetch('/admin/istatistikler?token='+data.token);
      if(check.ok) {
        adminToken = data.token;
        localStorage.setItem('admin_token', adminToken);
        document.getElementById('adminWelcome').textContent = email;
        panelYukle();
      } else {
        document.getElementById('loginMsg').innerHTML = '<div class="msg msg-error">Bu hesabin admin yetkisi yok.</div>';
      }
    } else {
      document.getElementById('loginMsg').innerHTML = '<div class="msg msg-error">Email veya sifre hatali.</div>';
    }
  } catch(e) { document.getElementById('loginMsg').innerHTML = '<div class="msg msg-error">Baglanti hatasi.</div>'; }
}

async function panelYukle() {
  document.getElementById('loginScreen').style.display = 'none';
  document.getElementById('mainPanel').style.display = 'block';
  await istatistikleriYukle();
  await kullanicilariYukle();
}

async function istatistikleriYukle() {
  try {
    const res = await fetch('/admin/istatistikler?token='+adminToken);
    if(res.status===401||res.status===403){adminCikis();return;}
    const d = await res.json();
    document.getElementById('statsGrid').innerHTML = `
      <div class="stat-card"><div class="num">${d.toplam_kullanici}</div><div class="label">Toplam Kullanici</div></div>
      <div class="stat-card green"><div class="num">${d.pro_kullanici}</div><div class="label">Pro Kullanici</div></div>
      <div class="stat-card"><div class="num">${d.free_kullanici}</div><div class="label">Free Kullanici</div></div>
      <div class="stat-card blue"><div class="num">${d.yeni_kayit_7gun}</div><div class="label">Yeni (7 gun)</div></div>
      <div class="stat-card green"><div class="num">$${d.tahmini_aylik_gelir}</div><div class="label">Tahmini Gelir/Ay</div></div>
      <div class="stat-card"><div class="num">${d.toplam_rapor}</div><div class="label">Toplam Rapor</div></div>
    `;
    document.getElementById('gelirOzet').innerHTML = `
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px">
        <div style="background:rgba(46,204,113,0.08);border:1px solid rgba(46,204,113,0.2);border-radius:12px;padding:16px">
          <div style="color:#2ecc71;font-size:1.5rem;font-weight:800">$${d.tahmini_aylik_gelir}</div>
          <div style="color:#aaa;font-size:0.85rem;margin-top:5px">Tahmini Aylik Gelir</div>
        </div>
        <div style="background:rgba(52,152,219,0.08);border:1px solid rgba(52,152,219,0.2);border-radius:12px;padding:16px">
          <div style="color:#3498db;font-size:1.5rem;font-weight:800">$${d.tahmini_aylik_gelir*12}</div>
          <div style="color:#aaa;font-size:0.85rem;margin-top:5px">Tahmini Yillik Gelir</div>
        </div>
        <div style="background:rgba(230,126,34,0.08);border:1px solid rgba(230,126,34,0.2);border-radius:12px;padding:16px">
          <div style="color:#e67e22;font-size:1.5rem;font-weight:800">${d.pro_kullanici}/${d.toplam_kullanici}</div>
          <div style="color:#aaa;font-size:0.85rem;margin-top:5px">Pro/Toplam Oran</div>
        </div>
      </div>
    `;
  } catch(e) {}
}

async function kullanicilariYukle() {
  try {
    const res = await fetch('/admin/kullanicilar?token='+adminToken);
    if(!res.ok) return;
    tumKullanicilar = await res.json();
    kullanicilariRender(tumKullanicilar);
  } catch(e) {}
}

function kullanicilariRender(liste) {
  const tbody = document.getElementById('kullaniciTablosu');
  if(!liste.length){tbody.innerHTML='<tr><td colspan="6" style="text-align:center;color:#aaa;padding:30px">Kullanici bulunamadi</td></tr>';return;}
  tbody.innerHTML = liste.map(u => {
    const isAdmin = u.email === 'erdemirakif007@gmail.com';
    const badge = isAdmin ? '<span class="badge badge-admin">ADMIN</span>' :
                  u.plan==='pro' ? '<span class="badge badge-pro">PRO</span>' :
                  '<span class="badge badge-free">FREE</span>';
    const tarih = u.created_at ? u.created_at.substring(0,10) : '-';
    const islemler = isAdmin ? '<span style="color:#555;font-size:0.8rem">—</span>' :
      (u.plan==='pro'
        ? `<button class="btn btn-small btn-red" style="margin-right:6px" onclick="planDegistir(${u.id},'free')">Free Yap</button>`
        : `<button class="btn btn-small btn-green" style="margin-right:6px" onclick="planDegistir(${u.id},'pro')">Pro Yap ⚡</button>`
      ) + `<button class="btn btn-small btn-red" onclick="kullaniciyiSil(${u.id},'${u.email}')">Sil</button>`;
    return `<tr><td style="color:#555">#${u.id}</td><td>${u.full_name}</td><td style="color:#aaa">${u.email}</td><td>${badge}</td><td style="color:#555">${tarih}</td><td>${islemler}</td></tr>`;
  }).join('');
}

function kullanicilariFiltrele() {
  const q = document.getElementById('searchInput').value.toLowerCase();
  kullanicilariRender(tumKullanicilar.filter(u => u.email.toLowerCase().includes(q) || u.full_name.toLowerCase().includes(q)));
}

async function planDegistir(userId, yeniPlan) {
  try {
    const res = await fetch('/admin/plan-degistir',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token:adminToken,user_id:userId,plan:yeniPlan})});
    const data = await res.json();
    if(res.ok){mesajGoster(data.mesaj,'success');await kullanicilariYukle();await istatistikleriYukle();}
    else mesajGoster(data.detail,'error');
  } catch(e){mesajGoster('Hata olustu.','error');}
}

async function kullaniciyiSil(userId, email) {
  if(!confirm(email+' kullanicisini silmek istediginizden emin misiniz?')) return;
  try {
    const res = await fetch('/admin/kullanici-sil/'+userId+'?token='+adminToken,{method:'DELETE'});
    const data = await res.json();
    if(res.ok){mesajGoster(data.mesaj,'success');await kullanicilariYukle();await istatistikleriYukle();}
  } catch(e){mesajGoster('Hata olustu.','error');}
}

function sekmeAc(sekme, btn) {
  document.querySelectorAll('[id^="sekme-"]').forEach(el=>el.style.display='none');
  document.getElementById('sekme-'+sekme).style.display='block';
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
}

function mesajGoster(msg, tip) {
  const el = document.getElementById('islemMsg');
  el.innerHTML = '<div class="msg msg-'+tip+'">'+msg+'</div>';
  setTimeout(()=>el.innerHTML='',4000);
}

function adminCikis() {
  localStorage.removeItem('admin_token');
  adminToken = null;
  document.getElementById('loginScreen').style.display='flex';
  document.getElementById('mainPanel').style.display='none';
}
</script>
</body>
</html>"""
