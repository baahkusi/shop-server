import shop40.db as db
from shop40.decors import login_required
from shop40.get_item_adapters import naive_loader

def get_items(req, **kwargs):
    """
    Get items for display
    :kwargs: limit, filters, device_hash, device_data, context(user's interest so far)
    """

    return naive_loader(req, **kwargs)

@login_required
def upload_images(req, **kwargs):
    """
    Upload Images of new products
    :kwargs: images
    """
    return {'status':True, 'data':'Uploads Successfull.'}
            

