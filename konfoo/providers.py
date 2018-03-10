# -*- coding: utf-8 -*-
"""
    providers.py
    ~~~~~~~~~~~~
    <Add description of the module here>.

    :copyright: (c) 2015-2018 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details
"""

import abc
from pathlib import Path


class Provider:
    """ A `Provider` class provides access for the :class:`Pointer` class to
    **read** and **write** byte streams from and back to a data *source*.
    The `Provider` class servers as a meta class. A derived class must
    implement the two methods :meth:`read` and :meth:`write` for reading
    and writing byte streams from and back to the data *source*.
    """

    @abc.abstractmethod
    def read(self, address=0, count=0):
        """ Returns a *number* of bytes read from a data `source` beginning at
        the start *address*.

        :param int address: start address.
        :param int count: number of bytes to read from a data `source`.

        .. note:: This abstract method must be implemented by a derived class.
        """
        return bytes()

    @abc.abstractmethod
    def write(self, buffer=bytes(), address=0, count=0):
        """ Writes the content of the *buffer* to a data `source` beginning
        at the start *address*.

        :param bytes buffer: content to write.
        :param int address: start address.
        :param int count: number of bytes to write to a data `source`.

        .. note:: This abstract method must be implemented by a derived class.
        """
        pass


class FileProvider(Provider):
    """ A `FileProvider` is a data :class:`Provider` for binary files. The *file*
    content is internal stored in a :attr:`~Provider.cache`. The :meth:`read` and
    :meth:`write` methods only operate on the internal :attr:`~Provider.cache`.

    Call :meth:`flush` to store the updated file content to the same or a new file.

    :param file: name and location of the file to read.
    :type file: :class:`~pathlib.Path`, :class:`str`
    """

    def __init__(self, file):
        #: File path.
        self.path = Path(file).absolute()
        # File cache.
        self._cache = bytearray(self.path.read_bytes())

    def __str__(self):
        return self.__class__.__name__ + "({0.path!s}, " \
                                         "{1!s})".format(self,
                                                         len(self._cache))

    def __repr__(self):
        return self.__class__.__name__ + "(file={0.path!r}, " \
                                         "size={1!r})".format(self,
                                                              len(self._cache))

    @property
    def cache(self):
        """ Returns the internal byte cache of the data `Provider` (read-only)."""
        return self._cache

    def read(self, address=0, count=0):
        """ Returns a *number* of bytes read from the :attr:`cache` beginning
        at the start *address*.

        :param int address: start address.
        :param int count: number of bytes to read from the cache.
        """
        return self._cache[address:]

    def write(self, buffer=bytes(), address=0, count=0):
        """ Writes the content of the *buffer* to the :attr:`cache` beginning
        at the start *address*.

        :param bytes buffer: content to write.
        :param int address: start address.
        :param int count: number of bytes to write to the cache.
        """
        view = memoryview(self._cache)
        view[address:address + count] = buffer

    def flush(self, file=str()):
        """ Flushes the updated file content to the given *file*.

        .. note::  Overwrites an existing file.

        :param str file: name and location of the file.
            Default is the original file.
        """
        if file:
            Path(file).write_bytes(self._cache)
        else:
            self.path.write_bytes(self._cache)
