.. currentmodule:: konfoo

.. testsetup:: *

    import json
    from binascii import hexlify
    from konfoo import *

.. _structure:

Structure
=========

KonFoo has a :class:`Structure` class and many :ref:`field <field>` classes to
declare the mapping part of a *byte stream* :ref:`mapper <mapper>`.
The order how you declare the :ref:`members <structure member>` in the
`structure`_ defines the order how the :ref:`members <structure member>` are
deserialized and serialized by the built-in deserializer and serializer.


.. _structure member:

Member
------

A `structure member`_ can be any :ref:`field <field>` or :ref:`container
<container>` class.


Define a Structure
------------------

You can define members of a `structure`_ by adding them in the
constructor method of the :class:`Structure` class.

.. code-block:: python

    class Identifier(Structure):

        def __init__(self):
            super().__init__()        # <- NEVER forget to call it first!
            self.version = Byte()     # 1st field
            self.id = Unsigned8()     # 2nd field
            self.length = Decimal8()  # 3rd field
            self.module = Char()      # 4th field
            self.index_fields()       # <- Indexes all fields (optional)

.. warning::
    A `structure`_ must always align to full bytes or an exception will be
    raised when an incomplete `structure`_ declaration is deserialized or
    serialized.


Align Fields in a Structure
---------------------------

You can :ref:`align <field alignment>` consecutive fields in a `structure`_ to
each other by using the ``align_to`` parameter of the :class:`Field` class.

.. code-block:: python
    :emphasize-lines: 5-8

    class Identifier(Structure):

        def __init__(self):
            super().__init__()
            self.version = Byte(4)       # 1st field aligned to 4 bytes
            self.id = Unsigned(8, 4)     # 2nd field aligned to 4 bytes
            self.length = Decimal(8, 4)  # 3rd field aligned to 4 bytes
            self.module = Char(4)        # 4th field aligned to 4 bytes
            self.index_fields()

.. note::
    The field :ref:`alignment <field alignment>` works only for the
    :class:`Decimal` :ref:`field <field>` classes.


Nest a Structure
----------------

You can **nest** a `structure`_ in another `structure`_.

    >>> # Define a new structure class.
    >>> class Identifier(Structure):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.version = Byte()
    ...         self.id = Unsigned8()
    ...         self.length = Decimal8()
    ...         self.module = Char()
    ...         self.index_fields()
    >>> # Create an instance.
    >>> identifier = Identifier()
    >>> # List the field values in the structure.
    >>> identifier.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Identifier.version', '0x0'),
     ('Identifier.id', '0x0'),
     ('Identifier.length', 0),
     ('Identifier.module', '\x00')]
    >>> # Define a new structure class with a nested structure.
    >>> class Header(Structure):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.type = Identifier()  # nested structure
    ...         self.size = Decimal32()
    ...         self.index_fields()
    >>> # Create an instance.
    >>> header = Header()
    >>> # List the field values in the structure.
    >>> header.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Header.type.version', '0x0'),
     ('Header.type.id', '0x0'),
     ('Header.type.length', 0),
     ('Header.type.module', '\x00'),
     ('Header.size', 0)]


Inherit from a Structure
------------------------

You can **inherit** the members from a `structure`_ class to extend or change it.

    >>> # Define a new structure class.
    >>> class HeaderV1(Structure):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.type = Decimal32()
    ...         self.index_fields()
    >>> # Create an instance.
    >>> header = HeaderV1()
    >>> # List the field values in the structure.
    >>> header.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('HeaderV1.type', 0)]
    >>> # Define a new structure class inherit from a structure the fields.
    >>> class HeaderV2(HeaderV1):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.size = Decimal32()
    ...         self.index_fields()
    >>> # Create an instance.
    >>> header = HeaderV2()
    >>> # List the field values in the structure.
    >>> header.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('HeaderV2.type', 0),
     ('HeaderV2.size', 0)]


Declare on the fly
------------------

