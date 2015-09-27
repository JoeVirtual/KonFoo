.. _concept:

Concept
=======

.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from binascii import hexlify, unhexlify
    from konfoo import *

KonFoo is based on declaring *byte stream mapper* through classes.
KonFoo has two abstract classes the `Field` class and the `Container`
class.

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
Let's us begin with declaring of one.


.. _mapping_declaration:

Mapping declaration
===================

KonFoo ships with a `Structure` class and many, many `Field` classes to declare
the mapping part of a *byte stream mapper* . The order how you declare the fields
in the mapping declaration defines the order how the fields are decoded and encoded
by the built-in decoding and encoding engine.

.. _create_mapping:

Create a mapping declaration
----------------------------


Define a mapper

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


Declare a mapper

    >>> mapper = Structure()
    >>> mapper.version = Byte()
    >>> mapper.id = Unsigned8()
    >>> mapper.length = Decimal8()
    >>> mapper.module = Char()


View a declaration

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

    Re-indexes all fields in the mapper as well.

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


    >>> mapper.decode(bytes.fromhex('01020946'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)


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


Saves the values of each field in the mapper to a INI file.

    >>> mapper.save("_static/structure.ini")

.. note::

    The class name of the instance is used for the section name as long as no *section*
    is given.


Loads the values of each field in the mapper from a INI file.

    >>> mapper.load("_static/structure.ini")
    [Structure]
    Structure.version = 0x1
    Structure.id = 0x2
    Structure.length = 9
    Structure.module = F

.. note::

    The class name of the instance is used for the section name as long as no *section*
    is given.


.. _reuse_mapping:

Re-use of a mapping declaration
-------------------------------

You can re-use a mapping declaration in other mapping declarations.

Define a mapper

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


.. code-block:: python

    # Mapping declaration
    class Header(Structure):

        def __init__(self):
            super().__init__()
            self.type_id = Identifier()   # re-used mapping declaration
            self.size = Decimal(32)
            self.next_index()


.. _aligning_mapping:

Aligning of fields in a mapping declaration
-------------------------------------------

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


Declare a mapper

    >>> mapper = Structure()
    >>> mapper.version = Byte(4)
    >>> mapper.id = Unsigned(8, 4)
    >>> mapper.length = Decimal(8, 4)
    >>> mapper.module = Char(4)


.. _byte_order_mapping:

Byte order of a mapping declaration
-----------------------------------




.. _factorising_mapping:

Factorising a mapping declaration
---------------------------------


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
            self.size = Signed16()
            self.item = StreamPointer(0)
            self.next_index()

Define a reference to a mapper

.. code-block:: python

    # Referenced mapping declaration
    class ContainerPointer(StructurePointer):

        def __init__(self, address=None):
            super().__init__(Container(), address)  # <- Mapping declaration

Declare a mapper.

    >>> mapper = Structure()
    >>> mapper.size = Signed16()
    >>> mapper.item = StreamPointer(0)

Declare a reference to the mapper via a pointer.

    >>> reference = Pointer(mapper)

Declare a reference to the mapper via a specialized pointer for structures.

    >>> reference = StructurePointer(mapper)


.. _nesting_reference:

Nesting a reference declaration
-------------------------------

.. code-block:: python

    # Mapping declaration
    class Buffer(Structure):

        def __init__(self):
            super().__init__()
            self.type_id = Identifier()  # re-used mapping declaration
            self.size = Decimal(32)
            self.length = Decimal(32)
            self.payload = StreamPointer(0)  # nested reference




.. _array_declaration:

Array declaration
=================


.. code-block:: python

    # Mapping declaration
    class List(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal(32)
            self.entry = Array(Signed32)



.. _enumeration_declaration:

Enum declaration
================




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








