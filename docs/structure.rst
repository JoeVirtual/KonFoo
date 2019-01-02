.. currentmodule:: konfoo

.. testsetup:: *

    import json
    import sys
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

    >>> class Identifier(Structure):
    ...
    ...     def __init__(self):
    ...         super().__init__()        # <- NEVER forget to call it first!
    ...         self.version = Byte()     # 1st field
    ...         self.id = Unsigned8()     # 2nd field
    ...         self.length = Decimal8()  # 3rd field
    ...         self.module = Char()      # 4th field
    ...         self.index_fields()       # <- Indexes all fields (optional)
    >>> # Create an instance of the structure.
    >>> identifier = Identifier()
    >>> # List the field values of the structure.
    >>> identifier.to_list()
    [('Identifier.version', '0x0'),
     ('Identifier.id', '0x0'),
     ('Identifier.length', 0),
     ('Identifier.module', '\x00')]
    >>> # List the field values of the structure as a CSV list.
    >>> identifier.to_csv()
    [{'id': 'Identifier.version', 'value': '0x0'},
     {'id': 'Identifier.id', 'value': '0x0'},
     {'id': 'Identifier.length', 'value': 0},
     {'id': 'Identifier.module', 'value': '\x00'}]
    >>> # View the structure field values as a JSON string.
    >>> identifier.to_json()
    '{"version": "0x0", "id": "0x0", "length": 0, "module": "\\u0000"}'

.. warning::
    A `structure`_ must always align to full bytes or an exception will be
    raised when an incomplete `structure`_ declaration is deserialized or
    serialized.


Align Fields in a Structure
---------------------------

You can :ref:`align <field alignment>` consecutive fields in a `structure`_ to
each other by using the ``align_to`` parameter of the :class:`Field` class.

    >>> class Identifier(Structure):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.version = Byte(align_to=4)       # 1st field aligned to 4 bytes
    ...         self.id = Unsigned(8, align_to=4)     # 2nd field aligned to 4 bytes
    ...         self.length = Decimal(8, align_to=4)  # 3rd field aligned to 4 bytes
    ...         self.module = Char(align_to=4)        # 4th field aligned to 4 bytes
    ...         self.index_fields()
    >>> # Create an instance of the structure.
    >>> identifier = Identifier()
    >>> # List the field alignments of the structure.
    >>> identifier.to_list('alignment')
    [('Identifier.version', Alignment(byte_size=4, bit_offset=0)),
     ('Identifier.id', Alignment(byte_size=4, bit_offset=8)),
     ('Identifier.length', Alignment(byte_size=4, bit_offset=16)),
     ('Identifier.module', Alignment(byte_size=4, bit_offset=24))]
    >>> # List the field alignments of the structure as a CSV list.
    >>> identifier.to_csv('alignment.byte_size', 'alignment.bit_offset')
    [{'id': 'Identifier.version', 'alignment.byte_size': 4, 'alignment.bit_offset': 0},
     {'id': 'Identifier.id', 'alignment.byte_size': 4, 'alignment.bit_offset': 8},
     {'id': 'Identifier.length', 'alignment.byte_size': 4, 'alignment.bit_offset': 16},
     {'id': 'Identifier.module', 'alignment.byte_size': 4, 'alignment.bit_offset': 24}]
    >>> # View the structure field alignments as a JSON string.
    >>> identifier.to_json('alignment')
    '{"version": [4, 0], "id": [4, 8], "length": [4, 16], "module": [4, 24]}'

.. note::
    The field :ref:`alignment <field alignment>` works only for the
    :class:`Decimal` :ref:`field <field>` classes.


Nest Structures
---------------

