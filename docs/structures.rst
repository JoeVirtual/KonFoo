.. _structures:

Structures
==========

.. currentmodule:: konfoo

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


Example
-------

.. testsetup:: *

    from pprint import pprint
    from konfoo import *


.. doctest:: ['structure']

    >>> class Identifier(Structure):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.version = Byte(4)
    ...         self.id = Unsigned(8, 4)
    ...         self.length = Decimal(8, 4)
    ...         self.module = Char(4)
    >>> id = Identifier()
    >>> id.field_length()
    (4, 0)
    >>> id.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pprint(id.field_indexes())
    {'version': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'id': Index(byte=0, bit=8, address=0, base_address=0, update=False),
     'object': Index(byte=0, bit=16, address=0, base_address=0, update=False),
     'module': Index(byte=0, bit=24, address=0, base_address=0, update=False)}
    >>> pprint(id.field_types())
    {'version': 'Byte',
     'id': 'Decimal8',
     'object': 'Char',
     'module': 'Char'}
    >>> pprint(id.field_values())
    {'version': '0x0',
     'id': 0,
     'object': '\x00',
     'module': '\x00'}

List the `Field` values of a `Structure` via a
standard list:

.. doctest:: ['structure']

    >>> pprint(id.to_list())
    [('Identifier.version', '0x0'),
     ('Identifier.id', 0),
     ('Identifier.object', '\x00'),
     ('Identifier.module', '\x00')]


List the `Field` values of a `Structure` via a
standard ordered dictionary.


.. doctest:: ['structure']

    >>> pprint(id.to_dict())
    {'Identifier': {'version': '0x0',
                    'id': 0,
                    'object': '\x00',
                    'module': '\x00'}}