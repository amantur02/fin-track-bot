from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

async_engine = create_async_engine(
    settings.postgres_async_url,
    pool_pre_ping=True,
    pool_size=settings.async_pool_size,
    pool_recycle=settings.async_pool_recycle,
    max_overflow=settings.async_max_overflow,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)
