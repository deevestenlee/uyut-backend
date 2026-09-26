from fastapi import APIRouter, Depends, HTTPException, status from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session from app.dependencies import require_admin from app.models import Product, ProductOption from app.schemas import OptionPriceUpdate, ProductAvailabilityUpdate, ProductOptionAdmin, ProductAdminShort
router = APIRouter(prefix="/api/v1/admin", tags=["Admin"], dependencies=[Depends(require_admin)])
@router.patch("/options/{option_id}/price", response_model=ProductOptionAdmin) async def update_option_price(option_id: int, payload: OptionPriceUpdate, session: AsyncSession = Depends(get_session)): option = await session.get(ProductOption, option_id) if not option: raise HTTPException(status_code=404, detail="Опция не найдена") option.price = payload.price await session.commit() await session.refresh(option) return ProductOptionAdmin.model_validate(option)
@router.patch("/products/{product_id}/toggle-availability", response_model=ProductAdminShort) async def toggle_product_availability(product_id: int, payload: ProductAvailabilityUpdate | None = None, session: AsyncSession = Depends(get_session)): product = await session.get(Product, product_id) if not product: raise HTTPException(status_code=404, detail="Блюдо не найдено")
product.is_available = payload.is_available if payload else not product.is_available
await session.commit()
await session.refresh(product)
return ProductAdminShort.model_validate(product)