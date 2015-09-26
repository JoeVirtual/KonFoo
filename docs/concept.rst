.. _concept:

Concept
*******

.. currentmodule:: konfoo

KonFoo is based on declaring byte stream mapper through classes.
KonFoo base on two abstract classes the `Field` class and the `Container`
class.

A `Field` holds the value of a area in a byte stream which the `Field` maps
and knows how to unpack and pack its value from and to a byte stream.

A `Container` holds `Container` and/or `Field` classes and knows how to view,
save and load the values of the `Field` items in a `Container` class.

The mixin `Pointer` class has both features of the two base classes and has
an interface to a data `Provider` to read and write byte streams from and
back to the data `Provider` for its attached byte stream mapper.

The build-in decoding and encoding engine unpacks and packs the byte stream
sequential to and from each `Field` in the declared byte stream mapper.


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

