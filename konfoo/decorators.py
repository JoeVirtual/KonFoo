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


def option(name, default=None):
    """Attaches an option with its *name* and *default* value to the
    keyword arguments, if the keyword does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            kwargs[name] = kwargs.get(name, default)
            return method(*args, **kwargs)

        return wrapper

    return decorator


def byte_order_option(default=Byteorder.default):
    """Attaches the byte order option with the *default* value to the
    keyword arguments, if the keyword does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            kwargs[Option.byteorder] = kwargs.get(Option.byteorder,
                                                  bool(default))
            return method(*args, **kwargs)

        return wrapper

    return decorator


def field_types_option(default=False):
    """Attaches the field type option with a *default* value to the
    keyword arguments, if the keyword does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            kwargs[Option.classes] = kwargs.get(Option.classes,
                                                bool(default))
            return method(*args, **kwargs)

        return wrapper

    return decorator


def nested_option(default=False):
    """Attaches the nested option with the *default* value to the
    keyword arguments, if the keyword does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            kwargs[Option.nested] = kwargs.get(Option.nested,
                                               bool(default))
            return method(*args, **kwargs)

        return wrapper

    return decorator


def verbose_option(default=False):
    """Attaches the verbose option with the *default* value to the
    keyword arguments, if the keyword does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            kwargs[Option.verbose] = kwargs.get(Option.verbose,
                                                bool(default))
            return method(*args, **kwargs)

        return wrapper

    return decorator
