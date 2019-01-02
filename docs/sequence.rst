.. currentmodule:: konfoo

.. testsetup:: *

    import json
    import sys
    from konfoo import *

.. _sequence:

Sequence
========

KonFoo has a :class:`Sequence` class to map a consecutive area of a *byte
stream* with different kind of :ref:`members <sequence member>`.
The order how you append the members to the `sequence`_ defines the order how
the members are deserialized and serialized by the built-in deserializer and
serializer.


.. _sequence member:

Member
------

A `sequence member`_ can be any :ref:`field <field>` or :ref:`container
<container>` class.


Create a Sequence
-----------------

You can **create** a `sequence`_ from a list of members.

    >>> # Create a sequence.
    >>> sequence = Sequence([
    ...     Byte(),
    ...     Unsigned8(),
    ...     Decimal8(),
    ...     Char()])
    >>> # List the field values of the sequence.
    >>> sequence.to_list() 
    [('Sequence[0]', '0x0'),
     ('Sequence[1]', '0x0'),
     ('Sequence[2]', 0),
     ('Sequence[3]', '\x00')]
    >>> # List the field values of the sequence as a CSV list.
    >>> sequence.to_csv()
    [{'id': 'Sequence[0]', 'value': '0x0'},
     {'id': 'Sequence[1]', 'value': '0x0'},
     {'id': 'Sequence[2]', 'value': 0},
     {'id': 'Sequence[3]', 'value': '\x00'}]
    >>> # View the sequence field values as a JSON string.
    >>> sequence.to_json()
    '["0x0", "0x0", 0, "\\u0000"]'


Append a Member
---------------

You can **append** a new member to the end of a `sequence`_.

    >>> # Create an empty sequence.
    >>> sequence = Sequence()
    >>> # Append a new member to the sequence.
    >>> sequence.append(Unsigned8())
    >>> # List the field values of the sequence.
    >>> sequence.to_list() 
    [('Sequence[0]', '0x0')]
    >>> # List the field values of the sequence as a CSV list.
    >>> sequence.to_csv()
    [{'id': 'Sequence[0]', 'value': '0x0'}]
    >>> # View the sequence field values as a JSON string.
    >>> sequence.to_json()
    '["0x0"]'


Insert a Member
---------------

You can **insert** a new member at a given position in a `sequence`_.

    >>> # Insert a new member to the sequence.
    >>> sequence.insert(0, Byte())
    >>> # List the field values of the sequence.
    >>> sequence.to_list() 
    [('Sequence[0]', '0x0'),
     ('Sequence[1]', '0x0')]
    >>> # List the field values of the sequence as a CSV list.
    >>> sequence.to_csv()
    [{'id': 'Sequence[0]', 'value': '0x0'},
     {'id': 'Sequence[1]', 'value': '0x0'}]
    >>> # View the sequence field values as a JSON string.
    >>> sequence.to_json()
    '["0x0", "0x0"]'


Extend a Sequence
-----------------

You can **extend** a `sequence`_ with a list of new members.

    >>> # Extend a sequence with a list of new members.
    >>> sequence.extend([Decimal8(), Char()])
    >>> # List the field values of the sequence.
    >>> sequence.to_list() 
    [('Sequence[0]', '0x0'),
     ('Sequence[1]', '0x0'),
     ('Sequence[2]', 0),
     ('Sequence[3]', '\x00')]
    >>> # List the field values of the sequence as a CSV list.
    >>> sequence.to_csv()
    [{'id': 'Sequence[0]', 'value': '0x0'},
     {'id': 'Sequence[1]', 'value': '0x0'},
     {'id': 'Sequence[2]', 'value': 0},
     {'id': 'Sequence[3]', 'value': '\x00'}]
    >>> # View the sequence field values as a JSON string.
    >>> sequence.to_json()
    '["0x0", "0x0", 0, "\\u0000"]'


Initialize a Sequence
----------------------

