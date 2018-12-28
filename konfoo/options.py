# -*- coding: utf-8 -*-
"""
    options.py
    ~~~~~~~~~~
    <Add description of the module here>.

    :copyright: (c) 2015-2018 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details
"""

from functools import wraps

from .categories import Category
from .globals import BYTEORDER, Byteorder


class Option(Category):
    byte_order = 'byte_order'
    nested = 'nested'
    verbose = 'verbose'


def byte_order_option(default=BYTEORDER):
    """ Attaches the option ``byte_order`` with its *default* value to the
    keyword arguments, when the option does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            option = Option.byte_order.value
            kwargs[option] = kwargs.get(option, default)
            return method(*args, **kwargs)

        return wrapper

    return decorator


def get_byte_order(options):
    option = Option.byte_order.value
    byte_order = options.get(option, BYTEORDER)
    if isinstance(byte_order, str):
        byte_order = Byteorder.get_member(byte_order, BYTEORDER)
    return byte_order


def nested_option(default=False):
    """ Attaches the option ``nested`` with its *default* value to the
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


def get_nested(options):
    option = Option.nested.value
    return options.get(option, False)


def verbose_option(default=False):
    """ Attaches the option ``verbose`` with its *default* value to the
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


def verbose(options, message=None):
    option = Option.verbose.value
    if options.get(option, False) and message:
        print(message)
