import datetime
from gino import Gino
from aiogram import Dispatcher
import sqlalchemy as sa
from data import config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table = sa.inspect(self.__class__)
        primary_key_columns = table.primary_key.columns
        values = {}
        for column in primary_key_columns:
            column_name = self._column_name_map[column.name]
            values[column.name] = getattr(self, column_name)
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now()
    )


# Установка связи с PostgreSQL
async def on_startup(dispatcher: Dispatcher):
    await db.set_bind(config.POSTGRES_URI)
