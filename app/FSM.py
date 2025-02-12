from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
import app.keyboards as kb
from datetime import datetime
from app.connect_db import ManagementEvent

router = Router()
db = ManagementEvent('telegram_event.db')

class Event(StatesGroup):
    datas = State()
    event = State()
    time_ev = State()
    save = State()


@router.message(F.text.lower() == "menu")
async def inline(message: Message):
    await message.answer("Options: ", reply_markup=kb.setting)

@router.callback_query(F.data == "add_event")
async def add_event(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Event.event)
    await callback.message.answer("Podaj datę: dd-mm-rrrr")

@router.callback_query(F.data == 'my_events')
async def my_events(callback: CallbackQuery):
    await callback.message.answer(db.show_event(callback.message.from_user.id))

@router.message(Event.event)
async def add_event_two(message: Message, state: FSMContext):
    try:
        datetime.strptime(message.text, '%d-%m-%Y')
        await state.update_data(datas= message.text)
        await state.set_state(Event.datas)
        await message.answer("Podaj Zdarzenie: ")
    except ValueError:
        await message.answer("Data jest nie poprawna")

@router.message(Event.datas)
async def add_data(message: Message, state: FSMContext):
    await state.update_data(event= message.text)
    await state.set_state(Event.time_ev)
    await message.answer('O któtej chcesz przypomnienie o zdarzeniu?\nNapisz w postaci: HH:MM')

@router.message(Event.time_ev)
async def add_time(message: Message, state: FSMContext):
    try:
        datetime.strptime(message.text, '%H:%M')
        await state.update_data(time_ev=message.text)
        person_event = await state.get_data()
        await message.answer(f"Data: {person_event['datas']} \n Event: {person_event['event']} \n Godzina przypomnienia {person_event['time_ev']}")
        await message.answer('Czy chesz zapisać zdarzenie w Calendar?', reply_markup=kb.saves)
    except ValueError:
        await message.answer('Podana zła godzina')

@router.callback_query(F.data ==  'tak')
async def zapisz(callback: CallbackQuery, state: FSMContext):
    try:
        person = await state.get_data()
        db.add_event(callback.message.from_user.id, person['event'], person['datas'], person['time_ev'])
        await callback.message.answer("Działa")
        await state.clear()
    except ValueError:
        await callback.message.answer("Coś poszło nie tal")

@router.callback_query(F.data == 'nie')
async def delete(message: Message, state: FSMContext):
    await message.answer('jest tekst')
    await state.clear()


