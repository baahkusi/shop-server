from peewee import ForeignKeyField, CharField, TextField
from playhouse.postgres_ext import JSONField, ArrayField
from .auth import Users, BaseModel

class Items(BaseModel):
    
    user = ForeignKeyField(Users, backref='items', lazy_load=False)
    item = JSONField()


class Tags(BaseModel):

    item = ForeignKeyField(Items, backref='tags', lazy_load=False)
    tag = CharField()


class Combinations(BaseModel):

    user = ForeignKeyField(Users, backref='combinations', lazy_load=False)
    items = ArrayField()


class Reviews(BaseModel):

    user = ForeignKeyField(Users, backref='items', lazy_load=False)
    item = ForeignKeyField(Items, backref='reviews', lazy_load=False)
    review = TextField()


class Likes(BaseModel):

    user = ForeignKeyField(Users, backref='likes', lazy_load=False)
    item = ForeignKeyField(Items, backref='likes', lazy_load=False)


class Follows(BaseModel):

    follower = ForeignKeyField(Users, backref='followers', lazy_load=False)
    followed = ForeignKeyField(Users, backref='follows', lazy_load=False)


class Orders(BaseModel):

    user = ForeignKeyField(Users, backref='orders', lazy_load=False)
    order = JSONField()
