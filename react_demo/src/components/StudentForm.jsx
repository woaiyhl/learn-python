import React, { useState } from "react";
import { Form, Input, InputNumber, Button } from "antd";

export default function StudentForm({ onSubmit }) {
  const [form] = Form.useForm();
  const [submitting, setSubmitting] = useState(false);

  const onFinish = async (values) => {
    setSubmitting(true);
    try {
      await onSubmit?.(values);
      form.resetFields();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Form form={form} layout="vertical" onFinish={onFinish} initialValues={{ age: 18 }}>
      <Form.Item
        label="姓名"
        name="name"
        rules={[
          { required: true, message: "请输入学生姓名" },
          { max: 50, message: "姓名不能超过 50 个字符" },
        ]}
      >
        <Input placeholder="例如：张三" />
      </Form.Item>

      <Form.Item
        label="邮箱"
        name="email"
        rules={[
          { required: true, message: "请输入邮箱" },
          { type: "email", message: "请输入有效的邮箱地址" },
        ]}
      >
        <Input placeholder="example@domain.com" />
      </Form.Item>

      <Form.Item
        label="年龄"
        name="age"
        rules={[{ type: "number", min: 1, max: 150, message: "年龄必须在 1-150 之间" }]}
      >
        <InputNumber style={{ width: "100%" }} placeholder="可选" />
      </Form.Item>

      <Form.Item className="mb-0 text-right">
        <Button type="primary" htmlType="submit" loading={submitting}>
          提交保存
        </Button>
      </Form.Item>
    </Form>
  );
}
