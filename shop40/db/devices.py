from peewee import CharField, ManyToManyField
from playhouse.postgres_ext import JSONField
from .base import BaseModel
from .shop40 import Users


class Devices(BaseModel):

    users = ManyToManyField(Users, backref='tags')
    device_hash = CharField()
    device_data = JSONField()
    browse_data = JSONField()

UserDevices = Devices.users.get_through_model()