.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *


.. _pointer:

Pointer
=======

KonFoo has a :class:`Pointer` class to reference ...

KonFoo provides the following specialized `pointer`_ fields

* a :class:`StructurePointer` field which refers to a
  :ref:`structure <structure>`
* a :class:`SequencePointer` field which refers to a
  :ref:`sequence <sequence>`
* a :class:`ArrayPointer` field which refers to a
  :ref:`array <array>`
* a :class:`StreamPointer` field which refers to a
  :class:`Stream` :ref:`field <field>`
* a :class:`StringPointer` field which refers to a
  :class:`String` :ref:`field <field>`


.. _relative pointer:

Relative Pointer
----------------

KonFoo has a :class:`RelativePointer` class. The only difference between the a
`pointer`_ field and a `relative pointer`_  field is that the `data object`_
is relative addressed by a `relative pointer`_ field instead of absolute
addressed.

KonFoo provides the following specialized `relative pointer`_ fields

* a :class:`StructureRelativePointer` field which refers to a
  :ref:`structure <structure>`
* a :class:`SequenceRelativePointer` field which refers to a
  :ref:`sequence <sequence>`
* a :class:`ArrayRelativePointer` field which refers to a
  :ref:`array <array>`
* a :class:`StreamRelativePointer` field which refers to a
  :class:`Stream` :ref:`field <field>`
* a :class:`StringRelativePointer` field which refers to a
  :class:`String` :ref:`field <field>`


.. _data object:

Data object
-----------

A `data object`_ of a `pointer`_ field can be any :ref:`field <field>` or
:ref:`container <container>` class.


Define a Data Object
--------------------

You define a structured `data object`_ like this:

.. code-block:: python
    :emphasize-lines: 7

    # Data object
    class Container(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal32()
            self.item = Pointer()  # No data object assigned
            self.next_index()


Define a Data Object Pointer
----------------------------

You define the `pointer`_ for the `data object`_ by

.. code-block:: python
    :emphasize-lines: 5

    # Pointer field
    class ContainerPointer(Pointer):

        def __init__(self, address=None, byte_order=BYTEORDER):
            super().__init__(Container(), address, byte_order)  # Data object


Nesting a Pointer
-----------------

Nesting `pointer`_ fields.

.. code-block:: python
    :emphasize-lines: 7

    # Data object
    class Container(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal32()
            self.item = Pointer(Stream())  # Nested pointer field


.. code-block:: python

    # Pointer
    class ContainerPointer(Pointer):

        def __init__(self, address=None):
            super().__init__(Container(), address)  # Data object


Declare on the fly
------------------

You can declare a `data object`_ on the fly.

    >>> data = Structure()
    >>> data.size = Decimal32()
    >>> data.item = Pointer(Stream())
    >>> pprint(data.to_list(nested=True)) # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', 0),
     ('Structure.item', '0x0'),
     ('Structure.item.data', '')]

You can declare a `pointer`_ on the fly.

    >>> pointer = Pointer(data)
    >>> pprint(pointer.to_list(nested=True))
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]


View a Pointer
--------------

You can **view** a `pointer`_ field

    >>> pointer # doctest: +NORMALIZE_WHITESPACE
    Pointer(index=Index(byte=0, bit=0,
                        address=0, base_address=0,
                        update=False),
            alignment=(4, 0),
            bit_size=32,
            value='0x0')


You can **view** the `data object`_ of a `pointer`_ with the property
:attr:`~Pointer.data` of the `pointer`_ field.

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


Blueprint of a Pointer
----------------------

You can get the blueprint of a `pointer`_ by calling the method
:meth:`~Pointer.blueprint`.

    >>> pprint(pointer.blueprint())
    OrderedDict([('address', 0),
                 ('alignment', [4, 0]),
                 ('class', 'Pointer'),
                 ('index', [0, 0]),
                 ('max', 4294967295),
                 ('min', 0),
                 ('name', 'Pointer'),
                 ('order', 'auto'),
                 ('signed', False),
                 ('size', 32),
                 ('type', 'Pointer'),
                 ('value', '0x0'),
                 ('member',
                  [OrderedDict([('class', 'Structure'),
                                ('name', 'data'),
                                ('size', 2),
                                ('type', 'Structure'),
                                ('member',
                                 [OrderedDict([('address', 0),
                                               ('alignment', [4, 0]),
                                               ('class', 'Decimal32'),
                                               ('index', [0, 0]),
                                               ('max', 4294967295),
                                               ('min', 0),
                                               ('name', 'size'),
                                               ('order', 'auto'),
                                               ('signed', False),
                                               ('size', 32),
                                               ('type', 'Field'),
                                               ('value', 0)]),
                                  OrderedDict([('address', 0),
                                               ('alignment', [4, 0]),
                                               ('class', 'Pointer'),
                                               ('index', [0, 0]),
                                               ('max', 4294967295),
                                               ('min', 0),
                                               ('name', 'item'),
                                               ('order', 'auto'),
                                               ('signed', False),
                                               ('size', 32),
                                               ('type', 'Pointer'),
                                               ('value', '0x0'),
                                               ('member',
                                                [OrderedDict([('address', 0),
                                                              ('alignment', [0, 0]),
                                                              ('class', 'Stream'),
                                                              ('index', [0, 0]),
                                                              ('name', 'data'),
                                                              ('order', 'auto'),
                                                              ('size', 0),
                                                              ('type', 'Field'),
                                                              ('value',
                                                               '')])])])])])])])


