# -*- coding: utf-8 -*-
"""
options.py
~~~~~~~~~~
Function decorators.

:copyright: (c) 2015-2022 by Jochen Gerhaeusser.
:license: BSD, see LICENSE for details
"""
from __future__ import annotations

from functools import wraps
from typing import (Any, Callable)

from .categories import Category
from .globals import (
    Byteorder, BYTEORDER)


class Option(Category):
    byte_order: Option = 'byte_order'
    nested: Option = 'nested'
    verbose: Option = 'verbose'


def byte_order_option(
    default: Byteorder = BYTEORDER) -> Callable[[Callable[..., Any]],
                                                Callable[..., Any]]:
    """ Attaches the option ``byte_order`` with its *default* value to the
    keyword arguments, when the option does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(method)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            option = Option.byte_order.value
            kwargs[option] = kwargs.get(option, default)
            return method(*args, **kwargs)

        return wrapper

    return decorator


def get_byte_order(options: dict[str, Any]) -> Byteorder:
    option = Option.byte_order.value
    byte_order = options.get(option, BYTEORDER)
    if isinstance(byte_order, str):
        byte_order = Byteorder.get_member(byte_order, BYTEORDER)
    return byte_order


def nested_option(
    default: bool = False) -> Callable[[Callable[..., Any]],
                                       Callable[..., Any]]:
    """ Attaches the option ``nested`` with its *default* value to the
    keyword arguments when the option does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(method)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            option = Option.nested.value
            kwargs[option] = kwargs.get(option, bool(default))
            return method(*args, **kwargs)

        return wrapper

    return decorator


def get_nested(options: dict[str, Any]) -> bool:
    option = Option.nested.value
    return options.get(option, False)


def verbose_option(
    default: bool = False) -> Callable[[Callable[..., Any]],
                                       Callable[..., Any]]:
    """ Attaches the option ``verbose`` with its *default* value to the
    keyword arguments when the option does not exist. All positional
    arguments and keyword arguments are forwarded unchanged.
    """

    def decorator(method: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(method)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            option = Option.verbose.value
            kwargs[option] = kwargs.get(option, bool(default))
            return method(*args, **kwargs)

        return wrapper

    return decorator


def verbose(options: dict[str, Any],
            message: str | None = None) -> None:
    option = Option.verbose.value
    if options.get(option, False) and message:
        print(message)
