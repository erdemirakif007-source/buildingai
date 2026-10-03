import { apiFetch, apiBlob } from '../../lib/api.js'

export const fetchListe       = (siteId, token, signal) => apiFetch(`/api/hakedis/liste/${siteId}`, { token, signal })
export const fetchDetay       = (id, token, signal)     => apiFetch(`/api/hakedis/detay/${id}`, { token, signal })
export const fetchDecisions   = (id, token, signal)     => apiFetch(`/api/hakedis/decisions/${id}`, { token, signal })
export const fetchCaps        = (id, token, signal)     => apiFetch(`/api/v2/payments/${id}/capabilities`, { token, signal })
export const fetchAllocations = (id, token, signal)     => apiFetch(`/api/v2/payments/${id}/allocations`, { token, signal })
export const createHakedis    = (body, token)           => apiFetch('/api/hakedis/olustur', { method: 'POST', body, token })
export const updateKalem      = (body, token)           => apiFetch('/api/hakedis/kalem-guncelle', { method: 'PATCH', body, token })
export const updateDurum      = (id, body, token)       => apiFetch(`/api/hakedis/durum-guncelle/${id}`, { method: 'PATCH', body, token })
export const cancelHakedis    = (id, token)             => apiFetch(`/api/hakedis/sil/${id}`, { method: 'DELETE', token })
export const downloadPdf      = (id, token)             => apiBlob(`/api/hakedis/pdf/${id}`, token)
