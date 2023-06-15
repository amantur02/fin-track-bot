from aiogram import Bot, Dispatcher, types
from .constants import TOKEN
from db.db_session import AsyncSessionLocal
from schemas import User
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from exception import AlreadyExistsException

from service.auth_services import create_user_wallet_services

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def with_db_session(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        async with AsyncSessionLocal() as db_session:
            return await func(message, db_session=db_session, *args, **kwargs)
    return wrapper


@dp.message_handler(commands=['start'])
@with_db_session
async def start_command(
        message: types.Message,
        db_session: AsyncSession
):
    try:
        # Get the user information
        username = message.from_user.username
        user_id = message.from_user.id

        user = User(
            username=username,
            telegram_id=user_id
        )

        await create_user_wallet_services(
            user_data=user, db_session=db_session
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="Welcome! Your user and wallet have been created."
        )
    except AlreadyExistsException as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text=e.message
        )
