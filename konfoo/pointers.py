# -*- coding: utf-8 -*-
"""
    pointers.py
    ~~~~~~~~~~~
    <Add description of the module here>.

    :copyright: (c) 2015-2018 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details
"""

from .core import (
    Pointer, StructurePointer, ArrayPointer, StreamPointer,
    StringPointer,
    RelativePointer, StructureRelativePointer, ArrayRelativePointer,
    StreamRelativePointer, StringRelativePointer,
    Float)
from .fields import (
    Signed8, Signed16, Signed32,
    Unsigned8, Unsigned16, Unsigned32)
from .globals import BYTEORDER


class Pointer8(Pointer):
    """ A `Pointer8` field is a :class:`Pointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class Pointer16(Pointer):
    """ A `Pointer16` field is a :class:`Pointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class Pointer24(Pointer):
    """ A `Pointer24` field is a :class:`Pointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class Pointer32(Pointer):
    """ A `Pointer32` field is a :class:`Pointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class Pointer48(Pointer):
    """ A `Pointer48` field is a :class:`Pointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class Pointer64(Pointer):
    """ A `Pointer64` field is a :class:`Pointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class StructurePointer8(StructurePointer):
    """ A `StructurePointer8` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class StructurePointer16(StructurePointer):
    """ A `StructurePointer16` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class StructurePointer24(StructurePointer):
    """ A `StructurePointer24` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class StructurePointer32(StructurePointer):
    """ A `StructurePointer32` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class StructurePointer48(StructurePointer):
    """ A `StructurePointer48` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class StructurePointer64(StructurePointer):
    """ A `StructurePointer64` field is a :class:`StructurePointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class ArrayPointer8(ArrayPointer):
    """ An `ArrayPointer8` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class ArrayPointer16(ArrayPointer):
    """ An `ArrayPointer16` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class ArrayPointer24(ArrayPointer):
    """ An `ArrayPointer24` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class ArrayPointer32(ArrayPointer):
    """ An `ArrayPointer32` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class ArrayPointer48(ArrayPointer):
    """ An `ArrayPointer48` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class ArrayPointer64(ArrayPointer):
    """ An `ArrayPointer64` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class StreamPointer8(StreamPointer):
    """ A `StreamPointer8` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size=size,
                         address=address,
                         bit_size=8)


class StreamPointer16(StreamPointer):
    """ A `StreamPointer16` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=16,
                         field_order=field_order)


class StreamPointer24(StreamPointer):
    """ A `StreamPointer24` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=24,
                         field_order=field_order)


class StreamPointer32(StreamPointer):
    """ A `StreamPointer32` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=32,
                         field_order=field_order)


class StreamPointer48(StreamPointer):
    """ A `StreamPointer48` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=48,
                         field_order=field_order)


class StreamPointer64(StreamPointer):
    """ A `StreamPointer64` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=64,
                         field_order=field_order)


class StringPointer8(StringPointer):
    """ A `StringPointer8` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size, address, bit_size=8)


class StringPointer16(StringPointer):
    """ A `StringPointer16` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=16,
                         field_order=field_order)


class StringPointer24(StringPointer):
    """ A `StringPointer24` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=24,
                         field_order=field_order)


class StringPointer32(StringPointer):
    """ A `StringPointer32` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=32,
                         field_order=field_order)


class StringPointer48(StringPointer):
    """ A `StringPointer48` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=48,
                         field_order=field_order)


class StringPointer64(StringPointer):
    """ A `StringPointer64` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=64,
                         field_order=field_order)


class FloatPointer(Pointer):
    """ A `FloatPointer` field is a :class:`Pointer` field
    which refers to a :class:`Float` field.
    """

    def __init__(self, address=None, data_order=BYTEORDER,
                 bit_size=32, align_to=None, field_order='auto'):
        super().__init__(template=Float(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Signed8Pointer(Pointer):
    """ A `FloatPointer` field is a :class:`Pointer` field
    which refers to a :class:`Signed8` field.
    """

    def __init__(self, address=None, data_order=BYTEORDER,
                 bit_size=32, align_to=None, field_order='auto'):
        super().__init__(template=Signed8(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Signed16Pointer(Pointer):
    """ A `Signed16Pointer` field is a :class:`Pointer` field
    which refers to a :class:`Signed16` field.
    """

    def __init__(self, address=None, data_order=BYTEORDER,
                 bit_size=32, align_to=None, field_order='auto'):
        super().__init__(template=Signed16(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Signed32Pointer(Pointer):
    """ A `Signed32Pointer` field is a :class:`Pointer` field
    which refers to a :class:`Signed32` field.
    """

    def __init__(self, address=None, data_order=BYTEORDER,
                 bit_size=32, align_to=None, field_order='auto'):
        super().__init__(template=Signed32(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Unsigned8Pointer(Pointer):
    """ An `Unsigned8Pointer` field is a :class:`Pointer` field
    which refers to an :class:`Unsigned8` field.
    """

    def __init__(self, address=None, data_order=BYTEORDER,
                 bit_size=32, align_to=None, field_order='auto'):
        super().__init__(template=Unsigned8(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Unsigned16Pointer(Pointer):
    """ An `Unsigned16Pointer` field is a :class:`Pointer` field
    which refers to an :class:`Unsigned16` field.
    """

    def __init__(self, address=None, data_order=BYTEORDER,
                 bit_size=32, align_to=None, field_order='auto'):
        super().__init__(template=Unsigned16(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Unsigned32Pointer(Pointer):
    """ An `Unsigned32Pointer` field is a :class:`Pointer` field
    which refers to an :class:`Unsigned32` field.
    """

    def __init__(self, address=None, data_order=BYTEORDER,
                 bit_size=32, align_to=None, field_order='auto'):
        super().__init__(template=Unsigned32(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class RelativePointer8(RelativePointer):
    """ A `RelativePointer8` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class RelativePointer16(RelativePointer):
    """ A `RelativePointer16` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class RelativePointer24(RelativePointer):
    """ A `RelativePointer24` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class RelativePointer32(RelativePointer):
    """ A `RelativePointer32` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class RelativePointer48(RelativePointer):
    """ A `RelativePointer48` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class RelativePointer64(RelativePointer):
    """ A `RelativePointer64` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class StructureRelativePointer8(StructureRelativePointer):
    """ A `StructureRelativePointer8` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class StructureRelativePointer16(StructureRelativePointer):
    """ A `StructureRelativePointer16` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class StructureRelativePointer24(StructureRelativePointer):
    """ A `StructureRelativePointer24` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class StructureRelativePointer32(StructureRelativePointer):
    """ A `StructureRelativePointer32` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class StructureRelativePointer48(StructureRelativePointer):
    """ A `StructureRelativePointer48` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class StructureRelativePointer64(StructureRelativePointer):
    """ A `StructureRelativePointer64` field is a :class:`StructureRelativePointer`
    field with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template=None, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class ArrayRelativePointer8(ArrayRelativePointer):
    """ An `ArrayRelativePointer8` field is an :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class ArrayRelativePointer16(ArrayRelativePointer):
    """ An `ArrayRelativePointer16` field is an :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class ArrayRelativePointer24(ArrayRelativePointer):
    """ An `ArrayRelativePointer24` field is an :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class ArrayRelativePointer32(ArrayRelativePointer):
    """ An `ArrayRelativePointer32` field is an :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class ArrayRelativePointer48(ArrayRelativePointer):
    """ An `ArrayRelativePointer48` field is an :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class ArrayRelativePointer64(ArrayRelativePointer):
    """ An `ArrayRelativePointer64` field is an :class:`ArrayRelativePointer`
    field with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, template, address=None, data_order=BYTEORDER,
                 field_order='auto'):
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class StreamRelativePointer8(StreamRelativePointer):
    """ A `StreamRelativePointer8` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size=size,
                         address=address,
                         bit_size=8)


class StreamRelativePointer16(StreamRelativePointer):
    """ A `StreamRelativePointer16` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=16,
                         field_order=field_order)


class StreamRelativePointer24(StreamRelativePointer):
    """ A `StreamRelativePointer24` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=24,
                         field_order=field_order)


class StreamRelativePointer32(StreamRelativePointer):
    """ A `StreamRelativePointer32` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=32,
                         field_order=field_order)


class StreamRelativePointer48(StreamRelativePointer):
    """ A `StreamRelativePointer48` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=48,
                         field_order=field_order)


class StreamRelativePointer64(StreamRelativePointer):
    """ A `StreamRelativePointer64` field is a :class:`StreamRelativePointer`
    field with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=64,
                         field_order=field_order)


class StringRelativePointer8(StringRelativePointer):
    """ A `StringRelativePointer8` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of one byte.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size=size,
                         address=address,
                         bit_size=8)


class StringRelativePointer16(StringRelativePointer):
    """ A `StringRelativePointer16` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=16,
                         field_order=field_order)


class StringRelativePointer24(StringRelativePointer):
    """ A `StringRelativePointer24` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of three bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=24,
                         field_order=field_order)


class StringRelativePointer32(StringRelativePointer):
    """ A `StringRelativePointer32` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of four bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=32,
                         field_order=field_order)


class StringRelativePointer48(StringRelativePointer):
    """ A `StringRelativePointer48` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of six bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=48,
                         field_order=field_order)


class StringRelativePointer64(StringRelativePointer):
    """ A `StringRelativePointer64` field is a :class:`StringRelativePointer`
    field with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self, size=0, address=None, field_order='auto'):
        super().__init__(size=size,
                         address=address,
                         bit_size=64,
                         field_order=field_order)
