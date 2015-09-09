# -*- coding: utf-8 -*-
"""
    fields.py
    ~~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD-style, see LICENSE for details
"""

from .core import Enumeration, Byteorder, \
    Float, Decimal, Signed, Unsigned, Bitset, Bool, Enum, Scaled, Bipolar, Unipolar, \
    Pointer, StreamPointer, RelativePointer, StreamRelativePointer


class Decimal8(Decimal):
    """A `Decimal8` field is a signed :class:`Decimal` field with
    a *size* of one byte and is by default signed.
    """

    def __init__(self, signed=False):
        super().__init__(bit_size=8, signed=signed)


class Decimal16(Decimal):
    """A `Decimal16` field is a :class:`Decimal` field with a *size* of
    two bytes and is by default signed.
    """

    def __init__(self, signed=False):
        super().__init__(bit_size=16, signed=signed)


class Decimal24(Decimal):
    """A `Decimal24` field is a :class:`Decimal` field with a *size* of
    three bytes and is by default signed.
    """

    def __init__(self, signed=False):
        super().__init__(bit_size=24, signed=signed)


class Decimal32(Decimal):
    """A `Decimal32` field is a :class:`Decimal` field with a *size* of
    four bytes and is by default signed.
    """

    def __init__(self, signed=False):
        super().__init__(bit_size=32, signed=signed)


class Signed8(Signed):
    """A `Signed8` field is a :class:`Signed` field with a *size* of
    one byte.
    """

    def __init__(self):
        super().__init__(bit_size=8)


class Signed16(Signed):
    """A `Signed16` field is a :class:`Signed` field with a *size* of
    two bytes.
    """

    def __init__(self):
        super().__init__(bit_size=16)


class Signed24(Signed):
    """A `Signed24` field is a :class:`Signed` field with a *size* of
    three bytes.
    """

    def __init__(self):
        super().__init__(bit_size=24)


class Signed32(Signed):
    """A `Signed32` field is a :class:`Signed` field with a *size* of
    four bytes.
    """

    def __init__(self):
        super().__init__(bit_size=32)


class Unsigned8(Unsigned):
    """A `Unsigned8` field is a :class:`Unsigned` field with a *size* of
    one byte.
    """

    def __init__(self):
        super().__init__(bit_size=8)


class Unsigned16(Unsigned):
    """A `Unsigned16` field is a :class:`Unsigned` field with a *size* of
    two bytes.
    """

    def __init__(self):
        super().__init__(bit_size=16)


class Unsigned24(Unsigned):
    """A `Unsigned24` field is a :class:`Unsigned` field with a *size* of
    three bytes.
    """

    def __init__(self):
        super().__init__(bit_size=24)


class Unsigned32(Unsigned):
    """A `Unsigned32` field is a :class:`Unsigned` field with a *size* of
    four bytes.
    """

    def __init__(self):
        super().__init__(bit_size=32)


class Bitset8(Bitset):
    """A `Bitset8` field is a :class:`Bitset` field with a *size* of
    one byte and the coding byteorder is 'little' endian.
    """

    def __init__(self, byte_order=Byteorder.little):
        super().__init__(8, 1, byte_order)


class Bitset16(Bitset):
    """A `Bitset16` field is a :class:`Bitset` field with a *size* of
    two bytes and the default coding byteorder is 'little' endian.
    """

    def __init__(self, byte_order=Byteorder.little):
        super().__init__(16, 2, byte_order)


class Bitset24(Bitset):
    """A `Bitset24` field is a :class:`Bitset` field with a *size* of
    three bytes and the coding default byteorder is 'little' endian.
    """

    def __init__(self, byte_order=Byteorder.little):
        super().__init__(24, 3, byte_order)


class Bitset32(Bitset):
    """A `Bitset32` field is a :class:`Bitset` field with a *size* of
     four bytes and the default coding byteorder is 'little' endian.
    """

    def __init__(self, byte_order=Byteorder.little):
        super().__init__(32, 4, byte_order)


class Bool8(Bool):
    """A `Bool8` field is a :class:`Bool` field with a *size* of
    one byte.
    """

    def __init__(self):
        super().__init__(bit_size=8)


class Bool16(Bool):
    """A `Bool16` field is a :class:`Bool` field with a *size* of
    two bytes.
    """

    def __init__(self):
        super().__init__(bit_size=16)


class Bool24(Bool):
    """A `Bool24` field is a :class:`Bool` field with a *size* of
    three bytes.
    """

    def __init__(self):
        super().__init__(bit_size=16)


class Bool32(Bool):
    """A `Bool32` field is a :class:`Bool` field with a *size* of
    four bytes.
    """

    def __init__(self):
        super().__init__(bit_size=32)


class Antivalent(Enum):
    """A `Antivalent` field is a :class:`Enum` field with a *size* of
    two bits and a fix assigned enumeration.
    """

    class Validity(Enumeration):
        error = 0
        invalid = 1
        valid = 2
        undefined = 3

    def __init__(self, align_to=None):
        super().__init__(bit_size=2, align_to=align_to, enumeration=Antivalent.Validity)


class Enum4(Enum):
    """A `Enum4` field is a :class:`Enum` field with a *size* of
    four bits.
    """

    def __init__(self, align_to=None, enumeration=None):
        super().__init__(bit_size=4, align_to=align_to, enumeration=enumeration)


class Enum8(Enum):
    """A `Enum8` field is a :class:`Enum` field with a *size* of
    one byte.
    """

    def __init__(self, enumeration=None):
        super().__init__(bit_size=8, enumeration=enumeration)


