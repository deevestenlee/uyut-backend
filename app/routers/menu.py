from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Product

router = APIRouter(prefix="/api/menu", tags=["Menu"])


@router.get("")
async def get_menu(session: AsyncSession = Depends(get_db)):
    stmt = (
        select(Product)
        .where(Product.is_active.is_(True))
        .options(selectinload(Product.variants))
    )
    result = await session.execute(stmt)
    products = result.scalars().unique().all()
    return products
