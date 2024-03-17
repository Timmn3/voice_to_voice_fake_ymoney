from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="Мориарти", callback_data='Мориарти'),
                                    ],
                                    [
                                        InlineKeyboardButton(text="Моргенштерн", callback_data='Моргенштерн'),
                                    ],
                                    [
                                        InlineKeyboardButton(text="Нолик (м/ф Фиксики)", callback_data='Нолик')
                                    ],
                                    [
                                        InlineKeyboardButton(text="Иванзоло", callback_data='Иванзоло')
                                    ],
                                    [
                                        InlineKeyboardButton(text="Ева Элфи", callback_data='Ева Элфи')
                                    ],
                                    [
                                        InlineKeyboardButton(text="Kussia", callback_data='Kussia')
                                    ]
                                ])


