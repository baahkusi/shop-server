import cloudinary
from cloudinary.uploader import upload
from shop40.config import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, TESTING

def upload_images(images, tags):
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
        imgs.append(
            upload(
                image,
                folder = 'test' if TESTING=='true' else 'africaniz',
                tags = tags,
                format = 'jpg'
            )
        )

    return imgs
