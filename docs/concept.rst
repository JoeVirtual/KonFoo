.. _concept:

Concept
*******

.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from binascii import hexlify, unhexlify
    from konfoo import *

KonFoo is based on declaring *byte stream mapper* through classes.
KonFoo base on two abstract classes the `Field` class and the `Container`
class.

A `Field` holds the value of a area in a byte stream which the `Field` maps
and knows how to unpack and pack its value from and to a byte stream.

A `Container` holds `Field` and/or `Container` classes and knows how to view,
save and load the values of the `Field` items in a `Container` class.

The mixin `Pointer` class has both features of the two base classes and has
an interface to a data `Provider` to read and write byte streams from and
back to the data `Provider` for its attached *byte stream mapper*.

The build-in decoding and encoding engine unpacks and packs the byte stream
sequential to and from each `Field` in the declared *byte stream mapper*.

How does a *byte stream mapper* look like. Let's us begin with declaring of one.

    >>> mapper = Structure()
    >>> mapper.version = Byte(4)
    >>> mapper.id = Unsigned(8, 4)
    >>> mapper.length = Decimal(8, 4)
    >>> mapper.module = Char(4)
    >>> mapper
    Structure([('version', Byte(index=Index(byte=0, bit=0,
                                            address=0, base_address=0,
                                            update=False),
                                alignment=(4, 0),
                                bit_size=8,
                                value='0x0')),
                ('id', Unsigned(index=Index(byte=0, bit=0,
                                            address=0, base_address=0,
                                            update=False),
                                alignment=(4, 0),
                                bit_size=8,
                                value='0x0')),
                ('length', Decimal(index=Index(byte=0, bit=0,
                                               address=0, base_address=0,
                                               update=False),
                                   alignment=(4, 0),
                                   bit_size=8,
                                   value=0)),
                ('module', Char(index=Index(byte=0, bit=0,
                                            address=0, base_address=0,
                                            update=False),
                                alignment=(4, 0),
                                bit_size=8,
                                value='\x00'))])



    List the length of the field in the mapper as tuple
    ``(bytes, remaining bits)``:

    >>> mapper.field_length()
    (4, 0)


    >>> mapper.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)


    >>> mapper.decode(bytes.fromhex('01020946'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)


    List the index of each field in the mapper as a nested ordered dictionary.

    >>> pprint(mapper.field_indexes())
    {'version': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'id': Index(byte=0, bit=8, address=0, base_address=0, update=False),
     'length': Index(byte=0, bit=16, address=0, base_address=0, update=False),
     'module': Index(byte=0, bit=24, address=0, base_address=0, update=False)}


    List the type of each field in the mapper as a nested ordered dictionary.

    >>> pprint(mapper.field_types())
    {'version': 'Byte',
     'id': 'Unsigned8',
     'length': 'Decimal8',
     'module': 'Char'}


    List the value of each field in the mapper as a nested ordered dictionary.

    >>> pprint(mapper.field_values())
    {'version': '0x1',
     'id': '0x2',
     'length': 9,
     'module': 'F'}

    List all field items in the mapper as a flat list.

    >>> pprint(mapper.field_items())
    [('version',
     Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=(4, 0),
          bit_size=8,
          value='0x1')),
    ('id',
     Unsigned(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=(4, 0),
              bit_size=8,
              value='0x2')),
    ('length',
     Decimal(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
             alignment=(4, 0),
             bit_size=8,
             value=9)),
    ('module',
     Char(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=(4, 0),
          bit_size=8,
          value='F'))]


    List the value of each field in the mapper as a **flat** list.

    >>> pprint(mapper.to_list())
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]


    List the value of each field in the mapper as a **flat** ordered dictionary.

    >>> pprint(mapper.to_dict())
    {'Structure': {'version': '0x1',
                   'id': '0x2',
                   'length': 9,
                   'module': 'F'}}


    Saves the values of each field in the mapper to a INI file.

    >>> mapper.save("_static/structure.ini")


    Loads the values of each field in the mapper from a INI file.

    >>> mapper.load("_static/structure.ini")
    [Structure]
    Structure.version = 0x1
    Structure.id = 0x2
    Structure.length = 9
    Structure.module = F


Create a mapping declaration
----------------------------

KonFoo gives you for declaring the mapping part of a *byte stream mapper*
a empty `Structure` class and many, many `Field` classes.

The order how you declare the fields in the constructor of the mapping
declaration defines the order how the fields are decoded and encoded
by the built-in decoding and encoding engine.

.. code-block:: python

    # Mapping declaration
    class Identifier(Structure):

        def __init__(self):
            super().__init__()
            self.version = Byte(4)       # 1st field aligned to 4 bytes
            self.id = Unsigned(8, 4)     # 2nd field aligned to 4 bytes
            self.length = Decimal(8, 4)  # 3rd field aligned to 4 bytes
            self.module = Char(4)        # 4th field aligned to 4 bytes

.. _reuse_declaration:

Re-use a mapping declaration
----------------------------

You can re-use a mapping declaration in other mapping declarations.

.. code-block:: python

    # Mapping declaration
    class Header(Structure):

        def __init__(self):
            super().__init__()
            self.type_id = Identifier()   # re-used mapping declaration
            self.size = Decimal(32)



Refer to nested byte area in a mapping declaration
--------------------------------------------------

.. code-block:: python

    # Mapping declaration
    class Buffer(Structure):

        def __init__(self):
            super().__init__()
            self.type_id = Identifier()
            self.size = Decimal(32)
            self.length = Decimal(32)
            self.payload = StreamPointer(0)  # nested reference


.. code-block:: python

    # Mapping declaration
    class List(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal(32)
            self.entry = Array(Signed32)




Factorising
-----------



Resizing
--------




.. _fields:

Fields
======

Fields ...


Properties
----------

Name

Size

Alignment

Byteorder

Index

Value



Aligning
--------



Indexing
--------



Decoding
--------



Unpacking
---------



Encoding
--------



Packing
-------



.. _structures:

Structures
==========

Structures ...


Declaring
---------

Example:

.. code-block:: python

    class Identifier(Structure):

        def __init__(self):
            super().__init__()
            self.version = Byte(4)
            self.id = Unsigned(8, 4)
            self.length = Decimal(8, 4)
            self.module = Char(4)


Nesting
-------

Example:

.. code-block:: python

    class Header(Structure):

        def __init__(self):
            super().__init__()
            self.info = Identifier()


.. _arrays:

Arrays
======

Arrays ...


Declaring
---------



Factorising
-----------



Resizing
--------



.. _pointers:

Pointers
========

Pointers ...


Properties
----------

address

base_address

data object

byte order

size

bytestream



Reading
-------



Writing
-------



.. _providers:

Providers
=========

Providers ...


Properties
----------

source

stream



.. _containers:

Containers
==========

Containers ...


Viewing
-------



Saving
------



Loading
-------