import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import Base, engine

# Импортируем роутеры напрямую из их файлов (без использования __init__.py)
from app.routers.admin import router as admin_router
from app.routers.menu import router as menu_router
from app.routers.orders import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Cafe Mini App API",
    version="1.0.0",
    lifespan=lifespan,
)

# Подключаем роутеры
app.include_router(menu_router)
app.include_router(orders_router)
app.include_router(admin_router)

# Раздача визуальной части (статического фронтенда)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"status": "ok", "message": "API is running"}


@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok"}
