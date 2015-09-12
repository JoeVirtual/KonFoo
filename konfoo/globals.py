# -*- coding: utf-8 -*-
"""
    globals.py
    ~~~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD-style, see LICENSE for details
"""

from functools import wraps

from .enums import Enumeration
from .categories import Category


class ItemClass(Enumeration):
    Field = 1
    Container = 2
    Pointer = 3
    Structure = 10
    Sequence = 11
    Array = 12
    Stream = 20
    String = 21
    Float = 30
    Decimal = 40
    Bit = 41
    Byte = 42
    Char = 43
    Signed = 44
    Unsigned = 45
    Bitset = 46
    Bool = 47
    Enum = 48
    Scaled = 49
    Fraction = 50
    Bipolar = 51
    Unipolar = 52
    Datetime = 53


class Option(Category):
    field_types = 'field_types'
    byte_order = 'byte_order'
    nested = 'nested'
    verbose = 'verbose'


class Byteorder(Category):
    auto = 'auto'
    little = 'little'
    big = 'big'


#: Default Byteorder
BYTEORDER = Byteorder.little


def get_byte_order(options):
    option = Option.byte_order.value
    return options.get(option, BYTEORDER)


def get_field_types(options):
    option = Option.field_types.value
    return options.get(option, False)


def get_nested(options):
    option = Option.nested.value
    return options.get(option, False)


def verbose(options, message=None):
    option = Option.verbose.value
    if options.get(option, False) and message:
        print(message)


def byte_order_option(default=BYTEORDER):
    """Attaches the option ``byte_order`` with its *default* value to the
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


def limiter(value, minimum, maximum):
    """Returns the *value* limited between *minimum* and *maximum*
    whereby the *maximum* wins over the *minimum*.

    Example:

    >>> limiter(64, 0, 255)
    64
    >>> limiter(-128, 0, 255)
    0
    >>> limiter(0, 127, -128)
    -128
    """
    return min(max(value, minimum), maximum)
