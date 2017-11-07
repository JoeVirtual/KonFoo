.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
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
            self.next_index()         # <- Indexes all fields (optional)

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
            self.next_index()

.. note:: The field :ref:`alignment <field alignment>` works only for the
          :class:`Decimal` :ref:`field <field>` classes.


Re-use a Structure
------------------

You can re-use a `structure`_

.. code-block:: python
    :emphasize-lines: 5

    class Header(Structure):

        def __init__(self):
            super().__init__()
            self.type = Identifier()  # re-used structure
            self.size = Decimal32()
            self.next_index()


Parametrize a Structure
-----------------------

You can define a `structure`_ with arguments.

.. code-block:: python
    :emphasize-lines: 1-4

    >>> class Parametrized(Structure):
    ...     def __init__(self, arg, *args, **kwargs):
    ...         super().__init__()
    ...         self.field = arg
    >>> structure = Parametrized(Byte())
    >>> structure # doctest: +NORMALIZE_WHITESPACE
    Parametrized([('field',
                    Byte(index=Index(byte=0, bit=0,
                                     address=0, base_address=0,
                                     update=False),
                         alignment=(1, 0),
                         bit_size=8,
                         value='0x0'))])


Inherit from a Structure
------------------------

You can inherit the members from a `structure`_ class to extend or change it.

.. code-block:: python
    :emphasize-lines: 23-29

    >>> class HeaderV1(Structure):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.type = Decimal32()
    ...         self.next_index()
    >>> header = HeaderV1()
    >>> header.field_items() # doctest: +NORMALIZE_WHITESPACE
    HeaderV1([('type',
                Decimal32(index=Index(byte=0, bit=0,
                                      address=0, base_address=0,
                                      update=False),
                          alignment=(4, 0),
                          bit_size=32,
                          value='0x0'))])
    >>> class HeaderV2(HeaderV1):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.size = Decimal32()
    >>> header = HeaderV2()
    >>> header # doctest: +NORMALIZE_WHITESPACE
    HeaderV2([('type',
                Decimal32(index=Index(byte=0, bit=0,
                                      address=0, base_address=0,
                                      update=False),
                          alignment=(4, 0),
                          bit_size=32,
                          value='0x0')),
               ('size',
                Decimal32(index=Index(byte=4, bit=0,
                                      address=4, base_address=0,
                                      update=False),
                          alignment=(4, 0),
                          bit_size=32,
                          value='0x0'))])


Declare on the fly
------------------

You can **declare** a `structure`_ on the fly.

    >>> structure = Structure()
    >>> structure.version = Byte()
    >>> structure.id = Unsigned8()
    >>> structure.length = Decimal8()
    >>> structure.module = Char()
    >>> structure.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pprint(structure.field_indexes()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('version',
                  Index(byte=0, bit=0, address=0, base_address=0, update=False)),
                 ('id',
                  Index(byte=1, bit=0, address=1, base_address=0, update=False)),
                 ('length',
                  Index(byte=2, bit=0, address=2, base_address=0, update=False)),
                 ('module',
                  Index(byte=3, bit=0, address=3, base_address=0, update=False))])

You can **nest** `structure`_ 's on the fly.

.. code-block:: python
    :emphasize-lines: 2-6

    >>> structure = Structure()
    >>> structure.type = Structure()
    >>> structure.type.version = Byte()
    >>> structure.type.id = Unsigned8()
    >>> structure.type.length = Decimal8()
    >>> structure.type.module = Char()
    >>> structure.size = Decimal32()
    >>> structure.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.type.version', '0x0'),
     ('Structure.type.id', '0x0'),
     ('Structure.type.length', 0),
     ('Structure.type.module', '\x00'),
     ('Structure.size', 0)]


You can declare a `structure`_ with :ref:`aligned <field alignment>` fields on
the fly.

.. code-block:: python
    :emphasize-lines: 2-5

    >>> structure = Structure()
    >>> structure.version = Byte(4)
    >>> structure.id = Unsigned(8, 4)
    >>> structure.length = Decimal(8, 4)
    >>> structure.module = Char(4)
    >>> structure.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pprint(structure.field_indexes())
    {'version': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'id': Index(byte=0, bit=8, address=0, base_address=0, update=False),
     'length': Index(byte=0, bit=16, address=0, base_address=0, update=False),
     'module': Index(byte=0, bit=24, address=0, base_address=0, update=False)}


