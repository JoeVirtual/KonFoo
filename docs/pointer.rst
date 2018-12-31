.. currentmodule:: konfoo

.. testsetup:: *

    import json
    import sys
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

Data Object
-----------

A `data object`_ of a `pointer`_ field can be any :ref:`field <field>` or
:ref:`container <container>` class.


Define a Data Object
--------------------

Define a `data object`_ by defining an *data object* class.

    >>> class DataObject(Structure):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.size = Decimal(16)
    ...         self.item = Pointer()
    ...         self.index_fields()
    >>> # Create an instance of the data object.
    >>> data_object = DataObject()
    >>> # List the field values of the data object.
    >>> data_object.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('DataObject.size', 0),
     ('DataObject.item', '0x0')]
    >>> # List the field values of the data object as a CSV list.
    >>> data_object.to_csv() # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'DataObject.size', 'value': 0},
     {'id': 'DataObject.item', 'value': '0x0'}]
    >>> # View the data object field values as a JSON string.
    >>> data_object.to_json() # doctest: +NORMALIZE_WHITESPACE
    '{"size": 0, "item": "0x0"}'
    >>> # List the field values of the data object and nested pointers.
    >>> data_object.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('DataObject.size', 0),
     ('DataObject.item', '0x0')]
    >>> # List the field values of the data object and nested pointers as a CSV list.
    >>> data_object.to_csv(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'DataObject.size', 'value': 0},
     {'id': 'DataObject.item', 'value': '0x0'}]
    >>> # View the data object and nested pointers field values as a JSON string.
    >>> data_object.to_json(nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"size": 0,
      "item": {"value": "0x0",
               "data": null}}'


.. _data object pointer:

Define a Data Object Pointer
----------------------------

Define a `data object pointer`_ class for the `data object`_ attached to the
`pointer`_.

    >>> class DataObjectPointer(Pointer):
    ...
    ...     def __init__(self, address=None, byte_order=BYTEORDER):
    ...         super().__init__(template=DataObject(),
    ...                          address=address,
    ...                          data_order=byte_order)
    >>> # Create an instance of the pointer.
    >>> pointer = DataObjectPointer()
    >>> # List the field values of the pointer.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('DataObjectPointer.field', '0x0'),
     ('DataObjectPointer.data.size', 0),
     ('DataObjectPointer.data.item', '0x0')]
    >>> # List the field values of the pointer as a CSV list.
    >>> pointer.to_csv() # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'DataObjectPointer.field', 'value': '0x0'},
     {'id': 'DataObjectPointer.data.size', 'value': 0},
     {'id': 'DataObjectPointer.data.item', 'value': '0x0'}]
    >>> # View the pointer field values as a JSON string.
    >>> pointer.to_json() # doctest: +NORMALIZE_WHITESPACE
    '{"value": "0x0",
      "data": {"size": 0,
               "item": "0x0"}}'
    >>> # List the field values of the pointer and nested pointers.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('DataObjectPointer.field', '0x0'),
     ('DataObjectPointer.data.size', 0),
     ('DataObjectPointer.data.item', '0x0')]
    >>> # List the field values of the pointer and nested pointers as a CSV list.
    >>> pointer.to_csv(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'DataObjectPointer.field', 'value': '0x0'},
     {'id': 'DataObjectPointer.data.size', 'value': 0},
     {'id': 'DataObjectPointer.data.item', 'value': '0x0'}]
    >>> # View the pointer and nested pointers field values as a JSON string.
    >>> pointer.to_json(nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"value": "0x0",
      "data": {"size": 0,
               "item": {"value": "0x0",
                        "data": null}}}'


Nest Pointers
-------------

