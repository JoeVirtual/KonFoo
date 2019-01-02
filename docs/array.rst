.. currentmodule:: konfoo

.. testsetup:: *

    import copy
    import json
    import sys
    from konfoo import *

.. _array:

Array
=====

KonFoo has an :class:`Array` class to map a consecutive area of a *byte stream*
with the same kind of :ref:`array elements <array element>` (member).


.. _array element:

Array Element
-------------

An `array element`_ (member) can be any :ref:`field <field>` or
:ref:`container <container>` **class**.


Define an Array
---------------

Define an `array`_ by using a **class** as the `array element`_ *template*.

    >>> class ByteArray(Array):
    ...
    ...     def __init__(self, capacity=0):
    ...         # Array element class.
    ...         super().__init__(template=Byte, capacity=capacity)
    >>> # Create an instance of the array.
    >>> array = ByteArray(4)
    >>> # List the field values of the array.
    >>> array.to_list()
    [('ByteArray[0]', '0x0'),
     ('ByteArray[1]', '0x0'),
     ('ByteArray[2]', '0x0'),
     ('ByteArray[3]', '0x0')]
    >>> # List the field values of the array as a CSV list.
    >>> array.to_csv()
    [{'id': 'ByteArray[0]', 'value': '0x0'},
     {'id': 'ByteArray[1]', 'value': '0x0'},
     {'id': 'ByteArray[2]', 'value': '0x0'},
     {'id': 'ByteArray[3]', 'value': '0x0'}]
    >>> # View the array field values as a JSON string.
    >>> array.to_json()
    '["0x0", "0x0", "0x0", "0x0"]'


Define an `array`_ by using an **instance** as the `array element`_ *template*.

    >>> class ByteArray(Array):
    ...
    ...     def __init__(self, capacity=0):
    ...         # Array element instance.
    ...         super().__init__(template=Byte(), capacity=capacity)
    >>> # Create an instance of the array.
    >>> array = ByteArray(4)
    >>> # List the field values of the array.
    >>> array.to_list()
    [('ByteArray[0]', '0x0'),
     ('ByteArray[1]', '0x0'),
     ('ByteArray[2]', '0x0'),
     ('ByteArray[3]', '0x0')]
    >>> # List the field values of the array as a CSV list.
    >>> array.to_csv()
    [{'id': 'ByteArray[0]', 'value': '0x0'},
     {'id': 'ByteArray[1]', 'value': '0x0'},
     {'id': 'ByteArray[2]', 'value': '0x0'},
     {'id': 'ByteArray[3]', 'value': '0x0'}]
    >>> # View the array field values as a JSON string.
    >>> array.to_json()
    '["0x0", "0x0", "0x0", "0x0"]'

.. important::
    Only recommended for *primitive* :ref:`field <field>` instances without *nested*
    members.
    For an `array element`_ instance with *nested* members the *nested* members will
    be assigned to all other *array elements* of the `array`_.


Array of Data Object Pointers
-----------------------------

Define an `array`_ of :ref:`pointers <pointer>` by using a concrete data object
pointer **class** for the the attached :ref:`data object <data object>` as the
`array element`_ *template*.

    >>> # Define an data object pointer class.
    >>> class BytePointer(Pointer):
    ...     def __init__(self):
    ...         super().__init__(Byte())
    >>> # Create an instance of the array.
    >>> array = Array(BytePointer, 2)
    >>> # List the field values of the array and nested pointers.
    >>> array.to_list(nested=True)
    [('Array[0]', '0x0'),
     ('Array[0].data', '0x0'),
     ('Array[1]', '0x0'),
     ('Array[1].data', '0x0')]
    >>> # List the field values of the array and nested pointers as a CSV list.
    >>> array.to_csv(nested=True)
    [{'id': 'Array[0]', 'value': '0x0'},
     {'id': 'Array[0].data', 'value': '0x0'},
     {'id': 'Array[1]', 'value': '0x0'},
     {'id': 'Array[1].data', 'value': '0x0'}]
    >>> # View the array and nested pointers field values as a JSON string.
    >>> array.to_json(nested=True)
    '[{"value": "0x0", "data": "0x0"},
      {"value": "0x0", "data": "0x0"}]'
    >>> # Set field value of the pointer of the fist array element.
    >>> array[0].value = 1
    >>> # Set field value of the data object of the fist array element.
    >>> array[0].data.value = 2
    >>> # List the field values of the array and nested pointers.
    >>> array.to_list(nested=True)
    [('Array[0]', '0x1'),
     ('Array[0].data', '0x2'),
     ('Array[1]', '0x0'),
     ('Array[1].data', '0x0')]
    >>> # List the field values of the array and nested pointers as a CSV list.
    >>> array.to_csv(nested=True)
    [{'id': 'Array[0]', 'value': '0x1'},
     {'id': 'Array[0].data', 'value': '0x2'},
     {'id': 'Array[1]', 'value': '0x0'},
     {'id': 'Array[1].data', 'value': '0x0'}]
    >>> # View the array field values as a JSON string.
    >>> array.to_json(nested=True)
    '[{"value": "0x1", "data": "0x2"},
      {"value": "0x0", "data": "0x0"}]'


