/**
 * ifcExportGuide.ts
 *
 * BuildingAI BIM Viewer — IFC Export Rehberi Modal
 *
 * Kullanıcılara Revit ve AutoCAD'den IFC export yapmanın
 * nasıl yapılacağını gösteren yardımcı bir modal penceresi.
 *
 * ─── TABS ─────────────────────────────────────────────
 *  Tab 1 : Revit'ten IFC Export   (5 adım)
 *  Tab 2 : AutoCAD'den IFC Export (3 alternatif seçenek)
 *  Tab 3 : IFC Nedir?             (bilgi paragrafları)
 *  Tab 4 : Sık Sorulan Sorular    (SSS — akordiyon)
 *
 * ─── DAVRANIŞLAR ──────────────────────────────────────
 *  - ESC ile kapanır
 *  - Backdrop click ile kapanır
 *  - Tab navigasyonu klavye ile desteklenir
 *  - Akordiyon SSS'ler click ile açılır/kapanır
 */
/* ─── Sabitler ─────────────────────────────────────────────────────────── */
const MODAL_ID = 'ifc-guide-modal';
const BACKDROP_ID = 'ifc-guide-backdrop';
/* ─── İçerik verisi ────────────────────────────────────────────────────── */
const REVIT_STEPS = [
    {
        num: 1,
        title: 'Dosya → Dışa Aktar → IFC',
        desc: 'Revit menüsünden <strong>Dosya</strong> → <strong>Dışa Aktar</strong> → <strong>IFC</strong> yolunu izleyin. '
            + 'Alternatif olarak Uygulama Menüsü (sol üst "R" simgesi) üzerinden de ulaşabilirsiniz.',
        icon: '📂',
    },
    {
        num: 2,
        title: 'IFC Versiyonu Seçin',
        desc: 'Açılan pencerede <strong>IFC versiyonu</strong> açılır listesinden <strong>IFC4</strong> seçin. '
            + 'Eski sistemlerle uyumluluk için IFC2x3 de tercih edilebilir; ancak IFC4 daha fazla semantik bilgi içerir.',
        icon: '🏷️',
    },
    {
        num: 3,
        title: 'Dışa Aktarılacak Kapsamı Belirleyin',
        desc: '"<strong>Geçerli görünüm</strong>" seçeneği yalnızca aktif görünümde görünen elemanları export eder. '
            + '"<strong>Tüm model</strong>" seçeneği tüm elemanları dahil eder. '
            + 'Büyük projelerde kat bazlı görünümler oluşturup her katı ayrı export etmek dosya boyutunu küçültür.',
        icon: '🗂️',
    },
    {
        num: 4,
        title: 'Export Ayarları — Miktarları Dahil Et',
        desc: '"<strong>IFC Dışa Aktarma Kurulumu</strong>" bölümünde <strong>"Temel miktarları dahil et"</strong> '
            + 'seçeneğini işaretleyin. Bu sayede hacim, alan ve uzunluk bilgileri IFC dosyasına yazılır; '
            + 'BuildingAI bu değerleri otomatik olarak okur.',
        icon: '⚙️',
    },
    {
        num: 5,
        title: 'Kaydedin ve BuildingAI\'a Yükleyin',
        desc: 'Dosyayı kaydedin ve <strong>BuildingAI</strong> arayüzünde "IFC Aç" butonunu kullanarak yükleyin. '
            + 'Büyük modelleri (100 MB+) sıkıştırılmış IFC (IFCZIP) olarak kaydedebilirsiniz.',
        icon: '☁️',
    },
];
const AUTOCAD_OPTIONS = [
    {
        label: 'AutoCAD Architecture Kullanıcıları İçin',
        icon: '🏢',
        badge: 'Önerilen',
        steps: [
            'Dosya → Dışa Aktar → IFC yolunu izleyin.',
            'IFC versiyonunu seçin: IFC4 veya IFC2x3.',
            'Katmanları ve eleman tiplerini kontrol edin.',
            'Dışa aktarın ve BuildingAI\'a yükleyin.',
        ],
    },
    {
        label: 'Düz AutoCAD Kullanıcıları İçin — ODA File Converter',
        icon: '🔄',
        steps: [
            'DWG dosyanızı kaydedin.',
            'Ücretsiz <a href="https://www.opendesign.com/guestfiles/oda_file_converter" target="_blank" rel="noopener noreferrer" class="bv-guide-link">ODA File Converter</a>\'ı indirin (opendesign.com).',
            'Converter\'da kaynak format olarak <strong>DWG</strong>, hedef format olarak <strong>IFC</strong> seçin.',
            '"Convert" butonuna tıklayın ve çıkan IFC dosyasını BuildingAI\'a yükleyin.',
        ],
    },
    {
        label: 'BIM Collab ZOOM ile DWG → IFC',
        icon: '🔍',
        steps: [
            '<a href="https://www.bimcollab.com/bimcollab-zoom/" target="_blank" rel="noopener noreferrer" class="bv-guide-link">BIM Collab ZOOM</a> uygulamasını (ücretsiz) indirin.',
            'DWG dosyanızı ZOOM\'da açın.',
            '"Dışa Aktar → IFC" menüsünü kullanın.',
            'Oluşan IFC dosyasını BuildingAI\'a yükleyin.',
        ],
    },
];
const FAQ_ITEMS = [
    {
        question: 'DWG dosyamı direkt yükleyebilir miyim?',
        answer: 'Hayır. BuildingAI yalnızca <strong>.ifc</strong> ve <strong>.ifczip</strong> formatlarını destekler. '
            + 'DWG dosyanızı önce IFC\'ye dönüştürmeniz gerekiyor. '
            + '"AutoCAD\'den IFC Export" sekmesindeki seçeneklerden birini kullanabilirsiniz.',
    },
    {
        question: 'IFC dosyam çok büyük (500 MB+), ne yapmalıyım?',
        answer: 'Büyük dosyalarda şu yöntemleri deneyebilirsiniz:<br>'
            + '① Revit\'te her kat için ayrı görünüm oluşturup <strong>kat bazlı export</strong> yapın.<br>'
            + '② Export sırasında <strong>IFCZIP</strong> formatını tercih edin (otomatik sıkıştırma uygular).<br>'
            + '③ MEP (mekanik/elektrik/tesisat) elemanlarını ayrı bir modele taşıyıp ayrı export edin.',
    },
    {
        question: 'Export\'ta bazı elemanlar kayıp, neden?',
        answer: 'En yaygın sebepler:<br>'
            + '① <strong>IFC class filtresi</strong>: Export ayarlarında bazı eleman tipleri devre dışı bırakılmış olabilir. '
            + 'Revit\'te "IFC Export Setup" → "Classes and Properties" bölümünü kontrol edin.<br>'
            + '② Elemanlar farklı bir <strong>Workset</strong>\'te ve o workset aktif değil.<br>'
            + '③ Elemanlar <strong>görünümde gizlenmiş</strong>. Geçerli görünüm yerine "Tüm model" seçeneğini deneyin.',
    },
    {
        question: '2D AutoCAD çizimim var, 3D model yok. Ne yapabilirim?',
        answer: '2D çizimlerden IFC export anlamlı bir sonuç vermez; IFC 3D model tabanlı bir formattır. '
            + 'Seçenekleriniz:<br>'
            + '① Projeyi <strong>Revit</strong> veya <strong>AutoCAD Architecture</strong>\'da 3D olarak yeniden modelleyin.<br>'
            + '② <strong>FreeCAD</strong> (ücretsiz) ile 2D çizimlerden 3D model oluşturun.<br>'
            + '③ 2D belgeleri referans olarak saklamak için PDF formatını kullanın, 3D görüntüleme için IFC gerekli.',
    },
];
/* ─── Yardımcı fonksiyonlar ────────────────────────────────────────────── */
/**
 * Şu anda açık olan IFC Rehberi modalını döndürür.
 * Modal yoksa null döner.
 */
