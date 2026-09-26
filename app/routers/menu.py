from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.models import Category, Dish
from app.schemas import CategoryOut

router = APIRouter(prefix="/api/menu", tags=["Menu"])


@router.get("", response_model=list[CategoryOut])
async def get_menu(session: AsyncSession = Depends(get_session)):
    stmt = (
        select(Category)
        .where(Category.is_active.is_(True))
        .order_by(Category.position, Category.id)
        .options(
            selectinload(Category.dishes.and_(Dish.is_available.is_(True)))
            .selectinload(Dish.options)
        )
    )
    result = await session.execute(stmt)
    return list(result.scalars().unique().all())
