from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.methods import forward_message
from aiogram import Bot, Dispatcher

from bot import bot
from config import config
from handlers.keyboards import *
from handlers.phrases import payment_phrases
from handlers.buttons import buttons

router = Router()


# Состояния диалога в сценарии отправки чека
class PaymentSending(StatesGroup):
    sending_photo = State()
    sending_name = State()
    sending_date = State()


# Инициация сценария отправки чека
@router.message(F.text == buttons['add_payment'])
async def cmd_payment(message: Message, state: FSMContext):
    await message.answer(
        text=payment_phrases['payment_img'],
        reply_markup=payment_keyboard()
    )
    await state.set_state(PaymentSending.sending_photo)


# Получили фото
@router.message(PaymentSending.sending_photo, F.photo != None)
async def photo_sent(message: Message, state: FSMContext):
    await state.update_data(sent_photo=message)
    await message.answer(
        text=payment_phrases['payment_name'],
        reply_markup=payment_keyboard()
    )
    await state.set_state(PaymentSending.sending_name)


# Фото не было получено
@router.message(PaymentSending.sending_photo)
async def photo_sent_incorrectly(message: Message):
    await message.answer(
        text=payment_phrases['payment_img_incorrect'],
        reply_markup=payment_keyboard()
    )


# Получили имя
@router.message(PaymentSending.sending_name, F.text != None)
async def name_sent(message: Message, state: FSMContext):
    await state.update_data(sent_name=message.text)
    await message.answer(
        text=payment_phrases['payment_date'],
        reply_markup=payment_keyboard()
    )
    await state.set_state(PaymentSending.sending_date)


# Имя не было получено
@router.message(PaymentSending.sending_name)
async def name_sent_incorrectly(message: Message):
    await message.answer(
        text=payment_phrases['payment_name_incorrect'],
        reply_markup=payment_keyboard()
    )


# Получили дату
@router.message(PaymentSending.sending_date, F.text != None)
async def name_sent(message: Message, state: FSMContext):
    user_data = await state.get_data()
    # Пересылка сообщения с картинкой(чтобы был виден отправитель)
    await bot.forward_message(
        chat_id=config['admins_chat_id'],
        from_chat_id=message.chat.id,
        message_id=user_data['sent_photo'].message_id
    )
    # Сборка остальной информации в одно сообщение и отправка
    await bot.send_message(
        chat_id=config['admins_chat_id'],
        text=f"{user_data['sent_name']}\n{message.text}"
    )
    # Отправка завершающего сценарий сообщения
    await message.answer(
        text=payment_phrases['payment_finish'],
        reply_markup=base_keyboard()
    )
    # Сброс state
    await state.clear()


# Дата не была получена
@router.message(PaymentSending.sending_date)
async def name_sent_incorrectly(message: Message):
    await message.answer(
        text=payment_phrases['payment_date_incorrect'],
        reply_markup=payment_keyboard()
    )
