# -*- coding: utf-8 -*-
"""
    providers.py
    ~~~~~~~~~~~~
    <Add descritpion of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD-style, see LICENSE for details
"""


class Provider:
    """A `Provider` ...

    """
    def __init__(self):
        self._is_open = False

    @property
    def is_open(self):
        return self._is_open

    def read(self, address=0, count=0):
        """Reads the *number* of bytes from a data `source` beginning at
        the start *address*.

        :param int address: start address.
        :param int count: number of bytes to read from a data `source`.
        """
        return bytes()

    def write(self, buffer=bytes(), address=0, count=0):
        """ Writes the content of the *buffer* to a data `source` beginning
        at the start *address*.

        :param bytes buffer: content to write.
        :param int address: start address.
        :param int count: number of bytes to write to a data `source`.
        """
        pass