You can *nest* `pointer`_.

    >>> # Create an nested pointer with no data object attached.
    >>> pointer = Pointer(Pointer())
    >>> # List the field values of the pointer.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x0'),
     ('Pointer.data', '0x0')]
    >>> # List the field values of the pointer as a CSV list.
    >>> pointer.to_csv() # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'Pointer.field', 'value': '0x0'},
     {'id': 'Pointer.data', 'value': '0x0'}]
    >>> # View the pointer field values as a JSON string.
    >>> pointer.to_json() # doctest: +NORMALIZE_WHITESPACE
    '{"value": "0x0",
      "data": "0x0"}'
    >>> # List the field values of the pointer and nested pointers.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x0'),
     ('Pointer.data', '0x0')]
    >>> # List the field values of the pointer and nested pointers as a CSV list.
    >>> pointer.to_csv(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'Pointer.field', 'value': '0x0'},
     {'id': 'Pointer.data', 'value': '0x0'}]
    >>> # View the pointer and nested pointers field values as a JSON string.
    >>> pointer.to_json(nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"value": "0x0",
      "data": {"value": "0x0",
               "data": null}}'

    >>> # Create an nested pointer with a data object attached.
    >>> pointer = Pointer(Pointer(Byte()))
    >>> # List the field values of the pointer.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x0'),
     ('Pointer.data', '0x0')]
    >>> # List the field values of the pointer as a CSV list.
    >>> pointer.to_csv() # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'Pointer.field', 'value': '0x0'},
     {'id': 'Pointer.data', 'value': '0x0'}]
    >>> # View the pointer field values as a JSON string.
    >>> pointer.to_json() # doctest: +NORMALIZE_WHITESPACE
    '{"value": "0x0",
      "data": "0x0"}'
    >>> # List the field values of the pointer and nested pointers.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x0'),
     ('Pointer.data', '0x0'),
     ('Pointer.data.data', '0x0')]
    >>> # List the field values of the pointer and nested pointers as a CSV list.
    >>> pointer.to_csv(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'Pointer.field', 'value': '0x0'},
     {'id': 'Pointer.data', 'value': '0x0'},
     {'id': 'Pointer.data.data', 'value': '0x0'}]
    >>> # View the pointer and nested pointers field values as a JSON string.
    >>> pointer.to_json(nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"value": "0x0",
      "data": {"value": "0x0",
               "data": "0x0"}}'


Access the Data Object
----------------------

You can **access** the `data object`_ referenced by a `pointer`_ with the
:attr:`~Pointer.data` attribute of a `pointer`_ field.

    >>> # Create a nested pointer.
    >>> pointer = Pointer(Pointer(Byte()))
    >>> # Index the pointer field and the fields of the attached data object.
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Access the data object referenced the pointer field.
    >>> pointer.data  # doctest: +NORMALIZE_WHITESPACE
    Pointer(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
            alignment=Alignment(byte_size=4, bit_offset=0),
            bit_size=32,
            value='0x0')
    >>> # Access the data object referenced a nested pointer field.
    >>> pointer.data.data  # doctest: +NORMALIZE_WHITESPACE
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=Alignment(byte_size=1, bit_offset=0),
         bit_size=8,
         value='0x0')


You can **check** if a `data object`_ is a :ref:`field <field>`.

    >>> is_field(pointer.data)
    True


You can **check** what kind of :ref:`field <field>` it is.

    >>> # Field is a bit field.
    >>> pointer.data.is_bit()
    False
    >>> # Field is a boolean field.
    >>> pointer.data.is_bool()
    False
    >>> # Field is a decimal field.
    >>> pointer.data.is_decimal()
    True
    >>> # Field is a float field.
    >>> pointer.data.is_float()
    False
    >>> # Field is a pointer field.
    >>> pointer.data.is_pointer()
    True
    >>> # Field is a stream field.
    >>> pointer.data.is_stream()
    False
    >>> # Field is a string field.
    >>> pointer.data.is_string()
    False


Address of the Data Object
--------------------------

You can get the *data source* **address** of the `data object`_ referenced by the
`pointer`_ with the :attr:`~Pointer.address` attribute of a `pointer`_ field.

    >>> # Data source address of the data object referenced by the pointer.
    >>> pointer.address
    0


Byte Order of the Data Object
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


Byte Stream for the Data Object
-------------------------------

You can get the internal **byte stream** used by the `pointer`_ to deserialize or
serialize its referenced `data object`_ with the :attr:`~Pointer.bytestream`
attribute of a `pointer`_ field.

    >>> # Get the internal byte stream of the pointer.
    >>> pointer.bytestream
    ''

You can set the internal **byte stream** used by the `pointer`_ to deserialize or
serialize its referenced `data object`_ with the :attr:`~Pointer.bytestream`
attribute of a `pointer`_ field.

    >>> # Set the internal byte stream of the pointer.
    >>> pointer.bytestream = '000000000000'
    >>> pointer.bytestream
    '000000000000'


Declare on the fly
------------------

