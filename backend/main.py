import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import education, auth
from app.middleware.auth import AuthMiddleware
from app.core.config import settings
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()

app = FastAPI(title="AI Utdanningsassistent for Barn")

# 配置CORS - 修改这部分
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.40:3000",
    "http://localhost:8000",
    "http://192.168.1.40:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600
)

# 添加认证中间件
app.middleware("http")(AuthMiddleware())

# 添加路由
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(education.router, prefix="/api/education", tags=["education"])

# 设置特定模块的日志级别
logging.getLogger("passlib").setLevel(logging.ERROR)
logging.getLogger("python_multipart").setLevel(logging.WARNING)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 