You can **initialize** the fields in a `sequence`_ by calling the method
:meth:`~Sequence.initialize_fields`.

    >>> # Create a sequence.
    >>> sequence = Sequence([
    ...     Byte(),
    ...     Unsigned8(),
    ...     Decimal8(),
    ...     Char()])
    >>> # List the field values of the sequence.
    >>> sequence.to_list() 
    [('Sequence[0]', '0x0'),
     ('Sequence[1]', '0x0'),
     ('Sequence[2]', 0),
     ('Sequence[3]', '\x00')]
    >>> # List the field values of the sequence as a CSV list.
    >>> sequence.to_csv()
    [{'id': 'Sequence[0]', 'value': '0x0'},
     {'id': 'Sequence[1]', 'value': '0x0'},
     {'id': 'Sequence[2]', 'value': 0},
     {'id': 'Sequence[3]', 'value': '\x00'}]
    >>> # View the sequence field values as a JSON string.
    >>> sequence.to_json()
    '["0x0", "0x0", 0, "\\u0000"]'

    >>> # Initialize the fields in the sequence.
    >>> sequence.initialize_fields([1, 2, 9, 0x46])
    >>> # List the field values of the sequence.
    >>> sequence.to_list()
    [('Sequence[0]', '0x1'),
     ('Sequence[1]', '0x2'),
     ('Sequence[2]', 9),
     ('Sequence[3]', 'F')]
    >>> # List the field values of the sequence as a CSV list.
    >>> sequence.to_csv()
    [{'id': 'Sequence[0]', 'value': '0x1'},
     {'id': 'Sequence[1]', 'value': '0x2'},
     {'id': 'Sequence[2]', 'value': 9},
     {'id': 'Sequence[3]', 'value': 'F'}]
    >>> # View the sequence field values as a JSON string.
    >>> sequence.to_json()
    '["0x1", "0x2", 9, "F"]'


Display a Sequence
------------------

You can **display** the `sequence`_.

    >>> # Create a sequence.
    >>> sequence = Sequence([
    ...     Byte(),
    ...     Unsigned8(),
    ...     Decimal8(),
    ...     Char()])
    >>> # Index the fields in the sequence.
    >>> sequence.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Display the sequence.
    >>> sequence
    [Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=Alignment(byte_size=1, bit_offset=0),
          bit_size=8,
          value='0x0'),
     Unsigned8(index=Index(byte=1, bit=0, address=1, base_address=0, update=False),
               alignment=Alignment(byte_size=1, bit_offset=0),
               bit_size=8,
               value='0x0'),
     Decimal8(index=Index(byte=2, bit=0, address=2, base_address=0, update=False),
              alignment=Alignment(byte_size=1, bit_offset=0),
              bit_size=8,
              value=0),
     Char(index=Index(byte=3, bit=0, address=3, base_address=0, update=False),
          alignment=Alignment(byte_size=1, bit_offset=0),
          bit_size=8,
          value='\x00')]


Metadata of a Sequence
----------------------

You can get the metadata of the `sequence`_ by calling the method
:meth:`~Sequence.describe`.

    >>> # Get the description of the sequence.
    >>> sequence.describe()
    OrderedDict([('class', 'Sequence'),
                 ('name', 'Sequence'),
                 ('size', 4),
                 ('type', 'Sequence'),
                 ('member',
                  [OrderedDict([('address', 0),
                                ('alignment', [1, 0]),
                                ('class', 'Byte'),
                                ('index', [0, 0]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'Sequence[0]'),
                                ('order', 'auto'),
                                ('signed', False),
                                ('size', 8),
                                ('type', 'Field'),
                                ('value', '0x0')]),
                  OrderedDict([('address', 1),
                                ('alignment', [1, 0]),
                                ('class', 'Unsigned8'),
                                ('index', [1, 0]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'Sequence[1]'),
                                ('order', 'auto'),
                                ('signed', False),
                                ('size', 8),
                                ('type', 'Field'),
                                ('value', '0x0')]),
                   OrderedDict([('address', 2),
                                ('alignment', [1, 0]),
                                ('class', 'Decimal8'),
                                ('index', [2, 0]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'Sequence[2]'),
                                ('order', 'auto'),
                                ('signed', False),
                                ('size', 8),
                                ('type', 'Field'),
                                ('value', 0)]),
                   OrderedDict([('address', 3),
                                ('alignment', [1, 0]),
                                ('class', 'Char'),
                                ('index', [3, 0]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'Sequence[3]'),
                                ('order', 'auto'),
                                ('signed', False),
                                ('size', 8),
                                ('type', 'Field'),
                                ('value', '\x00')])])])

    >>> json.dump(sequence.describe(), sys.stdout, indent=2)
    {
      "class": "Sequence",
      "name": "Sequence",
      "size": 4,
      "type": "Sequence",
      "member": [
        {
          "address": 0,
          "alignment": [
            1,
            0
          ],
          "class": "Byte",
          "index": [
            0,
            0
          ],
          "max": 255,
          "min": 0,
          "name": "Sequence[0]",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": "0x0"
        },
        {
          "address": 1,
          "alignment": [
            1,
            0
          ],
          "class": "Unsigned8",
          "index": [
            1,
            0
          ],
          "max": 255,
          "min": 0,
          "name": "Sequence[1]",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": "0x0"
        },
        {
          "address": 2,
          "alignment": [
            1,
            0
          ],
          "class": "Decimal8",
          "index": [
            2,
            0
          ],
          "max": 255,
          "min": 0,
          "name": "Sequence[2]",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": 0
        },
        {
          "address": 3,
          "alignment": [
            1,
            0
          ],
          "class": "Char",
          "index": [
            3,
            0
          ],
          "max": 255,
          "min": 0,
          "name": "Sequence[3]",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": "\u0000"
        }
      ]
    }


