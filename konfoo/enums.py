# -*- coding: utf-8 -*-
"""
    enums.py
    ~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details.
"""

import enum


class Enumeration(enum.Enum):
    """The `Enumeration` class is a subclass from the :class:`~enum.IntEnum` class
    provided by the Python standard module :mod:`enum` and extends its
    base class with methods

    * to `describe` a specific `Enumeration` member by its `name`, `value` pair
    * to list the `member names` of a `Enumeration`
    * to list the `member values` of a `Enumeration`
    * to `get` the `value` of the `Enumeration` member with the matching `name`
    * to `get` the `name` of the `Enumeration` member with the matching `value`
    * to `get` the `member` of the `Enumeration` with the matching `value`

    Example:

    >>> class Color(Enumeration):
    ...     black = 0x000000
    ...     maroon = 0x080000
    ...     white = 0xffffff
    >>> str(Color.maroon)
    '(maroon, 524288)'
    >>> repr(Color.maroon)
    'Color.maroon = 524288'
    >>> Color.maroon.describe()
    ('maroon', 524288)
    >>> Color.names()
    ['black', 'maroon', 'white']
    >>> Color.values()
    [0, 524288, 16777215]
    >>> Color.get_value('maroon')
    524288
    >>> Color.get_name(0)
    'black'
    >>> Color.get_member(0)
    Color.black = 0
    """

    def __str__(self):
        """Return str(self).

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> str(Color.maroon)
        '(maroon, 524288)'
        """
        return "({0.name!s}, {0.value!s})".format(self)

    def __repr__(self):
        """Return repr(self). See help(type(self)) for accurate signature.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> repr(Color.maroon)
        'Color.maroon = 524288'
        """
        return self.__class__.__name__ + ".{0.name!s} = {0.value!r}".format(self)

    def describe(self):
        """Returns the `name`, `value` pair to describe a specific `Enumeration` member.

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
    def names(cls):
        """Returns a list of the member `names` of a `Enumeration`.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> Color.names()
        ['black', 'maroon', 'white']
        """
        return [member[1].name for member in cls.__members__.items()]

    @classmethod
    def values(cls):
        """Returns a list of the member `values` of a `Enumeration`.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> Color.values()
        [0, 524288, 16777215]
        """
        return [member[1].value for member in cls.__members__.items()]

    @classmethod
    def get_name(cls, value):
        """Returns the `name` of the `Enumeration` member with the matching *value*
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
        for v, n in zip(cls.values(), cls.names()):
            if v == value:
                return n
        return str()

    @classmethod
    def get_value(cls, name):
        """Returns the `value` of the `Enumeration` member with the matching *name*
        or `None` if no member match.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> Color.get_value('white')
        16777215
        >>> Color.get_value('red')

        """
        for v, n in zip(cls.values(), cls.names()):
            if n == name:
                return v
        return None

    @classmethod
    def get_member(cls, value, default=None):
        """Returns the first `Enumeration` member with the matching *value*
        or the specified *default* value if no member match.

        Example:

        >>> class Color(Enumeration):
        ...     black = 0x000000
        ...     maroon = 0x080000
        ...     white = 0xffffff
        >>> Color.get_member(0)
        Color.black = 0
        >>> Color.get_member(0x777777, None)

        """
        for member in cls.__members__.items():
            if member[1].value == value:
                return member[1]
        return default
