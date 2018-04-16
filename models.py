from peewee import SqliteDatabase, Model, DateField, CharField, FloatField
import datetime
import config
import logging


logger = logging.getLogger("main.models")
db = SqliteDatabase(config.DATABASE)


class MemHistory(Model):
    date = DateField(default=datetime.date.today())
    app = CharField()
    used_mem = FloatField()

    class Meta:
        database = db
