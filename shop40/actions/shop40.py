from playhouse.shortcuts import model_to_dict
from shop40.db import Items, Users
from .decors import login_required
from .get_items_adapters import naive_loader, users_shop, seller_fetch
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
        return {'status': False, 'data': 'Item Unavailable.'}
    user = Users.get_by_id(item.user.id)

    data = {
        'seller_id':user.id,
        'seller_name':user.name,
        'seller_info':user.info,
        'id':item.id,
        'item':item.item
    }
    return {'status': True, 'data':{item.id: data} }


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
        return {'status': False, 'data': repr(e)}

    try:
        seller = Users.get_by_id(int(kwargs['seller_id']))
        if 'update' in kwargs:
            item = Items.update(item=item).where(Items.id==int(kwargs['id'])).execute()
            item = Items.get_by_id(item)
        else:
            item = Items.create(user=seller, item=item)
        add_tags(item, item.item['tags'])
    except Exception as e:
        return {'status': False, 'data': repr(e)}

    return {'status': True, 'data': {'item_id':item.id},'msg':'Upload Successfull.'}


@login_required
def verify_payment(req, **kwargs):
    """
    Verify and make payment for an order.
    :kwargs: payment
    """

    return {'status': True, 'data': 'Payment Made.'}


@login_required
def place_order(req, **kwargs):
    """
    Place an order.
    :kwargs: order_details
    """

    return {'status': True, 'data': 'Order Placed.'}


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
                    return {'status': False, 'data': 'Username Exists.'}
                Users.update(name=kwargs['data']['name']).where(
                    Users.id == req.user.id).execute()

            if req.user.email != kwargs['data']['email']:
                if Users.select().where(
                        Users.email == kwargs['data']['email']).exists():
                    return {'status': False, 'data': 'Email Exists.'}
                Users.update(email=kwargs['data']['email'],
                             email_verified=False).where(
                                 Users.id == req.user.id).execute()

            if req.user.phone != kwargs['data']['phone']:
                if Users.select().where(
                        Users.phone == kwargs['data']['phone']).exists():
                    return {'status': False, 'data': 'Phone Exists.'}
                Users.update(phone=kwargs['data']['phone'],
                             phone_verified=False).where(
                                 Users.id == req.user.id).execute()
        else:
            return {'status': False, 'data': 'Dunno what to do.'}

    except Exception as e:
        return {'status': False, 'data': repr(e)}

    return {'status': True, 'data': 'Info Updated.'}