.. _array element factory:

Array Element Factory
---------------------

An `array element factory`_ is necessary whenever you use an `array element`_ which
needs arguments and/or keywords to be instantiated **and** contains *nested* members,
in this case you must assign an `array element factory`_ as the `array element`_
*template* to the `array`_.

For *primitive* :ref:`field <field>` instances without *nested* members, no factory
is required, because the `array`_ is able to produce complete copies of a *primitive*
:ref:`field <field>` instance.

    >>> # Define an array element factory.
    >>> class FieldPointerFactory:
    ...     """ A factory class to produce a pointer array element to any field. """
    ...
    ...     def __init__(self, template):
    ...         # Data object: field template (instance or class).
    ...         self.template = template
    ...
    ...     def _create_data_object(self):
    ...         """ Produces the data object attached to the pointer. """
    ...         if is_field(self.template):
    ...             # Copy data object instance from instance template
    ...             return copy.copy(self.template)
    ...         elif callable(self.template):
    ...             # Create data object instance from class template
    ...             data_object = self.template()
    ...             if is_field(data_object):
    ...                 return data_object
    ...             else:
    ...                 raise FactoryTypeError(self, self.template, data_object)
    ...         else:
    ...             raise MemberTypeError(self, self.template)
    ...
    ...     def __call__(self):
    ...         """ Produces the array element. """
    ...         return Pointer(self._create_data_object())
    >>> # Create an instance of the array.
    >>> array = Array(FieldPointerFactory(Byte()), 2)
    >>> # List the field values of the array and nested pointers.
    >>> array.to_list(nested=True)
    [('Array[0]', '0x0'),
     ('Array[0].data', '0x0'),
     ('Array[1]', '0x0'),
     ('Array[1].data', '0x0')]
    >>> # List the field values of the array and nested pointers as a CSV list.
    >>> array.to_csv(nested=True)
    [{'id': 'Array[0]', 'value': '0x0'},
     {'id': 'Array[0].data', 'value': '0x0'},
     {'id': 'Array[1]', 'value': '0x0'},
     {'id': 'Array[1].data', 'value': '0x0'}]
    >>> # View the array and nested pointers field values as a JSON string.
    >>> array.to_json(nested=True)
    '[{"value": "0x0", "data": "0x0"},
      {"value": "0x0", "data": "0x0"}]'
    >>> # Set field value of the pointer of the fist array element.
    >>> array[0].value = 1
    >>> # Set field value of the data object of the fist array element.
    >>> array[0].data.value = 2
    >>> # List the field values of the array and nested pointers.
    >>> array.to_list(nested=True)
    [('Array[0]', '0x1'),
     ('Array[0].data', '0x2'),
     ('Array[1]', '0x0'),
     ('Array[1].data', '0x0')]
    >>> # List the field values of the array and nested pointers as a CSV list.
    >>> array.to_csv(nested=True)
    [{'id': 'Array[0]', 'value': '0x1'},
     {'id': 'Array[0].data', 'value': '0x2'},
     {'id': 'Array[1]', 'value': '0x0'},
     {'id': 'Array[1].data', 'value': '0x0'}]
    >>> # View the array and nested pointers field values as a JSON string.
    >>> array.to_json(nested=True)
    '[{"value": "0x1", "data": "0x2"},
      {"value": "0x0", "data": "0x0"}]'


