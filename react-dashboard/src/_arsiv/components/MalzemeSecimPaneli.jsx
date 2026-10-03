import { useState, useEffect, useCallback, useRef } from "react";
import {
  Plus, X, Search, Loader2, ChevronDown, ChevronUp,
  Package, AlertCircle, Check, Lock
} from "lucide-react";

// ── Turkish normalization ─────────────────────────────────────────────────────
const trNorm = (s = "") =>
  s.toLowerCase()
    .replace(/ğ/g, "g").replace(/ü/g, "u").replace(/ş/g, "s")
    .replace(/ı/g, "i").replace(/ö/g, "o").replace(/ç/g, "c")
    .replace(/Ğ/g, "g").replace(/Ü/g, "u").replace(/Ş/g, "s")
    .replace(/İ/g, "i").replace(/Ö/g, "o").replace(/Ç/g, "c");

// ── useDebounce ───────────────────────────────────────────────────────────────
function useDebounce(value, delay = 300) {
  const [deb, setDeb] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDeb(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return deb;
}

// ── EkMalzemeModal ────────────────────────────────────────────────────────────
function EkMalzemeModal({ token, isKalemiId, isKalemiMetraj, onEkle, onClose }) {
  const [arama, setArama] = useState("");
  const [sonuclar, setSonuclar] = useState([]);
  const [yukleniyor, setYukleniyor] = useState(false);
  const [hata, setHata] = useState("");
  const debArama = useDebounce(arama, 300);
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    if (debArama.trim().length < 2) {
      setSonuclar([]);
      return;
    }
    setYukleniyor(true);
    setHata("");
    const aramaUrl = `/api/katalog/ara?q=${encodeURIComponent(debArama)}&tip=malzeme`
      + (isKalemiId ? `&is_kalemi_id=${isKalemiId}` : "");
    fetch(
      aramaUrl,
      { headers: { Authorization: `Bearer ${token}` } }
    )
      .then((r) => {
        if (!r.ok) throw new Error("Arama başarısız");
        return r.json();
      })
      .then((data) => {
        setSonuclar(data.malzemeler || []);
      })
      .catch((e) => setHata(e.message))
      .finally(() => setYukleniyor(false));
  }, [debArama, token, isKalemiId]);

  return (
    <div className="fixed inset-0 z-60 flex items-center justify-center p-4 bg-black/70">
      <div className="bg-gray-900 border border-gray-700 rounded-xl w-full max-w-lg shadow-2xl flex flex-col max-h-[70vh]">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <h3 className="text-white font-semibold flex items-center gap-2">
            <Package size={18} className="text-blue-400" />
            Malzeme Kataloğundan Ekle
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Search */}
        <div className="p-4 border-b border-gray-700">
          <div className="relative">
            <Search
              size={16}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            />
            <input
              ref={inputRef}
              value={arama}
              onChange={(e) => setArama(e.target.value)}
              placeholder="Malzeme ara... (min. 2 karakter)"
              className="w-full bg-gray-800 border border-gray-600 rounded-lg py-2 pl-9 pr-4 text-white placeholder-gray-500 text-sm focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>

        {/* Results */}
        <div className="flex-1 overflow-y-auto">
          {yukleniyor && (
            <div className="flex justify-center items-center py-8">
              <Loader2 size={20} className="animate-spin text-blue-400" />
            </div>
          )}
          {hata && (
            <div className="flex items-center gap-2 p-4 text-red-400 text-sm">
              <AlertCircle size={16} />
              {hata}
            </div>
          )}
          {!yukleniyor && !hata && debArama.length >= 2 && sonuclar.length === 0 && (
            <div className="text-center py-8 text-gray-500 text-sm">
              Sonuç bulunamadı
            </div>
          )}
          {!yukleniyor && debArama.length < 2 && (
            <div className="text-center py-8 text-gray-500 text-sm">
              Aramak için en az 2 karakter girin
            </div>
          )}
          {sonuclar.map((m) => (
            <button
              key={m.id}
              onClick={() => onEkle(m)}
              className="w-full text-left px-4 py-3 hover:bg-gray-800 border-b border-gray-800 transition-colors group"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <p className="text-white text-sm font-medium truncate group-hover:text-blue-300">
                    {m.ad}
                  </p>
                  <p className="text-gray-500 text-xs mt-0.5">
                    {m.poz_no} • {m.kategori}
                    {m.alt_kategori ? ` › ${m.alt_kategori}` : ""}
                  </p>
                </div>
                <span className="ml-3 text-xs text-gray-400 bg-gray-700 px-2 py-0.5 rounded shrink-0">
                  {m.birim}
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── MalzemeSatir ──────────────────────────────────────────────────────────────
function MalzemeSatir({ malzeme, onChange, onKaldir }) {
  const { zorunlu, poz_no, ad, birim, miktar, guncel_fiyat } = malzeme;
  const tutar =
    miktar != null && guncel_fiyat != null
      ? (parseFloat(miktar) * parseFloat(guncel_fiyat)).toFixed(2)
      : null;

  return (
    <tr className="border-b border-gray-700/50 bg-gray-900/60 hover:bg-gray-800/50 transition-colors">
      {/* Checkbox / Lock */}
      <td className="px-3 py-2.5 text-center">
        {zorunlu ? (
          <span title="Zorunlu malzeme — kaldırılamaz">
            <Lock size={14} className="text-orange-400 mx-auto" />
          </span>
        ) : (
          <input
            type="checkbox"
            checked={malzeme.secili !== false}
            onChange={(e) => onChange({ secili: e.target.checked })}
            className="w-4 h-4 cursor-pointer accent-blue-400"
            style={{ accentColor: '#60a5fa' }}
          />
        )}
      </td>

      {/* Poz No */}
      <td className="px-3 py-2.5">
        <span className="text-xs font-mono bg-orange-500/20 text-orange-300 px-1.5 py-0.5 rounded">
          {poz_no || "—"}
        </span>
      </td>

      {/* Ad */}
      <td className="px-3 py-2.5">
        <span className="text-sm text-white font-medium">{ad}</span>
        {zorunlu && (
          <span className="ml-1.5 text-xs bg-orange-500/25 text-orange-300 px-1.5 py-0.5 rounded inline-block">
            zorunlu
          </span>
        )}
      </td>

      {/* Birim */}
      <td className="px-3 py-2.5 text-center">
        <span className="text-xs text-gray-300">{birim}</span>
      </td>

      {/* Miktar */}
      <td className="px-3 py-2.5">
        <input
          type="number"
          min="0"
          step="0.01"
          value={miktar ?? ""}
          onChange={(e) => onChange({ miktar: parseFloat(e.target.value) || 0 })}
          className="w-20 bg-gray-700 border border-gray-600 rounded px-2 py-1 text-white text-sm text-right focus:outline-none focus:border-blue-500"
        />
      </td>

      {/* Güncel Fiyat */}
      <td className="px-3 py-2.5 text-right">
        {guncel_fiyat != null ? (
          <span className="text-sm text-green-400">
            {parseFloat(guncel_fiyat).toLocaleString("tr-TR", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}{" "}
            ₺
          </span>
        ) : (
          <span className="text-xs text-gray-500">—</span>
        )}
      </td>

      {/* Tutar */}
      <td className="px-3 py-2.5 text-right">
        {tutar != null ? (
          <span className="text-sm text-white font-medium">
            {parseFloat(tutar).toLocaleString("tr-TR", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}{" "}
            ₺
          </span>
        ) : (
          <span className="text-xs text-gray-500">—</span>
        )}
      </td>

      {/* Kaldır */}
      <td className="px-3 py-2.5 text-center">
        {!zorunlu && (
          <button
            onClick={onKaldir}
            className="text-gray-500 hover:text-red-400 transition-colors"
            title="Kaldır"
          >
            <X size={14} />
          </button>
        )}
      </td>
    </tr>
  );
}

// ── MalzemeSecimPaneli (main export) ─────────────────────────────────────────
export default function MalzemeSecimPaneli({ token, isKalemiId, readonly = false }) {
  const [malzemeler, setMalzemeler] = useState([]);
  const [isKalemiMetraj, setIsKalemiMetraj] = useState(null);
  const [yukleniyor, setYukleniyor] = useState(true);
  const [kaydediliyor, setKaydediliyor] = useState(false);
  const [hata, setHata] = useState("");
  const [basari, setBasari] = useState("");
  const [ekModalAcik, setEkModalAcik] = useState(false);
  const [degismis, setDegismis] = useState(false);

  // ── Fetch malzemeler ──────────────────────────────────────────────────────
  const fetchMalzemeler = useCallback(() => {
    if (!isKalemiId) return;
    setYukleniyor(true);
    setHata("");
    fetch(`/api/v2/is-kalemleri/${isKalemiId}/csb-malzemeler`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => {
        if (!r.ok) throw new Error("Malzemeler yüklenemedi");
        return r.json();
      })
      .then((data) => {
        setMalzemeler(
          (data.malzemeler || []).map((m) => ({ ...m, secili: true }))
        );
        setIsKalemiMetraj(data.metraj ?? null);
      })
      .catch((e) => setHata(e.message))
      .finally(() => setYukleniyor(false));
  }, [isKalemiId, token]);

  useEffect(() => {
    fetchMalzemeler();
  }, [fetchMalzemeler]);

  // ── Satır değişikliği ─────────────────────────────────────────────────────
  const handleChange = useCallback((malzemeId, updates) => {
    setMalzemeler((prev) =>
      prev.map((m) => (m.id === malzemeId ? { ...m, ...updates } : m))
    );
    setDegismis(true);
  }, []);

  // ── Satır kaldırma (UI'dan işaretle) ─────────────────────────────────────
  const handleKaldir = useCallback((malzemeId) => {
    setMalzemeler((prev) => prev.filter((m) => m.id !== malzemeId));
    setDegismis(true);
  }, []);

  // ── Katalogdan malzeme ekleme ─────────────────────────────────────────────
  const handleEkMalzemeEkle = useCallback(
    (katalogMalzeme) => {
      const zatenVar = malzemeler.some(
        (m) => m.malzeme_katalog_id === katalogMalzeme.id
      );
      if (zatenVar) {
        setBasari("Bu malzeme zaten listede.");
        setTimeout(() => setBasari(""), 2000);
        setEkModalAcik(false);
        return;
      }
      // Katalog çarpanı varsa pozun metrajıyla çarp, yoksa 1 kullan
      let miktar = 1;
      if (katalogMalzeme.carpan != null && isKalemiMetraj != null) {
        miktar = parseFloat((isKalemiMetraj * katalogMalzeme.carpan).toFixed(4));
      }
      const yeni = {
        id: `yeni_${Date.now()}`,
        malzeme_katalog_id: katalogMalzeme.id,
        poz_no: katalogMalzeme.poz_no,
        ad: katalogMalzeme.ad,
        birim: katalogMalzeme.birim,
        miktar,
        guncel_fiyat: katalogMalzeme.guncel_fiyat ?? null,
        zorunlu: false,
        secili: true,
        _yeni: true,
      };
      setMalzemeler((prev) => [...prev, yeni]);
      setDegismis(true);
      setEkModalAcik(false);
    },
    [malzemeler, isKalemiMetraj]
  );

  // ── Kaydet ────────────────────────────────────────────────────────────────
  const handleKaydet = async () => {
    setKaydediliyor(true);
    setHata("");
    setBasari("");

    try {
      // Yeni eklenenler
      const ekle = malzemeler
        .filter((m) => m._yeni && m.secili !== false)
        .map((m) => ({
          malzeme_katalog_id: m.malzeme_katalog_id,
          miktar: m.miktar ?? 1,
        }));

      // Güncellenecekler (id sayısal, değişmiş miktar)
      const guncelle = malzemeler
        .filter((m) => !m._yeni && typeof m.id === "number" && m.secili !== false)
        .map((m) => ({ id: m.id, miktar: m.miktar }));

      // Kaldırılacaklar — artık listede olmayan id'ler (sayısal, zorunlu olmayan)
      // (Kullanıcı X'e basınca zaten listeden çıkardık; burada original ile karşılaştır)
      // Ayrıca secili=false olanları da kaldır
      const kaldir_ids = malzemeler
        .filter((m) => !m._yeni && typeof m.id === "number" && m.secili === false && !m.zorunlu)
        .map((m) => m.id);

      const body = {};
      if (ekle.length) body.ekle = ekle;
      if (guncelle.length) body.guncelle = guncelle;
      if (kaldir_ids.length) body.cikar = kaldir_ids;

      const res = await fetch(`/api/v2/is-kalemleri/${isKalemiId}/malzemeler`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Kaydetme başarısız");
      }

      setBasari("Malzemeler kaydedildi.");
      setDegismis(false);
      setTimeout(() => setBasari(""), 3000);
      fetchMalzemeler(); // Refresh from server
    } catch (e) {
      setHata(e.message);
    } finally {
      setKaydediliyor(false);
    }
  };

  // ── Toplam maliyet ────────────────────────────────────────────────────────
  const toplamMaliyet = malzemeler
    .filter((m) => m.secili !== false)
    .reduce((acc, m) => {
      if (m.miktar != null && m.guncel_fiyat != null)
        return acc + parseFloat(m.miktar) * parseFloat(m.guncel_fiyat);
      return acc;
    }, 0);

  const fiyatliSayisi = malzemeler.filter(
    (m) => m.secili !== false && m.guncel_fiyat != null
  ).length;

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <div className="bg-gray-900/50 border border-gray-700 rounded-xl overflow-hidden">
      {/* Panel Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-gray-800/50 border-b border-gray-700">
        <h3 className="text-white font-semibold flex items-center gap-2 text-sm">
          <Package size={16} className="text-blue-400" />
          Önerilen Malzemeler
          {!yukleniyor && (
            <span className="text-xs text-gray-400 font-normal">
              ({malzemeler.filter((m) => m.secili !== false).length} malzeme)
            </span>
          )}
        </h3>
        {!readonly && (
          <div className="flex items-center gap-2">
            {basari && (
              <span className="text-xs text-green-400 flex items-center gap-1">
                <Check size={12} />
                {basari}
              </span>
            )}
            <button
              onClick={() => setEkModalAcik(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-700 hover:bg-gray-600 text-white text-xs rounded-lg border border-gray-600 transition-colors"
            >
              <Plus size={13} />
              Ek Malzeme Ekle
            </button>
            {degismis && (
              <button
                onClick={handleKaydet}
                disabled={kaydediliyor}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-60 text-white text-xs rounded-lg transition-colors"
              >
                {kaydediliyor ? (
                  <Loader2 size={13} className="animate-spin" />
                ) : (
                  <Check size={13} />
                )}
                {kaydediliyor ? "Kaydediliyor..." : "Kaydet"}
              </button>
            )}
          </div>
        )}
      </div>

      {/* Error */}
      {hata && (
        <div className="flex items-center gap-2 px-4 py-2.5 bg-red-900/20 border-b border-red-700/30 text-red-400 text-sm">
          <AlertCircle size={14} />
          {hata}
        </div>
      )}

      {/* Loading */}
      {yukleniyor && (
        <div className="flex justify-center items-center py-10">
          <Loader2 size={22} className="animate-spin text-blue-400" />
        </div>
      )}

      {/* Empty */}
      {!yukleniyor && malzemeler.length === 0 && (
        <div className="text-center py-10 text-gray-500">
          <Package size={32} className="mx-auto mb-2 opacity-30" />
          <p className="text-sm">
            {readonly
              ? "Bu iş kalemine malzeme eklenmemiş."
              : 'Malzeme yok. "Ek Malzeme Ekle" ile ekleyebilirsiniz.'}
          </p>
        </div>
      )}

      {/* Table */}
      {!yukleniyor && malzemeler.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-700 bg-gray-800/60">
                <th className="px-3 py-2 text-center text-xs text-gray-300 font-semibold w-8">
                  {readonly ? "" : "✓"}
                </th>
                <th className="px-3 py-2 text-left text-xs text-gray-300 font-semibold w-24">
                  Poz No
                </th>
                <th className="px-3 py-2 text-left text-xs text-gray-300 font-semibold">
                  Malzeme Adı
                </th>
                <th className="px-3 py-2 text-center text-xs text-gray-300 font-semibold w-16">
                  Birim
                </th>
                <th className="px-3 py-2 text-right text-xs text-gray-300 font-semibold w-24">
                  Miktar
                </th>
                <th className="px-3 py-2 text-right text-xs text-gray-300 font-semibold w-28">
                  Güncel Fiyat
                </th>
                <th className="px-3 py-2 text-right text-xs text-gray-300 font-semibold w-28">
                  Tutar
                </th>
                {!readonly && (
                  <th className="px-3 py-2 w-8" />
                )}
              </tr>
            </thead>
            <tbody>
              {malzemeler.map((m) =>
                readonly ? (
                  <tr
                    key={m.id}
                    className="border-b border-gray-700/50 bg-gray-900/60 hover:bg-gray-800/50 transition-colors"
                  >
                    <td className="px-3 py-2.5 text-center">
                      {m.zorunlu ? (
                        <Lock size={13} className="text-orange-400 mx-auto" />
                      ) : (
                        <Check size={13} className="text-green-400 mx-auto" />
                      )}
                    </td>
                    <td className="px-3 py-2.5">
                      <span className="text-xs font-mono bg-orange-500/20 text-orange-300 px-1.5 py-0.5 rounded">
                        {m.poz_no || "—"}
                      </span>
                    </td>
                    <td className="px-3 py-2.5">
                      <span className="text-sm text-white font-medium">{m.ad}</span>
                      {m.zorunlu && (
                        <span className="ml-1.5 text-xs bg-orange-500/25 text-orange-300 px-1.5 py-0.5 rounded inline-block">
                          zorunlu
                        </span>
                      )}
                    </td>
                    <td className="px-3 py-2.5 text-center">
                      <span className="text-xs text-gray-300">{m.birim}</span>
                    </td>
                    <td className="px-3 py-2.5 text-right">
                      <span className="text-sm text-white">{m.miktar ?? "—"}</span>
                    </td>
                    <td className="px-3 py-2.5 text-right">
                      {m.guncel_fiyat != null ? (
                        <span className="text-sm text-green-400">
                          {parseFloat(m.guncel_fiyat).toLocaleString("tr-TR", {
                            minimumFractionDigits: 2,
                          })}{" "}
                          ₺
                        </span>
                      ) : (
                        <span className="text-xs text-gray-500">—</span>
                      )}
                    </td>
                    <td className="px-3 py-2.5 text-right">
                      {m.miktar != null && m.guncel_fiyat != null ? (
                        <span className="text-sm text-white font-medium">
                          {(parseFloat(m.miktar) * parseFloat(m.guncel_fiyat)).toLocaleString(
                            "tr-TR",
                            { minimumFractionDigits: 2 }
                          )}{" "}
                          ₺
                        </span>
                      ) : (
                        <span className="text-xs text-gray-500">—</span>
                      )}
                    </td>
                  </tr>
                ) : (
                  <MalzemeSatir
                    key={m.id}
                    malzeme={m}
                    onChange={(updates) => handleChange(m.id, updates)}
                    onKaldir={() => handleKaldir(m.id)}
                  />
                )
              )}
            </tbody>

            {/* Footer totals */}
            {fiyatliSayisi > 0 && (
              <tfoot>
                <tr className="border-t border-gray-600 bg-gray-800/40">
                  <td
                    colSpan={readonly ? 6 : 6}
                    className="px-3 py-2.5 text-right text-xs text-gray-400"
                  >
                    Tahmini Malzeme Maliyeti ({fiyatliSayisi} fiyatlı malzeme)
                  </td>
                  <td className="px-3 py-2.5 text-right">
                    <span className="text-sm text-blue-400 font-semibold">
                      {toplamMaliyet.toLocaleString("tr-TR", {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })}{" "}
                      ₺
                    </span>
                  </td>
                  {!readonly && <td />}
                </tr>
              </tfoot>
            )}
          </table>
        </div>
      )}

      {/* Ek Malzeme Modal */}
      {ekModalAcik && (
        <EkMalzemeModal
          token={token}
          isKalemiId={isKalemiId}
          isKalemiMetraj={isKalemiMetraj}
          onEkle={handleEkMalzemeEkle}
          onClose={() => setEkModalAcik(false)}
        />
      )}
    </div>
  );
}
