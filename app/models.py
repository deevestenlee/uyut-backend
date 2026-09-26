from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import public, admin
from app.seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Асинхронно создаем все таблицы в базе данных при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Наполняем базу начальными данными (хлебом)
    try:
        await seed_data()
    except Exception as e:
        print(f"Seed info: {e}")

    yield


app = FastAPI(title="Bakery API", lifespan=lifespan)

# Подключаем роутеры
app.include_router(public.router)
app.include_router(admin.router, prefix="/admin")


@app.get("/")
async def root():
    return {"message": "Welcome to Bakery API"}
