"""
This file contains various methods for loading products for display
"""
from shop40.db import Items, Users


def naive_loader(**kwargs):
    """
    The naive loader is basically naive, loads items from top to down
    :kwargs: page
    """
    batch = 16
    page = kwargs['page']-1
    start = page*batch
    end = start + batch
    return Items.select(Users.id.alias('seller_id'),
                        Users.name.alias('seller'),
                        Items.id,
                        Items.item).join(Users).dicts()[start:end]


def users_shop(**kwargs):
    """
    This is the ultimate loader. It loads items based on the user to give a unique shopping experience.
    """

    return naive_loader(**kwargs)