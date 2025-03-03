from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.api.endpoints import auth, templates, games, discord
from app.core.middleware import LoggingMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for FlorisBoard Game and Discord Enhancement",
    version="0.1.0",
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

# 包含路由
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(templates.router, prefix=settings.API_V1_STR)
app.include_router(games.router, prefix=settings.API_V1_STR)
app.include_router(discord.router, prefix=settings.API_V1_STR)

# 启动事件
@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to FlorisBoard Enhancement API"}

@app.get("/health")
async def health():
    return {"status": "ok"}