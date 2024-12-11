from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# URL для подключения к PostgreSQL (используем asyncpg для асинхронности)
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/audio_db"

# Создание асинхронного engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика для создания асинхронных сессий
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# Асинхронный генератор сессий
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
