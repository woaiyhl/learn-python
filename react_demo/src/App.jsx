import React, { useEffect, useState } from "react";
import { Layout, Button, message, Modal, Typography } from "antd";
import { PlusOutlined, UserOutlined } from "@ant-design/icons";
import { listStudents, createStudent, deleteStudent } from "./api/client.js";
import StudentList from "./components/StudentList.jsx";
import StudentForm from "./components/StudentForm.jsx";

const { Header, Content } = Layout;
const { Title } = Typography;

export default function App() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [messageApi, contextHolder] = message.useMessage();

  // 加载数据
  const refresh = async () => {
    setLoading(true);
    try {
      const data = await listStudents();
      setStudents(Array.isArray(data) ? data : []);
    } catch (e) {
      messageApi.error("加载学生列表失败");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  // 创建学生
  const handleCreate = async (payload) => {
    try {
      await createStudent(payload);
      messageApi.success("添加成功");
      setIsModalOpen(false); // 关闭弹窗
      await refresh(); // 刷新列表
    } catch (e) {
      messageApi.error("添加失败，请检查邮箱是否重复");
    }
  };

  // 删除学生
  const handleDelete = async (id) => {
    try {
      await deleteStudent(id);
      messageApi.success("删除成功");
      await refresh();
    } catch (e) {
      messageApi.error("删除失败");
    }
  };

  return (
    <Layout className="min-h-screen">
      {contextHolder}

      {/* 顶部导航 */}
      <Header className="flex items-center justify-between px-6 bg-white border-b border-gray-200">
        <div className="flex items-center gap-2 text-xl font-bold text-gray-800">
          <UserOutlined className="text-blue-600" />
          <span>学生管理系统</span>
        </div>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>
          添加学生
        </Button>
      </Header>

      {/* 主要内容区域 */}
      <Content className="p-6 max-w-5xl mx-auto w-full">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <div className="mb-4 flex items-center justify-between">
            <Title level={4} style={{ margin: 0 }}>
              学生列表
            </Title>
            <span className="text-gray-500">共 {students.length} 人</span>
          </div>

          <StudentList items={students} loading={loading} onDelete={handleDelete} />
        </div>
      </Content>

      {/* 添加学生弹窗 */}
      <Modal
        title="添加新学生"
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null} // 让 Form 组件自己控制按钮
        destroyOnClose
      >
        <StudentForm onSubmit={handleCreate} />
      </Modal>
    </Layout>
  );
}
