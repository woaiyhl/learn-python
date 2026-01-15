const base = import.meta.env?.VITE_API_BASE ?? 'http://127.0.0.1:8001'

const json = async (res) => {
  const ct = res.headers?.get('content-type') ?? ''
  if (!ct.includes('application/json')) return null
  return res.json()
}

export const listStudents = async () => {
  const r = await fetch(`${base}/students`)
  if (!r.ok) throw new Error('bad_response')
  return json(r)
}

export const createStudent = async (payload) => {
  const r = await fetch(`${base}/students`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload ?? {}),
  })
  if (!r.ok) throw new Error('bad_response')
  return json(r)
}

export const deleteStudent = async (id) => {
  const r = await fetch(`${base}/students/${id}`, { method: 'DELETE' })
  if (!r.ok) throw new Error('bad_response')
  return json(r)
}