You can **declare** a `data object`_ on the fly.

    >>> # Create a data object.
    >>> data_object = Structure(
    ...     size = Decimal(16),
    ...     item = Pointer(String()))
    >>> # List the field values of the data object.
    >>> data_object.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', 0),
     ('Structure.item', '0x0')]
    >>> # List the field values of the data object as a CSV list.
    >>> data_object.to_csv() # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'Structure.size', 'value': 0},
     {'id': 'Structure.item', 'value': '0x0'}]
    >>> # View the data object field values as a JSON string.
    >>> data_object.to_json() # doctest: +NORMALIZE_WHITESPACE
    '{"size": 0, "item": "0x0"}'
    >>> # List the field values of the data object and nested pointers.
    >>> data_object.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', 0),
     ('Structure.item', '0x0'),
     ('Structure.item.data', '')]
    >>> # List the field values of the data object and nested pointers as a CSV list.
    >>> data_object.to_csv(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'Structure.size', 'value': 0},
     {'id': 'Structure.item', 'value': '0x0'},
     {'id': 'Structure.item.data', 'value': ''}]
    >>> # View the data object and nested pointers field values as a JSON string.
    >>> data_object.to_json(nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"size": 0,
      "item": {"value": "0x0",
               "data": ""}}'

You can **declare** a `pointer`_ on the fly.

    >>> # Create a pointer for the data object.
    >>> pointer = Pointer(data_object)
    >>> # List the field values of the pointer.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0')]
    >>> # List the field values of the pointer as a CSV list.
    >>> pointer.to_csv() # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'Pointer.field', 'value': '0x0'},
     {'id': 'Pointer.data.size', 'value': 0},
     {'id': 'Pointer.data.item', 'value': '0x0'}]
    >>> # View the pointer field values as a JSON string.
    >>> pointer.to_json() # doctest: +NORMALIZE_WHITESPACE
    '{"value": "0x0",
      "data": {"size": 0,
               "item": "0x0"}}'
    >>> # List all field values of the pointer and nested pointers.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]
    >>> # List the field values of the pointer and nested pointers as a CSV list.
    >>> pointer.to_csv(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'Pointer.field', 'value': '0x0'},
     {'id': 'Pointer.data.size', 'value': 0},
     {'id': 'Pointer.data.item', 'value': '0x0'},
     {'id': 'Pointer.data.item.data', 'value': ''}]
    >>> # View the pointer and nested pointers field values as a JSON string.
    >>> pointer.to_json(nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"value": "0x0",
      "data": {"size": 0,
               "item": {"value": "0x0",
                        "data": ""}}}'


Initialize a Pointer
--------------------

You can **initialize** the fields in a `pointer`_ by calling the method
:meth:`~Pointer.initialize_fields`.

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String(14))))
    >>> # List the field values of the pointer and nested pointers.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]
    >>> # List the field values of the pointer and nested pointers as a CSV list.
    >>> pointer.to_csv(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'Pointer.field', 'value': '0x0'},
     {'id': 'Pointer.data.size', 'value': 0},
     {'id': 'Pointer.data.item', 'value': '0x0'},
     {'id': 'Pointer.data.item.data', 'value': ''}]
    >>> # View the pointer and nested pointers field values as a JSON string.
    >>> pointer.to_json(nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"value": "0x0",
      "data": {"size": 0,
               "item": {"value": "0x0",
                        "data": ""}}}'

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
    >>> # List the field values of the pointer and nested pointers.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x1'),
     ('Pointer.data.size', 14),
     ('Pointer.data.item', '0x10'),
     ('Pointer.data.item.data', 'Konfoo is Fun')]
    >>> # List the field values of the pointer and nested pointers as a CSV list.
    >>> pointer.to_csv(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [{'id': 'Pointer.field', 'value': '0x1'},
     {'id': 'Pointer.data.size', 'value': 14},
     {'id': 'Pointer.data.item', 'value': '0x10'},
     {'id': 'Pointer.data.item.data', 'value': 'Konfoo is Fun'}]
    >>> # View the pointer and nested pointers field values as a JSON string.
    >>> pointer.to_json(nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"value": "0x1",
      "data": {"size": 14,
               "item": {"value": "0x10",
                        "data": "Konfoo is Fun"}}}'


Display a Pointer
-----------------

You can **display** a `pointer`_ field.

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
            alignment=Alignment(byte_size=4, bit_offset=0),
            bit_size=32,
            value='0x0')


Display the Data Object
-----------------------

