.. currentmodule:: konfoo

.. testsetup:: *

    import json
    from binascii import hexlify
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
    >>> # List the field type names & field values in the sequence.
    >>> sequence.to_list('name', 'value')  # doctest: +NORMALIZE_WHITESPACE
    [('Sequence[0]', ('Byte', '0x0')),
     ('Sequence[1]', ('Unsigned8', '0x0')),
     ('Sequence[2]', ('Decimal8', 0)),
     ('Sequence[3]', ('Char', '\x00'))]


Number of Sequence Members
--------------------------

You can **get** the number of sequence members in the `sequence`_ with the build-in
function :func:`len`.

    >>> # Create a sequence.
    >>> sequence = Sequence([
    ...     Byte(),
    ...     Unsigned8(),
    ...     Decimal8(),
    ...     Char()])
    >>> # Number of the sequence members in the sequence.
    >>> len(sequence)
    4


Append a Member
---------------

You can **append** a new member to the end of a `sequence`_.

    >>> # Create an empty sequence.
    >>> sequence = Sequence()
    >>> # Append a new member to the sequence.
    >>> sequence.append(Unsigned8())
    >>> # List the field type names & field values in the sequence.
    >>> sequence.to_list('name', 'value')  # doctest: +NORMALIZE_WHITESPACE
    [('Sequence[0]', ('Unsigned8', '0x0'))]


Insert a Member
---------------

You can **insert** a new member at a given position in a `sequence`_.

    >>> # Insert a new member to the sequence.
    >>> sequence.insert(0, Byte())
    >>> # List the field type names & field values in the sequence.
    >>> sequence.to_list('name', 'value')  # doctest: +NORMALIZE_WHITESPACE
    [('Sequence[0]', ('Byte', '0x0')),
     ('Sequence[1]', ('Unsigned8', '0x0'))]


Extend a Sequence
-----------------

You can **extend** a `sequence`_ with a list of new members.

    >>> # Extend a sequence with a list of new members.
    >>> sequence.extend([Decimal8(), Char()])
    >>> # List the field type names & field values in the sequence.
    >>> sequence.to_list('name', 'value')  # doctest: +NORMALIZE_WHITESPACE
    [('Sequence[0]', ('Byte', '0x0')),
     ('Sequence[1]', ('Unsigned8', '0x0')),
     ('Sequence[2]', ('Decimal8', 0)),
     ('Sequence[3]', ('Char', '\x00'))]

View a Sequence
---------------

You can **view** the `sequence`_

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
    >>> sequence # doctest: +NORMALIZE_WHITESPACE
    [Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0'),
     Unsigned8(index=Index(byte=1, bit=0, address=1, base_address=0, update=False),
               alignment=(1, 0),
               bit_size=8,
               value='0x0'),
     Decimal8(index=Index(byte=2, bit=0, address=2, base_address=0, update=False),
              alignment=(1, 0),
              bit_size=8,
              value=0),
     Char(index=Index(byte=3, bit=0, address=3, base_address=0, update=False),
          alignment=(1, 0),
          bit_size=8,
          value='\x00')]


Metadata of a Sequence
----------------------

