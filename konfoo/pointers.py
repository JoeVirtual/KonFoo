# -*- coding: utf-8 -*-
"""
    pointers.py
    ~~~~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015-2017 by Jochen Gerhaeusser.
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
        # Field bit size
        self._set_bit_size(8, 8, auto_align=True)


class Pointer16(Pointer):
    """ A `Pointer16` field is a :class:`Pointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(16, 8, auto_align=True)


class Pointer24(Pointer):
    """ A `Pointer24` field is a :class:`Pointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(24, 8, auto_align=True)


class Pointer32(Pointer):
    """ A `Pointer32` field is a :class:`Pointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(32, 8, auto_align=True)


class Pointer48(Pointer):
    """ A `Pointer48` field is a :class:`Pointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(48, 8, auto_align=True)


class Pointer64(Pointer):
    """ A `Pointer64` field is a :class:`Pointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(64, 8, auto_align=True)


class StructurePointer8(StructurePointer):
    """ A `StructurePointer8` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(8, 8, auto_align=True)


class StructurePointer16(StructurePointer):
    """ A `StructurePointer16` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(16, 8, auto_align=True)


class StructurePointer24(StructurePointer):
    """ A `StructurePointer24` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(24, 8, auto_align=True)


class StructurePointer32(StructurePointer):
    """ A `StructurePointer32` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(32, 8, auto_align=True)


class StructurePointer48(StructurePointer):
    """ A `StructurePointer48` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(48, 8, auto_align=True)


class StructurePointer64(StructurePointer):
    """ A `StructurePointer64` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(64, 8, auto_align=True)


class ArrayPointer8(ArrayPointer):
    """ A `ArrayPointer8` field is a :class:`ArrayPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(8, 8, auto_align=True)


class ArrayPointer16(ArrayPointer):
    """ A `ArrayPointer16` field is a :class:`ArrayPointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(16, 8, auto_align=True)


class ArrayPointer24(ArrayPointer):
    """ A `ArrayPointer24` field is a :class:`ArrayPointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(24, 8, auto_align=True)


class ArrayPointer32(ArrayPointer):
    """ A `ArrayPointer32` field is a :class:`ArrayPointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(32, 8, auto_align=True)


class ArrayPointer48(ArrayPointer):
    """ A `ArrayPointer48` field is a :class:`ArrayPointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(48, 8, auto_align=True)


class ArrayPointer64(ArrayPointer):
    """ A `ArrayPointer64` field is a :class:`ArrayPointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(64, 8, auto_align=True)


class StreamPointer8(StreamPointer):
    """ A `StreamPointer8` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(8, 8, auto_align=True)


class StreamPointer16(StreamPointer):
    """ A `StreamPointer16` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(16, 8, auto_align=True)


class StreamPointer24(StreamPointer):
    """ A `StreamPointer24` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(24, 8, auto_align=True)


class StreamPointer32(StreamPointer):
    """ A `StreamPointer32` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(32, 8, auto_align=True)


class StreamPointer48(StreamPointer):
    """ A `StreamPointer48` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(48, 8, auto_align=True)


class StreamPointer64(StreamPointer):
    """ A `StreamPointer64` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(64, 8, auto_align=True)


class StringPointer8(StringPointer):
    """ A `StringPointer8` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(8, 8, auto_align=True)


class StringPointer16(StringPointer):
    """ A `StringPointer16` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(16, 8, auto_align=True)


class StringPointer24(StringPointer):
    """ A `StringPointer24` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(24, 8, auto_align=True)


class StringPointer32(StringPointer):
    """ A `StringPointer32` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(32, 8, auto_align=True)


class StringPointer48(StringPointer):
    """ A `StringPointer48` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(48, 8, auto_align=True)


class StringPointer64(StringPointer):
    """ A `StringPointer64` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(64, 8, auto_align=True)


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
        # Field bit size
        self._set_bit_size(8, 8, auto_align=True)