function _getModal() {
    return document.getElementById(MODAL_ID);
}
/**
 * Modalı kapatır ve DOM'dan kaldırır.
 */
function _closeModal() {
    const backdrop = document.getElementById(BACKDROP_ID);
    const modal = _getModal();
    if (backdrop) {
        backdrop.classList.add('bv-guide-backdrop--out');
        setTimeout(() => backdrop.remove(), 260);
    }
    if (modal) {
        modal.classList.add('bv-guide-modal--out');
        setTimeout(() => modal.remove(), 260);
    }
}
/**
 * Aktif tab'ı değiştirir.
 *
 * @param tabId   - Gösterilecek tab'ın ID'si
 * @param tabsEl  - Tab butonlarının parent elementi
 * @param pagesEl - Tab içeriklerinin parent elementi
 */
function _switchTab(tabId, tabsEl, pagesEl) {
    // Butonları güncelle
    tabsEl.querySelectorAll('.bv-guide-tab-btn').forEach(btn => {
        const active = btn.dataset['tab'] === tabId;
        btn.classList.toggle('bv-guide-tab-btn--active', active);
        btn.setAttribute('aria-selected', String(active));
    });
    // Sayfaları güncelle
    pagesEl.querySelectorAll('.bv-guide-page').forEach(page => {
        const active = page.dataset['tabPage'] === tabId;
        page.classList.toggle('bv-guide-page--active', active);
        page.setAttribute('aria-hidden', String(!active));
    });
}
/* ─── İçerik oluşturucular ─────────────────────────────────────────────── */
/**
 * Tab 1: Revit'ten IFC Export sayfasını oluşturur.
 */
