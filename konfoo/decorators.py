# -*- coding: utf-8 -*-
"""
    decorators.py
    ~~~~~~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD-style, see LICENSE for details
"""

from functools import wraps
from .categories import Byteorder, Option


def byte_order_option(default=Byteorder.default):
    """Attaches the option ``byte_order`` with its *default* value to the
    keyword arguments, when the option does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            option = Option.byteorder.value
            kwargs[option] = kwargs.get(option, default)
            return method(*args, **kwargs)

        return wrapper

    return decorator


def field_types_option(default=False):
    """Attaches the option ``field_types`` with its *default* value to the
    keyword arguments when the option does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            option = Option.field_types.value
            kwargs[option] = kwargs.get(option, bool(default))
            return method(*args, **kwargs)

        return wrapper

    return decorator


def nested_option(default=False):
    """Attaches the option ``nested`` with its *default* value to the
    keyword arguments when the option does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            option = Option.nested.value
            kwargs[option] = kwargs.get(option, bool(default))
            return method(*args, **kwargs)

        return wrapper

    return decorator


def verbose_option(default=False):
    """Attaches the option ``verbose`` with its *default* value to the
    keyword arguments when the option does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            option = Option.verbose.value
            kwargs[option] = kwargs.get(option, bool(default))
            return method(*args, **kwargs)

        return wrapper

    return decorator
