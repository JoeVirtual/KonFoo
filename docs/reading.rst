.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *


.. _reading:

Reading
=======



Create a Provider
-----------------

You create a data :ref:`provider <provider>` to access the *data source*.

    >>> # Create a data provider for the data source.
    >>> provider = FileProvider('./_static/data.bin')
    >>> provider
    FileProvider(file='./_static/data.bin', size=17)
    >>> provider.cache
    bytearray(b"\x0f\x00KonFoo is \'Fun\'")

.. note::
    We use here a :ref:`file provider <file provider>` but you can write your own
    :ref:`provider <provider>` class to access any kind of *data source*.


Create the Mapper
-----------------

You create a *byte stream* :ref:`mapper <mapper>` for the binary *data* in the
*data source*.

.. code-block:: python
    :emphasize-lines: 5-6

    class Mapper(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal16()
            self.content = String(15)
            self.index_fields()


or

    >>> # Create a mapper.
    >>> mapper = Structure(
    ...     length = Decimal16(),
    ...     content = String(15))
    >>> # Index the fields in the mapper.
    >>> mapper.index_fields()
    Index(byte=17, bit=0, address=17, base_address=0, update=False)
    >>> # List the field values in the mapper.
    >>> mapper.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Structure.length', 0),
     ('Structure.content', '')]


Create an Entry Point
---------------------

You create an *entry point* for the :ref:`mapper <mapper>` to the *data source*
by attaching the :ref:`mapper <mapper>` to the :ref:`data object <data object>`
of a :ref:`pointer <pointer>` field.

.. code-block:: python
    :emphasize-lines: 4-5

    class MapperPointer(Pointer):

        def __init__(self, address=None, byte_order=BYTEORDER):
            # Attach the mapper as the referenced data object to the pointer.
            super().__init__(Mapper(), address, byte_order)

or

    >>> # Create an entry point for the mapper.
    >>> pointer = Pointer(mapper, address=0, data_order='little')
    >>> # List the field values of the pointer and its attached data object.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.length', 0),
     ('Pointer.data.content', '')]
    >>> # Address of the data object referenced by the pointer.
    >>> pointer.address
    0


Read from a Data Source
-----------------------

You **read** the required *byte stream* for the :ref:`data object <data object>`
referenced by the :ref:`pointer <pointer>` with a data :ref:`provider <provider>`
**from** the *data source* by calling the method :class:`~Pointer.read_from` of the
:ref:`pointer <pointer>` field.

    >>> # Read from the provider the necessary bytes and deserialize it.
    >>> pointer.read_from(provider, null_allowed=True)
    >>> # List the field values of the pointer and its attached data object.
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.length', 15),
     ('Pointer.data.content', "KonFoo is 'Fun'")]
    >>> len(pointer.data.content)
    15
