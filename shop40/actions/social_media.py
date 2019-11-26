"""
Here we handle social media interactions. For instance, we have the following;

1. Posting to facebook, instagram and twitter.
2. Sending direct messages to users.
3. Running advertisement campaigns.
"""


def upload_to_facebook(item):
    pass


def upload_to_instagram(item):
    pass


def upload_to_twitter(item):
    pass


def upload_to_social_media(item, media=['facebook']):
    
    if 'f' in media:
        fb = upload_to_facebook(item_post)

    if 'i' in 'fit':
        insta = upload_to_instagram(item_post)

    if 't' in 'fit':
        tt = upload_to_twitter(item_post)

    return {'status':True, 'msg':'Uploads Successfull'}