# -*- coding: utf-8 -*-
"""
providers.py
~~~~~~~~~~~~
Data provider.

:copyright: (c) 2015-2022 by Jochen Gerhaeusser.
:license: BSD, see LICENSE for details
"""
from __future__ import annotations

import abc
from pathlib import Path


class Provider:
    """ The :class:`Provider` class provides access for the :class:`Pointer`
    class to **read** and **write** byte streams from and back to a data
    *source*.

    The :class:`Provider` class servers as a metaclass.

    A derived class must implement the two methods :meth:`read` and :meth:`write`
    for reading and writing byte streams from and back to the data *source*.
    """

    @abc.abstractmethod
    def read(self,
             address: int = 0,
             count: int = 0) -> bytes:
        """ Returns a *number* of bytes read from a data `source` beginning at
        the start *address*.

        :param int address: start address to read from.
        :param int count: number of bytes to read from a data `source`.

        .. note:: This abstract method must be implemented by a derived class.
        """
        return bytes()

    @abc.abstractmethod
    def write(self,
              buffer: bytes | bytearray = bytearray(),
              address: int = 0,
              count: int = 0) -> None:
        """ Writes the content of the *buffer* to a data `source` beginning
        at the start *address*.

        :param bytes|bytearray buffer: content to write.
        :param int address: start address to write to.
        :param int count: number of bytes to write to a data `source`.

        .. note:: This abstract method must be implemented by a derived class.
        """
        pass


class FileProvider(Provider):
    """ The :class:`FileProvider` is a byte stream :class:`Provider` for binary
    files.

    The *file* content is internal stored in a :attr:`~Provider.cache`.

    The :meth:`read` and :meth:`write` methods only operate on the internal
    :attr:`~Provider.cache`.

    Call :meth:`flush` to store the updated file content to the same or a new
    file.

    :param Path|str file: name and location of the file to read.
    """

    def __init__(self, file: Path | str) -> None:
        #: File path.
        self.path = Path(file).absolute()
        # File cache.
        self._cache = bytearray(self.path.read_bytes())

    def __str__(self) -> str:
        return (f"{self.__class__.__name__}"
                f"({self.path!s}, {len(self._cache)!s})")

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}"
                f"(file={self.path!r}, size={len(self._cache)!r})")

    @property
    def cache(self) -> bytearray:
        """ Returns the internal byte stream cache of the `Provider`
        (read-only)."""
        return self._cache

    def read(self,
             address: int = 0,
             count: int = 0) -> bytes:
        """ Returns a *number* of bytes read from the :attr:`cache` beginning
        at the start *address*.

        :param int address: start address.
        :param int count: number of bytes to read from the cache.
        """
        return self._cache[address:]

    def write(self,
              buffer: bytes | bytearray = bytes(),
              address: int = 0,
              count: int = 0) -> None:
        """ Writes the content of the *buffer* to the :attr:`cache` beginning
        at the start *address*.

        :param bytes|bytearray buffer: content to write.
        :param int address: start address.
        :param int count: number of bytes to write to the cache.
        """
        view = memoryview(self._cache)
        view[address:address + count] = buffer

    def flush(self,
              file: Path | str | None = None) -> None:
        """ Flushes the updated file content to the given *file*.

        .. note::  Overwrites an existing file.

        :param Path|str|None file: name and location of the file.
            Default is the original file.
        """
        if file is None:
            self.path.write_bytes(self._cache)
        else:
            Path(file).write_bytes(self._cache)
