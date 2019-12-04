from peewee import ForeignKeyField, CharField, TextField, BooleanField, ManyToManyField, IntegerField
from playhouse.postgres_ext import JSONField, ArrayField
from .auth import Users, BaseModel


class Items(BaseModel):
    
    user = ForeignKeyField(Users, backref='items')
    is_published = BooleanField(default=False)
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
    info = JSONField(null=True)
    is_private = BooleanField(default=False)
    is_buyable = BooleanField(default=False)


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
    what = CharField(default="item")
    pk = IntegerField(default=0)
    is_liked = BooleanField(default=True)


class Follows(BaseModel):

    follower = ForeignKeyField(Users, backref='follows')
    followed = ForeignKeyField(Users, backref='followers')


class Orders(BaseModel):

    user = ForeignKeyField(Users, backref='orders')
    info = JSONField(null=True)
    payment = JSONField(null=True)
    location = JSONField(null=True)
    status = CharField(default='waiting') # waiting | processing | cancelled | suspended | completed


class OrderItems(BaseModel):

    order = ForeignKeyField(Orders, backref='items')
    order_item = JSONField()
    status = CharField(default='waiting') # waiting | processing | cancelled | suspended | completed


class Notifications(BaseModel):

    user = ForeignKeyField(Users, backref='notifications')
    message = TextField()
    is_read = BooleanField(default=False)
