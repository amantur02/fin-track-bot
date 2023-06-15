from aiogram import executor
from bot.bot import dp
from db.db_models import Base
from config import settings
from sqlalchemy import create_engine

engine = create_engine(settings.postgres_url)
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
