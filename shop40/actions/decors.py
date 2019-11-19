from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(req, **kwargs):

        if req.user:
            return func(req, **kwargs)
        else:
            return {'status':False, 'msg':'Login Required'}
    
    return wrapper


def user_required(user_types):

    def inner(func):

        @wraps(func)
        def wrapper(req, **kwargs):

            if req.user.user_type in user_types:
                return func(req, **kwargs)
            else:
                return {'status':False, 'msg':'Permission Required'}
    
    return inner