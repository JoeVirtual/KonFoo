.. currentmodule:: konfoo

.. testsetup:: *

    from konfoo import *

.. _reading:

Reading
=======

The procedure to **read** from a *data source* the required *byte stream* and
**deserialize** it with a *byte stream* :ref:`mapper <mapper>` includes four
steps.

Create the Byte Stream Provider
-------------------------------

First, create the *byte stream* :ref:`provider <provider>` to access the
*data source*.

    >>> # Create the byte stream provider for the data source.
    >>> provider = FileProvider("./_static/reading.bin")
    >>> provider.cache
    bytearray(b"\x0f\x00KonFoo is \'Fun\'")
    >>> provider.cache.hex()
    '0f004b6f6e466f6f206973202746756e27'

.. note::
    We use here a :class:`FileProvider` but you can write your own
    :ref:`provider <provider>` class to access any kind of *data source*.


Create the Byte Stream Mapper
-----------------------------

Second, create the *byte stream* :ref:`mapper <mapper>` for the *binary data*
to be mapped in the *data source*.

    >>> class FileMapper(Structure):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.length = Decimal16()
    ...         self.content = String(15)
    ...         self.index_fields()

or

    >>> # Create the byte stream mapper.
    >>> mapper = Structure(length = Decimal16(), content = String(15))

    >>> # Index the fields of the mapper.
    >>> mapper.index_fields()
    Index(byte=17, bit=0, address=17, base_address=0, update=False)

    >>> # List the field values of the mapper.
    >>> mapper.to_list()
    [('Structure.length', 0),
     ('Structure.content', '')]

    >>> # List the field values of the mapper as a CSV list.
    >>> mapper.to_csv()
    [{'id': 'Structure.length', 'value': 0},
     {'id': 'Structure.content', 'value': ''}]

    >>> # View the mapper field values as a JSON string.
    >>> mapper.to_json()
    '{"length": 0, "content": ""}'


Create the Byte Stream Reader
-----------------------------

Third, create a *reader* for the *byte stream* :ref:`mapper <mapper>` to the
*data source* by attaching the *byte stream* :ref:`mapper <mapper>` to the
:ref:`data object <data object>` of a :ref:`pointer <pointer>` field.

    >>> class FileReader(Pointer):
    ...
    ...     def __init__(self, address=None, byte_order=BYTEORDER):
    ...         super().__init__(FileMapper(), address, byte_order)

or

    >>> # Create the byte stream reader.
    >>> reader = Pointer(mapper, address=0, data_order='little')

    >>> # List the field values of the pointer and data object.
    >>> reader.to_list()
    [('Pointer.field', '0x0'),
     ('Pointer.data.length', 0),
     ('Pointer.data.content', '')]

    >>> # List the field values of the pointer and data object as a CSV list.
    >>> reader.to_csv()
    [{'id': 'Pointer.field', 'value': '0x0'},
     {'id': 'Pointer.data.length', 'value': 0},
     {'id': 'Pointer.data.content', 'value': ''}]

    >>> # View the pointer and data object field values as a JSON string.
    >>> reader.to_json()
    '{"value": "0x0",
      "data": {"length": 0, "content": ""}}'


Read from the Data Source
-------------------------

Fourth, **read** the required :ref:`byte stream <data object byte stream>` for
the :ref:`data object <data object>` attached to the :ref:`pointer <pointer>`
field with the *byte stream* :ref:`provider <provider>` **from** the *data source*
by calling the method :meth:`~Pointer.read_from` of the :ref:`pointer <pointer>`
field.

    >>> # Start address to read the byte stream for the data object from the data source.
    >>> reader.address
    0

    >>> # Reader points to zero (Null).
    >>> reader.is_null()
    True

    >>> # Internal byte stream of the reader for the data object.
    >>> reader.bytestream
    ''

    >>> # Read from the provider the byte stream and deserialize the byte stream.
    >>> reader.read_from(provider, null_allowed=True)

    >>> # Internal byte stream of the reader for the data object.
    >>> reader.bytestream
    '0f004b6f6e466f6f206973202746756e27'
    >>> bytes.fromhex(reader.bytestream)
    b"\x0f\x00KonFoo is 'Fun'"

    >>> # List the field values of the data object.
    >>> reader.data.to_list()
    [('Structure.length', 15),
     ('Structure.content', "KonFoo is 'Fun'")]

    >>> # List the field values of the data object as a CSV list.
    >>> reader.data.to_csv()
    [{'id': 'Structure.length', 'value': 15},
     {'id': 'Structure.content', 'value': "KonFoo is 'Fun'"}]

    >>> # View the data object field values as a JSON string.
    >>> reader.data.to_json()
    '{"length": 15, "content": "KonFoo is \'Fun\'"}'
