.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
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


Append a Member
---------------


    >>> sequence = Sequence()
    >>> sequence.append(Byte())
    >>> sequence  # doctest: +NORMALIZE_WHITESPACE
    [Byte(index=Index(byte=0, bit=0,
                      address=0, base_address=0,
                      update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0')]


Insert a Member
---------------

    >>> sequence.insert(0, Decimal16())
    >>> sequence  # doctest: +NORMALIZE_WHITESPACE
    [Decimal16(index=Index(byte=0, bit=0,
                           address=0, base_address=0,
                           update=False),
               alignment=(2, 0),
               bit_size=16,
               value=0),
     Byte(index=Index(byte=0, bit=0,
                      address=0, base_address=0,
                      update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0')]

Extend a Sequence
-----------------

    >>> sequence.extend([Signed8(), Scaled8(1.0)])
    >>> sequence  # doctest: +NORMALIZE_WHITESPACE
    [Decimal16(index=Index(byte=0, bit=0,
                           address=0, base_address=0,
                           update=False),
               alignment=(2, 0),
               bit_size=16,
               value=0),
     Byte(index=Index(byte=0, bit=0,
                      address=0, base_address=0,
                      update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0'),
     Signed8(index=Index(byte=0, bit=0,
                         address=0, base_address=0,
                         update=False),
             alignment=(1, 0),
             bit_size=8,
             value=0),
     Scaled8(index=Index(byte=0, bit=0,
                         address=0, base_address=0,
                         update=False),
             alignment=(1, 0),
             bit_size=8,
             value=0.0)]

View a Sequence
---------------

You can **view** the `sequence`_

    >>> sequence = Sequence(Byte())
    >>> sequence # doctest: +NORMALIZE_WHITESPACE
    [Byte(index=Index(byte=0, bit=0,
                      address=0, base_address=0,
                      update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0')]



Metadata of a Sequence
-----------------------

You can get the metadata of the `sequence`_ by calling the method
:meth:`~Sequence.describe`.

    >>> pprint(sequence.describe()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('class', 'Sequence'),
                 ('name', 'Sequence'),
                 ('size', 1),
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
                                ('value', '0x0')])])])


Size of a Sequence
------------------

You can get the **size** of a `sequence`_ as a tuple in the form of
``(number of bytes, number of remaining bits)`` by calling the method
:meth:`~Sequence.container_size`.

    >>> sequence.container_size()
    (1, 0)

.. note::
    The number of remaining bits must be always zero or the `sequence`_
    declaration is incomplete.


Indexing
--------

You can index all fields in a `sequence`_ by calling the method
:meth:`~Sequence.index_fields`.
The :class:`Index` after the last :ref:`field <field>` of the `sequence`_ is
returned.

    >>> sequence.index_fields(index=Index())
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> sequence.index_fields()
    Index(byte=1, bit=0, address=1, base_address=0, update=False)


Iterate over a Sequence
-----------------------

You can **iterate** over a `sequence`_.



View Field Attributes
---------------------

You can view the **attributes** of each :ref:`field <field>` in a `sequence`_
as a **nested** list by calling the method :meth:`~Sequence.view_fields`.

    >>> # View the field values
    >>> pprint(sequence.view_fields())
    ['0x0']
    >>> # View the field name and value pairs
    >>> pprint(sequence.view_fields('name', 'value'))
    [('Byte', '0x0')]
    >>> # View the field indexes
    >>> pprint(sequence.view_fields('index'))
    [Index(byte=0, bit=0, address=0, base_address=0, update=False)]



List Field Items
----------------

You can list all :ref:`field <field>` items in a `sequence`_
as a **flat** list by calling the method :meth:`~Sequence.field_items`.

    >>> pprint(sequence.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('.[0]',
      Byte(index=Index(byte=0, bit=0,
                       address=0, base_address=0,
                       update=False),
           alignment=(1, 0),
           bit_size=8,
           value='0x0'))]


View Field Values
-----------------

You can **view** the *value* of each :ref:`field <field>` in a `sequence`_
as a **flat** list by calling the method :meth:`~Container.to_list`.

    >>> pprint(sequence.to_list()) # doctest: +NORMALIZE_WHITESPACE
    [('Sequence..[0]', '0x0')]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *value* of each :ref:`field <field>` in a `sequence`_
as a **flat** ordered dictionary by calling the method
:meth:`~Container.to_dict`.

    >>> pprint(sequence.to_dict()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Sequence', OrderedDict([('.[0]', '0x0')]))])

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Save Field Values
-----------------

You can **save** the *value* of each :ref:`field <field>` in a `sequence`_
to an ``.ini`` file by calling the method :meth:`~Container.save`.

    >>> sequence.save("_static/sequence.ini", nested=True)

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.


Load Field Values
-----------------

You can **load** the *value* of each :ref:`field <field>` in a `sequence`_
from an ``.ini`` file by calling the method :meth:`~Container.load`.

    >>> sequence.load("_static/sequence.ini", nested=True)
    [Sequence]
    Sequence..[0] = 0x0

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.
