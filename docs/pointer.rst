.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *


.. _pointer:

Pointer
=======

KonFoo has a :class:`Pointer` class to reference a memory area in a *data source*
to be mapped with its attached `data object`_.

The :class:`Pointer` class provides an interface to *read* the necessary amount of
bytes for its attached `data object`_ through a data :ref:`provider <provider>`
*from* a *data source*.

The :class:`Pointer` class provides an interface to *write* the field :ref:`values
<field value>` of any :ref:`container <container>` or :ref:`field <field>` in its
attached `data object`_ through a data :ref:`provider <provider>` *to* the
*data source*.

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
* a :class:`ArrayRelativePointer` field which refers to an
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


Define a Data object
--------------------

You **define** a `data object`_ like this:

.. code-block:: python
    :emphasize-lines: 7-8

    # Data object
    class DataObject(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal(16)
            # Nested pointer field with no attached data object
            self.item = Pointer()
            self.index_fields()


Define a Data object pointer
----------------------------

You **define**  a `pointer`_ for a `data object`_ like this:

.. code-block:: python
    :emphasize-lines: 5-8

    # Pointer field
    class DataObjectPointer(Pointer):

        def __init__(self, address=None, byte_order=BYTEORDER):
            # Attach the data object to the pointer.
            super().__init__(template=DataObject(),
                             address=address,
                             data_order=byte_order)


Nest a Pointer
--------------

You can *nest* a `pointer`_ in a `data object`_.

.. code-block:: python
    :emphasize-lines: 7-8

    # Data object
    class DataObject(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal(16)
            # Nested pointer refers to a string field
            self.item = Pointer(String())


.. code-block:: python

    # Pointer
    class DataObjectPointer(Pointer):

        def __init__(self, address=None, byte_order=BYTEORDER):
            # Attach the data object to the pointer.
            super().__init__(DataObject(), address, byte_order)


Declare on the fly
------------------

You can **declare** a `data object`_ on the fly.

    >>> # Create a data object.
    >>> data = Structure()
    >>> # Add a field to the data object.
    >>> data.size = Decimal(16)
    >>> # Add a nested pointer field to the data object.
    >>> data.item = Pointer(String())
    >>> # List the field values in the data object.
    >>> data.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', 0),
     ('Structure.item', '0x0')]
    >>> # List the all field values in the data object.
    >>> data.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', 0),
     ('Structure.item', '0x0'),
     ('Structure.item.data', '')]

You can **declare** a `pointer`_ on the fly.

    >>> # Create a pointer for the data object.
    >>> pointer = Pointer(data)
    >>> # List the field values of the pointer and its attached data object.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0')]
    >>> # List all field values of the pointer and its attached data objects.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]


Access the Data object
----------------------

You can **access** the `data object`_ referenced by a `pointer`_ with the
:attr:`~Pointer.data` attribute of a `pointer`_ field.

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # Index the pointer field and its attached data object.
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Access the data object referenced by the pointer field.
    >>> pointer.data  # doctest: +NORMALIZE_WHITESPACE
    Structure([('size',
                Decimal(index=Index(byte=0, bit=0,
                                    address=0, base_address=0,
                                    update=False),
                        alignment=(2, 0),
                        bit_size=16,
                        value=0)),
               ('item',
                Pointer(index=Index(byte=2, bit=0,
                                    address=2, base_address=0,
                                    update=False),
                        alignment=(4, 0),
                        bit_size=32,
                        value='0x0'))])


Size of the Data object
-----------------------

You can get the byte **size** of the `data object`_ referenced by the `pointer`_
with the :attr:`~Pointer.data_size` attribute of a `pointer`_ field.

    >>> # Byte size of the data object referenced by the pointer.
    >>> pointer.data_size
    6


Index the Data object
---------------------

You can index each :ref:`field <field>` in the `data object`_ referenced by the
`pointer`_ field by calling the method :meth:`~Pointer.index_data`

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # List the field indexes of the data object referenced by the pointer.
    >>> pointer.data.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', Index(byte=0, bit=0,
                              address=0, base_address=0,
                              update=False)),
     ('Structure.item', Index(byte=0, bit=0,
                              address=0, base_address=0,
                              update=False))]
    >>> # Indexes the data object referenced by the pointer.
    >>> pointer.index_data()
    >>> # List the field indexes of the data object referenced by the pointer.
    >>> pointer.data.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', Index(byte=0, bit=0,
                              address=0, base_address=0,
                              update=False)),
     ('Structure.item', Index(byte=2, bit=0,
                              address=2, base_address=0,
                              update=False))]


Address of the Data object
--------------------------

