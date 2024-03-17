from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# пополнить баланс
ikb_balance = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="1 запрос - 29 рублей", callback_data='1 запрос')
    ],
    [
        InlineKeyboardButton(text="3 запроса - 69 рублей", callback_data='3 запроса')
    ],
    [
        InlineKeyboardButton(text="5 запросов - 99 рублей", callback_data='5 запросов'),

    ]
])

# поддержать нас
ikb_support_financially = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="10 рублей", callback_data='10 рублей')
    ],
    [
        InlineKeyboardButton(text="20 рублей", callback_data='20 рублей')
    ]
])

# оплатил
ikb_paid = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Оплатил", callback_data='Оплатил'),
        InlineKeyboardButton(text="Отменить", callback_data='Отменить'),

    ]
])