function _buildRevitPage() {
    const page = document.createElement('div');
    page.className = 'bv-guide-page bv-guide-page--active';
    page.dataset['tabPage'] = 'revit';
    page.setAttribute('role', 'tabpanel');
    page.setAttribute('aria-labelledby', 'tab-revit');
    page.setAttribute('aria-hidden', 'false');
    // Sayfa başlık
    const heading = document.createElement('div');
    heading.className = 'bv-guide-page-heading';
    heading.innerHTML = `
    <span class="bv-guide-page-icon">🏗️</span>
    <div>
      <h3 class="bv-guide-page-title">Revit'ten IFC Export</h3>
      <p class="bv-guide-page-subtitle">Aşağıdaki adımları sırasıyla izleyerek IFC dosyanızı oluşturun.</p>
    </div>
  `;
    page.appendChild(heading);
    // Adımlar
    const stepsList = document.createElement('ol');
    stepsList.className = 'bv-guide-steps';
    REVIT_STEPS.forEach(step => {
        const li = document.createElement('li');
        li.className = 'bv-guide-step';
        li.innerHTML = `
      <div class="bv-guide-step-num">${step.num}</div>
      <div class="bv-guide-step-body">
        <div class="bv-guide-step-header">
          <span class="bv-guide-step-icon">${step.icon}</span>
          <strong class="bv-guide-step-title">${step.title}</strong>
        </div>
        <p class="bv-guide-step-desc">${step.desc}</p>
      </div>
    `;
        stepsList.appendChild(li);
    });
    page.appendChild(stepsList);
    // Not kutusu
    const note = document.createElement('div');
    note.className = 'bv-guide-note bv-guide-note--info';
    note.innerHTML = `
    <span class="bv-guide-note-icon">💡</span>
    <span><strong>Not:</strong> Revit 2020 ve üzeri versiyonlarda IFC4 desteği tam olarak çalışır. 
    Daha eski sürümler için IFC2x3 formatını tercih edin.</span>
  `;
    page.appendChild(note);
    return page;
}
/**
 * Tab 2: AutoCAD'den IFC Export sayfasını oluşturur.
 */