You can **display** the `data object`_ of a `pointer`_ field.

    >>> # Display the data object referenced by the pointer
    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    Structure([('size',
                Decimal(index=Index(byte=0, bit=0,
                                    address=0, base_address=0,
                                    update=False),
                        alignment=Alignment(byte_size=2, bit_offset=0),
                        bit_size=16,
                        value=0)),
               ('item',
                Pointer(index=Index(byte=2, bit=0,
                                    address=2, base_address=0,
                                    update=False),
                        alignment=Alignment(byte_size=4, bit_offset=0),
                        bit_size=32,
                        value='0x0'))])

Metadata of a Pointer
---------------------

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

    >>> json.dump(pointer.describe(), sys.stdout, indent=2)
    {
      "address": 0,
      "alignment": [
        4,
        0
      ],
      "class": "Pointer",
      "index": [
        0,
        0
      ],
      "max": 4294967295,
      "min": 0,
      "name": "Pointer",
      "order": "auto",
      "signed": false,
      "size": 32,
      "type": "Pointer",
      "value": "0x0",
      "member": [
        {
          "class": "Structure",
          "name": "data",
          "size": 2,
          "type": "Structure",
          "member": [
            {
              "address": 0,
              "alignment": [
                2,
                0
              ],
              "class": "Decimal16",
              "index": [
                0,
                0
              ],
              "max": 65535,
              "min": 0,
              "name": "size",
              "order": "auto",
              "signed": false,
              "size": 16,
              "type": "Field",
              "value": 0
            },
            {
              "address": 2,
              "alignment": [
                4,
                0
              ],
              "class": "Pointer",
              "index": [
                2,
                0
              ],
              "max": 4294967295,
              "min": 0,
              "name": "item",
              "order": "auto",
              "signed": false,
              "size": 32,
              "type": "Pointer",
              "value": "0x0",
              "member": [
                {
                  "address": 0,
                  "alignment": [
                    0,
                    0
                  ],
                  "class": "String",
                  "index": [
                    0,
                    0
                  ],
                  "name": "data",
                  "order": "auto",
                  "size": 0,
                  "type": "Field",
                  "value": ""
                }
              ]
            }
          ]
        }
      ]
    }


Size of the Data Object
-----------------------

You can get the byte **size** of the `data object`_ referenced by the `pointer`_
with the :attr:`~Pointer.data_size` attribute of a `pointer`_ field.

    >>> # Byte size of the data object referenced by the pointer.
    >>> pointer.data_size
    6


Indexing
--------

