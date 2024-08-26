import os
import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from asyncpg import Record

from dotenv import load_dotenv

import db

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']

DB_USER = os.environ['DB_USER']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_USER_PASSWORD = os.environ['DB_USER_PASSWORD']
DB_NAME = os.environ['DB_NAME']


bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher()

db = db.DB(
    user=DB_USER,
    host=DB_HOST,
    port=DB_PORT,
    password=DB_USER_PASSWORD,
    database=DB_NAME,
)

async def get_random_row() -> Record:
    """Get a random row from a note table.."""
    async with db.get_connection() as conn:
        result = await conn.fetchrow("""
        SELECT notes.id, notes.text AS note, notes.additional_info AS info, topics.text AS topic, authors.name AS author FROM notes
        LEFT JOIN authors ON authors.id = notes.author_id
        JOIN notes_topics ON notes.id = public.notes_topics.note_id
        JOIN topics ON notes_topics.topic_id = topics.id
        ORDER BY random() limit 1;
        """)
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


@dispatcher.message()
async def reply_message(message: Message):
    """Accepts the messages and responds accordingly."""
    if message.text.lower() == "x":
        await message.answer("bye!")
        await shutdown_bot()
        sys.exit(0)

    reply = await get_a_random_note()
    await message.answer(text=reply)


async def main():
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
