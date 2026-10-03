import { useState } from 'react'
import { Package, PlusCircle } from 'lucide-react'
import { Button } from './Button'
import { Field, Input, Select, Textarea } from './Field'
import { Modal } from './Modal'
import { Badge } from './Badge'
import { Card } from './Card'
import { EmptyState } from './EmptyState'
import { Table } from './Table'
import { Tabs } from './Tabs'
import { Toggle } from './Toggle'
import { ToastProvider, useToast } from './Toast'
import { Spinner } from './Spinner'
import { formatMoney, formatNumber, formatDate, formatPercent } from './format'

// Renk paleti önizlemesi
const TOKEN_COLORS = [
  { label: 'brand', shades: [50,100,200,300,400,500,600,700,800,900] },
  { label: 'slate', shades: [50,100,200,300,400,500,600,700,800,900] },
]
const SEMANTIC_COLORS = [
  { key: '--bai-bg',           label: 'bg' },
  { key: '--bai-surface',      label: 'surface' },
  { key: '--bai-surface-muted',label: 'surface-muted' },
  { key: '--bai-border',       label: 'border' },
  { key: '--bai-border-strong',label: 'border-strong' },
  { key: '--bai-text',         label: 'text' },
  { key: '--bai-text-muted',   label: 'text-muted' },
  { key: '--bai-primary',      label: 'primary' },
  { key: '--bai-on-primary',   label: 'on-primary' },
  { key: '--bai-accent-soft',  label: 'accent-soft' },
  { key: '--bai-link',         label: 'link' },
  { key: '--bai-focus-ring',   label: 'focus-ring' },
]
const FONT_SIZES = ['xs','sm','md','base','lg','xl','2xl','3xl']

// Örnek hakediş verileri (gerçekçi, Türkçe)
const hakedisKalemleri = [
  { id: 1, pozNo: 'Y.16.001/01', tanim: 'Betonarme perde beton C30/37', birim: 'm³', miktar: 142.5, birimFiyat: 3850, tutar: 548625 },
  { id: 2, pozNo: 'Y.14.002/03', tanim: 'Ø14 Çelik hasır donatı B420C', birim: 'ton', miktar: 8.2, birimFiyat: 28400, tutar: 232880 },
  { id: 3, pozNo: 'Y.22.010/01', tanim: 'Kalıp ahşap perde ve kolon', birim: 'm²', miktar: 860, birimFiyat: 420, tutar: 361200 },
  { id: 4, pozNo: 'Y.31.001/02', tanim: 'Sıva + alçı ince sıva', birim: 'm²', miktar: 1240, birimFiyat: 185, tutar: 229400 },
  { id: 5, pozNo: 'Y.42.003/01', tanim: 'Seramik döşeme kaplaması', birim: 'm²', miktar: 380, birimFiyat: 310, tutar: 117800 },
]
const hakedisFooter = {
  tanim: 'Toplam',
  tutar: hakedisKalemleri.reduce((s, r) => s + r.tutar, 0),
}
const hakedisColumns = [
  { key: 'pozNo', header: 'Poz No' },
  { key: 'tanim', header: 'İş kalemi tanımı' },
  { key: 'birim', header: 'Birim' },
  { key: 'miktar', header: 'Miktar', numeric: true, render: r => formatNumber(r.miktar, 2) },
  { key: 'birimFiyat', header: 'Birim fiyat', numeric: true, render: r => formatMoney(r.birimFiyat) },
  { key: 'tutar', header: 'Tutar', numeric: true, render: r => formatMoney(r.tutar) },
]
const hakedisFooterRow = {
  pozNo: '', tanim: 'Toplam', birim: '', miktar: '', birimFiyat: '',
  tutar: formatMoney(hakedisFooter.tutar),
}

const tabsTabs = [
  { key: 'genel', label: 'Genel bilgiler', content: <p className="text-text-muted text-sm">Şantiye genel bilgi içeriği burada görünür.</p> },
  { key: 'hakediş', label: 'Hakediş', content: <p className="text-text-muted text-sm">Hakediş içeriği burada görünür.</p> },
  { key: 'stok', label: 'Stok', content: <p className="text-text-muted text-sm">Stok içeriği burada görünür.</p> },
]

