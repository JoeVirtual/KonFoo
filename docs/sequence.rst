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
the members are decoded and encoded by the built-in decoding and encoding engine.


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

    >>> sequence = Sequence()
    >>> sequence # doctest: +NORMALIZE_WHITESPACE
    []


Blueprint of a Sequence
-----------------------

You can get the blueprint of the `sequence`_ by calling the method
:meth:`~Sequence.blueprint`.

    >>> pprint(sequence.blueprint()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('class', 'Sequence'),
                 ('name', 'Sequence'),
                 ('size', 0),
                 ('type', 'Sequence'),
                 ('member', [])])


Length of a Sequence
--------------------

You can get the **length** of a `sequence`_ as a tuple in the form of
``(number of bytes, remaining bits)`` by calling the method
:meth:`~Sequence.field_length`.

    >>> sequence.field_length()
    (0, 0)

.. note::

   The remaining bits must be always zero or the `sequence`_ declaration is
   incomplete.


Indexing
--------

You can get the *byte stream* :class:`Index` after the last :ref:`field <field>`
in a `sequence`_ by calling the method :meth:`~Sequence.next_index`.

    >>> sequence.next_index()
    Index(byte=0, bit=0, address=0, base_address=0, update=False)

.. note::

    The method re-indexes all members in the `sequence`_ as well.


Iterate over a Sequence
-----------------------

You can **iterate** over a `sequence`_.




List field indexes
------------------

You can list the :class:`Index` of each :ref:`field <field>` in a `sequence`_
as a **nested** list by calling the method :meth:`~Sequence.field_indexes`.

    >>> pprint(sequence.field_indexes()) # doctest: +NORMALIZE_WHITESPACE
    []


List field types
----------------

You can list the **types** of each :ref:`field <field>` in a `sequence`_
as a **nested** list by calling the method :meth:`~Sequence.field_types`.

    >>> pprint(sequence.field_types()) # doctest: +NORMALIZE_WHITESPACE
    []


List field values
-----------------

You can list the **values** of each :ref:`field <field>` in a `sequence`_
as a **nested** list by calling the method :meth:`~Sequence.field_values`.


    >>> pprint(sequence.field_values())
    []


List field items
----------------

You can list all :ref:`field <field>` items in a `sequence`_
as a **flat** list by calling the method :meth:`~Sequence.field_items`.

    >>> pprint(sequence.field_items()) # doctest: +NORMALIZE_WHITESPACE
    []


View field values
-----------------

You can **view** the *values* of each :ref:`field <field>` in a `sequence`_
as a **flat** list by calling the method :meth:`~Container.to_list`.

    >>> pprint(sequence.to_list()) # doctest: +NORMALIZE_WHITESPACE
    []

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *values* of each :ref:`field <field>` in a `sequence`_
as a **flat** ordered dictionary by calling the method
:meth:`~Container.to_dict`.

    >>> pprint(sequence.to_dict()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Sequence', OrderedDict())])

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


Save field values
-----------------

You can **save** the *values* of each :ref:`field <field>` in a `sequence`_
to an INI file by calling the method :meth:`~Container.save`.

    >>> sequence.save("_static/sequence.ini", nested=True)

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


Load field values
-----------------

You can **load** the *values* of each :ref:`field <field>` in a `sequence`_
from an INI file by calling the method :meth:`~Container.load`.

    >>> sequence.load("_static/sequence.ini", nested=True)
    [Sequence]


.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.
