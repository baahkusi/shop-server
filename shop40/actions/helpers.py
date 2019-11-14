import cloudinary
from cloudinary.uploader import upload
from shop40.config import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, TESTING, db
from shop40.db import Tags, Items
from shop40.utils import shadow_print



def upload_images(images, tags = []):
    """
    Upload Images of new product.
    """

    cloudinary.config( 
        cloud_name = "neaonnim", 
        api_key = CLOUDINARY_API_KEY, 
        api_secret = CLOUDINARY_API_SECRET 
    )


    imgs = []
    
    for image in images:

        # Image already uploaded
        if not isinstance(image, str):
            imgs.append(image)
            continue

        img = upload(
                image,
                folder = 'test' if TESTING=='true' else 'africaniz',
                tags = tags,
                format = 'jpg'
            )
        imgs.append({
            'url':img['secure_url'],
            'id':img['public_id']
        })

    return imgs


def add_tags(item, tags):
    """
    Create tags for new product.
    """
    for tag in tags:
        try:
            record = Tags.select().where(Tags.tag == tag.lower())
            if record.exists():
                record = record.get()
                with db.atomic():
                    if item not in record.items[:]:
                        record.items.add(item)
            else:
             tag = Tags.create(tag=tag.lower())
             tag.items.add(item)
        except Exception as e:
            shadow_print(e)
            return False
    
    return True