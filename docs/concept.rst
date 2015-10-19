.. _introduction:

Introduction
============

.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from binascii import hexlify, unhexlify
    from konfoo import *

.. _concept:

Concept
-------

KonFoo is based on defining or declaring *byte stream mapper* through classes.
KonFoo has two abstract classes the `Field` class and the `Container` class.

A `Field` holds the value of a area in a byte stream which the `Field` maps
and knows how to unpack and pack its value from and to a byte stream.

A `Container` holds `Field` and/or `Container` classes and knows how to view,
save and load the values of the `Field` items in a `Container` class.

The mixin `Pointer` class has both features of the two base classes and has
an interface to a data `Provider` to read and write byte streams from and
back to the data `Provider` for its referenced *byte stream mapper*.

The build-in decoding and encoding engine unpacks and packs the byte stream
sequential to and from each `Field` in the declared *byte stream mapper*.

How does a *byte stream mapper* look like.
Let's us begin with defining or declaring of one.


.. _mapping_declaration:

Mapping declaration
===================

KonFoo ships with a `Structure` class and many, many `Field` classes to declare
the mapping part of a *byte stream mapper*. The order how you declare the fields
in the mapping declaration defines the order how the fields are decoded and encoded
by the built-in decoding and encoding engine.

.. _create_mapper:

Create a mapping declaration
----------------------------

Define a mapper.

.. code-block:: python

    # Mapping declaration
    class Identifier(Structure):

        def __init__(self):
            super().__init__()        # <- NEVER forget to call it first !!!
            self.version = Byte()     # 1st field
            self.id = Unsigned8()     # 2nd field
            self.length = Decimal8()  # 3rd field
            self.module = Char()      # 4th field
            self.next_index()         # <- Indexes all fields (optional)

.. warning::

    A **mapping declaration** must always align to full bytes or an exception
    will be raised when decoding or encoding an incomplete declaration.


Declare a mapper instance.

    >>> mapper = Structure()
    >>> mapper.version = Byte()
    >>> mapper.id = Unsigned8()
    >>> mapper.length = Decimal8()
    >>> mapper.module = Char()


View a mapper instance.

    >>> mapper
    Structure([('version', Byte(index=Index(byte=0, bit=0,
                                            address=0, base_address=0,
                                            update=False),
                                alignment=(1, 0),
                                bit_size=8,
                                value='0x0')),
                ('id', Unsigned8(index=Index(byte=0, bit=0,
                                             address=0, base_address=0,
                                             update=False),
                                alignment=(1, 0),
                                bit_size=8,
                                value='0x0')),
                ('length', Decimal8(index=Index(byte=0, bit=0,
                                                address=0, base_address=0,
                                                update=False),
                                   alignment=(1, 0),
                                   bit_size=8,
                                   value=0)),
                ('module', Char(index=Index(byte=0, bit=0,
                                            address=0, base_address=0,
                                            update=False),
                                alignment=(1, 0),
                                bit_size=8,
                                value='\x00'))])


Get the length of the mapper as a tuple in the form of
``(number of bytes, remaining bits)``.

    >>> mapper.field_length()
    (4, 0)

.. note::

   The remaining bits must be always zero or the declaration is incomplete.


Get the byte stream index after the last field of the mapper.

    >>> mapper.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)

.. note::

    The method :meth:`next_index` re-indexes all fields in the mapper as well.

List the index of each field in the mapper as a **nested** ordered dictionary.

    >>> pprint(mapper.field_indexes())
    {'version': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'id': Index(byte=1, bit=0, address=1, base_address=0, update=False),
     'length': Index(byte=2, bit=0, address=2, base_address=0, update=False),
     'module': Index(byte=3, bit=0, address=3, base_address=0, update=False)}


List the type of each field in the mapper as a **nested** ordered dictionary.

    >>> pprint(mapper.field_types())
    {'version': 'Byte',
     'id': 'Unsigned8',
     'length': 'Decimal8',
     'module': 'Char'}


Decode a byte stream with a mapper.

    >>> bytestream = bytes.fromhex('01020946f00f00')
    >>> mapper.decode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)


Encode a byte stream with a mapper.

    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> mapper.encode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'01020946'


Accessing a field in a mapper.

    >>> mapper.version
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=(1, 0),
         bit_size=8,
         value='0x1')


