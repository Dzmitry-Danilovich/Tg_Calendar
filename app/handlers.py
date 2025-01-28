from aiogram import F, Router

from aiogram.types import Message
from aiogram.filters import CommandStart, Command

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await  message.answer(f"Hi, {message.from_user.first_name}")

@router.message(Command("Give_ID"))
async def set_id(message: Message):
    await message.reply(f"Your ID: {message.from_user.id}")

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Help")

@router.message(F.text.lower() == "how are you")
async def how_are_you(message: Message):
    await message.answer("I'm fine")
