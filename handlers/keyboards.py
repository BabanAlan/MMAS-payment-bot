from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers.buttons import buttons

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def base_keyboard():
    keyboard = make_row_keyboard([buttons['add_payment']])
    return keyboard


def payment_keyboard():
    keyboard = make_row_keyboard([buttons['back']])
    return keyboard
