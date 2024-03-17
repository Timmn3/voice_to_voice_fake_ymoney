from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# отмена
ikb_cancel = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Продолжить", callback_data='Продолжить'),
        InlineKeyboardButton(text="Отмена", callback_data='Отмена')
    ],

])