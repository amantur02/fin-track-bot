from aiogram import Bot, Dispatcher, types
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Get the user information
    username = message.from_user.username
    user_id = message.from_user.id

    # Create the user and wallet in the database
    await create_user_and_wallet(username, user_id, phone)

    # Send a welcome message to the user
    await message.reply("Welcome! Your user and wallet have been created.")

