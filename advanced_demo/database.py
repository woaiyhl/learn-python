from sqlalchemy import create_engine  # 导入 create_engine 用于创建数据库连接引擎
from sqlalchemy.ext.declarative import (
    declarative_base,
)  # 导入 declarative_base 用于创建 ORM 模型的基类
from sqlalchemy.orm import sessionmaker  # 导入 sessionmaker 用于创建数据库会话工厂

# 数据库文件路径，这里使用 SQLite
# SQLite 是一个轻量级的基于文件的数据库，非常适合开发和测试
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# 如果使用 PostgreSQL，链接格式如下：
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# 创建数据库引擎
# engine 是 SQLAlchemy 与数据库交互的核心接口
# connect_args={"check_same_thread": False} 仅用于 SQLite
# 因为 SQLite 默认只允许创建连接的线程使用该连接，而 FastAPI 是多线程的
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建 SessionLocal 类
# 这是一个工厂类，每次调用 SessionLocal() 都会返回一个新的数据库会话 (Session) 对象
# autocommit=False: 禁止自动提交事务，需要手动 commit，保证数据一致性
# autoflush=False: 禁止自动刷新，即在查询前不自动将变更同步到数据库
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 Base 类
# 所有的数据库模型 (Model) 类都必须继承自这个 Base 类
# 这样 SQLAlchemy 才能知道哪些类是数据库表
Base = declarative_base()
