import logging
from enum import StrEnum

from aiogram import Bot, Dispatcher, F
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from good_advice_bot.bot.repository import Entities

logger = logging.getLogger(__name__)


class ButtonsText(StrEnum):
    GET_A_RANDOM_NOTE = "Get a random note"


class GoodAdviceTelegramBot:
    """
    Bot entity

    Handles messages from Telegram.
    """

    def __init__(self, bot: Bot, dispatcher: Dispatcher, entities: Entities) -> None:
        """Initializes the bot."""
        self.bot: Bot = bot
        self.dispatcher = dispatcher
        self.entities = entities
        self.get_a_random_note_button = KeyboardButton(text=ButtonsText.GET_A_RANDOM_NOTE)
        self.default_keyboard = ReplyKeyboardMarkup(keyboard=[[self.get_a_random_note_button]])

        self.reply_get_a_random_note_handler = self.dispatcher.message(
            F.text == ButtonsText.GET_A_RANDOM_NOTE,
        )(self.reply_get_a_random_note_handler)
        self.reply_message_handler = self.dispatcher.message()(self.reply_message_handler)

    async def get_a_random_note(self) -> str:
        """Get a formatted string with a random note."""
        random_line = await self.entities.notes.get_random_one()
        note = random_line["note"]
        topic = random_line["topic"]
        author = random_line["author"]
        info = random_line["info"]
        reply = f"Note: {note}\nTopic: {topic}\nAuthor: {author}"
        if info:
            reply = f"{reply}\nAdditional info: {info}"
        return reply

    async def start_polling(self) -> None:
        """Function to start listening to messages from Telegram."""
        logger.info("Bot is waking up...")
        await self.dispatcher.start_polling(self.bot)

    async def reply_get_a_random_note_handler(self, message: Message) -> None:
        """Handles a request to get a random note."""
        logger.info("Got a new message from chat id %d", message.chat.id)
        reply = await self.get_a_random_note()

        await message.answer(
            text=reply,
            reply_markup=self.default_keyboard,
        )
        logger.info("Replied to the message from %d", message.chat.id)

    async def reply_message_handler(self, message: Message) -> None:
        """Accepts any unexpected messages and gives a hint to use the button to get a note."""
        logger.info("Got a new message from chat id %d", message.chat.id)

        await message.answer(
            text="Push the button:",
            reply_markup=self.default_keyboard,
        )
        logger.info("Replied to the message from %d", message.chat.id)


def init_bot(bot_token: str) -> GoodAdviceTelegramBot:
    """Creates a new instance of a GoodAdviceTelegramBot."""
    bot = Bot(token=bot_token)
    dispatcher = Dispatcher()
    entities = Entities()

    return GoodAdviceTelegramBot(bot, dispatcher, entities)
