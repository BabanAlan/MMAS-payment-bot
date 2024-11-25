from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from handlers.keyboards import *
from handlers.phrases import common_phrases
from handlers.buttons import buttons
from bot import bot

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
@router.message(F.text == buttons['back'])
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text=common_phrases['cancel'],
        reply_markup=base_keyboard()
    )


# Обработка инлайн-кнопки отмены операции 
@router.callback_query(F.data == buttons['back'])
async def call_cancel(call: CallbackQuery, state: FSMContext):
    await state.set_data({})
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=common_phrases['cancel'],
        reply_markup=base_keyboard()
    )
