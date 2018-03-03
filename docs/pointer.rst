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
  :ref:`structure <structure>`.
* a :class:`SequencePointer` field which refers to a
  :ref:`sequence <sequence>`.
* a :class:`ArrayPointer` field which refers to an
  :ref:`array <array>`.
* a :class:`StreamPointer` field which refers to a
  :class:`Stream` :ref:`field <field>`.
* a :class:`StringPointer` field which refers to a
  :class:`String` :ref:`field <field>`.


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
            self.index_fields()


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


Metadata of a Pointer
----------------------

You can get the metadata of a `pointer`_ by calling the method
:meth:`~Pointer.describe`.

    >>> pprint(pointer.describe())
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

You can index the `pointer`_ field by calling the method
:meth:`~Field.index_field`.
The :class:`Index` after the `pointer`_ field is returned.

    >>> pointer.index_field(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)


You can index each :ref:`field <field>` in the `data object`_ referenced by the
`pointer`_ field by calling the method :meth:`~Pointer.index_data`.

    >>> pointer.index_data()

You can index the `pointer`_ field and each :ref:`field <field>` in the
`data object`_ referenced by the `pointer`_ field by calling the method
:meth:`~Pointer.index_fields`.
The :class:`Index` after the `pointer`_ field is returned.


    >>> pointer.index_fields(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)


Attributes of the Field
-----------------------

You can **access** the :ref:`field <field>` attributes of a `pointer`_ field
with the following attribute names:

    >>> # Field name.
    >>> pointer.name
    'Pointer32'
    >>> # Field value.
    >>> pointer.value
    '0x0'
    >>> # Field bit size.
    >>> pointer.bit_size
    32
    >>> # Field alignment.
    >>> pointer.alignment
    (4, 0)
    >>> # Field alignment: byte size.
    >>> pointer.alignment[0]
    4
    >>> # Field alignment: bit offset.
    >>> pointer.alignment[1]
    0
    >>> # Field byte order.
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> # Field byte order value.
    >>> pointer.byte_order.value
    'auto'
    >>> # Field index.
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> # Field index: byte offset within the byte stream.
    >>> pointer.index.byte
    0
    >>> # Field index: bit offset within the byte stream.
    >>> pointer.index.bit
    0
    >>> # Field index: memory address in the data source.
    >>> pointer.index.address
    0
    >>> # Field index: base address of the byte stream in the data source.
    >>> pointer.index.base_address
    0
    >>> # Field index: update request for the byte stream from the data source.
    >>> pointer.index.update
    False
    >>> # Field is a bit field.
    >>> pointer.is_bit()
    False
    >>> # Field is a boolean field.
    >>> pointer.is_bool()
    False
    >>> # Field is a decimal field.
    >>> pointer.is_decimal()
    True
    >>> # Field is a float field.
    >>> pointer.is_float()
    False
    >>> # Field is a pointer field.
    >>> pointer.is_pointer()
    True
    >>> # Field is a stream field.
    >>> pointer.is_stream()
    False
    >>> # Field is a string field.
    >>> pointer.is_string()
    False


Attributes of the Data Object
-----------------------------

You can **access** the attributes for the `data object`_ referenced by the
`pointer`_ field with the attribute names:

    >>> # Absolute address of the data object referenced by the pointer.
    >>> pointer.address
    0
    >>> # Base address of the data object referenced by the pointer.
    >>> pointer.base_address
    0
    >>> # Byte size of the data object referenced by the pointer.
    >>> pointer.data_size
    8
    >>> # Byte stream for the data object referenced by the pointer.
    >>> pointer.bytestream
    ''
    >>> # Byte order for the data object referenced by the pointer.
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.data_byte_order.value
    'little'


Access the Data Object
----------------------

You can **access** the `data object`_ referenced by a `pointer`_ field with its
attribute name:

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


View Field Attributes
---------------------

You can view the **attributes** of a `pointer`_ field and of each :ref:`field
<field>` in the `data object`_ referenced by the `pointer`_ field as a
**nested** ordered dictionary by calling the method :meth:`~Pointer.view_fields`.


    >>> pointer.view_fields()
    OrderedDict([('value', '0x0'),
                 ('data', OrderedDict([('size', 0), ('item', '0x0')]))])


List Field Items
----------------

You can list all :ref:`field <field>` items of a `pointer`_ as a **flat** list
by calling the method :meth:`~Pointer.field_items`.

    >>> pointer.field_items() # doctest: +NORMALIZE_WHITESPACE
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


List Field Values
-----------------

You can **list** the *values* of each :ref:`field <field>` of a `pointer`_ as a
**flat** list by calling the method :meth:`~Container.to_list`.

    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0')]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *values* of each :ref:`field <field>` of a `pointer`_ as a
**flat** ordered dictionary by calling the method :meth:`~Container.to_dict`.

    >>> pointer.to_dict() # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Pointer',
                  OrderedDict([('value', '0x0'),
                               ('data.size', 0),
                               ('data.item', '0x0')]))])

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Save Field Values
-----------------

You can **save** the *values* of each :ref:`field <field>` of a `pointer`_
to an ``.ini`` file by calling the method :meth:`~Container.save`.

    >>> # List the field values of the pointer.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]
    >>> # Save the field values to an '.ini' file.
    >>> pointer.save("_static/pointer.ini", nested=True)

The generated ``.ini`` file for the pointer looks like this:

.. literalinclude:: _static/pointer.ini
    :language: ini

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.


Load Field Values
-----------------

You can **load** the *values* of each :ref:`field <field>` of a `pointer`_
from an ``.ini`` file by calling the method :meth:`~Container.load`.

    >>> # Load the field values from an '.ini' file.
    >>> pointer.load("_static/pointer.ini", nested=True) # doctest: +NORMALIZE_WHITESPACE
    [Pointer]
    Pointer.value = 0x0
    Pointer.data.size = 0
    Pointer.data.item = 0x0
    Pointer.data.item.data =
    >>> # List the field values of the pointer.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.