You can **declare** a `structure`_ on the fly.

    >>> # Create an empty structure.
    >>> structure = Structure()
    >>> # Add fields to the structure.
    >>> structure.version = Byte()
    >>> structure.id = Unsigned8()
    >>> structure.length = Decimal8()
    >>> structure.module = Char()
    >>> # Index the fields in the structure.
    >>> structure.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field values in the structure.
    >>> structure.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', '0x0'),
     ('Structure.id', '0x0'),
     ('Structure.length', 0),
     ('Structure.module', '\x00')]


You can **declare** a `structure`_ with :ref:`aligned <field alignment>` fields on
the fly.

    >>> # Create an empty structure.
    >>> structure = Structure()
    >>> # Add aligned fields to the structure.
    >>> structure.version = Byte(4)
    >>> structure.id = Unsigned(8, 4)
    >>> structure.length = Decimal(8, 4)
    >>> structure.module = Char(4)
    >>> # Index the fields in the structure.
    >>> structure.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes in the structure.
    >>> structure.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.id', Index(byte=0, bit=8, address=0, base_address=0, update=False)),
     ('Structure.length', Index(byte=0, bit=16, address=0, base_address=0, update=False)),
     ('Structure.module', Index(byte=0, bit=24, address=0, base_address=0, update=False))]

You can **declare** a `structure`_ with keywords.

    >>> # Create a structure with keywords.
    >>> structure = Structure(
    ...     version=Byte(),
    ...     id=Unsigned8(),
    ...     length=Decimal8(),
    ...     module=Char())
    >>> # Index the fields in the structure.
    >>> structure.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field values in the structure.
    >>> structure.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', '0x0'),
     ('Structure.id', '0x0'),
     ('Structure.length', 0),
     ('Structure.module', '\x00')]

You can **nest** `structure`_'s on the fly.

    >>> # Create an empty structure.
    >>> structure = Structure()
    >>> # Add an empty nested structure to the structure.
    >>> structure.type = Structure()
    >>> # Add fields to the nested structure.
    >>> structure.type.version = Byte()
    >>> structure.type.id = Unsigned8()
    >>> structure.type.length = Decimal8()
    >>> structure.type.module = Char()
    >>> # Add a field to the structure.
    >>> structure.size = Decimal32()
    >>> # Indexes the fields in the structure.
    >>> structure.index_fields()
    Index(byte=8, bit=0, address=8, base_address=0, update=False)
    >>> # Lists the field values in the structure.
    >>> structure.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.type.version', '0x0'),
     ('Structure.type.id', '0x0'),
     ('Structure.type.length', 0),
     ('Structure.type.module', '\x00'),
     ('Structure.size', 0)]


You can **assign** a `structure`_ to a member of another `structure`_ on the fly.

    >>> # Create a structure to be nested.
    >>> nested = Structure(
    ...     version = Byte(4),
    ...     id = Unsigned(8, 4),
    ...     length = Decimal(8, 4),
    ...     module = Char(4))
    >>> # Create an empty structure.
    >>> structure = Structure()
    >>> # Assign the nested structure to the structure.
    >>> structure.type = nested
    >>> # Add a field to the structure.
    >>> structure.size = Decimal32()
    >>> # Lists the field values in the structure.
    >>> structure.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.type.version', '0x0'),
     ('Structure.type.id', '0x0'),
     ('Structure.type.length', 0),
     ('Structure.type.module', '\x00'),
     ('Structure.size', 0)]


View a Structure
----------------