Otherwise by creating an `array`_ using an **instance** with *nested* members as the
`array element`_ *template* assigns the *nested* members of the `array element`_
*template* to all other *array elements* of the `array`_.

    >>> # Create an instance of the array with nested members and without a factory.
    >>> array = Array(Pointer(Byte()), 2)
    >>> # List the field values of the array and nested pointers.
    >>> array.to_list(nested=True)
    [('Array[0]', '0x0'),
     ('Array[0].data', '0x0'),
     ('Array[1]', '0x0'),
     ('Array[1].data', '0x0')]
    >>> # List the field values of the array and nested pointers as a CSV list.
    >>> array.to_csv(nested=True)
    [{'id': 'Array[0]', 'value': '0x0'},
     {'id': 'Array[0].data', 'value': '0x0'},
     {'id': 'Array[1]', 'value': '0x0'},
     {'id': 'Array[1].data', 'value': '0x0'}]
    >>> # View the array and nested pointers field values as a JSON string.
    >>> array.to_json(nested=True)
    '[{"value": "0x0", "data": "0x0"},
      {"value": "0x0", "data": "0x0"}]'
    >>> # Set field value of the pointer of the fist array element.
    >>> array[0].value = 1
    >>> # Set field value of the data object of the fist array element.
    >>> array[0].data.value = 2
    >>> # List the field values of the array and nested pointers.
    >>> array.to_list(nested=True)
    [('Array[0]', '0x1'),
     ('Array[0].data', '0x2'),
     ('Array[1]', '0x0'),
     ('Array[1].data', '0x2')]
    >>> # List the field values of the array and nested pointers as a CSV list.
    >>> array.to_csv(nested=True)
    [{'id': 'Array[0]', 'value': '0x1'},
     {'id': 'Array[0].data', 'value': '0x2'},
     {'id': 'Array[1]', 'value': '0x0'},
     {'id': 'Array[1].data', 'value': '0x2'}]
    >>> # View the array and nested pointers field values as a JSON string.
    >>> array.to_json(nested=True)
    '[{"value": "0x1", "data": "0x2"},
      {"value": "0x0", "data": "0x2"}]'


Create an Array
---------------

You can **create** an `array`_ by assigning an `array element`_ *class* or
`array element factory`_ to the `array`_ and the number of array elements the
`array`_ holds.

    >>> # Create an array with an array element class.
    >>> array = Array(template=Byte, capacity=4)
    >>> array = Array(Byte, 4)
    >>> # List the field values of the array.
    >>> array.to_list()
    [('Array[0]', '0x0'),
     ('Array[1]', '0x0'),
     ('Array[2]', '0x0'),
     ('Array[3]', '0x0')]
    >>> # List the field values of the array as a CSV list.
    >>> array.to_csv()
    [{'id': 'Array[0]', 'value': '0x0'},
     {'id': 'Array[1]', 'value': '0x0'},
     {'id': 'Array[2]', 'value': '0x0'},
     {'id': 'Array[3]', 'value': '0x0'}]
    >>> # View the array field values as a JSON string.
    >>> array.to_json()
    '["0x0", "0x0", "0x0", "0x0"]'


Resize an Array
---------------

You can **resize** an `array`_ by calling :meth:`~Array.resize`.

    >>> # Create an empty array.
    >>> array = Array(Byte)
    >>> # List the field values of the array.
    >>> array.to_list()
    []
    >>> # View the array field values as a JSON string.
    >>> array.to_json()
    '[]'
    >>> # Resize the array.
    >>> array.resize(4)
    >>> # List the field values of the array.
    >>> array.to_list()
    [('Array[0]', '0x0'),
     ('Array[1]', '0x0'),
     ('Array[2]', '0x0'),
     ('Array[3]', '0x0')]
    >>> # List the field values of the array as a CSV list.
    >>> array.to_csv()
    [{'id': 'Array[0]', 'value': '0x0'},
     {'id': 'Array[1]', 'value': '0x0'},
     {'id': 'Array[2]', 'value': '0x0'},
     {'id': 'Array[3]', 'value': '0x0'}]
    >>> # View the array field values as a JSON string.
    >>> array.to_json()
    '["0x0", "0x0", "0x0", "0x0"]'


Initialize an Array
-------------------

