from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..core.config import settings
from ..core.logger import logger
from ..models.user import Base  # 导入 Base

# 数据库连接配置
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,  # 连接池大小
    max_overflow=10,  # 最大溢出连接数
    pool_timeout=30,  # 连接超时时间
    pool_recycle=1800,  # 连接回收时间
    echo=True  # 临时开启SQL日志
)

try:
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    logger.debug("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")
    raise

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 