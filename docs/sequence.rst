.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *


.. _sequence_template:

Sequence template
=================

KonFoo has a :class:`Sequence` class to declare ...



Define a template
-----------------



List field indexes
------------------

You can list the :class:`Index` of each :class:`Field` in the template as a
**nested** list by calling the method :meth:`~Sequence.field_indexes`.

    >>> pprint(sequence.field_indexes())
    []


List field types
----------------

You can list the **types** of each :class:`Field` in the template as a
**nested** ordered dictionary by calling the method
:meth:`~Sequence.field_types`.

    >>> pprint(sequence.field_types())
    {}


List field values
-----------------

You can list the **values** of each :class:`Field` in the template as a
**nested** ordered dictionary by calling the method
:meth:`~Sequence.field_values`.


    >>> pprint(sequence.field_values())
    []


List field items
----------------

You can list all :class:`Field` items in the template as a **flat** list
by calling the method :meth:`~Sequence.field_items`.

    >>> pprint(sequence.field_items()) # doctest: +NORMALIZE_WHITESPACE
    []


View field values
-----------------

You can **view** the *values* of each :class:`Field` in the template as a
**flat** list by calling the method :meth:`~Container.to_list`.

    >>> pprint(sequence.to_list())
    []

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *values* of each :class:`Field` in the template as a
**flat** ordered dictionary by calling the method :meth:`~Container.to_dict`.

    >>> pprint(sequence.to_dict())
    {'Sequence': []}

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


Save field values
-----------------

You can **save** the *values* of each :class:`Field` in the template to an
INI file by calling the method :meth:`~Container.save`.

    >>> sequence.save("_static/sequence.ini", nested=True)

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


Load field values
-----------------

You can **load** the *values* of each :class:`Field` in the template from an
INI file by calling the method :meth:`~Container.load`.

    >>> sequence.load("_static/sequence.ini", nested=True)
    [Sequence]


.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.
