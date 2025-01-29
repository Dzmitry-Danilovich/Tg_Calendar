from aiogram import F, Router

from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import app.keyboards as kb

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

@router.message(F.text.lower() == "menu")
async def inline(message: Message):
    await message.answer("Options: ", reply_markup=kb.setting)


@router.callback_query(F.data == "add_event")
async def add_event(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer("Podaj datę")

@router.callback_query(F.data == "my_events")
async def my_events(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('hh')