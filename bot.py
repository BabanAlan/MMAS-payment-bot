import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import payment_sending
from handlers import common
from config import config

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(config['bot_token'])


async def main():
    # Логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Подключение всех роутеров
    dp.include_router(common.router)
    dp.include_router(payment_sending.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    
