.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *

.. _provider:

Provider
========

KonFoo has an abstract :class:`Provider` class with an abstract interface to
**read** a *byte stream* from a *data source* and to **write** a *byte stream*
to a *data source*.

Read Interface
--------------

A :class:`Provider` class has the abstract method :meth:`Provider.read` which
must be implemented by a derived class to read at the given start address
the given number of bytes from the data source and returns the :class:`bytes`.


Write Interface
---------------

A :class:`Provider` class has the abstract method :meth:`Provider.write` which
must be implemented by a derived class to write the given number of bytes at
the given start address to the data source.


Example
-------

.. code-block:: python

    from konfoo import Provider
    from pathlib import Path

    class MyProvider(Provider):

        def __init__(self, file):
            #: File path.
            self.path = Path(file).absolute()
            #: File cache.
            self.cache = bytearray(self.path.read_bytes())

        def read(self, address=0, count=0):
            """ Returns a *number* of bytes read from the :attr:`cache` beginning
            at the start *address*.

            :param int address: start address.
            :param int count: number of bytes to read from the cache.
            """
            return self.cache[address:]

        def write(self, buffer=bytes(), address=0, count=0):
            """ Writes the content of the *buffer* to the :attr:`cache` beginning
            at the start *address*.

            :param bytes buffer: content to write.
            :param int address: start address.
            :param int count: number of bytes to write to the cache.
            """
            view = memoryview(self.cache)
            view[address:address + count] = buffer
