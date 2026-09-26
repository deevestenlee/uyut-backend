from fastapi import FastAPI from fastapi.middleware.cors import CORSMiddleware from app.routers import public, admin
app = FastAPI(title="Uyut Cafe API")
Разрешаем запросы с любого фронтенда
app.add_middleware( CORSMiddleware, allow_origins=[""], allow_credentials=True, allow_methods=[""], allow_headers=["*"], )
app.include_router(public.router) app.include_router(admin.router)
@app.get("/health") async def health(): return {"status": "ok"}