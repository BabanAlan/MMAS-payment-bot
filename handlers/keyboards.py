from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.buttons import buttons, types

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def base_keyboard():
    keyboard = make_row_keyboard([buttons['add_payment']])
    return keyboard


def payment_keyboard():
    keyboard = make_row_keyboard([buttons['back']])
    return keyboard


def types_keyboard():
    builder = InlineKeyboardBuilder()
    # Создание кнопок со типами оплаты
    for i in range(len(types)):
        builder.row(
            InlineKeyboardButton(
                text=types[i],
                callback_data=f"tps_{i+1}{types[i]}"
            )
        )

    # Создание кнопки "назад"
    builder.row(
        InlineKeyboardButton(
            text=buttons['back'],
            callback_data=buttons['back']
        )
    )

    builder.adjust(2)
    return builder.as_markup()
