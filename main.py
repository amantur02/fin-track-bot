from aiogram import executor
from bot import dp
from db_models import Base
from config import DB_URL
from sqlalchemy import create_engine

engine = create_engine(DB_URL)
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
