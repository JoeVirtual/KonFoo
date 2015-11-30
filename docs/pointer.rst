.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *

.. _pointer_template:

Pointer template
================

KonFoo has a :class:`Pointer` class to reference ...

KonFoo provides the following specialized :class:`Pointer` fields

* a :class:`StructurePointer` field which refers to a
  :class:`Structure` template
* a :class:`SequencePointer` field which refers to a :class:`Sequence`
* a :class:`ArrayPointer` field which refers to a :class:`Array` with
  a template for its :ref:`array element <array_element>`
* a :class:`StreamPointer` field which refers to a :class:`Stream` field
* a :class:`StringPointer` field which refers to a :class:`String` field


KonFoo has also :class:`RelativePointer` class. The only difference to the
:class:`Pointer` class is that the :attr:`~Pointer.data` object is relative
addressed instead of absolute addressed.

KonFoo provides the following specialized :class:`RelativePointer` fields

* a :class:`StructureRelativePointer` field which refers to a
  :class:`Structure` template
* a :class:`SequenceRelativePointer` field which refers to a :class:`Sequence`
* a :class:`ArrayRelativePointer` field which refers to a :class:`Array` with
  a template for its :ref:`array element <array_element>`
* a :class:`StreamRelativePointer` field which refers to a :class:`Stream` field
* a :class:`StringRelativePointer` field which refers to a :class:`String` field


.. _pointer_members:

Members
-------

A `Pointer`


.. _pointer_data_object:

Data object
-----------




Define a template
-----------------

You can define a template for the :attr:`~Pointer.data` object of the
:class:`Pointer` field.

.. code-block:: python

    # Data object template
    class Container(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal32()
            self.item = Pointer()  # No template
            self.next_index()


You can define a specific :class:`Pointer` field for a specific the
:attr:`~Pointer.data` object template.

.. code-block:: python

    # Pointer field
    class ContainerPointer(Pointer):

        def __init__(self, address=None):
            super().__init__(Container(), address)  # Data object template


Nesting
-------

Nesting pointer templates.

.. code-block:: python

    # Data object template
    class Container(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal32()
            self.item = Pointer(Stream())  # Nested template

.. code-block:: python

    # Pointer template
    class ContainerPointer(Pointer):

        def __init__(self, address=None):
            super().__init__(Container(), address)  # Data object template


Declare a template on the fly
-----------------------------

You can declare a data object pointer template on the fly.

    >>> data = Structure()
    >>> data.size = Decimal32()
    >>> data.item = Pointer(Stream())
    >>> pprint(data.to_list(nested=True))
    [('Structure.size', 0),
     ('Structure.item', '0x0'),
     ('Structure.item.data', b'')]

You can declare a template on the fly.

    >>> pointer = Pointer(data)
    >>> pprint(pointer.to_list(nested=True))
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0'),
     ('Pointer.data.item.data', b'')]


View a template
---------------

You can **view** a template with

    >>> pointer # doctest: +NORMALIZE_WHITESPACE
    Pointer(index=Index(byte=0, bit=0,
                        address=0, base_address=0,
                        update=False),
            alignment=(4, 0),
            bit_size=32,
            value='0x0')


You can **view** the :attr:`~Pointer.data` object template of the
:class:`Pointer` field with

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


Blueprint of a template
-----------------------

You can get the :ref:`blueprint <blueprint>` of a template by calling the
method :meth:`~Pointer.blueprint`.

    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'Pointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'Pointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0x0',
     'member': [{'class': 'Structure',
                 'name': 'data',
                 'size': 2,
                 'type': 'Structure',
                 'member': [{'address': 0,
                             'alignment': [4, 0],
                             'class': 'Decimal32',
                             'index': [0, 0],
                             'max': 4294967295,
                             'min': 0,
                             'name': 'size',
                             'order': 'auto',
                             'signed': False,
                             'size': 32,
                             'type': 'Field',
                             'value': 0},
                            {'address': 0,
                             'alignment': [4, 0],
                             'class': 'Pointer',
                             'index': [0, 0],
                             'max': 4294967295,
                             'min': 0,
                             'name': 'item',
                             'order': 'auto',
                             'signed': False,
                             'size': 32,
                             'type': 'Pointer',
                             'value': '0x0',
                             'member': [{'address': 0,
                                         'alignment': [0, 0],
                                         'class': 'Stream',
                                         'index': [0, 0],
                                         'name': 'data',
                                         'order': 'auto',
                                         'size': 0,
                                         'type': 'Field',
                                         'value': ''}]}]}]}


Indexing
--------

You can get the next byte stream :class:`Index` after the :class:`Pointer`
field by calling the method :meth:`~Field.next_index`.


    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)


You can index each :class:`Field` in the :attr:`~Pointer.data` object of the
:class:`Pointer` field by calling the method :meth:`~Pointer.subscript`.

    >>> pointer.subscript()


Accessing a member
------------------

You can **access** the :class:`Field` properties the :class:`Pointer` field
with the property names.

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



You can **access** the properties for the :attr:`~Pointer.data` object of the
:class:`Pointer` field

    >>> pointer.address
    0
    >>> pointer.base_address
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.order.value
    'little'
    >>> pointer.size
    8
    >>> pointer.bytestream
    b''


You can **access** a :ref:`member <template_member>` of the :attr:`~Pointer.data`
object of the :class:`Pointer` field with its name.

    >>> pointer.data  # doctest: +NORMALIZE_WHITESPACE
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


List fields
-----------

You can list all :class:`Field` items in the template as a **flat** list
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


List field indexes
------------------

You can list the :class:`Index` of each :class:`Field` in the template as a
**nested** ordered dictionary by calling the method
:meth:`~Pointer.field_indexes`.

    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': {'size': Index(byte=0, bit=0, address=0, base_address=0, update=False),
              'item': Index(byte=4, bit=0, address=4, base_address=0, update=False)}}


List field types
----------------

You can list the **types** of each :class:`Field` in the template as a
**nested** ordered dictionary by calling the method
:meth:`~Pointer.field_types`.

    >>> pprint(pointer.field_types())
    {'value': 'Pointer32',
     'data': OrderedDict([('size', 'Decimal32'), ('item', 'Pointer32')])}


List field values
-----------------

You can list the **values** of each :class:`Field` in the template as a
**nested** ordered dictionary by calling the method
:meth:`~Pointer.field_values`.


    >>> pprint(pointer.field_values())
    {'value': '0x0',
     'data': OrderedDict([('size', 0), ('item', '0x0')])}


You can list the **values** of each :class:`Field` in the template as a
**flat** list by calling the method :meth:`~Container.to_list`.

    >>> pprint(pointer.to_list())
    [('Pointer.value', '0x0'),
     ('Pointer.data.size', 0),
     ('Pointer.data.item', '0x0')]

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


You can list the **values** of each :class:`Field` in the template as a
**flat** ordered dictionary by calling the method :meth:`~Container.to_dict`.

    >>> pprint(pointer.to_dict())
    {'Pointer': {'value': '0x0',
                 'data.size': 0,
                 'data.item': '0x0'}}

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


Save field values
-----------------

You can **save** the values of each :class:`Field` in the template to an
INI file by calling the method :meth:`~Container.save`.

    >>> pointer.save("_static/pointer.ini", nested=True)

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


Load field values
-----------------

You can **load** the values of each :class:`Field` in the template from an
INI file by calling the method :meth:`~Container.load`.

    >>> pointer.load("_static/pointer.ini", nested=True)
    [Pointer]
    Pointer.value = 0x0
    Pointer.data.size = 0
    Pointer.data.item = 0x0
    Pointer.data.item.data = b''

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.