You can **view** the `structure`_

    >>> # Create a structure.
    >>> structure = Structure(
    ...     version=Byte(),
    ...     id=Unsigned8(),
    ...     length=Decimal8(),
    ...     module=Char())
    >>> # Index the fields in the structure.
    >>> structure.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Display the structure.
    >>> structure # doctest: +NORMALIZE_WHITESPACE
    Structure([('version', Byte(index=Index(byte=0, bit=0,
                                            address=0, base_address=0,
                                            update=False),
                                alignment=(1, 0),
                                bit_size=8,
                                value='0x0')),
                ('id', Unsigned8(index=Index(byte=1, bit=0,
                                             address=1, base_address=0,
                                             update=False),
                                alignment=(1, 0),
                                bit_size=8,
                                value='0x0')),
                ('length', Decimal8(index=Index(byte=2, bit=0,
                                                address=2, base_address=0,
                                                update=False),
                                   alignment=(1, 0),
                                   bit_size=8,
                                   value=0)),
                ('module', Char(index=Index(byte=3, bit=0,
                                            address=3, base_address=0,
                                            update=False),
                                alignment=(1, 0),
                                bit_size=8,
                                value='\x00'))])

Metadata of a Structure
-----------------------

You can get the metadata of the `structure`_ by calling the method
:meth:`~Structure.describe`.

    >>> # Get the description of the structure.
    >>> structure.describe() # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('class', 'Structure'),
                 ('name', 'Structure'),
                 ('size', 4),
                 ('type', 'Structure'),
                 ('member',
                  [OrderedDict([('address', 0),
                                ('alignment', [1, 0]),
                                ('class', 'Byte'),
                                ('index', [0, 0]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'version'),
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
                                ('name', 'id'),
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
                                ('name', 'length'),
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
                                ('name', 'module'),
                                ('order', 'auto'),
                                ('signed', False),
                                ('size', 8),
                                ('type', 'Field'),
                                ('value', '\x00')])])])


Size of a Structure
-------------------

You can get the **size** of a `structure`_ as a tuple in the form of
``(number of bytes, number of remaining bits)`` by calling the method
:meth:`~Structure.container_size`.

    >>> # Get the size of the structure.
    >>> structure.container_size()
    (4, 0)

.. note::
    The number of remaining bits must be always zero or the `structure`_
    declaration is incomplete.


Indexing
--------

You can index all fields in a `structure`_ by calling the method
:meth:`~Structure.index_fields`.
The :class:`Index` after the last :ref:`field <field>` of the `structure`_ is
returned.

    >>> # Create a structure.
    >>> structure = Structure(
    ...     version=Byte(),
    ...     id=Unsigned8(),
    ...     length=Decimal8(),
    ...     module=Char())
    >>> # List the field indexes of the structure.
    >>> structure.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.id', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.length', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.module', Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # Index the fields in the structure.
    >>> structure.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the fields in the structure with a start index.
    >>> structure.index_fields(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes in the structure.
    >>> structure.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
    ('Structure.id', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
    ('Structure.length', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
    ('Structure.module', Index(byte=3, bit=0, address=3, base_address=0, update=False))]

De-Serializing
--------------

You can **deserialize** a byte stream with a `structure`_ by calling the method
:meth:`~Structure.deserialize`.

    >>> # Create a structure.
    >>> structure = Structure(
    ...     version=Byte(),
    ...     id=Unsigned8(),
    ...     length=Decimal8(),
    ...     module=Char())
    >>> # Create a byte stream to be deserialized.
    >>> bytestream = bytes.fromhex('01020946f00f00')
    >>> # Deserialize the byte stream and map it to the structure.
    >>> structure.deserialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field values in the structure.
    >>> structure.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]

Serializing
-----------

You can **serialize** a byte stream with a `structure`_ by calling the method
:meth:`~Structure.serialize`.

    >>> # Create an empty byte stream.
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> # Serialize the structure to the byte stream.
    >>> structure.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Display the byte stream.
    >>> hexlify(bytestream)
    b'01020946'

or

    >>> hexlify(bytes(structure))
    b'01020946'


Access a Member
---------------

You can **access** a member in a `structure`_ with its name.

    >>> # Access a structure member with its attribute name.
    >>> structure.version # doctest: +NORMALIZE_WHITESPACE
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=(1, 0),
         bit_size=8,
         value='0x1')
    >>> # Access a structure member with its key name.
    >>> structure['version'] # doctest: +NORMALIZE_WHITESPACE
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=(1, 0),
         bit_size=8,
         value='0x1')


