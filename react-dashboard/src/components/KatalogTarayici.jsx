import { useState, useEffect, useCallback } from "react";
import {
  BookOpen, Search, ChevronRight, ChevronDown, Package,
  Wrench, Loader2, AlertCircle, X, ExternalLink, Tag
} from "lucide-react";

// ── Turkish normalization ─────────────────────────────────────────────────────
const trNorm = (s = "") =>
  s.toLowerCase()
    .replace(/ğ/g, "g").replace(/ü/g, "u").replace(/ş/g, "s")
    .replace(/ı/g, "i").replace(/ö/g, "o").replace(/ç/g, "c")
    .replace(/Ğ/g, "g").replace(/Ü/g, "u").replace(/Ş/g, "s")
    .replace(/İ/g, "i").replace(/Ö/g, "o").replace(/Ç/g, "c");

function useDebounce(value, delay = 300) {
  const [deb, setDeb] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDeb(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return deb;
}

// ── Sol panel: ağaç bileşeni ──────────────────────────────────────────────────
function AgacDugum({ etiket, ikon, sayisi, acik, onToggle, secili, onSec, alt = [] }) {
  const hasAlt = alt.length > 0;
  return (
    <div>
      <button
        onClick={() => (hasAlt ? onToggle() : onSec())}
        className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors text-left
          ${secili
            ? "bg-blue-600/20 text-blue-300 border border-blue-600/30"
            : "text-gray-300 hover:bg-gray-700/50 hover:text-white border border-transparent"
          }`}
      >
        <span className="text-gray-500 shrink-0">{ikon}</span>
        <span className="flex-1 truncate">{etiket}</span>
        {sayisi != null && (
          <span className="text-xs text-gray-500 shrink-0">{sayisi}</span>
        )}
        {hasAlt && (
          <span className="text-gray-500 shrink-0">
            {acik ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          </span>
        )}
      </button>
      {hasAlt && acik && (
        <div className="ml-4 mt-0.5 space-y-0.5">
          {alt.map((a) => (
            <button
              key={a.id}
              onClick={() => a.onSec()}
              className={`w-full flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs transition-colors text-left
                ${a.secili
                  ? "bg-blue-600/20 text-blue-300 border border-blue-600/30"
                  : "text-gray-400 hover:bg-gray-700/40 hover:text-white border border-transparent"
                }`}
            >
              <span className="flex-1 truncate">{a.etiket}</span>
              {a.sayisi != null && (
                <span className="text-xs text-gray-600">{a.sayisi}</span>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

// ── İş kalemi detay paneli ────────────────────────────────────────────────────
function IsKalemiDetay({ token, item }) {
  const [detay, setDetay] = useState(null);
  const [yukleniyor, setYukleniyor] = useState(false);
  const [hata, setHata] = useState("");
  const [malzemeAcik, setMalzemeAcik] = useState(true);

  useEffect(() => {
    if (!item) return;
    setYukleniyor(true);
    setHata("");
    setDetay(null);
    fetch(`/api/katalog/is-kalemleri/${item.id}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => {
        if (!r.ok) throw new Error("Yüklenemedi");
        return r.json();
      })
      .then(setDetay)
      .catch((e) => setHata(e.message))
      .finally(() => setYukleniyor(false));
  }, [item, token]);

  if (!item) return null;

  return (
    <div className="bg-gray-800/40 border border-gray-700 rounded-xl overflow-hidden">
      {/* Header */}
      <div className="px-5 py-4 border-b border-gray-700 bg-gray-800/60">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-mono text-blue-400 bg-blue-900/30 px-2 py-0.5 rounded">
                {item.poz_no}
              </span>
              <span className="text-xs text-gray-500">{item.birim}</span>
            </div>
            <h3 className="text-white font-semibold text-base leading-snug">{item.ad}</h3>
            <p className="text-xs text-gray-400 mt-0.5">
              {item.grup}
              {item.alt_grup ? ` › ${item.alt_grup}` : ""}
            </p>
          </div>
        </div>
        {item.aciklama && (
          <p className="mt-2 text-sm text-gray-400 leading-relaxed">{item.aciklama}</p>
        )}
      </div>

      {yukleniyor && (
        <div className="flex justify-center py-8">
          <Loader2 size={20} className="animate-spin text-blue-400" />
        </div>
      )}
      {hata && (
        <div className="flex items-center gap-2 px-5 py-4 text-red-400 text-sm">
          <AlertCircle size={14} />
          {hata}
        </div>
      )}

      {detay && (
        <>
          {/* Maliyet özet */}
          {detay.tahmini_birim_maliyet != null && (
            <div className="px-5 py-3 bg-blue-900/10 border-b border-gray-700/50">
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">Tahmini Birim Maliyeti</span>
                <span className="text-sm font-semibold text-blue-300">
                  {parseFloat(detay.tahmini_birim_maliyet).toLocaleString("tr-TR", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}{" "}
                  ₺ / {detay.birim}
                </span>
              </div>
            </div>
          )}

          {/* Malzemeler */}
          {detay.malzemeler && detay.malzemeler.length > 0 && (
            <div>
              <button
                onClick={() => setMalzemeAcik((v) => !v)}
                className="w-full flex items-center justify-between px-5 py-3 text-sm text-gray-300 hover:text-white hover:bg-gray-800/30 transition-colors border-b border-gray-700/50"
              >
                <span className="flex items-center gap-2 font-medium">
                  <Package size={14} className="text-blue-400" />
                  Kullanılan Malzemeler ({detay.malzemeler.length})
                </span>
                {malzemeAcik ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
              </button>

              {malzemeAcik && (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-gray-700/50 bg-gray-800/20">
                        <th className="px-4 py-2 text-left text-xs text-gray-500 font-medium">Poz No</th>
                        <th className="px-4 py-2 text-left text-xs text-gray-500 font-medium">Malzeme</th>
                        <th className="px-4 py-2 text-center text-xs text-gray-500 font-medium">Birim</th>
                        <th className="px-4 py-2 text-right text-xs text-gray-500 font-medium">Miktar</th>
                        <th className="px-4 py-2 text-right text-xs text-gray-500 font-medium">Güncel Fiyat</th>
                        <th className="px-4 py-2 text-center text-xs text-gray-500 font-medium">Zorunlu</th>
                      </tr>
                    </thead>
                    <tbody>
                      {detay.malzemeler.map((m) => (
                        <tr
                          key={m.id}
                          className="border-b border-gray-700/30 hover:bg-gray-800/20"
                        >
                          <td className="px-4 py-2.5">
                            <span className="text-xs font-mono text-gray-400">{m.poz_no || "—"}</span>
                          </td>
                          <td className="px-4 py-2.5">
                            <span className="text-white text-sm">{m.ad}</span>
                            {m.alt_kategori && (
                              <span className="ml-2 text-xs text-gray-500">{m.alt_kategori}</span>
                            )}
                          </td>
                          <td className="px-4 py-2.5 text-center">
                            <span className="text-xs text-gray-300">{m.birim}</span>
                          </td>
                          <td className="px-4 py-2.5 text-right">
                            <span className="text-sm text-white">{m.miktar ?? "—"}</span>
                          </td>
                          <td className="px-4 py-2.5 text-right">
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
                          <td className="px-4 py-2.5 text-center">
                            {m.zorunlu ? (
                              <span className="text-xs text-yellow-500">Evet</span>
                            ) : (
                              <span className="text-xs text-gray-600">—</span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

// ── Malzeme detay paneli ──────────────────────────────────────────────────────
function MalzemeDetay({ token, item }) {
  const [detay, setDetay] = useState(null);
  const [yukleniyor, setYukleniyor] = useState(false);
  const [hata, setHata] = useState("");
  const [isKalemiAcik, setIsKalemiAcik] = useState(true);

  useEffect(() => {
    if (!item) return;
    setYukleniyor(true);
    setHata("");
    setDetay(null);
    fetch(`/api/katalog/malzemeler/${item.id}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => {
        if (!r.ok) throw new Error("Yüklenemedi");
        return r.json();
      })
      .then(setDetay)
      .catch((e) => setHata(e.message))
      .finally(() => setYukleniyor(false));
  }, [item, token]);

  if (!item) return null;

  return (
    <div className="bg-gray-800/40 border border-gray-700 rounded-xl overflow-hidden">
      {/* Header */}
      <div className="px-5 py-4 border-b border-gray-700 bg-gray-800/60">
        <div className="flex items-start gap-3">
          <Package size={18} className="text-blue-400 mt-0.5 shrink-0" />
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-mono text-blue-400 bg-blue-900/30 px-2 py-0.5 rounded">
                {item.poz_no}
              </span>
              <span className="text-xs text-gray-500">{item.birim}</span>
            </div>
            <h3 className="text-white font-semibold text-base">{item.ad}</h3>
            <p className="text-xs text-gray-400 mt-0.5">
              {item.kategori}
              {item.alt_kategori ? ` › ${item.alt_kategori}` : ""}
            </p>
          </div>
        </div>
        {item.aciklama && (
          <p className="mt-2 text-sm text-gray-400">{item.aciklama}</p>
        )}
      </div>

      {yukleniyor && (
        <div className="flex justify-center py-8">
          <Loader2 size={20} className="animate-spin text-blue-400" />
        </div>
      )}
      {hata && (
        <div className="flex items-center gap-2 px-5 py-4 text-red-400 text-sm">
          <AlertCircle size={14} />
          {hata}
        </div>
      )}

      {detay?.iliskili_is_kalemleri?.length > 0 && (
        <div>
          <button
            onClick={() => setIsKalemiAcik((v) => !v)}
            className="w-full flex items-center justify-between px-5 py-3 text-sm text-gray-300 hover:text-white hover:bg-gray-800/30 transition-colors border-b border-gray-700/50"
          >
            <span className="flex items-center gap-2 font-medium">
              <Wrench size={14} className="text-orange-400" />
              Kullanıldığı İş Kalemleri ({detay.iliskili_is_kalemleri.length})
            </span>
            {isKalemiAcik ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          </button>

          {isKalemiAcik && (
            <div className="divide-y divide-gray-700/30">
              {detay.iliskili_is_kalemleri.map((ik) => (
                <div key={ik.id} className="px-5 py-3 hover:bg-gray-800/20">
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono text-orange-400/80">{ik.poz_no}</span>
                        <span className="text-xs text-gray-500">{ik.birim}</span>
                      </div>
                      <p className="text-sm text-white mt-0.5">{ik.ad}</p>
                      <p className="text-xs text-gray-500 mt-0.5">
                        {ik.grup}{ik.alt_grup ? ` › ${ik.alt_grup}` : ""}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── Ana Bileşen: KatalogTarayici ──────────────────────────────────────────────
export default function KatalogTarayici({ token }) {
  // Panel: "is_kalemleri" | "malzemeler"
  const [panel, setPanel] = useState("is_kalemleri");

  // İş Kalemleri state
  const [ikGruplar, setIkGruplar] = useState([]);
  const [ikAcikGruplar, setIkAcikGruplar] = useState(new Set());
  const [ikSeciliGrup, setIkSeciliGrup] = useState(null);
  const [ikSeciliAltGrup, setIkSeciliAltGrup] = useState(null);
  const [ikListesi, setIkListesi] = useState([]);
  const [ikYukleniyor, setIkYukleniyor] = useState(false);
  const [ikSecili, setIkSecili] = useState(null);

  // Malzeme state
  const [mKategoriler, setMKategoriler] = useState([]);
  const [mAcikKategoriler, setMAcikKategoriler] = useState(new Set());
  const [mSeciliKategori, setMSeciliKategori] = useState(null);
  const [mSeciliAltKategori, setMSeciliAltKategori] = useState(null);
  const [mListesi, setMListesi] = useState([]);
  const [mYukleniyor, setMYukleniyor] = useState(false);
  const [mSecili, setMSecili] = useState(null);

  // Global search
  const [arama, setArama] = useState("");
  const [aramaYukleniyor, setAramaYukleniyor] = useState(false);
  const [aramaSonuclari, setAramaSonuclari] = useState(null);
  const debArama = useDebounce(arama, 300);

  // ── Fetch gruplar + kategoriler ─────────────────────────────────────────
  useEffect(() => {
    fetch("/api/katalog/is-kalemi-gruplar", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => setIkGruplar(data.gruplar || []))
      .catch(() => {});

    fetch("/api/katalog/malzeme-kategoriler", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => setMKategoriler(data.kategoriler || []))
      .catch(() => {});
  }, [token]);

  // ── Fetch is kalemleri listesi ──────────────────────────────────────────
  useEffect(() => {
    if (panel !== "is_kalemleri" || aramaSonuclari !== null) return;
    setIkYukleniyor(true);
    const params = new URLSearchParams();
    if (ikSeciliGrup) params.set("grup", ikSeciliGrup);
    if (ikSeciliAltGrup) params.set("alt_grup", ikSeciliAltGrup);
    fetch(`/api/katalog/is-kalemleri?${params}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => setIkListesi(data.is_kalemleri || []))
      .catch(() => setIkListesi([]))
      .finally(() => setIkYukleniyor(false));
  }, [panel, ikSeciliGrup, ikSeciliAltGrup, aramaSonuclari, token]);

  // ── Fetch malzeme listesi ───────────────────────────────────────────────
  useEffect(() => {
    if (panel !== "malzemeler" || aramaSonuclari !== null) return;
    setMYukleniyor(true);
    const params = new URLSearchParams();
    if (mSeciliKategori) params.set("kategori", mSeciliKategori);
    if (mSeciliAltKategori) params.set("alt_kategori", mSeciliAltKategori);
    fetch(`/api/katalog/malzemeler?${params}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => setMListesi(data.malzemeler || []))
      .catch(() => setMListesi([]))
      .finally(() => setMYukleniyor(false));
  }, [panel, mSeciliKategori, mSeciliAltKategori, aramaSonuclari, token]);

  // ── Global arama ────────────────────────────────────────────────────────
  useEffect(() => {
    if (debArama.trim().length < 2) {
      setAramaSonuclari(null);
      return;
    }
    setAramaYukleniyor(true);
    fetch(`/api/katalog/ara?q=${encodeURIComponent(debArama)}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then(setAramaSonuclari)
      .catch(() => setAramaSonuclari({ is_kalemleri: [], malzemeler: [] }))
      .finally(() => setAramaYukleniyor(false));
  }, [debArama, token]);

  // ── Sol Panel Ağaç ─────────────────────────────────────────────────────
  const toggleIkGrup = (grup) => {
    setIkAcikGruplar((prev) => {
      const next = new Set(prev);
      next.has(grup) ? next.delete(grup) : next.add(grup);
      return next;
    });
  };

  const toggleMKategori = (kat) => {
    setMAcikKategoriler((prev) => {
      const next = new Set(prev);
      next.has(kat) ? next.delete(kat) : next.add(kat);
      return next;
    });
  };

  // ── Sağ panel içeriği ───────────────────────────────────────────────────
  const renderSagPanel = () => {
    // Arama modu
    if (aramaSonuclari !== null) {
      const toplamSonuc =
        (aramaSonuclari.is_kalemleri?.length || 0) +
        (aramaSonuclari.malzemeler?.length || 0);
      return (
        <div className="space-y-4">
          <p className="text-sm text-gray-400">
            &ldquo;{debArama}&rdquo; için {toplamSonuc} sonuç bulundu
          </p>

          {aramaSonuclari.is_kalemleri?.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                İş Kalemleri ({aramaSonuclari.is_kalemleri.length})
              </h4>
              <div className="space-y-1">
                {aramaSonuclari.is_kalemleri.map((ik) => (
                  <button
                    key={ik.id}
                    onClick={() => { setIkSecili(ik); setArama(""); }}
                    className={`w-full text-left px-4 py-3 rounded-lg border transition-colors
                      ${ikSecili?.id === ik.id
                        ? "bg-blue-600/20 border-blue-600/40 text-blue-300"
                        : "bg-gray-800/40 border-gray-700 hover:bg-gray-700/50 text-white"
                      }`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono text-orange-400">{ik.poz_no}</span>
                      <span className="text-xs text-gray-500">{ik.birim}</span>
                    </div>
                    <p className="text-sm mt-0.5">{ik.ad}</p>
                    <p className="text-xs text-gray-500">{ik.grup}{ik.alt_grup ? ` › ${ik.alt_grup}` : ""}</p>
                  </button>
                ))}
              </div>
            </div>
          )}

          {aramaSonuclari.malzemeler?.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Malzemeler ({aramaSonuclari.malzemeler.length})
              </h4>
              <div className="space-y-1">
                {aramaSonuclari.malzemeler.map((m) => (
                  <button
                    key={m.id}
                    onClick={() => { setMSecili(m); setArama(""); setPanel("malzemeler"); }}
                    className={`w-full text-left px-4 py-3 rounded-lg border transition-colors
                      ${mSecili?.id === m.id
                        ? "bg-blue-600/20 border-blue-600/40 text-blue-300"
                        : "bg-gray-800/40 border-gray-700 hover:bg-gray-700/50 text-white"
                      }`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono text-blue-400">{m.poz_no}</span>
                      <span className="text-xs text-gray-500">{m.birim}</span>
                    </div>
                    <p className="text-sm mt-0.5">{m.ad}</p>
                    <p className="text-xs text-gray-500">{m.kategori}{m.alt_kategori ? ` › ${m.alt_kategori}` : ""}</p>
                  </button>
                ))}
              </div>
            </div>
          )}

          {toplamSonuc === 0 && (
            <div className="text-center py-12 text-gray-500">
              <Search size={32} className="mx-auto mb-2 opacity-30" />
              <p className="text-sm">Sonuç bulunamadı</p>
            </div>
          )}
        </div>
      );
    }

    if (panel === "is_kalemleri") {
      return (
        <div className="space-y-3">
          {ikYukleniyor && (
            <div className="flex justify-center py-10">
              <Loader2 size={20} className="animate-spin text-blue-400" />
            </div>
          )}
          {!ikYukleniyor && ikListesi.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              <Wrench size={32} className="mx-auto mb-2 opacity-30" />
              <p className="text-sm">İş kalemi bulunamadı</p>
            </div>
          )}
          {!ikYukleniyor && ikListesi.map((ik) => (
            <button
              key={ik.id}
              onClick={() => setIkSecili(ikSecili?.id === ik.id ? null : ik)}
              className={`w-full text-left px-4 py-3 rounded-xl border transition-all
                ${ikSecili?.id === ik.id
                  ? "bg-blue-600/15 border-blue-600/40 ring-1 ring-blue-600/20"
                  : "bg-gray-800/40 border-gray-700 hover:bg-gray-700/40 hover:border-gray-600"
                }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-mono text-orange-400">{ik.poz_no}</span>
                    <span className="text-xs text-gray-500 bg-gray-700/50 px-1.5 py-0.5 rounded">
                      {ik.birim}
                    </span>
                    {ik.alt_grup && (
                      <span className="text-xs text-gray-500">{ik.alt_grup}</span>
                    )}
                  </div>
                  <p className={`text-sm font-medium leading-snug ${ikSecili?.id === ik.id ? "text-blue-200" : "text-white"}`}>
                    {ik.ad}
                  </p>
                  {ik.aciklama && (
                    <p className="text-xs text-gray-500 mt-1 truncate">{ik.aciklama}</p>
                  )}
                </div>
                <ChevronRight
                  size={14}
                  className={`shrink-0 mt-1 transition-transform ${ikSecili?.id === ik.id ? "rotate-90 text-blue-400" : "text-gray-600"}`}
                />
              </div>
            </button>
          ))}

          {/* Detay */}
          {ikSecili && (
            <div className="mt-2">
              <IsKalemiDetay token={token} item={ikSecili} />
            </div>
          )}
        </div>
      );
    }

    // panel === "malzemeler"
    return (
      <div className="space-y-3">
        {mYukleniyor && (
          <div className="flex justify-center py-10">
            <Loader2 size={20} className="animate-spin text-blue-400" />
          </div>
        )}
        {!mYukleniyor && mListesi.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <Package size={32} className="mx-auto mb-2 opacity-30" />
            <p className="text-sm">Malzeme bulunamadı</p>
          </div>
        )}
        {!mYukleniyor && mListesi.map((m) => (
          <button
            key={m.id}
            onClick={() => setMSecili(mSecili?.id === m.id ? null : m)}
            className={`w-full text-left px-4 py-3 rounded-xl border transition-all
              ${mSecili?.id === m.id
                ? "bg-blue-600/15 border-blue-600/40 ring-1 ring-blue-600/20"
                : "bg-gray-800/40 border-gray-700 hover:bg-gray-700/40 hover:border-gray-600"
              }`}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-mono text-blue-400">{m.poz_no}</span>
                  <span className="text-xs text-gray-500 bg-gray-700/50 px-1.5 py-0.5 rounded">
                    {m.birim}
                  </span>
                  {m.alt_kategori && (
                    <span className="text-xs text-gray-500">{m.alt_kategori}</span>
                  )}
                </div>
                <p className={`text-sm font-medium ${mSecili?.id === m.id ? "text-blue-200" : "text-white"}`}>
                  {m.ad}
                </p>
              </div>
              <ChevronRight
                size={14}
                className={`shrink-0 mt-1 transition-transform ${mSecili?.id === m.id ? "rotate-90 text-blue-400" : "text-gray-600"}`}
              />
            </div>
          </button>
        ))}

        {/* Detay */}
        {mSecili && (
          <div className="mt-2">
            <MalzemeDetay token={token} item={mSecili} />
          </div>
        )}
      </div>
    );
  };

  // ─────────────────────────────────────────────────────────────────────────
  return (
    <div className="flex flex-col h-full min-h-0">
      {/* Sayfa başlığı */}
      <div className="px-6 py-4 border-b border-gray-700 shrink-0">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-600/20 rounded-lg">
              <BookOpen size={20} className="text-blue-400" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-white">ÇŞB Katalog</h1>
              <p className="text-xs text-gray-400">Çevre ve Şehircilik Bakanlığı iş kalemleri ve malzeme kataloğu</p>
            </div>
          </div>

          {/* Global search */}
          <div className="relative w-72">
            <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              value={arama}
              onChange={(e) => setArama(e.target.value)}
              placeholder="Katalogda ara..."
              className="w-full bg-gray-800 border border-gray-600 rounded-xl py-2 pl-9 pr-8 text-white placeholder-gray-500 text-sm focus:outline-none focus:border-blue-500 transition-colors"
            />
            {arama && (
              <button
                onClick={() => setArama("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
              >
                <X size={14} />
              </button>
            )}
            {aramaYukleniyor && (
              <Loader2
                size={13}
                className="absolute right-3 top-1/2 -translate-y-1/2 animate-spin text-blue-400"
              />
            )}
          </div>
        </div>
      </div>

      {/* Ana içerik */}
      <div className="flex flex-1 min-h-0 overflow-hidden">
        {/* Sol panel: Ağaç */}
        <div className="w-64 shrink-0 border-r border-gray-700 flex flex-col overflow-hidden">
          {/* Tab seçici */}
          <div className="flex border-b border-gray-700 shrink-0">
            <button
              onClick={() => { setPanel("is_kalemleri"); setArama(""); }}
              className={`flex-1 py-2.5 text-xs font-medium transition-colors flex items-center justify-center gap-1.5
                ${panel === "is_kalemleri"
                  ? "text-white border-b-2 border-blue-500 bg-gray-800/30"
                  : "text-gray-400 hover:text-white"
                }`}
            >
              <Wrench size={13} />
              İş Kalemleri
            </button>
            <button
              onClick={() => { setPanel("malzemeler"); setArama(""); }}
              className={`flex-1 py-2.5 text-xs font-medium transition-colors flex items-center justify-center gap-1.5
                ${panel === "malzemeler"
                  ? "text-white border-b-2 border-blue-500 bg-gray-800/30"
                  : "text-gray-400 hover:text-white"
                }`}
            >
              <Package size={13} />
              Malzemeler
            </button>
          </div>

          {/* Ağaç */}
          <div className="flex-1 overflow-y-auto p-2 space-y-0.5">
            {panel === "is_kalemleri" && (
              <>
                <AgacDugum
                  etiket="Tüm İş Kalemleri"
                  ikon={<Wrench size={14} />}
                  secili={!ikSeciliGrup}
                  onSec={() => { setIkSeciliGrup(null); setIkSeciliAltGrup(null); setIkSecili(null); }}
                />
                {ikGruplar.map((g) => (
                  <AgacDugum
                    key={g.grup}
                    etiket={g.grup}
                    ikon={<Tag size={13} />}
                    sayisi={g.toplam_kalemi}
                    acik={ikAcikGruplar.has(g.grup)}
                    onToggle={() => toggleIkGrup(g.grup)}
                    secili={ikSeciliGrup === g.grup && !ikSeciliAltGrup}
                    onSec={() => {
                      setIkSeciliGrup(g.grup);
                      setIkSeciliAltGrup(null);
                      setIkSecili(null);
                    }}
                    alt={(g.alt_gruplar || []).map((ag) => ({
                      id: ag.alt_grup,
                      etiket: ag.alt_grup,
                      sayisi: ag.kalemi_sayisi,
                      secili: ikSeciliAltGrup === ag.alt_grup,
                      onSec: () => {
                        setIkSeciliGrup(g.grup);
                        setIkSeciliAltGrup(ag.alt_grup);
                        setIkSecili(null);
                      },
                    }))}
                  />
                ))}
              </>
            )}

            {panel === "malzemeler" && (
              <>
                <AgacDugum
                  etiket="Tüm Malzemeler"
                  ikon={<Package size={14} />}
                  secili={!mSeciliKategori}
                  onSec={() => { setMSeciliKategori(null); setMSeciliAltKategori(null); setMSecili(null); }}
                />
                {mKategoriler.map((k) => (
                  <AgacDugum
                    key={k.kategori}
                    etiket={k.kategori}
                    ikon={<Tag size={13} />}
                    sayisi={k.malzeme_sayisi}
                    acik={mAcikKategoriler.has(k.kategori)}
                    onToggle={() => toggleMKategori(k.kategori)}
                    secili={mSeciliKategori === k.kategori && !mSeciliAltKategori}
                    onSec={() => {
                      setMSeciliKategori(k.kategori);
                      setMSeciliAltKategori(null);
                      setMSecili(null);
                    }}
                    alt={(k.alt_kategoriler || []).map((ak) => ({
                      id: ak.alt_kategori,
                      etiket: ak.alt_kategori,
                      sayisi: ak.malzeme_sayisi,
                      secili: mSeciliAltKategori === ak.alt_kategori,
                      onSec: () => {
                        setMSeciliKategori(k.kategori);
                        setMSeciliAltKategori(ak.alt_kategori);
                        setMSecili(null);
                      },
                    }))}
                  />
                ))}
              </>
            )}
          </div>
        </div>

        {/* Sağ panel */}
        <div className="flex-1 overflow-y-auto p-4">
          {renderSagPanel()}
        </div>
      </div>
    </div>
  );
}
