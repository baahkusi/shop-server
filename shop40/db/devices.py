from peewee import CharField
from playhouse.postgres_ext import JSONField
from .base import BaseModel


class Devices(BaseModel):

    device_hash = CharField()
    device_data = JSONField()
    browse_data = JSONField()