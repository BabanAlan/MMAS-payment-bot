from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.methods import forward_message
from aiogram import Bot, Dispatcher

from keyboards import *

router = Router()
bot = Bot('6454073989:AAEUfJqGTPX2I3oEUMrpQyKq2KnCqzEpVSo')


class PaymentSending(StatesGroup):
    sending_photo = State()
    sending_name = State()
    sending_date = State()


# Инициация сценария отправки чека
@router.message(F.text.lower() == "➕пиркрепить чек")
async def cmd_payment(message: Message, state: FSMContext):
    await message.answer(
        text="Пришлите, пожалуйста, фото чека:",
        reply_markup=payment_keyboard()
    )
    await state.set_state(PaymentSending.sending_photo)


# Получили фото
@router.message(PaymentSending.sending_photo, F.photo != None)
async def photo_sent(message: Message, state: FSMContext):
    await state.update_data(sent_photo=message)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, напишите ФИО занимающегося (за кого оплата):",
        reply_markup=payment_keyboard()
    )
    await state.set_state(PaymentSending.sending_name)


# Фото не было получено
@router.message(PaymentSending.sending_photo)
async def photo_sent_incorrectly(message: Message):
    await message.answer(
        text="Формат сообщения не подходит.\n\n"
             "Пожалуйста, пришлите ФОТО:",
        reply_markup=payment_keyboard()
    )


# Получили имя
@router.message(PaymentSending.sending_name, F.text != None)
async def name_sent(message: Message, state: FSMContext):
    await state.update_data(sent_name=message.text)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите дату занятия (оплаченной тренировки):",
        reply_markup=payment_keyboard()
    )
    await state.set_state(PaymentSending.sending_date)


# Имя не было получено
@router.message(PaymentSending.sending_name)
async def name_sent_incorrectly(message: Message):
    await message.answer(
        text="Имя введено неверно.\n"
             "Пожалуйста, напишите ФИО:",
        reply_markup=payment_keyboard()
    )


# Получили дату
@router.message(PaymentSending.sending_date, F.text != None)
async def name_sent(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.forward_message(
        chat_id="-4594099956",
        from_chat_id=message.chat.id,
        message_id=user_data['sent_photo'].message_id
    )
    await bot.send_message(
        chat_id="-4594099956",
        text=f"{user_data['sent_name']}\n{message.text}"
    )
    
    await message.answer(
        text="Большое спасбо!",
        reply_markup=base_keyboard()
    )
    await state.clear()


# Дата не была получена
@router.message(PaymentSending.sending_date)
async def name_sent_incorrectly(message: Message):
    await message.answer(
        text="Дата введена неверно.\n"
             "Пожалуйста, пришлите дату:",
        reply_markup=payment_keyboard()
    )
