import os
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import select, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload

# 1. БАЗА ДАННЫХ
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    DATABASE_URL, 
    echo=False,
    connect_args={"prepared_statement_cache_size": 0}
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# 2. МОДЕЛИ (БД)
class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)
    badge: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    variants: Mapped[List["ProductVariant"]] = relationship(back_populates="product", cascade="all, delete-orphan")

class ProductVariant(Base):
    __tablename__ = "product_variants"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    size: Mapped[str] = mapped_column(String)  # S / L
    price: Mapped[float] = mapped_column(Float)
    product: Mapped["Product"] = relationship(back_populates="variants")

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    delivery_date: Mapped[str] = mapped_column(String)
    total_price: Mapped[float] = mapped_column(Float)

# 3. СХЕМЫ (Pydantic)
class VariantOut(BaseModel):
    id: int
    size: str
    price: float
    class Config:
        from_attributes = True

class ProductOut(BaseModel):
    id: int
    code: str
    title: str
    description: str
    image: str
    badge: Optional[str]
    variants: List[VariantOut]
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    delivery_date: str
    total_price: float

# 4. ПРИЛОЖЕНИЕ & ЭНДПОИНТЫ
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Bakery API", lifespan=lifespan)

@app.get("/api/menu", response_model=List[ProductOut])
async def get_menu(db: AsyncSession = Depends(get_db)):
    stmt = select(Product).where(Product.is_active.is_(True)).options(selectinload(Product.variants))
    result = await db.execute(stmt)
    return result.scalars().unique().all()

@app.post("/api/orders")
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    new_order = Order(**order_data.model_dump())
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return {"status": "success", "order_id": new_order.id}

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"status": "ok", "message": "Bakery API is running"}