class RelativePointer16(RelativePointer):
    """ A `RelativePointer16` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(16, 8, auto_align=True)


class RelativePointer24(RelativePointer):
    """ A `RelativePointer24` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(24, 8, auto_align=True)


class RelativePointer32(RelativePointer):
    """ A `RelativePointer32` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(32, 8, auto_align=True)


class RelativePointer48(RelativePointer):
    """ A `RelativePointer48` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(48, 8, auto_align=True)


class RelativePointer64(RelativePointer):
    """ A `RelativePointer64` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(64, 8, auto_align=True)


class StructureRelativePointer8(StructureRelativePointer):
    """ A `StructureRelativePointer8` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(8, 8, auto_align=True)


class StructureRelativePointer16(StructureRelativePointer):
    """ A `StructureRelativePointer16` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(16, 8, auto_align=True)


class StructureRelativePointer24(StructureRelativePointer):
    """ A `StructureRelativePointer24` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(24, 8, auto_align=True)


class StructureRelativePointer32(StructureRelativePointer):
    """ A `StructureRelativePointer32` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(32, 8, auto_align=True)


class StructureRelativePointer48(StructureRelativePointer):
    """ A `StructureRelativePointer48` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(48, 8, auto_align=True)


class StructureRelativePointer64(StructureRelativePointer):
    """ A `StructureRelativePointer64` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(64, 8, auto_align=True)


class ArrayRelativePointer8(ArrayRelativePointer):
    """ A `ArrayRelativePointer8` field is a :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(8, 8, auto_align=True)


class ArrayRelativePointer16(ArrayRelativePointer):
    """ A `ArrayRelativePointer16` field is a :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(16, 8, auto_align=True)


class ArrayRelativePointer24(ArrayRelativePointer):
    """ A `ArrayRelativePointer24` field is a :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(24, 8, auto_align=True)


class ArrayRelativePointer32(ArrayRelativePointer):
    """ A `ArrayRelativePointer32` field is a :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(32, 8, auto_align=True)


class ArrayRelativePointer48(ArrayRelativePointer):
    """ A `ArrayRelativePointer48` field is a :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(48, 8, auto_align=True)


class ArrayRelativePointer64(ArrayRelativePointer):
    """ A `ArrayRelativePointer64` field is a :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template, address=None, byte_order=BYTEORDER):
        super().__init__(template=template, address=address, byte_order=byte_order)
        # Field bit size
        self._set_bit_size(64, 8, auto_align=True)


class StreamRelativePointer8(StreamRelativePointer):
    """ A `StreamRelativePointer8` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(8, 8, auto_align=True)


class StreamRelativePointer16(StreamRelativePointer):
    """ A `StreamRelativePointer16` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(16, 8, auto_align=True)


class StreamRelativePointer24(StreamRelativePointer):
    """ A `StreamRelativePointer24` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(24, 8, auto_align=True)


class StreamRelativePointer32(StreamRelativePointer):
    """ A `StreamRelativePointer32` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(32, 8, auto_align=True)


class StreamRelativePointer48(StreamRelativePointer):
    """ A `StreamRelativePointer48` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(48, 8, auto_align=True)


class StreamRelativePointer64(StreamRelativePointer):
    """ A `StreamRelativePointer64` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(64, 8, auto_align=True)


class StringRelativePointer8(StringRelativePointer):
    """ A `StringRelativePointer8` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(8, 8, auto_align=True)


class StringRelativePointer16(StringRelativePointer):
    """ A `StringRelativePointer16` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(16, 8, auto_align=True)


class StringRelativePointer24(StringRelativePointer):
    """ A `StringRelativePointer24` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(24, 8, auto_align=True)


class StringRelativePointer32(StringRelativePointer):
    """ A `StringRelativePointer32` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(32, 8, auto_align=True)


class StringRelativePointer48(StringRelativePointer):
    """ A `StringRelativePointer48` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(48, 8, auto_align=True)


class StringRelativePointer64(StringRelativePointer):
    """ A `StringRelativePointer64` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address)
        # Field bit size
        self._set_bit_size(64, 8, auto_align=True)
