"""
Here we handle social media interactions. For instance, we have the following;

1. Posting to facebook, instagram and twitter.
2. Sending direct messages to users.
3. Running advertisement campaigns.
"""


def upload_to_facebook(post):
    pass


def upload_to_instagram(post):
    pass


def upload_to_twitter(post):
    pass


def upload_to_social_media(post, media='fit'):
    
    if 'f' in 'fit':
        fb = upload_to_facebook(post)

    if 'i' in 'fit':
        insta = upload_to_instagram(post)

    if 't' in 'fit':
        tt = upload_to_twitter(post)

    return {'status':True, 'msg':'Uploads Successfull'}