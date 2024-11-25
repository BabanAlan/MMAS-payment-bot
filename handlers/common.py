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
        text=common_phrases['start'],
        reply_markup=base_keyboard()
    )


# Обработка кнопки отмены операции
@router.message(StateFilter(F.text == buttons['back'])
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text=common_phrases['cancel'],
        reply_markup=base_keyboard()
    )
