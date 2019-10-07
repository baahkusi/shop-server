from shop40.db import User, Login, DataBaseMappings
from shop40.utils import fresh_pin, send_email, token, get_data, pay_user, points_to_amount
from shop40.decors import login_required


def register(req, **kwargs):
    """
    :kwargs: email, device, user_type
    """

    try:

        user = User.create(email=kwargs['email'], user_type=kwargs['user_type'])
        
        if user.user_type == 'client':
            login = Login.create(user=user.id, device=kwargs['device'])
            login.pin = int(f"{fresh_pin()}{login.id}")
            login.save()
            message = f'<strong>Login code {login.pin}</strong>'
        else:
            message = f'''You got an invitation to be a<strong> {user.user_type} @Akasanoma</strong>. 
                            Go to <a href="http://akasanoma.surge.sh">Akasanoma Login.</a> 
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

        user = User.get(email=kwargs['email'])
        login = Login.get(
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

        user = User.get(email=kwargs['email'])
        login = Login.create(user=user.id, device=kwargs['device'])
        login.pin = int(f"{fresh_pin()}{login.id}")
        login.save()
        message = f'<strong>Login code {login.pin}</strong>'
        send_email(kwargs['email'], message)

    except Exception as e:
        return {'status': False, 'data': repr(e)}

    return {'status': True, 'data': ''}


@login_required
def redeem_points(req, **kwargs):
    """
    :kwargs: user_id, points, payment_data
    """
    try:

        user = User.get(email=kwargs['email'])

        # make sure user has sufficient points
        if user.points < kwargs['points']:
            return {'status': False, 'data':'Insufficient Points'}

        amount = points_to_amount(kwargs['points'])

        if not pay_user(amount, **kwargs['payment_data']):
            return {'status': False, 'data':'Could Not pay user'}

        user.points -= kwargs['points']
        user.save()

    except Exception as e:
        return {'status': False, 'data':repr(e)}

    return {'status': True, 'data':''}


def read(req, **kwargs):
    """
    :kwargs: resource, id, data_def
    """
    try:

        resource = DataBaseMappings[kwargs['resource']]
        resource = resource.get_by_id(id)
        data_def = kwargs['data_def']  # fields specified by user
        data = get_data(resource, data_def)

    except Exception as e:
        return {'status': False, 'data':repr(e)}

    return {'status': True, 'data':data}


def read_many(req, **kwargs):
    """
    :kwargs: resource, data_def, filters
    """
    try:

        resource = DataBaseMappings[kwargs['resource']]
        data_def = kwargs['data_def']  # fields specified by user
        filters = kwargs['filters']  # query filters
        resources = resource.get(**filters)
        data = [get_data(resource, data_def) for resource in resources]  # slow

    except Exception as e:
        return {'status': False, 'data':repr(e)}

    return {'status': True, 'data':data}


@login_required
def create(req, **kwargs):
    """
    :kwargs: resource, data
    """
    try:

        resource = DataBaseMappings[kwargs['resource']]
        resource.create(**kwargs['data'])

    except Exception as e:
        return {'status': False, 'data':repr(e)}

    return {'status': True, 'data':''}


@login_required
def update(req, **kwargs):
    """
    :kwargs: resource, id, data
    """
    try:

        resource = DataBaseMappings[kwargs['resource']]
        data = resource.update(**kwargs['data']).execute()

    except Exception as e:
        return {'status': False, 'data':repr(e)}

    return {'status': True, 'data':data}


@login_required
def delete(req, **kwargs):
    """
    :kwargs: resource, id
    """
    try:

        resource = DataBaseMappings[kwargs['resource']]
        data = resource.delete().where(id=kwargs['id']).execute()

    except Exception as e:
        return {'status': False, 'data':repr(e)}

    return {'status': True, 'data':data}


actions = {
    "create":create,
    "read":read,
    "update":update,
    "delete":delete,
    "login":login,
    "register":register,
    "redeem_points":redeem_points,
    "generate_pin":generate_pin,
}
