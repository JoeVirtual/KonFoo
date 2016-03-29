# -*- coding: utf-8 -*-
"""
    exceptions.py
    ~~~~~~~~~~~~~
    <Add description of the module here>.
    
    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details
"""


class ByteOrderTypeError(TypeError):
    """ Raised if an inappropriate byte order type is assigned to a field class.
    """

    def __init__(self, field, byte_order):
        message = "{}: Inappropriate byte order type '{}'.".format(
            field.__class__.__name__, type(byte_order).__name__)
        super().__init__(message)


class EnumTypeError(TypeError):
    """ Raised if an inappropriate enum type is assigned to a field class.
    """

    def __init__(self, field, enumeration):
        message = "{}: Inappropriate enum type '{}'.".format(
            field.__class__.__name__, type(enumeration).__name__)
        super().__init__(message)


class FactoryTypeError(TypeError):
    """ Raised if an inappropriate member type is produced by a factory class.
    """

    def __init__(self, field, factory, item, member=None, index=None):
        _message = "{}: Inappropriate member type '{}'".format(
            field.__class__.__name__, type(item).__name__)
        _member = " assigned to member [{}]".format(member) if member is not None else ''
        _index = " at index ({}.byte, {}.bit)".format(index) if index is not None else ''
        _factory = " by factory {}.".format(factory.__name__)
        super().__init__(_message + _member + _index + _factory)


class MemberTypeError(TypeError):
    """ Raised if an inappropriate member type is assigned to any container class.
    """

    def __init__(self, field, item, member=None, index=None):
        if callable(item):
            _message = "{}: Inappropriate member type '{}'".format(
                field.__class__.__name__, item.__name__)
        else:
            _message = "{}: Inappropriate member type '{}'".format(
                field.__class__.__name__, type(item).__name__)
        _member = " assigned to member [{}]".format(member) if member is not None else ''
        _index = " at index ({}.byte, {}.bit)".format(index) if index is not None else ''
        super().__init__(_message + _member + _index + '.')


class ProviderTypeError(TypeError):
    """ Raised if an inappropriate data provider type is assigned to a pointer class.
    """

    def __init__(self, field, provider):
        message = "{}: Inappropriate data provider type '{}'.".format(
            field.__class__.__name__, type(provider).__name__)
        super().__init__(message)


class ContainerLengthError(ValueError):
    """ Raised if a container class has an inappropriate field length.
    """

    def __init__(self, field, length):
        message = "{}: Inappropriate field length ({}, {}).".format(
            field.__class__.__name__, length[0], length[1])
        super().__init__(message)


class FieldAddressError(ValueError):
    """ Raised if an inappropriate address is assigned to a field class.
    """

    def __init__(self, field, index, address):
        message = "{}: Inappropriate field address value '{}' at index ({}, {}).".format(
            field.__class__.__name__, address, index.byte, index.bit)
        super().__init__(message)


class FieldAlignmentError(ValueError):
    """ Raised if an inappropriate alignment value is assigned to a field class.
    """

    def __init__(self, field, index, alignment):
        message = "{}: Invalid field alignment value '({}, {})' at index ({}, {}).".format(
            field.__class__.__name__, alignment[0], alignment[1], index.byte, index.bit)
        super().__init__(message)


class FieldByteOrderError(ValueError):
    """ Raised if an inappropriate byte order value is assigned to a field class.
    """

    def __init__(self, field, index, byte_order):
        message = "{}: Inappropriate field byte order value '{}' at index ({}, {}).".format(
            field.__class__.__name__, byte_order.name, index.byte, index.bit)
        super().__init__(message)


class FieldIndexError(ValueError):
    """ Raised if an inappropriate index value is assigned to a field class.
    """

    def __init__(self, field, index):
        message = "{}: Inappropriate field index ({}, {}).".format(
            field.__class__.__name__, index.byte, index.bit)
        super().__init__(message)


class FieldSizeError(ValueError):
    """ Raised if an inappropriate bit size value is assigned to a field class.
    """

    def __init__(self, field, index, size):
        message = "{}: Inappropriate field size value '{}' at index ({}, {})".format(
            field.__class__.__name__, size, index.byte, index.bit)
        super().__init__(message)


class FieldTypeError(TypeError):
    """ Raised if an inappropriate argument type is assigned to a field class.
    """

    def __init__(self, field, index, value):
        message = "{}: Inappropriate argument type '{}' at index ({}, {}).".format(
            field.__class__.__name__, type(value).__name__, index.byte, index.bit)
        super().__init__(message)


class FieldValueError(ValueError):
    """ Raised if an inappropriate argument value is assigned to a field class.
    """

    def __init__(self, field, index, value):
        message = "{}: Inappropriate argument value '{}' at index ({}, {}).".format(
            field.__class__.__name__, value, index.byte, index.bit)
        super().__init__(message)


class FieldValueEncodingError(ValueError):
    """ Raised if an inappropriate value encoding is assigned to a field class.
    """

    def __init__(self, field, index, encoding):
        message = "{}: Inappropriate value encoding '{}' at index ({}, {}).".format(
            field.__class__.__name__, encoding, index.byte, index.bit)
        super().__init__(message)


class FieldGroupByteOrderError(Exception):
    """ Raised if the byte order of a field contradicts its aligned field group.
    """

    def __init__(self, field, index, byte_order):
        message = "{}: Field byte order '{}' contradicts the field group byte order '{}' at index ({}, {}).".format(
            field.__class__.__name__, field.byte_order.name, byte_order.name, index.byte, index.bit)
        super().__init__(message)


class FieldGroupOffsetError(Exception):
    """ Raised if the alignment offset of a field does not match with its field group.
    """

    def __init__(self, field, index, alignment):
        message = "{}: Field alignment offset '{}' does not match field group offset '{}' at index ({}, {}).".format(
            field.__class__.__name__, field.alignment[1], alignment[1], index.byte, index.bit)
        super().__init__(message)


class FieldGroupSizeError(Exception):
    """ Raised if the alignment size of a field does not match with its field group.
    """

    def __init__(self, field, index, alignment):
        message = "{}: Field alignment size '{}' does not match field group size '{}' at index ({}, {}).".format(
            field.__class__.__name__, field.alignment[0], alignment[0], index.byte, index.bit)
        super().__init__(message)