You can get the *data source* **address** of the `data object`_ referenced by the
`pointer`_ with the :attr:`~Pointer.address` attribute of a `pointer`_ field.

    >>> # Data source address of the data object referenced by the pointer.
    >>> pointer.address
    0


Byte order of the Data object
-----------------------------

You can get the **byte order** used by the `pointer`_ to deserialize or serialize
its referenced `data object`_ with the :attr:`~Pointer.data_byte_order` attribute
of a `pointer`_ field.

    >>> # Byte order to de-/serialize the data objects referenced by the pointer.
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.data_byte_order.value
    'little'

.. note:: The default byte order for a `data object`_ is little endian.

You can set the **byte order** used by the `pointer`_ to deserialize or serialize
its referenced `data object`_ with the :attr:`~Pointer.data_byte_order` attribute
of a `pointer`_ field.

    >>> # Set byte order to de-/serialize the data objects referenced by the pointer.
    >>> pointer.data_byte_order = 'big'
    >>> # Byte order to de-/serialize the data objects referenced by the pointer.
    >>> pointer.data_byte_order
    Byteorder.big = 'big'


Byte stream for the Data object
-------------------------------

You can get the internal **byte stream** used by the `pointer`_ to deserialize or
serialize its referenced `data object`_ with the :attr:`~Pointer.bytestream`
attribute of a `pointer`_ field.

    >>> # Internal byte stream to de-/serialize the data object referenced by the pointer.
    >>> pointer.bytestream
    ''

You can set the internal **byte stream** used by the `pointer`_ to deserialize or
serialize its referenced `data object`_ with the :attr:`~Pointer.bytestream`
attribute of a `pointer`_ field.

    >>> # Set the internal byte stream of the pointer.
    >>> pointer.bytestream = '000000000000'
    >>> pointer.bytestream
    '000000000000'


Deserialize the Data object
---------------------------

You can **deserialize** the `data object`_ referenced by the `pointer`_ by calling
the method :meth:`~Pointer.deserialize_data` of a `pointer`_ field.

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # List the field values in the data object referenced by the pointer.
    >>> pointer.data.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', 0),
     ('Structure.item', '0x0')]
    >>> # Internal byte stream of the pointer.
    >>> pointer.bytestream
    ''
    >>> # Deserialize the data object with an external byte stream.
    >>> pointer.deserialize_data(bytes.fromhex('0e0010000000'))
    Index(byte=6, bit=0, address=6, base_address=0, update=False)
    >>> # Set the internal byte stream of the pointer.
    >>> pointer.bytestream = '0e0010000000'
    >>> # Deserialize the data object with the internal byte stream.
    >>> pointer.deserialize_data()
    Index(byte=6, bit=0, address=6, base_address=0, update=False)
    >>> # List the field values in the data object referenced by the pointer.
    >>> pointer.data.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', 14),
     ('Structure.item', '0x10')]


Serialize the Data object
-------------------------

You can **serialize** the `data object`_ referenced by the `pointer`_ by calling
the method :meth:`~Pointer.serialize_data` of a `pointer`_ field.

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # List the field values in the data object referenced by the pointer.
    >>> pointer.data.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', 0),
     ('Structure.item', '0x0')]
    >>> # Serialize the data object referenced by the pointer.
    >>> pointer.serialize_data()
    b'\x00\x00\x00\x00\x00\x00'


Read the Byte stream
--------------------

You can **read** the *byte stream* used by the `pointer`_ to deserialize its
referenced `data object`_ **from** a *data source* through a data
:ref:`provider <provider>` by calling the method :meth:`~Pointer.read_from` of
a `pointer`_ field.



Initialize a Pointer
--------------------

You can **initialize** the fields in a `pointer`_ by calling the method
:meth:`~Pointer.initialize_fields`.

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String(14))))
    >>> # View all field values of the pointer and its attached data objects.
    >>> pointer.view_fields(nested=True) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('value', '0x0'),
                 ('data',
                  OrderedDict([('size', 0),
                               ('item',
                                OrderedDict([('value', '0x0'),
                                             ('data', '')]))]))])
    >>> # Initialize the fields values of the pointer and its attached data objects.
    >>> pointer.initialize_fields({
    ...     'value': 0x1,
    ...     'data': {
    ...         'size': 14,
    ...         'item': {
    ...             'value': 0x10,
    ...             'data': 'Konfoo is Fun'
    ...         }
    ...     }
    ... })
    >>> # List the field values of the pointer and its attached data object.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x1'),
     ('Pointer.data.size', 14),
     ('Pointer.data.item', '0x10')]
    >>> # List all field values of the pointer and its attached data objects.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x1'),
     ('Pointer.data.size', 14),
     ('Pointer.data.item', '0x10'),
     ('Pointer.data.item.data', 'Konfoo is Fun')]