You can **nest** a `structure`_ in another `structure`_.

    >>> # Define a new structure class with a nested structure.
    >>> class Header(Structure):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.type = Identifier()  # nested structure
    ...         self.size = Decimal32()
    ...         self.index_fields()
    >>> # Create an instance of the structure.
    >>> header = Header()
    >>> # List the field values of the structure.
    >>> header.to_list()
    [('Header.type.version', '0x0'),
     ('Header.type.id', '0x0'),
     ('Header.type.length', 0),
     ('Header.type.module', '\x00'),
     ('Header.size', 0)]
    >>> # List the field values of the structure as a CSV list.
    >>> header.to_csv()
    [{'id': 'Header.type.version', 'value': '0x0'},
     {'id': 'Header.type.id', 'value': '0x0'},
     {'id': 'Header.type.length', 'value': 0},
     {'id': 'Header.type.module', 'value': '\x00'},
     {'id': 'Header.size', 'value': 0}]
    >>> # View the structure field values as a JSON string.
    >>> header.to_json()
    '{"type": {"version": "0x0", "id": "0x0", "length": 0, "module": "\\u0000"},
      "size": 0}'


Inherit from a Structure
------------------------

You can **inherit** the members from a `structure`_ class to extend or change it.

    >>> # Define a new structure class.
    >>> class HeaderV1(Structure):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.type = Identifier()
    ...         self.index_fields()
    >>> # Create an instance of the structure.
    >>> header = HeaderV1()
    >>> # List the field values of the structure.
    >>> header.to_list()
    [('HeaderV1.type.version', '0x0'),
     ('HeaderV1.type.id', '0x0'),
     ('HeaderV1.type.length', 0),
     ('HeaderV1.type.module', '\x00')]
    >>> # List the field values of the structure as a CSV list.
    >>> header.to_csv()
    [{'id': 'HeaderV1.type.version', 'value': '0x0'},
     {'id': 'HeaderV1.type.id', 'value': '0x0'},
     {'id': 'HeaderV1.type.length', 'value': 0},
     {'id': 'HeaderV1.type.module', 'value': '\x00'}]
    >>> # View the structure field values as a JSON string.
    >>> header.to_json()
    '{"type": {"version": "0x0", "id": "0x0", "length": 0, "module": "\\u0000"}}'

    >>> # Define a new structure class inherit from a structure the fields.
    >>> class HeaderV2(HeaderV1):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.size = Decimal32()
    ...         self.index_fields()
    >>> # Create an instance of the structure.
    >>> header = HeaderV2()
    >>> # List the field values of the structure.
    >>> header.to_list()
    [('HeaderV2.type.version', '0x0'),
     ('HeaderV2.type.id', '0x0'),
     ('HeaderV2.type.length', 0),
     ('HeaderV2.type.module', '\x00'),
     ('HeaderV2.size', 0)]
    >>> # List the field values of the structure as a CSV list.
    >>> header.to_csv()
    [{'id': 'HeaderV2.type.version', 'value': '0x0'},
     {'id': 'HeaderV2.type.id', 'value': '0x0'},
     {'id': 'HeaderV2.type.length', 'value': 0},
     {'id': 'HeaderV2.type.module', 'value': '\x00'},
     {'id': 'HeaderV2.size', 'value': 0}]
    >>> # View the structure field values as a JSON string.
    >>> header.to_json()
    '{"type": {"version": "0x0", "id": "0x0", "length": 0, "module": "\\u0000"},
      "size": 0}'


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
    >>> # List the field values of the structure.
    >>> structure.to_list()
    [('Structure.version', '0x0'),
     ('Structure.id', '0x0'),
     ('Structure.length', 0),
     ('Structure.module', '\x00')]
    >>> # List the field values of the structure as a CSV list.
    >>> structure.to_csv()
    [{'id': 'Structure.version', 'value': '0x0'},
     {'id': 'Structure.id', 'value': '0x0'},
     {'id': 'Structure.length', 'value': 0},
     {'id': 'Structure.module', 'value': '\x00'}]
    >>> # View the structure field values as a JSON string.
    >>> structure.to_json()
    '{"version": "0x0", "id": "0x0", "length": 0, "module": "\\u0000"}'


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
    >>> # List the field alignments of the structure.
    >>> structure.to_list('alignment')
    [('Structure.version', Alignment(byte_size=4, bit_offset=0)),
     ('Structure.id', Alignment(byte_size=4, bit_offset=8)),
     ('Structure.length', Alignment(byte_size=4, bit_offset=16)),
     ('Structure.module', Alignment(byte_size=4, bit_offset=24))]
    >>> # List the field alignments of the structure as a CSV list.
    >>> structure.to_csv('alignment.byte_size', 'alignment.bit_offset')
    [{'id': 'Structure.version', 'alignment.byte_size': 4, 'alignment.bit_offset': 0},
     {'id': 'Structure.id', 'alignment.byte_size': 4, 'alignment.bit_offset': 8},
     {'id': 'Structure.length', 'alignment.byte_size': 4, 'alignment.bit_offset': 16},
     {'id': 'Structure.module', 'alignment.byte_size': 4, 'alignment.bit_offset': 24}]
    >>> # View the structure field alignments as a JSON string.
    >>> structure.to_json('alignment')
    '{"version": [4, 0], "id": [4, 8], "length": [4, 16], "module": [4, 24]}'

