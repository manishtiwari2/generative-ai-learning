import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
# Note: In v3, Dispatcher handles multiple bots, so do not pass "bot" into Dispatcher()
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


# Handler for /start and /help commands
@dp.message(Command("start", "help"))
async def command_start_handler(message: types.Message):
    """This handler receives messages with /start or /help command."""
    await message.reply("Hi\nI am Echo Bot!\nPowered by Manish Tiwari.")


# Handler for all other text messages (Echo)
@dp.message()
async def echo(message: types.Message):
    """This will return echo."""
    # Check if the message contains text to prevent errors with images/stickers
    if message.text:
        await message.answer(message.text)


# Main asynchronous entry point replacing executor
async def main():
    # skip_updates=True is replaced by deleting pending updates before polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
