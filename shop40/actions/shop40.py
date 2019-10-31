from shop40.db import Items, Users
from .decors import login_required
from .get_items_adapters import naive_loader, users_shop
from .helpers import upload_images, add_tags


def get_items(req, **kwargs):
    """
    Get items for display
    :kwargs: limit, filters, device_hash, context(user's interest so far)
    """

    if req.user:
        return users_shop(req, **kwargs)
    else:
        return naive_loader(**kwargs)


# @login_required
def upload_item(req, **kwargs):
    """
    Upload new product.
    :kwargs: item_details, seller_id
    """
    item = kwargs['item_details']
    
    item['images'] = upload_images(item['images'], item['tags'])

    try:
        for i in range(len(item['options'])):
        
            for j in range(len(item['options'][i]['values'])):
                item['options'][i]['values'][j]['images'] = upload_images(item['options'][i]['values'][j]['images'], item['tags'])
    except Exception as e:
        return {'status':False, 'data':repr(e)}
    
    
    try:
        seller = Users.get_by_id(int(kwargs['seller_id']))
        item = Items.create(user=seller, item=item)
        add_tags(item, item.item['tags'])
    except Exception as e:
        return {'status':False, 'data':repr(e)}

    return {'status':True, 'data':'Upload Successfull.'}


@login_required
def verify_payment(req, **kwargs):
    """
    Verify and make payment for an order.
    :kwargs: payment
    """

    return {'status':True, 'data':'Payment Made.'}


@login_required
def place_order(req, **kwargs):
    """
    Place an order.
    :kwargs: order_details
    """

    return {'status':True, 'data':'Order Placed.'}