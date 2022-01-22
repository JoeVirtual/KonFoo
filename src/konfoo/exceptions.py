# -*- coding: utf-8 -*-
"""
exceptions.py
~~~~~~~~~~~~~
<Add description of the module here>.

:copyright: (c) 2015-2020 by Jochen Gerhaeusser.
:license: BSD, see LICENSE for details
"""


class ByteOrderTypeError(TypeError):
    """ Raised if an inappropriate byte order type is assigned to a field class.
    """

    def __init__(self, field, byte_order):
        message = (
            f"{field.__class__.__name__}: Inappropriate byte order type "
            f"'{type(byte_order).__name__1}'.")
        super().__init__(message)


class ByteOrderValueError(ValueError):
    """ Raised if an inappropriate byte order value is assigned to a field class.
    """

    def __init__(self, field, index, byte_order):
        message = (f"{field.__class__.__name__}: "
                   f"Invalid field byte order value '{byte_order}' "
                   f"at index ({index.byte}, {index.bit}).")
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
        message = (f"{field.__class__.__name__}: Inappropriate member type "
                   f"'{type(item).__name__}'")
        if member is not None:
            message += f" assigned to member [{member}]"
        if index is not None:
            message += f" at index ({index.byte}, {index.bit})"
        message += f" by factory {factory.__name__}."
        super().__init__(message)


class MemberTypeError(TypeError):
    """ Raised if an inappropriate member type is assigned to any container class.
    """

    def __init__(self, field, item, member=None, index=None):
        message = f"{field.__class__.__name__}: Inappropriate member type "
        if callable(item):
            message += f"'{item.__name__}'"
        else:
            message += f"'{type(item).__name__}'"
        if member is not None:
            message += f" assigned to member [{member}]"
        if index is not None:
            message += f" at index ({index.byte}, {index.bit})"
        super().__init__(message + ".")


class ProviderTypeError(TypeError):
    """ Raised if an inappropriate data provider type is assigned to a pointer
    class.
    """

    def __init__(self, field, provider):
        message = (
            f"{field.__class__.__name__}: Inappropriate data provider type "
            f"'{type(provider).__name__}'.")
        super().__init__(message)


class ContainerLengthError(ValueError):
    """ Raised if a container class has an inappropriate field length.
    """

    def __init__(self, field, length):
        message = (
            f"{field.__class__.__name__}: Inappropriate field length "
            f"({length[0]}, {length[1]}).")
        super().__init__(message)


class FieldAddressError(ValueError):
    """ Raised if an inappropriate address is assigned to a field class.
    """

    def __init__(self, field, index, address):
        message = (
            f"{field.__class__.__name__}: Inappropriate field address value "
            f"'{address}' at index ({index.byte}, {index.bit}).")
        super().__init__(message)


class FieldAlignmentError(ValueError):
    """ Raised if an inappropriate alignment value is assigned to a field class.
    """

    def __init__(self, field, index, alignment):
        message = (
            f"{field.__class__.__name__}: Invalid field alignment value "
            f"'({alignment.byte_size,}, {alignment.bit_offset})' "
            f"at index ({index.byte}, {index.bit}).")
        super().__init__(message)


class FieldByteOrderError(ValueError):
    """ Raised if an inappropriate byte order value is assigned to a field class.
    """

    def __init__(self, field, index, byte_order):
        message = (
            f"{field.__class__.__name__}: Inappropriate field byte order value "
            f"'{byte_order.name}' at index ({index.byte}, {index.bit}).")
        super().__init__(message)


class FieldIndexError(ValueError):
    """ Raised if an inappropriate index value is assigned to a field class.
    """

    def __init__(self, field, index):
        message = (
            f"{field.__class__.__name__}: Inappropriate field index "
            f"({index.byte}, {index.bit}).")
        super().__init__(message)


class FieldSizeError(ValueError):
    """ Raised if an inappropriate bit size value is assigned to a field class.
    """

    def __init__(self, field, index, size):
        message = (
            f"{field.__class__.__name__}: Inappropriate field size value "
            f"'{size}' at index ({index.byte}, {index.bit})")
        super().__init__(message)


class FieldTypeError(TypeError):
    """ Raised if an inappropriate argument type is assigned to a field class.
    """

    def __init__(self, field, index, value):
        message = (
            f"{field.__class__.__name__}: Inappropriate argument type "
            f"'{type(value).__name__}' at index ({index.byte}, {index.bit}).")
        super().__init__(message)


class FieldValueError(ValueError):
    """ Raised if an inappropriate argument value is assigned to a field class.
    """

    def __init__(self, field, index, value):
        message = (
            f"{field.__class__.__name__,}: Inappropriate argument value "
            f"'{value}' at index ({index.byte}, {index.bit}).")
        super().__init__(message)


class FieldValueEncodingError(ValueError):
    """ Raised if an inappropriate value encoding is assigned to a field class.
    """

    def __init__(self, field, index, encoding):
        message = (
            f"{field.__class__.__name__}: Inappropriate value encoding "
            f"'{encoding}' at index ({index.byte}, {index.bit}).")
        super().__init__(message)


class FieldGroupByteOrderError(Exception):
    """ Raised if the byte order of a field contradicts its aligned field group.
    """

    def __init__(self, field, index, byte_order):
        message = (
            f"{field.__class__.__name__}: Field byte order "
            f"'{field.byte_order.name}' contradicts the field group byte order "
            f"'{byte_order.name}' at index ({index.byte}, {index.bit}).")
        super().__init__(message)


class FieldGroupOffsetError(Exception):
    """ Raised if the alignment offset of a field does not match with its field
    group.
    """

    def __init__(self, field, index, alignment):
        message = (
            f"{field.__class__.__name__}: Field alignment offset "
            f"'{field.alignment.bit_offset}' does not match field group offset "
            f"'{alignment.bit_offset}' at index ({index.byte}, {index.bit}).")
        super().__init__(message)


class FieldGroupSizeError(Exception):
    """ Raised if the alignment size of a field does not match with its field
    group.
    """

    def __init__(self, field, index, alignment):
        message = (
            f"{field.__class__.__name__}: Field alignment size "
            f"'{field.alignment.byte_size}' does not match field group size "
            f"'{alignment.byte_size}' at index ({index.byte}, {index.bit}).")
        super().__init__(message)
