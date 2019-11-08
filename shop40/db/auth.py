from peewee import CharField, ManyToManyField, BooleanField, ForeignKeyField, SmallIntegerField, IntegerField, DateTimeField, TextField
from playhouse.postgres_ext import JSONField, ArrayField
from .base import BaseModel


class Groups(BaseModel):
    
    name = CharField(max_length=8, unique=True)
    actions = ArrayField() # list of actions allowed for group


class Users(BaseModel):

    email = CharField(unique=True)
    groups = ManyToManyField(Groups, backref='users')
    password = CharField(max_length=512)
    name = CharField(unique=True, default="sbk")
    auth_mode = CharField(max_length=64, default='login') #login  social
    level = CharField(default='customer') # root | superuser | staff | customer | seller
    email_verified = BooleanField(default=False)
    phone_verified = BooleanField(default=False)
    info = JSONField(default= lambda : {})
    is_active = BooleanField(default=True)
    last_login = DateTimeField(null=True)
    login_count = IntegerField(default=0)

    @property
    def login(self):
        return self.logins.get()


class Logins(BaseModel):

    user = ForeignKeyField(Users, backref='logins')
    device_hash = CharField()
    device_data = JSONField()
    token = CharField(max_length=512)


class Activations(BaseModel):

    user = ForeignKeyField(Users, backref='logins')
    code = CharField(unique=True)