You can **declare** a `structure`_ with keywords.

    >>> # Create a structure with keywords.
    >>> structure = Structure(
    ...     version=Byte(4),
    ...     id=Unsigned(8, 4),
    ...     length=Decimal(8, 4),
    ...     module=Char(4))
    >>> # List the field values of the structure.
    >>> structure.to_list()
    [('Structure.version', '0x0'),
     ('Structure.id', '0x0'),
     ('Structure.length', 0),
     ('Structure.module', '\x00')]
    >>> # List the field values of the structure as a CSV list.
    >>> structure.to_csv()
    [{'id': 'Structure.version', 'value': '0x0'},
     {'id': 'Structure.id', 'value': '0x0'},
     {'id': 'Structure.length', 'value': 0},
     {'id': 'Structure.module', 'value': '\x00'}]
    >>> # View the structure field values as a JSON string.
    >>> structure.to_json()
    '{"version": "0x0", "id": "0x0", "length": 0, "module": "\\u0000"}'

You can **nest** `structure`_'s on the fly.

    >>> # Create an empty structure.
    >>> structure = Structure()
    >>> # Add an empty nested structure to the structure.
    >>> structure.type = Structure()
    >>> # Add fields to the nested structure.
    >>> structure.type.version = Byte(4)
    >>> structure.type.id = Unsigned(8, 4)
    >>> structure.type.length = Decimal(8, 4)
    >>> structure.type.module = Char(4)
    >>> # Add a field to the structure.
    >>> structure.size = Decimal32()
    >>> # List the field values of the structure.
    >>> structure.to_list()
    [('Structure.type.version', '0x0'),
     ('Structure.type.id', '0x0'),
     ('Structure.type.length', 0),
     ('Structure.type.module', '\x00'),
     ('Structure.size', 0)]
    >>> # List the field values of the structure as a CSV list.
    >>> structure.to_csv()
    [{'id': 'Structure.type.version', 'value': '0x0'},
     {'id': 'Structure.type.id', 'value': '0x0'},
     {'id': 'Structure.type.length', 'value': 0},
     {'id': 'Structure.type.module', 'value': '\x00'},
     {'id': 'Structure.size', 'value': 0}]
    >>> # View the structure field values as a JSON string.
    >>> structure.to_json()
    '{"type": {"version": "0x0", "id": "0x0", "length": 0, "module": "\\u0000"},
      "size": 0}'

