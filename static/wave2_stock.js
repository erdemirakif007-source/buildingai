(() => {
  const $ = id => document.getElementById(id);
  const esc = text => String(text ?? '').replace(/[&<>"']/g, x => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
  const site = () => localStorage.getItem('bai_aktif_santiye') || '';
  const headers = {'Content-Type':'application/json'};
  let pendingKey = null;
  async function api(path, method='GET', data) {
    const response=await fetch(path,{method,headers:{...headers,Authorization:'Bearer '+(localStorage.getItem('bai_token')||'')},body:data?JSON.stringify(data):undefined});
    const value=await response.json();
    if (!response.ok) throw new Error(value.detail || 'İşlem başarısız. Tekrar deneyin.');
    return value;
  }
  function status(text, error=false) {const target=$('w2StockMessage');if(target){target.textContent=text;target.style.color=error?'#b91c1c':'#166534';}}
  async function load() {
    const siteId=site(), epoch=window._baiProjectEpoch || 0;
    if(!siteId){status('Proje seçin.',true);return;}
    try {
      const [catalog,ledger,sites,works]=await Promise.all([
        api('/api/v2/materials'),api(`/api/v2/santiye/${siteId}/inventory`),api('/santiyeler'),api(`/api/v2/santiye/${siteId}/is-kalemleri`)
      ]);
      if(siteId!==site()||epoch!==(window._baiProjectEpoch||0))return;
      $('w2StockMaterial').innerHTML='<option value="">Malzeme seçin</option>'+catalog.materials.map(x=>`<option value="${esc(x.key)}" data-unit="${esc(x.unit)}">${esc(x.group || 'Diğer')} · ${esc(x.name)} · ${esc(x.unit)}</option>`).join('');
      $('w2StockTarget').innerHTML='<option value="">Hedef proje (transfer)</option>'+(sites.santiyeler||[]).filter(x=>String(x.id)!==siteId).map(x=>`<option value="${Number(x.id)}">${esc(x.ad)}</option>`).join('');
      $('w2StockWork').innerHTML='<option value="">Genel kullanım / bağlantı yok</option>'+(works.kalemler||[]).map(x=>`<option value="${Number(x.id)}">${esc(x.ad)}</option>`).join('');
      $('w2StockBalances').innerHTML=ledger.balances.length?ledger.balances.map(x=>`<div>${esc(x.material_key)} ${esc(x.variant)}: <strong>${esc(x.quantity)} ${esc(x.unit)}</strong></div>`).join(''):'Henüz izlenebilir stok hareketi yok.';
      $('w2StockHistory').innerHTML=ledger.movements.length?ledger.movements.slice().reverse().map(x=>`<div>${esc(x.created_at.slice(0,10))} · ${esc(x.kind)} · ${esc(x.quantity)} ${esc(x.unit)} ${esc(x.material_key)} ${esc(x.variant)}${x.price!=null?` · ${esc(x.price)} ${esc(x.price_currency)} / ${esc(x.unit)} (${esc(x.price_source)})`:''}</div>`).join(''):'Hareket geçmişi boş.';
      $('w2StockLegacy').textContent=ledger.legacy_unreconciled_count?`${ledger.legacy_unreconciled_count} eski stok kaydı yeni defterle henüz uzlaştırılmadı.`:'';
      status('');
    } catch(error){status(error.message,true);}
  }
  function init() {
    const stock=$('stokPage');if(!stock)return;
    const left=stock.firstElementChild;
    const box=document.createElement('section');box.id='w2StockBox';box.className='w2-stock';
    box.innerHTML=`<h2>İzlenebilir stok defteri</h2><p>Katalog ürünleri stok değildir. Bakiye yalnız aşağıdaki hareketlerden oluşur; farklı birimler otomatik çevrilmez.</p><div id="w2StockLegacy"></div><div id="w2StockBalances"></div>
      <form id="w2StockForm"><select id="w2StockMaterial" name="material_key" required></select><input name="variant" placeholder="Teknik varyant / ölçü"><input name="unit" placeholder="Birim" required><select name="kind"><option value="receipt">Giriş</option><option value="issue">Çıkış / tüketim</option><option value="transfer">Transfer</option><option value="return">İade girişi</option><option value="correction_in">Düzeltme artışı</option><option value="correction_out">Düzeltme azalışı</option></select><input name="quantity" type="number" min="0.001" step="0.001" placeholder="Miktar" required><select id="w2StockTarget" name="destination_site_id"></select><select id="w2StockWork" name="work_item_id"></select><input name="price" type="number" min="0" step="0.01" placeholder="Birim fiyat (biliniyorsa)"><input name="price_currency" placeholder="Fiyat para birimi (TRY)"><input name="price_source" placeholder="Fiyat kaynağı"><input name="price_scope" placeholder="KDV / nakliye kapsamı (biliniyorsa)"><input name="note" placeholder="Dayanak / not"><button>Hareket kaydet</button></form>
      <form id="w2CustomMaterial"><input name="name" placeholder="Özel malzeme adı" required><input name="unit" placeholder="Birim" required><button>Özel malzeme ekle</button></form><div id="w2StockMessage" role="status"></div><h3>Hareket geçmişi</h3><div id="w2StockHistory"></div>`;
    left.insertBefore(box,left.firstChild);
    // The previous stock widgets use a separate, unreconciled data model.
    // Keep their nodes for older handlers, but present only the traceable ledger.
    for (const child of left.children) if (child !== box) child.style.display='none';
    for (const child of stock.children) if (child !== left) child.style.display='none';
    $('w2StockMaterial').onchange=()=>{const selected=$('w2StockMaterial').selectedOptions[0];if(selected?.dataset.unit)$('w2StockForm').elements.unit.value=selected.dataset.unit;};
    $('w2StockForm').onsubmit=async event=>{
      event.preventDefault();const button=event.submitter;button.disabled=true;
      if(!pendingKey)pendingKey=crypto.randomUUID();
      const data=Object.fromEntries(new FormData(event.target));
      const body={...data,request_key:pendingKey,destination_site_id:Number(data.destination_site_id)||null,work_item_id:Number(data.work_item_id)||null,price:data.price===''?null:data.price};
      try{await api(`/api/v2/santiye/${site()}/inventory/movements`,'POST',body);pendingKey=null;event.target.reset();await load();status('Hareket kaydedildi.');}
      catch(error){status(`${error.message} Form korundu; aynı işlem yeniden denenebilir.`,true);}
      finally{button.disabled=false;}
    };
    $('w2CustomMaterial').onsubmit=async event=>{
      event.preventDefault();const button=event.submitter;button.disabled=true;
      try{await api('/api/v2/materials','POST',Object.fromEntries(new FormData(event.target)));event.target.reset();await load();status('Özel malzeme kataloğa eklendi.');}
      catch(error){status(error.message,true);}finally{button.disabled=false;}
    };
    document.addEventListener('click',event=>{if(event.target.closest('#nav-stok'))setTimeout(load,0);});
    new MutationObserver(()=>{if(stock.style.display!=='none')load();}).observe(stock,{attributes:true,attributeFilter:['style']});
    if(stock.style.display!=='none')load();
    $('globalSantiyeSecici')?.addEventListener('change',()=>{if(stock.style.display!=='none')load();});
  }
  document.addEventListener('DOMContentLoaded',init);
})();
