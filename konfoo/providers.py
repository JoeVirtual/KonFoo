# -*- coding: utf-8 -*-
"""
    providers.py
    ~~~~~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD-style, see LICENSE for details
"""


class Provider:
    """A `Provider` ...

    :param source: generic data source.
    """

    def __init__(self, source):
        self._source = source
        self._stream = bytes()

    def read(self, address=0, count=0):
        """Reads the *number* of bytes from a data `source` beginning at
        the start *address*.

        :param int address: start address.

        :param int count: number of bytes to read from a data `source`.

        .. note::

           This is method must be overwritten by a derived class.
        """
        return self._stream

    def write(self, buffer=bytes(), address=0, count=0):
        """ Writes the content of the *buffer* to a data `source` beginning
        at the start *address*.

        :param bytes buffer: content to write.

        :param int address: start address.

        :param int count: number of bytes to write to a data `source`.

        .. note::

           This is method must be overwritten by a derived class.
        """
        pass


class FileProvider(Provider):
    """A `FileProvider` is a data :class:`Provider` for binary files.

    :param str source: file name and location.
    """

    def __init__(self, source):
        super().__init__(source)
        if not isinstance(self._source, str):
            raise TypeError(self._source)
        if isinstance(source, str):
            self._stream = bytearray(open(source, 'rb').read())
        else:
            raise TypeError(source)

    def read(self, address=0, count=0):
        return self._stream[address:]

    def write(self, buffer=bytes(), address=0, count=0):
        view = memoryview(self._stream)
        view[address:address + count] = buffer