function _buildAutoCADPage() {
    const page = document.createElement('div');
    page.className = 'bv-guide-page';
    page.dataset['tabPage'] = 'autocad';
    page.setAttribute('role', 'tabpanel');
    page.setAttribute('aria-labelledby', 'tab-autocad');
    page.setAttribute('aria-hidden', 'true');
    // Sayfa başlık
    const heading = document.createElement('div');
    heading.className = 'bv-guide-page-heading';
    heading.innerHTML = `
    <span class="bv-guide-page-icon">📐</span>
    <div>
      <h3 class="bv-guide-page-title">AutoCAD'den IFC Export</h3>
      <p class="bv-guide-page-subtitle">AutoCAD'de native IFC export bulunmaz. Aşağıdaki alternatiflerden birini seçin.</p>
    </div>
  `;
    page.appendChild(heading);
    // Seçenekler
    AUTOCAD_OPTIONS.forEach((opt, idx) => {
        const card = document.createElement('div');
        card.className = 'bv-guide-option-card';
        card.setAttribute('id', `autocad-option-${idx + 1}`);
        const cardHeader = document.createElement('div');
        cardHeader.className = 'bv-guide-option-header';
        cardHeader.innerHTML = `
      <span class="bv-guide-option-letter">${String.fromCharCode(65 + idx)}</span>
      <span class="bv-guide-option-icon">${opt.icon}</span>
      <span class="bv-guide-option-label">${opt.label}</span>
      ${opt.badge ? `<span class="bv-guide-badge bv-guide-badge--accent">${opt.badge}</span>` : ''}
    `;
        card.appendChild(cardHeader);
        const stepsList = document.createElement('ol');
        stepsList.className = 'bv-guide-option-steps';
        opt.steps.forEach(s => {
            const li = document.createElement('li');
            li.innerHTML = s;
            stepsList.appendChild(li);
        });
        card.appendChild(stepsList);
        page.appendChild(card);
    });
    // Uyarı kutusu
    const warning = document.createElement('div');
    warning.className = 'bv-guide-note bv-guide-note--warning';
    warning.innerHTML = `
    <span class="bv-guide-note-icon">⚠️</span>
    <span><strong>Önemli Uyarı:</strong> Düz AutoCAD'den yapılan IFC export'lar 
    <strong>semantik bilgi içermez</strong> — duvar, kolon, döşeme ayrımı olmaz; 
    tüm geometri tek tip olarak aktarılır. En iyi sonuç için projenizi 
    <strong>Revit</strong> veya <strong>AutoCAD Architecture</strong>'da modelleyin.</span>
  `;
    page.appendChild(warning);
    return page;
}
/**
 * Tab 3: IFC Nedir? sayfasını oluşturur.
 */