class Enum16(Enum):
    """A `Enum16` field is a :class:`Enum` field with a *size* of
    two bytes.
    """

    def __init__(self, enumeration=None):
        super().__init__(bit_size=16, enumeration=enumeration)


class Enum24(Enum):
    """A `Enum24` field is a :class:`Enum` field with a *size* of
    three bytes.
    """

    def __init__(self, enumeration=None):
        super().__init__(bit_size=24, enumeration=enumeration)


class Enum32(Enum):
    """A `Enum32` field is a :class:`Enum` field with a *size* of
    four bytes.
    """

    def __init__(self, enumeration=None):
        super().__init__(bit_size=32, enumeration=enumeration)


class Scaled8(Scaled):
    """A `Scaled8` field is a :class:`Scaled` field with a *size* of
    onw byte.
    """

    def __init__(self, scale):
        super().__init__(scale, bit_size=8)


class Scaled16(Scaled):
    """A `Scaled16` field is a :class:`Scaled` field with a *size* of
    two bytes.
    """

    def __init__(self, scale):
        super().__init__(scale, bit_size=16)


class Scaled24(Scaled):
    """A `Scaled24` field is a :class:`Scaled` field with a *size* of
    three bytes.
    """

    def __init__(self, scale):
        super().__init__(scale, bit_size=24)


class Scaled32(Scaled):
    """A `Scaled32` field is a :class:`Scaled` field with a *size* of
    four bytes.
    """

    def __init__(self, scale):
        super().__init__(scale, bit_size=16)


class Bipolar2(Bipolar):
    """A `Bipolar2` field is a :class:`Bipolar` field with a *size* of
    two bytes and an integer part of two bits.
    """

    def __init__(self):
        super().__init__(bits_integer=2, bit_size=16)


class Bipolar4(Bipolar):
    """A `Bipolar4` field is a :class:`Bipolar` field with a *size* of
    two bytes and an integer part of four bits.
    """

    def __init__(self):
        super().__init__(bits_integer=4, bit_size=16)


class Unipolar2(Unipolar):
    """A `Unipolar2` field is a :class:`Unipolar` field with a *size* of
    two bytes and an integer part of two bits.
    """

    def __init__(self):
        super().__init__(bits_integer=2, bit_size=16)


class Pointer8(Pointer):
    """A `Pointer8` field is a :class:`Pointer` field with a *size* of
    one byte.
    """

    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class Pointer16(Pointer):
    """A `Pointer16` field is a :class:`Pointer` field with a *size* of
    two bytes.
    """

    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class Pointer32(Pointer):
    """A `Pointer16` field is a :class:`Pointer` field with a *size* of
    four bytes.
    """

    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class Pointer64(Pointer):
    """A `Pointer16` field is a :class:`Pointer` field with a *size* of
    eight bytes.
    """

    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 8
        # Field bit size
        self._bit_size = 64


class StreamPointer8(StreamPointer):
    """A `StreamPointer8` field is a :class:`StreamPointer` field
    with a `Pointer` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class StreamPointer16(StreamPointer):
    """A `StreamPointer16` field is a :class:`StreamPointer` field
    with a `Pointer` *size* of two bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class StreamPointer32(StreamPointer):
    """A `StreamPointer32` field is a :class:`StreamPointer` field
    with a `Pointer` *size* of four bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class RelativePointer8(RelativePointer):
    """A `RelativePointer8` field is a :class:`RelativePointer` field
    with a *size* of one byte.
    """

    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class RelativePointer16(RelativePointer):
    """A `RelativePointer16` field is a :class:`RelativePointer` field
    with a *size* of two bytes.
    """

    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class RelativePointer32(RelativePointer):
    """A `RelativePointer32` field is a :class:`RelativePointer` field
    with a *size* of four bytes.
    """

    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class RelativePointer64(RelativePointer):
    """A `RelativePointer64` field is a :class:`RelativePointer` field
    with a *size* of eight bytes.
    """

    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 8
        # Field bit size
        self._bit_size = 64


class StreamRelativePointer8(StreamRelativePointer):
    """A `StreamRelativePointer8` field is a :class:`StreamRelativePointer`
    field with a `RelativePointer` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class StreamRelativePointer16(StreamRelativePointer):
    """A `StreamRelativePointer16` field is a :class:`StreamRelativePointer`
    field with a `RelativePointer` *size* of two byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class StreamRelativePointer32(StreamRelativePointer):
    """A `StreamRelativePointer32` field is a :class:`StreamRelativePointer`
    field with a `RelativePointer` *size* of four byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class FloatPointer(Pointer):
    def __init__(self, address=None, byte_order=Byteorder.default):
        super().__init__(Float(), address, byte_order=byte_order)


class Signed8Pointer(Pointer):
    def __init__(self, address=None, byte_order=Byteorder.default):
        super().__init__(Signed8(), address, byte_order=byte_order)


class Signed16Pointer(Pointer):
    def __init__(self, address=None, byte_order=Byteorder.default):
        super().__init__(Signed16(), address, byte_order=byte_order)


class Signed32Pointer(Pointer):
    def __init__(self, address=None, byte_order=Byteorder.default):
        super().__init__(Signed32(), address, byte_order=byte_order)


class Unsigned8Pointer(Pointer):
    def __init__(self, address=None, byte_order=Byteorder.default):
        super().__init__(Unsigned8(), address, byte_order=byte_order)


class Unsigned16Pointer(Pointer):
    def __init__(self, address=None, byte_order=Byteorder.default):
        super().__init__(Unsigned16(), address, byte_order=byte_order)


class Unsigned32Pointer(Pointer):
    def __init__(self, address=None, byte_order=Byteorder.default):
        super().__init__(Unsigned32(), address, byte_order=byte_order)
