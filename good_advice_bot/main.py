import asyncio
import logging
import os
import sys
from enum import StrEnum

from aiogram import Bot, Dispatcher, F
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from asyncpg import Record
from db import DB
from dotenv import load_dotenv

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(name)s:%(lineno)s:%(message)s",
    level="DEBUG",
)
logging.getLogger("asyncio").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

DB_USER = os.environ["DB_USER"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USER_PASSWORD = os.environ["DB_USER_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]


bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher()

db = DB(
    user=DB_USER,
    host=DB_HOST,
    port=DB_PORT,
    password=DB_USER_PASSWORD,
    database=DB_NAME,
)


class ButtonText(StrEnum):
    GET_A_RANDOM_NOTE = "Get a random note"


GET_A_RANDOM_NOTE_BUTTON = KeyboardButton(text="Get a random note")
DEFAULT_KEYBOARD = ReplyKeyboardMarkup(keyboard=[[GET_A_RANDOM_NOTE_BUTTON]])


async def get_random_row() -> Record:
    """Get a random row from a note table."""
    async with db.get_connection() as conn:
        result = await conn.fetchrow(
            """
        SELECT
            notes.id,
            notes.text AS note,
            notes.additional_info AS info,
            topics.text AS topic,
            authors.name AS author
        FROM notes
        LEFT JOIN authors ON authors.id = notes.author_id
        JOIN notes_topics ON notes.id = public.notes_topics.note_id
        JOIN topics ON notes_topics.topic_id = topics.id
        ORDER BY random() limit 1;
        """,
        )
    return result


async def shutdown_bot() -> None:
    """Gracefully shutdown db pool and Telegram dispatcher."""
    await db.close()
    dispatcher.shutdown()


async def get_a_random_note() -> str:
    """Get a formatted string with a random note."""
    random_line = await get_random_row()
    note = random_line["note"]
    topic = random_line["topic"]
    author = random_line["author"]
    info = random_line["info"]
    reply = f"Note: {note}\nTopic: {topic}\nAuthor: {author}"
    if info:
        reply = f"{reply}\nAdditional info: {info}"
    return reply


@dispatcher.message(F.text == ButtonText.GET_A_RANDOM_NOTE)
async def reply_get_a_random_note(message: Message) -> None:
    logger.info("Got a new message from chat id %d", message.chat.id)
    reply = await get_a_random_note()

    await message.answer(
        text=reply,
        reply_markup=DEFAULT_KEYBOARD,
    )
    logger.info("Replied to the message from %d", message.chat.id)


@dispatcher.message(F.text == "x")
async def turn_off_the_bot(message: Message) -> None:
    logger.info("Got a command to shut down from %d. Bye!", message.chat.id)
    await message.answer("bye!")
    await shutdown_bot()
    sys.exit(0)


@dispatcher.message()
async def reply_message(message: Message) -> None:
    """Accepts the messages and responds accordingly."""
    logger.info("Got a new message from chat id %d", message.chat.id)

    await message.answer(
        text="Push the button:",
        reply_markup=DEFAULT_KEYBOARD,
    )
    logger.info("Replied to the message from %d", message.chat.id)


async def main() -> None:
    """Makes the bot listen to new Telegram messages."""
    logger.info("Bot is waking up...")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
