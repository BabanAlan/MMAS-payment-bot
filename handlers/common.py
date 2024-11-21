from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import *
from handlers.phrases import common_phrases
from handlers.buttons import buttons

router = Router()

# Начальное сообщение
@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Сюда вы можете присылать чеки, для подтверждения оплаты тренировки"
        "Инструкция по получению чека - https://intercom.help/selector/ru/articles/8355060-"
        "где-найти-и-как-должен-выглядеть-чек-об-оплате",

        reply_markup=base_keyboard()
    )


# Всевозможная обработка сообщения об отмене операции
@router.message(StateFilter("PaymentSending:sending_photo"), F.text == buttons['back'])
@router.message(StateFilter("PaymentSending:sending_name"), F.text == buttons['back'])
@router.message(StateFilter("PaymentSending:sending_date"), F.text == buttons['back'])
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text=common_phrases['cancel'],
        reply_markup=base_keyboard()
    )
