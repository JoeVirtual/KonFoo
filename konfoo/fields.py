# -*- coding: utf-8 -*-
"""
    fields.py
    ~~~~~~~~~
    <Add descritpion of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD-style, see LICENSE for details
"""

from .core import Enumeration, Byteorder, \
    Float, Decimal, Signed, Unsigned, Bitset, Bool, Enum, Scaled, Bipolar, Unipolar, \
    Pointer, StreamPointer, \
    RelativePointer, StreamRelativePointer


class Decimal8(Decimal):
    def __init__(self, signed=False):
        super().__init__(bit_size=8, signed=signed)


class Decimal16(Decimal):
    def __init__(self, signed=False):
        super().__init__(bit_size=16, signed=signed)


class Decimal24(Decimal):
    def __init__(self, signed=False):
        super().__init__(bit_size=24, signed=signed)


class Decimal32(Decimal):
    def __init__(self, signed=False):
        super().__init__(bit_size=32, signed=signed)


class Signed8(Signed):
    def __init__(self):
        super().__init__(bit_size=8)


class Signed16(Signed):
    def __init__(self):
        super().__init__(bit_size=16)


class Signed24(Signed):
    def __init__(self):
        super().__init__(bit_size=24)


class Signed32(Signed):
    def __init__(self):
        super().__init__(bit_size=32)


class Unsigned8(Unsigned):
    def __init__(self):
        super().__init__(bit_size=8)


class Unsigned16(Unsigned):
    def __init__(self):
        super().__init__(bit_size=16)


class Unsigned24(Unsigned):
    def __init__(self):
        super().__init__(bit_size=24)


class Unsigned32(Unsigned):
    def __init__(self):
        super().__init__(bit_size=32)


class Bitset8(Bitset):
    def __init__(self, byte_order=Byteorder.little):
        super().__init__(8, 1, byte_order)


class Bitset16(Bitset):
    def __init__(self, byte_order=Byteorder.little):
        super().__init__(16, 2, byte_order)


class Bitset24(Bitset):
    def __init__(self, byte_order=Byteorder.little):
        super().__init__(24, 3, byte_order)


class Bitset32(Bitset):
    def __init__(self, byte_order=Byteorder.little):
        super().__init__(32, 4, byte_order)


class Bool8(Bool):
    def __init__(self):
        super().__init__(bit_size=8)


class Bool16(Bool):
    def __init__(self):
        super().__init__(bit_size=16)


class Bool24(Bool):
    def __init__(self):
        super().__init__(bit_size=16)


class Bool32(Bool):
    def __init__(self):
        super().__init__(bit_size=32)


class Antivalent(Enum):
    class Validity(Enumeration):
        error = 0
        invalid = 1
        valid = 2
        undefined = 3

    def __init__(self, align_to=None):
        super().__init__(bit_size=2, align_to=align_to, enumeration=Antivalent.Validity)


class Enum4(Enum):
    def __init__(self, align_to=None, enumeration=None):
        super().__init__(bit_size=4, align_to=align_to, enumeration=enumeration)


class Enum8(Enum):
    def __init__(self, enumeration=None):
        super().__init__(bit_size=8, enumeration=enumeration)


class Enum16(Enum):
    def __init__(self, enumeration=None):
        super().__init__(bit_size=16, enumeration=enumeration)


class Enum24(Enum):
    def __init__(self, enumeration=None):
        super().__init__(bit_size=24, enumeration=enumeration)


class Enum32(Enum):
    def __init__(self, enumeration=None):
        super().__init__(bit_size=32, enumeration=enumeration)


class Scaled8(Scaled):
    def __init__(self, scale):
        super().__init__(scale, bit_size=8)


class Scaled16(Scaled):
    def __init__(self, scale):
        super().__init__(scale, bit_size=16)


class Scaled24(Scaled):
    def __init__(self, scale):
        super().__init__(scale, bit_size=24)


class Scaled32(Scaled):
    def __init__(self, scale):
        super().__init__(scale, bit_size=16)


class Bipolar2(Bipolar):
    def __init__(self):
        super().__init__(bits_integer=2, bit_size=16)


class Bipolar4(Bipolar):
    def __init__(self):
        super().__init__(bits_integer=4, bit_size=16)


class Unipolar2(Unipolar):
    def __init__(self):
        super().__init__(bits_integer=2, bit_size=16)


class Pointer8(Pointer):
    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class Pointer16(Pointer):
    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class Pointer32(Pointer):
    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class Pointer64(Pointer):
    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 8
        # Field bit size
        self._bit_size = 64


class StreamPointer8(StreamPointer):
    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class StreamPointer16(StreamPointer):
    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class StreamPointer32(StreamPointer):
    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class RelativePointer8(RelativePointer):
    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class RelativePointer16(RelativePointer):
    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class RelativePointer32(RelativePointer):
    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class RelativePointer64(RelativePointer):
    def __init__(self, template=None, address=None, byte_order=Byteorder.default):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 8
        # Field bit size
        self._bit_size = 64


class StreamRelativePointer8(StreamRelativePointer):
    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class StreamRelativePointer16(StreamRelativePointer):
    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class StreamRelativePointer32(StreamRelativePointer):
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
