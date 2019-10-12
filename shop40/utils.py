import os
import random
from hashlib import sha1
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .config import SENDGRID_API_KEY


def send_email(to_email, message):

    message = Mail(
        from_email='africaniz@example.com',
        to_emails=to_email,
        subject='Login Pin',
        html_content=message)

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    return response


def fresh_pin():
    """
    Generate a random 5 digit pin
    """
    return ''.join([str(random.randint(0,9)) for n in range(5)])


def gen_token(email, pin):
    """
    Generate a SHA1 Encoded String as token
    """
    return sha1(f"{pin},{email}".encode()).hexdigest()


def shadow_print(s):
    print(s)