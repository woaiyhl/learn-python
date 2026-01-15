from datetime import datetime, timedelta  # 用于处理时间和时间间隔
from typing import Optional  # Optional 表示“可选类型”，用于标注参数/字段允许为 None
from jose import jwt  # python-jose 库，用于生成和解码 JWT (JSON Web Token)
from passlib.context import CryptContext  # passlib 库，用于密码哈希处理

# 密钥配置 (注意：在真实生产环境中，绝对不能硬编码在代码里！应该从环境变量读取)
# 可以使用 os.getenv("SECRET_KEY") 获取
SECRET_KEY = "your-secret-key-keep-it-secret"
ALGORITHM = "HS256"  # JWT 签名算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token 过期时间（分钟）

# 创建密码哈希上下文
# schemes=["bcrypt"]: 指定使用 bcrypt 算法进行哈希，这是一种非常安全的哈希算法
# deprecated="auto": 自动处理废弃的哈希方案
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    验证密码是否匹配
    plain_password: 用户输入的明文密码
    hashed_password: 数据库中存储的哈希密码
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    生成密码哈希值
    将明文密码转换为乱码般的哈希字符串，存入数据库
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    生成 JWT 访问令牌
    data: 要包含在 Token 中的数据（Payload）
    expires_delta: 过期时间间隔
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # 默认过期时间为 15 分钟
        expire = datetime.utcnow() + timedelta(minutes=15)

    # 将过期时间添加到 Payload 中，字段名为 "exp" (JWT 标准字段)
    to_encode.update({"exp": expire})

    # 使用密钥和指定算法对数据进行签名，生成 Token 字符串
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
