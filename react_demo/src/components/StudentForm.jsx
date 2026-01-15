import React, { useState } from 'react'

export default function StudentForm({ onSubmit }) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [age, setAge] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    const payload = {
      name: name?.trim(),
      email: email?.trim(),
      age: age ? Number(age) : null,
    }
    onSubmit?.(payload)
    setName('')
    setEmail('')
    setAge('')
  }

  return (
    <form className="bg-white rounded-md shadow p-4" onSubmit={handleSubmit}>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <input
          className="border rounded px-3 py-2"
          placeholder="姓名"
          value={name ?? ''}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          className="border rounded px-3 py-2"
          placeholder="邮箱"
          value={email ?? ''}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="border rounded px-3 py-2"
          placeholder="年龄"
          type="number"
          value={age ?? ''}
          onChange={(e) => setAge(e.target.value)}
        />
      </div>
      <div className="mt-3">
        <button className="bg-blue-600 text-white px-4 py-2 rounded">添加</button>
      </div>
    </form>
  )
}

