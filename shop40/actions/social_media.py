"""
Here we handle social media interactions. For instance, we have the following;

1. Posting to facebook, instagram and twitter.
2. Sending direct messages to users.
3. Running advertisement campaigns.
"""
from io import BytesIO
import json
import requests
from ..config import FB_ACCESS_TOKEN, FB_PAGE_ID


def upload_to_facebook(item, msg):
    import facebook
    fb = facebook.GraphAPI(access_token=FB_ACCESS_TOKEN, version='3.1')
    images = []
    for image in item['images']:
        req = requests.get(image.url)
        img = BytesIO(req.content)
        fb_img = fb.put_photo(image=img, published=False)
        images.append({'media_fbid': fb_img['id']})
    images = json.dumps(images)
    link = f'https://www.africaniz.com/items/{item.id}'
    post_obj = fb.put_object(parent_object='104860027643603',
                  connection_name='feed',
                  message=msg,
                  link=link,
                  attached_media=images)
    return post_obj


def upload_to_instagram(item, msg):
    pass


def upload_to_twitter(item, msg):
    pass


def upload_to_social_media(item, msg, media=['facebook']):

    if 'facebook' in media:
        fb = upload_to_facebook(item, msg)

    if 'instagram' in media:
        insta = upload_to_instagram(item, msg)

    if 'twitter' in media:
        tt = upload_to_twitter(item, msg)

    return {'status': True, 'msg': 'Uploads Successfull'}
