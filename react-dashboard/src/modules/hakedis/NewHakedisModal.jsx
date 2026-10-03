import { useState } from 'react'
import { createHakedis } from './api.js'
import { Button } from '../../ui/Button.jsx'
import { Field } from '../../ui/Field.jsx'
import { Input } from '../../ui/Field.jsx'
import { Modal } from '../../ui/Modal.jsx'
import { useToast } from '../../ui/Toast.jsx'

export function NewHakedisModal({ open, onClose, siteId, token, defaultStart, defaultEnd, onCreated }) {
  const [start, setStart] = useState(defaultStart || '')
  const [end, setEnd]     = useState(defaultEnd || '')
  const [busy, setBusy]   = useState(false)
  const [errors, setErrors] = useState({})
  const toast = useToast()

  // Varsayılan tarihleri modal açıldığında senkronize et
  function handleOpen() {
    setStart(defaultStart || '')
    setEnd(defaultEnd || '')
    setErrors({})
  }

  async function handleSubmit(e) {
    e.preventDefault()
    const errs = {}
    if (!start) errs.start = 'Başlangıç tarihi gerekli.'
    if (!end) errs.end = 'Bitiş tarihi gerekli.'
    if (start && end && start > end) errs.end = 'Bitiş tarihi başlangıç tarihinden önce olamaz.'
    if (Object.keys(errs).length) { setErrors(errs); return }

    setBusy(true)
    try {
      const result = await createHakedis({ santiye_id: siteId, donem_baslangic: start, donem_bitis: end }, token)
      toast({ message: 'Hakediş oluşturuldu.', tone: 'success' })
      onCreated(result.hakedis_id)
    } catch (err) {
      // 409/422 → modal içinde göster
      const msg = err.message || 'Bir hata oluştu.'
      if (err.status === 409 || err.status === 422) {
        setErrors({ server: msg })
      } else {
        toast({ message: msg, tone: 'danger' })
      }
    } finally {
      setBusy(false)
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Yeni hakediş oluştur"
      size="sm"
      footer={
        <>
          <Button variant="secondary" onClick={onClose} disabled={busy}>Vazgeç</Button>
          <Button type="submit" form="new-hakedis-form" loading={busy}>Oluştur</Button>
        </>
      }
    >
      <form id="new-hakedis-form" onSubmit={handleSubmit} className="flex flex-col gap-4">
        {errors.server && (
          <p role="alert" className="text-sm text-danger-fg bg-danger-bg border border-danger-border rounded px-3 py-2">
            {errors.server}
          </p>
        )}
        <Field label="Dönem başlangıcı" required error={errors.start}>
          <Input
            type="date"
            value={start}
            onChange={e => { setStart(e.target.value); setErrors(v => ({ ...v, start: '' })) }}
          />
        </Field>
        <Field label="Dönem bitişi" required error={errors.end}>
          <Input
            type="date"
            value={end}
            onChange={e => { setEnd(e.target.value); setErrors(v => ({ ...v, end: '' })) }}
          />
        </Field>
      </form>
    </Modal>
  )
}
