from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_async_url: str = (
        "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/fin_track"
    )
    postgres_url: str = "postgresql://postgres:postgres@127.0.0.1:5432/fin_track"
    SQLALCHEMY_DATABASE_URI = postgres_url

    async_pool_size: int = 5
    async_max_overflow: int = 0
    async_pool_recycle: int = -1

    sync_pool_size: int = 5
    sync_max_overflow: int = 0
    sync_pool_recycle: int = -1


settings = Settings()