Accessing field properties in a mapper.

    >>> mapper.version.value
    '0x1'
    >>> mapper.version.name
    'Byte'
    >>> mapper.version.bit_size
    8
    >>> mapper.version.alignment
    (1, 0)
    >>> mapper.version.byte_order
    Byteorder.auto = 'auto'
    >>> mapper.version.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> mapper.version.index.address
    0


List the value of each field in the mapper as a **nested** ordered dictionary.

    >>> pprint(mapper.field_values())
    {'version': '0x1',
     'id': '0x2',
     'length': 9,
     'module': 'F'}


List all field items in the mapper as a **flat** list.

    >>> pprint(mapper.field_items())
    [('version',
     Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x1')),
    ('id',
     Unsigned8(index=Index(byte=1, bit=0, address=1, base_address=0, update=False),
               alignment=(1, 0),
               bit_size=8,
               value='0x2')),
    ('length',
     Decimal8(index=Index(byte=2, bit=0, address=2, base_address=0, update=False),
              alignment=(1, 0),
              bit_size=8,
              value=9)),
    ('module',
     Char(index=Index(byte=3, bit=0, address=3, base_address=0, update=False),
          alignment=(1, 0),
          bit_size=8,
          value='F'))]


List the value of each field in the mapper as a **flat** list.

    >>> pprint(mapper.to_list())
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]

.. note::

    The class name of the instance is used for the root name as long as no *name*
    is given.


List the value of each field in the mapper as a **flat** ordered dictionary.

    >>> pprint(mapper.to_dict())
    {'Structure': {'version': '0x1',
                   'id': '0x2',
                   'length': 9,
                   'module': 'F'}}

.. note::

    The class name of the instance is used for the root name as long as no *name*
    is given.


Saves the values of each field in the mapper to an INI file.

    >>> mapper.save("_static/structure.ini")

.. note::

    The class name of the instance is used for the section name as long as no *section*
    is given.


Loads the values of each field in the mapper from an INI file.

    >>> mapper.load("_static/structure.ini")
    [Structure]
    Structure.version = 0x1
    Structure.id = 0x2
    Structure.length = 9
    Structure.module = F

.. note::

    The class name of the instance is used for the section name as long as no *section*
    is given.


Get a blueprint of a mapper.

    >>> pprint(mapper.blueprint())
    {'class': 'Structure',
     'name': 'Structure',
     'size': 4,
     'type': 'Structure',
     'member': [{'address': 0,
                 'alignment': [1, 0],
                 'class': 'Byte',
                 'index': [0, 0],
                 'max': 255,
                 'min': 0,
                 'name': 'version',
                 'order': 'auto',
                 'signed': False,
                 'size': 8,
                 'type': 'Field',
                 'value': '0x1'},
                {'address': 1,
                 'alignment': [1, 0],
                 'class': 'Unsigned8',
                 'index': [1, 0],
                 'max': 255,
                 'min': 0,
                 'name': 'id',
                 'order': 'auto',
                 'signed': False,
                 'size': 8,
                 'type': 'Field',
                 'value': '0x2'},
                {'address': 2,
                 'alignment': [1, 0],
                 'class': 'Decimal8',
                 'index': [2, 0],
                 'max': 255,
                 'min': 0,
                 'name': 'length',
                 'order': 'auto',
                 'signed': False,
                 'size': 8,
                 'type': 'Field',
                 'value': 9},
                {'address': 3,
                 'alignment': [1, 0],
                 'class': 'Char',
                 'index': [3, 0],
                 'max': 255,
                 'min': 0,
                 'name': 'module',
                 'order': 'auto',
                 'signed': False,
                 'size': 8,
                 'type': 'Field',
                 'value': 'F'}]}


.. _reuse_mapper:

Re-use of a mapping declaration
-------------------------------

You can re-use a mapping declaration in other mapping declarations.

Define a mapper

.. code-block:: python

    # Mapping declaration
    class Identifier(Structure):

        def __init__(self):
            super().__init__()
            self.version = Byte()
            self.id = Unsigned8()
            self.length = Decimal8()
            self.module = Char()
            self.next_index()

Re-use a mapper

.. code-block:: python

    # Mapping declaration
    class Header(Structure):

        def __init__(self):
            super().__init__()
            self.type = Identifier()   # re-used mapping declaration
            self.size = Decimal32()
            self.next_index()

Declare a mapper instance

    >>> identifier = Structure()
    >>> identifier.version = Byte()
    >>> identifier.id = Unsigned8()
    >>> identifier.length = Decimal8()
    >>> identifier.module = Char()

