# -*- coding: utf-8 -*-
"""
KonFoo
~~~~~~
Public package API.

:copyright: (c) 2015-2022 by Jochen Gerhaeusser.
:license: BSD, see LICENSE for details.
"""

# Categories
from .categories import Category
# Core classes
from .core import (
    is_any, is_field, is_container, is_array, is_structure,
    is_pointer, is_mixin,
    Patch, Index, Alignment,
    Container, Structure, Sequence, Array,
    Field,
    Stream, String,
    Float, Double,
    Decimal, Bit, Byte, Char, Signed, Unsigned, Bitset, Bool, Enum, Scaled,
    Fraction, Bipolar, Unipolar, Datetime, IPv4Address,
    Pointer, StructurePointer, SequencePointer, ArrayPointer, StreamPointer,
    StringPointer, AutoStringPointer,
    RelativePointer, StructureRelativePointer, SequenceRelativePointer,
    ArrayRelativePointer, StreamRelativePointer, StringRelativePointer
)
# Enumerations
from .enums import Enumeration
# Exceptions
from .exceptions import (
    ByteOrderTypeError, ByteOrderValueError,
    EnumTypeError, FactoryTypeError, MemberTypeError,
    ProviderTypeError, ContainerLengthError,
    FieldAddressError, FieldAlignmentError, FieldByteOrderError,
    FieldIndexError, FieldSizeError, FieldTypeError, FieldValueError,
    FieldValueEncodingError,
    FieldGroupByteOrderError, FieldGroupOffsetError, FieldGroupSizeError
)
# Field classes
from .fields import (
    Decimal8, Decimal16, Decimal24, Decimal32, Decimal64,
    Signed8, Signed16, Signed24, Signed32, Signed64,
    Unsigned8, Unsigned16, Unsigned24, Unsigned32, Unsigned64,
    Bool8, Bool16, Bool24, Bool32, Bool64,
    Antivalent, Enum4, Enum8, Enum16, Enum24, Enum32, Enum64,
    Bitset8, Bitset16, Bitset24, Bitset32, Bitset64,
    Scaled8, Scaled16, Scaled24, Scaled32, Scaled64,
    Bipolar2, Bipolar4, Unipolar2
)
# Globals
from .globals import Byteorder, BYTEORDER
# Pointer classes
from .pointers import (
    Pointer8, Pointer16, Pointer24,
    Pointer32, Pointer48, Pointer64,
    StructurePointer8, StructurePointer16, StructurePointer24,
    StructurePointer32, StructurePointer48, StructurePointer64,

    ArrayPointer8, ArrayPointer16, ArrayPointer24,
    ArrayPointer32, ArrayPointer48, ArrayPointer64,
    StreamPointer8, StreamPointer16, StreamPointer24,

    StreamPointer32, StreamPointer48, StreamPointer64,
    StringPointer8, StringPointer16, StringPointer24,

    StringPointer32, StringPointer48, StringPointer64,

    FloatPointer,

    Signed8Pointer, Signed16Pointer, Signed32Pointer,

    Unsigned8Pointer, Unsigned16Pointer, Unsigned32Pointer
)
# Relative pointer classes
from .pointers import (
    RelativePointer8, RelativePointer16, RelativePointer24,
    RelativePointer32, RelativePointer48, RelativePointer64,

    StructureRelativePointer8, StructureRelativePointer16,
    StructureRelativePointer24, StructureRelativePointer32,
    StructureRelativePointer48, StructureRelativePointer64,

    ArrayRelativePointer8, ArrayRelativePointer16, ArrayRelativePointer24,
    ArrayRelativePointer32, ArrayRelativePointer48, ArrayRelativePointer64,

    StreamRelativePointer8, StreamRelativePointer16, StreamRelativePointer24,
    StreamRelativePointer32, StreamRelativePointer48, StreamRelativePointer64,

    StringRelativePointer8, StringRelativePointer16, StringRelativePointer24,
    StringRelativePointer32, StringRelativePointer48, StringRelativePointer64,
)
# Providers
from .providers import Provider, FileProvider
# Utilities
from .utils import d3flare_json, HexViewer

