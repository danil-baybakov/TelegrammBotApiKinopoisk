import peewee
from peewee import SqliteDatabase, Model, CharField, DateTimeField, IntegerField, FloatField
import os
import datetime

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(CURRENT_PATH, 'tg_bot.db')

db = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = db


class ParamsStorage(BaseModel):
    cid = IntegerField(unique=True)
    command = CharField(max_length=30, null=True)
    genre = CharField(max_length=100, null=True)
    limit = IntegerField(null=True)
    order = IntegerField(null=True)
    min_rating = FloatField(null=True)
    max_rating = FloatField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now())


class History(BaseModel):
    cid = IntegerField(null=True)
    command = CharField(max_length=30, null=True)
    genre = CharField(max_length=100, null=True)
    limit = IntegerField(null=True)
    order = IntegerField(null=True)
    min_rating = FloatField(null=True)
    max_rating = FloatField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now())


def create_tables():
    with db:
        db.create_tables([ParamsStorage, History])
