# -*- coding: utf-8 -*-
"""
    KonFoo
    ~~~~~~

    KonFoo is a Python Package for creating byte stream mappers in a declarative
    way with as little code as necessary to help fighting the confusion with the
    foo of the all too well-known memory dumps or hexadecimal views of binary
    data.

    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details.
"""

# Enumerations
from .enums import Enumeration

# Categories
from .categories import Category

# Globals
from .globals import Byteorder, BYTEORDER

# Exceptions
from .exceptions import (
    KonFooError, FileError, RangeError, SizeError, LengthError,
    AlignmentError, OffsetError)

# Providers
from .providers import Provider, FileProvider

# Core classes
from .core import (
    is_any, is_field, is_container, is_array, is_structure,
    is_pointer, is_mixin,
    Patch, Index, zero,
    Container, Structure, Sequence, Array,
    Field,
    Stream, String,
    Float,
    Decimal, Bit, Byte, Char, Signed, Unsigned, Bitset, Bool, Enum, Scaled,
    Fraction, Bipolar, Unipolar, Datetime,
    Pointer, StructurePointer, SequencePointer, ArrayPointer, StreamPointer,
    StringPointer, AutoStringPointer,
    RelativePointer, StructureRelativePointer, SequenceRelativePointer,
    ArrayRelativePointer, StreamRelativePointer, StringRelativePointer)

# Field classes
from .fields import (
    Decimal8, Decimal16, Decimal24, Decimal32,
    Signed8, Signed16, Signed24, Signed32,
    Unsigned8, Unsigned16, Unsigned24, Unsigned32,
    Bool8, Bool16, Bool24, Bool32,
    Antivalent, Enum4, Enum8, Enum16, Enum24, Enum32,
    Bitset8, Bitset16, Bitset24, Bitset32,
    Scaled8, Scaled16, Scaled24, Scaled32,
    Bipolar2, Bipolar4, Unipolar2)

# Pointer classes
from .pointers import (
    Pointer8, Pointer16, Pointer32, Pointer64,
    StructurePointer8, StructurePointer16, StructurePointer32,
    ArrayPointer8, ArrayPointer16, ArrayPointer32,
    StreamPointer8, StreamPointer16, StreamPointer32,
    StringPointer8, StringPointer16, StringPointer32,
    FloatPointer,
    Signed8Pointer, Signed16Pointer, Signed32Pointer,
    Unsigned8Pointer, Unsigned16Pointer, Unsigned32Pointer)

# Relative pointer classes
from .pointers import (
    RelativePointer8, RelativePointer16, RelativePointer32, RelativePointer64,
    StructureRelativePointer8, StructureRelativePointer16,
    StructureRelativePointer32,
    ArrayRelativePointer8, ArrayRelativePointer16, ArrayRelativePointer32,
    StreamRelativePointer8, StreamRelativePointer16, StreamRelativePointer32,
    StringRelativePointer8, StringRelativePointer16, StringRelativePointer32)

# Utilities
from .utils import d3json, HexViewer

__all__ = [
    # Enumerations
    'Enumeration',

    # Categories
    'Category',

    # Globals
    'Byteorder', 'BYTEORDER',

    # Exceptions
    'KonFooError',
    'FileError', 'RangeError', 'SizeError', 'LengthError',
    'AlignmentError', 'OffsetError',

    # Provider
    'Provider', 'FileProvider',

    # Core classes
    'is_any', 'is_field',
    'is_container', 'is_array', 'is_structure',
    'is_pointer', 'is_mixin',

    'Patch', 'Index', 'zero',

    'Container', 'Structure', 'Sequence', 'Array',

    'Field', 'Stream', 'String', 'Float', 'Decimal', 'Bit', 'Byte', 'Char',
    'Signed', 'Unsigned', 'Bitset', 'Bool', 'Enum', 'Scaled', 'Fraction',
    'Bipolar', 'Unipolar', 'Datetime',

    'Pointer', 'StructurePointer', 'SequencePointer', 'ArrayPointer',
    'StreamPointer', 'StringPointer', 'AutoStringPointer',

    'RelativePointer', 'StructureRelativePointer', 'SequenceRelativePointer',
    'ArrayRelativePointer', 'StreamRelativePointer', 'StringRelativePointer',

    # Field classes
    'Decimal8', 'Decimal16', 'Decimal24', 'Decimal32',
    'Signed8', 'Signed16', 'Signed24', 'Signed32',
    'Unsigned8', 'Unsigned16', 'Unsigned24', 'Unsigned32',
    'Bool8', 'Bool16', 'Bool24', 'Bool32',
    'Antivalent', 'Enum4', 'Enum8', 'Enum16', 'Enum24', 'Enum32',
    'Bitset8', 'Bitset16', 'Bitset24', 'Bitset32',
    'Scaled8', 'Scaled16', 'Scaled24', 'Scaled32',
    'Bipolar2', 'Bipolar4', 'Unipolar2',

    # Pointer classes
    'Pointer8', 'Pointer16', 'Pointer32', 'Pointer64',
    'StructurePointer8', 'StructurePointer16', 'StructurePointer32',
    'ArrayPointer8', 'ArrayPointer16', 'ArrayPointer32',
    'StreamPointer8', 'StreamPointer16', 'StreamPointer32',
    'StringPointer8', 'StringPointer16', 'StringPointer32',
    'FloatPointer',
    'Signed8Pointer', 'Signed16Pointer', 'Signed32Pointer',
    'Unsigned8Pointer', 'Unsigned16Pointer', 'Unsigned32Pointer',

    # Relative pointer classes
    'RelativePointer8', 'RelativePointer16', 'RelativePointer32',
    'RelativePointer64',
    'StructureRelativePointer8', 'StructureRelativePointer16',
    'StructureRelativePointer32',
    'ArrayRelativePointer8', 'ArrayRelativePointer16',
    'ArrayRelativePointer32',
    'StreamRelativePointer8', 'StreamRelativePointer16',
    'StreamRelativePointer32',
    'StringRelativePointer8', 'StringRelativePointer16',
    'StringRelativePointer32',

    # Utilities
    'd3json', 'HexViewer',
]

__version__ = '0.1.a1'
