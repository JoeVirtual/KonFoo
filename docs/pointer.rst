.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *

.. _pointer_template:

Pointer template
================

KonFoo has a :class:`Pointer` class to reference ...

The :class:`RelativePointer` class is the same as the :class:`Pointer` class only
the template for the data object is relative addressed instead of absolute
addressed.

KonFoo provides specialized pointers for :class:`Structures <StructurePointer>`,
:class:`Sequences <SequencePointer>`, :class:`Arrays <ArrayPointer>`,
:class:`Streams <StreamPointer>`  and :class:`Strings <StringPointer>` which have
additional features for their data object templates.

.. _pointer_members:

Members
-------




.. _pointer_data_object:

Data object
-----------



Define a template
-----------------

Define a data object template.

.. code-block:: python

    # Data object template
    class Container(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal32()
            self.item = Pointer()  # No template
            self.next_index()

Define a pointer template.

.. code-block:: python

    # Pointer template
    class ContainerPointer(Pointer):

        def __init__(self, address=None):
            super().__init__(Container(), address)  # Data object template


Nesting
-------

Nesting pointer templates.

.. code-block:: python

    # Data object template
    class Container(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal32()
            self.item = Pointer(Stream())  # Nested template

.. code-block:: python

    # Pointer template
    class ContainerPointer(Pointer):

        def __init__(self, address=None):
            super().__init__(Container(), address)  # Data object template


Declare a template on the fly
-----------------------------

Declare a data object pointer template on the fly.

    >>> data = Structure()
    >>> data.size = Decimal32()
    >>> data.item = Pointer(Stream())
    >>> pprint(data.to_list(nested=True))
    [('Structure.size', 0),
     ('Structure.item', '0x0'),
     ('Structure.item.data', b'')]

Declare a template on the fly.

    >>> pointer = Pointer(data)
    >>> pprint(pointer.to_list(nested=True))
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', b'')]


View of a template
------------------

View the pointer template.

    >>> pointer # doctest: +NORMALIZE_WHITESPACE
    Pointer(index=Index(byte=0, bit=0,
                        address=0, base_address=0,
                        update=False),
            alignment=(4, 0),
            bit_size=32,
            value='0x0')


View the data object template of a pointer template.

    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    Structure([('size',
                Decimal32(index=Index(byte=0, bit=0,
                                      address=0, base_address=0,
                                      update=False),
                alignment=(4, 0),
                bit_size=32,
                value=0)),
               ('item',
                Pointer(index=Index(byte=0, bit=0,
                                    address=0, base_address=0,
                                    update=False),
                        alignment=(4, 0),
                        bit_size=32,
                        value='0x0'))])


Blueprint of a template
-----------------------

Blueprint of a template.

    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'Pointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'Pointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0x0',
     'member': [{'class': 'Structure',
                 'name': 'Structure',
                 'size': 2,
                 'type': 'Structure',
                 'member': [{'address': 0,
                             'alignment': [4, 0],
                             'class': 'Decimal32',
                             'index': [0, 0],
                             'max': 4294967295,
                             'min': 0,
                             'name': 'size',
                             'order': 'auto',
                             'signed': False,
                             'size': 32,
                             'type': 'Field',
                             'value': 0},
                            {'address': 0,
                             'alignment': [4, 0],
                             'class': 'Pointer',
                             'index': [0, 0],
                             'max': 4294967295,
                             'min': 0,
                             'name': 'item',
                             'order': 'auto',
                             'signed': False,
                             'size': 32,
                             'type': 'Pointer',
                             'value': '0x0',
                             'member': [{'address': 0,
                                         'alignment': [0, 0],
                                         'class': 'Stream',
                                         'index': [0, 0],
                                         'name': 'Stream',
                                         'order': 'auto',
                                         'size': 0,
                                         'type': 'Field',
                                         'value': ''}]}]}]}


Accessing a member
------------------

Accessing the properties for the :class:`Pointer` field itself of a template.

    >>> pointer.name
    'Pointer32'
    >>> pointer.value
    '0x0'
    >>> pointer.bit_size
    32
    >>> pointer.alignment
    (4, 0)
    >>> pointer.alignment[0]
    4
    >>> pointer.alignment[1]
    0
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.byte_order.value
    'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index.byte
    0
    >>> pointer.index.bit
    0
    >>> pointer.index.address
    0
    >>> pointer.index.base_address
    0
    >>> pointer.index.update
    False
    >>> pointer.is_bit()
    False
    >>> pointer.is_bool()
    False
    >>> pointer.is_decimal()
    True
    >>> pointer.is_float()
    False
    >>> pointer.is_pointer()
    True
    >>> pointer.is_stream()
    False
    >>> pointer.is_string()
    False

Accessing the properties for the data object of a :class:`Pointer` template.

    >>> pointer.address
    0
    >>> pointer.base_address
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.order.value
    'little'
    >>> pointer.size
    8
    >>> pointer.bytestream
    b''


Accessing a member of the data object template in a :class:`Pointer` template.

    >>> pointer.data.size # doctest: +NORMALIZE_WHITESPACE
    Decimal32(index=Index(byte=0, bit=0,
                          address=0, base_address=0,
                          update=False),
              alignment=(4, 0),
              bit_size=32,
              value=0)

Indexing
--------

Get the next :class:`Index` after the :class:`Pointer` field.

    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)

Indexes the data object template.

    >>> pointer.subscript()


List fields
-----------

List all field items in the template as a **flat** list.

    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      Pointer(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=(4, 0),
              bit_size=32,
              value='0x0')),
     ('data.size',
      Decimal32(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
                alignment=(4, 0),
                bit_size=32,
                value=0)),
     ('data.item',
      Pointer(index=Index(byte=4, bit=0, address=4, base_address=0, update=False),
              alignment=(4, 0),
              bit_size=32,
              value='0x0'))]


List field indexes
------------------


List the :class:`Index` of each field in the template as a **nested** ordered
dictionary.

    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': {'size': Index(byte=0, bit=0, address=0, base_address=0, update=False),
              'item': Index(byte=4, bit=0, address=4, base_address=0, update=False)}}


List field types
----------------

List the type of each field in the template as a **nested** ordered dictionary.

    >>> pprint(pointer.field_types())
    {'value': 'Pointer32',
     'data': OrderedDict([('size', 'Decimal32'), ('item', 'Pointer32')])}


List field values
-----------------

List the value of each field in the template as a **nested** ordered dictionary.

    >>> pprint(pointer.field_values())
    {'value': '0x0',
     'data': OrderedDict([('size', 0), ('item', '0x0')])}

List the value of each field in the template as a **flat** list.

    >>> pprint(pointer.to_list())
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0')]

.. note::

    The class name of the instance is used for the root name as long as no *name*
    is given.

List the value of each field in the mapper as a **flat** ordered dictionary.

    >>> pprint(pointer.to_dict())
    {'Pointer': {'value': '0x0',
                 'data.size': 0,
                 'data.item': '0x0'}}

.. note::

    The class name of the instance is used for the root name as long as no *name*
    is given.


Save field values
-----------------

Saves the values of each field in the template to an INI file.

    >>> pointer.save("_static/pointer.ini", nested=True)

.. note::

    The class name of the instance is used for the section name as long as no *section*
    is given.


Load field values
-----------------

Loads the values of each field in the template from an INI file.

    >>> pointer.load("_static/pointer.ini", nested=True)
    [Pointer]
    Pointer.value = 0x0
    Pointer.data.size = 0
    Pointer.data.item = 0x0
    Pointer.data.item.data = b''

.. note::

    The class name of the instance is used for the section name as long as no *section*
    is given.