You can **assign** a `structure`_ to a member in a other `structure`_ on the fly.

.. code-block:: python
    :emphasize-lines: 2

    >>> reuse = Structure()
    >>> reuse.type = structure  # assign structure
    >>> reuse.size = Decimal32()
    >>> reuse.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.type.version', '0x0'),
     ('Structure.type.id', '0x0'),
     ('Structure.type.length', 0),
     ('Structure.type.module', '\x00'),
     ('Structure.size', 0)]


View a Structure
----------------

You can **view** the `structure`_

.. code-block:: python
    :emphasize-lines: 6

    >>> structure = Structure()
    >>> structure.version = Byte()
    >>> structure.id = Unsigned8()
    >>> structure.length = Decimal8()
    >>> structure.module = Char()
    >>> structure # doctest: +NORMALIZE_WHITESPACE
    Structure([('version', Byte(index=Index(byte=0, bit=0,
                                            address=0, base_address=0,
                                            update=False),
                                alignment=(1, 0),
                                bit_size=8,
                                value='0x0')),
                ('id', Unsigned8(index=Index(byte=0, bit=0,
                                             address=0, base_address=0,
                                             update=False),
                                alignment=(1, 0),
                                bit_size=8,
                                value='0x0')),
                ('length', Decimal8(index=Index(byte=0, bit=0,
                                                address=0, base_address=0,
                                                update=False),
                                   alignment=(1, 0),
                                   bit_size=8,
                                   value=0)),
                ('module', Char(index=Index(byte=0, bit=0,
                                            address=0, base_address=0,
                                            update=False),
                                alignment=(1, 0),
                                bit_size=8,
                                value='\x00'))])

Blueprint of a Structure
------------------------

You can get the blueprint of the `structure`_ by calling the method
:meth:`~Structure.blueprint`.

    >>> pprint(structure.blueprint()) # doctest: +NORMALIZE_WHITESPACE
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


Length of a Structure
---------------------

You can get the **length** of a `structure`_ as a tuple in the form of
``(number of bytes, remaining bits)`` by calling the method
:meth:`~Structure.field_length`.

    >>> structure.field_length()
    (4, 0)

.. note::

   The remaining bits must be always zero or the `structure`_ declaration is
   incomplete.


Indexing
--------

You can get the *byte stream* :class:`Index` after the last :ref:`field <field>`
of a `structure`_ by calling the method :meth:`~Structure.next_index`.

    >>> structure.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)

.. note::

    The method re-indexes all members of the `structure`_ as well.


De-Serializing
--------------

You can **deserialize** a byte stream with a `structure`_ by calling the method
:meth:`~Structure.deserialize`.

    >>> bytestream = bytes.fromhex('01020946f00f00')
    >>> structure.deserialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)


Serializing
-----------

You can **serialize** a byte stream with a `structure`_ by calling the method
:meth:`~Structure.serialize`.

    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> structure.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'01020946'


Access a Member
---------------

You can **access** a member in a `structure`_ with its name.

    >>> structure.version # doctest: +NORMALIZE_WHITESPACE
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=(1, 0),
         bit_size=8,
         value='0x1')
    >>> structure['version'] # doctest: +NORMALIZE_WHITESPACE
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=(1, 0),
         bit_size=8,
         value='0x1')


Properties of a Member Field
----------------------------

You can **access** the :class:`Field` properties of a :ref:`field <field>`
member in a `structure`_ with the property names:

    >>> structure.version.name
    'Byte'
    >>> structure.version.value
    '0x1'
    >>> structure.version.bit_size
    8
    >>> structure.version.alignment
    (1, 0)
    >>> structure.version.alignment[0]
    1
    >>> structure.version.alignment[1]
    0
    >>> structure.version.byte_order
    Byteorder.auto = 'auto'
    >>> structure.version.byte_order.value
    'auto'
    >>> structure.version.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> structure.version.index.address
    0
    >>> structure.version.index.byte
    0
    >>> structure.version.index.bit
    0
    >>> structure.version.index.address
    0
    >>> structure.version.index.base_address
    0
    >>> structure.version.index.update
    False
    >>> structure.version.is_bit()
    False
    >>> structure.version.is_bool()
    False
    >>> structure.version.is_decimal()
    True
    >>> structure.version.is_float()
    False
    >>> structure.version.is_pointer()
    False
    >>> structure.version.is_stream()
    False
    >>> structure.version.is_string()
    False


