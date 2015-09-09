# -*- coding: utf-8 -*-
"""
    exceptions.py
    ~~~~~~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD-style, see LICENSE for details
"""

from .enums import Enumeration


class ExitCodes(Enumeration):
    Exception = 1
    FileError = 2
    RangeError = 3
    IndexError = 4
    SizeError = 5
    LengthError = 6
    AlignmentError = 7
    OffsetError = 8


class KonFooException(Exception):
    """An exception that KonF'00' can handle and show to the user."""

    #: The exit code for this exception
    exit_code = ExitCodes.Exception
    pass


class FileError(KonFooException):
    """

    """
    exit_code = ExitCodes.FileError
    pass


class OutOfRange(KonFooException):
    """

    """
    exit_code = ExitCodes.RangeError
    pass


class InvalidIndex(KonFooException):
    """

    """
    exit_code = ExitCodes.IndexError
    pass


class InvalidSize(KonFooException):
    """

    """
    exit_code = ExitCodes.SizeError
    pass


class InvalidLength(KonFooException):
    """

    """
    exit_code = ExitCodes.LengthError
    pass


class BadAligned(KonFooException):
    """

    """
    exit_code = ExitCodes.AlignmentError
    pass


class BadOffset(KonFooException):
    """

    """
    exit_code = ExitCodes.OffsetError
    pass