View a Pointer
--------------

You can **view** a `pointer`_ field.

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # Index the pointer field and its attached data object.
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Display the pointer field.
    >>> pointer # doctest: +NORMALIZE_WHITESPACE
    Pointer(index=Index(byte=0, bit=0,
                        address=0, base_address=0,
                        update=False),
            alignment=(4, 0),
            bit_size=32,
            value='0x0')
    >>> # Display the data object referenced by the pointer
    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    Structure([('size',
                Decimal(index=Index(byte=0, bit=0,
                                    address=0, base_address=0,
                                    update=False),
                        alignment=(2, 0),
                        bit_size=16,
                        value=0)),
               ('item',
                Pointer(index=Index(byte=2, bit=0,
                                    address=2, base_address=0,
                                    update=False),
                        alignment=(4, 0),
                        bit_size=32,
                        value='0x0'))])


Metadata of a Pointer
----------------------

You can get the metadata of a `pointer`_ by calling the method
:meth:`~Pointer.describe`.

    >>> # Get the description of the pointer.
    >>> pointer.describe() # doctest: +NORMALIZE_WHITESPACE
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
                                               ('alignment', [2, 0]),
                                               ('class', 'Decimal16'),
                                               ('index', [0, 0]),
                                               ('max', 65535),
                                               ('min', 0),
                                               ('name', 'size'),
                                               ('order', 'auto'),
                                               ('signed', False),
                                               ('size', 16),
                                               ('type', 'Field'),
                                               ('value', 0)]),
                                  OrderedDict([('address', 2),
                                               ('alignment', [4, 0]),
                                               ('class', 'Pointer'),
                                               ('index', [2, 0]),
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
                                                              ('class', 'String'),
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

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # List the field indexes of the pointer and its attached data object.
    >>> pointer.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', Index(byte=0, bit=0,
                             address=0, base_address=0,
                             update=False)),
     ('Pointer.data.size', Index(byte=0, bit=0,
                                 address=0, base_address=0,
                                 update=False)),
     ('Pointer.data.item', Index(byte=0, bit=0,
                                 address=0, base_address=0,
                                 update=False))]
    >>> # List all field indexes of the pointer and its attached data objects.
    >>> pointer.to_list('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', Index(byte=0, bit=0,
                             address=0, base_address=0,
                             update=False)),
     ('Pointer.data.size', Index(byte=0, bit=0,
                                 address=0, base_address=0,
                                 update=False)),
     ('Pointer.data.item', Index(byte=0, bit=0,
                                 address=0, base_address=0,
                                 update=False)),
     ('Pointer.data.item.data', Index(byte=0, bit=0,
                                      address=0, base_address=0,
                                      update=False))]
    >>> # Index the pointer field.
    >>> pointer.index_field() # doctest: +NORMALIZE_WHITESPACE
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the pointer field with a start index.
    >>> pointer.index_field(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes of the pointer and its attached data object.
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes of the pointer and its attached data object.
    >>> pointer.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', Index(byte=0, bit=0,
                             address=0, base_address=0,
                             update=False)),
     ('Pointer.data.size', Index(byte=0, bit=0,
                                 address=0, base_address=0,
                                 update=False)),
     ('Pointer.data.item', Index(byte=0, bit=0,
                                 address=0, base_address=0,
                                 update=False))]


You can index the `pointer`_ field and each :ref:`field <field>` in the
`data object`_ referenced by the `pointer`_ field by calling the method
:meth:`~Pointer.index_fields`.
The :class:`Index` after the `pointer`_ field is returned.

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # List the field indexes of the pointer and its attached data object.
    >>> pointer.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', Index(byte=0, bit=0,
                             address=0, base_address=0,
                             update=False)),
     ('Pointer.data.size', Index(byte=0, bit=0,
                                 address=0, base_address=0,
                                 update=False)),
     ('Pointer.data.item', Index(byte=0, bit=0,
                                 address=0, base_address=0,
                                 update=False))]
    >>> # Index the pointer field and its attached data object.
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the pointer field and its attached data object with a start index.
    >>> pointer.index_fields(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the pointer field and all attached data objects.
    >>> pointer.index_fields(nested=True)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List all field indexes of the pointer and its attached data objects.
    >>> pointer.to_list('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', Index(byte=0, bit=0,
                             address=0, base_address=0,
                             update=False)),
     ('Pointer.data.size', Index(byte=0, bit=0,
                                 address=0, base_address=0,
                                 update=False)),
     ('Pointer.data.item', Index(byte=2, bit=0,
                                 address=2, base_address=0,
                                 update=False)),
     ('Pointer.data.item.data', Index(byte=0, bit=0,
                                      address=0, base_address=0,
                                      update=False))]



