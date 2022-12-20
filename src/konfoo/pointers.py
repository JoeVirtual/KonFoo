# -*- coding: utf-8 -*-
"""
pointers.py
~~~~~~~~~~~
Pre-defined pointer field variants.

:copyright: (c) 2015-2022 by Jochen Gerhaeusser.
:license: BSD, see LICENSE for details
"""
from __future__ import annotations

from typing import (Callable, Literal)

from .core import (
    Structure, Sequence, Field,
    Pointer, StructurePointer, ArrayPointer, StreamPointer,
    StringPointer,
    RelativePointer, StructureRelativePointer, ArrayRelativePointer,
    StreamRelativePointer, StringRelativePointer,
    Float)
from .fields import (
    Signed8, Signed16, Signed32,
    Unsigned8, Unsigned16, Unsigned32)
from .globals import Byteorder, BYTEORDER


class Pointer8(Pointer):
    """ The :class:`Pointer8` field is a :class:`Pointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER) -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class Pointer16(Pointer):
    """ The :class:`Pointer16` field is a :class:`Pointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class Pointer24(Pointer):
    """ The :class:`Pointer24` field is a :class:`Pointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class Pointer32(Pointer):
    """ The :class:`Pointer32` field is a :class:`Pointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class Pointer48(Pointer):
    """ The :class:`Pointer48` field is a :class:`Pointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class Pointer64(Pointer):
    """ The :class:`Pointer64` field is a :class:`Pointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class StructurePointer8(StructurePointer):
    """ The :class:`StructurePointer8` field is a
    :class:`StructurePointer` field with a :class:`Field` *size* of one byte.
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER) -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class StructurePointer16(StructurePointer):
    """ The :class:`StructurePointer16` field is a
    :class:`StructurePointer` field with a :class:`Field` *size* of two bytes.
    """

    def __init__(self, template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class StructurePointer24(StructurePointer):
    """ The :class:`StructurePointer24` field is a
    :class:`StructurePointer` field with a :class:`Field` *size* of three bytes.
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class StructurePointer32(StructurePointer):
    """ The :class:`StructurePointer32` field is a
    :class:`StructurePointer` field with a :class:`Field` *size* of four bytes.
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class StructurePointer48(StructurePointer):
    """ The :class:`StructurePointer48` field is a
    :class:`StructurePointer` field  with a :class:`Field` *size* of six bytes.
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class StructurePointer64(StructurePointer):
    """ The :class:`StructurePointer64` field is a
    :class:`StructurePointer` field with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class ArrayPointer8(ArrayPointer):
    """ The :class:`ArrayPointer8` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER) -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class ArrayPointer16(ArrayPointer):
    """ The :class:`ArrayPointer16` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class ArrayPointer24(ArrayPointer):
    """ The :class:`ArrayPointer24` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class ArrayPointer32(ArrayPointer):
    """ The :class:`ArrayPointer32` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class ArrayPointer48(ArrayPointer):
    """ The :class:`ArrayPointer48` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class ArrayPointer64(ArrayPointer):
    """ The :class:`ArrayPointer64` field is an :class:`ArrayPointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class StreamPointer8(StreamPointer):
    """ The :class:`StreamPointer8` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None) -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=8)


class StreamPointer16(StreamPointer):
    """ The :class:`StreamPointer16` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=16,
                         field_order=field_order)


class StreamPointer24(StreamPointer):
    """ The :class:`StreamPointer24` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=24,
                         field_order=field_order)


class StreamPointer32(StreamPointer):
    """ The :class:`StreamPointer32` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=32,
                         field_order=field_order)


class StreamPointer48(StreamPointer):
    """ The :class:`StreamPointer48` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=48,
                         field_order=field_order)


class StreamPointer64(StreamPointer):
    """ The :class:`StreamPointer64` field is a :class:`StreamPointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=64,
                         field_order=field_order)


class StringPointer8(StringPointer):
    """ The :class:`StringPointer8` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None, ) -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=8)


class StringPointer16(StringPointer):
    """ The :class:`StringPointer16` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=16,
                         field_order=field_order)


class StringPointer24(StringPointer):
    """ The :class:`StringPointer24` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=24,
                         field_order=field_order)


class StringPointer32(StringPointer):
    """ The :class:`StringPointer32` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=32,
                         field_order=field_order)


class StringPointer48(StringPointer):
    """ The :class:`StringPointer48` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=48,
                         field_order=field_order)


