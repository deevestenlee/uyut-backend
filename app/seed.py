import asyncio
import logging
from sqlalchemy import delete
from app.database import engine, Base, AsyncSessionLocal
from app.models import Product, ProductVariant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await session.execute(delete(ProductVariant))
        await session.execute(delete(Product))
        await session.commit()

        tartin = Product(
            code="001",
            title="Тартин",
            description="Тонкая корка с характерным хрустом, открытый упругий мякиш.",
            image="https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800",
            badge="ХИТ",
        )
        session.add(tartin)
        await session.flush()

        v1 = ProductVariant(product_id=tartin.id, size="S", price=350)
        v2 = ProductVariant(product_id=tartin.id, size="L", price=550)
        session.add_all([v1, v2])

        tomato = Product(
            code="007",
            title="С вялеными томатами и базиликом",
            description="Вяленые томаты дают умами и легкую сладость, базилик — свежесть.",
            image="https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=800",
            badge="РЕКОМЕНДАЦИЯ",
        )
        session.add(tomato)
        await session.flush()

        v3 = ProductVariant(product_id=tomato.id, size="S", price=700)
        v4 = ProductVariant(product_id=tomato.id, size="L", price=1100)
        session.add_all([v3, v4])

        await session.commit()
        logger.info("Данные успешно добавлены в базу!")


if __name__ == "__main__":
    asyncio.run(seed_data())
