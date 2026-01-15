import React from 'react'

export default function StudentList({ items, onDelete }) {
  const list = Array.isArray(items) ? items : []
  return (
    <div className="bg-white rounded-md shadow">
      <table className="w-full text-left">
        <thead>
          <tr className="border-b">
            <th className="p-3">ID</th>
            <th className="p-3">姓名</th>
            <th className="p-3">邮箱</th>
            <th className="p-3">年龄</th>
            <th className="p-3">操作</th>
          </tr>
        </thead>
        <tbody>
          {list.length === 0 ? (
            <tr>
              <td className="p-3 text-gray-500" colSpan={5}>暂无数据</td>
            </tr>
          ) : (
            list.map((s) => (
              <tr key={s?.id} className="border-b">
                <td className="p-3">{s?.id ?? ''}</td>
                <td className="p-3">{s?.name ?? ''}</td>
                <td className="p-3">{s?.email ?? ''}</td>
                <td className="p-3">{s?.age ?? ''}</td>
                <td className="p-3">
                  <button
                    className="text-red-600 hover:underline"
                    onClick={() => onDelete?.(s?.id)}
                  >
                    删除
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}

