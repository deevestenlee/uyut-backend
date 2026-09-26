from fastapi import FastAPI from fastapi.middleware.cors import CORSMiddleware from app.routers import public, admin
app = FastAPI(title="Uyut Bakery API")
app.add_middleware( CORSMiddleware, allow_origins=[""], allow_credentials=True, allow_methods=[""], allow_headers=["*"], )
app.include_router(public.router, prefix="/api/v1") app.include_router(admin.router, prefix="/api/v1/admin")
@app.get("/") def root(): return {"message": "Uyut Bakery API is running"}