Re-use a mapper instance

    >>> header = Structure()
    >>> header.type = identifier
    >>> header.size = Decimal32()
    >>> pprint(header.to_list())
    [('Structure.type.version', '0x0'),
     ('Structure.type.id', '0x0'),
     ('Structure.type.length', 0),
     ('Structure.type.module', '\x00'),
     ('Structure.size', 0)]

Declare mapper instances in on step

    >>> mapper = Structure()
    >>> mapper.type = Structure()
    >>> mapper.type.version = Byte()
    >>> mapper.type.id = Unsigned8()
    >>> mapper.type.length = Decimal8()
    >>> mapper.type.module = Char()
    >>> mapper.size = Decimal32()
    >>> pprint(mapper.to_list())
    [('Structure.type.version', '0x0'),
     ('Structure.type.id', '0x0'),
     ('Structure.type.length', 0),
     ('Structure.type.module', '\x00'),
     ('Structure.size', 0)]


.. _aligned_mapper:

Align fields in a mapping declaration
-------------------------------------

Define a mapper with aligned fields

.. code-block:: python

    # Mapping declaration
    class Identifier(Structure):

        def __init__(self):
            super().__init__()
            self.version = Byte(4)       # 1st field aligned to 4 bytes
            self.id = Unsigned(8, 4)     # 2nd field aligned to 4 bytes
            self.length = Decimal(8, 4)  # 3rd field aligned to 4 bytes
            self.module = Char(4)        # 4th field aligned to 4 bytes
            self.next_index()


Declare a mapper instance with aligned fields

    >>> mapper = Structure()
    >>> mapper.version = Byte(4)
    >>> mapper.id = Unsigned(8, 4)
    >>> mapper.length = Decimal(8, 4)
    >>> mapper.module = Char(4)


.. _byte_order_mapper:

Byte order of a mapping declaration
-----------------------------------

Each field in a mapping declaration defines its own decoding/encoding byte order.
The default byte order of a field is 'auto' this means that the field use the
byte order which the byte stream defines to unpack and pack the required bytes
and bits for its field value from and to the byte stream.


.. _parametrized_mapper:

Parametrize a mapping declaration
---------------------------------


.. code-block:: python

    # Parametrized mapping declaration
    class Parametrized(Structure):

        def __init__(self, arg, *args, **kwargs):
            super().__init__()
            # Do stuff here with these parameters


.. _factorized_mapper:

Factorize a mapping declaration
-------------------------------


.. code-block:: python

    # Parametrized mapping declaration
    class Parametrized(Structure):

        def __init__(self, arg, *args, **kwargs):
            super().__init__()
            # Do stuff here with these parameters

.. code-block:: python

    # Factory for a parametrized mapping declaration
    class Factory:
        def __init__(self, arg, *args, **kwargs):
            self.arg = arg
            self.args = args
            self.kwargs = kwargs

        def __call__(self):
            return Parametrized(self.arg, self.args, self.kwargs)



.. _reference_declaration:

Reference declaration
=====================



.. _create_reference:

Create a reference declaration
------------------------------

Define a mapper

.. code-block:: python

    # Mapping declaration
    class Container(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal32()
            self.item = Pointer()
            self.next_index()

Define a reference to a mapper

.. code-block:: python

    # Referenced mapping declaration
    class ContainerPointer(StructurePointer):

        def __init__(self, address=None):
            super().__init__(Container(), address)  # <- Mapping declaration

Declare a mapper.

    >>> mapper = Structure()
    >>> mapper.size = Decimal32()
    >>> mapper.item = Pointer()

Declare a reference to the mapper via a pointer.

    >>> reference = Pointer(mapper)

Declare a reference to the mapper via a specialized pointer for structures.

    >>> reference = StructurePointer(mapper)


.. _nested_reference:

Nesting a reference declaration
-------------------------------

.. code-block:: python

    # Mapping declaration
    class Container(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal32()
            self.item = Pointer(Stream())  # nested reference




.. _array_declaration:

Array declaration
=================

.. code-block:: python

    # Mapping declaration
    class List(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal32()
            self.entry = Array(Signed32)


.. _enumeration_declaration:

Enum declaration
================

.. _create_enumeration:

Create a enumeration declaration
--------------------------------


Reading
=======



Decoding
========



Resizing on the fly
-------------------



Updating on the fly
-------------------



Declaring on the fly
--------------------



Encoding
========



Writing
=======



Saving
======



Loading
=======