You can get the metadata of the `sequence`_ by calling the method
:meth:`~Sequence.describe`.

    >>> # Get the description of the sequence.
    >>> sequence.describe() # doctest: +NORMALIZE_WHITESPACE
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
    >>> # List the field indexes in the sequence.
    >>> sequence.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Sequence[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Sequence[1]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Sequence[2]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Sequence[3]', Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # Index the fields in the sequence.
    >>> sequence.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the fields in the sequence with a start index.
    >>> sequence.index_fields(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes in the sequence.
    >>> sequence.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Sequence[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Sequence[1]', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
     ('Sequence[2]', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Sequence[3]', Index(byte=3, bit=0, address=3, base_address=0, update=False))]


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
    >>> # List the field values in the sequence.
    >>> sequence.to_list('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    [('Sequence[0]', ('Byte', '0x1')),
     ('Sequence[1]', ('Unsigned8', '0x2')),
     ('Sequence[2]', ('Decimal8', 9)),
     ('Sequence[3]', ('Char', 'F'))]


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
    >>> hexlify(bytestream)
    b'01020946'

or

    >>> hexlify(bytes(sequence))
    b'01020946'

Access a Member
---------------

You can **access** a member in a `sequence`_ by its index.

    >>> # Access a sequence member with its index.
    >>> sequence[0] # doctest: +NORMALIZE_WHITESPACE
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=(1, 0),
         bit_size=8,
         value='0x1')


Attributes of a Member Field
----------------------------

You can **access** the :class:`Field` attributes of a :ref:`field <field>`
member in a `sequence`_ with the attribute names:

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
    (1, 0)
    >>> # Field alignment: byte size of the aligned field group.
    >>> sequence[0].alignment[0]
    1
    >>> # Field alignment: bit offset of the field in its field group.
    >>> sequence[0].alignment[1]
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

    >>> [member.item_type for member in sequence] # doctest: +NORMALIZE_WHITESPACE
    [ItemClass.Byte = 42,
     ItemClass.Unsigned = 45,
     ItemClass.Decimal = 40,
     ItemClass.Char = 43]


You can **iterate** over all :ref:`field <field>` members of a `sequence`_.

    >>> [member.name for member in sequence if is_field(member)]
    ['Byte', 'Unsigned8', 'Decimal8', 'Char']


View Field Attributes
---------------------

You can view the **attributes** of each :ref:`field <field>` in a `sequence`_
as a **nested** list by calling the method :meth:`~Sequence.view_fields`.

    >>> # View the field values.
    >>> sequence.view_fields() # doctest: +NORMALIZE_WHITESPACE
    ['0x1', '0x2', 9, 'F']
    >>> # View the field type name, field value pairs.
    >>> sequence.view_fields('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    [('Byte', '0x1'),
     ('Unsigned8', '0x2'),
     ('Decimal8', 9),
     ('Char', 'F')]
    >>> # View the field indexes.
    >>> sequence.view_fields('index') # doctest: +NORMALIZE_WHITESPACE
    [Index(byte=0, bit=0, address=0, base_address=0, update=False),
     Index(byte=1, bit=0, address=1, base_address=0, update=False),
     Index(byte=2, bit=0, address=2, base_address=0, update=False),
     Index(byte=3, bit=0, address=3, base_address=0, update=False)]


List Field Items
----------------

You can list all :ref:`field <field>` items in a `sequence`_
as a **flat** list by calling the method :meth:`~Sequence.field_items`.

    >>> # List the field items in the sequence.
    >>> sequence.field_items() # doctest: +NORMALIZE_WHITESPACE
    [('[0]', Byte(index=Index(byte=0, bit=0,
                              address=0, base_address=0,
                              update=False),
                  alignment=(1, 0),
                  bit_size=8,
                  value='0x1')),
     ('[1]', Unsigned8(index=Index(byte=1, bit=0,
                                   address=1, base_address=0,
                                   update=False),
                       alignment=(1, 0),
                       bit_size=8,
                       value='0x2')),
     ('[2]', Decimal8(index=Index(byte=2, bit=0,
                                  address=2, base_address=0,
                                  update=False),
                      alignment=(1, 0),
                       bit_size=8,
                       value=9)),
     ('[3]', Char(index=Index(byte=3, bit=0,
                              address=3, base_address=0,
                              update=False),
                  alignment=(1, 0),
                  bit_size=8,
                  value='F'))]


View Field Values
-----------------

You can **view** the *value* of each :ref:`field <field>` in a `sequence`_
as a **flat** list by calling the method :meth:`~Container.to_list`.

    >>> # List the field values in the sequence.
    >>> sequence.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Sequence[0]', '0x1'),
     ('Sequence[1]', '0x2'),
     ('Sequence[2]', 9),
     ('Sequence[3]', 'F')]
    >>> # List the field type names & field values in the sequence.
    >>> sequence.to_list('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    [('Sequence[0]', ('Byte', '0x1')),
     ('Sequence[1]', ('Unsigned8', '0x2')),
     ('Sequence[2]', ('Decimal8', 9)),
     ('Sequence[3]', ('Char', 'F'))]
    >>> # List the field indexes in the sequence.
    >>> sequence.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Sequence[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Sequence[1]', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
     ('Sequence[2]', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Sequence[3]', Index(byte=3, bit=0, address=3, base_address=0, update=False))]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *value* of each :ref:`field <field>` in a `sequence`_
as a **flat** ordered dictionary by calling the method
:meth:`~Container.to_dict`.

    >>> # List the field values in the sequence.
    >>> sequence.to_dict() # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Sequence',
                  OrderedDict([('[0]', '0x1'),
                               ('[1]', '0x2'),
                               ('[2]', 9),
                               ('[3]', 'F')]))])
    >>> print(json.dumps(sequence.to_dict(), indent=2)) # doctest: +NORMALIZE_WHITESPACE
    {
      "Sequence": {
        "[0]": "0x1",
        "[1]": "0x2",
        "[2]": 9,
        "[3]": "F"
      }
    }
    >>> # List the field type names & field values in the sequence.
    >>> sequence.to_dict('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Sequence',
                  OrderedDict([('[0]', ('Byte', '0x1')),
                               ('[1]', ('Unsigned8', '0x2')),
                               ('[2]', ('Decimal8', 9)),
                               ('[3]', ('Char', 'F'))]))])
    >>> # List the field indexes in the sequence.
    >>> sequence.to_dict('index') # doctest: +NORMALIZE_WHITESPACE
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


Save Field Values
-----------------

You can **save** the *value* of each :ref:`field <field>` in a `sequence`_
to an ``.ini`` file by calling the method :meth:`~Container.save`.

    >>> # List the field values in the sequence.
    >>> sequence.to_list() # doctest: +NORMALIZE_WHITESPACE
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

You can **load** the *value* of each :ref:`field <field>` in a `sequence`_
from an ``.ini`` file by calling the method :meth:`~Container.load`.

    >>> # Create a sequence.
    >>> sequence = Sequence([
    ...     Byte(),
    ...     Unsigned8(),
    ...     Decimal8(),
    ...     Char()])
    >>> # Load the field values from an '.ini' file.
    >>> sequence.load("_static/sequence.ini", nested=True)
    [Sequence]
    Sequence[0] = 0x1
    Sequence[1] = 0x2
    Sequence[2] = 9
    Sequence[3] = F
    >>> # List the field values in the sequence.
    >>> sequence.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Sequence[0]', '0x1'),
     ('Sequence[1]', '0x2'),
     ('Sequence[2]', 9),
     ('Sequence[3]', 'F')]

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.