You can index the `pointer`_ field and each :ref:`field <field>` in the `data object`_
referenced by the `pointer`_ field by calling the method :meth:`~Pointer.index_fields`.
The :class:`Index` after the `pointer`_ field is returned.

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # List the field indexes of the pointer and the nested pointers.
    >>> pointer.to_list('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.size',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.item',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.item.data',
     Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # View the pointer and the nested pointers field indexes as a JSON string.
    >>> pointer.data.to_json('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"size": [0, 0, 0, 0, false],
      "item": {"value": [0, 0, 0, 0, false],
               "data": [0, 0, 0, 0, false]}}'

    >>> # Index the pointer field and its attached data object fields.
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the pointer field and its attached data object fields with a start index.
    >>> pointer.index_fields(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes of the pointer and the nested pointers.
    >>> pointer.to_list('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
     [('Pointer.field',
      Index(byte=0, bit=0, address=0, base_address=0, update=False)),
      ('Pointer.data.size',
      Index(byte=0, bit=0, address=0, base_address=0, update=False)),
      ('Pointer.data.item',
      Index(byte=2, bit=0, address=2, base_address=0, update=False)),
      ('Pointer.data.item.data',
      Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # View the pointer and the nested pointers field indexes as a JSON string.
    >>> pointer.data.to_json('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"size": [0, 0, 0, 0, false],
      "item": {"value": [2, 0, 2, 0, false],
               "data": [0, 0, 0, 0, false]}}'

    >>> # Index the pointer field and the fields of the nested pointers.
    >>> pointer.index_fields(nested=True)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the pointer field and the fields of the nested pointers with a start index.
    >>> pointer.index_fields(index=Index(), nested=True)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes of the pointer and the nested pointers.
    >>> pointer.to_list('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.size',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.item',
     Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Pointer.data.item.data',
     Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # View the pointer and the nested pointers field indexes as a JSON string.
    >>> pointer.data.to_json('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"size": [0, 0, 0, 0, false],
      "item": {"value": [2, 0, 2, 0, false],
               "data": [0, 0, 0, 0, false]}}'

Index the Pointer Field
-----------------------

You can index the `pointer`_ field by calling the method :meth:`~Field.index_field`.
The :class:`Index` after the `pointer`_ field is returned.

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # List the field indexes of the pointer and the nested pointers.
    >>> pointer.to_list('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.size',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.item',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.item.data',
     Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # View the pointer and the nested pointers field indexes as a JSON string.
    >>> pointer.data.to_json('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"size": [0, 0, 0, 0, false],
      "item": {"value": [0, 0, 0, 0, false],
               "data": [0, 0, 0, 0, false]}}'

    >>> # Index the pointer field.
    >>> pointer.index_field() # doctest: +NORMALIZE_WHITESPACE
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the pointer field with a start index.
    >>> pointer.index_field(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes of the pointer and the nested pointers.
    >>> pointer.to_list('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.size',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.item',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.item.data',
     Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # View the pointer and the nested pointers field indexes as a JSON string.
    >>> pointer.data.to_json('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"size": [0, 0, 0, 0, false],
      "item": {"value": [0, 0, 0, 0, false],
               "data": [0, 0, 0, 0, false]}}'

Index the Data Object
---------------------

You can index each :ref:`field <field>` in the `data object`_ referenced by the
`pointer`_ field by calling the method :meth:`~Pointer.index_data`

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # List the field indexes of the data object and the nested pointers.
    >>> pointer.data.to_list('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.item',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.item.data',
     Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # View the data object and the nested pointers field indexes as a JSON string.
    >>> pointer.data.to_json('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"size": [0, 0, 0, 0, false],
      "item": {"value": [0, 0, 0, 0, false],
               "data": [0, 0, 0, 0, false]}}'

    >>> # Indexes the data object referenced by the pointer.
    >>> pointer.index_data()
    >>> # List the field indexes of the data object and the nested pointers.
    >>> pointer.data.to_list('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size',
     Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.item',
     Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Structure.item.data',
     Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # View the data object and the nested pointers field indexes as a JSON string.
    >>> pointer.data.to_json('index', nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"size": [0, 0, 0, 0, false],
      "item": {"value": [2, 0, 2, 0, false],
               "data": [0, 0, 0, 0, false]}}'



Reading
-------

You can **read** the *byte stream* used by the `pointer`_ to deserialize its
referenced `data object`_ **from** a *data source* through a data
:ref:`provider <provider>` by calling the method :meth:`~Pointer.read_from` of
a `pointer`_ field.


De-Serializing
--------------

You can **deserialize** the `pointer`_ field from a byte stream by calling the
method :meth:`~Pointer.deserialize`.


Deserialize the Data Object
---------------------------

You can **deserialize** the `data object`_ referenced by the `pointer`_ by calling
the method :meth:`~Pointer.deserialize_data` of a `pointer`_ field.

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # List the field values of the data object referenced by the pointer.
    >>> pointer.data.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', 0),
     ('Structure.item', '0x0')]
    >>> # View the data object field values as a JSON string.
    >>> pointer.data.to_json() # doctest: +NORMALIZE_WHITESPACE
    '{"size": 0, "item": "0x0"}'
    >>> # Internal byte stream of the pointer.
    >>> pointer.bytestream
    ''
    >>> # Deserialize the data object with an external byte stream.
    >>> pointer.deserialize_data(bytes.fromhex('0e0010000000'))
    Index(byte=6, bit=0, address=6, base_address=0, update=False)
    >>> # Set the internal byte stream of the pointer.
    >>> pointer.bytestream = '0e0010000000'
    >>> # Deserialize the data object with the internal byte stream of the pointer.
    >>> pointer.deserialize_data()
    Index(byte=6, bit=0, address=6, base_address=0, update=False)
    >>> # List the field values of the data object referenced by the pointer.
    >>> pointer.data.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', 14),
     ('Structure.item', '0x10')]
    >>> # View the data object field values as a JSON string.
    >>> pointer.data.to_json() # doctest: +NORMALIZE_WHITESPACE
    '{"size": 14, "item": "0x10"}'


Serializing
-----------

You can **serialize** the `pointer`_ field to a byte stream by calling the
method :meth:`~Pointer.serialize`.


Serialize the Data Object
-------------------------

You can **serialize** the `data object`_ referenced by the `pointer`_ by calling
the method :meth:`~Pointer.serialize_data` of a `pointer`_ field.

    >>> # Create a pointer.
    >>> pointer = Pointer(
    ...     Structure(
    ...         size=Decimal(16),
    ...         item=Pointer(String())))
    >>> # List the field values of the data object referenced by the pointer.
    >>> pointer.data.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.size', 0),
     ('Structure.item', '0x0')]
    >>> # View the data object field values as a JSON string.
    >>> pointer.data.to_json() # doctest: +NORMALIZE_WHITESPACE
    '{"size": 0, "item": "0x0"}'
    >>> # Serialize the data object referenced by the pointer.
    >>> pointer.serialize_data()
    b'\x00\x00\x00\x00\x00\x00'


Writing
-------



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
    >>> # Field bit size.
    >>> pointer.bit_size
    32
    >>> # Field alignment.
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> # Field alignment: byte size of the aligned field group.
    >>> pointer.alignment.byte_size
    4
    >>> # Field alignment: bit offset of the field in its field group.
    >>> pointer.alignment.bit_offset
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


You can **check** if a `pointer`_ is a ``Null``-pointer.

    >>> # Field points to zero.
    >>> pointer.is_null()
    True


View Field Attributes
---------------------

You can **view** the *attributes* of a `pointer`_ field and of each :ref:`field <field>`
of the `data object`_ referenced by the `pointer`_ field as an ordered dictionary
by calling the method :meth:`~Pointer.view_fields`.
Default attribute is the field :attr:`~Field.value`.

    >>> # View the pointer field values.
    >>> pointer.view_fields() # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('value', '0x0'),
                 ('data',
                  OrderedDict([('size', 0),
                               ('item', '0x0')]))])
    >>> # View the pointer and nested pointers field values.
    >>> pointer.view_fields(nested=True) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('value', '0x0'),
                 ('data',
                  OrderedDict([('size', 0),
                               ('item',
                                OrderedDict([('value', '0x0'),
                                             ('data', '')]))]))])
    >>> # View the pointer field type names & field values.
    >>> pointer.view_fields('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('name', 'Pointer32'),
                 ('value', '0x0'),
                 ('data',
                  OrderedDict([('size', {'name': 'Decimal16',
                                         'value': 0}),
                               ('item', {'name': 'Pointer32',
                                         'value': '0x0'})]))])
    >>> # View the pointer field indexes.
    >>> pointer.view_fields('index') # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('value',
                  Index(byte=0, bit=0, address=0, base_address=0, update=False)),
                 ('data',
                  OrderedDict([('size',
                                Index(byte=0, bit=0, address=0, base_address=0, update=False)),
                               ('item',
                                Index(byte=2, bit=0, address=2, base_address=0, update=False))]))])


