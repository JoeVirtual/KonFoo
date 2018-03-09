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

    class FileCachedProvider(Provider):

        def __init__(self, source):
            #: File path
            self._source = Path(source).absolute()
            #: File cache
            self.cache = bytearray(self.path.read_bytes())

        def read(self, address=0, count=0):
            return self._cache[address:]

        def write(self, buffer=bytes(), address=0, count=0):
            view = memoryview(self.cache)
            view[address:address + count] = buffer
