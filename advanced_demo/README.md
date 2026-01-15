# advanced_demo 项目说明

这个目录是一个用于学习的 FastAPI + SQLAlchemy + JWT 认证示例项目，包含：

- 用户注册、登录
- JWT（JSON Web Token）认证
- 文章的基础 CRUD（创建/读取）

## 文件结构与职责

| 文件               | 主要职责                                                                                                | 你应该重点关注什么                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `main.py`          | 应用入口：创建 FastAPI 实例、定义路由、组装依赖（数据库会话、当前用户）、实现登录认证流程               | `Depends`（依赖注入）、`OAuth2PasswordBearer`、`get_current_user` 如何从请求头拿到 Token 并校验 |
| `database.py`      | 数据库基础设施：创建数据库引擎 `engine`、会话工厂 `SessionLocal`、声明式基类 `Base`                     | `engine / SessionLocal / Base` 三件套分别解决“连库 / 开会话 / 定义模型”                         |
| `models.py`        | 数据库模型（ORM）：定义 `User`、`Post` 两张表及它们的关系                                               | `Column` 字段定义、`ForeignKey` 外键、`relationship` 关系映射、`back_populates` 双向关联        |
| `schemas.py`       | API 数据模型（Pydantic）：定义请求体/响应体结构，如 `UserCreate`、`User`、`PostCreate`、`Post`、`Token` | “请求用什么结构、响应返回什么结构”，以及 `from_attributes=True`（从 ORM 对象取值）              |
| `crud.py`          | 数据访问层：封装对数据库的增删改查（本项目主要是用户与文章的查询、创建）                                | `db.add/commit/refresh` 的意义，查询链式调用 `query/filter/first/all`                           |
| `utils.py`         | 安全与认证工具：密码哈希、密码校验、JWT Token 生成                                                      | `bcrypt` 哈希、`verify_password`、`create_access_token` 的 payload/exp 字段                     |
| `requirements.txt` | 依赖清单：用于安装项目所需第三方库                                                                      | 每个依赖在项目中对应的用途（FastAPI、SQLAlchemy、Pydantic、jose、passlib 等）                   |

## 模块关系（建议按这个顺序理解）

1. `database.py` 提供数据库连接与会话
2. `models.py` 用 `Base` 定义表结构
3. `schemas.py` 定义 API 的入参/出参数据结构
4. `utils.py` 提供密码与 JWT 工具
5. `crud.py` 用 `Session` 操作 `models`，并接收/返回 `schemas`
6. `main.py` 把以上全部“串起来”，对外提供 HTTP API

## 快速运行（可选）

在上级目录（包含 `advanced_demo/` 的目录）执行：

```bash
pip install -r advanced_demo/requirements.txt
uvicorn advanced_demo.main:app --reload
```

启动后访问：

- Swagger 文档：`http://127.0.0.1:8000/docs`
- Apifox 项目：`https://app.apifox.com/project/7688079`
