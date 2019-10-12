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