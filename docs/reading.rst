.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *


.. _reading:

Reading
=======

You create a data :ref:`provider <provider>` for the *data source*.

    >>> provider = FileProvider('./_static/data.bin')
    >>> provider
    FileProvider(file='./_static/data.bin', size=15)
    >>> provider.cache
    bytearray(b"KonFoo is \'Fun\'")

.. note:: We use here a :ref:`file provider <file provider>` but you can write
    your own :ref:`provider <provider>` class to access your kind of *data
    source*.


You create a *byte stream* :ref:`mapper <mapper>` for the *data source*.

    >>> mapper = Structure()
    >>> mapper.content = String(15)
    >>> mapper # doctest: +NORMALIZE_WHITESPACE
    Structure([('content', String(index=Index(byte=0, bit=0,
                                              address=0,  base_address=0,
                                              update=False),
                                  alignment=(15, 0),
                                  bit_size=120,
                                  value=''))])

You create an entry point via a :ref:`pointer <pointer>` to the *data source*.

    >>> pointer = Pointer()
    >>> pointer.data = mapper
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.content', '')]

You read the required *byte stream* for the :ref:`data object <data object>`
referenced by the :ref:`pointer <pointer>` via the data :ref:`provider <provider>`
from the *data source* by calling the method :class:`~Pointer.read_from` of the
:ref:`pointer <pointer>`.

    >>> pointer.read_from(provider, null_allowed=True)
    >>> pointer.to_list() # doctest: +NORMALIZE_WHITESPACE
    [('Pointer.value', '0x0'),
     ('Pointer.data.content', "KonFoo is 'Fun'")]
