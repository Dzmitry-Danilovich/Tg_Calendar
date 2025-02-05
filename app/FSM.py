from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
import app.keyboards as kb

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
    await state.update_data(datas= message.text)
    await state.set_state(Event.datas)
    await message.answer("Podaj Zdarzenie: ")

@router.message(Event.datas)
async def add_data(message: Message, state: FSMContext):
    await state.update_data(event= message.text)
    person_event = await state.get_data()
    await message.answer("Akrualizowanie ukończone")
    await message.answer(f"Data: {person_event}")
    await state.set_state(Event.time_ev)
    await message.answer('O któtej chcesz przypomnienie o zdarzeniu?')

@router.message(Event.time_ev)
async def add_time(message: Message, state: FSMContext):
    await state.update_data(time_ev=message.text)
    person_event = await state.get_data()
    await message.answer(f"Data: {person_event['datas']} \n Event: {person_event['event']} \n Godzina przypomnienia {person_event['time_ev']}")
    await message.answer('Czy chesz zapisać zdarzenie w Calendar?', reply_markup=kb.saves)


@router.callback_query(F.data ==  'tak')
async def zapisz(message: Message, state: FSMContext):
    await message.answer("wybarana opcja tak")
    await state.clear()

@router.callback_query(F.data == 'nie')
async def delete(message: Message, state: FSMContext):
    await state.clear()