You can **assign** a `structure`_ to a member of another `structure`_ on the fly.

    >>> # Create a structure to be nested.
    >>> identifier = Structure(
    ...     version = Byte(4),
    ...     id = Unsigned(8, 4),
    ...     length = Decimal(8, 4),
    ...     module = Char(4))
    >>> # Create an empty structure.
    >>> structure = Structure()
    >>> # Add a nested structure to the structure.
    >>> structure.type = identifier
    >>> # Add a field to the structure.
    >>> structure.size = Decimal32()
    >>> # List the field values of the structure.
    >>> structure.to_list()
    [('Structure.type.version', '0x0'),
     ('Structure.type.id', '0x0'),
     ('Structure.type.length', 0),
     ('Structure.type.module', '\x00'),
     ('Structure.size', 0)]
    >>> # List the field values of the structure as a CSV list.
    >>> structure.to_csv()
    [{'id': 'Structure.type.version', 'value': '0x0'},
     {'id': 'Structure.type.id', 'value': '0x0'},
     {'id': 'Structure.type.length', 'value': 0},
     {'id': 'Structure.type.module', 'value': '\x00'},
     {'id': 'Structure.size', 'value': 0}]
    >>> # View the structure field values as a JSON string.
    >>> structure.to_json()
    '{"type": {"version": "0x0", "id": "0x0", "length": 0, "module": "\\u0000"},
      "size": 0}'


Initialize a Structure
----------------------

You can **initialize** the fields in a `structure`_ by calling the method
:meth:`~Structure.initialize_fields`.

    >>> # Create a structure.
    >>> structure = Structure(
    ...     version=Byte(4),
    ...     id=Unsigned(8, 4),
    ...     length=Decimal(8, 4),
    ...     module=Char(4))
    >>> # List the field values of the structure.
    >>> structure.to_list()
    [('Structure.version', '0x0'),
     ('Structure.id', '0x0'),
     ('Structure.length', 0),
     ('Structure.module', '\x00')]
    >>> # List the field values of the structure as a CSV list.
    >>> structure.to_csv()
    [{'id': 'Structure.version', 'value': '0x0'},
     {'id': 'Structure.id', 'value': '0x0'},
     {'id': 'Structure.length', 'value': 0},
     {'id': 'Structure.module', 'value': '\x00'}]
    >>> # View the structure field values as a JSON string.
    >>> structure.to_json()
    '{"version": "0x0", "id": "0x0", "length": 0, "module": "\\u0000"}'

    >>> # Initialize the fields of the structure.
    >>> structure.initialize_fields(
    ...     dict(version=1, id=2, length=9, module=0x46))
    >>> # Initialize the fields in the structure.
    >>> structure.initialize_fields({
    ...     "version": "0x1",
    ...     "id": "0x2",
    ...     "length": 9,
    ...     "module": "F"
    ... })
    >>> # List the field values of the structure.
    >>> structure.to_list()
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]
    >>> # List the field values of the structure as a CSV list.
    >>> structure.to_csv()
    [{'id': 'Structure.version', 'value': '0x1'},
     {'id': 'Structure.id', 'value': '0x2'},
     {'id': 'Structure.length', 'value': 9},
     {'id': 'Structure.module', 'value': 'F'}]
    >>> # View the structure field values as a JSON string.
    >>> structure.to_json()
    '{"version": "0x1", "id": "0x2", "length": 9, "module": "F"}'


Display a Structure
-------------------

You can **display** the `structure`_.

    >>> # Create a structure.
    >>> structure = Structure(
    ...     version=Byte(4),
    ...     id=Unsigned(8, 4),
    ...     length=Decimal(8, 4),
    ...     module=Char(4))
    >>> # Index the fields in the structure.
    >>> structure.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Display the structure.
    >>> structure
    Structure([('version', Byte(index=Index(byte=0, bit=0,
                                            address=0, base_address=0,
                                            update=False),
                                alignment=Alignment(byte_size=4, bit_offset=0),
                                bit_size=8,
                                value='0x0')),
                ('id', Unsigned(index=Index(byte=0, bit=8,
                                            address=0, base_address=0,
                                            update=False),
                                alignment=Alignment(byte_size=4, bit_offset=8),
                                bit_size=8,
                                value='0x0')),
                ('length', Decimal(index=Index(byte=0, bit=16,
                                               address=0, base_address=0,
                                               update=False),
                                   alignment=Alignment(byte_size=4, bit_offset=16),
                                   bit_size=8,
                                   value=0)),
                ('module', Char(index=Index(byte=0, bit=24,
                                            address=0, base_address=0,
                                            update=False),
                                alignment=Alignment(byte_size=4, bit_offset=24),
                                bit_size=8,
                                value='\x00'))])


