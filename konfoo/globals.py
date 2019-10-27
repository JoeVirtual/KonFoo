# -*- coding: utf-8 -*-
"""
    globals.py
    ~~~~~~~~~~
    <Add description of the module here>.

    :copyright: (c) 2015-2019 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details
"""

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
    Double = 31
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
    IPAddress = 54


class Byteorder(Category):
    """ Byte order categories."""
    auto = 'auto'
    little = 'little'
    big = 'big'


#: Default Byteorder
BYTEORDER = Byteorder.little


def clamp(value, minimum, maximum):
    """ Returns the *value* limited between *minimum* and *maximum*
    whereby the *maximum* wins over the *minimum*.

    Example:

    >>> clamp(64, 0, 255)
    64
    >>> clamp(-128, 0, 255)
    0
    >>> clamp(0, 127, -128)
    -128
    """
    return min(max(value, minimum), maximum)
