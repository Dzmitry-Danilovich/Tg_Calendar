from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
import app.keyboards as kb
from datetime import datetime

router = Router()

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
async def zapisz(message: Message, state: FSMContext):
    await message.answer("wybarana opcja tak")
    await state.clear()

@router.callback_query(F.data == 'nie')
async def delete(message: Message, state: FSMContext):
    await message.answer('jest tekst')
    await state.clear()

db.close()
