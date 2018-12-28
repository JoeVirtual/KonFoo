# -*- coding: utf-8 -*-
"""
    fields.py
    ~~~~~~~~~
    <Add description of the module here>.

    :copyright: (c) 2015-2018 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details
"""

from .core import (
    Decimal, Signed, Unsigned, Bitset, Bool, Enum, Scaled, Bipolar, Unipolar)
from .enums import Enumeration


class Decimal8(Decimal):
    """ A `Decimal8` field is a :class:`Decimal` field with a *size* of
    one byte and is by default unsigned.
    """

    def __init__(self, signed=False, byte_order='auto'):
        super().__init__(bit_size=8,
                         signed=signed,
                         byte_order=byte_order)


class Decimal16(Decimal):
    """ A `Decimal16` field is a :class:`Decimal` field with a *size* of
    two bytes and is by default unsigned.
    """

    def __init__(self, signed=False, byte_order='auto'):
        super().__init__(bit_size=16,
                         signed=signed,
                         byte_order=byte_order)


class Decimal24(Decimal):
    """ A `Decimal24` field is a :class:`Decimal` field with a *size* of
    three bytes and is by default unsigned.
    """

    def __init__(self, signed=False, byte_order='auto'):
        super().__init__(bit_size=24,
                         signed=signed,
                         byte_order=byte_order)


class Decimal32(Decimal):
    """ A `Decimal32` field is a :class:`Decimal` field with a *size* of
    four bytes and is by default unsigned.
    """

    def __init__(self, signed=False, byte_order='auto'):
        super().__init__(bit_size=32,
                         signed=signed,
                         byte_order=byte_order)


class Decimal64(Decimal):
    """ A `Decimal64` field is a :class:`Decimal` field with a *size* of
    eight bytes and is by default unsigned.
    """

    def __init__(self, signed=False, byte_order='auto'):
        super().__init__(bit_size=64,
                         signed=signed,
                         byte_order=byte_order)


class Signed8(Signed):
    """ A `Signed8` field is a :class:`Signed` field with a *size* of
    one byte.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=8,
                         byte_order=byte_order)


class Signed16(Signed):
    """ A `Signed16` field is a :class:`Signed` field with a *size* of
    two bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=16,
                         byte_order=byte_order)


class Signed24(Signed):
    """ A `Signed24` field is a :class:`Signed` field with a *size* of
    three bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=24,
                         byte_order=byte_order)


class Signed32(Signed):
    """ A `Signed32` field is a :class:`Signed` field with a *size* of
    four bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=32, byte_order=byte_order)


class Signed64(Signed):
    """ A `Signed64` field is a :class:`Signed` field with a *size* of
    eight bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=64,
                         byte_order=byte_order)


class Unsigned8(Unsigned):
    """ A `Unsigned8` field is an :class:`Unsigned` field with a *size* of
    one byte.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=8,
                         byte_order=byte_order)


class Unsigned16(Unsigned):
    """ A `Unsigned16` field is an :class:`Unsigned` field with a *size* of
    two bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=16,
                         byte_order=byte_order)


class Unsigned24(Unsigned):
    """ A `Unsigned24` field is an :class:`Unsigned` field with a *size* of
    three bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=24,
                         byte_order=byte_order)


class Unsigned32(Unsigned):
    """ A `Unsigned32` field is an :class:`Unsigned` field with a *size* of
    four bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=32,
                         byte_order=byte_order)


class Unsigned64(Unsigned):
    """ A `Unsigned64` field is an :class:`Unsigned` field with a *size* of
    eight bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=64,
                         byte_order=byte_order)


class Bitset8(Bitset):
    """ A `Bitset8` field is a :class:`Bitset` field with a *size* of
    one byte.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=8,
                         byte_order=byte_order)


class Bitset16(Bitset):
    """ A `Bitset16` field is a :class:`Bitset` field with a *size* of
    two bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=16,
                         byte_order=byte_order)


class Bitset24(Bitset):
    """ A `Bitset24` field is a :class:`Bitset` field with a *size* of
    three bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=24,
                         byte_order=byte_order)


class Bitset32(Bitset):
    """ A `Bitset32` field is a :class:`Bitset` field with a *size* of
    four bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=32,
                         byte_order=byte_order)


class Bitset64(Bitset):
    """ A `Bitset64` field is a :class:`Bitset` field with a *size* of
    eight bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=64,
                         byte_order=byte_order)


class Bool8(Bool):
    """ A `Bool8` field is a :class:`Bool` field with a *size* of
    one byte.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=8,
                         byte_order=byte_order)