class StringPointer64(StringPointer):
    """ The :class:`StringPointer64` field is a :class:`StringPointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=64,
                         field_order=field_order)


class FloatPointer(Pointer):
    """ The :class:`FloatPointer` field is a :class:`Pointer` field
    which refers to a :class:`Float` field.
    """

    def __init__(self,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=Float(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Signed8Pointer(Pointer):
    """ The :class:`FloatPointer` field is a :class:`Pointer` field
    which refers to a :class:`Signed8` field.
    """

    def __init__(self,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=Signed8(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Signed16Pointer(Pointer):
    """ The :class:`Signed16Pointer` field is a :class:`Pointer` field
    which refers to a :class:`Signed16` field.
    """

    def __init__(self,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=Signed16(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Signed32Pointer(Pointer):
    """ The :class:`Signed32Pointer` field is a :class:`Pointer` field
    which refers to a :class:`Signed32` field.
    """

    def __init__(self,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=Signed32(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Unsigned8Pointer(Pointer):
    """ The :class:`Unsigned8Pointer` field is a :class:`Pointer` field
    which refers to an :class:`Unsigned8` field.
    """

    def __init__(self,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=Unsigned8(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Unsigned16Pointer(Pointer):
    """ The :class:`Unsigned16Pointer` field is a :class:`Pointer` field
    which refers to an :class:`Unsigned16` field.
    """

    def __init__(self,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=Unsigned16(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class Unsigned32Pointer(Pointer):
    """ The :class:`Unsigned32Pointer` field is a :class:`Pointer` field
    which refers to an :class:`Unsigned32` field.
    """

    def __init__(self,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=Unsigned32(),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)


class RelativePointer8(RelativePointer):
    """ The :class:`RelativePointer8` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER) -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class RelativePointer16(RelativePointer):
    """ The :class:`RelativePointer16` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class RelativePointer24(RelativePointer):
    """ The :class:`RelativePointer24` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class RelativePointer32(RelativePointer):
    """ The :class:`RelativePointer32` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class RelativePointer48(RelativePointer):
    """ The :class:`RelativePointer48` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class RelativePointer64(RelativePointer):
    """ The :class:`RelativePointer64` field is a :class:`RelativePointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class StructureRelativePointer8(StructureRelativePointer):
    """ The :class:`StructureRelativePointer8` field is a
    :class:`StructureRelativePointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER) -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class StructureRelativePointer16(StructureRelativePointer):
    """ The :class:`StructureRelativePointer16` field is a
    :class:`StructureRelativePointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class StructureRelativePointer24(StructureRelativePointer):
    """ The :class:`StructureRelativePointer24` field is a
    :class:`StructureRelativePointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class StructureRelativePointer32(StructureRelativePointer):
    """ The :class:`StructureRelativePointer32` field is a
    :class:`StructureRelativePointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class StructureRelativePointer48(StructureRelativePointer):
    """ The :class:`StructureRelativePointer48` field is a
    :class:`StructureRelativePointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class StructureRelativePointer64(StructureRelativePointer):
    """ The :class:`StructureRelativePointer64` field is a
    :class:`StructureRelativePointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class ArrayRelativePointer8(ArrayRelativePointer):
    """ The :class:`ArrayRelativePointer8` field is an
    :class:`ArrayRelativePointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER) -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=8)


class ArrayRelativePointer16(ArrayRelativePointer):
    """ The :class:`ArrayRelativePointer16` field is an
    :class:`ArrayRelativePointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=16,
                         field_order=field_order)


class ArrayRelativePointer24(ArrayRelativePointer):
    """ The :class:`ArrayRelativePointer24` field is an
    :class:`ArrayRelativePointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=24,
                         field_order=field_order)


class ArrayRelativePointer32(ArrayRelativePointer):
    """ The :class:`ArrayRelativePointer32` field is an
    :class:`ArrayRelativePointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=32,
                         field_order=field_order)


class ArrayRelativePointer48(ArrayRelativePointer):
    """ The :class:`ArrayRelativePointer48` field is an
    :class:`ArrayRelativePointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=48,
                         field_order=field_order)


class ArrayRelativePointer64(ArrayRelativePointer):
    """ The :class:`ArrayRelativePointer64` field is an
    :class:`ArrayRelativePointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         capacity=capacity,
                         address=address,
                         data_order=data_order,
                         bit_size=64,
                         field_order=field_order)


class StreamRelativePointer8(StreamRelativePointer):
    """ The :class:`StreamRelativePointer8` field is a
    :class:`StreamRelativePointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None):
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=8)


class StreamRelativePointer16(StreamRelativePointer):
    """ The :class:`StreamRelativePointer16` field is a
    :class:`StreamRelativePointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=16,
                         field_order=field_order)


class StreamRelativePointer24(StreamRelativePointer):
    """ The :class:`StreamRelativePointer24` field is a
    :class:`StreamRelativePointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=24,
                         field_order=field_order)


class StreamRelativePointer32(StreamRelativePointer):
    """ The :class:`StreamRelativePointer32` field is a
    :class:`StreamRelativePointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=32,
                         field_order=field_order)


class StreamRelativePointer48(StreamRelativePointer):
    """ The :class:`StreamRelativePointer48` field is a
    :class:`StreamRelativePointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=48,
                         field_order=field_order)


class StreamRelativePointer64(StreamRelativePointer):
    """ The :class:`StreamRelativePointer64` field is a
    :class:`StreamRelativePointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=64,
                         field_order=field_order)


class StringRelativePointer8(StringRelativePointer):
    """ The :class:`StringRelativePointer8` field is a
    :class:`StringRelativePointer` field
    with a :class:`Field` *size* of one byte.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None) -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=8)


class StringRelativePointer16(StringRelativePointer):
    """ The :class:`StringRelativePointer16` field is a
    :class:`StringRelativePointer` field
    with a :class:`Field` *size* of two bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=16,
                         field_order=field_order)


class StringRelativePointer24(StringRelativePointer):
    """ The :class:`StringRelativePointer24` field is a
    :class:`StringRelativePointer` field
    with a :class:`Field` *size* of three bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=24,
                         field_order=field_order)


class StringRelativePointer32(StringRelativePointer):
    """ The :class:`StringRelativePointer32` field is a
    :class:`StringRelativePointer` field
    with a :class:`Field` *size* of four bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=32,
                         field_order=field_order)


class StringRelativePointer48(StringRelativePointer):
    """ The :class:`StringRelativePointer48` field is a
    :class:`StringRelativePointer` field
    with a :class:`Field` *size* of six bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=48,
                         field_order=field_order)


class StringRelativePointer64(StringRelativePointer):
    """ The :class:`StringRelativePointer64` field is a
    :class:`StringRelativePointer` field
    with a :class:`Field` *size* of eight bytes.
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=capacity,
                         address=address,
                         bit_size=64,
                         field_order=field_order)