View as a JSON string
---------------------

You can view the *attributes* of a `pointer`_ field and of each :ref:`field <field>`
of the `data object`_ referenced by the `pointer`_ field as a **JSON** formatted
string by calling the method :meth:`~Container.to_json`.
Default attribute is the field :attr:`~Field.value`.

    >>> # View the pointer field values as a JSON string.
    >>> pointer.to_json()
    '{"value": "0x0", "data": {"size": 0, "item": "0x0"}}'
    >>> print(pointer.to_json(indent=2)) # doctest: +NORMALIZE_WHITESPACE
    {
      "value": "0x0",
      "data": {
        "size": 0,
        "item": "0x0"
      }
    }
    >>> # View the pointer and nested pointers field values as a JSON string.
    >>> pointer.to_json(nested=True) # doctest: +NORMALIZE_WHITESPACE
    '{"value": "0x0",
      "data": {"size": 0,
               "item": {"value": "0x0",
                        "data": ""}}}'
    >>> # View the pointer field type names & field values as a JSON string.
    >>> pointer.to_json('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    '{"name": "Pointer32",
      "value": "0x0",
      "data": {"size": {"name": "Decimal16",
                        "value": 0},
               "item": {"name": "Pointer32",
                        "value": "0x0"}}}'
    >>> # View the pointer field indexes as a JSON string.
    >>> pointer.to_json('index')  # doctest: +NORMALIZE_WHITESPACE
    '{"value": [0, 0, 0, 0, false],
      "data": {"size": [0, 0, 0, 0, false],
               "item": [2, 0, 2, 0, false]}}'


List Field Items
----------------

