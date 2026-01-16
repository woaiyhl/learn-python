import os

# dotenv 用于从 .env 文件中加载环境变量，方便管理敏感配置
# python-dotenv 文档：https://github.com/theskumar/python-dotenv
from dotenv import load_dotenv

# SQLAlchemy 是 Python 主流 ORM/数据库工具，提供统一的数据库访问接口
# 官方文档：https://docs.sqlalchemy.org/
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# 从项目根目录的 .env 文件读取数据库连接配置
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "learn_mysql")


# 使用 SQLAlchemy 的 URL 形式配置 MySQL 连接
# "mysql+pymysql" 表示使用 PyMySQL 作为 MySQL 数据库驱动
# PyMySQL 文档：https://pymysql.readthedocs.io/
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"


# create_engine 创建数据库引擎对象，负责管理底层连接池
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True)


# sessionmaker 是会话工厂，用来创建数据库会话（Session）实例
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base 是所有 ORM 模型需要继承的基类
Base = declarative_base()
