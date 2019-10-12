from peewee import CharField, ManyToManyField, BooleanField, ForeignKeyField, SmallIntegerField
from playhouse.postgres_ext import JSONField
from .base import BaseModel


class Groups(BaseModel):
    
    name = CharField(max_length=8, unique=True)
    actions = CharField(unique=True) # comma seperated list of actions allowed for group


class Users(BaseModel):

    email = CharField(unique=True)
    phone = CharField(null=True, unique=True)
    groups = ManyToManyField(Groups, backref='users')
    password = CharField(max_length=512)
    auth_mode = CharField(max_length=64, default='login')
    level = CharField(default='customer') # root | superuser | staff | customer | seller
    is_verified = BooleanField(default=False)
    is_active = BooleanField(default=True)

    @property
    def login(self):
        return self.logins.get()


class Logins(BaseModel):

    user = ForeignKeyField(Users, backref='logins', lazy_load=False)
    device_hash = CharField()
    device_data = JSONField()
    token = CharField(max_length=512)