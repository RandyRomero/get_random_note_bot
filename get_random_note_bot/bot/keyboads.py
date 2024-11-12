from enum import StrEnum

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class ButtonsText(StrEnum):
    GET_A_RANDOM_NOTE = "Get a random note"


GET_A_RANDOM_NOTE_BUTTON = KeyboardButton(text=ButtonsText.GET_A_RANDOM_NOTE)
DEFAULT_KEYBOARD = ReplyKeyboardMarkup(keyboard=[[GET_A_RANDOM_NOTE_BUTTON]])
