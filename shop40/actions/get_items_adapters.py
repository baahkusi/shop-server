"""
This file contains various methods for loading products for display
"""
from shop40.db import Items, Users


def naive_loader(**kwargs):
    """
    The naive loader is basically naive, loads items from top to down
    :kwargs: page, limit
    """
    limit = kwargs['limit']
    page = kwargs['page'] - 1
    start = page * limit
    end = start + limit
    return Items.select(Users.id.alias('seller_id'),
                        Users.name.alias('seller'), Items.id,
                        Items.item).join(Users).dicts()[start:end]


def users_shop(**kwargs):
    """
    This is the ultimate loader. It loads items based on the user to give a unique shopping experience.
    """

    return naive_loader(**kwargs)


def seller_fetch(**kwargs):
    """
    This fecthes items for a particular seller, also loaded from top to down
    :kwargs: seller
    """
    limit = kwargs['limit']
    page = kwargs['page'] - 1
    start = page * limit
    end = start + limit
    return Items.select(Items.ctime.to_timestamp().alias('timestamp'), Items.id, Items.item).join(Users).where(
        Users.id == kwargs['seller']).dicts()[start:end]
