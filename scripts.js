// --- 🔐 GÜVENLİK KAPISI (YENİ EKLENDİ) ---
async function girisYap() {
    const email = document.getElementById('loginEmail').value;
    const pass = document.getElementById('loginPass').value;
    const btn = document.querySelector('.auth-btn');

    if(!email || !pass) return alert("Şefim, bilgileri eksik girmeyelim.");

    btn.innerText = "⏳ Kontrol Ediliyor...";

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: pass })
        });
        
        const data = await response.json();

        if (response.ok) {
            document.getElementById('auth-overlay').style.display = 'none';
            document.getElementById('mainApp').style.display = 'block';
            havaGuncelle();
        } else {
            alert("Hata: " + data.detail);
            btn.innerText = "Şantiyeye Giriş Yap";
        }
    } catch (e) {
        alert("Bağlantı hatası! Sunucu çalışıyor mu?");
        btn.innerText = "Şantiyeye Giriş Yap";
    }
}

// --- 🌑 SİDEBAR KONTROLLERİ ---
function toggleSidebar() {
    const side = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const isActive = side.classList.toggle('active');
    if (isActive) overlay.classList.add('active');
    else overlay.classList.remove('active');
}

// --- 💾 RAPOR KAYDETME SİSTEMİ ---
async function gunlukRaporuKaydet() {
    const turkceMetin = document.getElementById('analizMetni') ? document.getElementById('analizMetni').innerText : "";
    const ingilizceMetin = document.getElementById('englishMetni') ? document.getElementById('englishMetni').innerText : "";
    const resBox = document.getElementById('result');
    
    if (!turkceMetin) {
        alert("Şefim, kaydedecek bir analiz yok! Önce bir soru sorun.");
        return;
    }

    const tamRapor = `TURKISH ANALYSIS:\\n${turkceMetin}\\n\\nENGLISH REPORT:\\n${ingilizceMetin}`;

    try {
        const response = await fetch('/rapor_kaydet', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rapor_metni: tamRapor })
        });
        const data = await response.json();
        
        resBox.innerHTML += `<div style="margin-top:15px; padding:10px; background:rgba(46,204,113,0.2); color:#2ecc71; border-radius:10px; text-align:center; font-weight:bold;">✅ \${data.mesaj}</div>`;
    } catch (e) {
        alert("Rapor kaydedilemedi!");
    }
}

// --- 🗂️ ARŞİV VE GEÇMİŞ KONTROLLERİ ---
let butunRaporlar = [];

function toggleHistory() {
    const sidebar = document.getElementById('historySidebar');
    if (sidebar.style.left === '0px') {
        sidebar.style.left = '-350px';
    } else {
        sidebar.style.left = '0px';
        loadHistoryList(); 
    }
}

async function loadHistoryList() {
    const listDiv = document.getElementById('historyList');
    const sortType = document.getElementById('historySort').value;
    listDiv.innerHTML = "<i style='color:#888;'>Kayıtlar aranıyor...</i>";

    try {
        const response = await fetch('/rapor_listesi');
        const data = await response.json();
        butunRaporlar = data.raporlar;
        renderHistoryList(butunRaporlar, sortType);
    } catch (e) {
        listDiv.innerHTML = "<span style='color:red;'>Bağlantı hatası!</span>";
    }
}

// ... (diğer kodların aynen devam ediyor)

async function runCalc(type) {
    let title, fields, url;
    if(type === 'beton') { title = "🧱 Beton Metrajı"; fields = [{key:'v1',label:'Boy (m)',placeholder:'5'}, {key:'v2',label:'En (m)',placeholder:'0.5'}, {key:'v3',label:'Yükseklik (m)',placeholder:'2.8'}]; } 
    else if(type === 'demir_ag') { title = "⚖️ Donatı Ağırlığı"; fields = [{key:'v1',label:'Çap (mm)',placeholder:'14'}, {key:'v2',label:'Uzunluk (m)',placeholder:'120'}]; } 
    
    const dataInput = await openModal(title, fields);
    if (!dataInput) return;

    const resBox = document.getElementById('result');
    resBox.innerHTML = "<i>Şefim, hesaplanıyor...</i>";
    
    try {
        const response = await fetch(`/hesapla?tip=${type}&v1=${dataInput.v1}&v2=${dataInput.v2 || 0}&v3=${dataInput.v3 || 0}`);
        const data = await response.json();
        resBox.innerHTML = `<div class="res-title">📊 ANALİZ SONUCU</div><div class="res-value">${data.sonuc}</div><div class="res-detail">${data.detay}</div>`;
        sesliOku();
    } catch (e) { 
        resBox.innerHTML = "⚠️ HESAPLAMA HATASI"; 
    }
}