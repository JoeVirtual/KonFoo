# -*- coding: utf-8 -*-
"""
utils.py
~~~~~~~~
Utilities.

:copyright: (c) 2015-2022 by Jochen Gerhaeusser.
:license: BSD, see LICENSE for details.
"""
from __future__ import annotations

import json
from typing import (Any)

from .globals import ItemClass


class HexViewer:
    """ The :class:`HexViewer` class writes or prints a source file or a
    byte stream as a hexadecimal dump to a output file or the console.

    :param int columns: number of output columns.
        Allowed values are ``8``, ``16`` or ``32``.

    Example:

    >>> viewer = HexViewer()
    >>> viewer.dump(b'KonF`00` is Fun.')
             | 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 |
    ---------+-------------------------------------------------+-----------------
    00000000 | 4B 6F 6E 46 60 30 30 60 20 69 73 20 46 75 6E 2E | KonF`00` is Fun.
    """

    def __init__(self, columns: int = 16) -> None:
        self._columns = 16
        if columns in (8, 16, 32):
            self._columns = columns

    @property
    def columns(self) -> int:
        """ Number of output columns."""
        return self._columns

    @columns.setter
    def columns(self, value: int) -> None:
        if value in (8, 16, 32):
            self._columns = int(value)

    @staticmethod
    def _view_area(stream: bytes = bytes(),
                   index: int = 0,
                   count: int = 0) -> tuple[int, int]:
        """ Returns the (start, stop) index for the viewing area of the
        byte stream.

        :param int index: start index of the viewing area.
            Default is the beginning of the stream.
        :param int count: number of bytes to view.
            Default is to the end of the stream.
        """
        # Byte stream size
        size = len(stream)

        # Start index of the viewing area
        start = max(min(index, size), -size)
        if start < 0:
            start += size

        # Stop index of the viewing area
        if not count:
            count = size
        if count > 0:
            stop = min(start + count, size)
        else:
            stop = size

        return start, stop

    def file_dump(self,
                  source: str,
                  index: int = 0,
                  count: int = 0,
                  output: str = str()) -> None:
        """ Dumps the content of the *source* file to the console or to the
        optional given *output* file.

        :param str source: location and name of the source file.
        :param int index: optional start index of the viewing area in bytes.
            Default is from the begin of the file.
        :param int count: optional number of bytes to view.
            Default is to the end of the file.
        :param str output: location and name for the optional output file.
        """
        stream = open(source, 'rb').read()
        self.dump(stream, index, count, output)

    def dump(self,
             stream: bytes,
             index: int = 0,
             count: int = 0,
             output: str = str()) -> None:
        """ Dumps the content of the byte *stream* to the console or to the
        optional given *output* file.

        :param bytes stream: byte stream to view.
        :param int index: optional start index of the viewing area in bytes.
            Default is the beginning of the stream.
        :param int count: optional number of bytes to view.
            Default is to the end of the stream.
        :param str output: location and name for the optional output file.
        """

        def numerate(template: str,
                     _count: int) -> str:
            return ''.join(template.format(x) for x in range(_count))

        def write_to(file_handle,
                     content: str) -> None:
            if file_handle:
                file_handle.write(content + "\n")
            else:
                print(content)

        dst = None
        if output:
            dst = open(output, 'w')

        start, stop = self._view_area(stream, index, count)
        digits = max(len(hex(start + stop)) - 2, 8)

        # Write header
        write_to(dst,
                 " " * digits +
                 " |" +
                 numerate(" {0:02d}", self.columns) +
                 " |")
        write_to(dst,
                 "-" * digits +
                 "-+" +
                 "-" * (self.columns * 3) +
                 "-+-" +
                 "-" * self.columns)

        # Set start row and column
        row = int(start / self.columns)
        column = int(start % self.columns)

        # Initialize output for start index row
        output_line = "{0:0{1:d}X} |".format(row * self.columns,
                                             digits)
        output_line += " .." * column
        output_ascii = "." * column

        # Iterate over viewing area
        for value in stream[start:stop]:
            column += 1
            output_line += " {0:02X}".format(int(value))
            if value in range(32, 126):
                output_ascii += "{0:c}".format(value)
            else:
                output_ascii += "."
            column %= self.columns
            if not column:
                # Write output line
                output_line += ' | ' + output_ascii
                write_to(dst, output_line)
                # Next row
                row += 1
                output_line = "{0:0{1:d}X} |".format(row * self.columns,
                                                     digits)
                output_ascii = ""

        # Write output of stop index row
        if column:
            # Fill missing columns with white spaces
            output_line += " " * (self.columns - column) * 3
            output_line += " | " + output_ascii
            write_to(dst, output_line)


def d3flare_json(metadata: dict[str, Any],
                 file=None,
                 **options: Any) -> str | None:
    """ Converts the *metadata* dictionary of a container or field into a
    ``flare.json`` formatted string or formatted stream written to the *file*

    The ``flare.json`` format is defined by the `d3.js <https://d3js.org/>`_
    graphic library.

    The ``flare.json`` format looks like this:

    .. code-block:: JSON

        {
            "class": "class of the field or container",
            "name":  "name of the field or container",
            "size":  "bit size of the field",
            "value": "value of the field",
            "children": []
        }

    :param dict metadata: metadata generated from a :class:`Structure`,
        :class:`Sequence`, :class:`Array` or any :class:`Field` instance.
    :param file: optional file-like object to write to
    """

    def convert(parent: dict[str, Any]) -> dict[str, Any]:
        node = dict()
        item_type = parent.get('type')
        node['class'] = parent.get('class')
        node['name'] = parent.get('name')

        if item_type is ItemClass.Field.name:
            node['size'] = parent.get('size')
            node['value'] = parent.get('value')

        children = parent.get('member')
        if children:
            # Any containable class with children
            node['children'] = list()
            if item_type is ItemClass.Pointer.name:
                # Create pointer address field as child
                field = dict()
                field['class'] = node['class']
                field['name'] = f"*{node['name']}"
                field['size'] = parent.get('size')
                field['value'] = parent.get('value')
                node['children'].append(field)
            for child in map(convert, children):
                # Recursive function call map(fnc, args).
                node['children'].append(child)
        elif item_type is ItemClass.Pointer.name:
            # Null pointer (None pointer)
            node['size'] = parent.get('size')
            node['value'] = parent.get('value')
        return node

    options['indent'] = options.get('indent', 2)

    if file:
        return json.dump(convert(metadata), file, **options)
    else:
        return json.dumps(convert(metadata), **options)