Attributes of a Member Field
----------------------------

You can **access** the :class:`Field` attributes of a :ref:`field <field>`
member in a `structure`_ with the attribute names:

    >>> # Field name.
    >>> structure.version.name
    'Byte'
    >>> # Field value.
    >>> structure.version.value
    '0x1'
    >>> # Field bit size.
    >>> structure.version.bit_size
    8
    >>> # Field alignment.
    >>> structure.version.alignment
    (1, 0)
    >>> # Field alignment: byte size of the aligned field group.
    >>> structure.version.alignment[0]
    1
    >>> # Field alignment: bit offset of the field in its field group.
    >>> structure.version.alignment[1]
    0
    >>> # Field byte order.
    >>> structure.version.byte_order
    Byteorder.auto = 'auto'
    >>> # Field byte order value.
    >>> structure.version.byte_order.value
    'auto'
    >>> # Field index.
    >>> structure.version.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> # Field index: byte offset of the field in the byte stream.
    >>> structure.version.index.byte
    0
    >>> # Field index: bit offset of the field relative to its byte offset.
    >>> structure.version.index.bit
    0
    >>> # Field index: memory address of the field in the data source.
    >>> structure.version.index.address
    0
    >>> # Field index: start address of the byte stream in the data source.
    >>> structure.version.index.base_address
    0
    >>> # Field index: update request for the byte stream.
    >>> structure.version.index.update
    False
    >>> # Field is a bit field.
    >>> structure.version.is_bit()
    False
    >>> # Field is a boolean field.
    >>> structure.version.is_bool()
    False
    >>> # Field is a decimal field.
    >>> structure.version.is_decimal()
    True
    >>> # Field is a float field.
    >>> structure.version.is_float()
    False
    >>> # Field is a pointer field.
    >>> structure.version.is_pointer()
    False
    >>> # Field is a stream field.
    >>> structure.version.is_stream()
    False
    >>> # Field is a string field.
    >>> structure.version.is_string()
    False


Iterate over Members
--------------------

You can **iterate** over the member names of a `structure`_.

    >>> [name for name in structure.keys()] # doctest: +NORMALIZE_WHITESPACE
    ['version', 'id', 'length', 'module']

You can **iterate** over all kind of member items of a `structure`_.

    >>> [(name, member.item_type) for name, member in structure.items()] # doctest: +NORMALIZE_WHITESPACE
    [('version', ItemClass.Byte = 42),
     ('id', ItemClass.Unsigned = 45),
     ('length', ItemClass.Decimal = 40),
     ('module', ItemClass.Char = 43)]

You can **iterate** over all kind of members of a `structure`_.

    >>> [member.item_type for member in structure.values()] # doctest: +NORMALIZE_WHITESPACE
    [ItemClass.Byte = 42,
     ItemClass.Unsigned = 45,
     ItemClass.Decimal = 40,
     ItemClass.Char = 43]

You can **iterate** over all :ref:`field <field>` members of a `structure`_.

    >>> [member.name for member in structure.values() if is_field(member)]
    ['Byte', 'Unsigned8', 'Decimal8', 'Char']


View Field Attributes
---------------------

You can view the **attributes** of each :ref:`field <field>` of a `structure`_
as a **nested** ordered dictionary by calling the method
:meth:`~Structure.view_fields`.

    >>> # View the field values.
    >>> structure.view_fields() # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('version', '0x1'),
                 ('id', '0x2'),
                 ('length', 9),
                 ('module', 'F')])
    >>> # View the field type name, field value pairs.
    >>> structure.view_fields('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('version', ('Byte', '0x1')),
                 ('id', ('Unsigned8', '0x2')),
                 ('length', ('Decimal8', 9)),
                 ('module', ('Char', 'F'))])
    >>> # View the field indexes.
    >>> structure.view_fields('index') # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('version',
                  Index(byte=0, bit=0, address=0, base_address=0, update=False)),
                 ('id',
                  Index(byte=1, bit=0, address=1, base_address=0, update=False)),
                 ('length',
                  Index(byte=2, bit=0, address=2, base_address=0, update=False)),
                 ('module',
                  Index(byte=3, bit=0, address=3, base_address=0, update=False))])


