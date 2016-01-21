# -*- coding: utf-8 -*-
"""
    exceptions.py
    ~~~~~~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details
"""

from .enums import Enumeration


class KonFooError(Exception):
    """An exception that KonF'00' can handle and show to the user."""


class FileError(KonFooError):
    """

    """
    pass


class RangeError(KonFooError):
    """

    """
    pass


class SizeError(KonFooError):
    """

    """
    pass


class LengthError(KonFooError):
    """

    """
    pass


class AlignmentError(KonFooError):
    """

    """
    pass


class OffsetError(KonFooError):
    """

    """
    pass
