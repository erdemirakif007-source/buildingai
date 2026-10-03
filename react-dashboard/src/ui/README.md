# UI Bileşen Kütüphanesi — Kurallar

## text-transform: uppercase kullanılmaz

Bileşenlerde ve önizleme sayfasında `text-transform: uppercase` (Tailwind `uppercase` class'ı dahil)
kullanılmaz. Türkçe'de sayfa `lang="tr"` olduğunda CSS `uppercase` dönüşümü "i" harfini "İ"
yaparak yanlış görünüme yol açar (örn. "BUİLDİNGAI").

Büyük harf gerekiyorsa metin kaynak kodunda büyük yazılır; CSS ile dönüşüm yapılmaz.

## text-subtle sadece surface üzerinde

`text-subtle` (`--bai-text-subtle`) token'ı yalnızca beyaz/surface arka plan (`bg-surface`)
üzerinde kullanılır. Sayfa zemini (`bg-bg`, gri) ya da renkli arka planlar üzerinde
`text-muted` kullanılır.

**Yanlış:** `<div className="bg-bg"><span className="text-subtle">…</span></div>`  
**Doğru:** `<div className="bg-bg"><span className="text-muted">…</span></div>`
