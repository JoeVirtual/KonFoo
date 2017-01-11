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

    >>> provider = FileProvider('./_static/data.bin')
    >>> provider
    FileProvider(file='./_static/data.bin', size=17)
    >>> provider.cache
    bytearray(b"\x0f\x00KonFoo is \'Fun\'")


.. note:: We use here a :ref:`file provider <file provider>` but you can write
    your own :ref:`provider <provider>` class to access any kind of *data
    source*.


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
            self.next_index()


or

    >>> mapper = Structure()
    >>> mapper.length = Decimal16()
    >>> mapper.content = String(15)
    >>> mapper.next_index()
    Index(byte=17, bit=0, address=17, base_address=0, update=False)
    >>> mapper # doctest: +NORMALIZE_WHITESPACE
    Structure([('length', Decimal16(index=Index(byte=0, bit=0,
                                              address=0,  base_address=0,
                                              update=False),
                                   alignment=(2, 0),
                                   bit_size=16,
                                   value=0)),
               ('content', String(index=Index(byte=2, bit=0,
                                              address=2,  base_address=0,
                                              update=False),
                                  alignment=(15, 0),
                                  bit_size=120,
                                  value=''))])


Create an Entry Point
---------------------

You create an *entry point* for the :ref:`mapper <mapper>` to the *data source*
by attaching the :ref:`mapper <mapper>` to the :ref:`data object <data object>`
of a :ref:`pointer <pointer>`.

.. code-block:: python
    :emphasize-lines: 5

    class MapperPointer(Pointer):

        def __init__(self, address=None, byte_order=BYTEORDER):
            super().__init__(Mapper(), address, byte_order)

or

    >>> pointer = Pointer(mapper)
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.length', 0),
     ('Pointer.data.content', '')]


Read from a Data Source
-----------------------

You read the required *byte stream* for the :ref:`data object <data object>`
referenced by the :ref:`pointer <pointer>` via the data :ref:`provider <provider>`
from the *data source* by calling the method :class:`~Pointer.read_from` of the
:ref:`pointer <pointer>`.

    >>> pointer.read_from(provider, null_allowed=True)
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.length', 15),
     ('Pointer.data.content', "KonFoo is 'Fun'")]
    >>> len(pointer.data.content)
    15