__all__ = [
    # Enumerations
    'Enumeration',

    # Categories
    'Category',

    # Globals
    'Byteorder', 'BYTEORDER',

    # Exceptions
    'ByteOrderTypeError',
    'ByteOrderValueError',
    'EnumTypeError',

    'FactoryTypeError',
    'MemberTypeError',
    'ProviderTypeError',

    'ContainerLengthError',

    'FieldAddressError',
    'FieldAlignmentError',
    'FieldByteOrderError',
    'FieldIndexError',
    'FieldSizeError',
    'FieldValueError',
    'FieldTypeError',
    'FieldValueEncodingError',

    'FieldGroupByteOrderError',
    'FieldGroupOffsetError',
    'FieldGroupSizeError',

    # Provider
    'Provider',
    'FileProvider',

    # Core classes
    'is_any',
    'is_field',
    'is_container',
    'is_array',
    'is_structure',
    'is_pointer',
    'is_mixin',

    'Patch',
    'Index',
    'Alignment',

    'Container',

    'Structure',

    'Sequence',
    'Array',

    'Field',

    'Stream',
    'String',

    'Float', 'Double',

    'Decimal',
    'Bit',
    'Byte',
    'Char',
    'Signed',
    'Unsigned',
    'Bitset',
    'Bool',
    'Enum',
    'Scaled',
    'Fraction',
    'Bipolar',
    'Unipolar',
    'Datetime',
    'IPv4Address',

    'Pointer',
    'StructurePointer',
    'SequencePointer', 'ArrayPointer',
    'StreamPointer', 'StringPointer', 'AutoStringPointer',

    'RelativePointer',
    'StructureRelativePointer',
    'SequenceRelativePointer', 'ArrayRelativePointer',
    'StreamRelativePointer', 'StringRelativePointer',

    # Field classes
    'Decimal8',
    'Decimal16',
    'Decimal24',
    'Decimal32',
    'Decimal64',

    'Signed8',
    'Signed16',
    'Signed24',
    'Signed32',
    'Signed64',

    'Unsigned8',
    'Unsigned16',
    'Unsigned24',
    'Unsigned32',
    'Unsigned64',

    'Bool8',
    'Bool16',
    'Bool24',
    'Bool32',
    'Bool64',

    'Antivalent',

    'Enum4',
    'Enum8',
    'Enum16',
    'Enum24',
    'Enum32',
    'Enum64',

    'Bitset8',
    'Bitset16',
    'Bitset24',
    'Bitset32',
    'Bitset64',

    'Scaled8',
    'Scaled16',
    'Scaled24',
    'Scaled32',
    'Scaled64',

    'Bipolar2',
    'Bipolar4',

    'Unipolar2',

    # Pointer classes
    'Pointer8',
    'Pointer16',
    'Pointer24',
    'Pointer32',
    'Pointer48',
    'Pointer64',

    'StructurePointer8',
    'StructurePointer16',
    'StructurePointer24',
    'StructurePointer32',
    'StructurePointer48',
    'StructurePointer64',

    'ArrayPointer8',
    'ArrayPointer16',
    'ArrayPointer24',
    'ArrayPointer32',
    'ArrayPointer48',
    'ArrayPointer64',

    'StreamPointer8',
    'StreamPointer16',
    'StreamPointer24',
    'StreamPointer32',
    'StreamPointer48',
    'StreamPointer64',

    'StringPointer8',
    'StringPointer16',
    'StringPointer24',
    'StringPointer32',
    'StringPointer48',
    'StringPointer64',

    'FloatPointer',
    'Signed8Pointer',
    'Signed16Pointer',
    'Signed32Pointer',
    'Unsigned8Pointer',
    'Unsigned16Pointer',
    'Unsigned32Pointer',

    # Relative pointer classes
    'RelativePointer8',
    'RelativePointer16',
    'RelativePointer24',
    'RelativePointer32',
    'RelativePointer48',
    'RelativePointer64',

    'StructureRelativePointer8',
    'StructureRelativePointer16',
    'StructureRelativePointer24',
    'StructureRelativePointer32',
    'StructureRelativePointer48',
    'StructureRelativePointer64',

    'ArrayRelativePointer8',
    'ArrayRelativePointer16',
    'ArrayRelativePointer24',
    'ArrayRelativePointer32',
    'ArrayRelativePointer48',
    'ArrayRelativePointer64',

    'StreamRelativePointer8',
    'StreamRelativePointer16',
    'StreamRelativePointer24',
    'StreamRelativePointer32',
    'StreamRelativePointer48',
    'StreamRelativePointer64',

    'StringRelativePointer8',
    'StringRelativePointer16',
    'StringRelativePointer24',
    'StringRelativePointer32',
    'StringRelativePointer48',
    'StringRelativePointer64',

    # Utilities
    'd3flare_json', 'HexViewer',
]

__version__ = '2.1.0'
