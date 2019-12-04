"""
This file contains various methods for loading products for display
"""
from shop40.db import Combinations, Users, Items


def get_combo_items(combos):
    combo_items = []

    for combo in combos:
        items = Items.select(Users.id.alias('seller_id'),
                             Users.name.alias('seller'), Items.id,
                             Items.item).join(Users).where(
                                 Items.id.in_(combo.items)).dicts()[:]

        combo_items.append({
            'items': items,
            'id': combo.id,
            'info': combo.info,
            'is_buyable': combo.is_buyable,
            'is_private': combo.is_private
        })

    return combo_items


def combo_loader(**kwargs):
    """
    The combo loader is basically naive, loads Combinations from top to down
    :kwargs: page, limit
    """
    limit = kwargs['limit']
    page = kwargs['page'] - 1
    start = page * limit
    end = start + limit
    combos = Combinations.select().join(Users).order_by(Combinations.id.desc())[start:end]
    return get_combo_items(combos)


def user_combos(**kwargs):
    """
    This fecthes combos for a particular user, also loaded from top to down
    :kwargs: user
    """
    limit = kwargs['limit']
    page = kwargs['page'] - 1
    start = page * limit
    end = start + limit
    combos = Combinations.select().join(Users).where(Users.id == kwargs['user']).order_by(Combinations.id.desc())[start:end]
    return get_combo_items(combos)
