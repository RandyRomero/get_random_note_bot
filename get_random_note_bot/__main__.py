import asyncio
import logging
import os

from get_random_note_bot.bot.main import get_new_bot

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(name)s:%(lineno)s:%(message)s",
    level="DEBUG",
)
logging.getLogger("asyncio").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_TELEGRAM_ID = os.environ["ADMIN_TELEGRAM_ID"]


async def main() -> None:
    bot = get_new_bot(BOT_TOKEN)
    await bot.bot.send_message(chat_id=ADMIN_TELEGRAM_ID, text="Starting get_random_note_bot...")
    await bot.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