You can **initialize** the fields in an `array`_ by calling the method
:meth:`~Array.initialize_fields`.

    >>> # Create an array.
    >>> array = Array(Byte, 4)
    >>> # List the field values of the array.
    >>> array.to_list()
    [('Array[0]', '0x0'),
     ('Array[1]', '0x0'),
     ('Array[2]', '0x0'),
     ('Array[3]', '0x0')]
    >>> # List the field values of the array as a CSV list.
    >>> array.to_csv()
    [{'id': 'Array[0]', 'value': '0x0'},
     {'id': 'Array[1]', 'value': '0x0'},
     {'id': 'Array[2]', 'value': '0x0'},
     {'id': 'Array[3]', 'value': '0x0'}]
    >>> # View the array field values as a JSON string.
    >>> array.to_json()
    '["0x0", "0x0", "0x0", "0x0"]'

    >>> # Initialize the fields of the array with a fill pattern.
    >>> array.initialize_fields([1 ,2])
    >>> # List the field values of the array.
    >>> array.to_list()
    [('Array[0]', '0x1'),
     ('Array[1]', '0x2'),
     ('Array[2]', '0x1'),
     ('Array[3]', '0x2')]
    >>> # List the field values of the array as a CSV list.
    >>> array.to_csv()
    [{'id': 'Array[0]', 'value': '0x1'},
     {'id': 'Array[1]', 'value': '0x2'},
     {'id': 'Array[2]', 'value': '0x1'},
     {'id': 'Array[3]', 'value': '0x2'}]
    >>> # View the array field values as a JSON string.
    >>> array.to_json()
    '["0x1", "0x2", "0x1", "0x2"]'


Display an Array
----------------

You can **display** the `array`_.

    >>> # Create an array.
    >>> array = Array(Byte, 4)
    >>> # Index the fields in the array.
    >>> array.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Display the array.
    >>> array
    [Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=Alignment(byte_size=1, bit_offset=0),
          bit_size=8,
          value='0x0'),
     Byte(index=Index(byte=1, bit=0, address=1, base_address=0, update=False),
          alignment=Alignment(byte_size=1, bit_offset=0),
          bit_size=8,
          value='0x0'),
     Byte(index=Index(byte=2, bit=0, address=2, base_address=0, update=False),
          alignment=Alignment(byte_size=1, bit_offset=0),
          bit_size=8,
          value='0x0'),
     Byte(index=Index(byte=3, bit=0, address=3, base_address=0, update=False),
          alignment=Alignment(byte_size=1, bit_offset=0),
          bit_size=8,
          value='0x0')]


Metadata of an Array
---------------------

