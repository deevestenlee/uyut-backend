from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.database import Base, engine
from app.routers import admin, menu, orders

app = FastAPI(title="Cafe Mini App")

# Подключаем роутеры API
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(admin.router)

# Подключаем папку со статикой (визуалом)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    # Главная страница с визуалом
    return FileResponse("static/index.html")
