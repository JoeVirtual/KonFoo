.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from binascii import hexlify
    from konfoo import *

.. _structure_template:

Structure template
==================

KonFoo ships with a :class:`Structure` class and many :class:`Field` classes to
declare the mapping part of a *byte stream mapper*. The order how you declare the
fields in the :class:`Structure` defines the order how the fields are decoded and
encoded by the built-in decoding and encoding engine.

Define a Structure
------------------

You can define the :ref:`members <template_member>` of a :class:`Structure`
by adding them in the constructor method of the :class:`Structure` class.

.. code-block:: python

    # Structure template
    class Identifier(Structure):

        def __init__(self):
            super().__init__()        # <- NEVER forget to call it first!
            self.version = Byte()     # 1st field
            self.id = Unsigned8()     # 2nd field
            self.length = Decimal8()  # 3rd field
            self.module = Char()      # 4th field
            self.next_index()         # <- Indexes all fields (optional)

.. warning::

    A **structure template** must always align to full bytes or an exception
    will be raised when decoding or encoding an incomplete template declaration.


Align fields in a Structure
---------------------------

You can :ref:`align <field_alignment>` consecutive fields in a :class:`Structure`
to each other by using the ``align_to`` parameter of the :class:`Field` class.

.. code-block:: python
   :emphasize-lines: 6-9

    # Structure template
    class Identifier(Structure):

        def __init__(self):
            super().__init__()
            self.version = Byte(4)       # 1st field aligned to 4 bytes
            self.id = Unsigned(8, 4)     # 2nd field aligned to 4 bytes
            self.length = Decimal(8, 4)  # 3rd field aligned to 4 bytes
            self.module = Char(4)        # 4th field aligned to 4 bytes
            self.next_index()


Re-use a template
-----------------

You can re-use a template in other templates.

.. code-block:: python
    :emphasize-lines: 6

    # Structure template
    class Header(Structure):

        def __init__(self):
            super().__init__()
            self.type = Identifier()  # re-used template
            self.size = Decimal32()
            self.next_index()


Parametrize a template
----------------------

You can define a template with arguments.

.. code-block:: python
    :emphasize-lines: 6

    >>> # Template with arguments
    >>> class Parametrized(Structure):
    ...     def __init__(self, arg, *args, **kwargs):
    ...         super().__init__()
    ...         self.field = arg
    >>> structure = Parametrized(Byte)
    >>> structure = Parametrized(Byte())
    >>> structure # doctest: +NORMALIZE_WHITESPACE
    Parametrized([('field',
                    Byte(index=Index(byte=0, bit=0,
                                     address=0, base_address=0,
                                     update=False),
                         alignment=(1, 0),
                         bit_size=8,
                         value='0x0'))])

Factorize a template
--------------------

You can factorize a template by defining a **factory** class or function to
instantiate a template with parameters. This is necessary when you use a
template with arguments for a :ref:`array element <array_element>` template,
in this case you assign the class constructor of the **factory** or the
**factory** function as the :ref:`array element <array_element>` template
instead of the class constructor of the template.

    >>> class Parametrized(Structure):
    ...     def __init__(self, arg, *args, **kwargs):
    ...         super().__init__()
    ...         self.field = arg
    >>> class Factory:
    ...     def __init__(self, arg, *args, **kwargs):
    ...         self.arg = arg
    ...         self.args = args
    ...         self.kwargs = kwargs
    ...
    ...     def __call__(self):
    ...         return Parametrized(self.arg, *self.args, **self.kwargs)
    >>> factory = Factory(Byte)
    >>> factory.arg  # doctest: +NORMALIZE_WHITESPACE
    <class 'konfoo.core.Byte'>
    >>> factory.args
    ()
    >>> factory.kwargs
    {}
    >>> factory() # doctest: +NORMALIZE_WHITESPACE
    Parametrized([('field',
                    Byte(index=Index(byte=0, bit=0,
                                     address=0, base_address=0,
                                     update=False),
                    alignment=(1, 0),
                    bit_size=8,
                    value='0x0'))])
    >>> array = Array(Factory(Byte), 2)
    >>> [item.field.value for item in array]
    ['0x0', '0x0']
    >>> array[0].field.value = 16
    >>> [item.field.value for item in array]
    ['0x10', '0x0']


