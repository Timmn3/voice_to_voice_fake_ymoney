from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.shemas.user import User


# добавление пользователя
async def add_user(user_id: int, first_name: str, last_name: str, username: str, status: str,
                   balance: float, bill_id: str):
    try:
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                    status=status, balance=balance, bill_id=bill_id)
        await user.create()
    except UniqueViolationError:
        print('Пользователь не добавлен')


# выбрать всех пользователей
async def select_all_users():
    users = await User.query.gino.all()
    return users


# выбрать всех пользователей с балансом больше 2 рублей
async def select_all_users_big_balance():
    users = await User.select('user_id').where(User.balance > 0).gino.all()
    return users


# выбрать всех пользователей с балансом меньше 30 рублей
async def select_all_users_balance_lower_100():
    users = await User.select('user_id').where(User.balance < 30).gino.all()
    return users


# подсчет количества пользователей
async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count


# выбрать пользователя
async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


# обновляет имя пользователя
async def update_status(user_id, status):
    user = await select_user(user_id)
    await user.update(status=status).apply()


# функция для проверки аргументов переданных при регистрации
async def check_args(args, user_id: int):
    if args == '':  # если в аргумент передана пустая строка
        args = '0'
        return args

    elif not args.isnumeric():  # если не только цифры, а и буквы
        args = '0'
        return args

    elif args.isnumeric():  # если только цифры
        if int(args) == user_id:  # если аргумент является id пользователя
            args = '0'
            return args
        # получаем из БД пользователя у которого user_id такой же, как и переданный аргумент
        elif await select_user(user_id=int(args)) is None:  # если его нет
            args = '0'
            return args

        else:  # если аргумент прошел все проверки
            args = str(args)
            return args

    else:  # если, что-то пошло не так
        args = '0'
        return args


async def change_balance(user_id: int, amount: int):  # функция изменения баланса
    user = await select_user(user_id)
    new_balance = user.balance + amount
    await user.update(balance=new_balance).apply()


async def check_balance(user_id: int, amount):  # функция для проверки баланса
    user = await select_user(user_id=user_id)  # получаем юзера
    try:
        amount = int(amount)  # переводим строку в число
        if user.balance + amount >= 0:
            await change_balance(user_id, amount)
            return True  # Если у пользователя есть деньги
        elif user.balance + amount < 0:
            return 'no maney'  # если у пользователя нет денег
    except Exception:  # Если передаем буквы в строке
        return False


async def user_balance(user_id: int):  # какой баланс у пользователя
    user = await select_user(user_id)  # получаем юзера
    try:
        return user.balance
    except Exception:
        return False


async def user_bill_id(user_id: int):  # получаем идентификатор заказа
    user = await select_user(user_id)  # получаем юзера
    return user.bill_id


async def change_bill_id(user_id: int, value):  # измененяем идентификатор заказа
    user = await select_user(user_id)
    new_bill_id = value
    await user.update(bill_id=new_bill_id).apply()


async def clear_bill_id(user_id: int):  # очищаем идентификатор заказа
    user = await select_user(user_id)
    await user.update(bill_id='').apply()