function _buildIfcInfoPage() {
    const page = document.createElement('div');
    page.className = 'bv-guide-page';
    page.dataset['tabPage'] = 'ifcinfo';
    page.setAttribute('role', 'tabpanel');
    page.setAttribute('aria-labelledby', 'tab-ifcinfo');
    page.setAttribute('aria-hidden', 'true');
    page.innerHTML = `
    <div class="bv-guide-page-heading">
      <span class="bv-guide-page-icon">📖</span>
      <div>
        <h3 class="bv-guide-page-title">IFC Nedir?</h3>
        <p class="bv-guide-page-subtitle">Industry Foundation Classes — açık ve evrensel BIM formatı.</p>
      </div>
    </div>

    <div class="bv-guide-info-section">
      <h4 class="bv-guide-info-title">Genel Tanım</h4>
      <p class="bv-guide-info-text">
        <strong>IFC (Industry Foundation Classes)</strong>, inşaat ve yapı sektöründe 
        bina ve altyapı projelerini dijital ortamda tanımlamak için kullanılan 
        <strong>açık ve vendor-bağımsız</strong> bir veri formatıdır. 
        buildingSMART International tarafından geliştirilen IFC, ISO standardı 
        (ISO 16739) olarak kabul görmüştür.
      </p>
      <p class="bv-guide-info-text">
        IFC yalnızca geometri değil; <strong>elemanlara ait semantik bilgileri</strong> de saklar. 
        Bir duvarın kalınlığı, malzemesi, yangın dayanımı, enerji özellikleri 
        ve diğer tüm nitelikler IFC dosyasının içinde yer alır. 
        Bu sayede farklı disiplinler (mimari, yapısal, MEP) arasında bilgi kaybı 
        olmadan veri aktarımı yapılabilir.
      </p>
      <p class="bv-guide-info-text">
        BuildingAI, IFC formatını birincil giriş formatı olarak kullanır çünkü 
        <strong>açık format</strong> olması sayesinde herhangi bir lisans gerektirmez, 
        <strong>geleceğe dönük</strong> veri saklama imkânı sunar ve 
        platformlar arası <strong>tam interoperabilite</strong> sağlar.
      </p>
    </div>

    <div class="bv-guide-info-section">
      <h4 class="bv-guide-info-title">Neden IFC Kullanıyoruz?</h4>
      <div class="bv-guide-reason-grid">
        <div class="bv-guide-reason-card">
          <div class="bv-guide-reason-icon">🔓</div>
          <div class="bv-guide-reason-title">Açık Format</div>
          <div class="bv-guide-reason-desc">Herhangi bir yazılım firmasına bağımlı değil; ücretsiz ve herkese açık bir standarttır.</div>
        </div>
        <div class="bv-guide-reason-card">
          <div class="bv-guide-reason-icon">🌐</div>
          <div class="bv-guide-reason-title">Evrensel Standart</div>
          <div class="bv-guide-reason-desc">buildingSMART tarafından yönetilen, ISO 16739 olarak tescillenmiş global standart.</div>
        </div>
        <div class="bv-guide-reason-card">
          <div class="bv-guide-reason-icon">🔗</div>
          <div class="bv-guide-reason-title">Semantik Zenginlik</div>
          <div class="bv-guide-reason-desc">Geometrinin ötesinde malzeme, tip, özellik setleri ve ilişki bilgileri içerir.</div>
        </div>
        <div class="bv-guide-reason-card">
          <div class="bv-guide-reason-icon">🚀</div>
          <div class="bv-guide-reason-title">Sürekli Gelişim</div>
          <div class="bv-guide-reason-desc">IFC4.3, yol, köprü ve altyapı projelerini de kapsayan en güncel sürümdür.</div>
        </div>
      </div>
    </div>

    <div class="bv-guide-info-section">
      <h4 class="bv-guide-info-title">IFC Destekleyen Programlar</h4>
      <div class="bv-guide-software-list">
        <div class="bv-guide-software-item">
          <span class="bv-guide-sw-dot bv-guide-sw-dot--green"></span>
          <span class="bv-guide-sw-name">Autodesk Revit</span>
          <span class="bv-guide-sw-note">Tam IFC4 desteği (v2020+)</span>
        </div>
        <div class="bv-guide-software-item">
          <span class="bv-guide-sw-dot bv-guide-sw-dot--green"></span>
          <span class="bv-guide-sw-name">Graphisoft ArchiCAD</span>
          <span class="bv-guide-sw-note">Tam IFC4 desteği</span>
        </div>
        <div class="bv-guide-software-item">
          <span class="bv-guide-sw-dot bv-guide-sw-dot--green"></span>
          <span class="bv-guide-sw-name">Trimble Tekla Structures</span>
          <span class="bv-guide-sw-note">Yapısal IFC desteği</span>
        </div>
        <div class="bv-guide-software-item">
          <span class="bv-guide-sw-dot bv-guide-sw-dot--green"></span>
          <span class="bv-guide-sw-name">Nemetschek Allplan</span>
          <span class="bv-guide-sw-note">Tam IFC4 desteği</span>
        </div>
        <div class="bv-guide-software-item">
          <span class="bv-guide-sw-dot bv-guide-sw-dot--yellow"></span>
          <span class="bv-guide-sw-name">AutoCAD Architecture</span>
          <span class="bv-guide-sw-note">Kısmi IFC desteği</span>
        </div>
        <div class="bv-guide-software-item">
          <span class="bv-guide-sw-dot bv-guide-sw-dot--green"></span>
          <span class="bv-guide-sw-name">FreeCAD (BIM Workbench)</span>
          <span class="bv-guide-sw-note">Tam IFC4 desteği — ücretsiz</span>
        </div>
      </div>
    </div>
  `;
    return page;
}
/**
 * Tab 4: Sık Sorulan Sorular sayfasını oluşturur.
 * Akordiyon düzende SSS öğeleri render eder.
 */
