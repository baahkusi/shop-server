from playhouse.shortcuts import model_to_dict
from shop40.db import Items, Users, Combinations, Likes
from .decors import login_required
from .get_items_adapters import naive_loader, users_shop, seller_fetch
from .get_combos_adapters import combo_loader, user_combos
from .helpers import upload_images, add_tags


def get_items(req, **kwargs):
    """
    Get items for display
    :kwargs: fetch (just list items of seller), limit ,page, filters, device_hash, context(user's interest so far)
    """
    if 'fetch' in kwargs:
        data = seller_fetch(**kwargs)
    elif req.user:
        data = users_shop(**kwargs)
    else:
        data = naive_loader(**kwargs)

    return {'status': True, 'data': data}


def fetch_item(req, **kwargs):
    """
    Gets a single item
    :kwargs: item
    """
    item = Items.select().where(Items.id == kwargs['item']).join(Users).get()

    if not item:
        return {'status': False, 'msg': 'Item Unavailable.'}
    user = Users.get_by_id(item.user.id)
    likes = Likes.select().where(Likes.what == 'item',
                                 Likes.pk == item.id).count()
    data = {
        'seller_id': user.id,
        'seller_name': user.name,
        'seller_info': user.info,
        'id': item.id,
        'likes': likes,
        'item': item.item
    }
    return {'status': True, 'data': {item.id: data}}


@login_required
def upload_item(req, **kwargs):
    """
    Upload new product.
    :kwargs: item_details, seller_id, update ( whether it is an update)
    """
    item = kwargs['item_details']

    item['images'] = upload_images(item['images'], item['tags'])

    try:
        for i in range(len(item['options'])):

            for j in range(len(item['options'][i]['values'])):
                item['options'][i]['values'][j]['images'] = upload_images(
                    item['options'][i]['values'][j]['images'], item['tags'])
    except Exception as e:
        return {'status': False, 'msg': 'Images Upload Failed.'}

    try:
        seller = Users.get_by_id(int(kwargs['seller_id']))
        if 'update' in kwargs:
            item = Items.update(item=item).where(
                Items.id == int(kwargs['id'])).execute()
            item = Items.get_by_id(int(kwargs['id']))
        else:
            item = Items.create(user=seller, item=item)
        add_tags(item, item.item['tags'])
        #upload to sccial media
    except Exception as e:
        return {'status': False, 'msg': 'Upload Failed.'}

    return {
        'status': True,
        'data': {
            'item_id': item.id
        },
        'msg': 'Upload Successfull.'
    }


@login_required
def verify_payment(req, **kwargs):
    """
    Verify and make payment for an order.
    :kwargs: payment
    """

    return {'status': True, 'msg': 'Payment Made.'}


@login_required
def place_order(req, **kwargs):
    """
    Place an order.
    :kwargs: order_details
    """

    return {'status': True, 'msg': 'Order Placed.'}


@login_required
def set_info(req, **kwargs):
    """
    Set information of user
    :kwargs: info, data
    """

    try:
        old_info = req.user.info
        if kwargs['info'] in ['personal', 'social']:
            old_info[kwargs['info']] = kwargs['data']
            Users.update(info=old_info).where(
                Users.id == req.user.id).execute()
        elif kwargs['info'] == 'profile':
            data = kwargs['data']
            data['brand'] = upload_images(data['brand'], [data['title']])
            data['logo'] = upload_images(data['logo'], [data['title']])
            old_info[kwargs['info']] = data
            Users.update(info=old_info).where(
                Users.id == req.user.id).execute()
        elif kwargs['info'] == 'account':
            if req.user.name != kwargs['data']['name']:
                if Users.select().where(
                        Users.name == kwargs['data']['name']).exists():
                    return {'status': False, 'msg': 'Username Exists.'}
                Users.update(name=kwargs['data']['name']).where(
                    Users.id == req.user.id).execute()

            if req.user.email != kwargs['data']['email']:
                if Users.select().where(
                        Users.email == kwargs['data']['email']).exists():
                    return {'status': False, 'msg': 'Email Exists.'}
                Users.update(email=kwargs['data']['email'],
                             email_verified=False).where(
                                 Users.id == req.user.id).execute()

            if req.user.phone != kwargs['data']['phone']:
                if Users.select().where(
                        Users.phone == kwargs['data']['phone']).exists():
                    return {'status': False, 'msg': 'Phone Exists.'}
                Users.update(phone=kwargs['data']['phone'],
                             phone_verified=False).where(
                                 Users.id == req.user.id).execute()
        else:
            return {'status': False, 'msg': 'Dunno what to do.'}

    except Exception as e:
        return {'status': False, 'msg': 'SetInfo Failed.'}

    return {'status': True, 'msg': 'Info Updated.'}


@login_required
def create_combo(req, **kwargs):
    """
    :kwargs: name, items, update(Boolean, whether to update), id(if update==True)
    """
    try:
        if kwargs['update']:
            combo = Combinations.get_or_none(id=kwargs['id'])
            if combo and combo.user == req.user:
                combo.name = kwargs['name']
                combo.items = kwargs['items']
                combo.save()
            else:
                return {'status': False, 'msg': 'Not Existent'}
        else:
            pk = Combinations.create(user=req.user,
                                     name=kwargs['name'],
                                     items=kwargs['items'])
    except Exception as e:
        return {'status': False, 'msg': ''}
    return {'status': True, 'msg': ''}


def get_combos(req, **kwargs):
    """
    :kwargs: fetch (user fetch), limit ,page, user
    """

    if 'fetch' in kwargs:
        data = user_combos(**kwargs)
    elif 'light' in kwargs:
        data = Combinations.select(Combinations.id, Combinations.name,
                                   Combinations.items).join(Users).where(
                                       Users.id == kwargs['user']).dicts()[:]
    else:
        data = combo_loader(**kwargs)

    return {'status': True, 'data': data}


def fetch_combo(req, **kwargs):
    """
    :kwargs: id,
    """

    combo = Combinations.get_or_none(id=kwargs['id'])

    if combo:
        try:
            combo_items = Items.select(Users.id.alias('seller_id'),
                                       Users.name.alias('seller'), Items.id,
                                       Items.item).join(Users).where(
                                           Items.id.in_(
                                               combo.items)).dicts()[:]
        except Exception as e:
            return {'status': False, 'msg': 'Running Items.'}
    else:
        return {'status': False, 'msg': 'Combo Missing.'}

    data = {
        'items': combo_items,
        'id': combo.id,
        'info': combo.info,
        'is_buyable': combo.is_buyable,
        'is_private': combo.is_private
    }

    return {'status': True, 'data': data}


@login_required
def like(req, **kwargs):
    """
    :kwargs: what, pk
    """
    try:
        like = Likes.select().where(Likes.user == req.user,
                                    Likes.what == kwargs['what'],
                                    Likes.pk == kwargs['pk'])

        if like.exists():
            like = like.get()
            like.is_liked = not like.is_liked
            like.save()
            msg = 'UnLike Happened.'
        else:
            Likes.create(user=req.user, what=kwargs['what'], pk=kwargs['pk'])
            msg = 'Like Happened.'
    except Exception as e:
        return {'status': False, 'msg': 'Like Error.'}

    return {'status': True, 'msg': msg}
