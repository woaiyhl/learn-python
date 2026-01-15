import React, { useEffect, useState } from 'react'
import { listStudents, createStudent, deleteStudent } from './api/client.js'
import StudentList from './components/StudentList.jsx'
import StudentForm from './components/StudentForm.jsx'

export default function App() {
  const [students, setStudents] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const refresh = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await listStudents()
      setStudents(Array.isArray(data) ? data : [])
    } catch (e) {
      setError('加载失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refresh()
  }, [])

  const handleCreate = async (payload) => {
    try {
      await createStudent(payload)
      await refresh()
    } catch {
      setError('创建失败')
    }
  }

  const handleDelete = async (id) => {
    try {
      await deleteStudent(id)
      await refresh()
    } catch {
      setError('删除失败')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto p-6">
        <h1 className="text-2xl font-semibold mb-4">学生管理</h1>
        {error ? <div className="text-red-600 mb-3">{error}</div> : null}
        <StudentForm onSubmit={handleCreate} />
        <div className="mt-6">
          {loading ? (
            <div className="text-gray-500">加载中...</div>
          ) : (
            <StudentList items={students} onDelete={handleDelete} />
          )}
        </div>
      </div>
    </div>
  )
}

