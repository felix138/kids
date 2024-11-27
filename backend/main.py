from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import education

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