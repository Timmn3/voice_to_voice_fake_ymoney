from yoomoney import Quickpay
from yoomoney import Client
from data.config import YOOMONEY_TOKEN, wallet_number
from loguru import logger


async def payment_yoomoney(bill_id, amount):
    quickpay = Quickpay(
        receiver=wallet_number,
        quickpay_form="shop",
        targets="Оплата бота",
        paymentType="SB",
        sum=amount,
        label=bill_id
    )
    return quickpay.redirected_url  # возвращаем ссылку на оплату


async def check_payment_status(bill_id):
    try:
        client = Client(YOOMONEY_TOKEN)
        history = client.operation_history(label=bill_id)
        for operation in history.operations:
            if operation.label == bill_id:
                return operation.status  # success
        return None
    except Exception as e:
        logger.error(e)
        return None


# какая сумма платежа
async def amount_of_payment_yoomoney(bill_id):
    try:
        client = Client(YOOMONEY_TOKEN)
        history = client.operation_history(label=bill_id)
        for operation in history.operations:
            if operation.label == bill_id:
                return operation.amount  # сумма
        return None
    except Exception as e:
        logger.error(e)
        return None
