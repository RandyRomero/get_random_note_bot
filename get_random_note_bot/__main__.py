import asyncio
import logging

from get_random_note_bot import settings
from get_random_note_bot.bot.main import get_new_bot

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(name)s:%(lineno)s:%(message)s",
    level="DEBUG",
)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("aiogram").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def main() -> None:
    bot = get_new_bot(settings.BOT_TOKEN)
    # todo: create a send message proxy method in TelegramBot class
    await bot.bot.send_message(
        chat_id=settings.ADMIN_TELEGRAM_ID,
        text="Starting get_random_note_bot...",
    )
    await bot.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
