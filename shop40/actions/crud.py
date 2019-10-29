import shop40.db as db
from .decors import login_required


def read(req, **kwargs):
    """
    :kwargs: resource, id
    """
    try:

        resource = getattr(db, kwargs['resource'])
        data = resource.get_by_id(id)

    except Exception as e:
        return {'status': False, 'data':repr(e)}

    return {'status': True, 'data':data}


def read_many(req, **kwargs):
    """
    :kwargs: resource, filters
    """
    try:

        resource = getattr(db, kwargs['resource'])
        filters = kwargs['filters']  # query filters
        data = resource.get(**filters)

    except Exception as e:
        return {'status': False, 'data':repr(e)}

    return {'status': True, 'data':data}


@login_required
def create(req, **kwargs):
    """
    :kwargs: resource, data
    """
    try:

        resource = getattr(db, kwargs['resource'])
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

        resource = getattr(db, kwargs['resource'])
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

        resource = getattr(db, kwargs['resource'])
        data = resource.delete().where(id=kwargs['id']).execute()

    except Exception as e:
        return {'status': False, 'data':repr(e)}

    return {'status': True, 'data':data}

