.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *

.. _array_template:

Array template
==============

KonFoo has a :class:`Array` class to declare ...



.. _array_element:

Array element
-------------

A :class:`Array` element can be any :class:`Field` or :class:`Container` class.


Define a template
-----------------

Define a array in a template by calling the array element constructor.

.. code-block:: python

    # Template
    class EntryList(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal32()
            self.entry = Array(Decimal32, 5)  # Array


Define a array in a template by using a array element instance.

.. code-block:: python

    # Template
    class List(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal32()
            self.entry = Array(Decimal32(), 5) # Array


Define a array in a template by calling a factory class or function.

.. code-block:: python

    # Factory for the array element template
    class Factory:
        def __init__(self, size):
            self.size = size

        def __call__(self):
            return String(size)

.. code-block:: python

    # Template
    class List(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal32()
            self.entry = Array(Factory(10), 5)  # Array


List field indexes
------------------

You can list the :class:`Index` of each :class:`Field` in the template as a
**nested** ordered dictionary by calling the method
:meth:`~Sequence.field_indexes`.

    >>> pprint(array.field_indexes())
    {}


List field types
----------------

You can list the **types** of each :class:`Field` in the template as a
**nested** ordered dictionary by calling the method
:meth:`~Sequence.field_types`.

    >>> pprint(array.field_types())
    {}


List field values
-----------------

You can list the **values** of each :class:`Field` in the template as a
**nested** ordered dictionary by calling the method
:meth:`~Sequence.field_values`.


    >>> pprint(array.field_values())
    {}


List field items
----------------

You can list all :class:`Field` items in the template as a **flat** list
by calling the method :meth:`~Sequence.field_items`.

    >>> pprint(array.field_items()) # doctest: +NORMALIZE_WHITESPACE
    []


View field values
-----------------

You can **view** the *values* of each :class:`Field` in the template as a
**flat** list by calling the method :meth:`~Container.to_list`.

    >>> pprint(array.to_list())
    []

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *values* of each :class:`Field` in the template as a
**flat** ordered dictionary by calling the method :meth:`~Container.to_dict`.

    >>> pprint(array.to_dict())
    {'Array': [] }

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


Save field values
-----------------

You can **save** the *values* of each :class:`Field` in the template to an
INI file by calling the method :meth:`~Container.save`.

    >>> array.save("_static/array.ini", nested=True)

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


Load field values
-----------------

You can **load** the *values* of each :class:`Field` in the template from an
INI file by calling the method :meth:`~Container.load`.

    >>> array.load("_static/array.ini", nested=True)
    [Array]


.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.
