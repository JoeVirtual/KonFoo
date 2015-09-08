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

# Core field_types
from .core import Index, Container, Structure, Sequence, Array, \
    Pointer, StructurePointer, SequencePointer, ArrayPointer, StreamPointer, StringPointer, \
    RelativePointer, StreamRelativePointer, StringRelativePointer, \
    Field, Stream, String, Float, Decimal, Bit, Byte, Char, Signed, Unsigned, Bitset, \
    Bool, Enum, Scaled, Fraction, Bipolar, Unipolar, Datetime

# Enumerations
from .enums import Enumeration, ItemClass

# Categories
from .categories import Category, Byteorder, Option

# Decorators
from .decorators import option, byte_order_option, field_types_option, nested_option, verbose_option

# Exceptions
from .exceptions import KonFooException, FileError, OutOfRange, \
    InvalidIndex, InvalidSize, InvalidLength, BadAligned, BadOffset

# Utilities
from .utils import d3json

__all__ = [
    # Provider
    'Provider',

    # Container
    'Container',
    'Structure',
    'Sequence', 'Array',

    # Fields
    'Field',
    # Stream Fields
    'Stream', 'String',
    # Floating Point Fields
    'Float',
    # Fixed Point Fields
    'Decimal',
    'Bit', 'Byte',
    'Char',
    'Signed', 'Unsigned',
    'Bitset',
    'Bool', 'Enum',
    'Scaled',
    'Fraction', 'Bipolar', 'Unipolar',
    'Datetime',

    # Absolute Pointer
    'Pointer',
    'StructurePointer', 'SequencePointer', 'ArrayPointer',
    'StreamPointer', 'StringPointer',
    # Relative Pointer
    'RelativePointer',
    'StreamRelativePointer', 'StringRelativePointer',

    # Enumerations
    'Enumeration', 'ItemClass',

    # Categories
    'Category', 'Byteorder', 'Option',

    # Decorators
    'option',
    'byte_order_option',
    'field_types_option',
    'nested_option',
    'verbose_option',

    # Exceptions
    'KonFooException',
    'FileError',
    'OutOfRange',
    'InvalidIndex', 'InvalidSize', 'InvalidLength',
    'BadAligned', 'BadOffset',

    # Utilities
    'd3json',
]

__version__ = '0.0-dev'
