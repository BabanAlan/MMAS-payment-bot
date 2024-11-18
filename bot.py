import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import payment_sending
from handlers import common

dp = Dispatcher(storage=MemoryStorage())
bot = Bot('6454073989:AAEUfJqGTPX2I3oEUMrpQyKq2KnCqzEpVSo')

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp.include_router(common.router)
    dp.include_router(payment_sending.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
