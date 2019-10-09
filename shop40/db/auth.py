from peewee import *
from playhouse.postgres_ext import JSONField
from .base import BaseModel

class Groups(BaseModel):
    
    name = CharField(max_length=8, unique=True)
    actions = CharField(unique=True) # comma seperated list of actions allowed for group


class Users(BaseModel):

    email = CharField(max_length=256, null=True, unique=True)
    phone = CharField(max_length=256, unique=True)
    groups = ManyToManyField(Groups, backref='users')
    auth_mode = CharField(max_length=64, default='login')
    is_root = BooleanField(default=False)
    is_verified = BooleanField(default=False)
    is_active = BooleanField(default=True)

    @property
    def login(self):
        return self.logins.get()


class Logins(BaseModel):

    user = ForeignKeyField(Users, backref='logins', primary_key=True, lazy_load=False)
    pin = IntegerField(null=True)
    device_hash = CharField(null=True)
    device_data = JSONField()
    token = CharField(max_length=512, null=True)
    duration = SmallIntegerField(default=30, null=True)