You can get the metadata of the `array`_ by calling the method
:meth:`~Sequence.describe`.

    >>> # Get the description of the array.
    >>> array.describe()
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

    >>> json.dump(array.describe(), sys.stdout, indent=2)
    {
      "class": "Array",
      "name": "Array",
      "size": 4,
      "type": "Array",
      "member": [
        {
          "address": 0,
          "alignment": [
            1,
            0
          ],
          "class": "Byte",
          "index": [
            0,
            0
          ],
          "max": 255,
          "min": 0,
          "name": "Array[0]",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": "0x0"
        },
        {
          "address": 1,
          "alignment": [
            1,
            0
          ],
          "class": "Byte",
          "index": [
            1,
            0
          ],
          "max": 255,
          "min": 0,
          "name": "Array[1]",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": "0x0"
        },
        {
          "address": 2,
          "alignment": [
            1,
            0
          ],
          "class": "Byte",
          "index": [
            2,
            0
          ],
          "max": 255,
          "min": 0,
          "name": "Array[2]",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": "0x0"
        },
        {
          "address": 3,
          "alignment": [
            1,
            0
          ],
          "class": "Byte",
          "index": [
            3,
            0
          ],
          "max": 255,
          "min": 0,
          "name": "Array[3]",
          "order": "auto",
          "signed": false,
          "size": 8,
          "type": "Field",
          "value": "0x0"
        }
      ]
    }


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
    >>> array.to_list('index')
    [('Array[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Array[1]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Array[2]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Array[3]', Index(byte=0, bit=0, address=0, base_address=0, update=False))]
    >>> # List the field indexes of the array as a CSV list.
    >>> array.to_csv('index.byte', 'index.address')
    [{'id': 'Array[0]', 'index.byte': 0, 'index.address': 0},
     {'id': 'Array[1]', 'index.byte': 0, 'index.address': 0},
     {'id': 'Array[2]', 'index.byte': 0, 'index.address': 0},
     {'id': 'Array[3]', 'index.byte': 0, 'index.address': 0}]
    >>> # View the array field indexes as a JSON string.
    >>> array.to_json('index')
    '[[0, 0, 0, 0, false],
      [0, 0, 0, 0, false],
      [0, 0, 0, 0, false],
      [0, 0, 0, 0, false]]'

    >>> # Index the fields in the array.
    >>> array.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # Index the fields in the array with a start index.
    >>> array.index_fields(index=Index())
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> # List the field indexes of the array.
    >>> array.to_list('index')
    [('Array[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Array[1]', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
     ('Array[2]', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Array[3]', Index(byte=3, bit=0, address=3, base_address=0, update=False))]
    >>> # List the field indexes of the array as a CSV list.
    >>> array.to_csv('index.byte', 'index.address')
    [{'id': 'Array[0]', 'index.byte': 0, 'index.address': 0},
     {'id': 'Array[1]', 'index.byte': 1, 'index.address': 1},
     {'id': 'Array[2]', 'index.byte': 2, 'index.address': 2},
     {'id': 'Array[3]', 'index.byte': 3, 'index.address': 3}]
    >>> # View the array field indexes as a JSON string.
    >>> array.to_json('index')
    '[[0, 0, 0, 0, false],
      [1, 0, 1, 0, false],
      [2, 0, 2, 0, false],
      [3, 0, 3, 0, false]]'


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
    >>> array.to_list()
    [('Array[0]', '0x1'),
     ('Array[1]', '0x2'),
     ('Array[2]', '0x3'),
     ('Array[3]', '0x4')]
    >>> # List the field values of the array as a CSV list.
    >>> array.to_csv()
    [{'id': 'Array[0]', 'value': '0x1'},
     {'id': 'Array[1]', 'value': '0x2'},
     {'id': 'Array[2]', 'value': '0x3'},
     {'id': 'Array[3]', 'value': '0x4'}]
    >>> # View the array field values as a JSON string.
    >>> array.to_json()
    '["0x1", "0x2", "0x3", "0x4"]'


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
    >>> bytestream.hex()
    '01020304'

or

    >>> bytes(array).hex()
    '01020304'


Number of Array Elements
------------------------

You can **get** the number of `array`_ elements with the built-in function
:func:`len`.

    >>> # Number of the array elements.
    >>> len(array)
    4


Access an Array Element
-----------------------

You can **access** an `array element`_ of an `array`_ by its index.

    >>> # Access an array member by its index.
    >>> array[0]
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=Alignment(byte_size=1, bit_offset=0),
         bit_size=8,
         value='0x1')


Attributes of an Array Element Field
------------------------------------

You can **access** the :class:`Field` attributes of an :ref:`field <field>`
*array element* of an `array`_ with the attribute names:

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
    Alignment(byte_size=1, bit_offset=0)
    >>> # Field alignment: byte size of the aligned field group.
    >>> array[0].alignment.byte_size
    1
    >>> # Field alignment: bit offset of the field in its field group.
    >>> array[0].alignment.bit_offset
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
    >>> # Field index: byte offset of the field in the byte stream.
    >>> array[0].index.byte
    0
    >>> # Field index: bit offset of the field relative to its byte offset.
    >>> array[0].index.bit
    0
    >>> # Field index: memory address of the field in the data source.
    >>> array[0].index.address
    0
    >>> # Field index: start address of the byte stream in the data source.
    >>> array[0].index.base_address
    0
    >>> # Field index: update request for the byte stream.
    >>> array[0].index.update
    False


You can **check** if an `array element`_ is a :ref:`field <field>`.

    >>> is_field(array[0])
    True


You can **check** what kind of :ref:`field <field>` it is.

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


Iterate over Array Elements
---------------------------

You can **iterate** over the array elements of an `array`_.

    >>> [element.item_type for element in array]
    [ItemClass.Byte = 42,
     ItemClass.Byte = 42,
     ItemClass.Byte = 42,
     ItemClass.Byte = 42]


View Field Attributes
---------------------

You can **view** the *attributes* of each :ref:`field <field>` of an `array`_
as a list by calling the method :meth:`~Sequence.view_fields`.
Default attribute is the field :attr:`~Field.value`.

    >>> # View the array field values.
    >>> array.view_fields() 
    ['0x1', '0x2', '0x3', '0x4']
    >>> # View the array field type names & field values.
    >>> array.view_fields('name', 'value') 
    [{'name': 'Byte', 'value': '0x1'},
     {'name': 'Byte', 'value': '0x2'},
     {'name': 'Byte', 'value': '0x3'},
     {'name': 'Byte', 'value': '0x4'}]
    >>> # View the array field indexes.
    >>> array.view_fields('index')
    [Index(byte=0, bit=0, address=0, base_address=0, update=False),
     Index(byte=1, bit=0, address=1, base_address=0, update=False),
     Index(byte=2, bit=0, address=2, base_address=0, update=False),
     Index(byte=3, bit=0, address=3, base_address=0, update=False)]

.. note::
    The *attributes* of each :ref:`field <field>` for containers *nested* in the
    `array`_ are viewed as well (chained method call).


View as a JSON string
---------------------

You can view the *attributes* of each :ref:`field <field>` of an `array`_
as a **JSON** formatted string by calling the method :meth:`~Container.to_json`.
Default attribute is the field :attr:`~Field.value`.

    >>> # View the array field values as a JSON string.
    >>> array.to_json()
    '["0x1", "0x2", "0x3", "0x4"]'
    >>> print(array.to_json(indent=2))
    [
      "0x1",
      "0x2",
      "0x3",
      "0x4"
    ]
    >>> # View the array field type names & field values as a JSON string.
    >>> array.to_json('name', 'value') 
    '[{"name": "Byte", "value": "0x1"},
      {"name": "Byte", "value": "0x2"},
      {"name": "Byte", "value": "0x3"},
      {"name": "Byte", "value": "0x4"}]'
    >>> # View the array field indexes as a JSON string.
    >>> array.to_json('index') 
    '[[0, 0, 0, 0, false],
      [1, 0, 1, 0, false],
      [2, 0, 2, 0, false],
      [3, 0, 3, 0, false]]'

