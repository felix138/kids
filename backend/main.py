import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import education
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 检查必要的环境变量
required_env_vars = ["GROK_API_KEY", "GROK_API_BASE"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

app = FastAPI(title="AI Utdanningsassistent for Barn")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(education.router, prefix="/api/education", tags=["education"])

@app.get("/")
async def root():
    return {"message": "Velkommen til AI Utdanningsassistent for Barn API"} 