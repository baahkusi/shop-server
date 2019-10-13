from shop40.db.shop40 import *
from shop40.decors import login_required
from shop40.get_item_adapters import naive_loader, users_shop


def get_items(req, **kwargs):
    """
    Get items for display
    :kwargs: limit, filters, device_hash, device_data, context(user's interest so far)
    """

    if req.user:
        return users_shop(req, **kwargs)
    else:
        return naive_loader(req, **kwargs)


@login_required
def upload_images(req, **kwargs):
    """
    Upload Images of new product.
    :kwargs: images
    """
    print(kwargs['images'])
    return {'status':True, 'data':'Uploads Successfull.'}


@login_required
def upload_item(req, **kwargs):
    """
    Upload new product.
    :kwargs: item_details
    """

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