.. note::
    The *attributes* of each :ref:`field <field>` for containers *nested* in the
    `array`_ are viewed as well (chained method call).


List Field Items
----------------

You can list all :ref:`field <field>` items of an `array`_
as a **flatten** list by calling the method :meth:`~Sequence.field_items`.

    >>> # List the field items of the array.
    >>> array.field_items()
    [('[0]', Byte(index=Index(byte=0, bit=0,
                              address=0, base_address=0,
                              update=False),
                  alignment=Alignment(byte_size=1, bit_offset=0),
                  bit_size=8,
                  value='0x1')),
     ('[1]', Byte(index=Index(byte=1, bit=0,
                              address=1, base_address=0,
                              update=False),
                  alignment=Alignment(byte_size=1, bit_offset=0),
                  bit_size=8,
                  value='0x2')),
     ('[2]', Byte(index=Index(byte=2, bit=0,
                              address=2, base_address=0,
                              update=False),
                  alignment=Alignment(byte_size=1, bit_offset=0),
                  bit_size=8,
                  value='0x3')),
     ('[3]', Byte(index=Index(byte=3, bit=0,
                              address=3, base_address=0,
                              update=False),
                  alignment=Alignment(byte_size=1, bit_offset=0),
                  bit_size=8,
                  value='0x4'))]


List Field Attributes
---------------------

You can **list** the *attributes* of each :ref:`field <field>` of an `array`_
as a **flatten** list by calling the method :meth:`~Container.to_list`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the array.
    >>> array.to_list()
    [('Array[0]', '0x1'),
     ('Array[1]', '0x2'),
     ('Array[2]', '0x3'),
     ('Array[3]', '0x4')]
    >>> # List the field type names & field values of the array.
    >>> array.to_list('name', 'value')
    [('Array[0]', ('Byte', '0x1')),
     ('Array[1]', ('Byte', '0x2')),
     ('Array[2]', ('Byte', '0x3')),
     ('Array[3]', ('Byte', '0x4'))]
    >>> # List the field indexes of the array.
    >>> array.to_list('index')
    [('Array[0]', Index(byte=0, bit=0, address=0, base_address=0, update=False)),
     ('Array[1]', Index(byte=1, bit=0, address=1, base_address=0, update=False)),
     ('Array[2]', Index(byte=2, bit=0, address=2, base_address=0, update=False)),
     ('Array[3]', Index(byte=3, bit=0, address=3, base_address=0, update=False))]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


