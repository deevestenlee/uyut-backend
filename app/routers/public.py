from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import Product

router = APIRouter(tags=["Public API"])


@router.get("/products")
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product).options(selectinload(Product.variants)).where(Product.is_active == True)
    )
    products = result.scalars().all()
    return products


@router.get("/products/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product).options(selectinload(Product.variants)).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
