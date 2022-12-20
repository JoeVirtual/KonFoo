# -*- coding: utf-8 -*-
"""
categories.py
~~~~~~~~~~~~~
Extended Python enum type.

:copyright: (c) 2015-2022 by Jochen Gerhaeusser.
:license: BSD, see LICENSE for details
"""
from __future__ import annotations

import enum
from typing import Any


class Category(enum.Enum):
    """ The :class:`Category` class is a is a subclass of the :class:`~enum.Enum`
    class provided by the Python standard module :mod:`enum`, and extends its
    base class with methods

    - to `describe` a specific `Category` member by its `name`, `value` tuple
    - to list the `member names` of a `Category`
    - to list the `member values` of a `Category`
    - to `get` the `value` of the `Category` member by its name
    - to `get` the `name` of the `Category` member by is value
    - to `get` the `member` of the `Category` by its value

    Example:

    >>> class Format(Category):
    ...     hour = 'hh'
    ...     minute = 'mm'
    ...     second = 'ss'
    >>> Format
    <enum 'Format'>
    >>> type(Format.hour)
    <enum 'Format'>
    >>> isinstance(Format, Category)
    False
    >>> issubclass(Format, Category)
    True
    >>> isinstance(Format.hour, Format)
    True
    >>> print(Format.hour)
    (hour, hh)
    >>> str(Format.hour)
    '(hour, hh)'
    >>> Format.hour
    Format.hour = 'hh'
    >>> repr(Format.hour)
    "Format.hour = 'hh'"
    >>> list(Format)
    [Format.hour = 'hh', Format.minute = 'mm', Format.second = 'ss']
    >>> [format for format in Format]
    [Format.hour = 'hh', Format.minute = 'mm', Format.second = 'ss']
    >>> Format.hour.name
    'hour'
    >>> Format.hour.value
    'hh'
    >>> Format.hour.describe()
    ('hour', 'hh')
    >>> [member.name for member in Format]
    ['hour', 'minute', 'second']
    >>> Format.names()
    ['hour', 'minute', 'second']
    >>> [member.value for member in Format]
    ['hh', 'mm', 'ss']
    >>> Format.values()
    ['hh', 'mm', 'ss']
    >>> Format['hour'].value
    'hh'
    >>> Format.get_value('hour')
    'hh'
    >>> Format('hh').name
    'hour'
    >>> Format.get_name('hh')
    'hour'
    >>> Format.get_member('hh')
    Format.hour = 'hh'
    >>> 'hh' in Format.values()
    True
    >>> 'hour' in Format.names()
    True
    """

    def __str__(self) -> str:
        """ Return str(self).

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> str(Format.hour)
        '(hour, hh)'
        """
        return f"({self.name!s}, {self.value!s})"

    def __repr__(self) -> str:
        """ Return repr(self). See help(type(self)) for accurate signature.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> repr(Format.hour)
        "Format.hour = 'hh'"
        """
        return f"{self.__class__.__name__}.{self.name!s} = {self.value!r}"

    def describe(self) -> tuple[str, Any]:
        """ Returns the `name`, `value` tuple to describe a specific `Category`
        member.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> Format.hour.describe()
        ('hour', 'hh')
        """
        return self.name, self.value

    @classmethod
    def names(cls) -> list[str]:
        """ Returns a list of the member `names` of a `Category`.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> Format.names()
        ['hour', 'minute', 'second']
        """
        return [member.name for member in cls]

    @classmethod
    def values(cls) -> list[Any]:
        """ Returns a list of the member `values` of a `Category`.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> Format.values()
        ['hh', 'mm', 'ss']
        """
        return [member.value for member in cls]

    @classmethod
    def get_name(cls, value: Any) -> str:
        """ Returns the `name` of the `Category` member matches the *value*,
        or an empty string if no member match.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> Format.get_name('hh')
        'hour'
        >>> Format.get_name('dd')
        ''
        """
        for member in cls:
            if member.value == value:
                return member.name
        return str()

    @classmethod
    def get_value(cls, name: str) -> Any | None:
        """ Returns the `value` of the `Category` member matches the *name*,
        or :data:`None` if no member match.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> Format.get_value('hour')
        'hh'
        >>> Format.get_value('day')

        """
        for member in cls:
            if member.name == name:
                return member.value
        return None

    @classmethod
    def get_member(cls,
                   value: Any,
                   default: Category | None = None) -> Category | None:
        """ Returns the first `Category` member matches the *value*, or the
        specified *default* member if no member match.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> Format.get_member('hh')
        Format.hour = 'hh'
        >>> Format.get_member('day', None)

        """
        for member in cls:
            if member.value == value:
                return member
        return default
