import datetime
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from keyboards.inline import ikb_balance, ikb_menu
from keyboards.inline.ikb_balance import ikb_paid
from loader import dp
from utils.db_api import user_commands as commands
from utils.db_api.user_commands import change_bill_id, user_bill_id, clear_bill_id, change_balance
from utils.misc.ymoney import payment_yoomoney, check_payment_status, amount_of_payment_yoomoney


@dp.message_handler(Command('balance'))  # по каманде /balance выводит баланс
async def show_balance(message: types.Message):
    balance = await commands.user_balance(int(message.from_user.id))
    await message.answer(f'Ваш остаток запросов: {int(balance)}', reply_markup=ikb_balance)


# функция создания идентификатора заказа
async def create_bill_id(user_id, amount):
    dt_now = datetime.datetime.now()  # текущее время
    bill_id = str(user_id) + str(dt_now)  # идентификатор заказа
    await change_bill_id(user_id, bill_id)  # записали в БД идентификатор заказа
    link = await payment_yoomoney(bill_id=bill_id, amount=amount)  # ссылка на оплату в qiwi
    return link


async def send_payment_message(call: CallbackQuery, amount: int):
    link = await create_bill_id(user_id=call.from_user.id, amount=amount)
    await call.message.edit_reply_markup()  # убрать клавиатуру
    await call.message.answer(f'Ссылка для пополнение баланса: \n{link}')
    await call.message.answer('Нажмите, что бы проверить или отменить оплату:', reply_markup=ikb_paid)


@dp.callback_query_handler(text="1 запрос")
async def handle_first_request(call: CallbackQuery):
    await send_payment_message(call, amount=29)


@dp.callback_query_handler(text="3 запроса")
async def handle_second_request(call: CallbackQuery):
    await send_payment_message(call, amount=69)


@dp.callback_query_handler(text="5 запросов")
async def handle_third_request(call: CallbackQuery):
    await send_payment_message(call, amount=99)


@dp.callback_query_handler(text="10 рублей")
async def handle_fourth_request(call: CallbackQuery):
    await send_payment_message(call, amount=10)


@dp.callback_query_handler(text="20 рублей")
async def handle_fifth_request(call: CallbackQuery):
    await send_payment_message(call, amount=20)


# проверка оплаты
# пользователь нажал проверить
@dp.callback_query_handler(text="Оплатил")
async def send_message(call: CallbackQuery):
    user_id = int(call.from_user.id)
    bill_id = await user_bill_id(user_id)  # получаем идентификатор заказа из БД
    status = await check_payment_status(bill_id=bill_id)  # Проверим статус выставленного счета
    await call.message.edit_reply_markup()  # убрать клавиатуру
    await call.message.delete()  # удаляем сообщение
    if status == 'success':
        money = await amount_of_payment_yoomoney(bill_id)  # проверяем сумму по запросу qiwi
        amount = await money_to_amount(money)
        await call.message.answer(f'Ваш статус: Оплачено')
        await change_balance(user_id, amount)  # заносим количество запросов в БД
        balance = await commands.user_balance(user_id)  # смотрим какая в БД сумма
        await call.message.answer(f'Ваш остаток запросов: {int(balance)}')
        await clear_bill_id(user_id)  # очищаем идентификатор заказа в БД
        await call.message.answer(f'Отправьте мне аудиофайл длиной до 30 секунд\n'
                                  f'Формат *.mp3 или *.wav')
    else:
        await call.message.answer(f'Попробуйте оплатить снова, после нажмите проверить:',
                                  reply_markup=ikb_paid)
        await call.message.answer(f'Ваш статус: {status}')


async def money_to_amount(money):
    money = money / 99 + money
    if 28 < money < 30.0:
        return 1
    elif 66 < money < 70.0:
        return 3
    elif 94 < money < 100.0:
        return 5
    else:
        return 0


# пользователь нажал отменить
@dp.callback_query_handler(text="Отменить")
async def send_message(call: CallbackQuery):
    await clear_bill_id(int(call.from_user.id))  # очищаем идентификатор заказа в БД
    await call.message.edit_reply_markup()  # убрать клавиатуру
    await call.message.delete()  # удаляем сообщение
    await call.message.answer(f'Отменено! Выберете голос одного из известных людей😎', reply_markup=ikb_menu)


@dp.message_handler(Command('balance_add'))  # по каманде /balance_add пополняем баланс
async def balance_add(message: types.Message):
    await change_balance(message.chat.id, 1)  # заносим количество запросов в БД
