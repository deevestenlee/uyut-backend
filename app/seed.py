import asyncio import logging from sqlalchemy import delete
from app.database import AsyncSessionLocal, engine, Base from app.models import RestaurantSettings, Category, Product, ProductOption
logging.basicConfig(level=logging.INFO) log = logging.getLogger("seed")
RESTAURANT_DATA = { "name": "Кафе «Уют»", "currency_symbol": "₩", "phone": "+82-10-8765-4321", "address": "Incheon, Yeonsu-gu, Hambak-mweol", "min_order_amount": 15000, }
MENU_DATA = [ { "category": {"name": "Восточная кухня", "sort_order": 1}, "products": [ { "title": "Узбекский Плов", "description": "Рассыпчатый плов с бараниной и специями", "is_spicy": False, "badge": "ХИТ", "is_available": True, "options": [("Стандартная", 12000), ("Большая", 16000)], }, { "title": "Лагман Уйгурский", "description": "Тянутая лапша с говядиной в остром соусе", "is_spicy": True, "badge": None, "is_available": True, "options": [("Порция", 11000)], }, ], }, { "category": {"name": "Русская кухня", "sort_order": 2}, "products": [ { "title": "Борщ Домашний", "description": "Наваристый борщ со сметаной", "is_spicy": False, "badge": "ПОПУЛЯРНОЕ", "is_available": True, "options": [("С говядиной", 10000)], }, { "title": "Пельмени Сибирские", "description": "Ручная лепка, подаются со сметаной", "is_spicy": False, "badge": None, "is_available": True, "options": [("Порция", 9000), ("Двойная", 15000)], }, ], }, ]
async def seed(): async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
async with AsyncSessionLocal() as session:
    try:
        await session.execute(delete(ProductOption))
        await session.execute(delete(Product))
        await session.execute(delete(Category))
        await session.execute(delete(RestaurantSettings))

        settings = RestaurantSettings(**RESTAURANT_DATA)
        session.add(settings)
        await session.flush()

        for block in MENU_DATA:
            category = Category(**block["category"])
            session.add(category)
            await session.flush()

            for p in block["products"]:
                p_copy = p.copy()
                options_data = p_copy.pop("options")
                product = Product(category_id=category.id, **p_copy)
                session.add(product)
                await session.flush()

                for opt_name, opt_price in options_data:
                    session.add(ProductOption(product_id=product.id, name=opt_name, price=opt_price))

        await session.commit()
        log.info("Готово. Тестовые данные Кафе «Уют» успешно загружены ✅")
    except Exception:
        await session.rollback()
        raise
if name == "main": asyncio.run(seed())