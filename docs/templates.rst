.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from binascii import hexlify
    from konfoo import *

.. _template:

Templates
=========


.. _template_member:

Members
-------




.. _container:

Containers
==========

Overview
--------

* :class:`Structure`
* :class:`Sequence`, :class:`Array`
* :class:`Pointer`, :class:`StructurePointer`, :class:`SequencePointer`,
  :class:`ArrayPointer`:class:`StreamPointer`, :class:`StringPointer`,
  :class:`AutoStringPointer`
* :class:`RelativePointer`, :class:`StructureRelativePointer`,
  :class:`SequenceRelativePointer`, :class:`ArrayRelativePointer`,
  :class:`StreamRelativePointer`, :class:`StringRelativePointer`


List field items
----------------

You can list all :class:`Field` items in the template as a **flat** list
by calling the method :meth:`~Container.field_items`.

    >>> pprint(container.field_items()) # doctest: +NORMALIZE_WHITESPACE
    []


View field values
-----------------

You can **view** the *values* of each :class:`Field` in the template as a
**flat** list by calling the method :meth:`~Container.to_list`.

    >>> pprint(container.to_list())
    []

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *values* of each :class:`Field` in the template as a
**flat** ordered dictionary by calling the method :meth:`~Container.to_dict`.

    >>> pprint(container.to_dict())
    {'Container': {}}

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


Save field values
-----------------

You can **save** the *values* of each :class:`Field` in the template to an
INI file by calling the method :meth:`~Container.save`.

    >>> container.save("_static/container.ini")

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


Load field values
-----------------

You can **load** the values of each :class:`Field` in the template from an
INI file by calling the method :meth:`~Container.load`.

    >>> container.load("_static/container.ini")
    [Container]


.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


.. _field:

Fields
======

Overview
--------

* :class:`Stream`, :class:`String`
* :class:`Float`
* :class:`Decimal` :class:`Bit`, :class:`Byte`, :class:`Char`, :class:`Signed`,
  :class:`Unsigned`, :class:`Bitset`, :class:`Bool`, :class:`Enum`, :class:`Scaled`,
  :class:`Fraction`, :class:`Bipolar`, :class:`Unipolar`, :class:`Datetime`
* :class:`Pointer`, :class:`StructurePointer`, :class:`SequencePointer`,
  :class:`ArrayPointer`:class:`StreamPointer`, :class:`StringPointer`,
  :class:`AutoStringPointer`
* :class:`RelativePointer`, :class:`StructureRelativePointer`,
  :class:`SequenceRelativePointer`, :class:`ArrayRelativePointer`,
  :class:`StreamRelativePointer`, :class:`StringRelativePointer`


.. _field_byte_order:

Byte order
----------

Each :class:`Field` defines its own decoding/encoding byte order. The default
byte order of a field is :class:`~Byteorder.auto` this means that the field use
the byte order which the byte stream defines to unpack and pack the required
bytes and bits for its field value from and to the byte stream.


.. _field_alignment:

Alignment
---------

:class:`Fields <Field>` can be aligned to each other ...



.. _enumeration:

Enumerations
============




.. _blueprint:

Blueprints
==========