class Bool16(Bool):
    """ A `Bool16` field is a :class:`Bool` field with a *size* of
    two bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=16,
                         byte_order=byte_order)


class Bool24(Bool):
    """ A `Bool24` field is a :class:`Bool` field with a *size* of
    three bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=24,
                         byte_order=byte_order)


class Bool32(Bool):
    """ A `Bool32` field is a :class:`Bool` field with a *size* of
    four bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=32,
                         byte_order=byte_order)


class Bool64(Bool):
    """ A `Bool64` field is a :class:`Bool` field with a *size* of
    eight bytes.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bit_size=64,
                         byte_order=byte_order)


class Antivalent(Enum):
    """ An `Antivalent` field is an :class:`Enum` field with a *size* of
    two bits and a fix assigned enumeration.
    """

    class Validity(Enumeration):
        error = 0
        correct = 1
        forced = 2
        undefined = 3

    def __init__(self, align_to=None, byte_order='auto'):
        super().__init__(bit_size=2,
                         align_to=align_to,
                         enumeration=Antivalent.Validity,
                         byte_order=byte_order)


class Enum4(Enum):
    """ An `Enum4` field is an :class:`Enum` field with a *size* of
    four bits.
    """

    def __init__(self, align_to=None, enumeration=None,
                 byte_order='auto'):
        super().__init__(bit_size=4,
                         align_to=align_to,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Enum8(Enum):
    """ An `Enum8` field is an :class:`Enum` field with a *size* of
    one byte.
    """

    def __init__(self, enumeration=None, byte_order='auto'):
        super().__init__(bit_size=8,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Enum16(Enum):
    """ An `Enum16` field is an :class:`Enum` field with a *size* of
    two bytes.
    """

    def __init__(self, enumeration=None, byte_order='auto'):
        super().__init__(bit_size=16,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Enum24(Enum):
    """ An `Enum24` field is an :class:`Enum` field with a *size* of
    three bytes.
    """

    def __init__(self, enumeration=None, byte_order='auto'):
        super().__init__(bit_size=24,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Enum32(Enum):
    """ An `Enum32` field is an :class:`Enum` field with a *size* of
    four bytes.
    """

    def __init__(self, enumeration=None, byte_order='auto'):
        super().__init__(bit_size=32,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Enum64(Enum):
    """ An `Enum64` field is an :class:`Enum` field with a *size* of
    eight bytes.
    """

    def __init__(self, enumeration=None, byte_order='auto'):
        super().__init__(bit_size=64,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Scaled8(Scaled):
    """ A `Scaled8` field is a :class:`Scaled` field with a *size* of
    one byte.
    """

    def __init__(self, scale, byte_order='auto'):
        super().__init__(scale=scale,
                         bit_size=8,
                         byte_order=byte_order)


class Scaled16(Scaled):
    """ A `Scaled16` field is a :class:`Scaled` field with a *size* of
    two bytes.
    """

    def __init__(self, scale, byte_order='auto'):
        super().__init__(scale=scale,
                         bit_size=16,
                         byte_order=byte_order)


class Scaled24(Scaled):
    """ A `Scaled24` field is a :class:`Scaled` field with a *size* of
    three bytes.
    """

    def __init__(self, scale, byte_order='auto'):
        super().__init__(scale=scale,
                         bit_size=24,
                         byte_order=byte_order)


class Scaled32(Scaled):
    """ A `Scaled32` field is a :class:`Scaled` field with a *size* of
    four bytes.
    """

    def __init__(self, scale, byte_order='auto'):
        super().__init__(scale=scale,
                         bit_size=32,
                         byte_order=byte_order)


class Scaled64(Scaled):
    """ A `Scaled64` field is a :class:`Scaled` field with a *size* of
    eight bytes.
    """

    def __init__(self, scale, byte_order='auto'):
        super().__init__(scale=scale,
                         bit_size=64,
                         byte_order=byte_order)


class Bipolar2(Bipolar):
    """ A `Bipolar2` field is a :class:`Bipolar` field with a *size* of
    two bytes and an integer part of two bits.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bits_integer=2,
                         bit_size=16,
                         byte_order=byte_order)


class Bipolar4(Bipolar):
    """ A `Bipolar4` field is a :class:`Bipolar` field with a *size* of
    two bytes and an integer part of four bits.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bits_integer=4,
                         bit_size=16,
                         byte_order=byte_order)


class Unipolar2(Unipolar):
    """ An `Unipolar2` field is an :class:`Unipolar` field with a *size* of
    two bytes and an integer part of two bits.
    """

    def __init__(self, byte_order='auto'):
        super().__init__(bits_integer=2,
                         bit_size=16,
                         byte_order=byte_order)