Metadata of a Structure
-----------------------

You can get the metadata of the `structure`_ by calling the method
:meth:`~Structure.describe`.

    >>> # Get the description of the structure.
    >>> structure.describe()
    OrderedDict([('class', 'Structure'),
                 ('name', 'Structure'),
                 ('size', 4),
                 ('type', 'Structure'),
                 ('member',
                  [OrderedDict([('address', 0),
                                ('alignment', [4, 0]),
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
                   OrderedDict([('address', 0),
                                ('alignment', [4, 8]),
                                ('class', 'Unsigned8'),
                                ('index', [0, 8]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'id'),
                                ('order', 'auto'),
                                ('signed', False),
                                ('size', 8),
                                ('type', 'Field'),
                                ('value', '0x0')]),
                   OrderedDict([('address', 0),
                                ('alignment', [4, 16]),
                                ('class', 'Decimal8'),
                                ('index', [0, 16]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'length'),
                                ('order', 'auto'),
                                ('signed', False),
                                ('size', 8),
                                ('type', 'Field'),
                                ('value', 0)]),
                   OrderedDict([('address', 0),
                                ('alignment', [4, 24]),
                                ('class', 'Char'),
                                ('index', [0, 24]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'module'),
                                ('order', 'auto'),
                                ('signed', False),
                                ('size', 8),
                                ('type', 'Field'),
                                ('value', '\x00')])])])

    >>> json.dump(structure.describe(), sys.stdout, indent=2)
    {
      "class": "Structure",
      "name": "Structure",
      "size": 4,
      "type": "Structure",
      "member": [
        {
          "address": 0,
          "alignment": [
            4,
            0
          ],
          "class": "Byte",
          "index": [
            0,
            0
          ],
          "max": 255,
          "min": 0,
          "name": "version",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": "0x0"
        },
        {
          "address": 0,
          "alignment": [
            4,
            8
          ],
          "class": "Unsigned8",
          "index": [
            0,
            8
          ],
          "max": 255,
          "min": 0,
          "name": "id",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": "0x0"
        },
        {
          "address": 0,
          "alignment": [
            4,
            16
          ],
          "class": "Decimal8",
          "index": [
            0,
            16
          ],
          "max": 255,
          "min": 0,
          "name": "length",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": 0
        },
        {
          "address": 0,
          "alignment": [
            4,
            24
          ],
          "class": "Char",
          "index": [
            0,
            24
          ],
          "max": 255,
          "min": 0,
          "name": "module",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": "\u0000"
        }
      ]
    }


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
    >>> structure.to_list('index')
    [('Structure.version', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.id', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.length', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.module', Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # List the field indexes of the structure as a CSV list.
    >>> structure.to_csv('index.byte', 'index.address')
    [{'id': 'Structure.version', 'index.byte': 0, 'index.address': 0},
     {'id': 'Structure.id', 'index.byte': 0, 'index.address': 0},
     {'id': 'Structure.length', 'index.byte': 0, 'index.address': 0},
     {'id': 'Structure.module', 'index.byte': 0, 'index.address': 0}]
    >>> # View the structure field indexes as a JSON string.
    >>> structure.to_json('index')
    '{"version": [0, 0, 0, 0, false],
      "id":      [0, 0, 0, 0, false],
      "length":  [0, 0, 0, 0, false],
      "module":  [0, 0, 0, 0, false]}'

    >>> # Index the fields in the structure.
    >>> structure.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the fields in the structure with a start index.
    >>> structure.index_fields(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes of the structure.
    >>> structure.to_list('index')
    [('Structure.version', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.id', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
     ('Structure.length', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Structure.module', Index(byte=3, bit=0, address=3, base_address=0, update=False))]
    >>> # List the field indexes of the structure as a CSV list.
    >>> structure.to_csv('index.byte', 'index.address')
    [{'id': 'Structure.version', 'index.byte': 0, 'index.address': 0},
     {'id': 'Structure.id', 'index.byte': 1, 'index.address': 1},
     {'id': 'Structure.length', 'index.byte': 2, 'index.address': 2},
     {'id': 'Structure.module', 'index.byte': 3, 'index.address': 3}]
    >>> # View the structure field indexes as a JSON string.
    >>> structure.to_json('index')
    '{"version": [0, 0, 0, 0, false],
      "id":      [1, 0, 1, 0, false],
      "length":  [2, 0, 2, 0, false],
      "module":  [3, 0, 3, 0, false]}'


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
    >>> # List the field values of the structure.
    >>> structure.to_list()
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]
    >>> # List the field values of the structure as a CSV list.
    >>> structure.to_csv()
    [{'id': 'Structure.version', 'value': '0x1'},
     {'id': 'Structure.id', 'value': '0x2'},
     {'id': 'Structure.length', 'value': 9},
     {'id': 'Structure.module', 'value': 'F'}]
    >>> # View the structure field values as a JSON string.
    >>> structure.to_json()
    '{"version": "0x1", "id": "0x2", "length": 9, "module": "F"}'


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
    >>> bytestream.hex()
    '01020946'

or

    >>> bytes(structure).hex()
    '01020946'



Number of Members
-----------------

You can **get** the number of `structure`_ members with the built-in function
:func:`len`.

    >>> # Number of structure members.
    >>> len(structure)
    4


Access a Member
---------------

You can **access** a `structure`_ member with its name.

    >>> # Access a structure member with its attribute name.
    >>> structure.version
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=Alignment(byte_size=1, bit_offset=0),
         bit_size=8,
         value='0x1')
    >>> # Access a structure member with its key name.
    >>> structure['version']
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=Alignment(byte_size=1, bit_offset=0),
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
    Alignment(byte_size=1, bit_offset=0)
    >>> # Field alignment: byte size of the aligned field group.
    >>> structure.version.alignment.byte_size
    1
    >>> # Field alignment: bit offset of the field in its field group.
    >>> structure.version.alignment.bit_offset
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


You can **check** if a `structure member`_ is a :ref:`field <field>`.

    >>> is_field(structure.version)
    True


You can **check** what kind of :ref:`field <field>` it is.

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

You can **iterate** over the `structure member`_ names.

    >>> [name for name in structure.keys()]
    ['version', 'id', 'length', 'module']

You can **iterate** over all kind of member items of a `structure`_.

    >>> [(name, member.item_type) for name, member in structure.items()]
    [('version', ItemClass.Byte = 42),
     ('id', ItemClass.Unsigned = 45),
     ('length', ItemClass.Decimal = 40),
     ('module', ItemClass.Char = 43)]

You can **iterate** over all kind of members of a `structure`_.

    >>> [member.item_type for member in structure.values()]
    [ItemClass.Byte = 42,
     ItemClass.Unsigned = 45,
     ItemClass.Decimal = 40,
     ItemClass.Char = 43]

You can **iterate** over all :ref:`field <field>` members of a `structure`_.

    >>> [member.name for member in structure.values() if is_field(member)]
    ['Byte', 'Unsigned8', 'Decimal8', 'Char']


View Field Attributes
---------------------

You can **view** the *attributes* of each :ref:`field <field>` of a `structure`_
as an ordered dictionary by calling the method :meth:`~Structure.view_fields`.
Default attribute is the field :attr:`~Field.value`.

    >>> # View the structure field values.
    >>> structure.view_fields()
    OrderedDict([('version', '0x1'),
                 ('id', '0x2'),
                 ('length', 9),
                 ('module', 'F')])
    >>> # View the structure field type names & field values.
    >>> structure.view_fields('name', 'value')
    OrderedDict([('version', {'name': 'Byte', 'value': '0x1'}),
                 ('id', {'name': 'Unsigned8', 'value': '0x2'}),
                 ('length', {'name': 'Decimal8', 'value': 9}),
                 ('module', {'name': 'Char', 'value': 'F'})])
    >>> # View the structure field indexes.
    >>> structure.view_fields('index')
    OrderedDict([('version',
                  Index(byte=0, bit=0, address=0, base_address=0, update=False)),
                 ('id',
                  Index(byte=1, bit=0, address=1, base_address=0, update=False)),
                 ('length',
                  Index(byte=2, bit=0, address=2, base_address=0, update=False)),
                 ('module',
                  Index(byte=3, bit=0, address=3, base_address=0, update=False))])

.. note::
    The *attributes* of each :ref:`field <field>` for containers *nested* in the
    `structure`_ are viewed as well (chained method call).


View as a JSON string
---------------------

You can view the *attributes* of each :ref:`field <field>` of a `structure`_
as a **JSON** formatted string by calling the method :meth:`~Container.to_json`.
Default attribute is the field :attr:`~Field.value`.

    >>> # View the structure field values as a JSON string.
    >>> structure.to_json()
    '{"version": "0x1", "id": "0x2", "length": 9, "module": "F"}'
    >>> print(structure.to_json(indent=2))
    {
      "version": "0x1",
      "id": "0x2",
      "length": 9,
      "module": "F"
    }
    >>> # View the structure field type names & field values as a JSON string.
    >>> structure.to_json('name', 'value')
    '{"version": {"name": "Byte", "value": "0x1"},
      "id": {"name": "Unsigned8", "value": "0x2"},
      "length": {"name": "Decimal8", "value": 9},
      "module": {"name": "Char", "value": "F"}}'
    >>> # View the structure field indexes as a JSON string.
    >>> structure.to_json('index')
    '{"version": [0, 0, 0, 0, false],
      "id": [1, 0, 1, 0, false],
      "length": [2, 0, 2, 0, false],
      "module": [3, 0, 3, 0, false]}'

.. note::
    The *attributes* of each :ref:`field <field>` for containers *nested* in the
    `structure`_ are viewed as well (chained method call).


List Field Items
----------------

You can list all :ref:`field <field>` items of a `structure`_
as a **flatten** list by calling the method :meth:`~Structure.field_items`.

    >>> # List the field items of the structure.
    >>> structure.field_items()
    [('version',
     Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=Alignment(byte_size=1, bit_offset=0),
          bit_size=8,
          value='0x1')),
    ('id',
     Unsigned8(index=Index(byte=1, bit=0, address=1, base_address=0, update=False),
               alignment=Alignment(byte_size=1, bit_offset=0),
               bit_size=8,
               value='0x2')),
    ('length',
     Decimal8(index=Index(byte=2, bit=0, address=2, base_address=0, update=False),
              alignment=Alignment(byte_size=1, bit_offset=0),
              bit_size=8,
              value=9)),
    ('module',
     Char(index=Index(byte=3, bit=0, address=3, base_address=0, update=False),
          alignment=Alignment(byte_size=1, bit_offset=0),
          bit_size=8,
          value='F'))]


List Field Attributes
---------------------

You can **list** the *attributes* of each :ref:`field <field>` of a `structure`_
as a **flatten** list by calling the method :meth:`~Container.to_list`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the structure.
    >>> structure.to_list()
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]
    >>> # List the field type names & values of the structure.
    >>> structure.to_list('name', 'value')
    [('Structure.version', ('Byte', '0x1')),
     ('Structure.id', ('Unsigned8', '0x2')),
     ('Structure.length', ('Decimal8', 9)),
     ('Structure.module', ('Char', 'F'))]
    >>> # List the field indexes of the structure.
    >>> structure.to_list('index')
    [('Structure.version', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Structure.id', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
     ('Structure.length', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Structure.module', Index(byte=3, bit=0, address=3, base_address=0, update=False))]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **list** the *attributes* of each :ref:`field <field>` of a `structure`_
as a **flatten** ordered dictionary by calling the method :meth:`~Container.to_dict`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the structure.
    >>> structure.to_dict()
    OrderedDict([('Structure',
                  OrderedDict([('version', '0x1'),
                               ('id', '0x2'),
                               ('length', 9),
                               ('module', 'F')]))])
    >>> # List the field type names & values of the structure.
    >>> structure.to_dict('name', 'value')
    OrderedDict([('Structure',
                  OrderedDict([('version', ('Byte', '0x1')),
                                ('id', ('Unsigned8', '0x2')),
                                ('length', ('Decimal8', 9)),
                                ('module', ('Char', 'F'))]))])
    >>> # List the field indexes in the structure.
    >>> structure.to_dict('index')
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


You can **list** the *attributes* of each :ref:`field <field>` of a `structure`_
as a **flatten** list of dictionaries containing the field *path* and the selected
field *attributes* by calling the method :meth:`~Container.to_csv`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the structure as a CSV list.
    >>> structure.to_csv()
    [{'id': 'Structure.version', 'value': '0x1'},
     {'id': 'Structure.id', 'value': '0x2'},
     {'id': 'Structure.length', 'value': 9},
     {'id': 'Structure.module', 'value': 'F'}]
    >>> # List the field type names & values of the structure as a CSV list.
    >>> structure.to_csv('name', 'value')
    [{'id': 'Structure.version', 'name': 'Byte', 'value': '0x1'},
     {'id': 'Structure.id', 'name': 'Unsigned8', 'value': '0x2'},
     {'id': 'Structure.length', 'name': 'Decimal8', 'value': 9},
     {'id': 'Structure.module', 'name': 'Char', 'value': 'F'}]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Write Field Attributes
----------------------

You can **write** the *attributes* of each :ref:`field <field>` of a `structure`_
to a ``.csv`` file by calling the method :meth:`~Container.write_csv`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the structure as a CSV list.
    >>> structure.to_csv()
    [{'id': 'Structure.version', 'value': '0x1'},
     {'id': 'Structure.id', 'value': '0x2'},
     {'id': 'Structure.length', 'value': 9},
     {'id': 'Structure.module', 'value': 'F'}]
    >>> # Save the structure field values to a '.csv' file.
    >>> structure.write_csv("_static/structure.csv")

The generated ``.csv`` file for the structure looks like this:

.. literalinclude:: _static/structure.csv

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Save Field Attributes
---------------------

You can **save** the *attributes* of each :ref:`field <field>` of a `structure`_
to an ``.ini`` file by calling the method :meth:`~Container.save`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the structure.
    >>> structure.to_list()
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]
    >>> # Save the structure field values to an '.ini' file.
    >>> structure.save("_static/structure.ini")

The generated ``.ini`` file for the structure looks like this:

.. literalinclude:: _static/structure.ini
    :language: ini

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.


Load Field Values
-----------------

You can **load** the *value* of each :ref:`field <field>` of a `structure`_
from an ``.ini`` file by calling the method :meth:`~Container.load`.

    >>> # Create a structure.
    >>> structure = Structure(
    ...     version=Byte(),
    ...     id=Unsigned8(),
    ...     length=Decimal8(),
    ...     module=Char())
    >>> # Load the structure field values from an '.ini' file.
    >>> structure.load("_static/structure.ini")
    [Structure]
    Structure.version = 0x1
    Structure.id = 0x2
    Structure.length = 9
    Structure.module = F
    >>> # List the field values of the structure.
    >>> structure.to_list()
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.
