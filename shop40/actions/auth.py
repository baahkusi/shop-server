import datetime
import bcrypt
from shop40.db import Users, Logins, Activations
from shop40.utils import fresh_pin, send_email, gen_token, shadow_print
from .decors import login_required


def register(req, **kwargs):
    """
    :kwargs: email, password
    """

    try:

        user = Users.create(
            email=kwargs["email"],
            password=bcrypt.hashpw(kwargs["password"].encode(),
                                   bcrypt.gensalt()),
        )

        message = f"""Welcome to <strong> @Africaniz</strong>,.Akwaaba. 
                            Go to <a href='{req.referer}'>Africaniz Login.</a>"""
        send_email(kwargs["email"], message)

    except Exception as e:
        shadow_print(e)
        return {"status": False, "data": "Registration Failure."}

    return {"status": True, "data": "Registration Success."}


def login(req, **kwargs):
    """
    :kwargs: email, password, device_hash, device_data
    """
    try:

        user = Users.get_or_none(email=kwargs["email"])

        if user:
            if bcrypt.checkpw(kwargs["password"].encode(),
                              user.password.encode()):

                token = gen_token(user.email, fresh_pin())

                Logins.create(
                    user=user,
                    device_hash=kwargs["device_hash"],
                    device_data=kwargs["device_data"],
                    token=token,
                )
                user_data = {
                    'email': user.email,
                    'level': user.level,
                    'email_verified': user.email_verified,
                    'phone_verified': user.phone_verified
                }
                Users.update(login_count=Users.login_count + 1,
                             last_login=datetime.datetime.now()).where(
                                 Users.id == user.id).execute()
                return {
                    "status": True,
                    "data": {
                        "token": token,
                        "user": user_data
                    }
                }
            else:
                return {"status": False, "data": "Wrong Password."}
        else:
            return {"status": False, "data": "Missing User."}

    except Exception as e:
        shadow_print(e)
        return {"status": False, "data": "Login Failed."}


@login_required
def resend_email(req, **kwargs):
    """
    :kwargs: email
    """

    try:

        user = Users.get_or_none(email=kwargs["email"])

        if user:
            message = f"""Welcome to <strong> @Africaniz</strong>,.Akwaaba. 
                        Go to <a href='{req.referer}'>Africaniz Login.</a>"""
            send_email(kwargs["email"], message)
            return {"status": True, "data": 'Email Sent.'}
        else:
            return {"status": False, "data": "Missing User."}

    except Exception as e:
        return {"status": False, "data": "Resend Failed."}


@login_required
def activate_account(req, **kwargs):
    """
    :kwargs: phase (there are two phases, first generate, second activate), code
    """

    if kwargs['phase'] == 'generate':
        try:
            activation = Activations.create(user=req.user, code=fresh_pin(6))
            message = f"""Here is your activation code from @Africaniz {activation.code}. It will expire in 30 minutes."""
            send_email(req.user.email, message)
        except Exception as e:
            return {'status': False, 'data': repr(e)}
        return {'status': True, 'data': 'Pin Sent.'}
    elif kwargs['phase'] == 'activate':
        try:
            activation = Activations.get_or_none(code=kwargs['code'])
            if activation:
                if activation.user == req.user:
                    Users.update(email_verified=True).where(
                        Users.id == req.user.id).execute()
                else:
                    return {'status': False, 'data': 'Wrong User.'}
            else:
                return {'status': False, 'data': 'Ungenerated Pin.'}
        except Exception as e:
            return {'status': False, 'data': repr(e)}
        return {'status': True, 'data': 'Account Activated.'}


@login_required
def decor_tester(req, **kwargs):
    """
    :kwargs: None
    """

    return {'status': True, 'data': 'Decor Tests Passed'}
