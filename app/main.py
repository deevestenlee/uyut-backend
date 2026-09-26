from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import public, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Асинхронное создание таблиц при старте приложения
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Bakery API", lifespan=lifespan)

# Подключение роутеров
app.include_router(public.router)
app.include_router(admin.router, prefix="/admin")


@app.get("/")
async def root():
    return {"message": "Uyut Bakery API is running"}
