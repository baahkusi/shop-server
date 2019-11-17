from peewee import ForeignKeyField, CharField, TextField, BooleanField, ManyToManyField
from playhouse.postgres_ext import JSONField, ArrayField
from .auth import Users, BaseModel


class Items(BaseModel):
    
    user = ForeignKeyField(Users, backref='items')
    info = JSONField(null=True)
    item = JSONField()


class Tags(BaseModel):

    items = ManyToManyField(Items, backref='tags')
    tag = CharField(unique=True)

ItemTag = Tags.items.get_through_model()


class Combinations(BaseModel):

    user = ForeignKeyField(Users, backref='combinations')
    name = CharField()
    items = ArrayField()
    is_private = BooleanField(default=False)


class Reviews(BaseModel):

    user = ForeignKeyField(Users, backref='reviews')
    item = ForeignKeyField(Items, backref='reviews')
    review = TextField()


class Comments(BaseModel):

    user = ForeignKeyField(Users, backref='comments')
    combo = ForeignKeyField(Combinations, backref='comments')
    review = TextField()

class Likes(BaseModel):

    user = ForeignKeyField(Users, backref='likes')
    item = ForeignKeyField(Items, backref='likes')


class Follows(BaseModel):

    follower = ForeignKeyField(Users, backref='follows')
    followed = ForeignKeyField(Users, backref='followers')


class Orders(BaseModel):

    user = ForeignKeyField(Users, backref='orders')
    status = CharField(default='waiting') # waiting | processing | cancelled | suspended completed


class OrderItems(BaseModel):

    order = ForeignKeyField(Orders, backref='items')
    order_item = JSONField()
    status = CharField(default='waiting') # waiting | processing | cancelled | suspended  completed



class Notifications(BaseModel):

    user = ForeignKeyField(Users, backref='notifications')
    message = TextField()
    is_read = BooleanField(default=False) 
