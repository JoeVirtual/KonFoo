.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *

.. _array:

Array
=====

KonFoo has a :class:`Array` class to map a consecutive area of a *byte stream*
with the same kind of `array elements <array element>`_.


.. _array element:

Array element
-------------

A `array element`_ can be any :ref:`field <field>` or :ref:`container <container>`
class **constructor**.


Define a Array
--------------

Define a `array`_ by calling the `array element`_ constructor.

.. code-block:: python
  :emphasize-lines: 4

    class ByteArray(Array):

        def __init__(self, size=0):
            super().__init__(Byte, size)  # Array element constructor


Define a `array`_ by using a `array element`_ instance.

.. code-block:: python
   :emphasize-lines: 4

    class ByteArray(Array):

        def __init__(self, size=0):
            super().__init__(Byte(), size)  # Array element instance

.. note:: Not recommended. It works only for simple :ref:`field <field>` instances.

Define a `array`_ by calling a **factory** class.

.. code-block:: python
   :emphasize-lines: 6-7

    # Factory for the array element
    class StringFactory:
        def __init__(self, size):
            self.size = size

        def __call__(self):
            return String(size)

.. code-block:: python
   :emphasize-lines: 4

    class StringArray(Array):

        def __init__(self, length, size=0):
            super().__init__(StringFactory(length), size)


View a Array
------------

You can **view** the `array`_

    >>> array = Array(Byte)
    >>> array # doctest: +NORMALIZE_WHITESPACE
    []


Blueprint of a Array
--------------------

You can get the blueprint of the `array`_ by calling the method
:meth:`~Sequence.blueprint`.

    >>> pprint(array.blueprint()) # doctest: +NORMALIZE_WHITESPACE
    {'class': 'Array',
     'name': 'Array',
     'size': 0,
     'type': 'Array',
     'member': []}


Length of a Array
-----------------

You can get the **length** of an `array`_ as a tuple in the form of
``(number of bytes, remaining bits)`` by calling the method
:meth:`~Array.field_length`.

    >>> array.field_length()
    (0, 0)

.. note::

   The remaining bits must be always zero or the `array`_ declaration is
   incomplete.


Indexing
--------

You can get the *byte stream* :class:`Index` after the last :ref:`field <field>`
in an `array`_ by calling the method :meth:`~Sequence.next_index`.

    >>> array.next_index()
    Index(byte=0, bit=0, address=0, base_address=0, update=False)

.. note::

    The method re-indexes all members in the `array`_ as well.


List field indexes
------------------

You can list the :class:`Index` of each :ref:`field <field>` in an `array`_
as a **nested** list by calling the method
:meth:`~Sequence.field_indexes`.

    >>> pprint(array.field_indexes()) # doctest: +NORMALIZE_WHITESPACE
    []


List field types
----------------

You can list the **types** of each :ref:`field <field>` in an `array`_
as a **nested** list by calling the method :meth:`~Sequence.field_types`.

    >>> pprint(array.field_types()) # doctest: +NORMALIZE_WHITESPACE
    []


List field values
-----------------

You can list the **values** of each :ref:`field <field>` in an `array`_
as a **nested** list by calling the method :meth:`~Sequence.field_values`.


    >>> pprint(array.field_values())
    []


List field items
----------------

You can list all :ref:`field <field>` items in an `array`_
as a **flat** list by calling the method :meth:`~Sequence.field_items`.

    >>> pprint(array.field_items()) # doctest: +NORMALIZE_WHITESPACE
    []


View field values
-----------------

You can **view** the *values* of each :ref:`field <field>` in an `array`_
as a **flat** list by calling the method :meth:`~Container.to_list`.

    >>> pprint(array.to_list()) # doctest: +NORMALIZE_WHITESPACE
    []

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *values* of each  :ref:`field <field>` in an `array`_
as a **flat** ordered dictionary by calling the method
:meth:`~Container.to_dict`.

    >>> pprint(array.to_dict()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Array', OrderedDict())])

.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


Save field values
-----------------

You can **save** the *values* of each :ref:`field <field>` in an `array`_
to an INI file by calling the method :meth:`~Container.save`.

    >>> array.save("_static/array.ini", nested=True)

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


Load field values
-----------------

You can **load** the *values* of each :ref:`field <field>` in an `array`_
from an INI file by calling the method :meth:`~Container.load`.

    >>> array.load("_static/array.ini", nested=True)
    [Array]


.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.
