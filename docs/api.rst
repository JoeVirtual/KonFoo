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

Pointer
=======

.. autoclass:: Pointer
   :members:

.. autoclass:: Pointer8
   :members:

.. autoclass:: Pointer16
   :members:

.. autoclass:: Pointer32
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

.. autoclass:: StructurePointer32
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

.. autoclass:: ArrayPointer32
   :members:

Stream Pointer
--------------

.. autoclass:: StreamPointer
   :members:

.. autoclass:: StreamPointer8
   :members:

.. autoclass:: StreamPointer16
   :members:

.. autoclass:: StreamPointer32
   :members:

String Pointer
~~~~~~~~~~~~~~

.. autoclass:: StringPointer
   :members:
   
.. autoclass:: StringPointer8
   :members:

.. autoclass:: StringPointer16
   :members:

.. autoclass:: StringPointer32
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

.. autoclass:: RelativePointer32
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

.. autoclass:: StructureRelativePointer32
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

.. autoclass:: ArrayRelativePointer32
   :members:

Stream Relative Pointer
-----------------------

.. autoclass:: StreamRelativePointer
   :members:

.. autoclass:: StreamRelativePointer8
   :members:

.. autoclass:: StreamRelativePointer16
   :members:

.. autoclass:: StreamRelativePointer32
   :members:

String Relative Pointer
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: StringRelativePointer
   :members:

.. autoclass:: StringRelativePointer8
   :members:

.. autoclass:: StringRelativePointer16
   :members:

.. autoclass:: StringRelativePointer32
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

Blueprint to JSON Converter
---------------------------

.. autofunction:: d3json

Hexadecimal Viewer
------------------

.. autoclass:: HexViewer
   :members: