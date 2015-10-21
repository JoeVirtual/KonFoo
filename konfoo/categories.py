# -*- coding: utf-8 -*-
"""
    categories.py
    ~~~~~~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD-style, see LICENSE for details
"""

import enum


class Category(enum.Enum):
    """The `Category` class is a is a subclass of the :class:`~enum.Enum` class
    provided by the Python standard module :mod:`enum` and extends its
    base class with methods

    * to `describe` a specific `Category` member by its `name`, `value` pair
    * to list the `member names` of a `Category`
    * to list the `member values` of a `Category`
    * to `get` the `value` of the `Category` member with the matching `name`
    * to `get` the `name` of the `Category` member with the matching `value`
    * to `get` the `member` of the `Category` with the matching `value`

    Example:

    >>> class Format(Category):
    ...     hour = 'hh'
    ...     minute = 'mm'
    ...     second = 'ss'
    >>> str(Format.hour)
    '(hour, hh)'
    >>> repr(Format.hour)
    "Format.hour = 'hh'"
    >>> Format.hour.describe()
    ('hour', 'hh')
    >>> Format.names()
    ['hour', 'minute', 'second']
    >>> Format.values()
    ['hh', 'mm', 'ss']
    >>> Format.get_value('hour')
    'hh'
    >>> Format.get_name('hh')
    'hour'
    >>> Format.get_member('hh')
    Format.hour = 'hh'
    """

    def __str__(self):
        """Return str(self).

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> str(Format.hour)
        '(hour, hh)'
        """
        return "({0.name!s}, {0.value!s})".format(self)

    def __repr__(self):
        """Return repr(self). See help(type(self)) for accurate signature.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> repr(Format.hour)
        "Format.hour = 'hh'"
        """
        return self.__class__.__name__ + ".{0.name!s} = {0.value!r}".format(self)

    def describe(self):
        """Returns the `name`, `value` pair to describe a specific `Category` member.

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
    def names(cls):
        """Returns a list of the member `names` of a `Category`.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> Format.names()
        ['hour', 'minute', 'second']
        """
        return [member[1].name for member in cls.__members__.items()]

    @classmethod
    def values(cls):
        """Returns a list of the member `values` of a `Category`.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> Format.values()
        ['hh', 'mm', 'ss']
        """
        return [member[1].value for member in cls.__members__.items()]

    @classmethod
    def get_name(cls, value):
        """Returns the `name` of the `Category` member with the matching *value*
        or a empty string if no member match.

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
        for v, n in zip(cls.values(), cls.names()):
            if v == value:
                return n
        return str()

    @classmethod
    def get_value(cls, name):
        """Returns the `value` of the `Category` member with the matching *name*
        or `None` if no member match.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> Format.get_value('hour')
        'hh'
        >>> Format.get_value('day')

        """
        for v, n in zip(cls.values(), cls.names()):
            if n == name:
                return v
        return None

    @classmethod
    def get_member(cls, value, default=None):
        """Returns the first `Category` member with the matching *value*
        or the specified *default* value if no member match.

        Example:

        >>> class Format(Category):
        ...     hour = 'hh'
        ...     minute = 'mm'
        ...     second = 'ss'
        >>> Format.get_member('hh')
        Format.hour = 'hh'
        >>> Format.get_member('day', None)

        """
        for member in cls.__members__.items():
            if member[1].value == value:
                return member[1]
        return default
