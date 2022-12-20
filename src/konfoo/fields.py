# -*- coding: utf-8 -*-
"""
fields.py
~~~~~~~~~
Pre-defined decimal field variants.

:copyright: (c) 2015-2022 by Jochen Gerhaeusser.
:license: BSD, see LICENSE for details
"""
from __future__ import annotations

from typing import Literal

from .core import (
    Decimal, Signed, Unsigned, Bitset, Bool, Enum, Scaled, Bipolar, Unipolar)
from .enums import Enumeration
from .globals import Byteorder


class Decimal8(Decimal):
    """ The :class:`Decimal8` field is a :class:`Decimal` field with a *size* of
    one byte and is by default unsigned.
    """

    def __init__(self,
                 signed: bool = False,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=8,
                         signed=signed,
                         byte_order=byte_order)


class Decimal16(Decimal):
    """ The :class:`Decimal16` field is a :class:`Decimal` field with a *size* of
    two bytes and is by default unsigned.
    """

    def __init__(self,
                 signed: bool = False,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=16,
                         signed=signed,
                         byte_order=byte_order)


class Decimal24(Decimal):
    """ The :class:`Decimal24` field is a :class:`Decimal` field with a *size* of
    three bytes and is by default unsigned.
    """

    def __init__(self,
                 signed: bool = False,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=24,
                         signed=signed,
                         byte_order=byte_order)


class Decimal32(Decimal):
    """ The :class:`Decimal32` field is a :class:`Decimal` field with a *size* of
    four bytes and is by default unsigned.
    """

    def __init__(self,
                 signed: bool = False,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=32,
                         signed=signed,
                         byte_order=byte_order)


class Decimal64(Decimal):
    """ The :class:`Decimal64` field is a :class:`Decimal` field with a *size* of
    eight bytes and is by default unsigned.
    """

    def __init__(self,
                 signed: bool = False,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=64,
                         signed=signed,
                         byte_order=byte_order)


class Signed8(Signed):
    """ The :class:`Signed8` field is a :class:`Signed` field with a *size* of
    one byte.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=8,
                         byte_order=byte_order)


class Signed16(Signed):
    """ The :class:`Signed16` field is a :class:`Signed` field with a *size* of
    two bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=16,
                         byte_order=byte_order)


class Signed24(Signed):
    """ The :class:`Signed24` field is a :class:`Signed` field with a *size* of
    three bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=24,
                         byte_order=byte_order)


class Signed32(Signed):
    """ The :class:`Signed32` field is a :class:`Signed` field with a *size* of
    four bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=32, byte_order=byte_order)


class Signed64(Signed):
    """ The :class:`Signed64` field is a :class:`Signed` field with a *size* of
    eight bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=64,
                         byte_order=byte_order)


class Unsigned8(Unsigned):
    """ The :class:`Unsigned8` field is an :class:`Unsigned` field with a *size* of
    one byte.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=8,
                         byte_order=byte_order)


class Unsigned16(Unsigned):
    """ The :class:`Unsigned16` field is an :class:`Unsigned` field
    with a *size* of two bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=16,
                         byte_order=byte_order)


class Unsigned24(Unsigned):
    """ The :class:`Unsigned24` field is an :class:`Unsigned` field
    with a *size* of three bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=24,
                         byte_order=byte_order)


class Unsigned32(Unsigned):
    """ The :class:`Unsigned32` field is an :class:`Unsigned` field
    with a *size* of four bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=32,
                         byte_order=byte_order)


class Unsigned64(Unsigned):
    """ The :class:`Unsigned64` field is an :class:`Unsigned` field
    with a *size* of eight bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=64,
                         byte_order=byte_order)


class Bitset8(Bitset):
    """ The :class:`Bitset8` field is a :class:`Bitset` field
    with a *size* of one byte.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=8,
                         byte_order=byte_order)


class Bitset16(Bitset):
    """ The :class:`Bitset16` field is a :class:`Bitset` field
    with a *size* of two bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=16,
                         byte_order=byte_order)


class Bitset24(Bitset):
    """ The :class:`Bitset24` field is a :class:`Bitset` field
    with a *size* of three bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=24,
                         byte_order=byte_order)


class Bitset32(Bitset):
    """ The :class:`Bitset32` field is a :class:`Bitset` field
    with a *size* of four bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=32,
                         byte_order=byte_order)


class Bitset64(Bitset):
    """ The :class:`Bitset64` field is a :class:`Bitset` field
    with a *size* of eight bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=64,
                         byte_order=byte_order)


class Bool8(Bool):
    """ The :class:`Bool8` field is a :class:`Bool` field
    with a *size* of one byte.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=8,
                         byte_order=byte_order)