Size of a Sequence
------------------

You can get the **size** of a `sequence`_ as a tuple in the form of
``(number of bytes, number of remaining bits)`` by calling the method
:meth:`~Sequence.container_size`.

    >>> # Get the size of the sequence.
    >>> sequence.container_size()
    (4, 0)

.. note::
    The number of remaining bits must be always zero or the `sequence`_
    declaration is incomplete.


Indexing
--------

You can index all fields in a `sequence`_ by calling the method
:meth:`~Sequence.index_fields`.
The :class:`Index` after the last :ref:`field <field>` of the `sequence`_ is
returned.

    >>> # Create a sequence.
    >>> sequence = Sequence([
    ...     Byte(),
    ...     Unsigned8(),
    ...     Decimal8(),
    ...     Char()])
    >>> # List the field indexes of the sequence.
    >>> sequence.to_list('index')
    [('Sequence[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Sequence[1]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Sequence[2]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Sequence[3]', Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # List the field indexes of the sequence as a CSV list.
    >>> sequence.to_csv('index.byte', 'index.address')
    [{'id': 'Sequence[0]', 'index.byte': 0, 'index.address': 0},
     {'id': 'Sequence[1]', 'index.byte': 0, 'index.address': 0},
     {'id': 'Sequence[2]', 'index.byte': 0, 'index.address': 0},
     {'id': 'Sequence[3]', 'index.byte': 0, 'index.address': 0}]
    >>> # View the sequence field indexes as a JSON string.
    >>> sequence.to_json('index')
    '[[0, 0, 0, 0, false],
      [0, 0, 0, 0, false],
      [0, 0, 0, 0, false],
      [0, 0, 0, 0, false]]'

    >>> # Index the fields in the sequence.
    >>> sequence.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the fields in the sequence with a start index.
    >>> sequence.index_fields(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes of the sequence.
    >>> sequence.to_list('index')
    [('Sequence[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Sequence[1]', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
     ('Sequence[2]', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Sequence[3]', Index(byte=3, bit=0, address=3, base_address=0, update=False))]
    >>> # List the field indexes of the sequence as a CSV list.
    >>> sequence.to_csv('index.byte', 'index.address')
    [{'id': 'Sequence[0]', 'index.byte': 0, 'index.address': 0},
     {'id': 'Sequence[1]', 'index.byte': 1, 'index.address': 1},
     {'id': 'Sequence[2]', 'index.byte': 2, 'index.address': 2},
     {'id': 'Sequence[3]', 'index.byte': 3, 'index.address': 3}]
    >>> # View the sequence field indexes as a JSON string.
    >>> sequence.to_json('index')
    '[[0, 0, 0, 0, false],
      [1, 0, 1, 0, false],
      [2, 0, 2, 0, false],
      [3, 0, 3, 0, false]]'


De-Serializing
--------------

You can **deserialize** a byte stream with a `sequence`_ by calling the method
:meth:`~Sequence.deserialize`.

    >>> # Create a sequence.
    >>> sequence = Sequence([
    ...     Byte(),
    ...     Unsigned8(),
    ...     Decimal8(),
    ...     Char()])
    >>> # Create a byte stream to be deserialized.
    >>> bytestream = bytes.fromhex('01020946f00f00')
    >>> # Deserialize the byte stream and map it to the sequence.
    >>> sequence.deserialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field values of the sequence.
    >>> sequence.to_list()
    [('Sequence[0]', '0x1'),
     ('Sequence[1]', '0x2'),
     ('Sequence[2]', 9),
     ('Sequence[3]', 'F')]
    >>> # List the field values of the sequence as a CSV list.
    >>> sequence.to_csv()
    [{'id': 'Sequence[0]', 'value': '0x1'},
     {'id': 'Sequence[1]', 'value': '0x2'},
     {'id': 'Sequence[2]', 'value': 9},
     {'id': 'Sequence[3]', 'value': 'F'}]
    >>> # View the sequence field values as a JSON string.
    >>> sequence.to_json()
    '["0x1", "0x2", 9, "F"]'


Serializing
-----------

You can **serialize** a byte stream with a `sequence`_ by calling the method
:meth:`~Sequence.serialize`.

    >>> # Create an empty byte stream.
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> # Serialize the sequence to the byte stream.
    >>> sequence.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # View the byte stream.
    >>> bytestream.hex()
    '01020946'

or

    >>> bytes(sequence).hex()
    '01020946'


Number of Members
-----------------

You can **get** the number of `sequence`_ members with the built-in function
:func:`len`.

    >>> # Number of sequence members.
    >>> len(sequence)
    4


Access a Member
---------------

You can **access** a `sequence member`_ by its index.

    >>> # Access a sequence member by its index.
    >>> sequence[0]
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=Alignment(byte_size=1, bit_offset=0),
         bit_size=8,
         value='0x1')


Attributes of a Member Field
----------------------------

You can **access** the :class:`Field` attributes of a :ref:`field <field>`
member of a `sequence`_ with the attribute names:

    >>> # Field name.
    >>> sequence[0].name
    'Byte'
    >>> # Field value.
    >>> sequence[0].value
    '0x1'
    >>> # Field bit size.
    >>> sequence[0].bit_size
    8
    >>> # Field alignment.
    >>> sequence[0].alignment
    Alignment(byte_size=1, bit_offset=0)
    >>> # Field alignment: byte size of the aligned field group.
    >>> sequence[0].alignment.byte_size
    1
    >>> # Field alignment: bit offset of the field in its field group.
    >>> sequence[0].alignment.bit_offset
    0
    >>> # Field byte order.
    >>> sequence[0].byte_order
    Byteorder.auto = 'auto'
    >>> # Field byte order value.
    >>> sequence[0].byte_order.value
    'auto'
    >>> # Field index.
    >>> sequence[0].index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> # Field index: byte offset of the field in the byte stream.
    >>> sequence[0].index.byte
    0
    >>> # Field index: bit offset of the field relative to its byte offset.
    >>> sequence[0].index.bit
    0
    >>> # Field index: memory address of the field in the data source.
    >>> sequence[0].index.address
    0
    >>> # Field index: start address of the byte stream in the data source.
    >>> sequence[0].index.base_address
    0
    >>> # Field index: update request for the byte stream.
    >>> sequence[0].index.update
    False


You can **check** if a `sequence member`_ is a :ref:`field <field>`.

    >>> is_field(sequence[0])
    True


You can **check** what kind of :ref:`field <field>` it is.

    >>> # Field is a bit field.
    >>> sequence[0].is_bit()
    False
    >>> # Field is a boolean field.
    >>> sequence[0].is_bool()
    False
    >>> # Field is a decimal field.
    >>> sequence[0].is_decimal()
    True
    >>> # Field is a float field.
    >>> sequence[0].is_float()
    False
    >>> # Field is a pointer field.
    >>> sequence[0].is_pointer()
    False
    >>> # Field is a stream field.
    >>> sequence[0].is_stream()
    False
    >>> # Field is a string field.
    >>> sequence[0].is_string()
    False


Iterate over Members
--------------------

You can **iterate** over all kind of members of a `sequence`_.

    >>> [member.item_type for member in sequence]
    [ItemClass.Byte = 42,
     ItemClass.Unsigned = 45,
     ItemClass.Decimal = 40,
     ItemClass.Char = 43]


You can **iterate** over all :ref:`field <field>` members of a `sequence`_.

    >>> [member.name for member in sequence if is_field(member)]
    ['Byte', 'Unsigned8', 'Decimal8', 'Char']


View Field Attributes
---------------------

You can **view** the *attributes* of each :ref:`field <field>` of a `sequence`_
as a list by calling the method :meth:`~Sequence.view_fields`.
Default attribute is the field :attr:`~Field.value`.

    >>> # View the sequence field values.
    >>> sequence.view_fields()
    ['0x1', '0x2', 9, 'F']
    >>> # View the sequence field type name & field values.
    >>> sequence.view_fields('name', 'value')
    [{'name': 'Byte', 'value': '0x1'},
     {'name': 'Unsigned8', 'value': '0x2'},
     {'name': 'Decimal8', 'value': 9},
     {'name': 'Char', 'value': 'F'}]
    >>> # View the sequence field indexes.
    >>> sequence.view_fields('index')
    [Index(byte=0, bit=0, address=0, base_address=0, update=False),
     Index(byte=1, bit=0, address=1, base_address=0, update=False),
     Index(byte=2, bit=0, address=2, base_address=0, update=False),
     Index(byte=3, bit=0, address=3, base_address=0, update=False)]

.. note::
    The *attributes* of each :ref:`field <field>` for containers *nested* in the
    `sequence`_ are viewed as well (chained method call).


View as a JSON string
---------------------

You can view the *attributes* of each :ref:`field <field>` of a `sequence`_
as a **JSON** formatted string by calling the method :meth:`~Container.to_json`.
Default attribute is the field :attr:`~Field.value`.

    >>> # View the sequence field values as a JSON string.
    >>> sequence.to_json()
    '["0x1", "0x2", 9, "F"]'
    >>> print(sequence.to_json(indent=2))
    [
      "0x1",
      "0x2",
      9,
      "F"
    ]
    >>> # View the sequence field type names & field values as a JSON string.
    >>> sequence.to_json('name', 'value')
    '[{"name": "Byte", "value": "0x1"},
      {"name": "Unsigned8", "value": "0x2"},
      {"name": "Decimal8", "value": 9},
      {"name": "Char", "value": "F"}]'
    >>> # View the sequence field indexes as a JSON string.
    >>> sequence.to_json('index') 
    '[[0, 0, 0, 0, false],
      [1, 0, 1, 0, false],
      [2, 0, 2, 0, false],
      [3, 0, 3, 0, false]]'

.. note::
    The *attributes* of each :ref:`field <field>` for containers *nested* in the
    `sequence`_ are viewed as well (chained method call).


List Field Items
----------------

You can list all :ref:`field <field>` items of a `sequence`_
as a **flatten** list by calling the method :meth:`~Sequence.field_items`.

    >>> # List the field items of the sequence.
    >>> sequence.field_items()
    [('[0]', Byte(index=Index(byte=0, bit=0,
                              address=0, base_address=0,
                              update=False),
                  alignment=Alignment(byte_size=1, bit_offset=0),
                  bit_size=8,
                  value='0x1')),
     ('[1]', Unsigned8(index=Index(byte=1, bit=0,
                                   address=1, base_address=0,
                                   update=False),
                       alignment=Alignment(byte_size=1, bit_offset=0),
                       bit_size=8,
                       value='0x2')),
     ('[2]', Decimal8(index=Index(byte=2, bit=0,
                                  address=2, base_address=0,
                                  update=False),
                      alignment=Alignment(byte_size=1, bit_offset=0),
                       bit_size=8,
                       value=9)),
     ('[3]', Char(index=Index(byte=3, bit=0,
                              address=3, base_address=0,
                              update=False),
                  alignment=Alignment(byte_size=1, bit_offset=0),
                  bit_size=8,
                  value='F'))]


List Field Attributes
---------------------

You can **list** the *attributes* of each :ref:`field <field>` of a `sequence`_
as a **flatten** list by calling the method :meth:`~Container.to_list`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the sequence.
    >>> sequence.to_list()
    [('Sequence[0]', '0x1'),
     ('Sequence[1]', '0x2'),
     ('Sequence[2]', 9),
     ('Sequence[3]', 'F')]
    >>> # List the field type names & field values of the sequence.
    >>> sequence.to_list('name', 'value')
    [('Sequence[0]', ('Byte', '0x1')),
     ('Sequence[1]', ('Unsigned8', '0x2')),
     ('Sequence[2]', ('Decimal8', 9)),
     ('Sequence[3]', ('Char', 'F'))]
    >>> # List the field indexes of the sequence.
    >>> sequence.to_list('index')
    [('Sequence[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Sequence[1]', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
     ('Sequence[2]', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Sequence[3]', Index(byte=3, bit=0, address=3, base_address=0, update=False))]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **list** the *attributes* of each :ref:`field <field>` of a `sequence`_
as a **flatten** ordered dictionary by calling the method :meth:`~Container.to_dict`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the sequence.
    >>> sequence.to_dict()
    OrderedDict([('Sequence',
                  OrderedDict([('[0]', '0x1'),
                               ('[1]', '0x2'),
                               ('[2]', 9),
                               ('[3]', 'F')]))])
    >>> # List the field type names & field values of the sequence.
    >>> sequence.to_dict('name', 'value')
    OrderedDict([('Sequence',
                  OrderedDict([('[0]', ('Byte', '0x1')),
                               ('[1]', ('Unsigned8', '0x2')),
                               ('[2]', ('Decimal8', 9)),
                               ('[3]', ('Char', 'F'))]))])
    >>> # List the field indexes of the sequence.
    >>> sequence.to_dict('index')
    OrderedDict([('Sequence',
                  OrderedDict([('[0]', Index(byte=0, bit=0,
                                             address=0, base_address=0,
                                             update=False)),
                               ('[1]', Index(byte=1, bit=0,
                                             address=1, base_address=0,
                                             update=False)),
                               ('[2]', Index(byte=2, bit=0,
                                             address=2, base_address=0,
                                             update=False)),
                               ('[3]', Index(byte=3, bit=0,
                                             address=3, base_address=0,
                                             update=False))]))])

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **list** the *attributes* of each :ref:`field <field>` of a `sequence`_
as a **flatten** list of dictionaries containing the field *path* and the selected
field *attributes* by calling the method :meth:`~Container.to_csv`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the sequence as a CSV list.
    >>> sequence.to_csv()
    [{'id': 'Sequence[0]', 'value': '0x1'},
     {'id': 'Sequence[1]', 'value': '0x2'},
     {'id': 'Sequence[2]', 'value': 9},
     {'id': 'Sequence[3]', 'value': 'F'}]
    >>> # List the field type names & values of the sequence as a CSV list.
    >>> sequence.to_csv('name', 'value')
    [{'id': 'Sequence[0]', 'name': 'Byte', 'value': '0x1'},
     {'id': 'Sequence[1]', 'name': 'Unsigned8', 'value': '0x2'},
     {'id': 'Sequence[2]', 'name': 'Decimal8', 'value': 9},
     {'id': 'Sequence[3]', 'name': 'Char', 'value': 'F'}]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Write Field Attributes
----------------------

You can **write** the *attributes* of each :ref:`field <field>` of a `sequence`_
to a ``.csv`` file by calling the method :meth:`~Container.write_csv`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the sequence as a CSV list.
    >>> sequence.to_csv()
    [{'id': 'Sequence[0]', 'value': '0x1'},
     {'id': 'Sequence[1]', 'value': '0x2'},
     {'id': 'Sequence[2]', 'value': 9},
     {'id': 'Sequence[3]', 'value': 'F'}]
    >>> # Save the structure field values to a '.csv' file.
    >>> sequence.write_csv("_static/sequence.csv")

The generated ``.csv`` file for the structure looks like this:

.. literalinclude:: _static/sequence.csv

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Save Field Attributes
---------------------

You can **save** the *attributes* of each :ref:`field <field>` of a `sequence`_
to an ``.ini`` file by calling the method :meth:`~Container.save`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the sequence.
    >>> sequence.to_list()
    [('Sequence[0]', '0x1'),
     ('Sequence[1]', '0x2'),
     ('Sequence[2]', 9),
     ('Sequence[3]', 'F')]
    >>> # Save the field values to an '.ini' file.
    >>> sequence.save("_static/sequence.ini", nested=True)

The generated ``.ini`` file for the sequence looks like this:

.. literalinclude:: _static/sequence.ini
    :language: ini

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.


Load Field Values
-----------------

You can **load** the *value* of each :ref:`field <field>` of a `sequence`_
from an ``.ini`` file by calling the method :meth:`~Container.load`.

    >>> # Create a sequence.
    >>> sequence = Sequence([
    ...     Byte(),
    ...     Unsigned8(),
    ...     Decimal8(),
    ...     Char()])
    >>> # Load the sequence field values from an '.ini' file.
    >>> sequence.load("_static/sequence.ini")
    [Sequence]
    Sequence[0] = 0x1
    Sequence[1] = 0x2
    Sequence[2] = 9
    Sequence[3] = F
    >>> # List the field values of the sequence.
    >>> sequence.to_list()
    [('Sequence[0]', '0x1'),
     ('Sequence[1]', '0x2'),
     ('Sequence[2]', 9),
     ('Sequence[3]', 'F')]

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.
