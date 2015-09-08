# -*- coding: utf-8 -*-
"""
    KonFoo
    ~~~~~~

    KonFoo is a Python Package for creating byte stream mappers in a declarative
    way with as little code as necessary to help fighting the confusion with the
    foo of the all too well-known memory dumps or binary data.

    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details.
"""

# Providers
from .providers import Provider

# Enumerations
from .enums import Enumeration, ItemClass

# Categories
from .categories import Category, Byteorder, Option

# Decorators
from .decorators import byte_order_option, field_types_option, \
    nested_option, verbose_option

# Exceptions
from .exceptions import KonFooException, FileError, OutOfRange, \
    InvalidIndex, InvalidSize, InvalidLength, BadAligned, BadOffset

# Core classes
from .core import Index, Container, Structure, Sequence, Array, \
    Field, Stream, String, Float, Decimal, Bit, Byte, Char, Signed, Unsigned, \
    Bitset, Bool, Enum, Scaled, Fraction, Bipolar, Unipolar, Datetime, \
    Pointer, StructurePointer, SequencePointer, ArrayPointer, StreamPointer, \
    StringPointer, RelativePointer, StreamRelativePointer, StringRelativePointer

# Field classes
from .fields import Decimal8, Decimal16, Decimal24, Decimal32, \
    Signed8, Signed16, Signed24, Signed32, \
    Unsigned8, Unsigned16, Unsigned24, Unsigned32, \
    Bool8, Bool16, Bool24, Bool32, \
    Antivalent, Enum4, Enum8, Enum16, Enum24, Enum32, \
    Bitset8, Bitset16, Bitset24, Bitset32, \
    Scaled8, Scaled16, Scaled24, Scaled32, \
    Bipolar2, Bipolar4, Unipolar2, \
    Pointer8, Pointer16, Pointer32, Pointer64, \
    StreamPointer8, StreamPointer16, StreamPointer32, \
    RelativePointer8, RelativePointer16, RelativePointer32, RelativePointer64, \
    StreamRelativePointer8, StreamRelativePointer16, StreamRelativePointer32

# Exceptions
from .exceptions import KonFooException, FileError, OutOfRange, \
    InvalidIndex, InvalidSize, InvalidLength, BadAligned, BadOffset

# Utilities
from .utils import d3json

__all__ = [
    # Provider
    'Provider',

    # Enumerations
    'Enumeration', 'ItemClass',

    # Decorators
    'byte_order_option', 'field_types_option', 'nested_option',
    'verbose_option',

    # Exceptions
    'KonFooException',
    'FileError', 'OutOfRange', 'InvalidIndex', 'InvalidSize',
    'InvalidLength', 'BadAligned', 'BadOffset',

    # Categories
    'Category', 'Byteorder', 'Option',

    # Core classes
    'Index', 'Container', 'Structure', 'Sequence', 'Array',

    'Field', 'Stream', 'String', 'Float', 'Decimal', 'Bit', 'Byte', 'Char',
    'Signed', 'Unsigned', 'Bitset', 'Bool', 'Enum', 'Scaled', 'Fraction',
    'Bipolar', 'Unipolar', 'Datetime',

    'Pointer', 'StructurePointer', 'SequencePointer', 'ArrayPointer',
    'StreamPointer', 'StringPointer',

    'RelativePointer', 'StreamRelativePointer', 'StringRelativePointer',

    # Field classes
    'Decimal8', 'Decimal16', 'Decimal24', 'Decimal32',
    'Signed8', 'Signed16', 'Signed24', 'Signed32',
    'Unsigned8', 'Unsigned16', 'Unsigned24', 'Unsigned32',
    'Bool8', 'Bool16', 'Bool24', 'Bool32',
    'Antivalent', 'Enum4', 'Enum8', 'Enum16', 'Enum24', 'Enum32',
    'Bitset8', 'Bitset16', 'Bitset24', 'Bitset32',
    'Scaled8', 'Scaled16', 'Scaled24', 'Scaled32',
    'Bipolar2', 'Bipolar4', 'Unipolar2',

    'Pointer8', 'Pointer16', 'Pointer32', 'Pointer64',
    'StreamPointer8', 'StreamPointer16', 'StreamPointer32',

    'RelativePointer8', 'RelativePointer16', 'RelativePointer32',
    'RelativePointer64',
    'StreamRelativePointer8', 'StreamRelativePointer16',
    'StreamRelativePointer32',

    # Utilities
    'd3json',
]

__version__ = '0.0-dev'
