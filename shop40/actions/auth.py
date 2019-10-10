from shop40.db import Users, Logins
from shop40.utils import fresh_pin, send_email, token


def register(req, **kwargs):
    """
    :kwargs: email, device, user_type
    """

    try:

        user = Users.create(email=kwargs['email'])
        
        if user.user_type == 'client':
            login = Logins.create(user=user.id, device=kwargs['device'])
            login.pin = int(f"{fresh_pin()}{login.id}")
            login.save()
            message = f'<strong>Login code {login.pin}</strong>'
        else:
            message = f'''You got an invitation to be a<strong> {user.user_type} @Africaniz</strong>. 
                            Go to <a href="http://africaniz.surge.sh">Africaniz Login.</a> 
                            "Testing Initial Dashboard, kindly try it out and give feedback"'''
        send_email(kwargs['email'], message)

    except Exception as e:
        return {'status': False, 'data': repr(e)}

    return {'status': True, 'data': ''}
    


def login(req, **kwargs):
    """
    :kwargs: email, fresh_pin, device
    """
    try:

        user = Users.get(email=kwargs['email'])
        login = Logins.get(
            user=user.id, pin=kwargs['fresh_pin'], device=kwargs['device'])

        if login.token:
            return {'status': False, 'data': 'Pin already used'}

        message = f'<strong>Login code {login.pin}</strong>'
        login.token = token(kwargs['email'], message)
        login.save()

    except Exception as e:
        return {'status': False, 'data': repr(e)}

    return {'status': True, 'data': {'token': login.token,'user_type':login.user.user_type}}


def generate_pin(req, **kwargs):
    """
    :kwargs: email, device
    """
    try:

        user = Users.get(email=kwargs['email'])
        login = Logins.create(user=user.id, device=kwargs['device'])
        login.pin = int(f"{fresh_pin()}{login.id}")
        login.save()
        message = f'<strong>Login code {login.pin}</strong>'
        send_email(kwargs['email'], message)

    except Exception as e:
        return {'status': False, 'data': repr(e)}

    return {'status': True, 'data': ''}