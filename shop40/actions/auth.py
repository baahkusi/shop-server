import datetime
import bcrypt
from shop40.db import Users, Logins, Activations, Notifications
from shop40.utils import fresh_pin, send_email, gen_token, shadow_print
from .decors import login_required, user_required


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
        return {"status": False, "msg": "Email Exists."}

    return {"status": True, "msg": "Registration Successfull."}


def login(req, **kwargs):
    """
    :kwargs: email, password, device_hash, device_data
    """
    try:

        user = Users.get_or_none(email=kwargs["email"])

        if user:

            if user.login_tries + 1 > 10:

                return {
                    "status":
                    False,
                    "msg":
                    "Your account has been blocked, you need to reset your password."
                }
            Users.update(login_tries=Users.login_tries +
                         1).where(Users.id == user.id).execute()

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
                    'id':
                    user.id,
                    'email':
                    user.email,
                    'phone':
                    user.phone,
                    'name':
                    user.name,
                    'level':
                    user.level,
                    'email_verified':
                    user.email_verified,
                    'phone_verified':
                    user.phone_verified,
                    'info':
                    user.info,
                    'is_active':
                    user.is_active,
                    'products':
                    user.items.select().count(),
                    'notes':
                    user.notifications.select().where(
                        Notifications.is_read == False).count()
                }

                Users.update(
                    login_count=Users.login_count + 1,
                    last_login=datetime.datetime.now(),
                    login_tries=0).where(Users.id == user.id).execute()

                return {
                    "status": True,
                    "data": {
                        "token": token,
                        "user": user_data
                    },
                    "msg": "Login Successfull."
                }
            else:
                return {"status": False, "msg": "Wrong Password."}
        else:
            return {"status": False, "msg": "Missing User."}

    except Exception as e:
        return {"status": False, "msg": "Login Failed."}


def get_user(req, **kwargs):
    """
    :kwargs: id
    """
    try:
        user = Users.get_or_none(id=int(kwargs['id']))
        data = {
            'id': user.id,
            'email': user.email,
            'phone': user.phone,
            'name': user.name,
            'level': user.level,
            'email_verified': user.email_verified,
            'phone_verified': user.phone_verified,
            'info': user.info,
            'is_active': user.is_active,
            'products': user.items.select().count(),
        }
    except Exception as e:
        return {'status': False, 'msg': 'User Missing.'}

    return {'status': True, 'data': {'user': data},'msg':'User Fetched.'}


@login_required
@user_required(['root','super','admin'])
def get_users(req, **kwargs):
    """
    :kwargs: None
    """

    try:
        if 'filter' in kwargs:
            filt = Users.level == kwargs['filter']
        else:
            filt = Users.level != 'customer'
        users = Users.select(
            Users.id, Users.email, Users.phone, Users.level, Users.name,
            Users.login_count, Users.login_tries, Users.logins_failed,
            Users.last_login.to_timestamp().alias('last_login')).where(filt).dicts()[:]
    except Exception as e:
        return {'status':False, 'msg':'Exception Raised.'}
    return {'status':True,'data':users,'msg':'Users Found.'}


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
            return {"status": True, "msg": 'Email Sent.'}
        else:
            return {"status": False, "msg": "Missing User."}

    except Exception as e:
        return {"status": False, "msg": "Resend Failed."}


@login_required
@user_required(['root'])
def create_user(req, **kwargs):
    """
    :kwargs: email, phone, level, country, city, code, phone_code, mode
    """
    try:
        info = {
            'personal': {
                'phone': kwargs['phone'],
                'email': kwargs['email'],
                'country': kwargs['country'],
                'code': kwargs['code'],
                'city': kwargs['city']
            }
        }
        if kwargs['mode'] == 'create':

            user = Users.create(email=kwargs['email'],
                                phone=kwargs['phone_code'],
                                level=kwargs['level'],
                                info=info)
            message = f"""Welcome to <strong> @Africaniz</strong>,.Akwaaba. 
                            Go to <a href='{req.referer}/auth/reset'>Africaniz Reset Password.</a>"""
            send_email(kwargs["email"], message)
        elif kwargs['mode'] == 'edit':
            user = Users.update(
                email=kwargs['email'],
                phone=kwargs['phone_code'],
                level=kwargs['level'],
            ).where(Users.id == kwargs['id']).execute()
            user = Users.get_by_id(kwargs['id'])
            user.info['personal']['city'] = info['personal']['city']
            user.info['personal']['code'] = info['personal']['code']
            user.info['personal']['country'] = info['personal']['country']
            user.info['personal']['email'] = info['personal']['email']
            user.info['personal']['phone'] = info['personal']['phone']
            user.save()
        else:
            return {'status': False, 'msg': 'Command Unknown.'}

    except Exception as e:
        return {'status': False, 'msg': 'Exception Raised.'}
    return {'status': True, 'msg': 'Task Done.'}


@login_required
@user_required(['root','super','admin'])
def switch_seller(req, **kwargs):
    """
    :kwargs: seller
    """

    return get_user(req ,id=kwargs['seller'])



@login_required
def activate_account(req, **kwargs):
    """
    :kwargs: phase (there are two phases, first generate, second activate), code
            medium ( phone | email)
    """

    if kwargs['phase'] == 'generate':
        try:
            activation = Activations.create(user=req.user, code=fresh_pin(6))
            message = f"""Here is your activation code from @Africaniz {activation.code}. It will expire in 5 minutes."""
            if kwargs['medium'] == 'email':
                if req.user.email_verified:
                    return {'status': False, 'msg': 'Email Verified.'}
                else:
                    send_email(req.user.email, message)
            elif kwargs['medium'] == 'phone':
                if not req.user.phone:
                    return {'status': False, 'msg': 'Null Number.'}
                if req.user.phone_verified:
                    return {'status': False, 'msg': 'Phone Verified.'}
                else:
                    pass
        except Exception as e:
            return {'status': False, 'msg': 'Try Again.'}
        return {'status': True, 'msg': 'Pin Sent.'}
    elif kwargs['phase'] == 'activate':
        try:
            activation = Activations.get_or_none(code=kwargs['code'])
            if activation:
                now = datetime.datetime.now()
                tdelta = now - activation.ctime

                if tdelta.seconds >= 5 * 60:
                    return {'status': False, 'msg': 'Pin Expired.'}
                if activation.user == req.user:
                    if kwargs['medium'] == 'email':
                        Users.update(email_verified=True).where(
                            Users.id == req.user.id).execute()
                        msg = 'Email'
                    elif kwargs['medium'] == 'phone':
                        Users.update(phone_verified=True).where(
                            Users.id == req.user.id).execute()
                        msg = 'Phone'
                else:
                    return {'status': False, 'msg': 'Wrong User.'}
            else:
                return {'status': False, 'msg': 'Ungenerated Pin.'}
        except Exception as e:
            return {'status': False, 'msg': "Server Error."}
        return {'status': True, 'msg': f'{msg} Activated.'}


@login_required
def auth(req, **kwargs):
    """
    :kwargs: None
    """

    return {'status': True, 'msg': 'Login Verified.'}


@login_required
def decor_tester(req, **kwargs):
    """
    :kwargs: None
    """

    return {'status': True, 'data': 'Decor Tests Passed'}
