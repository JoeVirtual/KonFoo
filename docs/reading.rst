.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *


.. _reading:

Reading
=======

The procedure to **read** from a *data source* the required *byte stream* and
**deserialize** it with a *byte stream* :ref:`mapper <mapper>` includes four
steps.

Create the Provider
-------------------

First, you create the data :ref:`provider <provider>` to access the *data source*.

    >>> # Create the data provider for the data source.
    >>> provider = FileProvider('./_static/data.bin')
    >>> provider
    FileProvider(file='./_static/data.bin', size=17)
    >>> provider.cache
    bytearray(b"\x0f\x00KonFoo is \'Fun\'")

.. note::
    We use here a :class:`FileProvider` but you can write your own
    :ref:`provider <provider>` class to access any kind of *data source*.


Create the Mapper
-----------------

Second, you create the *byte stream* :ref:`mapper <mapper>` for the *binary data*
to be mapped in the *data source*.

.. code-block:: python
    :emphasize-lines: 5-6

    class Mapper(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal16()
            self.content = String(15)
            self.index_fields()


or

    >>> # Create the byte stream mapper.
    >>> mapper = Structure(
    ...     length = Decimal16(),
    ...     content = String(15))
    >>> # Index the fields in the byte stream mapper.
    >>> mapper.index_fields()
    Index(byte=17, bit=0, address=17, base_address=0, update=False)
    >>> # List the field values in the byte stream mapper.
    >>> mapper.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.length', 0),
     ('Structure.content', '')]


Create the Entry Point
-----------------------

Third, you create the *entry point* for the *byte stream* :ref:`mapper <mapper>`
to the *data source* by attaching the *byte stream* :ref:`mapper <mapper>` to the
:ref:`data object <data object>` of a :ref:`pointer <pointer>` field.

.. code-block:: python
    :emphasize-lines: 4-5

    class MapperPointer(Pointer):

        def __init__(self, address=None, byte_order=BYTEORDER):
            # Attach the mapper as the referenced data object to the pointer.
            super().__init__(Mapper(), address, byte_order)

or

    >>> # Create the entry point for the mapper.
    >>> pointer = Pointer(mapper, address=0, data_order='little')
    >>> # List the field values of the pointer and its attached data object.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.length', 0),
     ('Pointer.data.content', '')]



Read from the Data Source
-------------------------

Fourth, you **read** the required *byte stream* for the :ref:`data object <data object>`
referenced by the :ref:`pointer <pointer>` field with the :ref:`provider <provider>`
**from** the *data source* by calling the method :meth:`~Pointer.read_from` of the
:ref:`pointer <pointer>` field.

    >>> # Start address to read the byte stream from the data source.
    >>> pointer.value
    '0x0'
    >>> # Pointer points to zero.
    >>> pointer.is_null()
    True
    >>> # Byte stream for the data object referenced by the pointer field.
    >>> pointer.bytestream
    ''
    >>> # Read from the provider the byte stream and deserialize the byte stream.
    >>> pointer.read_from(provider, null_allowed=True)
    >>> # Byte stream for the data object referenced by the pointer field.
    >>> pointer.bytestream
    '0f004b6f6e466f6f206973202746756e27'
    >>> bytes.fromhex(pointer.bytestream)
    b"\x0f\x00KonFoo is 'Fun'"
    >>> # List the field values of the pointer and its attached data object.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.length', 15),
     ('Pointer.data.content', "KonFoo is 'Fun'")]
    >>> len(pointer.data.content)
    15
