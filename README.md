# learn-python

一个包含 Python 学习脚本与 FastAPI + SQLAlchemy + JWT 示例的仓库。示例项目位于 `advanced_demo/` 目录。

## 环境要求
- Python 3.9+
- 建议使用虚拟环境（venv）进行依赖隔离

## 快速运行（FastAPI 示例）
在仓库根目录执行：

```bash
pip install -r advanced_demo/requirements.txt
python -m uvicorn advanced_demo.main:app --reload --host 127.0.0.1 --port 8000
```

启动后访问：
- Swagger 文档：`http://127.0.0.1:8000/docs`
- OpenAPI 文档：`http://127.0.0.1:8000/openapi.json`

## Apifox 对接
- 前置 URL：`http://127.0.0.1:8000`（不要加 /docs）
- 导入方式：在 Apifox 选择“导入 → OpenAPI/Swagger → 通过 URL 导入”，填 `http://127.0.0.1:8000/openapi.json`
- 项目链接：`https://app.apifox.com/project/7688079`

常用接口（示例）：
- POST `/users/` 注册用户（Body：JSON，包含 email、password）
- POST `/token` 登录获取 JWT（Body：x-www-form-urlencoded，字段 username、password；其中 username 即 email）
- GET `/users/me` 获取当前用户信息（需在请求头携带 `Authorization: Bearer <token>`）
- POST `/users/me/posts/` 发布文章（需鉴权）
- GET `/posts/` 获取文章列表（公开接口）

## 目录说明
- [advanced_demo](file:///Users/luhuawei/Documents/后端/python/advanced_demo) 示例项目根目录
  - [main.py](file:///Users/luhuawei/Documents/后端/python/advanced_demo/main.py) 应用入口与路由
  - [database.py](file:///Users/luhuawei/Documents/后端/python/advanced_demo/database.py) 连接与会话
  - [models.py](file:///Users/luhuawei/Documents/后端/python/advanced_demo/models.py) ORM 模型
  - [schemas.py](file:///Users/luhuawei/Documents/后端/python/advanced_demo/schemas.py) Pydantic 模型
  - [crud.py](file:///Users/luhuawei/Documents/后端/python/advanced_demo/crud.py) 数据访问封装
  - [utils.py](file:///Users/luhuawei/Documents/后端/python/advanced_demo/utils.py) 密码与 JWT 工具
  - [README.md](file:///Users/luhuawei/Documents/后端/python/advanced_demo/README.md) 示例项目说明

## 本地开发建议
- 端口占用时可改为 `--port 8001` 并对应访问 `http://127.0.0.1:8001`
- Apifox 鉴权：在“环境设置 → 全局请求头”添加 `Authorization: Bearer <access_token>`，或在接口“鉴权”选择 Bearer 并填入 Token

## 安全与配置
- 示例中的 `SECRET_KEY` 仅用于演示，生产环境务必改为从环境变量读取（例如 `.env` 或系统环境变量），避免硬编码密钥进入仓库
- 仓库已配置 `.gitignore`，默认忽略 venv、缓存与本地数据库文件（如 `*.db`）

## 常见问题
- 401 未授权：检查是否携带 `Authorization: Bearer <token>`，以及 Token 是否过期
- 422 校验失败：确认请求体字段名与类型与 `schemas.py` 定义一致
- 访问不到 `/openapi.json`：确认服务已启动并端口正确；必要时调整端口后在 Apifox 重新导入
