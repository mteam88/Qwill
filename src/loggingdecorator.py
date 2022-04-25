import logging
from functools import wraps

def logiof(func):
    if hasattr(func, 'loggingio'):  # Only decorate once
        return func

    @wraps(func) # functools to assist with transition
    def wrapper(*args, **kwargs):
        logging.debug(f'{func.__name__}({args}, {kwargs})')
        result = func(*args, **kwargs)
        logging.debug(f'{func.__name__} returns {result}')
        return result

    wrapper.loggingio = True # Only decorate once

    return wrapper