Indexing
--------

You can get the next *byte stream* :class:`Index` after a `pointer`_ field
by calling the method :meth:`~Field.next_index`.


    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)


You can index each member of a `data object`_ of a `pointer`_ field
by calling the method :meth:`~Pointer.subscript`.

    >>> pointer.subscript()


Properties of the Field
-----------------------

You can **access** the :ref:`field <field>` properties of a `pointer`_ field
with the following property names:

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


Properties of the Data Object
-----------------------------

You can **access** the properties for the `data object`_ of a `pointer`_ field
with the property names:

    >>> pointer.address
    0
    >>> pointer.base_address
    0
    >>> pointer.data_size
    8
    >>> pointer.bytestream
    ''
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.data_byte_order.value
    'little'


Access the Data Object
----------------------

You can **access** the `data object`_ of a `pointer`_ field with its
property name:

    >>> pointer.data  # doctest: +NORMALIZE_WHITESPACE
    Structure([('size',
                Decimal32(index=Index(byte=0, bit=0,
                                      address=0, base_address=0,
                                      update=False),
                alignment=(4, 0),
                bit_size=32,
                value=0)),
               ('item',
                Pointer(index=Index(byte=4, bit=0,
                                    address=4, base_address=0,
                                    update=False),
                        alignment=(4, 0),
                        bit_size=32,
                        value='0x0'))])


List field indexes
------------------

You can list the :class:`Index` of each :ref:`field <field>` of a `pointer`_
as a **nested** ordered dictionary by calling the method
:meth:`~Pointer.field_indexes`.

    >>> pprint(pointer.field_indexes())
    OrderedDict([('value',
                  Index(byte=0, bit=0, address=0, base_address=0, update=False)),
                 ('data',
                  OrderedDict([('size',
                                Index(byte=0, bit=0, address=0, base_address=0, update=False)),
                               ('item',
                                Index(byte=4, bit=0, address=4, base_address=0, update=False))]))])


List field types
----------------

You can list the **types** of each :ref:`field <field>` of a `pointer`_ as a
**nested** ordered dictionary by calling the method
:meth:`~Pointer.field_types`.

    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'),
                 ('data',
                  OrderedDict([('size', 'Decimal32'), ('item', 'Pointer32')]))])


List field values
-----------------

You can list the **values** of each :ref:`field <field>` of a `pointer`_ as a
**nested** ordered dictionary by calling the method
:meth:`~Pointer.field_values`.


    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0x0'),
                 ('data', OrderedDict([('size', 0), ('item', '0x0')]))])


List field items
----------------

You can list all :ref:`field <field>` items of a `pointer`_ as a **flat** list
by calling the method :meth:`~Pointer.field_items`.

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


View field values
-----------------

You can **view** the *values* of each :ref:`field <field>` of a `pointer`_ as a
**flat** list by calling the method :meth:`~Container.to_list`.

    >>> pprint(pointer.to_list())
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0')]

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *values* of each :ref:`field <field>` of a `pointer`_ as a
**flat** ordered dictionary by calling the method :meth:`~Container.to_dict`.

    >>> pprint(pointer.to_dict())
    OrderedDict([('Pointer',
                  OrderedDict([('value', '0x0'),
                               ('data.size', 0),
                               ('data.item', '0x0')]))])

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


Save field values
-----------------

You can **save** the *values* of each :ref:`field <field>` of a `pointer`_
to an INI file by calling the method :meth:`~Container.save`.

    >>> pointer.save("_static/pointer.ini", nested=True)

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


Load field values
-----------------

You can **load** the *values* of each :ref:`field <field>` of a `pointer`_
from an INI file by calling the method :meth:`~Container.load`.

    >>> pointer.load("_static/pointer.ini", nested=True)
    [Pointer]
    Pointer.value = 0x0
    Pointer.data.size = 0
    Pointer.data.item = 0x0
    Pointer.data.item.data =

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.
