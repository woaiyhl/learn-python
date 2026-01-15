import React from "react";
import { Table, Button, Popconfirm, Tag } from "antd";
import { DeleteOutlined } from "@ant-design/icons";

export default function StudentList({ items, loading, onDelete }) {
  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      width: 80,
    },
    {
      title: "姓名",
      dataIndex: "name",
      key: "name",
      render: (text) => <span className="font-medium">{text}</span>,
    },
    {
      title: "邮箱",
      dataIndex: "email",
      key: "email",
    },
    {
      title: "年龄",
      dataIndex: "age",
      key: "age",
      render: (age) => (age ? <Tag color="blue">{age} 岁</Tag> : <Tag color="default">-</Tag>),
    },
    {
      title: "操作",
      key: "action",
      render: (_, record) => (
        <Popconfirm
          title="确认删除"
          description={`确定要删除学生 "${record.name}" 吗？`}
          onConfirm={() => onDelete?.(record.id)}
          okText="删除"
          cancelText="取消"
          okButtonProps={{ danger: true }}
        >
          <Button type="text" danger icon={<DeleteOutlined />} size="small">
            删除
          </Button>
        </Popconfirm>
      ),
    },
  ];

  return (
    <Table
      rowKey="id"
      columns={columns}
      dataSource={items}
      loading={loading}
      pagination={{
        pageSize: 5,
        showTotal: (total) => `共 ${total} 条数据`,
      }}
    />
  );
}