function Section({ title, children }) {
  return (
    <section className="mb-12">
      <h2 className="text-2xl font-bold text-text mb-6 pb-2 border-b border-border">{title}</h2>
      {children}
    </section>
  )
}
function Row({ label, children }) {
  return (
    <div className="mb-6">
      {label && <p className="text-sm font-medium text-text-muted mb-2">{label}</p>}
      <div className="flex flex-wrap items-center gap-3">{children}</div>
    </div>
  )
}

function ToastDemo() {
  const toast = useToast()
  return (
    <Row label="Toast bildirimleri">
      <Button size="sm" variant="secondary" onClick={() => toast({ message: 'Hakediş başarıyla onaylandı.', tone: 'success' })}>Başarı</Button>
      <Button size="sm" variant="secondary" onClick={() => toast({ message: 'Stok hareketi kaydedilemedi. Sunucu hatası.', tone: 'danger' })}>Hata</Button>
      <Button size="sm" variant="secondary" onClick={() => toast({ message: '3 kalem güncellendi.', tone: 'info' })}>Bilgi</Button>
    </Row>
  )
}

export default function UiPreview() {
  const [modalOpen, setModalOpen] = useState(false)
  const [toggle1, setToggle1] = useState(true)
  const [toggle2, setToggle2] = useState(false)
  const [formError, setFormError] = useState('')
  const [loadingTable, setLoadingTable] = useState(false)

  return (
    <ToastProvider>
      <div className="min-h-dvh bg-bg">
        <div className="max-w-5xl mx-auto px-6 py-10">
          <div className="mb-10">
            <span className="text-sm font-semibold text-link">BuildingAI</span>
            <h1 className="text-3xl font-bold text-text mt-1">UI Bileşen Önizlemesi</h1>
            <p className="text-text-muted mt-2">Tasarım sistemi token'ları ve bileşen kütüphanesi.</p>
          </div>

          {/* Token: Renkler */}
          <Section title="Renk paleti">
            {TOKEN_COLORS.map(({ label, shades }) => (
              <div key={label} className="mb-4">
                <p className="text-sm text-text-muted mb-2 font-medium">{label}</p>
                <div className="flex gap-1 flex-wrap">
                  {shades.map(shade => (
                    <div key={shade} className="flex flex-col items-center gap-1">
                      <div
                        className="w-10 h-10 rounded border border-border"
                        style={{ background: `var(--bai-color-${label}-${shade})` }}
                        title={`${label}-${shade}`}
                      />
                      <span className="text-xs text-text-subtle">{shade}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
            <div className="mt-4">
              <p className="text-sm text-text-muted mb-2 font-medium">Anlamsal renkler</p>
              <div className="flex gap-2 flex-wrap">
                {SEMANTIC_COLORS.map(({ key, label }) => (
                  <div key={key} className="flex flex-col items-center gap-1">
                    <div
                      className="w-12 h-12 rounded border border-border"
                      style={{ background: `var(${key})` }}
                      title={key}
                    />
                    <span className="text-xs text-text-subtle">{label}</span>
                  </div>
                ))}
              </div>
            </div>
          </Section>

          {/* Token: Tipografi */}
          <Section title="Tipografi ölçeği">
            {FONT_SIZES.map(size => (
              <div key={size} className="flex items-baseline gap-6 py-2 border-b border-border last:border-0">
                <span className="text-sm text-text-subtle w-10 flex-none">{size}</span>
                <span style={{ fontSize: `var(--bai-font-size-${size})` }} className="text-text font-medium">
                  Şantiye hakkında kısa bilgi
                </span>
              </div>
            ))}
          </Section>

          {/* Button */}
          <Section title="Button">
            <Row label="Varyantlar">
              <Button variant="primary">Hakediş onay</Button>
              <Button variant="secondary">İptal</Button>
              <Button variant="ghost">Detay gör</Button>
              <Button variant="danger">Kaydı sil</Button>
            </Row>
            <Row label="Boyutlar">
              <Button size="sm">Küçük</Button>
              <Button size="md">Orta</Button>
              <Button size="lg">Büyük</Button>
            </Row>
            <Row label="İkon">
              <Button leftIcon={PlusCircle}>Kalem ekle</Button>
              <Button variant="secondary" rightIcon={Package}>Stok</Button>
            </Row>
            <Row label="Yükleniyor">
              <Button loading>Kaydediliyor…</Button>
              <Button variant="secondary" loading size="sm">İşleniyor</Button>
            </Row>
            <Row label="Devre dışı">
              <Button disabled>Onaylanamaz</Button>
              <Button variant="secondary" disabled>Düzenle</Button>
            </Row>
          </Section>

          {/* Form alanları */}
          <Section title="Form alanları (Field)">
            <div className="grid md:grid-cols-2 gap-6 max-w-2xl">
              <Field label="Şantiye adı" required>
                {props => <Input placeholder="Örn: Beşiktaş Rezidansı" {...props} />}
              </Field>
              <Field label="Birim fiyat (₺)" hint="Kuruş cinsinden giriniz.">
                {props => <Input numeric placeholder="0,00" {...props} />}
              </Field>
              <Field label="Durum">
                {props => (
                  <Select {...props}>
                    <option value="">Seçiniz…</option>
                    <option value="devam">Devam ediyor</option>
                    <option value="tamamlandi">Tamamlandı</option>
                    <option value="durduruldu">Durduruldu</option>
                  </Select>
                )}
              </Field>
              <Field label="Notlar">
                {props => <Textarea placeholder="Saha gözlemleri…" rows={3} {...props} />}
              </Field>
              <Field label="Miktar" error={formError || undefined}>
                {props => (
                  <div className="flex gap-2">
                    <Input numeric placeholder="0,00" {...props} />
                    <Button size="md" variant="secondary" type="button" onClick={() => setFormError(formError ? '' : 'Miktar sıfırdan büyük olmalı.')}>
                      Hata dene
                    </Button>
                  </div>
                )}
              </Field>
            </div>
          </Section>

          {/* Badge */}
          <Section title="Badge">
            <Row label="Tonlar">
              <Badge tone="neutral">Taslak</Badge>
              <Badge tone="success">Onaylandı</Badge>
              <Badge tone="danger">Reddedildi</Badge>
              <Badge tone="warning">Beklemede</Badge>
              <Badge tone="info">İncelemede</Badge>
              <Badge tone="brand">Yeni</Badge>
            </Row>
            <Row label="Noktalı">
              <Badge tone="success" dot>Aktif şantiye</Badge>
              <Badge tone="danger" dot>ISG uyarısı</Badge>
              <Badge tone="warning" dot>Stok azaldı</Badge>
            </Row>
          </Section>

          {/* Card */}
          <Section title="Card">
            <div className="grid md:grid-cols-2 gap-4">
              <Card title="Toplam hakediş" description="2026 yılı kümülatif" action={<Badge tone="success">Onaylı</Badge>}>
                <p className="text-3xl font-bold text-text tabular-nums">{formatMoney(1490105)}</p>
                <p className="text-sm text-text-muted mt-1">Son güncelleme: {formatDate('2026-09-28')}</p>
              </Card>
              <Card title="Stok özeti" padding="sm">
                <div className="space-y-2 mt-2">
                  {[['Çimento (çuval)', 480, 'adet'], ['Ø12 Demir', 2.4, 'ton'], ['Seramik', 340, 'm²']].map(([ad, miktar, birim]) => (
                    <div key={ad} className="flex justify-between text-sm">
                      <span className="text-text-muted">{ad}</span>
                      <span className="tabular-nums font-medium text-text">{formatNumber(miktar, 0)} {birim}</span>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </Section>

          {/* Spinner */}
          <Section title="Spinner">
            <Row label="Boyutlar">
              <Spinner size="sm" />
              <Spinner size="md" />
              <Spinner size="lg" />
            </Row>
          </Section>

          {/* Toggle */}
          <Section title="Toggle">
            <Row>
              <Toggle label="Bildirimleri etkinleştir" checked={toggle1} onChange={setToggle1} />
              <Toggle label="Otomatik senkronizasyon" checked={toggle2} onChange={setToggle2} />
              <Toggle label="Devre dışı" checked={true} disabled />
            </Row>
          </Section>

          {/* Tabs */}
          <Section title="Tabs">
            <Tabs tabs={tabsTabs} />
          </Section>

          {/* Table */}
          <Section title="Table — Hakediş kalemleri">
            <div className="flex gap-3 mb-4">
              <Button size="sm" variant="secondary" onClick={() => setLoadingTable(!loadingTable)}>
                {loadingTable ? 'Yükleniyor gizle' : 'Yükleniyor göster'}
              </Button>
            </div>
            <Table
              columns={hakedisColumns}
              rows={loadingTable ? [] : hakedisKalemleri}
              loading={loadingTable}
              footer={hakedisFooterRow}
              onRowClick={row => alert(`Seçilen kalem: ${row.tanim}`)}
            />
          </Section>

          {/* EmptyState */}
          <Section title="EmptyState">
            <div className="border border-border rounded">
              <EmptyState
                icon={Package}
                title="Henüz stok kalemi yok"
                description="İlk stok hareketini ekleyerek takibe başlayın."
                action={<Button leftIcon={PlusCircle} size="sm">Hareket ekle</Button>}
              />
            </div>
          </Section>

          {/* Modal */}
          <Section title="Modal">
            <Row>
              <Button onClick={() => setModalOpen(true)}>Modal aç (md)</Button>
            </Row>
            <Modal
              open={modalOpen}
              onClose={() => setModalOpen(false)}
              title="Stok hareketi ekle"
              size="md"
              footer={
                <>
                  <Button variant="secondary" onClick={() => setModalOpen(false)}>İptal</Button>
                  <Button onClick={() => setModalOpen(false)}>Kaydet</Button>
                </>
              }
            >
              <div className="flex flex-col gap-4">
                <Field label="Malzeme" required>
                  {props => (
                    <Select {...props}>
                      <option value="">Malzeme seçin…</option>
                      <option value="cimento">Çimento</option>
                      <option value="demir">Demir</option>
                      <option value="kum">Kum</option>
                    </Select>
                  )}
                </Field>
                <div className="grid grid-cols-2 gap-4">
                  <Field label="Miktar" required>
                    {props => <Input numeric placeholder="0,00" {...props} />}
                  </Field>
                  <Field label="Birim">
                    {props => (
                      <Select {...props}>
                        <option>adet</option>
                        <option>ton</option>
                        <option>m³</option>
                        <option>m²</option>
                      </Select>
                    )}
                  </Field>
                </div>
                <Field label="Açıklama">
                  {props => <Textarea rows={2} placeholder="İsteğe bağlı not…" {...props} />}
                </Field>
              </div>
            </Modal>
          </Section>

          {/* Toast */}
          <Section title="Toast">
            <ToastDemo />
          </Section>

          {/* Format yardımcıları */}
          <Section title="Format yardımcıları">
            <div className="space-y-2 font-mono text-sm text-text-muted">
              <p>formatMoney(1490105) → <strong className="text-text">{formatMoney(1490105)}</strong></p>
              <p>formatMoney(1490105, {'{cents:true}'}) → <strong className="text-text">{formatMoney(1490105, { cents: true })}</strong></p>
              <p>formatNumber(3.14159, 2) → <strong className="text-text">{formatNumber(3.14159, 2)}</strong></p>
              <p>formatDate('2026-09-28') → <strong className="text-text">{formatDate('2026-09-28')}</strong></p>
              <p>formatPercent(0.724) → <strong className="text-text">{formatPercent(0.724)}</strong></p>
            </div>
          </Section>
        </div>
      </div>
    </ToastProvider>
  )
}
