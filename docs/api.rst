API
***

.. module:: konfoo

.. testsetup:: *

    from pprint import pprint
    from binascii import hexlify, unhexlify
    from konfoo.globals import ItemClass
    from konfoo import *

This part of the documentation lists the full API reference of all public
classes and functions.


Provider
========

.. autoclass:: Provider
    :members:

FileProvider
------------

.. autoclass:: FileProvider
    :members:


Container
=========

.. autoclass:: Container
    :members:

Structure
---------

.. autoclass:: Structure
    :members:

Sequence
--------

.. autoclass:: Sequence
    :members:

Array
~~~~~

.. autoclass:: Array
    :members:

Fields
======

.. autoclass:: Field
    :members:

Stream
------

.. autoclass:: Stream
    :members:

String
~~~~~~

.. autoclass:: String
    :members:

Float
-----

.. autoclass:: Float
    :members:

Double
------

.. autoclass:: Double
    :members:

Decimal
-------

.. autoclass:: Decimal
    :members:

.. autoclass:: Decimal8
    :members:

.. autoclass:: Decimal16
    :members:

.. autoclass:: Decimal24
    :members:

.. autoclass:: Decimal32
    :members:

.. autoclass:: Decimal64
    :members:


Bit
~~~

.. autoclass:: Bit
    :members:

Byte
~~~~

.. autoclass:: Byte
    :members:

Char
~~~~

.. autoclass:: Char
    :members:

Signed
~~~~~~

.. autoclass:: Signed
    :members:

.. autoclass:: Signed8
    :members:

.. autoclass:: Signed16
    :members:

.. autoclass:: Signed24
    :members:

.. autoclass:: Signed32
    :members:

.. autoclass:: Signed64
    :members:

Unsigned
~~~~~~~~

.. autoclass:: Unsigned
    :members:

.. autoclass:: Unsigned8
    :members:

.. autoclass:: Unsigned16
    :members:

.. autoclass:: Unsigned24
    :members:

.. autoclass:: Unsigned32
    :members:

.. autoclass:: Unsigned64
    :members:

Bitset
~~~~~~

.. autoclass:: Bitset
    :members:

.. autoclass:: Bitset8
    :members:

.. autoclass:: Bitset16
    :members:

.. autoclass:: Bitset24
    :members:

.. autoclass:: Bitset32
    :members:

.. autoclass:: Bitset64
    :members:

Bool
~~~~

.. autoclass:: Bool
    :members:

.. autoclass:: Bool8
    :members:

.. autoclass:: Bool16
    :members:

.. autoclass:: Bool24
    :members:

.. autoclass:: Bool32
    :members:

.. autoclass:: Bool64
    :members:

Enum
~~~~

.. autoclass:: Enum
    :members:

.. autoclass:: Antivalent
    :members:

.. autoclass:: Enum4
    :members:

.. autoclass:: Enum8
    :members:

.. autoclass:: Enum16
    :members:

.. autoclass:: Enum24
    :members:

.. autoclass:: Enum32
    :members:

.. autoclass:: Enum64
    :members:

Scaled
~~~~~~

.. autoclass:: Scaled
    :members:

.. autoclass:: Scaled8
    :members:

.. autoclass:: Scaled16
    :members:

.. autoclass:: Scaled24
    :members:

.. autoclass:: Scaled32
    :members:

.. autoclass:: Scaled64
    :members:

Fraction
~~~~~~~~

.. autoclass:: Fraction
    :members:

Bipolar
~~~~~~~

.. autoclass:: Bipolar
    :members:

.. autoclass:: Bipolar2
    :members:

.. autoclass:: Bipolar4
    :members:

Unipolar
~~~~~~~~

.. autoclass:: Unipolar
    :members:

.. autoclass:: Unipolar2
    :members:

Datetime
~~~~~~~~

.. autoclass:: Datetime
    :members:

IPv4Address
~~~~~~~~~~~

.. autoclass:: IPv4Address
    :members:


Pointer
=======

.. autoclass:: Pointer
    :members:

.. autoclass:: Pointer8
    :members:

.. autoclass:: Pointer16
    :members:

.. autoclass:: Pointer24
    :members:

.. autoclass:: Pointer32
    :members:

.. autoclass:: Pointer48
    :members:

.. autoclass:: Pointer64
    :members:

Structure Pointer
-----------------

.. autoclass:: StructurePointer
    :members:

.. autoclass:: StructurePointer8
    :members:

.. autoclass:: StructurePointer16
    :members:

.. autoclass:: StructurePointer24
    :members:

.. autoclass:: StructurePointer32
    :members:

.. autoclass:: StructurePointer48
    :members:

.. autoclass:: StructurePointer64
    :members:


Sequence Pointer
----------------

.. autoclass:: SequencePointer
    :members:

Array Pointer
~~~~~~~~~~~~~

.. autoclass:: ArrayPointer
    :members:

