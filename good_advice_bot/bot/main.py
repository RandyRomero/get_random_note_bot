import logging

from aiogram import Bot, Dispatcher, F

from good_advice_bot.bot.handlers import Handlers
from good_advice_bot.bot.keyboads import ButtonsText
from good_advice_bot.bot.repository import Entities

logger = logging.getLogger(__name__)


class GoodAdviceTelegramBot:
    """
    Bot entity

    Handles messages from Telegram.
    """

    def __init__(self, bot: Bot, dispatcher: Dispatcher, handlers: Handlers) -> None:
        """Initializes the bot."""
        self.bot: Bot = bot
        self.dispatcher = dispatcher
        self.handlers = handlers

    async def start_polling(self) -> None:
        """Function to start listening to messages from Telegram."""
        logger.info("Bot is waking up...")
        await self.dispatcher.start_polling(self.bot)

    def register_handlers(self) -> None:
        """Registers handlers that respond to user messages to the bot."""
        self.dispatcher.message(F.text == ButtonsText.GET_A_RANDOM_NOTE)(
            self.handlers.reply_get_a_random_note_handler,
        )
        self.dispatcher.message()(self.handlers.reply_message_handler)


def get_new_bot(bot_token: str) -> GoodAdviceTelegramBot:
    """Creates a new instance of a GoodAdviceTelegramBot."""
    bot = Bot(token=bot_token)
    dispatcher = Dispatcher()
    entities = Entities()
    handlers = Handlers(entities)

    good_bot = GoodAdviceTelegramBot(bot, dispatcher, handlers)
    good_bot.register_handlers()
    return good_bot
