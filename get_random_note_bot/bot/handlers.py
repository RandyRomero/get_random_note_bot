import functools
import logging
import typing as tp

from aiogram.types import Message

from get_random_note_bot import settings
from get_random_note_bot.bot.keyboads import DEFAULT_KEYBOARD
from get_random_note_bot.bot.logic import get_a_random_note
from get_random_note_bot.bot.repository import Entities

logger = logging.getLogger(__name__)


T = tp.TypeVar("T")


def authenticate(
    handler: tp.Callable[[tp.Any, Message], tp.Awaitable[T]],
) -> tp.Callable[[tp.Any, Message], tp.Awaitable[T | None]]:
    """Wrapper around Telegram bot handlers."""

    @functools.wraps(handler)
    async def wrapper(class_instance: tp.Any, message: Message) -> T | None:
        user_id = getattr(message.from_user, "id", None)
        if user_id == settings.ADMIN_TELEGRAM_ID:
            return await handler(class_instance, message)

        await message.reply("The bot is a work a progress. See you later.")
        return None

    return wrapper


class Handlers:
    """Handlers that respond to user messages to a bot."""

    def __init__(self, entities: Entities) -> None:
        self.entities: Entities = entities

    @authenticate
    async def reply_get_a_random_note_handler(self, message: Message) -> None:
        """Handles a request to get a random note."""
        logger.info("Got a new message from chat id %d", message.chat.id)
        reply = await get_a_random_note(self.entities)

        await message.answer(
            text=reply,
            reply_markup=DEFAULT_KEYBOARD,
        )
        logger.info("Replied to the message from %d", message.chat.id)

    @authenticate
    async def reply_message_handler(self, message: Message) -> None:
        """Accepts any unexpected messages and gives a hint to use the button to get a note."""
        logger.info("Got a new message from chat id %d", message.chat.id)

        await message.answer(
            text="Push the button:",
            reply_markup=DEFAULT_KEYBOARD,
        )
        logger.info("Replied to the message from %d", message.chat.id)
