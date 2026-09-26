[26.09.2026 23:20] Dmitriy: import os from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker from sqlalchemy.orm import declarative_base
DATABASE_URL = os.getenv("DATABASE_URL")
Преобразуем postgresql:// в postgresql+asyncpg:// если требуется
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"): DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker( bind=engine, class_=AsyncSession, expire_on_commit=False )
Base = declarative_base()
async def get_db(): async with AsyncSessionLocal() as session: try: yield session finally: await session.close()
[26.09.2026 23:40] Dmitriy: import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