.. warning::

    If a factory argument is an **instance** of a :class:`Field` or
    :class:`Container` class this **instance** will be assigned to more than
    one :ref:`array element <array_element>`. To avoid this behavior assign
    the class constructor to the argument instead of an instance.


Declare a template on the fly
-----------------------------

You can **declare** a template on the fly.

    >>> structure = Structure()
    >>> structure.version = Byte()
    >>> structure.id = Unsigned8()
    >>> structure.length = Decimal8()
    >>> structure.module = Char()
    >>> structure.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pprint(structure.field_indexes())
    {'version': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'id': Index(byte=1, bit=0, address=1, base_address=0, update=False),
     'length': Index(byte=2, bit=0, address=2, base_address=0, update=False),
     'module': Index(byte=3, bit=0, address=3, base_address=0, update=False)}

You can **nest** templates on the fly.

    >>> structure = Structure()
    >>> structure.type = Structure()
    >>> structure.type.version = Byte()
    >>> structure.type.id = Unsigned8()
    >>> structure.type.length = Decimal8()
    >>> structure.type.module = Char()
    >>> structure.size = Decimal32()
    >>> pprint(structure.to_list())
    [('Structure.type.version', '0x0'),
     ('Structure.type.id', '0x0'),
     ('Structure.type.length', 0),
     ('Structure.type.module', '\x00'),
     ('Structure.size', 0)]


You can declare a template with :ref:`aligned <field_alignment>` fields
on the fly.

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


You can **re-use** a declared template on the fly in other templates on the fly.

    >>> reuse = Structure()
    >>> reuse.type = structure  # re-used template
    >>> reuse.size = Decimal32()
    >>> pprint(reuse.to_list())
    [('Structure.type.version', '0x0'),
     ('Structure.type.id', '0x0'),
     ('Structure.type.length', 0),
     ('Structure.type.module', '\x00'),
     ('Structure.size', 0)]


View a template
---------------

You can **view** a template with

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

Blueprint of a template
-----------------------

You can get the :ref:`blueprint <blueprint>` of a template by calling the
method :meth:`~Structure.blueprint`.

    >>> pprint(structure.blueprint())
    {'class': 'Structure',
     'name': 'Structure',
     'size': 4,
     'type': 'Structure',
     'member': [{'address': 0,
                 'alignment': [1, 0],
                 'class': 'Byte',
                 'index': [0, 0],
                 'max': 255,
                 'min': 0,
                 'name': 'version',
                 'order': 'auto',
                 'signed': False,
                 'size': 8,
                 'type': 'Field',
                 'value': '0x0'},
                {'address': 0,
                 'alignment': [1, 0],
                 'class': 'Unsigned8',
                 'index': [0, 0],
                 'max': 255,
                 'min': 0,
                 'name': 'id',
                 'order': 'auto',
                 'signed': False,
                 'size': 8,
                 'type': 'Field',
                 'value': '0x0'},
                {'address': 0,
                 'alignment': [1, 0],
                 'class': 'Decimal8',
                 'index': [0, 0],
                 'max': 255,
                 'min': 0,
                 'name': 'length',
                 'order': 'auto',
                 'signed': False,
                 'size': 8,
                 'type': 'Field',
                 'value': 0},
                {'address': 0,
                 'alignment': [1, 0],
                 'class': 'Char',
                 'index': [0, 0],
                 'max': 255,
                 'min': 0,
                 'name': 'module',
                 'order': 'auto',
                 'signed': False,
                 'size': 8,
                 'type': 'Field',
                 'value': '\x00'}]}


Length of a template
--------------------

You can get the **length** of the template as a tuple in the form of
``(number of bytes, remaining bits)`` by calling the method
:meth:`~Structure.field_length`.

    >>> structure.field_length()
    (4, 0)

.. note::

   The remaining bits must be always zero or the template declaration is
   incomplete.


Indexing
--------