.. autoclass:: ArrayPointer8
    :members:

.. autoclass:: ArrayPointer16
    :members:

.. autoclass:: ArrayPointer24
    :members:

.. autoclass:: ArrayPointer32
    :members:

.. autoclass:: ArrayPointer48
    :members:

.. autoclass:: ArrayPointer64
    :members:

Stream Pointer
--------------

.. autoclass:: StreamPointer
    :members:

.. autoclass:: StreamPointer8
    :members:

.. autoclass:: StreamPointer16
    :members:

.. autoclass:: StreamPointer24
    :members:

.. autoclass:: StreamPointer32
    :members:

.. autoclass:: StreamPointer48
    :members:

.. autoclass:: StreamPointer64
    :members:

String Pointer
~~~~~~~~~~~~~~

.. autoclass:: StringPointer
    :members:

.. autoclass:: StringPointer8
    :members:

.. autoclass:: StringPointer16
    :members:

.. autoclass:: StringPointer24
    :members:

.. autoclass:: StringPointer32
    :members:

.. autoclass:: StringPointer48
    :members:

.. autoclass:: StringPointer64
    :members:


Auto String Pointer
~~~~~~~~~~~~~~~~~~~

.. autoclass:: AutoStringPointer
    :members:


Relative Pointer
================

.. autoclass:: RelativePointer
    :members:

.. autoclass:: RelativePointer8
    :members:

.. autoclass:: RelativePointer16
    :members:

.. autoclass:: RelativePointer24
    :members:

.. autoclass:: RelativePointer32
    :members:

.. autoclass:: RelativePointer48
    :members:

.. autoclass:: RelativePointer64
    :members:


Structure Relative Pointer
--------------------------

.. autoclass:: StructureRelativePointer
    :members:

.. autoclass:: StructureRelativePointer8
    :members:

.. autoclass:: StructureRelativePointer16
    :members:

.. autoclass:: StructureRelativePointer24

    :members:
.. autoclass:: StructureRelativePointer32
    :members:

.. autoclass:: StructureRelativePointer48
    :members:

.. autoclass:: StructureRelativePointer64
    :members:


Sequence Relative Pointer
-------------------------

.. autoclass:: SequenceRelativePointer
    :members:

Array Relative Pointer
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ArrayRelativePointer
    :members:

.. autoclass:: ArrayRelativePointer8
    :members:

.. autoclass:: ArrayRelativePointer16
    :members:

.. autoclass:: ArrayRelativePointer24
    :members:

.. autoclass:: ArrayRelativePointer32
    :members:

.. autoclass:: ArrayRelativePointer48
    :members:

.. autoclass:: ArrayRelativePointer64
    :members:

Stream Relative Pointer
-----------------------

.. autoclass:: StreamRelativePointer
    :members:

.. autoclass:: StreamRelativePointer8
    :members:

.. autoclass:: StreamRelativePointer16
    :members:

.. autoclass:: StreamRelativePointer24
    :members:

.. autoclass:: StreamRelativePointer32
    :members:

.. autoclass:: StreamRelativePointer48
    :members:

.. autoclass:: StreamRelativePointer64
    :members:


String Relative Pointer
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: StringRelativePointer
    :members:

.. autoclass:: StringRelativePointer8
    :members:

.. autoclass:: StringRelativePointer16
    :members:

.. autoclass:: StringRelativePointer24
    :members:

.. autoclass:: StringRelativePointer32
    :members:

.. autoclass:: StringRelativePointer48
    :members:

.. autoclass:: StringRelativePointer64
    :members:



Byteorder
=========

.. autoclass:: Byteorder
    :members:
    :undoc-members:
    :inherited-members:

Field Index
===========

.. autoclass:: Index


Field Alignment
===============

.. autoclass:: Alignment

Memory Patch
============

.. autoclass:: Patch

Enumerations
============

.. autoclass:: Enumeration
    :members:

Categories
==========

.. autoclass:: Category
    :members:

Exceptions
==========

.. autoexception:: ByteOrderTypeError

.. autoexception:: EnumTypeError

.. autoexception:: FactoryTypeError

.. autoexception:: MemberTypeError

.. autoexception:: ProviderTypeError

.. autoexception:: ContainerLengthError

.. autoexception:: FieldAddressError

.. autoexception:: FieldAlignmentError

.. autoexception:: FieldByteOrderError

.. autoexception:: FieldIndexError

.. autoexception:: FieldSizeError

.. autoexception:: FieldTypeError

.. autoexception:: FieldValueError

.. autoexception:: FieldValueEncodingError

.. autoexception:: FieldGroupByteOrderError

.. autoexception:: FieldGroupOffsetError

.. autoexception:: FieldGroupSizeError


Utilities
=========

Metadata Converter
------------------

.. autofunction:: d3flare_json

Hexadecimal Viewer
------------------

.. autoclass:: HexViewer
    :members:
