// Saha → kontrol → hakediş: the existing /app remains the product shell.
(() => {
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const selectedSite = () => localStorage.getItem('bai_aktif_santiye') || '';
  const token = () => localStorage.getItem('bai_token') || '';
  let state = {areas:[], contracts:[], lines:[], works:[], measurements:[], payments:[], capabilities:{}};
  let loading = false;
  async function api(path, method='GET', data) {
    const response = await fetch(path, {method, headers:{Authorization:`Bearer ${token()}`, ...(data ? {'Content-Type':'application/json'} : {})}, body:data ? JSON.stringify(data) : undefined});
    const json = await response.json();
    if (!response.ok) throw new Error(json.detail || 'İşlem başarısız. Tekrar deneyin.');
    return json;
  }
  function options(rows, label) {
    return `<option value="">${esc(label)}</option>` + rows.map(row => `<option value="${Number(row.id)}">${esc(row.label)}</option>`).join('');
  }
  function currentContract() { return Number($('w2Contract')?.value || 0); }
  function currentPayment() { return Number($('w2Payment')?.value || 0); }
  function message(text, error=false) {
    const el = $('w2Message');
    if (el) { el.textContent=text; el.style.color=error ? '#b91c1c' : '#166534'; }
  }
  async function loadTasks() {
    const site=selectedSite(), epoch=window._baiProjectEpoch || 0;
    const host=$('w2Tasks');
    if(!host)return;
    if(!site){host.innerHTML='<h2>Yapılacak işler</h2><p>Proje seçin; bekleyen işler burada görünür.</p>';return;}
    try {
      const [measurements,payments,contracts,capabilities]=await Promise.all([
        api(`/api/v2/santiye/${site}/measurements`),api(`/api/hakedis/liste/${site}`),
        api(`/api/v2/santiye/${site}/contracts`),api(`/api/v2/santiye/${site}/capabilities`)
      ]);
      if(site!==selectedSite()||epoch!==(window._baiProjectEpoch||0))return;
      const rows=measurements.measurements||[];
      const pending=rows.filter(x=>x.status==='pending'&&capabilities.can_review&&x.created_by!==capabilities.user_id).length;
      const missing=rows.filter(x=>x.status==='draft'&&(!x.basis||!x.contract_line_id||!x.work_date||x.reported_quantity==null)).length;
      const paymentCount=(payments.hakedisler||[]).filter(x=>x.durum==='onay_bekliyor').length;
      const setup=(contracts.contracts||[]).length===0;
      const tasks=[];
      if(pending)tasks.push(`${pending} ölçüm kontrol bekliyor`);
      if(missing)tasks.push(`${missing} ölçüm taslağında bilgi eksik`);
      if(paymentCount)tasks.push(`${paymentCount} hakediş onay bekliyor`);
      if(setup)tasks.push('Birim fiyatlı sözleşme kurulumu eksik');
      const title=document.querySelector('#globalSantiyeSecici option:checked')?.textContent.trim()||`Proje #${site}`;
      host.innerHTML=`<div class="w2-tasks-head"><div><h2>Yapılacak işler</h2><p>${esc(title)} · Kayıtlı iş akışı</p></div><button type="button" id="w2TasksOpen">Saha zincirini aç</button></div>`+
        (tasks.length?`<ul>${tasks.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:'<p>Bu projede bekleyen kayıt görünmüyor.</p>');
      $('w2TasksOpen').onclick=()=>{window.navGit?.('hakedis');setTimeout(()=>$('w2Panel')?.removeAttribute('hidden'),0);load();};
    } catch(error){host.innerHTML=`<h2>Yapılacak işler</h2><p>${esc(error.message)} Sayfayı yeniden açıp tekrar deneyin.</p>`;}
  }
  async function load() {
    const site = selectedSite();
    const epoch = window._baiProjectEpoch || 0;
    if (!site) { message('Önce üst çubuktan proje seçin.', true); return; }
    const formerContract = $('w2Contract')?.value;
    const formerPayment = $('w2Payment')?.value;
    try {
      const [areas, contracts, works, measurements, payments, capabilities] = await Promise.all([
        api(`/api/v2/santiye/${site}/areas`), api(`/api/v2/santiye/${site}/contracts`),
        api(`/api/v2/santiye/${site}/is-kalemleri`), api(`/api/v2/santiye/${site}/measurements`),
        api(`/api/hakedis/liste/${site}`), api(`/api/v2/santiye/${site}/capabilities`)
      ]);
      if (site !== selectedSite() || epoch !== (window._baiProjectEpoch || 0)) return;
      state = {areas:areas.areas || [], contracts:contracts.contracts || [], works:works.kalemler || [], measurements:measurements.measurements || [], payments:payments.hakedisler || [], lines:[], capabilities};
      $('w2Site').textContent = document.querySelector('#globalSantiyeSecici option:checked')?.textContent.trim() || `Proje #${site}`;
      $('w2Area').innerHTML = options(state.areas.map(x=>({...x,label:x.name})), 'Alan seçin');
      $('w2Parent').innerHTML = options(state.areas.map(x=>({...x,label:x.name})), 'Üst alan yok');
      $('w2Contract').innerHTML = options(state.contracts.map(x=>({...x,label:`${x.name} · ${x.direction === 'employer' ? 'İşveren' : 'Taşeron'}`})), 'Sözleşme seçin');
      $('w2Work').innerHTML = options(state.works.map(x=>({...x,label:`${x.poz_no || ''} ${x.tanim || x.ad || 'İş kalemi'}`})), 'İş kalemi seçin');
      $('w2Payment').innerHTML = options(state.payments.filter(x=>x.durum === 'taslak').map(x=>({...x,label:`Hakediş #${x.hakedis_no}`})), 'Taslak hakediş seçin');
      if (formerContract && state.contracts.some(x=>String(x.id)===formerContract)) $('w2Contract').value=formerContract;
      if (formerPayment && state.payments.some(x=>String(x.id)===formerPayment)) $('w2Payment').value=formerPayment;
      await loadLines();
      renderMeasurements();
      message('');
    } catch (error) { message(error.message, true); }
  }
  async function loadLines() {
    const site=selectedSite();
    const contractId=currentContract();
    state.lines = contractId ? (await api(`/api/v2/contracts/${contractId}/lines`)).lines || [] : [];
    if (site !== selectedSite()) return;
    $('w2Line').innerHTML = options(state.lines.map(x=>({...x,label:`${x.code} · ${x.description} (${x.unit})`})), 'Sözleşme kalemi seçin');
  }
  function renderMeasurements() {
    const list=$('w2Measurements');
    const contractId=currentContract();
    const lineIds=new Set(state.lines.map(x=>x.id));
    const rows=state.measurements.filter(x=>!contractId || lineIds.has(x.contract_line_id));
    list.innerHTML = rows.length ? rows.map(m=>`<div class="w2-row">
      <strong>Ölçüm #${m.id}</strong> · ${esc(m.work_date || 'Tarih eksik')} · ${esc(m.reported_quantity ?? 'Miktar eksik')} ${esc(m.unit || '')}
      <span class="w2-pill">${esc({draft:'Taslak',pending:'Kontrol bekliyor',accepted:'Kontrol edildi',returned:'Geri gönderildi'}[m.status] || m.status)}</span>
      <div>${esc(m.basis || 'Dayanak eksik')} · Alan: ${esc(state.areas.find(a=>a.id===m.area_id)?.name || 'Proje geneli')}</div>
      ${m.status === 'accepted' ? `<small>Kabul: ${esc(m.accepted_quantity)} · Hakedişe kalan: ${esc(m.remaining_quantity)}</small>` : ''}
      ${m.review_reason ? `<small>Gerekçe: ${esc(m.review_reason)}</small>` : ''}
      ${m.status === 'draft' && m.created_by === state.capabilities.user_id ? `<button data-action="submit" data-id="${m.id}">Kontrole gönder</button>` : ''}
      ${m.status === 'pending' && state.capabilities.can_review && m.created_by !== state.capabilities.user_id ? `<input aria-label="Kabul edilen miktar" id="w2Accept${m.id}" type="number" min="0" step="0.001" value="${esc(m.reported_quantity || 0)}"><input aria-label="Kontrol gerekçesi" id="w2Reason${m.id}" placeholder="Kısmi kabul gerekçesi"><button data-action="review" data-id="${m.id}">Kontrolü kaydet</button>` : ''}
      ${m.status === 'accepted' && state.capabilities.can_write && Number(m.remaining_quantity)>0 ? `<button data-action="allocate" data-id="${m.id}">Seçili hakedişe ekle</button>` : ''}
      <button data-action="history" data-id="${m.id}">Karar geçmişi</button>
    </div>`).join('') : '<p>Bu sözleşmede ölçüm yok.</p>';
  }
  async function act(button, work) {
    if (loading) return;
    loading=true; button.disabled=true;
    try { await work(); await load(); await loadTasks(); }
    catch(error) { message(`${error.message} Girdileriniz korunuyor.`,true); }
    finally { loading=false; button.disabled=false; }
  }
  function form(id, handler) {
    $(id).addEventListener('submit', event=>{event.preventDefault(); act(event.submitter || $(id).querySelector('button'), ()=>handler(new FormData($(id))));});
  }
  function init() {
    const dashboard=$('contractorDashboard')?.querySelector('.engineer-dashboard__main');
    if(dashboard){const tasks=document.createElement('section');tasks.id='w2Tasks';tasks.className='w2-tasks';dashboard.insertBefore(tasks,dashboard.firstChild);}
    $('globalSantiyeSecici')?.addEventListener('change',loadTasks);
    document.addEventListener('click',event=>{if(event.target.closest('#nav-home'))setTimeout(loadTasks,0);});
    setTimeout(loadTasks,500);
    const page=$('hakedisPage');
    if (!page) return;
    const header=page.firstElementChild;
    const button=document.createElement('button');
    button.type='button'; button.textContent='Saha • sözleşme • kontrol'; button.className='w2-open';
    header.insertBefore(button, $('hakedisNewBtn'));
    const panel=document.createElement('div');
    panel.id='w2Panel'; panel.className='w2-panel'; panel.hidden=true;
    panel.innerHTML=`<div class="w2-card"><div class="w2-head"><div><h2>Saha, metraj ve hakediş</h2><p id="w2Site">Proje seçin</p></div><button id="w2Close" type="button">Kapat</button></div>
      <p id="w2Message" role="status"></p>
      <div class="w2-grid">
        <section><h3>1 · Çalışma alanı</h3><form id="w2AreaForm"><input name="name" placeholder="Rıhtım bölgesi, etap, çalışma noktası" required><select id="w2Parent" name="parent_id"></select><button>Alan ekle</button></form></section>
        <section><h3>2 · Birim fiyatlı sözleşme</h3><form id="w2ContractForm"><input name="name" placeholder="Sözleşme adı" required><input name="reference" placeholder="Referans"><select name="direction"><option value="employer">İşveren satış sözleşmesi</option><option value="subcontractor">Taşeron alış sözleşmesi</option></select><input name="counterparty" placeholder="Karşı taraf" required><input name="currency" value="TRY" maxlength="3" aria-label="Para birimi"><button>Sözleşme ekle</button></form>
          <label>Çalışılan sözleşme<select id="w2Contract"></select></label><form id="w2LineForm"><select id="w2Work" name="work_item_id"></select><input name="code" placeholder="Poz kodu" required><input name="description" placeholder="Açıklama (boşsa iş kalemi adı)"><input name="unit" placeholder="Birim (m³, m², adet)"><input name="quantity" type="number" step="0.001" min="0.001" placeholder="Sözleşme miktarı" required><input name="unit_price" type="number" step="0.01" min="0" placeholder="Birim fiyat" required><button>Kalemi bağla</button></form></section>
        <section><h3>3 · Ölçüm bildirimi</h3><form id="w2MeasureForm"><select id="w2Area" name="area_id"></select><select id="w2Line" name="contract_line_id"></select><input name="work_date" type="date"><input name="reported_quantity" type="number" step="0.001" min="0.001" placeholder="Bildirilen miktar"><textarea name="basis" placeholder="Ölçüm açıklaması ve dayanağı"></textarea><input name="evidence_ids" placeholder="Ekli belge kayıt numaraları (isteğe bağlı)"><button>Taslak kaydet</button></form><p>Eksik bilgilerle taslak kaydedilebilir. Kontrole gönderirken sözleşme kalemi, tarih, miktar ve dayanak gerekir. Alan boşsa proje geneli kullanılır; fotoğraf tek başına kesin metraj değildir.</p></section>
        <section><h3>4 · Hakediş</h3><form id="w2PaymentForm"><input name="start_date" type="date" required><input name="end_date" type="date" required><button>Sözleşme hakedişi aç</button></form><label>Açık hakediş<select id="w2Payment"></select></label><p>Kontrol edilmiş ölçümlerin kalan miktarını aşağıdan hakedişe ekleyin. Tutar sözleşme fiyatından hesaplanır.</p></section>
      </div><section><h3>Ölçümler ve kararlar</h3><div id="w2Measurements"></div></section>
    </div>`;
    document.body.appendChild(panel);
    button.onclick=()=>{panel.hidden=false;load();};
    $('w2Close').onclick=()=>{panel.hidden=true;};
    $('w2Contract').onchange=()=>{loadLines().then(renderMeasurements).catch(e=>message(e.message,true));};
    form('w2AreaForm', async data=>{await api(`/api/v2/santiye/${selectedSite()}/areas`,'POST',{name:data.get('name'),parent_id:Number(data.get('parent_id'))||null});});
    form('w2ContractForm', async data=>{await api(`/api/v2/santiye/${selectedSite()}/contracts`,'POST',Object.fromEntries(data));});
    form('w2LineForm', async data=>{if(!currentContract()) throw new Error('Önce sözleşme seçin.'); await api(`/api/v2/contracts/${currentContract()}/lines`,'POST',{...Object.fromEntries(data),work_item_id:Number(data.get('work_item_id'))});});
    let measurementKey=null;
    $('w2MeasureForm').addEventListener('input',()=>{measurementKey=null;});
    form('w2MeasureForm', async data=>{
      if(!measurementKey)measurementKey=crypto.randomUUID();
      const body={area_id:Number(data.get('area_id'))||null,contract_line_id:Number(data.get('contract_line_id'))||null,work_date:data.get('work_date')||null,reported_quantity:data.get('reported_quantity')||null,basis:data.get('basis')||'',evidence_ids:String(data.get('evidence_ids')||'').split(',').map(x=>Number(x.trim())).filter(Boolean),request_key:measurementKey};
      await api(`/api/v2/santiye/${selectedSite()}/measurements`,'POST',body);
      measurementKey=null;$('w2MeasureForm').reset();
    });
    form('w2PaymentForm', async data=>{if(!currentContract()) throw new Error('Önce sözleşme seçin.'); await api(`/api/v2/contracts/${currentContract()}/payments`,'POST',Object.fromEntries(data)); await window.hakedisListeYukle?.();});
    $('w2Measurements').addEventListener('click', event=>{
      const b=event.target.closest('button[data-action]'); if(!b) return;
      const id=Number(b.dataset.id);
      act(b, async()=>{
        if (b.dataset.action==='submit') await api(`/api/v2/measurements/${id}/submit`,'POST');
        if (b.dataset.action==='review') await api(`/api/v2/measurements/${id}/review`,'POST',{accepted_quantity:$(`w2Accept${id}`).value,reason:$(`w2Reason${id}`).value});
        if (b.dataset.action==='allocate') {if(!currentPayment()) throw new Error('Taslak hakediş seçin.'); const record=state.measurements.find(x=>x.id===id); await api(`/api/v2/payments/${currentPayment()}/allocations`,'POST',{measurement_id:id,quantity:record.remaining_quantity}); await window.hakedisListeYukle?.(); await window.hakedisDetayAc?.(currentPayment());}
        if (b.dataset.action==='history') {const data=await api(`/api/v2/measurements/${id}/decisions`); message(data.decisions.map(x=>`${x.previous_status} → ${x.new_status} · kullanıcı #${x.actor_id} · ${x.reason || ''}`).join(' | ') || 'Karar geçmişi yok.');}
      });
    });
  }
  document.addEventListener('DOMContentLoaded', init);
})();
