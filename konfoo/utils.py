# -*- coding: utf-8 -*-
"""
    utils.py
    ~~~~~~~~
    <Add description of the module here>.

    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details.
"""

import json
from collections import OrderedDict

from .enums import ItemClass


class HexViewer:
    """A `HexViewer` writes or prints a source file or a byte stream
    as a hexadecimal dump to a output file or the console.

    :param int columns: number of output columns.
        Allowed values are *8*, *16* or *32*.
    """

    def __init__(self, columns=16):
        self._columns = 16
        if columns in (8, 16, 32):
            self._columns = columns

    @property
    def columns(self):
        """Number of output columns."""
        return self._columns

    @columns.setter
    def columns(self, value):
        if value in (8, 16, 32):
            self._columns = int(value)

    @staticmethod
    def _view_area(stream=bytes(), index=0, count=0):
        """Returns the (start, stop) index for the viewing area of the
        byte stream.

        :param int index: start index of the viewing area.
            Default is the begin of the stream.

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

    def file_dump(self, source, index=0, count=0, output=str()):
        """Dumps the content of the *source* file to the console or to the
         optional given *output* file.

        :param str source: location and name of the source file.

        :param int index: optional index to begin with the view of the file
            in bytes. Default is from the begin of file.

        :param int count: optional number of bytes to view of the file.
            Default is to the end of file.

        :param str output: location and name for the optional output file.
        """
        stream = open(source, 'rb').read()
        self.dump(stream, index, count, output)

    def dump(self, stream, index=0, count=0, output=str()):
        """Dumps the content of a byte *stream* to the console or to the
         optional given *output* file.

        :param bytes stream: byte stream to view.

        :param int index: start index of the viewing area.
            Default is the begin of the stream.

        :param int count: number of bytes to view.
            Default is to the end of the stream.

        :param str output: location and name for the optional output file.
        """

        def numerate(pattern, _count):
            return ''.join(pattern.format(x) for x in range(_count))

        def write_to(file_handle, content):
            if file_handle:
                file_handle.write(content + "\n")
            else:
                print(content)

        file = None
        if output:
            file = open(output, 'w')

        start, stop = self._view_area(stream, index, count)
        digits = max(len(hex(start + stop)) - 2, 8)

        # Write header
        write_to(file, " " * digits + " |" + numerate(" {0:02d}", self.columns) + " |")
        write_to(file, "-" * digits + "-+" + "-" * (self.columns * 3) + "-+-" + "-" * self.columns)

        # Set start row and column
        row = int(start / self.columns)
        column = int(start % self.columns)

        # Initialize output for start index row
        output_line = "{0:0{1:d}X} |".format(row * self.columns, digits) + " .." * column
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
                write_to(file, output_line)
                # Next row
                row += 1
                output_line = "{0:0{1:d}X} |".format(row * self.columns, digits)
                output_ascii = ""

        # Write output of stop index row
        if column:
            # Fill missing columns with white spaces.
            output_line += " " * (self.columns - column) * 3
            output_line += " | " + output_ascii
            write_to(file, output_line)


def d3json(blueprint, **options):
    """Converts a *blueprint* into a JSON string.

    .. code-block:: JSON

        {
            "class": "class name",
            "name": "field name",
            "size":  "field bit size",
            "content": "field value",
            "children": []
        }

    :param dict blueprint: blueprint generated  from a `Structure`,
        `Sequence`, `Array` or any `Field` instance.

    :keyword int indent: indentation for the JSON string. Default is *2*.
    """

    def convert(root):
        dct = OrderedDict()
        field_type = root.get('type', None)
        dct['class'] = root.get('class', None)
        dct['name'] = root.get('name', None)

        if field_type is ItemClass.Field.name:
            dct['size'] = root.get('size', None)
            dct['content'] = root.get('value', None)

        children = root.get('member', None)
        # Any containable class with children
        if children:
            dct['children'] = list()
            # Create pointer address field as child
            if field_type is ItemClass.Pointer.name:
                field = OrderedDict()
                field['class'] = dct['class']
                field['name'] = '*' + dct['name']
                field['size'] = root.get('size', None)
                field['content'] = root.get('value', None)
                dct['children'].append(field)
            # Recursive function call map(fnc, args).
            for child in map(convert, children):
                dct['children'].append(child)
        # Null pointer (None pointer)
        elif field_type is ItemClass.Pointer.name:
            dct['size'] = root.get('size', None)
            dct['content'] = root.get('value', None)
        return dct

    options['indent'] = options.get('indent', 2)
    return json.dumps(convert(blueprint), **options)
