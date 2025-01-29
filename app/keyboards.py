from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

setting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Add event", callback_data='add_event')],
    [InlineKeyboardButton(text="My events", callback_data="my_events")]
])