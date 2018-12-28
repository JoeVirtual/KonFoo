# -*- coding: utf-8 -*-
"""
    exceptions.py
    ~~~~~~~~~~~~~
    <Add description of the module here>.

    :copyright: (c) 2015-2018 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details
"""


class ByteOrderTypeError(TypeError):
    """ Raised if an inappropriate byte order type is assigned to a field class.
    """

    def __init__(self, field, byte_order):
        message = "{0}: Inappropriate byte order type '{1}'.".format(
            field.__class__.__name__, type(byte_order).__name__)
        super().__init__(message)


class ByteOrderValueError(ValueError):
    """ Raised if an inappropriate byte order value is assigned to a field class.
    """

    def __init__(self, field, index, byte_order):
        message = "{0}: Invalid field byte order value '{1}' at index ({2}, {3}).".format(
            field.__class__.__name__, byte_order, index.byte, index.bit)
        super().__init__(message)


class EnumTypeError(TypeError):
    """ Raised if an inappropriate enum type is assigned to a field class.
    """

    def __init__(self, field, enumeration):
        message = "{0}: Inappropriate enum type '{1}'.".format(
            field.__class__.__name__, type(enumeration).__name__)
        super().__init__(message)


class FactoryTypeError(TypeError):
    """ Raised if an inappropriate member type is produced by a factory class.
    """

    def __init__(self, field, factory, item, member=None, index=None):
        _message = "{0}: Inappropriate member type '{1}'".format(
            field.__class__.__name__, type(item).__name__)
        _member = " assigned to member [{0}]".format(
            member) if member is not None else str()
        _index = " at index ({0}.byte, {0}.bit)".format(
            index) if index is not None else str()
        _factory = " by factory {0}.".format(factory.__name__)
        super().__init__(_message + _member + _index + _factory)


class MemberTypeError(TypeError):
    """ Raised if an inappropriate member type is assigned to any container class.
    """

    def __init__(self, field, item, member=None, index=None):
        if callable(item):
            _message = "{0}: Inappropriate member type '{1}'".format(
                field.__class__.__name__, item.__name__)
        else:
            _message = "{0}: Inappropriate member type '{1}'".format(
                field.__class__.__name__, type(item).__name__)
        _member = " assigned to member [{0}]".format(
            member) if member is not None else str()
        _index = " at index ({0}.byte, {0}.bit)".format(
            index) if index is not None else str()
        super().__init__(_message + _member + _index + '.')


class ProviderTypeError(TypeError):
    """ Raised if an inappropriate data provider type is assigned to a pointer class.
    """

    def __init__(self, field, provider):
        message = "{0}: Inappropriate data provider type '{1}'.".format(
            field.__class__.__name__, type(provider).__name__)
        super().__init__(message)


class ContainerLengthError(ValueError):
    """ Raised if a container class has an inappropriate field length.
    """

    def __init__(self, field, length):
        message = "{0}: Inappropriate field length ({1}, {2}).".format(
            field.__class__.__name__,
            length[0], length[1])
        super().__init__(message)


class FieldAddressError(ValueError):
    """ Raised if an inappropriate address is assigned to a field class.
    """

    def __init__(self, field, index, address):
        message = "{0}: Inappropriate field address value '{1}' at index ({2}, {3}).".format(
            field.__class__.__name__,
            address,
            index.byte, index.bit)
        super().__init__(message)


class FieldAlignmentError(ValueError):
    """ Raised if an inappropriate alignment value is assigned to a field class.
    """

    def __init__(self, field, index, alignment):
        message = "{0}: Invalid field alignment value '({1}, {2})' at index ({3}, {4}).".format(
            field.__class__.__name__,
            alignment.byte_size,
            alignment.bit_offset,
            index.byte, index.bit)
        super().__init__(message)


class FieldByteOrderError(ValueError):
    """ Raised if an inappropriate byte order value is assigned to a field class.
    """

    def __init__(self, field, index, byte_order):
        message = "{0}: Inappropriate field byte order value '{1}' at index ({2}, {3}).".format(
            field.__class__.__name__,
            byte_order.name,
            index.byte, index.bit)
        super().__init__(message)


class FieldIndexError(ValueError):
    """ Raised if an inappropriate index value is assigned to a field class.
    """

    def __init__(self, field, index):
        message = "{0}: Inappropriate field index ({1}, {2}).".format(
            field.__class__.__name__,
            index.byte, index.bit)
        super().__init__(message)


class FieldSizeError(ValueError):
    """ Raised if an inappropriate bit size value is assigned to a field class.
    """

    def __init__(self, field, index, size):
        message = "{0}: Inappropriate field size value '{1}' at index ({2}, {3})".format(
            field.__class__.__name__,
            size,
            index.byte, index.bit)
        super().__init__(message)


class FieldTypeError(TypeError):
    """ Raised if an inappropriate argument type is assigned to a field class.
    """

    def __init__(self, field, index, value):
        message = "{0}: Inappropriate argument type '{1}' at index ({2}, {3}).".format(
            field.__class__.__name__,
            type(value).__name__,
            index.byte, index.bit)
        super().__init__(message)


class FieldValueError(ValueError):
    """ Raised if an inappropriate argument value is assigned to a field class.
    """

    def __init__(self, field, index, value):
        message = "{0}: Inappropriate argument value '{1}' at index ({2}, {3}).".format(
            field.__class__.__name__,
            value,
            index.byte, index.bit)
        super().__init__(message)


class FieldValueEncodingError(ValueError):
    """ Raised if an inappropriate value encoding is assigned to a field class.
    """

    def __init__(self, field, index, encoding):
        message = "{0}: Inappropriate value encoding '{1}' at index ({2}, {3}).".format(
            field.__class__.__name__,
            encoding,
            index.byte, index.bit)
        super().__init__(message)


class FieldGroupByteOrderError(Exception):
    """ Raised if the byte order of a field contradicts its aligned field group.
    """

    def __init__(self, field, index, byte_order):
        message = "{0}: Field byte order '{1}' contradicts the field group byte order '{2}' at index ({3}, {4}).".format(
            field.__class__.__name__,
            field.byte_order.name,
            byte_order.name,
            index.byte, index.bit)
        super().__init__(message)


class FieldGroupOffsetError(Exception):
    """ Raised if the alignment offset of a field does not match with its field group.
    """

    def __init__(self, field, index, alignment):
        message = "{0}: Field alignment offset '{1}' does not match field group offset '{2}' at index ({3}, {4}).".format(
            field.__class__.__name__,
            field.alignment.bit_offset,
            alignment.bit_offset,
            index.byte, index.bit)
        super().__init__(message)


class FieldGroupSizeError(Exception):
    """ Raised if the alignment size of a field does not match with its field group.
    """

    def __init__(self, field, index, alignment):
        message = "{0}: Field alignment size '{1}' does not match field group size '{2}' at index ({3}, {4}).".format(
            field.__class__.__name__,
            field.alignment.byte_size,
            alignment.byte_size,
            index.byte, index.bit)
        super().__init__(message)