You can list all :ref:`field <field>` items of a `pointer`_
as a **flatten** list by calling the method :meth:`~Pointer.field_items`.

    >>> # List the field items of the pointer.
    >>> pointer.field_items() # doctest: +NORMALIZE_WHITESPACE
    [('field',
      Pointer(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=Alignment(byte_size=4, bit_offset=0),
              bit_size=32,
              value='0x0')),
     ('data.size',
      Decimal(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=Alignment(byte_size=2, bit_offset=0),
              bit_size=16,
              value=0)),
     ('data.item',
      Pointer(index=Index(byte=2, bit=0, address=2, base_address=0, update=False),
              alignment=Alignment(byte_size=4, bit_offset=0),
              bit_size=32,
              value='0x0'))]

    >>> # List the field items of the pointer and the nested pointers.
    >>> pointer.field_items(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('field',
      Pointer(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=Alignment(byte_size=4, bit_offset=0),
              bit_size=32,
              value='0x0')),
     ('data.size',
      Decimal(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=Alignment(byte_size=2, bit_offset=0),
              bit_size=16,
              value=0)),
     ('data.item',
      Pointer(index=Index(byte=2, bit=0, address=2, base_address=0, update=False),
              alignment=Alignment(byte_size=4, bit_offset=0),
              bit_size=32,
              value='0x0')),
     ('data.item.data',
      String(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
             alignment=Alignment(byte_size=0, bit_offset=0),
             bit_size=0,
             value=''))]


List Field Attributes
---------------------

You can **list** the *attributes* of each :ref:`field <field>` of a `pointer`_
as a **flatten** list by calling the method :meth:`~Container.to_list`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the pointer and its attached data object.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0')]
    >>> # List the field values of the pointer and the nested pointers.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]
    >>> # List the field type names & values of the pointer and its attached data object.
    >>> pointer.to_list('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', ('Pointer32', '0x0')),
     ('Pointer.data.size', ('Decimal16', 0)),
     ('Pointer.data.item', ('Pointer32', '0x0'))]
    >>> # List the field indexes of the pointer and its attached data object.
    >>> pointer.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field',
      Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.size',
      Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Pointer.data.item',
      Index(byte=2, bit=0, address=2, base_address=0, update=False))]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **list** the *attributes* of each :ref:`field <field>` of a `pointer`_
as a **flatten** ordered dictionary by calling the method :meth:`~Container.to_dict`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the pointer and its attached data object.
    >>> pointer.to_dict() # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Pointer',
        OrderedDict([('field', '0x0'),
                     ('data.size', 0),
                     ('data.item', '0x0')]))])
    >>> # List the field values of the pointer and the nested pointers.
    >>> pointer.to_dict(nested=True) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Pointer',
        OrderedDict([('field', '0x0'),
                     ('data.size', 0),
                     ('data.item', '0x0'),
                     ('data.item.data', '')]))])
    >>> # List the field type names & values of the pointer and its attached data object.
    >>> pointer.to_dict('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Pointer',
        OrderedDict([('field', ('Pointer32', '0x0')),
                     ('data.size', ('Decimal16', 0)),
                     ('data.item', ('Pointer32', '0x0'))]))])
    >>> # List the field indexes of the pointer and its attached data object.
    >>> pointer.to_dict('index') # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Pointer',
        OrderedDict([('field',
                      Index(byte=0, bit=0, address=0, base_address=0, update=False)),
                     ('data.size',
                      Index(byte=0, bit=0, address=0, base_address=0, update=False)),
                     ('data.item',
                      Index(byte=2, bit=0, address=2, base_address=0, update=False))]))])

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Save Field Attributes
---------------------

You can **save** the *attributes* of each :ref:`field <field>` of a `pointer`_
to an ``.ini`` file by calling the method :meth:`~Container.save`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the pointer and the nested pointers.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]
    >>> # Save the pointer and the nested pointers field values to an '.ini' file.
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

    >>> # Load the pointer and the nested pointers field values from an '.ini' file.
    >>> pointer.load("_static/pointer.ini", nested=True) # doctest: +NORMALIZE_WHITESPACE
    [Pointer]
    Pointer.field = 0x0
    Pointer.data.size = 0
    Pointer.data.item = 0x0
    Pointer.data.item.data =
    >>> # List the field values of the pointer and the nested pointers.
    >>> pointer.to_list(nested=True) # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.field', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', '')]

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.
