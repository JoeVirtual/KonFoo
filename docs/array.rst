.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *

.. _array:

Array
=====

KonFoo has an :class:`Array` class to map a consecutive area of a *byte stream*
with the same kind of :ref:`array elements <array element>`.


.. _array element:

Array element
-------------

An `array element`_ can be any :ref:`field <field>` or :ref:`container <container>`
class **constructor**.


Define an Array
---------------

Define an `array`_ by calling the `array element`_ constructor.

.. code-block:: python
  :emphasize-lines: 4

    class ByteArray(Array):

        def __init__(self, size=0):
            super().__init__(Byte, size)  # Array element constructor


Define an `array`_ by using an `array element`_ instance.

.. code-block:: python
   :emphasize-lines: 4

    class ByteArray(Array):

        def __init__(self, size=0):
            super().__init__(Byte(), size)  # Array element instance

.. note:: Not recommended. It works only for simple :ref:`field <field>` instances.

Define an `array`_ by calling a **factory** class.

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


Factorizing an Array element
----------------------------

You can factorize an `array element`_ by defining a **factory** class to instantiate
an `array element`_ with parameters. A **factory** is necessary whenever you use a
:ref:`mapper <mapper>` with arguments for an `array element`_, in this case you must
assign the constructor of the **factory** class as the `array element`_.

.. code-block:: python
    :emphasize-lines: 11-13, 28

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
    >>> array = Array(Factory(Byte), 2)  # assign the class constructor not an instance!
    >>> [item.field.value for item in array]
    ['0x0', '0x0']
    >>> array[0].field.value = 16
    >>> [item.field.value for item in array]
    ['0x10', '0x0']


.. warning::

    If a factory argument is an **instance** of a :ref:`field <field>` or
    :ref:`container <container>` class this **instance** will be assigned to
    more than one `array element`_. To avoid this behavior assign the class
    constructor to the argument instead of an instance.

View an Array
-------------

You can **view** the `array`_

    >>> array = Array(Byte, 1)
    >>> array # doctest: +NORMALIZE_WHITESPACE
    [Byte(index=Index(byte=0, bit=0,
                      address=0, base_address=0,
                      update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0')]


Metadata of an Array
---------------------

You can get the metadata of the `array`_ by calling the method
:meth:`~Sequence.describe`.

    >>> pprint(array.describe()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('class', 'Array'),
                 ('name', 'Array'),
                 ('size', 1),
                 ('type', 'Array'),
                 ('member',
                  [OrderedDict([('address', 0),
                                ('alignment', [1, 0]),
                                ('class', 'Byte'),
                                ('index', [0, 0]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'Array[0]'),
                                ('order', 'auto'),
                                ('signed', False),
                                ('size', 8),
                                ('type', 'Field'),
                                ('value', '0x0')])])])


Size of an Array
----------------

You can get the **size** of an `array`_ as a tuple in the form of
``(number of bytes, number of remaining bits)`` by calling the method
:meth:`~Sequence.container_size`.

    >>> array.container_size()
    (1, 0)

.. note::
    The number of remaining bits must be always zero or the `array`_
    declaration is incomplete.


Indexing
--------

You can index all fields in an `array`_ by calling the method
:meth:`~Sequence.index_fields`.
The :class:`Index` after the last :ref:`field <field>` of the `array`_ is
returned.

    >>> array.index_fields(index=Index())
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> array.index_fields()
    Index(byte=1, bit=0, address=1, base_address=0, update=False)


View Field Attributes
---------------------

You can view the **attributes** of each :ref:`field <field>` in an `array`_
as a **nested** list by calling the method :meth:`~Sequence.view_fields`.

    >>> # Views the field values
    >>> pprint(array.view_fields())
    ['0x0']
    >>> # Views the field name, value pairs
    >>> pprint(array.view_fields('name', 'value'))
    [('Byte', '0x0')]
    >>> # Views the field indexes
    >>> pprint(array.view_fields('index'))
    [Index(byte=0, bit=0, address=0, base_address=0, update=False)]


List Field Items
----------------

You can list all :ref:`field <field>` items in an `array`_
as a **flat** list by calling the method :meth:`~Sequence.field_items`.

    >>> pprint(array.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('.[0]', Byte(index=Index(byte=0, bit=0,
                               address=0, base_address=0,
                               update=False),
                   alignment=(1, 0),
                   bit_size=8,
                   value='0x0'))]


List Field Values
-----------------

You can **list** the *value* of each :ref:`field <field>` in an `array`_
as a **flat** list by calling the method :meth:`~Container.to_list`.

    >>> pprint(array.to_list()) # doctest: +NORMALIZE_WHITESPACE
    [('Array..[0]', '0x0')]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *value* of each :ref:`field <field>` in an `array`_
as a **flat** ordered dictionary by calling the method
:meth:`~Container.to_dict`.

    >>> pprint(array.to_dict()) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Array', OrderedDict([('.[0]', '0x0')]))])

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Save Field Values
-----------------

You can **save** the *value* of each :ref:`field <field>` in an `array`_
to an ``.ini`` file by calling the method :meth:`~Container.save`.

    >>> array.save("_static/array.ini", nested=True)

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.


Load Field Values
-----------------

You can **load** the *value* of each :ref:`field <field>` in an `array`_
from an ``.ini`` file by calling the method :meth:`~Container.load`.

    >>> array.load("_static/array.ini", nested=True)
    [Array]
    Array..[0] = 0x0


.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.
