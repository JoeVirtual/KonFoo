.. currentmodule:: konfoo

.. testsetup:: *

    import json
    from binascii import hexlify
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

    >>> # Create a array.
    >>> array = Array(Byte, 4)
    >>> # Index the fields in the sequence.
    >>> array.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> array # doctest: +NORMALIZE_WHITESPACE
    [Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0'),
     Byte(index=Index(byte=1, bit=0, address=1, base_address=0, update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0'),
     Byte(index=Index(byte=2, bit=0, address=2, base_address=0, update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0'),
     Byte(index=Index(byte=3, bit=0, address=3, base_address=0, update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0')]


Metadata of an Array
---------------------

You can get the metadata of the `array`_ by calling the method
:meth:`~Sequence.describe`.

    >>> # Get the description of the array.
    >>> array.describe() # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('class', 'Array'),
                 ('name', 'Array'),
                 ('size', 4),
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
                                ('value', '0x0')]),
                  OrderedDict([('address', 1),
                                ('alignment', [1, 0]),
                                ('class', 'Byte'),
                                ('index', [1, 0]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'Array[1]'),
                                ('order', 'auto'),
                                ('signed', False),
                                ('size', 8),
                                ('type', 'Field'),
                                ('value', '0x0')]),
                   OrderedDict([('address', 2),
                                ('alignment', [1, 0]),
                                ('class', 'Byte'),
                                ('index', [2, 0]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'Array[2]'),
                                ('order', 'auto'),
                                ('signed', False),
                                ('size', 8),
                                ('type', 'Field'),
                                ('value', '0x0')]),
                   OrderedDict([('address', 3),
                                ('alignment', [1, 0]),
                                ('class', 'Byte'),
                                ('index', [3, 0]),
                                ('max', 255),
                                ('min', 0),
                                ('name', 'Array[3]'),
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

    >>> # Get the size of the array.
    >>> array.container_size()
    (4, 0)

.. note::
    The number of remaining bits must be always zero or the `array`_
    declaration is incomplete.


Indexing
--------

You can index all fields in an `array`_ by calling the method
:meth:`~Sequence.index_fields`.
The :class:`Index` after the last :ref:`field <field>` of the `array`_ is
returned.

    >>> # Create an array.
    >>> array = Array(Byte, 4)
    >>> # List the field indexes of the array.
    >>> array.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Array[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Array[1]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Array[2]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Array[3]', Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # Index the fields in the array.
    >>> array.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the fields in the array with a start index.
    >>> array.index_fields(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes of the array.
    >>> array.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Array[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Array[1]', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
     ('Array[2]', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Array[3]', Index(byte=3, bit=0, address=3, base_address=0, update=False))]


De-Serializing
--------------

You can **deserialize** a byte stream with an `array`_ by calling the method
:meth:`~Sequence.deserialize`.

    >>> # Create an array.
    >>> array = Array(Byte, 4)
    >>> # Create a byte stream to be deserialized.
    >>> bytestream = bytes.fromhex('0102030405060708')
    >>> # Deserialize the byte stream and map it to the array.
    >>> array.deserialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field values of the array.
    >>> array.to_list('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    [('Array[0]', ('Byte', '0x1')),
     ('Array[1]', ('Byte', '0x2')),
     ('Array[2]', ('Byte', '0x3')),
     ('Array[3]', ('Byte', '0x4'))]


Serializing
-----------

You can **serialize** a byte stream with an `array`_ by calling the method
:meth:`~Sequence.serialize`.

    >>> # Create an empty byte stream.
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> # Serialize the array to the byte stream.
    >>> array.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # View the byte stream.
    >>> hexlify(bytestream)
    b'01020304'


Access a Member
---------------

You can **access** a member in a `array`_ by its index.

    >>> # Access a array member with its index.
    >>> array[0] # doctest: +NORMALIZE_WHITESPACE
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=(1, 0),
         bit_size=8,
         value='0x1')

Attributes of a Member Field
----------------------------

You can **access** the :class:`Field` attributes of a :ref:`field <field>`
member in a `array`_ with the attribute names:

    >>> # Field name.
    >>> array[0].name
    'Byte'
    >>> # Field value.
    >>> array[0].value
    '0x1'
    >>> # Field bit size.
    >>> array[0].bit_size
    8
    >>> # Field alignment.
    >>> array[0].alignment
    (1, 0)
    >>> # Field alignment: byte size.
    >>> array[0].alignment[0]
    1
    >>> # Field alignment: bit offset.
    >>> array[0].alignment[1]
    0
    >>> # Field byte order.
    >>> array[0].byte_order
    Byteorder.auto = 'auto'
    >>> # Field byte order value.
    >>> array[0].byte_order.value
    'auto'
    >>> # Field index.
    >>> array[0].index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> # Field index: byte offset within the byte stream.
    >>> array[0].index.byte
    0
    >>> # Field index: bit offset within the byte stream.
    >>> array[0].index.bit
    0
    >>> # Field index: memory address in the data source.
    >>> array[0].index.address
    0
    >>> # Field index: base address of the byte stream in the data source.
    >>> array[0].index.base_address
    0
    >>> # Field index: update request for the byte stream from the data source.
    >>> array[0].index.update
    False
    >>> # Field is a bit field.
    >>> array[0].is_bit()
    False
    >>> # Field is a boolean field.
    >>> array[0].is_bool()
    False
    >>> # Field is a decimal field.
    >>> array[0].is_decimal()
    True
    >>> # Field is a float field.
    >>> array[0].is_float()
    False
    >>> # Field is a pointer field.
    >>> array[0].is_pointer()
    False
    >>> # Field is a stream field.
    >>> array[0].is_stream()
    False
    >>> # Field is a string field.
    >>> array[0].is_string()
    False


Iterate over Members
--------------------

You can **iterate** over all kind of members of a `array`_.

    >>> [member.item_type for member in array] # doctest: +NORMALIZE_WHITESPACE
    [ItemClass.Byte = 42,
     ItemClass.Byte = 42,
     ItemClass.Byte = 42,
     ItemClass.Byte = 42]


You can **iterate** over all :ref:`field <field>` members of a `array`_.

    >>> [member.value for member in array if is_field(member)]
    ['0x1', '0x2', '0x3', '0x4']


View Field Attributes
---------------------

You can view the **attributes** of each :ref:`field <field>` in an `array`_
as a **nested** list by calling the method :meth:`~Sequence.view_fields`.

    >>> # View the field values.
    >>> array.view_fields()  # doctest: +NORMALIZE_WHITESPACE
    ['0x1', '0x2', '0x3', '0x4']
    >>> # View the field type name, field value pairs.
    >>> array.view_fields('name', 'value')  # doctest: +NORMALIZE_WHITESPACE
    [('Byte', '0x1'),
     ('Byte', '0x2'),
     ('Byte', '0x3'),
     ('Byte', '0x4')]
    >>> # View the field indexes.
    >>> array.view_fields('index') # doctest: +NORMALIZE_WHITESPACE
    [Index(byte=0, bit=0, address=0, base_address=0, update=False),
     Index(byte=1, bit=0, address=1, base_address=0, update=False),
     Index(byte=2, bit=0, address=2, base_address=0, update=False),
     Index(byte=3, bit=0, address=3, base_address=0, update=False)]


List Field Items
----------------

You can list all :ref:`field <field>` items in an `array`_
as a **flat** list by calling the method :meth:`~Sequence.field_items`.

    >>> # List the field items of the array.
    >>> array.field_items() # doctest: +NORMALIZE_WHITESPACE
    [('[0]', Byte(index=Index(byte=0, bit=0,
                              address=0, base_address=0,
                              update=False),
                  alignment=(1, 0),
                  bit_size=8,
                  value='0x1')),
     ('[1]', Byte(index=Index(byte=1, bit=0,
                              address=1, base_address=0,
                              update=False),
                  alignment=(1, 0),
                  bit_size=8,
                  value='0x2')),
     ('[2]', Byte(index=Index(byte=2, bit=0,
                              address=2, base_address=0,
                              update=False),
                  alignment=(1, 0),
                  bit_size=8,
                  value='0x3')),
     ('[3]', Byte(index=Index(byte=3, bit=0,
                              address=3, base_address=0,
                              update=False),
                  alignment=(1, 0),
                  bit_size=8,
                  value='0x4'))]


List Field Values
-----------------

You can **list** the *value* of each :ref:`field <field>` in an `array`_
as a **flat** list by calling the method :meth:`~Container.to_list`.

    >>> # List the field values of the array.
    >>> array.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Array[0]', '0x1'),
     ('Array[1]', '0x2'),
     ('Array[2]', '0x3'),
     ('Array[3]', '0x4')]
    >>> # List the field type names & field values of the array.
    >>> array.to_list('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    [('Array[0]', ('Byte', '0x1')),
     ('Array[1]', ('Byte', '0x2')),
     ('Array[2]', ('Byte', '0x3')),
     ('Array[3]', ('Byte', '0x4'))]
    >>> # List the field indexes of the array.
    >>> array.to_list('index') # doctest: +NORMALIZE_WHITESPACE
    [('Array[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Array[1]', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
     ('Array[2]', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Array[3]', Index(byte=3, bit=0, address=3, base_address=0, update=False))]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **view** the *value* of each :ref:`field <field>` in an `array`_
as a **flat** ordered dictionary by calling the method
:meth:`~Container.to_dict`.

    >>> # List the field values of the array.
    >>> array.to_dict() # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Array',
                  OrderedDict([('[0]', '0x1'),
                               ('[1]', '0x2'),
                               ('[2]', '0x3'),
                               ('[3]', '0x4')]))])
    >>> print(json.dumps(array.to_dict(), indent=2)) # doctest: +NORMALIZE_WHITESPACE
    {
      "Array": {
        "[0]": "0x1",
        "[1]": "0x2",
        "[2]": "0x3",
        "[3]": "0x4"
      }
    }
    >>> # List the field type names & field values of the array.
    >>> array.to_dict('name', 'value') # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Array',
                  OrderedDict([('[0]', ('Byte', '0x1')),
                               ('[1]', ('Byte', '0x2')),
                               ('[2]', ('Byte', '0x3')),
                               ('[3]', ('Byte', '0x4'))]))])
    >>> # List the field indexes of the array.
    >>> array.to_dict('index') # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Array',
                  OrderedDict([('[0]', Index(byte=0, bit=0,
                                             address=0, base_address=0,
                                             update=False)),
                               ('[1]', Index(byte=1, bit=0,
                                             address=1, base_address=0,
                                             update=False)),
                               ('[2]', Index(byte=2, bit=0,
                                             address=2, base_address=0,
                                             update=False)),
                               ('[3]', Index(byte=3, bit=0,
                                             address=3, base_address=0,
                                             update=False))]))])

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Save Field Values
-----------------

You can **save** the *value* of each :ref:`field <field>` in an `array`_
to an ``.ini`` file by calling the method :meth:`~Container.save`.

    >>> # List the field values of the array.
    >>> array.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Array[0]', '0x1'),
     ('Array[1]', '0x2'),
     ('Array[2]', '0x3'),
     ('Array[3]', '0x4')]
    >>> # Save the field values to an '.ini' file.
    >>> array.save("_static/array.ini", nested=True)


The generated ``.ini`` file for the array looks like this:

.. literalinclude:: _static/array.ini
    :language: ini

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.


Load Field Values
-----------------

You can **load** the *value* of each :ref:`field <field>` in an `array`_
from an ``.ini`` file by calling the method :meth:`~Container.load`.

    >>> # Create an array.
    >>> array = Array(Byte, 4)
    >>> # Load the field values from an '.ini' file.
    >>> array.load("_static/array.ini", nested=True)
    [Array]
    Array[0] = 0x1
    Array[1] = 0x2
    Array[2] = 0x3
    Array[3] = 0x4
    >>> # List the field values of the array.
    >>> array.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Array[0]', '0x1'),
     ('Array[1]', '0x2'),
     ('Array[2]', '0x3'),
     ('Array[3]', '0x4')]

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.
