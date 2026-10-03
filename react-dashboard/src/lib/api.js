export async function apiFetch(path, { method = 'GET', body, token, signal } = {}) {
  const init = {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(body !== undefined ? { 'Content-Type': 'application/json' } : {}),
    },
    ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
    ...(signal ? { signal } : {}),
  }
  const res = await fetch(path, init)
  if (res.status === 401) window.dispatchEvent(new Event('bai:unauthorized'))
  if (!res.ok) {
    let detail = `İstek başarısız (${res.status})`
    try { detail = (await res.json()).detail || detail } catch { /* */ }
    const err = new Error(detail)
    err.status = res.status
    throw err
  }
  return res.json()
}

export async function apiBlob(path, token, signal) {
  const res = await fetch(path, {
    headers: { Authorization: `Bearer ${token}` },
    ...(signal ? { signal } : {}),
  })
  if (!res.ok) {
    let detail = `İndirme başarısız (${res.status})`
    try { detail = (await res.json()).detail || detail } catch { /* */ }
    const err = new Error(detail)
    err.status = res.status
    throw err
  }
  return res.blob()
}