You can get the byte stream :class:`Index` after the last :class:`Field`
of the template by calling the method :meth:`~Structure.next_index`.

    >>> structure.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)

.. note::

    The method re-indexes all fields in the template as well.


Decoding
--------

You can **decode** a byte stream with a template by calling the method
:meth:`~Structure.decode`.

    >>> bytestream = bytes.fromhex('01020946f00f00')
    >>> structure.decode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)


Encoding
--------

You can **encode** a byte stream with a template by calling the method
:meth:`~Structure.encode`.

    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> structure.encode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'01020946'


Accessing a member
------------------

You can **access** a :ref:`member <template_member>` in a template with its
name.

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

You can **access** the :class:`Field` properties of a :ref:`member
<template_member>` in a template with the property names.

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


Iterating over members
----------------------

You can **iterate** over the :ref:`member <template_member>` names
of a template.

    >>> [key for key in structure.keys()]
    ['version', 'id', 'length', 'module']

You can **iterate** over all kind of :ref:`member <template_member>` items
of a template.

    >>> pprint([(key, value.item_type) for key, value in structure.items()])
    [('version', ItemClass.Byte = 42),
     ('id', ItemClass.Unsigned = 45),
     ('length', ItemClass.Decimal = 40),
     ('module', ItemClass.Char = 43)]

You can **iterate** over all :ref:`members <template_member>`
of a template.

    >>> pprint([value.item_type for value in structure.values()])
    [ItemClass.Byte = 42,
     ItemClass.Unsigned = 45,
     ItemClass.Decimal = 40,
     ItemClass.Char = 43]

You can **iterate** over :class:`Field` members of a template.

    >>> [value.name for value in structure.values() if is_field(value)]
    ['Byte', 'Unsigned8', 'Decimal8', 'Char']



List fields
-----------

You can list all :class:`Field` items in the template as a **flat** list
by calling the method :meth:`~Structure.field_items`.

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


List field indexes
------------------

You can list the :class:`Index` of each :class:`Field` in the template as a
**nested** ordered dictionary by calling the method
:meth:`~Structure.field_indexes`.

    >>> pprint(structure.field_indexes())
    {'version': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'id': Index(byte=1, bit=0, address=1, base_address=0, update=False),
     'length': Index(byte=2, bit=0, address=2, base_address=0, update=False),
     'module': Index(byte=3, bit=0, address=3, base_address=0, update=False)}


List field types
----------------

You can list the **types** of each :class:`Field` in the template as a
**nested** ordered dictionary by calling the method
:meth:`~Structure.field_types`.

    >>> pprint(structure.field_types())
    {'version': 'Byte',
     'id': 'Unsigned8',
     'length': 'Decimal8',
     'module': 'Char'}


List field values
-----------------

You can list the **values** of each :class:`Field` in the template as a
**nested** ordered dictionary by calling the method
:meth:`~Structure.field_values`.

    >>> pprint(structure.field_values())
    {'version': '0x1',
     'id': '0x2',
     'length': 9,
     'module': 'F'}


You can list the **values** of each :class:`Field` in the template as a
**flat** list by calling the method :meth:`~Container.to_list`.

    >>> pprint(structure.to_list())
    [('Structure.version', '0x1'),
     ('Structure.id', '0x2'),
     ('Structure.length', 9),
     ('Structure.module', 'F')]

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


You can list the **values** of each :class:`Field` in the template as a
**flat** ordered dictionary by calling the method :meth:`~Container.to_dict`.

    >>> pprint(structure.to_dict())
    {'Structure': {'version': '0x1',
                   'id': '0x2',
                   'length': 9,
                   'module': 'F'}}

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


Save field values
-----------------

You can **save** the values of each :class:`Field` in the template to an
INI file by calling the method :meth:`~Container.save`.

    >>> structure.save("_static/structure.ini")

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


Load field values
-----------------

You can **load** the values of each :class:`Field` in the template from an
INI file by calling the method :meth:`~Container.load`.

    >>> structure.load("_static/structure.ini")
    [Structure]
    Structure.version = 0x1
    Structure.id = 0x2
    Structure.length = 9
    Structure.module = F

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.
