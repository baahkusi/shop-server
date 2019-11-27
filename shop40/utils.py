import os
import random
from hashlib import sha1
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from shop40.config import SENDGRID_API_KEY, TESTING


def send_email(to_email, message, template={'id': '', 'data': ''}):

    message = Mail(from_email='shop40@africaniz.com',
                   to_emails=to_email,
                   subject='Africaniz',
                   html_content=message)

    if TESTING == 'false':
        message.dynamic_template_data = template['data']
        message.template_id = template['id']

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response
    except Exception as e:
        pass


def fresh_pin(n=5):
    """
    Generate a random n digit pin
    """
    return ''.join([str(random.randint(0, 9)) for n in range(n)])


def gen_token(email, pin):
    """
    Generate a SHA1 Encoded String as token
    """
    return sha1(f"{pin},{email}".encode()).hexdigest()


def shadow_print(s):
    if TESTING == 'true':
        print(s)
    else:
        pass