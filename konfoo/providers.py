# -*- coding: utf-8 -*-
"""
    providers.py
    ~~~~~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015-2017 by Jochen Gerhaeusser.
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

    :param source: generic data source.
    """

    def __init__(self, source):
        self._source = source
        self._cache = bytes()

    @property
    def cache(self):
        """ Returns the internal cache of the data `Provider` (read-only)."""
        return self._cache

    @abc.abstractmethod
    def read(self, address=0, count=0):
        """ Reads the *number* of bytes from a data `source` beginning at
        the start *address*.

        :param int address: start address.
        :param int count: number of bytes to read from a data `source`.

        .. note:: This abstract method must be implemented by a derived class.
        """
        return self._cache

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
    """ A `FileProvider` is a data :class:`Provider` for binary files. The file
    content is internal stored in a cache. The read and write methods only
    operate on the internal cache.

    Call :meth:`flush` to store the updated file content to a file.

    :param str source: name and location of the file.
    """

    def __init__(self, source):
        super().__init__(source)
        # File path
        self._source = Path(source).absolute()
        # File cache
        self._cache = bytearray(self._source.read_bytes())

    def __str__(self):
        return self.__class__.__name__ + "({0._source!s}, " \
                                         "{1!s})".format(self, len(self._cache))

    def __repr__(self):
        return self.__class__.__name__ + "(file={0._source!r}, " \
                                         "size={1!r})".format(self, len(self._cache))

    def read(self, address=0, count=0):
        return self._cache[address:]

    def write(self, buffer=bytes(), address=0, count=0):
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
            self._source.write_bytes(self._cache)