function _buildFaqPage() {
    const page = document.createElement('div');
    page.className = 'bv-guide-page';
    page.dataset['tabPage'] = 'faq';
    page.setAttribute('role', 'tabpanel');
    page.setAttribute('aria-labelledby', 'tab-faq');
    page.setAttribute('aria-hidden', 'true');
    const heading = document.createElement('div');
    heading.className = 'bv-guide-page-heading';
    heading.innerHTML = `
    <span class="bv-guide-page-icon">❓</span>
    <div>
      <h3 class="bv-guide-page-title">Sık Sorulan Sorular</h3>
      <p class="bv-guide-page-subtitle">IFC export sürecinde en çok karşılaşılan sorular ve çözümleri.</p>
    </div>
  `;
    page.appendChild(heading);
    const faqList = document.createElement('div');
    faqList.className = 'bv-guide-faq-list';
    FAQ_ITEMS.forEach((item, idx) => {
        const entry = document.createElement('div');
        entry.className = 'bv-guide-faq-item';
        const btnId = `faq-btn-${idx}`;
        const bodyId = `faq-body-${idx}`;
        const btn = document.createElement('button');
        btn.className = 'bv-guide-faq-q';
        btn.id = btnId;
        btn.setAttribute('aria-expanded', 'false');
        btn.setAttribute('aria-controls', bodyId);
        btn.type = 'button';
        btn.innerHTML = `
      <span class="bv-guide-faq-q-text">${item.question}</span>
      <span class="bv-guide-faq-chevron" aria-hidden="true">›</span>
    `;
        const body = document.createElement('div');
        body.className = 'bv-guide-faq-a';
        body.id = bodyId;
        body.setAttribute('role', 'region');
        body.setAttribute('aria-labelledby', btnId);
        body.setAttribute('hidden', 'true');
        body.innerHTML = `<p>${item.answer}</p>`;
        // Toggle mantığı
        btn.addEventListener('click', () => {
            const expanded = btn.getAttribute('aria-expanded') === 'true';
            btn.setAttribute('aria-expanded', String(!expanded));
            btn.classList.toggle('bv-guide-faq-q--open', !expanded);
            if (expanded) {
                body.setAttribute('hidden', 'true');
            }
            else {
                body.removeAttribute('hidden');
            }
        });
        entry.appendChild(btn);
        entry.appendChild(body);
        faqList.appendChild(entry);
    });
    page.appendChild(faqList);
    // Destek notu
    const note = document.createElement('div');
    note.className = 'bv-guide-note bv-guide-note--info';
    note.innerHTML = `
    <span class="bv-guide-note-icon">📩</span>
    <span>Sorunuz bu listede yok mu? 
    <a href="mailto:destek@buildingai.com" class="bv-guide-link">destek@buildingai.com</a> 
    adresinden bize ulaşabilirsiniz.</span>
  `;
    page.appendChild(note);
    return page;
}
/* ─── Modal oluşturma ──────────────────────────────────────────────────── */
/**
 * IFC Export Rehberi modalını oluşturur ve DOM'a ekler.
 * Modal zaten açıksa tekrar oluşturulmaz.
 */