De-Serializing
--------------

You can **deserialize** the `pointer`_ field from a byte stream by calling the
method :meth:`~Pointer.deserialize`.



Serializing
-----------

You can **serialize** the `pointer`_ field to a byte stream by calling the
method :meth:`~Pointer.serialize`.


Attributes of a Pointer Field
-----------------------------

You can **access** the :ref:`field <field>` attributes of a `pointer`_ field
with the following attribute names:

    >>> # Field name.
    >>> pointer.name
    'Pointer32'
    >>> # Field value.
    >>> pointer.value
    '0x0'
    >>> # Field points to zero.
    >>> pointer.is_null()
    True
    >>> # Field bit size.
    >>> pointer.bit_size
    32
    >>> # Field alignment.
    >>> pointer.alignment
    (4, 0)
    >>> # Field alignment: byte size of the aligned field group.
    >>> pointer.alignment[0]
    4
    >>> # Field alignment: bit offset of the field in its field group.
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
    >>> # Field index: byte offset of the field in the byte stream.
    >>> pointer.index.byte
    0
    >>> # Field index: bit offset of the field relative to its byte offset.
    >>> pointer.index.bit
    0
    >>> # Field index: memory address of the field in the data source.
    >>> pointer.index.address
    0
    >>> # Field index: start address of the byte stream in the data source.
    >>> pointer.index.base_address
    0
    >>> # Field index: update request for the byte stream.
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


View Field Attributes
---------------------

You can view the **attributes** of a `pointer`_ field and of each :ref:`field
<field>` in the `data object`_ referenced by the `pointer`_ field as a
**nested** ordered dictionary by calling the method :meth:`~Pointer.view_fields`.

    >>> # View the field values of the pointer and its attached data object.
    >>> pointer.view_fields() # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('value', '0x0'),
                 ('data',
                  OrderedDict([('size', 0),
                               ('item', '0x0')]))])
    >>> # View all field values of the pointer and its attached data objects.
    >>> pointer.view_fields(nested=True) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('value', '0x0'),
                 ('data',
                  OrderedDict([('size', 0),
                               ('item',
                                OrderedDict([('value', '0x0'),
                                             ('data', '')]))]))])


List Field Items
----------------

You can list all :ref:`field <field>` items of a `pointer`_ as a **flat** list
by calling the method :meth:`~Pointer.field_items`.

    >>> # List the field items of the pointer and its attached data object.
    >>> pointer.field_items() # doctest: +NORMALIZE_WHITESPACE
    [('value',
      Pointer(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=(4, 0),
              bit_size=32,
              value='0x0')),
     ('data.size',
      Decimal(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=(2, 0),
              bit_size=16,
              value=0)),
     ('data.item',
      Pointer(index=Index(byte=2, bit=0, address=2, base_address=0, update=False),
              alignment=(4, 0),
              bit_size=32,
              value='0x0'))]
    >>> # List all field items of the pointer and its attached data objects.
    >>> pointer.field_items(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      Pointer(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=(4, 0),
              bit_size=32,
              value='0x0')),
     ('data.size',
      Decimal(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=(2, 0),
              bit_size=16,
              value=0)),
     ('data.item',
      Pointer(index=Index(byte=2, bit=0, address=2, base_address=0, update=False),
              alignment=(4, 0),
              bit_size=32,
              value='0x0')),
     ('data.item.data',
      String(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
             alignment=(0, 0),
             bit_size=0,
             value=''))]


List Field Values
-----------------

You can **list** the *values* of each :ref:`field <field>` of a `pointer`_ as a
**flat** list by calling the method :meth:`~Container.to_list`.

    >>> # List the field values of the pointer and its attached data object.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0')]
    >>> # List all field values of the pointer and its attached data objects.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]

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

    >>> # List all field values of the pointer and its attached data objects.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]
    >>> # Save all field values to an '.ini' file.
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

    >>> # Load all field values from an '.ini' file.
    >>> pointer.load("_static/pointer.ini", nested=True) # doctest: +NORMALIZE_WHITESPACE
    [Pointer]
    Pointer.value = 0x0
    Pointer.data.size = 0
    Pointer.data.item = 0x0
    Pointer.data.item.data =
    >>> # List all field values of the pointer and its attached data objects.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.
