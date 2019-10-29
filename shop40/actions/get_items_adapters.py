"""
This file contains various methods for loading products for display
"""


def naive_loader(**kwargs):
    """
    The naive loader is basically naive, loads items from top to down
    :kwargs: items(Model), limit
    """
    Items = kwargs['items']
    limit = kwargs['limit']
    return Items.select()[:limit]


def users_shop(**kwargs):
    """
    This is the ultimate loader. It loads items based on the user to give a unique shopping experience.
    """

    return naive_loader(**kwargs)