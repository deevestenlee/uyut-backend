from fastapi import APIRouter, Depends, HTTPException, status from sqlalchemy import select from sqlalchemy.ext.asyncio import AsyncSession from sqlalchemy.orm import selectinload
from app.database import get_session from app.models import RestaurantSettings, Category, Product from app.schemas import InitResponse, RestaurantSettingsPublic, CategoryWithProducts
router = APIRouter(prefix="/api/v1", tags=["Public"])
@router.get("/init", response_model=InitResponse) async def init_client(session: AsyncSession = Depends(get_session)): res_settings = await session.execute(select(RestaurantSettings).limit(1)) settings = res_settings.scalar_one_or_none() if not settings: raise HTTPException(status_code=404, detail="Настройки не найдены")
stmt = (
    select(Category)
    .options(
        selectinload(Category.products.and_(Product.is_available.is_(True)))
        .selectinload(Product.options)
    )
    .order_by(Category.sort_order, Category.id)
)
res_cats = await session.execute(stmt)
categories = list(res_cats.scalars().unique().all())

return InitResponse(
    settings=RestaurantSettingsPublic.model_validate(settings),
    categories=[CategoryWithProducts.model_validate(c) for c in categories],
)