You can **list** the *attribute* of each :ref:`field <field>` of an `array`_
as a **flatten** ordered dictionary by calling the method :meth:`~Container.to_dict`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the array.
    >>> array.to_dict()
    OrderedDict([('Array',
                  OrderedDict([('[0]', '0x1'),
                               ('[1]', '0x2'),
                               ('[2]', '0x3'),
                               ('[3]', '0x4')]))])
    >>> # List the field type names & field values of the array.
    >>> array.to_dict('name', 'value')
    OrderedDict([('Array',
                  OrderedDict([('[0]', ('Byte', '0x1')),
                               ('[1]', ('Byte', '0x2')),
                               ('[2]', ('Byte', '0x3')),
                               ('[3]', ('Byte', '0x4'))]))])
    >>> # List the field indexes of the array.
    >>> array.to_dict('index')
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


You can **list** the *attributes* of each :ref:`field <field>` of a `array`_
as a **flatten** list of dictionaries containing the field *path* and the selected
field *attributes* by calling the method :meth:`~Container.to_csv`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the array as a CSV list.
    >>> array.to_csv()
    [{'id': 'Array[0]', 'value': '0x1'},
     {'id': 'Array[1]', 'value': '0x2'},
     {'id': 'Array[2]', 'value': '0x3'},
     {'id': 'Array[3]', 'value': '0x4'}]
    >>> # List the field values of the array as a CSV list.
    >>> array.to_csv('name', 'value')
    [{'id': 'Array[0]', 'name': 'Byte', 'value': '0x1'},
     {'id': 'Array[1]', 'name': 'Byte', 'value': '0x2'},
     {'id': 'Array[2]', 'name': 'Byte', 'value': '0x3'},
     {'id': 'Array[3]', 'name': 'Byte', 'value': '0x4'}]

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Write Field Attributes
----------------------

You can **write** the *attributes* of each :ref:`field <field>` of a `array`_
to a ``.csv`` file by calling the method :meth:`~Container.write_csv`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the array as a CSV list.
    >>> array.to_csv()
    [{'id': 'Array[0]', 'value': '0x1'},
     {'id': 'Array[1]', 'value': '0x2'},
     {'id': 'Array[2]', 'value': '0x3'},
     {'id': 'Array[3]', 'value': '0x4'}]
    >>> # Save the structure field values to a '.csv' file.
    >>> array.write_csv("_static/array.csv")

The generated ``.csv`` file for the structure looks like this:

.. literalinclude:: _static/array.csv

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Save Field Attributes
---------------------

You can **save** the *attributes* of each :ref:`field <field>` of an `array`_
to an ``.ini`` file by calling the method :meth:`~Container.save`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values of the array.
    >>> array.to_list()
    [('Array[0]', '0x1'),
     ('Array[1]', '0x2'),
     ('Array[2]', '0x3'),
     ('Array[3]', '0x4')]
    >>> # Save the array field values to an '.ini' file.
    >>> array.save("_static/array.ini", nested=True)


The generated ``.ini`` file for the array looks like this:

.. literalinclude:: _static/array.ini
    :language: ini

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.


Load Field Values
-----------------

You can **load** the *value* of each :ref:`field <field>` of an `array`_
from an ``.ini`` file by calling the method :meth:`~Container.load`.

    >>> # Create an array.
    >>> array = Array(Byte, 4)
    >>> # Load the array field values from an '.ini' file.
    >>> array.load("_static/array.ini")
    [Array]
    Array[0] = 0x1
    Array[1] = 0x2
    Array[2] = 0x3
    Array[3] = 0x4
    >>> # List the field values of the array.
    >>> array.to_list()
    [('Array[0]', '0x1'),
     ('Array[1]', '0x2'),
     ('Array[2]', '0x3'),
     ('Array[3]', '0x4')]

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.