class Bool16(Bool):
    """ The :class:`Bool16` field is a :class:`Bool` field
    with a *size* of two bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=16,
                         byte_order=byte_order)


class Bool24(Bool):
    """ The :class:`Bool24` field is a :class:`Bool` field
    with a *size* of three bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=24,
                         byte_order=byte_order)


class Bool32(Bool):
    """ The :class:`Bool32` field is a :class:`Bool` field
    with a *size* of four bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=32,
                         byte_order=byte_order)


class Bool64(Bool):
    """ The :class:`Bool64` field is a :class:`Bool` field
    with a *size* of eight bytes.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=64,
                         byte_order=byte_order)


class Antivalent(Enum):
    """ The :class:`Antivalent` field is an :class:`Enum` field
    with a *size* of two bits and a fix assigned enumeration.
    """

    class Validity(Enumeration):
        error = 0
        correct = 1
        forced = 2
        undefined = 3

    def __init__(self,
                 align_to: int | None = None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=2,
                         align_to=align_to,
                         enumeration=Antivalent.Validity,
                         byte_order=byte_order)


class Enum4(Enum):
    """ The :class:`Enum4` field is an :class:`Enum` field
    with a *size* of four bits.
    """

    def __init__(self,
                 align_to: int | None = None,
                 enumeration: Enumeration | None = None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=4,
                         align_to=align_to,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Enum8(Enum):
    """ The :class:`Enum8` field is an :class:`Enum` field
    with a *size* of one byte.
    """

    def __init__(self,
                 enumeration: Enumeration | None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=8,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Enum16(Enum):
    """ The :class:`Enum16` field is an :class:`Enum` field
    with a *size* of two bytes.
    """

    def __init__(self,
                 enumeration: Enumeration | None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=16,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Enum24(Enum):
    """ The :class:`Enum24` field is an :class:`Enum` field
    with a *size* of three bytes.
    """

    def __init__(self,
                 enumeration: Enumeration | None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=24,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Enum32(Enum):
    """ The :class:`Enum32` field is an :class:`Enum` field
    with a *size* of four bytes.
    """

    def __init__(self,
                 enumeration: Enumeration | None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=32,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Enum64(Enum):
    """ The :class:`Enum64` field is an :class:`Enum` field
    with a *size* of eight bytes.
    """

    def __init__(self,
                 enumeration: Enumeration | None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=64,
                         enumeration=enumeration,
                         byte_order=byte_order)


class Scaled8(Scaled):
    """ The :class:`Scaled8` field is a :class:`Scaled` field
    with a *size* of one byte.
    """

    def __init__(self,
                 scale: float | int,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(scale=scale,
                         bit_size=8,
                         byte_order=byte_order)


class Scaled16(Scaled):
    """ The :class:`Scaled16` field is a :class:`Scaled` field
    with a *size* of two bytes.
    """

    def __init__(self,
                 scale: float | int,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(scale=scale,
                         bit_size=16,
                         byte_order=byte_order)


class Scaled24(Scaled):
    """ The :class:`Scaled24` field is a :class:`Scaled` field
    with a *size* of three bytes.
    """

    def __init__(self,
                 scale: float | int,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(scale=scale,
                         bit_size=24,
                         byte_order=byte_order)


class Scaled32(Scaled):
    """ The :class:`Scaled32` field is a :class:`Scaled` field
    with a *size* of four bytes.
    """

    def __init__(self,
                 scale: float | int,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(scale=scale,
                         bit_size=32,
                         byte_order=byte_order)


class Scaled64(Scaled):
    """ The :class:`Scaled64` field is a :class:`Scaled` field
    with a *size* of eight bytes.
    """

    def __init__(self,
                 scale: float | int,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(scale=scale,
                         bit_size=64,
                         byte_order=byte_order)


class Bipolar2(Bipolar):
    """ The :class:`Bipolar2` field is a :class:`Bipolar` field
    with a *size* of two bytes and an integer part of two bits.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bits_integer=2,
                         bit_size=16,
                         byte_order=byte_order)


class Bipolar4(Bipolar):
    """ The :class:`Bipolar4` field is a :class:`Bipolar` field
    with a *size* of two bytes and an integer part of four bits.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bits_integer=4,
                         bit_size=16,
                         byte_order=byte_order)


class Unipolar2(Unipolar):
    """ The :class:`Unipolar2` field is an :class:`Unipolar` field
    with a *size* of two bytes and an integer part of two bits.
    """

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bits_integer=2,
                         bit_size=16,
                         byte_order=byte_order)
