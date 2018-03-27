import ast
from functools import wraps
import logging


def add_tag(param):
    def decorator(fun):
        @wraps(fun)
        def wrapper():
            return "<" + param + ">" + fun() + "</" + param + ">"

        return wrapper

    return decorator


@add_tag('h1')
def write_something():
    return 'something'


#####################################################
def validate_json(*params):
    def decorator(fun):
        @wraps(fun)
        def wrapper(json_str):
            _json = ast.literal_eval(json_str)
            for key in _json:
                if key not in params:
                    raise ValueError
            for par in params:
                if par not in _json:
                    raise ValueError
            return fun(json_str)

        return wrapper

    return decorator


@validate_json('first_name', 'last_name')
def process_json(json_data):
    return len(json_data)


#####################################################

def log_this(_logger, **kw):
    lev = {
        0: _logger.debug,
        10: _logger.debug,
        20: _logger.info,
        30: _logger.warning,
        40: _logger.error,
        50: _logger.critical}

    def decorator(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            rv = fun(*args, **kwargs)
            a = [str(x) for x in args] + [str(key) + '=' + str(value) for key, value in kwargs.items()]
            lev[kw['level']](kw['format'], fun.__name__, tuple(a), rv)
            return rv

        return wrapper

    return decorator


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@log_this(logger, level=logging.WARNING, format='%s: %s -> %s')
def my_func(a, b, c=None, d=False):
    return 'Wow!'


#####################################################
def main():
    result = write_something()
    assert result == '<h1>something</h1>'

    result = process_json('{"first_name": "James", "last_name": "Bond"}')
    assert result == 44

    # process_json('{"first_name": "James", "age": 45}')

    # process_json('{"first_name": "James"}')

    # process_json('{"first_name": "James", "last_name": "Bond", "age": 45}')

    my_func(1, 2, d=True)
    my_func(123, '098', d=True, c=None)

    print("OK")


if __name__ == "__main__":
    main()