List Field Items
----------------

You can list all :ref:`field <field>` items of a `structure`_
as a **flat** list by calling the method :meth:`~Structure.field_items`.

    >>> # List the field items in the structure.
    >>> structure.field_items() # doctest: +NORMALIZE_WHITESPACE
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


List Field Values
-----------------

You can **view** the *value* of each :ref:`field <field>` in a `structure`_
as a **flat** list by calling the method :meth:`~Container.to_list`.

    >>> # List the field values in the structure.
    >>> structure.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]
    >>> # List the field type names & field values in the structure.
    >>> structure.to_list('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', ('Byte', '0x1')),
     ('Structure.id', ('Unsigned8', '0x2')),
     ('Structure.length', ('Decimal8', 9)),
     ('Structure.module', ('Char', 'F'))]
    >>> # List the field indexes in the structure.
    >>> structure.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.id', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
     ('Structure.length', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Structure.module', Index(byte=3, bit=0, address=3, base_address=0, update=False))]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *value* of each :ref:`field <field>` in a `structure`_
as a **flat** ordered dictionary by calling the method
:meth:`~Container.to_dict`.

    >>> # List the field values in the structure.
    >>> structure.to_dict() # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Structure',
                  OrderedDict([('version', '0x1'),
                               ('id', '0x2'),
                               ('length', 9),
                               ('module', 'F')]))])
    >>> print(json.dumps(structure.to_dict(), indent=2)) # doctest: +NORMALIZE_WHITESPACE
    {
      "Structure": {
        "version": "0x1",
        "id": "0x2",
        "length": 9,
        "module": "F"
      }
    }
    >>> # List the field type names & field values in the structure.
    >>> structure.to_dict('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Structure',
                  OrderedDict([('version', ('Byte', '0x1')),
                                ('id', ('Unsigned8', '0x2')),
                                ('length', ('Decimal8', 9)),
                                ('module', ('Char', 'F'))]))])
    >>> # List the field indexes in the structure.
    >>> structure.to_dict('index') # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Structure',
                  OrderedDict([('version', Index(byte=0, bit=0,
                                                 address=0, base_address=0,
                                                 update=False)),
                               ('id', Index(byte=1, bit=0,
                                            address=1, base_address=0,
                                            update=False)),
                               ('length', Index(byte=2, bit=0,
                                                address=2, base_address=0,
                                                update=False)),
                               ('module', Index(byte=3, bit=0,
                                                address=3, base_address=0,
                                                update=False))]))])


.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Save Field Values
-----------------

You can **save** the *value* of each :ref:`field <field>` in a `structure`_
to an ``.ini`` file by calling the method :meth:`~Container.save`.

    >>> # List the field values in the structure.
    >>> structure.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]
    >>> # Save the field values to an '.ini' file.
    >>> structure.save("_static/structure.ini")

The generated ``.ini`` file for the structure looks like this:

.. literalinclude:: _static/structure.ini
    :language: ini

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.


Load Field Values
-----------------

You can **load** the *value* of each :ref:`field <field>` in a `structure`_
from an ``.ini`` file by calling the method :meth:`~Container.load`.

    >>> # Create a structure.
    >>> structure = Structure(
    ...     version=Byte(),
    ...     id=Unsigned8(),
    ...     length=Decimal8(),
    ...     module=Char())
    >>> # Load the field values from an '.ini' file.
    >>> structure.load("_static/structure.ini")
    [Structure]
    Structure.version = 0x1
    Structure.id = 0x2
    Structure.length = 9
    Structure.module = F
    >>> # List the field values in the structure.
    >>> structure.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.
