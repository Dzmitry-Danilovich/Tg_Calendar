import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from privateINF.ton import toke

bot = Bot(token=toke)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await  message.reply("shdjflsjd")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

