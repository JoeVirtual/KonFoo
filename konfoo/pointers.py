# -*- coding: utf-8 -*-
"""
    pointers.py
    ~~~~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details
"""

from .globals import BYTEORDER

from .core import (
    Pointer, StructurePointer, ArrayPointer, StreamPointer,
    StringPointer,
    RelativePointer, StructureRelativePointer, ArrayRelativePointer,
    StreamRelativePointer, StringRelativePointer,
    Float)

from .fields import (
    Signed8, Signed16, Signed32,
    Unsigned8, Unsigned16, Unsigned32)


class Pointer8(Pointer):
    """ A `Pointer8` field is a :class:`Pointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class Pointer16(Pointer):
    """ A `Pointer16` field is a :class:`Pointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class Pointer32(Pointer):
    """ A `Pointer32` field is a :class:`Pointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class Pointer64(Pointer):
    """ A `Pointer64` field is a :class:`Pointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 8
        # Field bit size
        self._bit_size = 64


class StructurePointer8(StructurePointer):
    """ A `StructurePointer8` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class StructurePointer16(StructurePointer):
    """ A `StructurePointer16` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of two byte.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class StructurePointer32(StructurePointer):
    """ A `StructurePointer32` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of four byte.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class ArrayPointer8(ArrayPointer):
    """ A `ArrayPointer8` field is a :class:`ArrayPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class ArrayPointer16(ArrayPointer):
    """ A `ArrayPointer16` field is a :class:`ArrayPointer` field
    with a :class:`Field` *size* of two byte.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class ArrayPointer32(ArrayPointer):
    """ A `ArrayPointer32` field is a :class:`ArrayPointer` field
    with a :class:`Field` *size* of four byte.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class StreamPointer8(StreamPointer):
    """ A `StreamPointer8` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class StreamPointer16(StreamPointer):
    """ A `StreamPointer16` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class StreamPointer32(StreamPointer):
    """ A `StreamPointer32` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class StringPointer8(StringPointer):
    """ A `StringPointer8` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class StringPointer16(StringPointer):
    """ A `StringPointer16` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class StringPointer32(StringPointer):
    """ A `StringPointer32` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class FloatPointer(Pointer):
    """ A `FloatPointer` field is a :class:`Pointer` field
    which refers to a :class:`Float` field.
    """

    def __init__(self, address=None, byte_order=BYTEORDER):
        super().__init__(Float(), address, byte_order=byte_order)


class Signed8Pointer(Pointer):
    """ A `FloatPointer` field is a :class:`Pointer` field
    which refers to a :class:`Signed8` field.
    """

    def __init__(self, address=None, byte_order=BYTEORDER):
        super().__init__(Signed8(), address, byte_order=byte_order)


class Signed16Pointer(Pointer):
    """ A `Signed16Pointer` field is a :class:`Pointer` field
    which refers to a :class:`Signed16` field.
    """

    def __init__(self, address=None, byte_order=BYTEORDER):
        super().__init__(Signed16(), address, byte_order=byte_order)


class Signed32Pointer(Pointer):
    """ A `Signed32Pointer` field is a :class:`Pointer` field
    which refers to a :class:`Signed32` field.
    """

    def __init__(self, address=None, byte_order=BYTEORDER):
        super().__init__(Signed32(), address, byte_order=byte_order)


class Unsigned8Pointer(Pointer):
    """ A `Unsigned8Pointer` field is a :class:`Pointer` field
    which refers to a :class:`Unsigned8` field.
    """

    def __init__(self, address=None, byte_order=BYTEORDER):
        super().__init__(Unsigned8(), address, byte_order=byte_order)


class Unsigned16Pointer(Pointer):
    """ A `Unsigned16Pointer` field is a :class:`Pointer` field
    which refers to a :class:`Unsigned16` field.
    """

    def __init__(self, address=None, byte_order=BYTEORDER):
        super().__init__(Unsigned16(), address, byte_order=byte_order)


class Unsigned32Pointer(Pointer):
    """ A `Unsigned32Pointer` field is a :class:`Pointer` field
    which refers to a :class:`Unsigned32` field.
    """

    def __init__(self, address=None, byte_order=BYTEORDER):
        super().__init__(Unsigned32(), address, byte_order=byte_order)


class RelativePointer8(RelativePointer):
    """ A `RelativePointer8` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class RelativePointer16(RelativePointer):
    """ A `RelativePointer16` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class RelativePointer32(RelativePointer):
    """ A `RelativePointer32` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class RelativePointer64(RelativePointer):
    """ A `RelativePointer64` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 8
        # Field bit size
        self._bit_size = 64


class StructureRelativePointer8(StructureRelativePointer):
    """ A `StructureRelativePointer8` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class StructureRelativePointer16(StructureRelativePointer):
    """ A `StructureRelativePointer16` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of two byte.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class StructureRelativePointer32(StructureRelativePointer):
    """ A `StructureRelativePointer32` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of four byte.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class ArrayRelativePointer8(ArrayRelativePointer):
    """ A `ArrayRelativePointer8` field is a :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class ArrayRelativePointer16(ArrayRelativePointer):
    """ A `ArrayRelativePointer16` field is a :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of two byte.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class ArrayRelativePointer32(ArrayRelativePointer):
    """ A `ArrayRelativePointer32` field is a :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of four byte.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class StreamRelativePointer8(StreamRelativePointer):
    """ A `StreamRelativePointer8` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class StreamRelativePointer16(StreamRelativePointer):
    """ A `StreamRelativePointer16` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of two byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class StreamRelativePointer32(StreamRelativePointer):
    """ A `StreamRelativePointer32` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of four byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32


class StringRelativePointer8(StringRelativePointer):
    """ A `StringRelativePointer8` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 1
        # Field bit size
        self._bit_size = 8


class StringRelativePointer16(StringRelativePointer):
    """ A `StringRelativePointer16` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of two byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 2
        # Field bit size
        self._bit_size = 16


class StringRelativePointer32(StringRelativePointer):
    """ A `StringRelativePointer32` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of four byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32
