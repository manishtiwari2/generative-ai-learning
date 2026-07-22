import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OpenAI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize modern OpenAI client (No more openai.api_key assignment)
ai_client = OpenAI(api_key=OPENAI_API_KEY)
model_name = "gpt-3.5-turbo"


class Reference:
    """A class to store the previous response from the openai API."""

    def __init__(self) -> None:
        self.response = ""


reference = Reference()

# Initialize bot and dispatcher for aiogram v3
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


def clear_past():
    """A function to clear the previous conversation and context."""
    reference.response = ""


@dp.message(Command("clear"))
async def clear(message: types.Message):
    """A handler to clear the previous conversation and context."""
    clear_past()
    await message.reply("I've cleared the past conversation and context.")


@dp.message(Command("start"))
async def welcome(message: types.Message):
    """This handler receives messages with /start command."""
    await message.reply(
        "Hi\nI am Prince's Tele Bot!\nCreated by Manish Tiwari. How can I assist you?"
    )


@dp.message(Command("help"))
async def helper(message: types.Message):
    """A handler to display the help menu."""
    help_command = """
    Hi There, I'm Telegram bot created by Manish Tiwari! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


@dp.message()
async def chatgpt(message: types.Message):
    """A handler to process user input and generate a response using the modern OpenAI client."""
    if not message.text:
        return

    print(f">>> USER: \n\t{message.text}")

    # Build conversation payload dynamically
    messages_payload = []
    if reference.response:
        messages_payload.append(
            {"role": "assistant", "content": reference.response}
        )
    messages_payload.append({"role": "user", "content": message.text})

    try:
        # Replaced deprecated openai.ChatCompletion.create()
        response = ai_client.chat.completions.create(
            model=model_name, messages=messages_payload
        )

        # Access data using modern object notation instead of dictionary brackets
        reference.response = response.choices[0].message.content

        print(f">>> chatGPT: \n\t{reference.response}")
        await message.answer(text=reference.response)

    except Exception as e:
        logging.error(f"OpenAI Error: {e}")
        await message.answer(
            "Sorry, I encountered an issue processing that request."
        )


async def main():
    # Clear old webhooks/pending updates before initializing polling loop
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
