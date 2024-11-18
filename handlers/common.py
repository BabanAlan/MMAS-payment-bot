from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import *

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Чек деньги платить было\nинструкция по получению ссылки",
        reply_markup=base_keyboard()
    )


@router.message(StateFilter("PaymentSending:sending_photo"), F.text.lower() == "🔙отмена")
@router.message(StateFilter("PaymentSending:sending_name"), F.text.lower() == "🔙отмена")
@router.message(StateFilter("PaymentSending:sending_date"), F.text.lower() == "🔙отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Операция отменена",
        reply_markup=base_keyboard()
    )
