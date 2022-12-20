# -*- coding: utf-8 -*-
"""
enums.py
~~~~~~~~
Extended Python integer enum type.

:copyright: (c) 2015-2022 by Jochen Gerhaeusser.
:license: BSD, see LICENSE for details.
"""
from __future__ import annotations

import enum


class Enumeration(enum.IntEnum):
    """ The :class:`Enumeration` class is a subclass from the
    :class:`~enum.IntEnum` class provided by the Python standard module
    :mod:`enum`, and extends its base class with methods

    - to `describe` a specific `Enumeration` member by its `name`, `value` tuple
    - to list the `member names` of an `Enumeration`
    - to list the `member values` of an `Enumeration`
    - to `get` the `value` of the `Enumeration` member by its name
    - to `get` the `name` of the `Enumeration` member by its value
    - to `get` the `member` of the `Enumeration` by its value

    Example:

    >>> class Color(Enumeration):
    ...     black = 0x000000
    ...     maroon = 0x080000
    ...     white = 0xffffff
    >>> Color
    <enum 'Color'>
    >>> type(Color.maroon)
    <enum 'Color'>
    >>> isinstance(Color, Enumeration)
    False
    >>> issubclass(Color, Enumeration)
    True
    >>> isinstance(Color.maroon, Color)
    True
    >>> print(Color.maroon)
    (maroon, 524288)
    >>> str(Color.maroon)
    '(maroon, 524288)'
    >>> Color.maroon
    Color.maroon = 524288
    >>> repr(Color.maroon)
    'Color.maroon = 524288'
    >>> list(Color)
    [Color.black = 0, Color.maroon = 524288, Color.white = 16777215]
    >>> [color for color in Color]
    [Color.black = 0, Color.maroon = 524288, Color.white = 16777215]
    >>> Color.maroon.name
    'maroon'
    >>> Color.maroon.value
    524288
    >>> Color.maroon.describe()
    ('maroon', 524288)
    >>> [member.name for member in Color]
    ['black', 'maroon', 'white']
    >>> Color.names()
    ['black', 'maroon', 'white']
    >>> [member.value for member in Color]
    [0, 524288, 16777215]
    >>> Color.values()
    [0, 524288, 16777215]
    >>> Color['maroon'].value
    524288
    >>> Color.get_value('maroon')
    524288
    >>> Color(0).name
    'black'
    >>> Color.get_name(0)
    'black'
    >>> Color.get_member(0)
    Color.black = 0
    >>> int(Color.black)
    0
    >>> 0 in Color.values()
    True
    >>> 'black' in Color.names()
    True
    """

    def __str__(self) -> str:
        """ Return str(self).

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> str(Color.maroon)
        '(maroon, 524288)'
        """
        return f"({self.name!s}, {self.value!s})"

    def __repr__(self) -> str:
        """ Return repr(self). See help(type(self)) for accurate signature.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> repr(Color.maroon)
        'Color.maroon = 524288'
        """
        return f"{self.__class__.__name__}.{self.name!s} = {self.value!r}"

    def describe(self) -> tuple[str, int]:
        """ Returns the `name`, `value` tuple to describe a specific
        `Enumeration` member.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> Color.maroon.describe()
        ('maroon', 524288)
        """
        return self.name, self.value

    @classmethod
    def names(cls) -> list[str]:
        """ Returns a list of the member `names` of an `Enumeration`.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> Color.names()
        ['black', 'maroon', 'white']
        """
        return [member.name for member in cls]

    @classmethod
    def values(cls) -> list[int]:
        """ Returns a list of the member `values` of an `Enumeration`.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> Color.values()
        [0, 524288, 16777215]
        """
        return [member.value for member in cls]

    @classmethod
    def get_name(cls,
                 value: int) -> str:
        """ Returns the `name` of the `Enumeration` member matches the *value*,
        or an empty string if no member match.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> Color.get_name(0xffffff)
        'white'
        >>> Color.get_name(0x777777)
        ''
        """
        for member in cls:
            if member.value == value:
                return member.name
        return str()

    @classmethod
    def get_value(cls,
                  name: str) -> int | None:
        """ Returns the `value` of the `Enumeration` member matches the *name*,
        or :data:`None` if no member match.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> Color.get_value('white')
        16777215
        >>> Color.get_value('red')

        """
        for member in cls:
            if member.name == name:
                return member.value
        return None

    @classmethod
    def get_member(cls,
                   value: int,
                   default: Enumeration | None = None) -> Enumeration | None:
        """ Returns the first `Enumeration` member matches the *value*, or the
        specified *default* member if no member match.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> Color.get_member(0)
        Color.black = 0
        >>> Color.get_member(0x777777, None)

        """
        for member in cls:
            if member.value == value:
                return member
        return default