function _buildModal() {
    // Zaten açıksa çık
    if (_getModal())
        return;
    /* ── Backdrop ─────────────────────────────────────────────────────── */
    const backdrop = document.createElement('div');
    backdrop.id = BACKDROP_ID;
    backdrop.className = 'bv-guide-backdrop';
    backdrop.setAttribute('aria-hidden', 'true');
    backdrop.addEventListener('click', _closeModal);
    /* ── Modal kapsayıcı ─────────────────────────────────────────────── */
    const modal = document.createElement('div');
    modal.id = MODAL_ID;
    modal.className = 'bv-guide-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'IFC Export Rehberi');
    // Tıklamanın backdrop'a geçmesini engelle
    modal.addEventListener('click', e => e.stopPropagation());
    /* ── Modal başlık çubuğu ─────────────────────────────────────────── */
    const header = document.createElement('div');
    header.className = 'bv-guide-header';
    header.innerHTML = `
    <div class="bv-guide-header-title">
      <span class="bv-guide-header-icon">📋</span>
      <span>IFC Export Rehberi</span>
      <span class="bv-guide-header-badge">BuildingAI</span>
    </div>
    <button 
      class="bv-guide-close-btn" 
      id="bv-guide-close-btn"
      type="button"
      title="Kapat (ESC)"
      aria-label="Rehberi kapat"
    >✕</button>
  `;
    modal.appendChild(header);
    /* ── Tab çubuğu ──────────────────────────────────────────────────── */
    const tabBar = document.createElement('div');
    tabBar.className = 'bv-guide-tabs';
    tabBar.setAttribute('role', 'tablist');
    tabBar.setAttribute('aria-label', 'Rehber bölümleri');
    const tabs = [
        { id: 'revit', label: 'Revit\'ten Export', icon: '🏗️' },
        { id: 'autocad', label: 'AutoCAD\'den Export', icon: '📐' },
        { id: 'ifcinfo', label: 'IFC Nedir?', icon: '📖' },
        { id: 'faq', label: 'Sık Sorulan Sorular', icon: '❓' },
    ];
    tabs.forEach((tab, idx) => {
        const btn = document.createElement('button');
        btn.className = 'bv-guide-tab-btn' + (idx === 0 ? ' bv-guide-tab-btn--active' : '');
        btn.type = 'button';
        btn.id = `tab-${tab.id}`;
        btn.dataset['tab'] = tab.id;
        btn.setAttribute('role', 'tab');
        btn.setAttribute('aria-selected', String(idx === 0));
        btn.setAttribute('aria-controls', `tabpanel-${tab.id}`);
        btn.innerHTML = `<span class="bv-guide-tab-icon">${tab.icon}</span><span class="bv-guide-tab-label">${tab.label}</span>`;
        tabBar.appendChild(btn);
    });
    modal.appendChild(tabBar);
    /* ── İçerik alanı ────────────────────────────────────────────────── */
    const content = document.createElement('div');
    content.className = 'bv-guide-content';
    content.appendChild(_buildRevitPage());
    content.appendChild(_buildAutoCADPage());
    content.appendChild(_buildIfcInfoPage());
    content.appendChild(_buildFaqPage());
    modal.appendChild(content);
    /* ── DOM'a ekle ──────────────────────────────────────────────────── */
    document.body.appendChild(backdrop);
    document.body.appendChild(modal);
    /* ── Event listener'ları bağla ────────────────────────────────────── */
    // Kapat butonu
    const closeBtn = modal.querySelector('#bv-guide-close-btn');
    closeBtn?.addEventListener('click', _closeModal);
    // Tab switching
    tabBar.addEventListener('click', e => {
        const btn = e.target.closest('.bv-guide-tab-btn');
        if (!btn)
            return;
        const tabId = btn.dataset['tab'];
        if (tabId)
            _switchTab(tabId, tabBar, content);
    });
    // Animasyon için küçük gecikme (DOM'a eklendikten sonra class ekle)
    requestAnimationFrame(() => {
        backdrop.classList.add('bv-guide-backdrop--in');
        modal.classList.add('bv-guide-modal--in');
    });
    // Focus yönetimi — erişilebilirlik
    closeBtn?.focus();
    console.log('[ifcExportGuide] Modal açıldı.');
}
/* ─── Klavye erişilebilirliği ──────────────────────────────────────────── */
/**
 * Belge seviyesinde ESC tuşu dinleyicisi.
 * Sadece modal açıkken çalışır.
 */
function _onKeyDown(e) {
    if (e.key === 'Escape' && _getModal()) {
        _closeModal();
    }
}
/* ─── Public API ───────────────────────────────────────────────────────── */
/**
 * IFC Export Rehberi butonunu ve modal sistemini başlatır.
 *
 * Toolbar içindeki bir container'a "IFC Nedir?" butonu ekler.
 * Butona tıklanınca modal açılır.
 *
 * @param toolbarEl - Butonun ekleneceği toolbar elementi
 */
export function initIfcExportGuide(toolbarEl) {
    console.log('[ifcExportGuide] Başlatılıyor...');
    // Rehber butonu oluştur
    const btn = document.createElement('button');
    btn.id = 'btn-ifc-guide';
    btn.className = 'bv-btn bv-btn--ghost bv-btn--icon';
    btn.type = 'button';
    btn.title = 'IFC Export Rehberi';
    btn.setAttribute('aria-label', 'IFC Export Rehberini aç');
    btn.setAttribute('aria-haspopup', 'dialog');
    btn.innerHTML = `<span aria-hidden="true">❓</span>`;
    // Tıklama: modalı aç
    btn.addEventListener('click', () => {
        _buildModal();
    });
    // Toolbar'a ekle
    toolbarEl.appendChild(btn);
    // Belge düzeyinde ESC listener (tek sefer)
    document.addEventListener('keydown', _onKeyDown);
    console.log('[ifcExportGuide] Hazır. Buton toolbar\'a eklendi.');
}
/**
 * IFC Export Rehberi modalını programatik olarak açar.
 * Toolbar dışından da çağrılabilir.
 */
export function openIfcGuide() {
    _buildModal();
}
/**
 * IFC Export Rehberi modalını programatik olarak kapatır.
 */
export function closeIfcGuide() {
    _closeModal();
}
//# sourceMappingURL=ifcExportGuide.js.map