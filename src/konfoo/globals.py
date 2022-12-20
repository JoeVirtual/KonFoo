# -*- coding: utf-8 -*-
"""
globals.py
~~~~~~~~~~
Package global definitions.

:copyright: (c) 2015-2022 by Jochen Gerhaeusser.
:license: BSD, see LICENSE for details
"""
from __future__ import annotations

from .categories import Category
from .enums import Enumeration


class ItemClass(Enumeration):
    Field: ItemClass = 1
    Container: ItemClass = 2
    Pointer: ItemClass = 3
    Structure: ItemClass = 10
    Sequence: ItemClass = 11
    Array: ItemClass = 12
    Stream: ItemClass = 20
    String: ItemClass = 21
    Float: ItemClass = 30
    Double: ItemClass = 31
    Decimal: ItemClass = 40
    Bit: ItemClass = 41
    Byte: ItemClass = 42
    Char: ItemClass = 43
    Signed: ItemClass = 44
    Unsigned: ItemClass = 45
    Bitset: ItemClass = 46
    Bool: ItemClass = 47
    Enum: ItemClass = 48
    Scaled: ItemClass = 49
    Fraction: ItemClass = 50
    Bipolar: ItemClass = 51
    Unipolar: ItemClass = 52
    Datetime: ItemClass = 53
    IPAddress: ItemClass = 54


class Byteorder(Category):
    """ Byte order categories."""
    #: Byte order is defined by the de-/serializer.
    auto: Byteorder = 'auto'
    #: Byte order is big endian.
    big: Byteorder = 'big'
    #: Byte order is big little.
    little: Byteorder = 'little'


#: Default byte order of the de-/serializer.
BYTEORDER: Byteorder = Byteorder.little


def clamp(value: int | float,
          minimum: int | float,
          maximum: int | float) -> int | float:
    """ Returns the *value* limited between the *minimum* and *maximum* value,
    whereby the *maximum* value wins over the *minimum* value.

    Example:

    >>> clamp(64, 0, 255)
    64
    >>> clamp(-128, 0, 255)
    0
    >>> clamp(0, 127, -128)
    -128
    """
    return min(max(value, minimum), maximum)