Iterate over Members
--------------------

You can **iterate** over the member names of a `structure`_.

    >>> [key for key in structure.keys()] # doctest: +NORMALIZE_WHITESPACE
    ['version', 'id', 'length', 'module']

You can **iterate** over all kind of member items of a `structure`_.

    >>> [(key, value.item_type) for key, value in structure.items()] # doctest: +NORMALIZE_WHITESPACE
    [('version', ItemClass.Byte = 42),
     ('id', ItemClass.Unsigned = 45),
     ('length', ItemClass.Decimal = 40),
     ('module', ItemClass.Char = 43)]

You can **iterate** over all kind of members of a `structure`_.

    >>> [value.item_type for value in structure.values()] # doctest: +NORMALIZE_WHITESPACE
    [ItemClass.Byte = 42,
     ItemClass.Unsigned = 45,
     ItemClass.Decimal = 40,
     ItemClass.Char = 43]

You can **iterate** over all :ref:`field <field>` members of a `structure`_.

    >>> [value.name for value in structure.values() if is_field(value)]
    ['Byte', 'Unsigned8', 'Decimal8', 'Char']


List field indexes
------------------

You can list the :class:`Index` of each :ref:`field <field>` of a `structure`_
as a **nested** ordered dictionary by calling the method
:meth:`~Structure.field_indexes`.

    >>> pprint(structure.field_indexes()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('version',
                  Index(byte=0, bit=0, address=0, base_address=0, update=False)),
                 ('id',
                  Index(byte=1, bit=0, address=1, base_address=0, update=False)),
                 ('length',
                  Index(byte=2, bit=0, address=2, base_address=0, update=False)),
                 ('module',
                  Index(byte=3, bit=0, address=3, base_address=0, update=False))])


List field types
----------------

You can list the **types** of each :ref:`field <field>` of a `structure`_
as a **nested** ordered dictionary by calling the method
:meth:`~Structure.field_types`.

    >>> pprint(structure.field_types()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('version', 'Byte'),
                 ('id', 'Unsigned8'),
                 ('length', 'Decimal8'),
                 ('module', 'Char')])


List field values
-----------------

You can list the **values** of each :ref:`field <field>` of a `structure`_
as a **nested** ordered dictionary by calling the method
:meth:`~Structure.field_values`.

    >>> pprint(structure.field_values()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('version', '0x1'),
                 ('id', '0x2'),
                 ('length', 9),
                 ('module', 'F')])


List field items
----------------

You can list all :ref:`field <field>` items of a `structure`_
as a **flat** list by calling the method :meth:`~Structure.field_items`.

    >>> pprint(structure.field_items()) # doctest: +NORMALIZE_WHITESPACE
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

View field values
-----------------

You can **view** the *values* of each :ref:`field <field>` of a `structure`_
as a **flat** list by calling the method :meth:`~Container.to_list`.

    >>> pprint(structure.to_list()) # doctest: +NORMALIZE_WHITESPACE
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *values* of each :ref:`field <field>` of a `structure`_
as a **flat** ordered dictionary by calling the method
:meth:`~Container.to_dict`.

    >>> pprint(structure.to_dict()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Structure',
                  OrderedDict([('version', '0x1'),
                               ('id', '0x2'),
                               ('length', 9),
                               ('module', 'F')]))])

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


Save field values
-----------------

You can **save** the *values* of each :ref:`field <field>` of a `structure`_
to an INI file by calling the method :meth:`~Container.save`.

    >>> structure.save("_static/structure.ini")

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


Load field values
-----------------

You can **load** the *values* of each :ref:`field <field>` of a `structure`_
from an INI file by calling the method :meth:`~Container.load`.

    >>> structure.load("_static/structure.ini")
    [Structure]
    Structure.version = 0x1
    Structure.id = 0x2
    Structure.length = 9
    Structure.module = F

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.
