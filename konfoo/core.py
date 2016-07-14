# -*- coding: utf-8 -*-
"""
    core.py
    ~~~~~~~
    <Add description of the module here>.

    :copyright: (c) 2015-2016 by Jochen Gerhaeusser.
    :license: BSD, see LICENSE for details
"""

import math
import struct
import copy
import time
import datetime
import calendar
import abc
from collections import Mapping, namedtuple, OrderedDict
from collections.abc import MutableSequence
from configparser import ConfigParser
from binascii import hexlify
from pprint import pprint

from konfoo.enums import Enumeration
from konfoo.globals import ItemClass, Byteorder, BYTEORDER, limiter
from konfoo.options import (
    Option,
    byte_order_option, get_byte_order, nested_option, get_nested,
    field_types_option, get_field_types, verbose_option, verbose
)
from konfoo.exceptions import (
    ByteOrderTypeError, EnumTypeError, FactoryTypeError, MemberTypeError,
    ProviderTypeError, ContainerLengthError,
    FieldAddressError, FieldAlignmentError, FieldByteOrderError,
    FieldIndexError, FieldSizeError, FieldTypeError, FieldValueError,
    FieldValueEncodingError,
    FieldGroupByteOrderError, FieldGroupOffsetError, FieldGroupSizeError
)
from konfoo.providers import Provider


def is_any(obj):
    return isinstance(obj, (Field, Structure, Sequence))


def is_provider(obj):
    return isinstance(obj, Provider)


def is_field(obj):
    return isinstance(obj, Field)


def is_container(obj):
    return isinstance(obj, (Sequence, Structure))


def is_sequence(obj):
    return isinstance(obj, Sequence)


def is_array(obj):
    return isinstance(obj, Array)


def is_structure(obj):
    return isinstance(obj, Structure)


def is_mapping(obj):
    return isinstance(obj, Mapping)


def is_pointer(obj):
    return isinstance(obj, Pointer)


def is_mixin(obj):
    return is_container(obj) or is_pointer(obj)


# Memory Patch
Patch = namedtuple('Patch', [
    'buffer',
    'address',
    'byteorder',
    'bit_size',
    'bit_offset',
    'inject'])
""" The `Patch` class contains the relevant information to patch a memory area
of a `data source` accessed via a data :class:`Provider` by a :class:`Pointer`
field.

:param bytes buffer: byte stream for the memory area to patch in the data
    source. The byte stream contains the data of the patch item.

:param int address: address of the memory area to patch in the data source.

:param byteorder: :class:`Byteorder` of the memory area to patch in the data
    source.

:param int bit_size: bit size of the patch item.

:param int bit_offset: bit offset of the patch item within the memory area.

:param bool inject: if `True` the patch item must be injected into the
    memory area of the data source.
"""

# Field Index
Index = namedtuple('Index', [
    'byte',
    'bit',
    'address',
    'base_address',
    'update'])
""" The `Index` class contains the relevant information of the location of a
:class:`Field` in a `byte stream` and in a `data source`. The `byte stream` is
normally provided by a :class:`Pointer` field. The `data source` is normally
accessed via a data :class:`Provider` by a :class:`Pointer` field.

:param int byte: byte offset of the :class:`Field` in the byte stream.

:param int bit: bit offset of the :class:`Field` relative to its byte offset.

:param int address: address of the :class:`Field` in the data source.

:param int base_address: base address of the data source.

:param bool update: if `True` the byte stream needs to be updated.
"""


def zero():
    return Index(0, 0, 0, 0, False)


class Container:
    """ The `Container` class is a meta class for all classes which can contain
    :class:`Field` items. Container classes are :class:`Structures <Structure>`,
    :class:`Sequences <Sequence>`, :class:`Arrays <Array>` and :class:`Pointers
    <Pointer>`.

    The `Container` class provides core features to **view**, **save** and
    **load** the *values* of the :class:`Field` items in the `Container`.
    """

    @abc.abstractmethod
    def field_items(self, root=str(), **options):
        """ Returns a **flat** list which contains the ``(path, item)`` tuples
        for each :class:`Field` in the `Container`.

        :param str root: root path.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `data` objects of all :class:`Pointer` fields in the `Container`
            list their  *nested* `data` object fields as well
            (chained method call).

        .. note:: This abstract method must be implemented by a derived class.
        """
        return list()

    @nested_option()
    @field_types_option()
    def to_list(self, name=str(), **options):
        """ Returns a **flat** list which contains tuples in the form of
        ``(path, value)`` or ``(path, type, value)`` for each :class:`Field`
        in the `Container`.

        The type entry of the tuple is optional.

        :param str name: name of the `Container`.
            Default is the class name of the instance.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `Container` lists their *nested* `data` object fields as well
            (chained method call).

        :keyword bool field_types: if `True` the type of the :class:`Field`
            is inserted into the tuple.
        """
        # Name of the Container
        root = name if name else self.__class__.__name__

        fields = list()
        for item in self.field_items(**options):
            path_to_field, field = item
            path_to_field = '{0}.{1}'.format(root, path_to_field)

            if get_field_types(options):
                byte, bit = field.alignment
                field_type = field.name + str((byte, bit))
                fields.append((path_to_field, field_type, field.value))
            else:
                fields.append((path_to_field, field.value))

        return fields

    @nested_option()
    @field_types_option()
    def to_dict(self, name=str(), **options):
        """ Returns a **flat** :class:`ordered dictionary <collections.OrderedDict>`
        which contains the ``{'path': value}`` or ``{'path|type': value}`` pairs
        for each :class:`Field` in the `Container`.

        :param str name: name of the `Container`.
            Default is the class name of the instance.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `Container` lists their *nested* `data` object fields as well
            (chained method call).

        :keyword bool field_types: if `True` the type of the :class:`Field`
            is append to the end of the path string with '|' as delimiter.
        """
        # Name of the Container
        root = name if name else self.__class__.__name__

        fields = OrderedDict()
        fields[root] = OrderedDict()
        for item in self.field_items(**options):
            path_to_field, field = item

            if get_field_types(options):
                byte, bit = field.alignment
                path_to_field += '|' + field.name + str((byte, bit))

            fields[root][path_to_field] = field.value
        return fields

    @nested_option()
    @field_types_option()
    def save(self, file, section=str(), **options):
        """ Saves the *values* of the :class:`Field`'s in the `Container` to
        an INI *file*.

        :param str file: name and location of the INI *file*.

        :param str section: section in the INI file to look for the
            :class:`Field` values of the `Container`. If no *section* is
            specified the class name of the instance is used.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `Container` saves their *nested* `data` object fields as well
            (chained method call).

        :keyword bool field_types: if `True` the type of the :class:`Field`
            is appended to its path string with the '|' sign as delimiter.

        Example:

        >>> class Foo(Structure):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.stream = Stream()
        ...         self.float = Float()
        ...         self.structure = Structure()
        ...         self.structure.decimal = Decimal(8)
        ...         self.array = Array(Byte, 3)
        ...         self.pointer = Pointer()
        >>> foo = Foo()
        >>> foo.save('foo.ini')

        File `foo.ini`:

        .. code-block:: ini

            [Foo]
            stream = b''
            float = 0.0
            structure.decimal = 0
            array[0] = 0x0
            array[1] = 0x0
            array[2] = 0x0
            pointer = 0x0
        """
        parser = ConfigParser()
        parser.read_dict(self.to_dict(section, **options))
        with open(file, 'w') as handle:
            parser.write(handle)
        handle.close()

    @nested_option()
    @field_types_option()
    @verbose_option(True)
    def load(self, file, section=str(), **options):
        """ Loads the *values* of the :class:`Field`'s in the `Container` from
        an INI *file*.

        :param str file: name and location of the INI *file*.

        :param str section: section in the INI *file* to look for the
            :class:`Field` values of the `Container`. If no *section* is
            specified the class name of the instance is used.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `Container` load their *nested* `data` object fields as well
            (chained method call).

        :keyword bool field_types: if `True` the type of the :class:`Field`
            is append to the end of the path string with '|' as delimiter.

        :keyword bool verbose: if `True` the loading is executed in verbose
            mode.

        File `foo.ini`:

        .. code-block:: ini

            [Foo]
            stream = b''
            float = 0.0
            structure.decimal = 0
            array[0] = 0x0
            array[1] = 0x0
            array[2] = 0x0
            pointer = 0x0

        Example:

        >>> class Foo(Structure):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.stream = Stream()
        ...         self.float = Float()
        ...         self.structure = Structure()
        ...         self.structure.decimal = Decimal(8)
        ...         self.array = Array(Byte, 3)
        ...         self.pointer = Pointer()
        >>> foo = Foo()
        >>> foo.load('foo.ini')
        [Foo]
        Foo.stream = b''
        Foo.float = 0.0
        Foo.structure.decimal = 0
        Foo.array[0] = 0x0
        Foo.array[1] = 0x0
        Foo.array[2] = 0x0
        Foo.pointer = 0x0
        """
        section = section if section else self.__class__.__name__

        parser = ConfigParser()
        parser.read(file)

        if parser.has_section(section):
            verbose(options, "[{0}]".format(section))

            for option, field in self.field_items(**options):
                if get_field_types(options):
                    byte, bit = field.alignment
                    option += '|' + field.name + str((byte, bit))

                if parser.has_option(section, option):
                    # Bool fields
                    if field.is_bool():
                        field.value = parser.getboolean(section, option)
                    # Float fields
                    elif field.is_float():
                        field.value = parser.getfloat(section, option)
                    # String fields
                    elif field.is_string():
                        field.value = parser.get(section, option)
                    # Stream fields
                    elif field.is_stream():
                        value = parser.get(section, option)
                        stream = bytes.fromhex(value.replace("b'", '').
                                               replace("'", ""))
                        # Auto size a zero sized stream field to
                        # the current stream length
                        if not field:
                            field.resize(len(stream))
                        field.value = stream
                    # Decimal fields
                    else:
                        field.value = parser.get(section, option)
                    verbose(options, "{0}.{1} = {2}".format(section, option, field.value))
        else:
            verbose(options, "No section [{0}] found.".format(section))


class Structure(OrderedDict, Container):
    """ A `Structure` is an :class:`ordered dictionary <collections.OrderedDict>`
    whereby the dictionary `key` describes the *name* of a *member* of the
    `Structure` and the `value` of the dictionary `key` describes the *type* of
    the *member*. Allowed *members* are :class:`Structure`, :class:`Sequence`,
    :class:`Array` or :class:`Field` instances.

    The `Structure` class extends the :class:`ordered dictionary
    <collections.OrderedDict>` from the Python standard module :mod:`collections`
    with the :class:`Container` class and attribute getter and setter for the
    ``{'key': value}`` pairs to access and to assign  the *members* of the
    `Structure` easier, but this comes with the cost that the dictionary `keys`
    must be valid Python attribute names.

    A `Structure` has additional methods to **read**, **decode**, **encode**
    and **view** binary data:

    *   **Read** from a :class:`Provider` the necessary bytes for each `data`
        object referenced by the :class:`Pointer` fields in a `Structure`
        via :meth:`read_from()`.
    *   **Decode** the :class:`Field` values of the `Structure` from a
        byte stream via :meth:`decode()`.
    *   **Encode** the :class:`Field` values of the `Structure` to a
        byte stream via :meth:`encode()`.
    *   Get the **next** :class:`Index` after the last :class:`Field` of the
        `Structure` via :meth:`next_index()`.
    *   Get the **first** :class:`Field` of the `Structure`
        via :meth:`first_field()`.
    *   Get the accumulated **length** of all :class:`Field`'s in the
        `Structure` via :meth:`field_length()`.
    *   View the **index** for each :class:`Field` in the `Structure`
        via :meth:`field_indexes()`.
    *   View the **type** for each :class:`Field` in the `Structure`
        via :meth:`field_types()`.
    *   View the **value** for each :class:`Field` in the `Structure`
        via :meth:`field_values()`.
    *   List the **item** and its path for each :class:`Field` in the `Structure`
        as a flat list via :meth:`field_items()`.
    *   Get a **blueprint** of the `Structure` via :meth:`blueprint()`.
    """
    item_type = ItemClass.Structure

    def __init__(self):
        super().__init__()

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, name, item):
        # Structure
        if is_structure(item):
            super().__setitem__(name, item)
        # Dictionaries
        elif is_mapping(item):
            super().__setitem__(name, Structure(item))
        # Sequence
        elif is_sequence(item):
            super().__setitem__(name, item)
        # Field
        elif is_field(item):
            super().__setitem__(name, item)
        else:
            raise MemberTypeError(self, item, name)

    def __getattr__(self, name):
        """ Returns the :class:`Field` of the `Structure` member whose dictionary key
        is equal to the *name*.

        If the attribute *name* is in the namespace of the `Ordered Dictionary`
        base class then the base class is called instead.

        The `__getattr__` method is only called when the method
        `__getattribute__` raises an `AttributeError` exception.
        """
        # Namespace check for ordered dictionary attribute
        if name.startswith('_OrderedDict__'):
            return super().__getattribute__(name)
        else:
            return self[name]

    def __setattr__(self, name, item):
        """ Assigns the *item* to the member of the `Structure` whose dictionary
        key is equal to the *name*.

        If the attribute *name* is in the namespace of the `Ordered Dictionary`
        base class then the base class is called instead.
        """
        # Namespace check for ordered dictionary attribute
        if name.startswith('_OrderedDict__'):
            return super().__setattr__(name, item)
        elif is_any(item):
            self[name] = item
        elif callable(item):
            # Field Factory
            setitem = item()
            if is_any(setitem):
                super().__setitem__(name, setitem)
            else:
                raise FactoryTypeError(self, item, setitem, name)
        else:
            raise MemberTypeError(self, item, name)

    @nested_option()
    def read_from(self, provider, **options):
        """ All :class:`Pointer` fields of the `Structure` read the necessary
        amount of bytes from the data :class:`Provider` for their *nested*
        :attr:`~Pointer.data` object fields. Null pointer are ignored.

        :param provider: data :class:`Provider`.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the `data`
            objects of all :class:`Pointer` fields of the `Structure` reads their
            *nested* `data` object fields as well (chained method call).
            Each :class:`Pointer` field stores the bytes for its *nested*
            :attr:`~Pointer.data` object in its own :attr:`~Pointer.bytestream`.
        """
        for item in self.values():
            # Container or Pointer
            if is_mixin(item):
                item.read_from(provider, **options)

    @byte_order_option()
    @nested_option()
    def decode(self, buffer=bytes(), index=zero(), **options):
        """ Decodes sequential bytes from the *buffer* starting at the begin
        of the *buffer* or with the given *index* by mapping the bytes to the
        :class:`Field`'s of the `Structure` in accordance with the decoding
        *byte order* of the *buffer* and the :class:`Field`.

        A specific *byte order* of a :class:`Field` overrules the decoding
        *byte order* of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the last
        :class:`Field` of the `Structure`.

        Optional the decoding of the *nested* :attr:`~Pointer.data` objects
        of all :class:`Pointer` fields of the `Structure` can be enabled.

        :param bytes buffer: bytestream.

        :param index: current read :class:`Index` within the *buffer*.

        :keyword byte_order: decoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` all :class:`Pointer` fields of a
            `Structure` decodes their *nested* `data` object fields as well
            (chained method call).
            Each :class:`Pointer` field uses for the decoding of its *nested*
            :attr:`~Pointer.data` object its own :attr:`~Pointer.bytestream`.
        """
        for item in self.values():
            index = item.decode(buffer, index, **options)
        return index

    @byte_order_option()
    @nested_option()
    def encode(self, buffer=bytearray(), index=zero(), **options):
        """ Encodes sequential bytes to the *buffer* starting at the begin of
        the *buffer* or with the given *index* by mapping the *values* of the
        :class:`Field`'s of the `Structure` to the bytes in accordance with
        the encoding *byte order* of the *buffer* and the :class:`Field`.

        A specific *byte order* of a :class:`Field` overrules the encoding
        *byte order* of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the last
        :class:`Field` of the `Structure`.

        Optional the encoding of the *nested* :attr:`~Pointer.data` objects
        of all :class:`Pointer` fields of the `Structure` can be enabled.

        :param bytearray buffer: bytestream.

        :param index: current write :class:`Index` within the *buffer*.

        :keyword byte_order: encoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` all :class:`Pointer` fields of the
            `Structure` encodes their *nested* `data` object fields as well
            (chained method call).
            Each :class:`Pointer` field uses for the encoding of its *nested*
            :attr:`~Pointer.data` object its own :attr:`~Pointer.bytestream`.
        """
        for item in self.values():
            index = item.encode(buffer, index, **options)
        return index

    @nested_option()
    def next_index(self, index=zero(), **options):
        """ Returns the :class:`Index` after the last :class:`Field`
        of the `Structure`.

        :param index: :class:`Index` of the first :class:`Field`
            of the `Structure`.

        :keyword bool nested: if `True` all :class:`Pointer` fields of the
            `Structure` indexes their *nested* `data` object fields as well
            (chained method call).
        """
        for name, item in self.items():
            # Container
            if is_container(item):
                index = item.next_index(index, **options)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                index = item.next_index(index)
                item.subscript()
            # Field
            elif is_field(item):
                index = item.next_index(index)
            else:
                raise MemberTypeError(self, item, name, index)
        return index

    def initialize(self, content):
        """ Initializes the :class:`Field` members in the `Structure` with
        the *values* in the *content* dictionary.

        :param dict content: a dictionary contains the :class:`Field`
            values for each member in the `Structure`.
        """
        for name, value in content.items():
            item = self[name]
            # Container or Pointer
            if is_mixin(item):
                item.initialize(value)
            # Fields
            elif is_field(item):
                item.value = value
            else:
                raise MemberTypeError(self, item, name)

    def first_field(self):
        """ Returns the first :class:`Field` of the `Structure` or `None` for
        an empty `Structure`.
        """
        for name, item in self.items():
            # Container
            if is_container(item):
                field = item.first_field()
                # Container is not empty
                if field is not None:
                    return field
            # Field
            elif is_field(item):
                return item
            else:
                raise MemberTypeError(self, item, name)
        return None

    def field_length(self):
        """ Returns the length of the `Structure` as a tuple in the form of
        ``(number of bytes, remaining number of bits)``.
        """
        length = 0
        for name, item in self.items():
            # Container
            if is_container(item):
                byte_length, bit_length = item.field_length()
                length += bit_length + byte_length * 8
            # Field
            elif is_field(item):
                length += item.bit_size
            else:
                raise MemberTypeError(self, item, name)
        return divmod(length, 8)

    @nested_option()
    def field_indexes(self, index=zero(), **options):
        """ Returns an :class:`ordered dictionary <collections.OrderedDict>`
        which contains the ``{'name': index}`` pairs for each :class:`Field`
        of the `Structure`.

        :param index: optional start :class:`Index` of the `Structure`.

        :keyword bool nested: if `True` all :class:`Pointer` fields of the
            `Structure` lists their *nested* `data` object fields as well
            (chained method call).
        """
        indexes = OrderedDict()
        for name, item in self.items():
            # Container
            if is_container(item):
                indexes[name] = item.field_indexes(index, **options)
                index = item.next_index(index)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                indexes[name] = item.field_indexes(index, **options)
                index = item.next_index(index)
            # Field
            elif is_field(item):
                index = item.next_index(index)
                indexes[name] = item.index
            else:
                raise MemberTypeError(self, item, name, index)
        return indexes

    @nested_option()
    def field_types(self, **options):
        """ Returns an :class:`ordered dictionary <collections.OrderedDict>`
        which contains the ``{'name': type}`` pairs for each :class:`Field`
        of the `Structure`.

        :keyword bool nested: if `True` all :class:`Pointer` fields of the
            `Structure` lists their *nested* `data` object fields as well
            (chained method call).
        """
        types = OrderedDict()
        for name, item in self.items():
            # Container
            if is_container(item):
                types[name] = item.field_types(**options)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                types[name] = item.field_types(**options)
            # Field
            elif is_field(item):
                types[name] = item.name
            else:
                raise MemberTypeError(self, item, name)
        return types

    @nested_option()
    def field_values(self, **options):
        """ Returns an :class:`ordered dictionary <collections.OrderedDict>`
        which contains the ``{'name': value}`` pairs for each :class:`Field`
        of the `Structure`.

        :keyword bool nested: if `True` all :class:`Pointer` fields of the
            `Structure` lists their *nested* `data` object fields as well
            (chained method call).
        """
        values = OrderedDict()
        for name, item in self.items():
            # Container
            if is_container(item):
                values[name] = item.field_values(**options)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                values[name] = item.field_values(**options)
            # Field
            elif is_field(item):
                values[name] = item.value
            else:
                raise MemberTypeError(self, item, name)
        return values

    @nested_option()
    def field_items(self, root=None, **options):
        """ Returns a **flat** list which contains the ``(path, item)`` tuples
        for each :class:`Field` of the `Structure`.

        :param str root: root path.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `data` objects of all :class:`Pointer` fields of the `Structure`
            list their *nested* `data` object fields as well
            (chained method call).
        """
        base = root if root else str()

        items = list()
        for name, item in self.items():
            path = '{0}.{1}'.format(base, name) if base else name
            # Container
            if is_container(item):
                for field in item.field_items(path, **options):
                    items.append(field)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                for field in item.field_items(path, **options):
                    items.append(field)
            # Field
            elif is_field(item):
                items.append((path, item))
            else:
                raise MemberTypeError(self, item, path)
        return items

    @nested_option(True)
    def blueprint(self, name=str(), **options):
        """ Returns the **blueprint** of the `Structure` as an
        :class:`ordered dictionary <collections.OrderedDict>`.

        .. code-block:: python

            blueprint = {
                'class': self.__class__.__name__,
                'name': name if name else self.__class__.__name__,
                'size': len(self),
                'type': Structure.item_type.name
                'member': [
                    item.blueprint(member) for member, item in self.items()
                ]
            }

        :param str name: optional name for the `Structure`.

        :keyword bool nested: if `True` all :class:`Pointer` fields of the
            `Structure` lists their *nested* `data` object fields as well
            (chained method call). Default is `True`.
        """
        members = list()
        obj = OrderedDict()
        obj['class'] = self.__class__.__name__
        obj['name'] = name if name else self.__class__.__name__
        obj['size'] = len(self)
        obj['type'] = Structure.item_type.name
        obj['member'] = members

        for member_name, item in self.items():
            # Container
            if is_container(item):
                members.append(item.blueprint(member_name, **options))
            # Pointer
            elif is_pointer(item) and get_nested(options):
                members.append(item.blueprint(member_name, **options))
            # Field
            elif is_field(item):
                members.append(item.blueprint(member_name, nested=False))
            else:
                raise MemberTypeError(self, item, member_name)
        return obj


class Sequence(MutableSequence, Container):
    """ A `Sequence` contains a list of different *items*. Allowed *items* are
    :class:`Structure`, :class:`Sequence`, :class:`Array` or :class:`Field`
    instances.

    A `Sequence` is:

    *   *containable*: ``item in self`` returns `True` if *item* is in the
        `Sequence`.
    *   *sized*: ``len(self)`` returns the number of items in the `Sequence`.
    *   *subscriptable* ``self[index]`` returns the *item* at the *index*
        of the `Sequence`.
    *   *iterable* ``iter(self)`` iterates over the *items* in the `Sequence`

    A `Sequence` supports the usual methods for sequences:

    *   **Append** an item to the `Sequence` via :meth:`append()`.
    *   **Insert** an item before the *index* into the `Sequence`
        via :meth:`insert()`.
    *   **Extend** the `Sequence` with items via :meth:`extend()`.
    *   **Clear** the `Sequence` via :meth:`clear()`.
    *   **Pop** an item with the *index* from the `Sequence` via :meth:`pop()`.
    *   **Remove** the first occurrence of an *item* from the `Sequence`
        via :meth:`remove()`.
    *   **Reverse** all items in the `Sequence` via :meth:`reverse()`.

    A `Sequence` has additional methods to **read**, **decode**, **encode**
    and **view** binary data:

    *   **Read** from a :class:`Provider` the necessary bytes for each `data`
        object referenced by the :class:`Pointer` fields in the `Sequence`
        via :meth:`read_from()`.
    *   **Decode** the :class:`Field` values in the `Sequence` from a byte stream
        via :meth:`decode()`.
    *   **Encode** the :class:`Field` values in the `Sequence` to a byte stream
        via :meth:`encode()`.
    *   Get the **next** :class:`Index` after the last :class:`Field` in the
        `Sequence` via :meth:`next_index()`.
    *   Get the **first** :class:`Field` in the `Sequence` via
        :meth:`first_field()`.
    *   Get the accumulated **length** of all :class:`Field`'s in a `Sequence`
        via :meth:`field_length()`.
    *   View the **index** for each :class:`Field` in the `Sequence`
        via :meth:`field_indexes()`.
    *   View the **type** for each :class:`Field` in the `Sequence`
        via :meth:`field_types()`.
    *   View the **value** for each :class:`Field` in the `Sequence`
        via :meth:`field_values()`.
    *   List the **item** and its path for each :class:`Field` in the `Sequence`
        as a flat list via :meth:`field_items()`.
    *   Get a **blueprint** of the `Sequence` via :meth:`blueprint()`.

    :param iterable: any *iterable* that contains items of :class:`Structure`,
        :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
        *iterable* is one of these instances itself then the *iterable* itself
        is appended to the `Sequence`.
    """

    item_type = ItemClass.Sequence

    def __init__(self, iterable=None):
        # Data object
        self._data = []

        if iterable is None:
            pass
        elif is_any(iterable):
            self.append(iterable)
        else:
            for name, item in enumerate(iterable):
                if not is_any(item):
                    raise MemberTypeError(self, item, name)
                self.append(item)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, item):
        if not is_any(item):
            raise MemberTypeError(self, item, index)
        self._data[index] = item

    def __delitem__(self, index):
        del self._data[index]

    def __iter__(self):
        return iter(self._data)

    def append(self, item):
        """ Appends the *item* to the end of the `Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        """
        if not is_any(item):
            raise MemberTypeError(self, item, len(self))
        self._data.append(item)

    def insert(self, index, item):
        """ Inserts the *item* before the *index* into the `Sequence`.

        :param int index: `Sequence` index.
        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        """
        if not is_any(item):
            raise MemberTypeError(self, item, len(self))
        self._data.insert(index, item)

    def pop(self, index=-1):
        """ Removes and returns the item at the *index* from the `Sequence`.

        :param int index: `Sequence` index.
        """
        return self._data.pop(index)

    def clear(self):
        """ Remove all items from the `Sequence`."""
        self._data.clear()

    def remove(self, item):
        """ Removes the first occurrence of an *item* from the `Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        """
        self._data.remove(item)

    def reverse(self):
        """ In place reversing of the `Sequence` items."""
        self._data.reverse()

    def extend(self, iterable):
        """ Extends the `Sequence` by appending items from the *iterable*.

        :param iterable: any *iterable* that contains items of :class:`Structure`,
            :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
            *iterable* is one of these instances itself then the *iterable* itself
            is appended to the `Sequence`.
        """
        # Sequence
        if is_sequence(iterable):
            self._data.extend(iterable)
        # Structure
        elif is_structure(iterable):
            members = [item for item in iterable.values()]
            self._data.extend(members)
        # Field
        elif is_field(iterable):
            self._data.extend([iterable])
        else:
            raise MemberTypeError(self, iterable, len(self))

    @nested_option()
    def read_from(self, provider, **options):
        """ All :class:`Pointer` fields in the `Sequence` read the necessary
        amount of bytes from the data :class:`Provider` for their *nested*
        :attr:`~Pointer.data` object fields. Null pointer are ignored.

        :param provider: data :class:`Provider`.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the `data`
            objects of all :class:`Pointer` fields in the `Sequence` reads their
            *nested* `data` object fields as well (chained method call).
            Each :class:`Pointer` field stores the bytes for its *nested*
            :attr:`~Pointer.data` object in its own :attr:`~Pointer.bytestream`.
        """
        for item in iter(self):
            # Container or Pointer
            if is_mixin(item):
                item.read_from(provider, **options)

    @byte_order_option()
    @nested_option()
    def decode(self, buffer=bytes(), index=zero(), **options):
        """ Decodes sequential bytes from the *buffer* starting at the begin
        of the *buffer* or with the given *index* by mapping the bytes to the
        :class:`Field`'s in the `Sequence` in accordance with the decoding
        *byte order* of the *buffer* and the :class:`Field`.

        A specific *byte order* of a :class:`Field` overrules the decoding
        *byte order* of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the last
        :class:`Field` in the `Sequence`.

        Optional the decoding of the *nested* :attr:`~Pointer.data` objects
        of all :class:`Pointer` fields in the `Sequence` can be enabled.

        :param bytes buffer: bytestream.

        :param index: current read :class:`Index` within the *buffer*.

        :keyword byte_order: decoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `Sequence` decodes their *nested* `data` object fields as well
            (chained method call).
            Each :class:`Pointer` field uses for the decoding of its *nested*
            :attr:`~Pointer.data` object its own :attr:`~Pointer.bytestream`.
        """
        for item in iter(self):
            index = item.decode(buffer, index, **options)
        return index

    @byte_order_option()
    @nested_option()
    def encode(self, buffer=bytearray(), index=zero(), **options):
        """ Encodes sequential bytes to the *buffer* starting at the begin of
        the *buffer* or with the given *index* by mapping the *values* of the
        :class:`Field`'s in the `Sequence` to the bytes in accordance with the
        encoding *byte order* of the *buffer* and the :class:`Field`.

        A specific *byte order* of a :class:`Field` overrules the encoding
        *byte order* of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the last
        :class:`Field` in the `Sequence`.

        Optional the encoding of the *nested* :attr:`~Pointer.data` objects
        of all :class:`Pointer` fields in the `Sequence` can be enabled.

        :param bytearray buffer: bytestream.

        :param index: current write :class:`Index` within the *buffer*.

        :keyword byte_order: encoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `Sequence` encodes their *nested* :attr:`~Pointer.data` object
            fields as well (chained method call).
            Each :class:`Pointer` field uses for the encoding of its *nested*
            :attr:`~Pointer.data` object its own :attr:`~Pointer.bytestream`.
        """
        for item in iter(self):
            index = item.encode(buffer, index, **options)
        return index

    @nested_option()
    def next_index(self, index=zero(), **options):
        """ Returns the :class:`Index` after the last :class:`Field`
        in the `Sequence`.

        :param index: :class:`Index` of the first :class:`Field`
            in the `Sequence`.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `Sequence` indexes their *nested* `data` object fields as well
            (chained method call).
        """
        for name, item in enumerate(self):
            # Container
            if is_container(item):
                index = item.next_index(index, **options)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                index = item.next_index(index)
                item.subscript()
            # Field
            elif is_field(item):
                index = item.next_index(index)
            else:
                raise MemberTypeError(self, item, name, index)
        return index

    def initialize(self, content):
        """ Initializes the :class:`Field` items in the `Sequence` with
        the *values* in the *content* list.

        :param list content: a list contains the :class:`Field` values for each
            item in the `Sequence`.
        """
        for name, pair in enumerate(zip(self, content)):
            item, value = pair
            # Container or Pointer
            if is_mixin(item):
                item.initialize(value)
            # Fields
            elif is_field(item):
                item.value = value
            else:
                raise MemberTypeError(self, item, name)

    def first_field(self):
        """ Returns the first :class:`Field` in the `Sequence` or `None` for
        an empty `Sequence`.
        """
        for name, item in enumerate(self):
            # Container
            if is_container(item):
                field = item.first_field()
                # Container is not empty
                if field is not None:
                    return field
            # Field
            elif is_field(item):
                return item
            else:
                raise MemberTypeError(self, item, name)
        return None

    def field_length(self):
        """ Returns the length of the `Sequence` as a tuple in the form of
        ``(number of bytes, remaining number of bits)``.
        """
        length = 0
        for name, item in enumerate(self):
            # Container
            if is_container(item):
                byte_length, bit_length = item.field_length()
                length += bit_length + byte_length * 8
            # Field
            elif is_field(item):
                length += item.bit_size
            else:
                raise MemberTypeError(self, item, name)
        return divmod(length, 8)

    @nested_option()
    def field_indexes(self, index=zero(), **options):
        """ Returns a list which contains ``(name, index)`` tuples for each
        :class:`Field` in the `Sequence`.

        :param index: optional start :class:`Index` of the `Sequence`.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `Sequence` lists their *nested* `data` object fields as well
            (chained method call).
        """
        indexes = list()
        for name, item in enumerate(self):
            # Container
            if is_container(item):
                indexes.append(item.field_indexes(index, **options))
                index = item.next_index(index)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                indexes.append(item.field_indexes(index, **options))
                index = item.next_index(index)
            # Field
            elif is_field(item):
                index = item.next_index(index)
                indexes.append(item.index)
            else:
                raise MemberTypeError(self, item, name, index)
        return indexes

    @nested_option()
    def field_types(self, **options):
        """ Returns a list which contains ``(name, type)`` tuples for each
        :class:`Field` in the `Sequence`.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `Sequence` lists their *nested* `data` object fields as well
            (chained method call).
        """
        types = list()
        for name, item in enumerate(self):
            # Container
            if is_container(item):
                types.append(item.field_types(**options))
            # Pointer
            elif is_pointer(item) and get_nested(options):
                types.append(item.field_types(**options))
            # Field
            elif is_field(item):
                types.append(item.name)
            else:
                raise MemberTypeError(self, item, name)
            return types

    @nested_option()
    def field_values(self, **options):
        """ Returns a list which contains ``(name, value)`` tuples for each
        :class:`Field` in the `Sequence`.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `Sequence` lists their *nested* `data` object fields as well
            (chained method call).
        """
        values = list()
        for name, item in enumerate(self):
            # Container
            if is_container(item):
                values.append(item.field_values(**options))
            # Pointer
            elif is_pointer(item) and get_nested(options):
                values.append(item.field_values(**options))
            # Field
            elif is_field(item):
                values.append(item.value)
            else:
                raise MemberTypeError(self, item, name)
        return values

    @nested_option()
    def field_items(self, root=str(), **options):
        """ Returns a **flat** list which contains the ``(path, item)`` tuples
        for each :class:`Field` in the `Sequence`.

        :param str root: root path.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `data` objects of all :class:`Pointer` fields in the `Sequence`
            list their *nested* `data` object fields as well
            (chained method call).
        """
        base = root if root else str()

        items = list()
        for name, item in enumerate(self):
            path = "{0}[{1}]".format(base, str(name)) if base else ".[{0}]".format(str(name))
            # Container
            if is_container(item):
                for field_item in item.field_items(path, **options):
                    items.append(field_item)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                for field_item in item.field_items(path, **options):
                    items.append(field_item)
            # Field
            elif is_field(item):
                items.append((path, item))
            else:
                raise MemberTypeError(self, item, path)
        return items

    @nested_option(True)
    def blueprint(self, name=str(), **options):
        """ Returns the **blueprint** of the `Sequence` as an
        :class:`ordered dictionary <collections.OrderedDict>`.

        .. code-block:: python

            blueprint = {
                'class': self.__class__.__name__,
                'name': name if name else self.__class__.__name__,
                'size': len(self),
                'type': Sequence.item_type.name
                'member': [
                    item.blueprint('name[idx]') for idx, item in enumerate(self)
                ]
            }

        :param str name: optional name for the `Sequence`.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            `Sequence` lists their *nested* `data` object fields as well
            (chained method call). Default is `True`.
        """
        members = list()
        obj = OrderedDict()
        obj['class'] = self.__class__.__name__
        obj['name'] = name if name else self.__class__.__name__
        obj['size'] = len(self)
        obj['type'] = Sequence.item_type.name
        obj['member'] = members

        for member_name, item in enumerate(self):
            # Container
            if is_container(item):
                members.append(item.blueprint("{0}[{1}]".
                                              format(obj['name'], member_name),
                                              **options))
            # Pointer
            elif is_pointer(item) and get_nested(options):
                members.append(item.blueprint("{0}[{1}]".
                                              format(obj['name'], member_name),
                                              **options))
            # Field
            elif is_field(item):
                members.append(item.blueprint("{0}[{1}]".
                                              format(obj['name'], member_name),
                                              nested=False))
            else:
                raise MemberTypeError(self, item, member_name)
        return obj


class Array(Sequence):
    """ A `Array` is a :class:`Sequence` which contains *elements* of one type.
    The *template* for the `Array` element can be any :class:`Field` instance
    or a *callable* which returns a :class:`Structure`, :class:`Sequence`,
    :class:`Array` or any :class:`Field` instance.

    The constructor method is necessary to ensure that the internal constructor
    for the `Array` element produces complete copies for each `Array` element
    including the *nested* objects in the *template* for the `Array` element.

    A `Array` of :class:`Pointer` fields should use a constructor method
    instead of assigning a :class:`Pointer` field instance directly as the
    `Array` element *template* to ensure that the *nested* :attr:`~Pointer.data`
    object of a :class:`Pointer` field is also complete copied for each
    `Array` element.

    A `Array` adapts and extends a :class:`Sequence` with the following
    features:

    *   **Append** a new `Array` element to the `Array` via :meth:`append()`.
    *   **Insert** a new `Array` element before the *index* into the `Array`
        via :meth:`insert()`.
    *   **Re-size** the `Array` via :meth:`resize()`.

    A `Array` replaces the ``type`` key of the :attr:`~Sequence.blueprint`
    of a :class:`Sequence` with its own `item` type.

    :param template: template for the `Array` element.
        The *template* can be any :class:`Field` instance or any *callable*
        that returns a :class:`Structure`, :class:`Sequence`, :class:`Array`
        or any :class:`Field` instance.

    :param int size: size of the `Array` in number of `Array` elements.
    """
    item_type = ItemClass.Array

    def __init__(self, template, size=0):
        super().__init__()

        # Template for the array element.
        if is_field(template):
            # Field: Array element instance
            self._template = template
        elif callable(template):
            # Callable: Array element factory
            element = template()
            if is_any(element):
                self._template = template
            else:
                raise FactoryTypeError(self, template, element)
        else:
            raise MemberTypeError(self, template)

        # Create array
        self.resize(size)

    def __create__(self):
        # Field: Array element instance
        if is_field(self._template):
            return copy.copy(self._template)
        # Callable: Array element factory
        else:
            return self._template()

    def initialize(self, content):
        """ Initializes the :class:`Field` elements in the `Array` with the
        *values* in the *content* list.

        If the *content* list is shorter than the `Array` then the *content*
        list is used as a rotating fill pattern for the :class:`Field` elements
        in the `Array`.

        :param list content: a list contains the :class:`Field` values for each
            element in the `Array` or one :class:`Field` value for all elements
            in the `Array`.
        """

        if isinstance(content, (list, tuple)):
            size = len(content)
            for i in range(0, len(self), size):
                for name, pair in enumerate(zip(self[i:i + size], content), start=i):
                    item, value = pair
                    # Container or Pointer
                    if is_mixin(item):
                        item.initialize(value)
                    # Fields
                    elif is_field(item):
                        item.value = value
                    else:
                        raise MemberTypeError(self, item, name)
        else:
            for name, item in enumerate(self):
                # Container or Pointer
                if is_mixin(item):
                    item.initialize(content)
                # Fields
                elif is_field(item):
                    item.value = content
                else:
                    raise MemberTypeError(self, item, name)

    def append(self):
        """ Appends a new `Array` element to the `Array`."""
        super().append(self.__create__())

    def insert(self, index):
        """ Inserts a new `Array` element before the *index* of the `Array`.

        :param int index: `Array` index.
        """
        super().insert(index, self.__create__())

    def resize(self, size):
        """ Re-sizes the `Array` by appending new `Array` elements or
        removing `Array` elements from the end.

        :param int size: new size of the `Array` in number of `Array`
            elements.
        """
        count = max(int(size), 0) - len(self)

        if count == 0:
            pass
        elif -count == len(self):
            self.clear()
        elif count > 0:
            for i in range(count):
                self.append()
        else:
            for i in range(abs(count)):
                self.pop()

    def blueprint(self, name=None, **options):
        obj = super().blueprint(name, **options)
        obj['type'] = Array.item_type.name
        return obj


class Field:
    """ The `Field` class is the meta class for all field classes.

    A `Field` has a specific **name**, **bit size**, **byte order**
    and can be **aligned to** other `Field`'s.

    A `Field` has methods to **unpack**, **pack**, **decode** and **encode**
    its field **value** from and to a byte stream and stores its location within
    the byte stream and the providing data source in its field **index**.

    :param int bit_size: is the *size* of the `Field` in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Field` to the number of bytes,
        can be between *1* and *8*.

    :param byte_order: coding :class:`Byteorder` of the field.
        Default is :class:`~Byteorder.auto`.
    """
    item_type = ItemClass.Field

    def __init__(self, bit_size=0, align_to=0, byte_order=Byteorder.auto):
        super().__init__()
        # Field index
        self._index = zero()
        # Field alignment
        self._align_to_byte_size = align_to
        self._align_to_bit_offset = 0
        # Field byte order
        self._byte_order = byte_order
        # Field bit size
        self._bit_size = bit_size
        # Field value
        self._value = None

    def __str__(self):
        return self.name + "({0.index!s}, " \
                           "{0.alignment!s}, " \
                           "{0.bit_size!s}, " \
                           "{0.value!s})".format(self)

    def __repr__(self):
        return self.__class__.__name__ + "(index={0.index!r}, " \
                                         "alignment={0.alignment!r}, " \
                                         "bit_size={0.bit_size!r}, " \
                                         "value={0.value!r})".format(self)

    @property
    def alignment(self):
        """ Returns the alignment of the `Field` (read-only) as a tuple in the
        form of ``(aligns to bytes, bit offset within the aligned bytes)``
        """
        return self._align_to_byte_size, self._align_to_bit_offset

    @property
    def bit_size(self):
        """ Returns the size of the `Field` in bits (read-only)."""
        return self._bit_size

    @property
    def byte_order(self):
        """ Coding :class:`Byteorder` of the `Field`."""
        return self._byte_order

    @byte_order.setter
    def byte_order(self, value):
        if not isinstance(value, Byteorder):
            raise ByteOrderTypeError(self, value)
        self._byte_order = value

    @property
    def index(self):
        """ :class:`Index` of the `Field`."""
        return self._index

    @index.setter
    def index(self, value):
        # Field index
        byte, bit, address, base, update = value

        # Invalid field index
        if byte < 0 or not (0 <= bit <= 64):
            raise FieldIndexError(self, value)

        # Field group size
        group_size, offset = divmod(self.bit_size + bit, 8)
        if offset:
            group_size += 1

        # Bad aligned field group?
        if self.alignment[0] < group_size:
            alignment = group_size, self.alignment[1]
            raise FieldGroupSizeError(self, value, alignment)

        # Bit field?
        if self.is_bit():
            # Bad aligned field group?
            if self.alignment[1] != bit:
                alignment = self.alignment[0], bit
                raise FieldGroupOffsetError(self, value, alignment)
        else:
            # Set field alignment offset
            self._align_to_bit_offset = bit

        # Invalid field address
        if address < 0:
            raise FieldAddressError(self, value, address)

        # Set field index
        self._index = Index(int(byte), int(bit),
                            int(address), int(base),
                            update)

    @property
    def name(self):
        """ Returns the type name of the `Field` (read-only)."""
        return self.item_type.name.capitalize() + str(self.bit_size)

    @property
    def value(self):
        """ Field value."""
        return self._value

    @value.setter
    def value(self, x):
        self._value = x

    @staticmethod
    def is_bit():
        """ Returns `False`."""
        return False

    @staticmethod
    def is_bool():
        """ Returns `False`."""
        return False

    @staticmethod
    def is_decimal():
        """ Returns `False`."""
        return False

    @staticmethod
    def is_float():
        """ Returns `False`."""
        return False

    @staticmethod
    def is_pointer():
        """ Returns `False`."""
        return False

    @staticmethod
    def is_stream():
        """ Returns `False`."""
        return False

    @staticmethod
    def is_string():
        """ Returns `False`."""
        return False

    @abc.abstractmethod
    @byte_order_option()
    def unpack(self, buffer=bytes(), index=zero(), **options):
        """ Unpacks the *value* of the `Field` from the *buffer* at the given
        *index* in accordance with the decoding *byte order* of the *buffer* and
        the `Field`.

        A specific *byte order* of a `Field` overrules the decoding *byte order*
        of the *buffer*.

        Returns the decoded field *value*.

        :param bytes buffer: bytestream.

        :param index: current read :class:`Index` within the *buffer*.

        :keyword byte_order: decoding :class:`Byteorder` of the *buffer*.

        .. note:: This abstract method must be implemented by a derived class.
        """
        # Returns the decoded field value.
        return None

    @abc.abstractmethod
    @byte_order_option()
    def pack(self, buffer=bytearray(), **options):
        """ Packs the *value* of the `Field` to the *buffer* at the given *index*
        in accordance with the encoding *byte order* of the *buffer* and the `Field`.

        A specific *byte order* of a `Field` overrules the encoding *byte order*
        of the *buffer*.

        Returns the :class:`bytes` encoded field *value*.

        :param bytearray buffer: bytestream.

        :keyword byte_order: encoding :class:`Byteorder` of the *buffer*.

        .. note:: This abstract method must be implemented by a derived class.
        """
        # Returns the byte encoded field value.
        return bytes()

    @byte_order_option()
    @nested_option()
    def decode(self, buffer=bytes(), index=zero(), **options):
        """ Decodes sequential bytes from the *buffer* starting at the begin of
        the *buffer* or with the given *index* by mapping the bytes to the *value*
        of the `Field` in accordance with the decoding *byte order* of the
        *buffer* and the `Field`.

        A specific *byte order* of a `Field` overrules the decoding *byte order*
        of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the `Field`.

        Optional the decoding of the *nested* :attr:`~Pointer.data` object
        of a :class:`Pointer` field can be enabled.

        :param bytes buffer: bytestream.

        :param index: current read :class:`Index` within the *buffer*.

        :keyword byte_order: decoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` a :class:`Pointer` field decodes its
            *nested* `data` object fields as well (chained method call).
            Each :class:`Pointer` field uses for the decoding of its *nested*
            :attr:`~Pointer.data` object its own :attr:`~Pointer.bytestream`.
        """
        self.index = index
        self._value = self.unpack(buffer, index, **options)
        return self.next_index(index)

    @byte_order_option()
    @nested_option()
    def encode(self, buffer=bytearray(), index=zero(), **options):
        """ Encodes sequential bytes to the *buffer* starting at the begin of
        the *buffer* or with the given *index* by mapping the *value* of the
        `Field` to the bytes in accordance with the encoding *byte order* of
        the *buffer* and the `Field`.

        A specific *byte order* of a `Field` overrules the encoding *byte order*
        of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the `Field`.

        Optional the encoding of the *nested* :attr:`~Pointer.data` object
        of a :class:`Pointer` field can be enabled.

        :param bytearray buffer: bytestream.

        :param index: current write :class:`Index` of the *buffer*.

        :keyword byte_order: encoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` a :class:`Pointer` field encodes its
            *nested* `data` object fields as well (chained method call).
            Each :class:`Pointer` field uses for the encoding of its *nested*
            :attr:`~Pointer.data` object its own :attr:`~Pointer.bytestream`.
        """
        self.index = index
        buffer += self.pack(buffer, **options)
        return self.next_index(index)

    def next_index(self, index=zero()):
        """ Returns the :class:`Index` after the `Field`.

        :param index: start :class:`Index` for the `Field`.
        """
        # Set field index
        # Note: Updates the field alignment offset as well
        self.index = index

        # Bit offset for the next field
        byte, bit, address, base, update = index
        bit += self.bit_size

        # Field group size
        group_size, offset = divmod(bit, 8)

        # Field alignment size
        field_size, _ = self.alignment

        # End of field group?
        if field_size == group_size:
            # Bad aligned field group?
            if offset is not 0:
                alignment = group_size + 1, self.alignment[1]
                raise FieldGroupSizeError(self, index, alignment)
            else:
                # Move byte index for the next field group
                byte += field_size
                # Reset bit offset for the next field group
                bit = 0
                # Move address for the next field group
                address += field_size
        # Index for the next field
        return Index(byte, bit, address, base, update)

    @nested_option(True)
    def blueprint(self, name=str(), **options):
        """ Returns the **blueprint** of a `Field` as an
        :class:`ordered dictionary <collections.OrderedDict>`.

        .. code-block:: python

            blueprint = {
                'address': self.index.address,
                'alignment': [self.alignment[0], self.alignment[1]],
                'class': self.name,
                'index': [self.index.byte, self.index.bit],
                'name': name if name else self.name,
                'order': self.byteorder.value,
                'size': self.bit_size,
                'type': Field.item_type.name,
                'value': self.value
            }

        :param str name: optional name for the `Field`.

        :keyword bool nested: if `True` a :class:`Pointer` field lists its
            *nested* :attr:`~Pointer.data` object fields as well
            (chained method call). Default is `True`.
        """
        obj = {
            'address': self.index.address,
            'alignment': [self.alignment[0], self.alignment[1]],
            'class': self.name,
            'order': self.byte_order.value,
            'index': [self.index.byte, self.index.bit],
            'name': name if name else self.name,
            'size': self.bit_size,
            'type': Field.item_type.name,
            'value': self.value
        }
        return OrderedDict(sorted(obj.items()))


class Stream(Field):
    """ A `Stream` field is a :class:`Field` with a variable *size* and
    returns its field *value* as a hexadecimal encoded string.

    Internally a `Stream` field uses a :class:`bytes` class to store the
    data of its field *value*.

    A `Stream` field is:

    *   *containable*: ``item in self`` returns `True` if *item* is part
        of the `Stream` field.
    *   *sized*: ``len(self)`` returns the length of the `Stream` field.
    *   *subscriptable* ``self[index]`` returns the *byte* at the *index*
        of the `Stream` field.
    *   *iterable* ``iter(self)`` iterates over the bytes of the `Stream`
        field.

    :param int size: is the *size* of the `Stream` field in bytes.

    Example:

    >>> stream = Stream()
    >>> stream.is_stream()
    True
    >>> stream.name
    'Stream'
    >>> stream.alignment
    (0, 0)
    >>> stream.byte_order
    Byteorder.auto = 'auto'
    >>> stream.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> stream.next_index()
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> stream.bit_size
    0
    >>> stream.value
    b''
    >>> stream.resize(10)
    >>> stream.name
    'Stream10'
    >>> stream.alignment
    (10, 0)
    >>> stream.bit_size
    80
    >>> stream.next_index()
    Index(byte=10, bit=0, address=10, base_address=0, update=False)
    >>> stream.value
    b'00000000000000000000'
    >>> stream.value = '0102030405'
    >>> stream.value
    b'01020304050000000000'
    >>> stream.resize(15)
    >>> stream.value
    b'010203040500000000000000000000'
    >>> stream.resize(10)
    >>> stream.value = '0102030405060708090a0b0c'
    >>> stream.value
    b'0102030405060708090a'
    >>> len(stream)
    10
    >>> [byte for byte in stream]  # converts to int
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> [hex(byte) for byte in stream]
    ['0x1', '0x2', '0x3', '0x4', '0x5', '0x6', '0x7', '0x8', '0x9', '0xa']
    >>> stream[5]  # converts to int
    6
    >>> 7 in stream
    True
    >>> 0x0 in stream
    False
    >>> hexlify(stream[5:])  # converts to bytes
    b'060708090a'
    >>> pprint(stream.blueprint())
    {'address': 0,
     'alignment': [10, 0],
     'class': 'Stream10',
     'index': [0, 0],
     'name': 'Stream10',
     'order': 'auto',
     'size': 80,
     'type': 'Field',
     'value': '0102030405060708090a'}
    """
    item_type = ItemClass.Stream

    def __init__(self, size=0):
        super().__init__()
        # Field value
        self._value = bytes()
        # Stream size
        self.resize(size)

    def __contains__(self, key):
        return key in self._value

    def __len__(self):
        return len(self._value)

    def __getitem__(self, key):
        return self._value[key]

    def __iter__(self):
        return iter(self._value)

    @property
    def name(self):
        """ Returns the type name of the `Stream` field (read-only)."""
        size = len(self)
        if size > 0:
            return self.item_type.name.capitalize() + str(size)
        else:
            return self.item_type.name.capitalize()

    @property
    def value(self):
        """ Field value."""
        return hexlify(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_stream(x, encoding='hex')

    @staticmethod
    def is_stream():
        """ Returns `True`."""
        return True

    def to_stream(self, value, encoding='hex'):
        if isinstance(value, str):
            if encoding == 'hex':
                bytestream = bytes.fromhex(value)
            elif encoding == 'ascii':
                bytestream = value.encode('ascii')
            else:
                raise FieldValueEncodingError(self, self.index, encoding)
        elif isinstance(value, (bytearray, bytes)):
            bytestream = bytes(value)
        else:
            raise FieldTypeError(self, self.index, value)
        bytestream = bytestream[:len(self)]
        bytestream += b'\x00' * max(len(self) - len(bytestream), 0)
        return bytestream

    @byte_order_option()
    def unpack(self, buffer=bytes(), index=zero(), **options):
        # Bad placed field
        if index.bit:
            raise FieldIndexError(self, index)

        # Content of the buffer mapped by the field
        offset = self.index.byte
        size = offset + len(self)
        return buffer[offset:size]

    @byte_order_option()
    def pack(self, buffer=bytearray(), **options):
        # Bad placed field
        if self.index.bit:
            raise FieldIndexError(self, self.index)
        return self._value

    def resize(self, size):
        """ Re-sizes the `Stream` field by appending zero bytes or
        removing bytes from the end.

        :param int size: `Stream` size in number of bytes.
        """
        count = max(int(size), 0) - len(self)

        if count == 0:
            pass
        elif -count == len(self):
            self._value = bytes()
        elif count > 0:
            self._value += b'\x00' * count
        else:
            self._value = self._value[:count]
        size = len(self)
        self._bit_size = size * 8
        self._align_to_byte_size = size

    def blueprint(self, name=str(), **options):
        obj = super().blueprint(name, **options)
        obj['value'] = str(obj['value']).replace("b'", "").replace("'", "")
        return obj


class String(Stream):
    """ A `String` field is a :class:`Stream` field with a variable *size* and
    returns its field *value* as a zero terminated ascii encoded string.

    A `String` field is:

    *   *containable*: ``item in self`` returns `True` if *item* is part
        of the `String` field.
    *   *sized*: ``len(self)`` returns the length of the `String` field.
    *   *subscriptable* ``self[index]`` returns the *byte* at the *index*
        of the `String` field.
    *   *iterable* ``iter(self)`` iterates over the bytes of the `String`
        field.

    :param int size: is the *size* of the `String` field in bytes.

    Example:

    >>> string = String()
    >>> string.is_stream()
    True
    >>> string.is_string()
    True
    >>> string.is_terminated()
    False
    >>> string.name
    'String'
    >>> string.alignment
    (0, 0)
    >>> string.byte_order
    Byteorder.auto = 'auto'
    >>> string.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> string.next_index()
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> string.bit_size
    0
    >>> string.value
    ''
    >>> string.resize(10)
    >>> string.name
    'String10'
    >>> string.alignment
    (10, 0)
    >>> string.bit_size
    80
    >>> string.next_index()
    Index(byte=10, bit=0, address=10, base_address=0, update=False)
    >>> string.value
    ''
    >>> string.value = 'KonFoo'
    >>> string.value
    'KonFoo'
    >>> string.resize(3)
    >>> string.value
    'Kon'
    >>> string.resize(10)
    >>> string.value
    'Kon'
    >>> string.value = 'KonFoo is Fun'
    >>> string.value
    'KonFoo is '
    >>> len(string)
    10
    >>> [byte for byte in string]  # converts to int
    [75, 111, 110, 70, 111, 111, 32, 105, 115, 32]
    >>> [chr(byte) for byte in string]  # converts to int
    ['K', 'o', 'n', 'F', 'o', 'o', ' ', 'i', 's', ' ']
    >>> chr(string[5])  # converts to int -> chr
    'o'
    >>> ord(' ') in string
    True
    >>> 0x0 in string
    False
    >>> string[:6]  # converts to bytes
    b'KonFoo'
    >>> string[3:6]  # converts to bytes
    b'Foo'
    >>> pprint(string.blueprint())
    {'address': 0,
     'alignment': [10, 0],
     'class': 'String10',
     'index': [0, 0],
     'name': 'String10',
     'order': 'auto',
     'size': 80,
     'type': 'Field',
     'value': 'KonFoo is '}
    """
    item_type = ItemClass.String

    @property
    def value(self):
        """ Field value."""
        length = self._value.find(b'\x00')
        if length >= 0:
            return self._value[:length].decode('ascii')
        else:
            return self._value.decode('ascii')

    @value.setter
    def value(self, x):
        self._value = self.to_stream(x, encoding='ascii')

    @staticmethod
    def is_string():
        """ Returns `True`."""
        return True

    def is_terminated(self):
        """ Returns `True` if the `String` field is zero-terminated."""
        return self._value.find(b'\x00') >= 0


class Float(Field):
    """ A `Float` field is a :class:`Field` with a fix *size* of four bytes
    and returns its field *value* as a single float.

    Internally a `Float` field uses a :class:`float` class to store the
    data of its field *value*.

    A `Float` field extends the :attr:`~Field.blueprint` of a :class:`Field`
    with a ``max`` and ``min`` key for its maximum and minimum possible field
    *value*.

    :param byte_order: coding :class:`Byteorder` of the `Float` field.

    Example:

    >>> real = Float()
    >>> real.is_float()
    True
    >>> real.name
    'Float32'
    >>> real.alignment
    (4, 0)
    >>> real.byte_order
    Byteorder.auto = 'auto'
    >>> real.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> real.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> real.bit_size
    32
    >>> real.min()
    -3.4028234663852886e+38
    >>> real.max()
    3.4028234663852886e+38
    >>> real.smallest()
    1.1754943508222875e-38
    >>> real.epsilon()
    5.960464477539063e-08
    >>> real.value
    0.0
    >>> real.value = 0x10
    >>> real.value
    16.0
    >>> real.value = -3.4028234663852887e+38
    >>> real.value
    -3.4028234663852886e+38
    >>> real.value = 3.4028234663852887e+38
    >>> real.value
    3.4028234663852886e+38
    >>> pprint(real.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'Float32',
     'index': [0, 0],
     'max': 3.4028234663852886e+38,
     'min': -3.4028234663852886e+38,
     'name': 'Float32',
     'order': 'auto',
     'size': 32,
     'type': 'Field',
     'value': 3.4028234663852886e+38}
    """
    item_type = ItemClass.Float

    def __init__(self, byte_order=Byteorder.auto):
        super().__init__(bit_size=32, align_to=4, byte_order=byte_order)
        # Field value
        self._value = float()

    @property
    def value(self):
        """ Field value."""
        return float(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_float(x)

    @staticmethod
    def is_float():
        """ Returns `True`."""
        return True

    def to_float(self, value):
        return limiter(float(value), self.min(), self.max())

    @staticmethod
    def epsilon():
        return 2 ** -24

    @staticmethod
    def smallest():
        return 2 ** -126

    @staticmethod
    def max():
        """ Returns the maximal possible field *value* of the `Float` field."""
        return (1 - Float.epsilon()) * 2 ** 128

    @staticmethod
    def min():
        """ Returns the minimal possible field *value* of the `Float` field."""
        return -(1 - Float.epsilon()) * 2 ** 128

    @byte_order_option()
    def unpack(self, buffer=bytes(), index=zero(), **options):
        # Bad placed field
        if index.bit:
            raise FieldIndexError(self, index)

        # Decoding byte order of the buffer
        byte_order = get_byte_order(options)

        # Field byte order overrules!
        if self.byte_order is not Byteorder.auto:
            byte_order = self.byte_order

        # Content of the buffer mapped by the field
        offset = index.byte
        size = offset + self.alignment[0]
        content = buffer[offset:size]

        # Not enough content!
        if len(content) != 4:
            return float()

        # Unpack the content from the buffer
        if byte_order is Byteorder.big:
            return struct.unpack('>f', content)[0]
        else:
            return struct.unpack('<f', content)[0]

    @byte_order_option()
    def pack(self, buffer=bytearray(), **options):
        # Bad placed field
        if self.index.bit:
            raise FieldIndexError(self, self.index)

        # Encoding byte order of the buffer
        byte_order = get_byte_order(options)

        # Field byte order overrules!
        if self.byte_order is not Byteorder.auto:
            byte_order = self.byte_order

        # Pack the field value to bytes
        if byte_order is Byteorder.big:
            return struct.pack('>f', self._value)
        else:
            return struct.pack('<f', self._value)

    def blueprint(self, name=str(), **options):
        obj = super().blueprint(name, **options)
        obj['max'] = self.max()
        obj['min'] = self.min()
        return OrderedDict(sorted(obj.items()))


class Decimal(Field):
    """ A `Decimal` field is a :class:`Field` with a variable *size*
    and returns its field *value* as a integer number.

    Internally a `Decimal` field uses a :class:`int` class to store the
    data of its field *value*.

    A `Decimal` field extends the :attr:`~Field.blueprint` of a :class:`Field`
    with a ``max`` and ``min`` key for its maximum and minimum possible field
    *value* and a ``sigend`` key to mark the decimal number as signed or
    unsigned.

    :param int bit_size: is the *size* of the `Decimal` field in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Decimal` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Decimal` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Decimal` field.

    :param bool signed: if `True` the `Decimal` field is signed otherwise
        unsigned.

    :param byte_order: coding :class:`Byteorder` of the `Decimal` field.

    Example:

    >>> unsigned = Decimal(16)
    >>> unsigned.is_decimal()
    True
    >>> unsigned.name
    'Decimal16'
    >>> unsigned.alignment
    (2, 0)
    >>> unsigned.byte_order
    Byteorder.auto = 'auto'
    >>> unsigned.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> unsigned.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unsigned.bit_size
    16
    >>> unsigned.min()
    0
    >>> unsigned.max()
    65535
    >>> unsigned.signed
    False
    >>> unsigned.value
    0
    >>> unsigned.decode(bytes.fromhex('0080'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unsigned.value
    32768
    >>> unsigned.value = 0x4000
    >>> unsigned.value
    16384
    >>> unsigned.value = -1
    >>> unsigned.value
    0
    >>> unsigned.value = 65536
    >>> unsigned.value
    65535
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> unsigned.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffff'
    >>> pprint(unsigned.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Decimal16',
     'index': [0, 0],
     'max': 65535,
     'min': 0,
     'name': 'Decimal16',
     'order': 'auto',
     'signed': False,
     'size': 16,
     'type': 'Field',
     'value': 65535}

    Example:

    >>> signed = Decimal(16, signed=True)
    >>> signed.is_decimal()
    True
    >>> signed.name
    'Decimal16'
    >>> signed.alignment
    (2, 0)
    >>> signed.byte_order
    Byteorder.auto = 'auto'
    >>> signed.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> signed.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> signed.bit_size
    16
    >>> signed.min()
    -32768
    >>> signed.max()
    32767
    >>> signed.signed
    True
    >>> signed.value
    0
    >>> signed.decode(bytes.fromhex('00c0'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> signed.value
    -16384
    >>> signed.value = -0x4000
    >>> signed.value
    -16384
    >>> signed.value = -32769
    >>> signed.value
    -32768
    >>> signed.value = 32768
    >>> signed.value
    32767
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> signed.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ff7f'
    >>> pprint(signed.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Decimal16',
     'index': [0, 0],
     'max': 32767,
     'min': -32768,
     'name': 'Decimal16',
     'order': 'auto',
     'signed': True,
     'size': 16,
     'type': 'Field',
     'value': 32767}
    """
    item_type = ItemClass.Decimal

    def __init__(self, bit_size, align_to=None, signed=False,
                 byte_order=Byteorder.auto):
        super().__init__(byte_order=byte_order)
        # Field signed?
        self._signed = bool(signed)
        # Field alignment, Field bit size
        if align_to:
            self._set_alignment(byte_size=align_to)
            self._set_bit_size(bit_size)
        else:
            self._set_bit_size(bit_size, auto_align=True)
        # Field value
        self._value = int()

    @property
    def value(self):
        """ Field value."""
        return int(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)

    @property
    def signed(self):
        """ Returns `True` if the `Decimal` field is signed."""
        return self._signed

    @signed.setter
    def signed(self, value):
        self._signed = bool(value)
        self._value = self._cast(self._value, self.min(), self.max(), self._signed)

    @staticmethod
    def is_decimal():
        """ Returns `True`."""
        return True

    def to_decimal(self, value, encoding=None):
        if isinstance(value, str):
            if encoding is None:
                decimal = int(value, 0)
            elif encoding == 'ascii':
                decimal = ord(value[:1])
            else:
                raise FieldValueEncodingError(self, self.index, encoding)
        else:
            decimal = int(value)
        return limiter(decimal, self.min(), self.max())

    def _set_alignment(self, byte_size, bit_offset=0, auto_align=False):
        # Field alignment offset
        field_offset = int(bit_offset)

        # Auto alignment
        if auto_align:
            # Field alignment size
            field_size, offset = divmod(field_offset, 8)
            if offset is not 0:
                field_size += 1
            field_size = max(field_size, 1)
        # No auto alignment
        else:
            # Field alignment size
            field_size = int(byte_size)

        # Field alignment
        alignment = field_size, field_offset

        # Invalid field alignment size
        if field_size not in (1, 2, 3, 4, 5, 6, 7, 8):
            raise FieldAlignmentError(self, self.index, alignment)

        # Invalid field alignment offset
        if not (0 <= field_offset <= 63):
            raise FieldAlignmentError(self, self.index, alignment)

        # Invalid field alignment
        if field_offset >= field_size * 8:
            raise FieldAlignmentError(self, self.index, alignment)

        # Set field alignment
        self._align_to_byte_size = field_size
        self._align_to_bit_offset = field_offset

    def _set_bit_size(self, size, step=1, auto_align=False):
        # Field size
        bit_size = int(size)

        # Invalid field size
        if bit_size % step != 0 or not (1 <= bit_size <= 64):
            raise FieldSizeError(self, self.index, bit_size)

        # Field group size
        group_size, offset = divmod(bit_size, 8)
        # Auto alignment
        if auto_align:
            if offset is not 0:
                self._align_to_byte_size = group_size + 1
            else:
                self._align_to_byte_size = group_size
        # Invalid field alignment
        elif group_size > self.alignment[0]:
            alignment = group_size, self.alignment[1]
            raise FieldAlignmentError(self, self.index, alignment)
        # Set field size
        self._bit_size = bit_size

    def _cast(self, value, minimum, maximum, signed):
        # Sign conversion
        if minimum <= value <= maximum:
            return value
        elif signed:
            return value | ~self.bit_mask()
        else:
            return value & self.bit_mask()

    def _max(self, signed):
        # Maximal possible field value
        if signed:
            return 2 ** (self._bit_size - 1) - 1
        else:
            return 2 ** self._bit_size - 1

    def _min(self, signed):
        # Minimal possible field value
        if signed:
            return -2 ** (self._bit_size - 1)
        else:
            return 0

    def bit_mask(self):
        return 2 ** self._bit_size - 1

    def max(self):
        """ Returns the maximal possible field *value* of the `Decimal` field."""
        return self._max(self._signed)

    def min(self):
        """ Returns the minimal possible field *value* of the `Decimal` field."""
        return self._min(self._signed)

    def as_unsigned(self):
        """ Returns the field *value* of the `Decimal` field as an unsigned integer."""
        return self._cast(self._value, self._min(False), self._max(False), False)

    def as_signed(self):
        """ Returns the field *value* of the `Decimal` field as a signed integer."""
        return self._cast(self._value, self._min(True), self._max(True), True)

    @byte_order_option()
    def unpack(self, buffer=bytes(), index=zero(), **options):
        # Content of the buffer mapped by the field group
        offset = index.byte
        size = offset + self.alignment[0]
        content = buffer[offset:size]

        # Decoding byte order of the buffer
        byte_order = get_byte_order(options)

        # Decode field value from the buffer
        value = int.from_bytes(content, byte_order.value)
        value >>= index.bit
        value &= self.bit_mask()

        # Field alignment
        field_size, field_offset = divmod(self.bit_size, 8)

        # Byte order conversion for field value necessary?
        if self.byte_order is Byteorder.auto:
            # No specific field byte order
            pass
        elif self.byte_order is byte_order:
            # Field byte order matches the
            # decoding byte order of the buffer
            pass
        elif field_size < 1:
            # Byte order not relevant for field's smaller than one byte
            pass
        elif field_offset != 0:
            # Bad sized field for independent byte order conversion
            raise FieldGroupByteOrderError(self, index, byte_order)
        elif field_size == 1:
            # Byte order not relevant for field's with one byte
            pass
        else:
            # Convert byte order of the field value
            value = int.from_bytes(value.to_bytes(field_size, byte_order.value),
                                   self.byte_order.value)

        # Limit field value
        if value > self.max():
            value |= ~self.bit_mask()
        return value

    @byte_order_option()
    def pack(self, buffer=bytearray(), **options):
        # Field value
        value = limiter(self._value, self.min(), self.max())
        value &= self.bit_mask()

        # Encoding byte order of the buffer
        byte_order = get_byte_order(options)

        # Field alignment
        field_size, field_offset = divmod(self.bit_size, 8)

        # Byte order conversion for field value necessary?
        if self.byte_order is Byteorder.auto:
            # No specific field byte order
            pass
        elif self.byte_order is byte_order:
            # Field byte order matches the
            # encoding byte order of the buffer
            pass
        elif field_size < 1:
            # Byte order not relevant for field's smaller than one byte
            pass
        elif field_offset != 0:
            # Bad sized field for independent byte order conversion
            raise FieldGroupByteOrderError(self, self.index, byte_order)
        elif field_size == 1:
            # Byte order not relevant for field's with one byte
            pass
        else:
            # Convert byte order of the field value
            value = int.from_bytes(value.to_bytes(field_size, self.byte_order.value),
                                   byte_order.value)

        # Shift the field value to its field group offset
        value <<= self.index.bit

        # Content for the buffer mapped by the field group
        offset = self.index.byte
        size = offset + self.alignment[0]
        if len(buffer) == size:
            # Map the field value into the existing field group content of the buffer
            view = memoryview(buffer)
            value |= int.from_bytes(buffer[offset:size], byte_order.value)
            view[offset:size] = value.to_bytes(self.alignment[0],
                                               byte_order.value)
            return bytes()
        else:
            # Extent the buffer with the field group content and the field value
            return value.to_bytes(self.alignment[0], byte_order.value)

    def blueprint(self, name=None, **options):
        obj = super().blueprint(name, **options)
        obj['max'] = self.max()
        obj['min'] = self.min()
        obj['signed'] = self.signed
        return OrderedDict(sorted(obj.items()))


class Bit(Decimal):
    """ A `Bit` field is an unsigned :class:`Decimal` with a *size* of
    one bit and returns its field *value* as an unsigned integer number.

    :param int number: is the bit offset of the `Bit` field within the
        aligned bytes, can be between *0* and *63*.

    :param int align_to: aligns the `Bit` field to the number of bytes,
        can be between *1* and *8*.

    Example:

    >>> bit = Bit(0)
    >>> bit.is_decimal()
    True
    >>> bit.is_bit()
    True
    >>> bit.name
    'Bit'
    >>> bit.alignment
    (1, 0)
    >>> bit.byte_order
    Byteorder.auto = 'auto'
    >>> bit.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> bit.next_index()
    Index(byte=0, bit=1, address=0, base_address=0, update=False)
    >>> bit.signed
    False
    >>> bit.value
    0
    >>> bit.decode(bytes.fromhex('01'))
    Index(byte=0, bit=1, address=0, base_address=0, update=False)
    >>> bit.value
    1
    >>> bit.value = 0
    >>> bit.value
    0
    >>> bit.value = False
    >>> bit.value
    0
    >>> bit.value = True
    >>> bit.value
    1
    >>> bit.value = -1
    >>> bit.value
    0
    >>> bit.value = 2
    >>> bit.value
    1
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> bit.encode(bytestream)
    Index(byte=0, bit=1, address=0, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'01'
    >>> pprint(bit.blueprint())
    {'address': 0,
     'alignment': [1, 0],
     'class': 'Bit',
     'index': [0, 0],
     'max': 1,
     'min': 0,
     'name': 'Bit',
     'order': 'auto',
     'signed': False,
     'size': 1,
     'type': 'Field',
     'value': 1}
    """
    item_type = ItemClass.Bit

    def __init__(self, number, align_to=None):
        super().__init__(bit_size=1, align_to=align_to)
        # Field alignment
        if align_to:
            self._set_alignment(byte_size=align_to, bit_offset=number)
        else:
            self._set_alignment(byte_size=0, bit_offset=number, auto_align=True)

    @property
    def name(self):
        """ Returns the type name of the `Bit` field (read-only)."""
        return self.item_type.name.capitalize()

    @staticmethod
    def is_bit():
        """ Returns `True`."""
        return True


class Byte(Decimal):
    """ A `Byte` field is an unsigned :class:`Decimal` field with a *size* of
    one byte and returns its field *value* as a hexadecimal encoded string.

    :param int align_to: aligns the `Byte` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Byte` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Byte` field.

    Example:

    >>> byte = Byte()
    >>> byte.is_decimal()
    True
    >>> byte.name
    'Byte'
    >>> byte.alignment
    (1, 0)
    >>> byte.byte_order
    Byteorder.auto = 'auto'
    >>> byte.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> byte.next_index()
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> byte.bit_size
    8
    >>> byte.min()
    0
    >>> byte.max()
    255
    >>> byte.signed
    False
    >>> byte.value
    '0x0'
    >>> byte.decode(bytes.fromhex('20'))
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> byte.value
    '0x20'
    >>> byte.value = 16
    >>> byte.value
    '0x10'
    >>> byte.value = -1
    >>> byte.value
    '0x0'
    >>> byte.value = 256
    >>> byte.value
    '0xff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> byte.encode(bytestream)
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ff'
    >>> pprint(byte.blueprint())
    {'address': 0,
     'alignment': [1, 0],
     'class': 'Byte',
     'index': [0, 0],
     'max': 255,
     'min': 0,
     'name': 'Byte',
     'order': 'auto',
     'signed': False,
     'size': 8,
     'type': 'Field',
     'value': '0xff'}
    """
    item_type = ItemClass.Byte

    def __init__(self, align_to=None):
        super().__init__(bit_size=8, align_to=align_to)

    @property
    def name(self):
        """ Returns the type name of the `Byte` field (read-only)."""
        return self.item_type.name.capitalize()

    @property
    def value(self):
        """ Field value."""
        return hex(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)


class Char(Decimal):
    """ A `Char` field is an unsigned :class:`Decimal` field with a *size* of
    one byte and returns its field *value* as a unicode encoded string.

    :param int align_to: aligns the `Char` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Char` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Char` field.

    Example:

    >>> char = Char()
    >>> char.is_decimal()
    True
    >>> char.name
    'Char'
    >>> char.alignment
    (1, 0)
    >>> char.byte_order
    Byteorder.auto = 'auto'
    >>> char.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> char.next_index()
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> char.bit_size
    8
    >>> char.min()
    0
    >>> char.max()
    255
    >>> char.signed
    False
    >>> ord(char.value)
    0
    >>> char.decode(bytes.fromhex('41'))
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> char.value
    'A'
    >>> char.value = 66
    >>> char.value
    'B'
    >>> char.value = 0x41
    >>> char.value
    'A'
    >>> char.value = 'F'
    >>> char.value
    'F'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> char.encode(bytestream)
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'46'
    >>> pprint(char.blueprint())
    {'address': 0,
     'alignment': [1, 0],
     'class': 'Char',
     'index': [0, 0],
     'max': 255,
     'min': 0,
     'name': 'Char',
     'order': 'auto',
     'signed': False,
     'size': 8,
     'type': 'Field',
     'value': 'F'}
    """
    item_type = ItemClass.Char

    def __init__(self, align_to=None):
        super().__init__(bit_size=8, align_to=align_to)

    @property
    def name(self):
        """ Returns the type name of the `Char` field (read-only)."""
        return self.item_type.name.capitalize()

    @property
    def value(self):
        """ Field value."""
        return chr(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x, encoding='ascii')


class Signed(Decimal):
    """ A `Signed` field is a signed :class:`Decimal` field with a variable
    *size* and returns its field *value* as a signed integer number.

    :param int bit_size: is the *size* of the `Signed` field in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Signed` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Signed` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Signed` field.

    :param byte_order: coding :class:`Byteorder` of the `Signed` field.

    Example:

    >>> signed = Signed(16)
    >>> signed.is_decimal()
    True
    >>> signed.name
    'Signed16'
    >>> signed.alignment
    (2, 0)
    >>> signed.byte_order
    Byteorder.auto = 'auto'
    >>> signed.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> signed.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> signed.bit_size
    16
    >>> signed.min()
    -32768
    >>> signed.max()
    32767
    >>> signed.signed
    True
    >>> signed.value
    0
    >>> signed.decode(bytes.fromhex('00c0'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> signed.value
    -16384
    >>> signed.value = -0x4000
    >>> signed.value
    -16384
    >>> signed.value = -32769
    >>> signed.value
    -32768
    >>> signed.value = 32768
    >>> signed.value
    32767
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> signed.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ff7f'
    >>> pprint(signed.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Signed16',
     'index': [0, 0],
     'max': 32767,
     'min': -32768,
     'name': 'Signed16',
     'order': 'auto',
     'signed': True,
     'size': 16,
     'type': 'Field',
     'value': 32767}
    """
    item_type = ItemClass.Signed

    def __init__(self, bit_size, align_to=None, byte_order=Byteorder.auto):
        super().__init__(bit_size, align_to, True, byte_order)


class Unsigned(Decimal):
    """ A `Unsigned` field is an unsigned :class:`Decimal` field with a
    variable *size* and returns its field *value* as a hexadecimal encoded
    string.

    :param int bit_size: is the *size* of the `Unsigned` field in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Unsigned` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Unsigned` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Unsigned` field.

    :param byte_order: coding :class:`Byteorder` of the `Unsigned` field.

    Example:

    >>> unsigned = Unsigned(16)
    >>> unsigned.is_decimal()
    True
    >>> unsigned.name
    'Unsigned16'
    >>> unsigned.alignment
    (2, 0)
    >>> unsigned.byte_order
    Byteorder.auto = 'auto'
    >>> unsigned.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> unsigned.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unsigned.bit_size
    16
    >>> unsigned.min()
    0
    >>> unsigned.max()
    65535
    >>> unsigned.signed
    False
    >>> unsigned.value
    '0x0'
    >>> unsigned.decode(bytes.fromhex('00c0'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unsigned.value
    '0xc000'
    >>> unsigned.value = 0x4000
    >>> unsigned.value
    '0x4000'
    >>> unsigned.value = -0x1
    >>> unsigned.value
    '0x0'
    >>> unsigned.value = 0x10000
    >>> unsigned.value
    '0xffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> unsigned.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffff'
    >>> pprint(unsigned.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Unsigned16',
     'index': [0, 0],
     'max': 65535,
     'min': 0,
     'name': 'Unsigned16',
     'order': 'auto',
     'signed': False,
     'size': 16,
     'type': 'Field',
     'value': '0xffff'}
    """
    item_type = ItemClass.Unsigned

    def __init__(self, bit_size, align_to=None, byte_order=Byteorder.auto):
        super().__init__(bit_size, align_to, False, byte_order)

    @property
    def value(self):
        """ Field value."""
        return hex(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)


class Bitset(Decimal):
    """ A `Bitset` field is an unsigned :class:`Decimal` field with a variable
    *size* and returns its field *value* as a binary encoded string.

    :param int bit_size: is the *size* of the `Bitset` field in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Bitset` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Bitset` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Bitset` field.

    :param byte_order: coding :class:`Byteorder` of the `Bitset` field.

    Example:

    >>> bitset = Bitset(16)
    >>> bitset.is_decimal()
    True
    >>> bitset.name
    'Bitset16'
    >>> bitset.alignment
    (2, 0)
    >>> bitset.byte_order
    Byteorder.auto = 'auto'
    >>> bitset.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> bitset.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bitset.bit_size
    16
    >>> bitset.min()
    0
    >>> bitset.max()
    65535
    >>> bitset.signed
    False
    >>> bitset.value
    '0b0000000000000000'
    >>> bitset.decode(bytes.fromhex('f00f'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bitset.value
    '0b0000111111110000'
    >>> bitset.value = 0b1111
    >>> bitset.value
    '0b0000000000001111'
    >>> bitset.value = -1
    >>> bitset.value
    '0b0000000000000000'
    >>> bitset.value = 0x10000
    >>> bitset.value
    '0b1111111111111111'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> bitset.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffff'
    >>> pprint(bitset.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Bitset16',
     'index': [0, 0],
     'max': 65535,
     'min': 0,
     'name': 'Bitset16',
     'order': 'auto',
     'signed': False,
     'size': 16,
     'type': 'Field',
     'value': '0b1111111111111111'}
    """
    item_type = ItemClass.Bitset

    def __init__(self, bit_size, align_to=None, byte_order=Byteorder.auto):
        super().__init__(bit_size, align_to, False, byte_order)

    @property
    def value(self):
        """ Field value."""
        return '{0:#0{1}b}'.format(self._value, self.bit_size + 2)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)


class Bool(Decimal):
    """ A `Bool` field is an unsigned :class:`Decimal` field with a variable
    *size* and returns its field *value* as a boolean.

    :param int bit_size: is the *size* of the `Bool` field in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Bool` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Bool` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Bool` field.

    :param byte_order: coding :class:`Byteorder` of the `Bool` field.

    Example:

    >>> boolean = Bool(16)
    >>> boolean.is_decimal()
    True
    >>> boolean.is_bool()
    True
    >>> boolean.name
    'Bool16'
    >>> boolean.alignment
    (2, 0)
    >>> boolean.byte_order
    Byteorder.auto = 'auto'
    >>> boolean.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> boolean.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> boolean.bit_size
    16
    >>> boolean.min()
    0
    >>> boolean.max()
    65535
    >>> boolean.signed
    False
    >>> boolean.value
    False
    >>> boolean.decode(bytes.fromhex('0f00'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> boolean.value
    True
    >>> boolean.value = False
    >>> boolean.value
    False
    >>> boolean.value = -1
    >>> boolean.value
    False
    >>> boolean.value = 0x10000
    >>> boolean.value
    True
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> boolean.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffff'
    >>> pprint(boolean.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Bool16',
     'index': [0, 0],
     'max': 65535,
     'min': 0,
     'name': 'Bool16',
     'order': 'auto',
     'signed': False,
     'size': 16,
     'type': 'Field',
     'value': True}
    """
    item_type = ItemClass.Bool

    def __init__(self, bit_size, align_to=None, byte_order=Byteorder.auto):
        super().__init__(bit_size, align_to, False, byte_order)

    @property
    def value(self):
        """ Field value."""
        return bool(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)

    @staticmethod
    def is_bool():
        """ Returns `True`."""
        return True


class Enum(Decimal):
    """ A `Enum` field is an unsigned :class:`Decimal` field with a variable
    *size* and returns its field *value* as a integer number.

    If an :class:`Enumeration` is available and a member matches the integer
    number then the member name string is returned otherwise the integer number
    is returned.

    :param int bit_size: is the *size* of the `Enum` field in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Enum` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Enum` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Enum` field.

    :param enumeration: :class:`Enumeration` definition of the `Enum` field.

    :param byte_order: coding :class:`Byteorder` of the `Enum` field.

    Example:

    >>> enum = Enum(16, enumeration=ItemClass)
    >>> enum.is_decimal()
    True
    >>> enum.name
    'Enum16'
    >>> enum.alignment
    (2, 0)
    >>> enum.byte_order
    Byteorder.auto = 'auto'
    >>> enum.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> enum.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> enum.bit_size
    16
    >>> enum.min()
    0
    >>> enum.max()
    65535
    >>> enum.signed
    False
    >>> enum.value
    0
    >>> enum.decode(bytes.fromhex('2800'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> enum.value
    'Decimal'
    >>> enum.value = 48
    >>> enum.value
    'Enum'
    >>> enum.value = 'Enum'
    >>> enum.value
    'Enum'
    >>> enum.value = 40
    >>> enum.value
    'Decimal'
    >>> enum.value = -1
    >>> enum.value
    0
    >>> enum.value = 65536
    >>> enum.value
    65535
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> enum.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffff'
    >>> pprint(enum.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Enum16',
     'index': [0, 0],
     'max': 65535,
     'min': 0,
     'name': 'Enum16',
     'order': 'auto',
     'signed': False,
     'size': 16,
     'type': 'Field',
     'value': 65535}
    """
    item_type = ItemClass.Enum

    def __init__(self, bit_size, align_to=None, enumeration=None,
                 byte_order=Byteorder.auto):
        super().__init__(bit_size, align_to, False, byte_order)
        # Field enumeration class
        if enumeration is None:
            self._enum = None
        elif issubclass(enumeration, Enumeration):
            self._enum = enumeration
        else:
            raise EnumTypeError(self, enumeration)

    @property
    def value(self):
        """ Field value."""
        if self._enum and issubclass(self._enum, Enumeration):
            name = self._enum.get_name(self._value)
            if name:
                return name
        return self._value

    @value.setter
    def value(self, x):
        if isinstance(x, str):
            try:
                decimal = int(x, 0)
            except ValueError:
                if self._enum and issubclass(self._enum, Enumeration):
                    decimal = int(self._enum.get_value(x))
                    if decimal < 0:
                        raise FieldValueError(self, self.index, x)
                else:
                    raise FieldValueError(self, self.index, x)
        else:
            decimal = x
        self._value = self.to_decimal(decimal)


class Scaled(Decimal):
    """ A `Scaled` field is a signed :class:`Decimal` field with a variable
    *size* and returns its scaled field *value* as a float.

    The scaled field *value* is:

        ``(unscaled field value / scaling base) * scaling factor``

    The unscaled field *value* is:

        ``(scaled field value / scaling factor) * scaling base``

    The scaling base is:

        ``2 ** (field size - 1) / 2``

    A `Scaled` field extends the :attr:`~Field.blueprint` of a :class:`Decimal`
    with a ``scale`` key for its scaling factor.

    :param float scale: scaling factor of the `Scaled` field.

    :param int bit_size: is the *size* of the `Scaled` field in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Scaled` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Scaled` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Scaled` field.

    :param byte_order: coding :class:`Byteorder` of the `Scaled` field.

    Example:

    >>> scaled = Scaled(100, 16)
    >>> scaled.is_decimal()
    True
    >>> scaled.name
    'Scaled16'
    >>> scaled.alignment
    (2, 0)
    >>> scaled.byte_order
    Byteorder.auto = 'auto'
    >>> scaled.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> scaled.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> scaled.bit_size
    16
    >>> scaled.min()
    -32768
    >>> scaled.max()
    32767
    >>> scaled.scale
    100.0
    >>> scaled.scaling_base()
    16384.0
    >>> scaled.signed
    True
    >>> scaled.value
    0.0
    >>> scaled.decode(bytes.fromhex('0040'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> scaled.value
    100.0
    >>> scaled.value = -100
    >>> scaled.value
    -100.0
    >>> scaled.value = -200.001
    >>> scaled.value
    -200.0
    >>> scaled.value = 200
    >>> scaled.value
    199.993896484375
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> scaled.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ff7f'
    >>> pprint(scaled.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Scaled16',
     'index': [0, 0],
     'max': 32767,
     'min': -32768,
     'name': 'Scaled16',
     'order': 'auto',
     'scale': 100.0,
     'signed': True,
     'size': 16,
     'type': 'Field',
     'value': 199.993896484375}
    """
    item_type = ItemClass.Scaled

    def __init__(self, scale, bit_size, align_to=None,
                 byte_order=Byteorder.auto):
        super().__init__(bit_size, align_to, True, byte_order)
        # Field scaling factor
        self._scale = float(scale)

    @property
    def value(self):
        """ Field value."""
        return self.as_float(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_scaled(x)

    def as_float(self, value):
        return (value / self.scaling_base()) * self.scale

    def to_scaled(self, value):
        return self.to_decimal((float(value) / self.scale) * self.scaling_base())

    @property
    def scale(self):
        """ Scaling factor of the `Scaled` field."""
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = float(value)

    def scaling_base(self):
        """ Returns the scaling base of the `Scaled` field."""
        return 2 ** (self.bit_size - 1) / 2

    def blueprint(self, name=None, **options):
        obj = super().blueprint(name, **options)
        obj['scale'] = self.scale
        return OrderedDict(sorted(obj.items()))


class Fraction(Decimal):
    """ A `Fraction` field is an unsigned :class:`Decimal` field with a
    variable *size* and returns its fractional field *value* as a float.

    A fractional number is bitwise encoded and has up to three bit
    parts for this task.

    The first part are the bits for the fraction part of a fractional number.
    The number of bits for the fraction part is derived from the *bit size*
    of the field and the required bits for the other two parts.
    The fraction part is always smaller than one.

        ``fraction part = (2**bits - 1) / (2**bits)``

    The second part are the *bits* for the *integer* part of a fractional
    number.

        ``integer part = (2**bits - 1)``

    The third part is the bit for the sign of a *signed* fractional
    number. Only a *signed* fractional number posses this bit.

        ``sign part = {'0': '+', '1': '-'}``

    A fractional number is multiplied by hundred.

    :param int bits_integer: number of bits for the integer part of the
        fraction number, can be between *1* and the *size* of the
        `Fraction` field.

    :param int bit_size: is the *size* of the `Fraction` field in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Fraction` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Fraction` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Fraction` field.

    :param bool signed: if `True` the `Fraction` field is signed otherwise
        unsigned.

    :param byte_order: coding :class:`Byteorder` of the `Fraction` field

    Example:

    >>> unipolar = Fraction(2, 16)
    >>> unipolar.is_decimal()
    True
    >>> unipolar.name
    'Fraction2.16'
    >>> unipolar.alignment
    (2, 0)
    >>> unipolar.byte_order
    Byteorder.auto = 'auto'
    >>> unipolar.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> unipolar.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unipolar.bit_size
    16
    >>> unipolar.min()
    0
    >>> unipolar.max()
    65535
    >>> unipolar.signed
    False
    >>> unipolar.value
    0.0
    >>> unipolar.decode(bytes.fromhex('0080'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unipolar.value
    200.0
    >>> unipolar.value = 100
    >>> unipolar.value
    100.0
    >>> unipolar.as_float(0x4000)
    100.0
    >>> unipolar.value = -1
    >>> unipolar.value
    0.0
    >>> unipolar.value = 400
    >>> unipolar.value
    399.993896484375
    >>> unipolar.as_float(0xffff)
    399.993896484375
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> unipolar.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffff'
    >>> pprint(unipolar.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Fraction2.16',
     'index': [0, 0],
     'max': 65535,
     'min': 0,
     'name': 'Fraction2.16',
     'order': 'auto',
     'signed': False,
     'size': 16,
     'type': 'Field',
     'value': 399.993896484375}

    Example:

    >>> bipolar = Fraction(2, 16, 2, True)
    >>> bipolar.is_decimal()
    True
    >>> bipolar.name
    'Fraction2.16'
    >>> bipolar.alignment
    (2, 0)
    >>> bipolar.byte_order
    Byteorder.auto = 'auto'
    >>> bipolar.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> bipolar.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bipolar.bit_size
    16
    >>> bipolar.min()
    0
    >>> bipolar.max()
    65535
    >>> bipolar.signed
    False
    >>> bipolar.value
    0.0
    >>> bipolar.decode(bytes.fromhex('0040'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bipolar.value
    100.0
    >>> bipolar.value = -100
    >>> bipolar.value
    -100.0
    >>> bipolar.as_float(0xc000)
    -100.0
    >>> bipolar.as_float(0x8000)
    -0.0
    >>> bipolar.value = -200
    >>> bipolar.value
    -199.993896484375
    >>> bipolar.as_float(0xffff)
    -199.993896484375
    >>> bipolar.value = 200
    >>> bipolar.value
    199.993896484375
    >>> bipolar.as_float(0x7fff)
    199.993896484375
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> bipolar.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ff7f'
    >>> pprint(bipolar.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Fraction2.16',
     'index': [0, 0],
     'max': 65535,
     'min': 0,
     'name': 'Fraction2.16',
     'order': 'auto',
     'signed': True,
     'size': 16,
     'type': 'Field',
     'value': 199.993896484375}
    """
    item_type = ItemClass.Fraction

    def __init__(self, bits_integer, bit_size, align_to=None, signed=False,
                 byte_order=Byteorder.auto):
        super().__init__(bit_size, align_to, False, byte_order)
        # Number of bits of the integer part of the fraction number
        self._bits_integer = limiter(int(bits_integer), 1, self._bit_size)
        # Fraction number signed?
        if self._bit_size <= 1:
            self._signed_fraction = False
        else:
            self._signed_fraction = bool(signed)

    @property
    def name(self):
        """ Returns the type name of the `Fraction` field (read-only)."""
        return "{0}{1}.{2}".format(self.item_type.name.capitalize(),
                                   self._bits_integer,
                                   self.bit_size)

    @property
    def value(self):
        """ Field value."""
        return self.as_float(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_fraction(x)

    def as_float(self, value):
        factor = 100.0
        bits_fraction = max(self.bit_size - self._bits_integer, 0)
        fraction = (value & (2 ** bits_fraction - 1)) / 2 ** bits_fraction
        if self._signed_fraction:
            mask = 2 ** (self.bit_size - 1)
            if value & mask:
                factor = -100.0
            integer = (value & (mask - 1)) >> max(bits_fraction, 0)
        else:
            integer = value >> max(bits_fraction, 0)
        return (integer + fraction) * factor

    def to_fraction(self, value):
        normalized = float(value) / 100.0
        bits_fraction = max(self.bit_size - self._bits_integer, 0)
        if self._signed_fraction:
            integer = abs(int(normalized)) << max(bits_fraction, 0)
            fraction = int(math.fabs(normalized - int(normalized)) * 2 ** bits_fraction)
            if normalized < 0:
                mask = 2 ** (self.bit_size - 1)
            else:
                mask = 0
            decimal = limiter(integer | fraction, 0, 2 ** (self.bit_size - 1) - 1)
            decimal |= mask
        else:
            normalized = max(normalized, 0)
            integer = int(normalized) << max(bits_fraction, 0)
            fraction = int((normalized - int(normalized)) * 2 ** bits_fraction)
            decimal = limiter(integer | fraction, 0, 2 ** self.bit_size - 1)
        return self.to_decimal(decimal)

    def blueprint(self, name=None, **options):
        obj = super().blueprint(name, **options)
        obj['signed'] = self._signed_fraction
        return OrderedDict(sorted(obj.items()))


class Bipolar(Fraction):
    """ A `Bipolar` field is a signed :class:`Fraction` field with a variable
    *size* and returns its fractional field value as a float.

    :param int bits_integer: number of bits for the integer part of the
        fraction number, can be between *1* and the *size* of the
        `Bipolar` field.

    :param int bit_size: is the *size* of the `Bipolar` field in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Bipolar` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Bipolar` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Bipolar` field.

    :param byte_order: coding :class:`Byteorder` of the `Bipolar` field.

    Example:

    >>> bipolar = Bipolar(2, 16)
    >>> bipolar.is_decimal()
    True
    >>> bipolar.name
    'Bipolar2.16'
    >>> bipolar.alignment
    (2, 0)
    >>> bipolar.byte_order
    Byteorder.auto = 'auto'
    >>> bipolar.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> bipolar.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bipolar.bit_size
    16
    >>> bipolar.min()
    0
    >>> bipolar.max()
    65535
    >>> bipolar.signed
    False
    >>> bipolar.value
    0.0
    >>> bipolar.value = -100
    >>> bipolar.value
    -100.0
    >>> bipolar.as_float(0xc000)
    -100.0
    >>> bipolar.as_float(0x8000)
    -0.0
    >>> bipolar.value = -200
    >>> bipolar.value
    -199.993896484375
    >>> bipolar.as_float(0xffff)
    -199.993896484375
    >>> bipolar.value = 200
    >>> bipolar.value
    199.993896484375
    >>> bipolar.as_float(0x7fff)
    199.993896484375
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> bipolar.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ff7f'
    >>> pprint(bipolar.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Bipolar2.16',
     'index': [0, 0],
     'max': 65535,
     'min': 0,
     'name': 'Bipolar2.16',
     'order': 'auto',
     'signed': True,
     'size': 16,
     'type': 'Field',
     'value': 199.993896484375}
    """
    item_type = ItemClass.Bipolar

    def __init__(self, bits_integer, bit_size, align_to=None,
                 byte_order=Byteorder.auto):
        super().__init__(bits_integer, bit_size, align_to, True, byte_order)


class Unipolar(Fraction):
    """ A `Unipolar` field is an unsigned :class:`Fraction` field with a variable
    *size* and returns its fractional field *value* as a float.

    :param int bits_integer: number of bits for the integer part of the
        fraction number, can be between *1* and the *size* of the
        `Unipolar` field.

    :param int bit_size: is the *size* of the `Unipolar` field in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Unipolar` field to the number of bytes,
        can be between *1* and *8*.
        If no field *alignment* is set the `Unipolar` field  aligns itself
        to the next matching byte size corresponding to the *size* of the
        `Unipolar` field.

    :param byte_order: coding :class:`Byteorder` of the `Unipolar` field.

    Example:

    >>> unipolar = Unipolar(2, 16)
    >>> unipolar.is_decimal()
    True
    >>> unipolar.name
    'Unipolar2.16'
    >>> unipolar.alignment
    (2, 0)
    >>> unipolar.byte_order
    Byteorder.auto = 'auto'
    >>> unipolar.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> unipolar.next_index()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unipolar.bit_size
    16
    >>> unipolar.min()
    0
    >>> unipolar.max()
    65535
    >>> unipolar.signed
    False
    >>> unipolar.value
    0.0
    >>> unipolar.decode(bytes.fromhex('0080'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unipolar.value
    200.0
    >>> unipolar.value = 100
    >>> unipolar.value
    100.0
    >>> unipolar.as_float(0x4000)
    100.0
    >>> unipolar.value = -1
    >>> unipolar.value
    0.0
    >>> unipolar.value = 400
    >>> unipolar.value
    399.993896484375
    >>> unipolar.as_float(0xffff)
    399.993896484375
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> unipolar.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffff'
    >>> pprint(unipolar.blueprint())
    {'address': 0,
     'alignment': [2, 0],
     'class': 'Unipolar2.16',
     'index': [0, 0],
     'max': 65535,
     'min': 0,
     'name': 'Unipolar2.16',
     'order': 'auto',
     'signed': False,
     'size': 16,
     'type': 'Field',
     'value': 399.993896484375}
    """
    item_type = ItemClass.Unipolar

    def __init__(self, bits_integer, bit_size, align_to=None,
                 byte_order=Byteorder.auto):
        super().__init__(bits_integer, bit_size, align_to, False, byte_order)


class Datetime(Decimal):
    """ A `Datetime` field is an unsigned :class:`Decimal` field with a fix
    *size* of four bytes and returns its field *value* as a UTC datetime
    encoded string in the format *YYYY-mm-dd HH:MM:SS*.

    :param byte_order: coding :class:`Byteorder` of the `Datetime` field.

    Example:

    >>> datetime = Datetime()
    >>> datetime.is_decimal()
    True
    >>> datetime.name
    'Datetime32'
    >>> datetime.alignment
    (4, 0)
    >>> datetime.byte_order
    Byteorder.auto = 'auto'
    >>> datetime.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> datetime.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> datetime.bit_size
    32
    >>> datetime.min()
    0
    >>> datetime.max()
    4294967295
    >>> datetime.signed
    False
    >>> datetime.value
    '1970-01-01 00:00:00'
    >>> datetime.decode(bytes.fromhex('ffffffff'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> datetime.value
    '2106-02-07 06:28:15'
    >>> datetime.value = '1969-12-31 23:59:59'
    >>> datetime.value
    '1970-01-01 00:00:00'
    >>> datetime.value = '2106-02-07 06:28:16'
    >>> datetime.value
    '2106-02-07 06:28:15'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> datetime.encode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffffffff'
    >>> pprint(datetime.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'Datetime32',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'Datetime32',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Field',
     'value': '2106-02-07 06:28:15'}
    """
    item_type = ItemClass.Datetime

    def __init__(self, byte_order=Byteorder.auto):
        super().__init__(bit_size=32, byte_order=byte_order)

    @property
    def value(self):
        """ Field value."""
        return str(datetime.datetime.utcfromtimestamp(self._value))

    @value.setter
    def value(self, x):
        self._value = self.to_timestamp(x)

    def to_timestamp(self, value):
        decimal = calendar.timegm(time.strptime(value, "%Y-%m-%d %H:%M:%S"))
        return self.to_decimal(decimal)


class Pointer(Decimal, Container):
    """ A `Pointer` field is an unsigned :class:`Decimal` field with a *size* of
    four bytes and returns its field *value* as a hexadecimal encoded string.

    A `Pointer` field refers absolutely to a :attr:`data` object of a data
    :class:`Provider`.

    The `Pointer` class extends the :class:`Decimal` field with the
    :class:`Container` class for its referenced :attr:`data` object.

    A `Pointer` field has additional features to **read**, **write**, **decode**,
    **encode** and **view** binary data:

    *   **Refresh** each :class:`Field` in the :attr:`data` object
        with the internal :attr:`bytestream` of the `Pointer` field
        via :meth:`refresh()`.
    *   **Read** from a :class:`Provider` the necessary amount of bytes for
        the referenced :attr:`data` object of the `Pointer` field
        via :meth:`read_from()`.
    *   **Write** to a :class:`Provider` the necessary amount of bytes for
        the referenced :attr:`data` object of the `Pointer` field
        via :meth:`write_to()`.
    *   **Indexes** each :class:`Field` in the :attr:`data` object referenced
        by the `Pointer` field via :meth:`subscript()`.
    *   View the **index** of the `Pointer` field and for each :class:`Field`
        in the referenced :attr:`data` object of the `Pointer` field
        via :meth:`field_indexes()`.
    *   View the **type** of the `Pointer` field and for each :class:`Field`
        in the referenced :attr:`data` object of the `Pointer` field
        via :meth:`field_types()`.
    *   View the **value** of the `Pointer` field and for each :class:`Field`
        in the referenced :attr:`data` object of the `Pointer` field
        via :meth:`field_values()`.
    *   List the **item** and its path for the `Pointer` field and for each
        :class:`Field` in the referenced :attr:`data` object of the `Pointer`
        field as a flat list via :meth:`field_items()`.
    *   Get a **blueprint** of the `Pointer` field via :meth:`blueprint()`.

    :param template: template for the :attr:`data` object referenced by
        the `Pointer` field.

    :param int address: absolute address of the :attr:`data` object
        referenced by the `Pointer` field.

    :param byte_order: coding :class:`Byteorder` of the :attr:`bytestream`
        of the `Pointer` field.

    Example:

    >>> pointer = Pointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    >>> pointer.size
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.initialize({'value': 0x8000})
    >>> pointer.value
    '0x8000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> pointer.encode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffffffff'
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    b'4b6f6e466f6f2069732046756e'
    >>> pointer.as_bytestream()
    bytearray(b'')
    >>> pointer.refresh()
    Index(byte=0, bit=0, address=4294967295, base_address=4294967295, update=False)
    >>> pointer.as_bytestream()
    bytearray(b'')
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'Pointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'Pointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff'}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': Index(byte=0, bit=0, address=4294967295, base_address=4294967295, update=False)}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', None)])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', None)])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      Pointer(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=(4, 0),
              bit_size=32,
              value='0xffffffff'))]
    >>> pprint(pointer.to_list())
    [('Pointer.value', '0xffffffff')]
    >>> pprint(pointer.to_dict())
    OrderedDict([('Pointer', OrderedDict([('value', '0xffffffff')]))])
    """
    item_type = ItemClass.Pointer

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(bit_size=32, align_to=4)
        # Field value
        if address:
            self.value = address
        # Data object
        self._data = self.data = template
        # Data objects bytestream
        self._data_stream = bytes()
        # Data objects byte order
        self._data_byte_order = self.order = byte_order

    @property
    def address(self):
        """ Returns the absolute address of the :attr:`data` object
        referenced by the `Pointer` field (read-only).
        """
        return self._value

    @property
    def base_address(self):
        """ Returns the base address of the data :class:`Provider` for the
        :attr:`data` object referenced by the `Pointer` field (read-only).
        """
        return self._value

    @property
    def bytestream(self):
        """ Bytestream of the `Pointer` field for the referenced :attr:`data`
        object. Returned as a hexadecimal encoded string.
        """
        return hexlify(self._data_stream)

    @bytestream.setter
    def bytestream(self, value):
        if isinstance(value, str):
            self._data_stream = bytes.fromhex(value)
        elif isinstance(value, (bytearray, bytes)):
            self._data_stream = bytes(value)
        else:
            raise FieldTypeError(self, self.index, value)

    @property
    def data(self):
        """ `Data` object referenced by the `Pointer` field."""
        return self._data

    @data.setter
    def data(self, value):
        if value is None:
            self._data = None
        elif is_any(value):
            self._data = value
        else:
            raise MemberTypeError(self, value, 'data')

    @property
    def order(self):
        """ Coding :class:`Byteorder` of the :attr:`bytestream`
        of the `Pointer` field.
        """
        return self._data_byte_order

    @order.setter
    def order(self, byteorder):
        if not isinstance(byteorder, Byteorder):
            raise ByteOrderTypeError(self, byteorder)
        if byteorder not in (Byteorder.big, Byteorder.little):
            raise FieldByteOrderError(self, self.index, byteorder.value)
        self._data_byte_order = byteorder

    @property
    def size(self):
        """ Returns the size of the :attr:`data` object in bytes (read-only)."""
        # Container
        if is_container(self._data):
            byte_length, bit_length = self._data.field_length()
            return byte_length + math.ceil(bit_length / 8)
        # Field
        elif is_field(self._data):
            return math.ceil(self._data.bit_size / 8)
        else:
            return 0

    @property
    def value(self):
        """ Field value."""
        return hex(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)

    @staticmethod
    def is_pointer():
        """ Returns `True`."""
        return True

    def is_null(self):
        """ Returns `True` if the `Pointer` field points to zero."""
        return self._value is 0

    def refresh(self):
        """ Refresh each :class:`Field` in the :attr:`data` object with the
        internal :attr:`bytestream` of the `Pointer` field and returns the
        :class:`Index` of the :attr:`bytestream` after the last :class:`Field`
        in the :attr:`data` object.
        """
        index = Index(0, 0, self.address, self.base_address, False)
        if self._data:
            index = self._data.decode(self._data_stream,
                                      index,
                                      nested=False,
                                      byte_order=self.order)
        return index

    def as_bytestream(self):
        buffer = bytearray()
        if self._data:
            self._data.encode(buffer,
                              Index(0, 0,
                                    self.address, self.base_address,
                                    False),
                              byte_order=self.order)
        return buffer

    @nested_option(True)
    def read_from(self, provider, null_allowed=False, **options):
        """ Reads from the data :class:`Provider` the necessary amount of bytes
        for the nested :attr:`data` object of the `Pointer` field.

        A `Pointer` field has its own :attr:`bytestream` to store the binary data
        from the data :class:`Provider`.

        :param provider: data :class:`Provider`.

        :param bool null_allowed: if `True` read access of address zero (null)
            is allowed.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            :attr:`data` object of the `Pointer` field reads their *nested*
            :attr:`~Pointer.data` object fields as well (chained method call).
            Each `Pointer` field stores the bytes for its *nested*
            :attr:`data` object in its own :attr:`bytestream`.
        """
        if self._data is None:
            pass
        elif is_provider(provider):
            if self._value < 0:
                pass
            elif null_allowed or self._value > 0:
                while True:
                    self.bytestream = provider.read(self.address, self.size)
                    index = self.refresh()
                    # Incomplete data object
                    if index.bit != 0:
                        length = index.byte, index.bit
                        raise ContainerLengthError(self, length)
                    if not index.update:
                        break
                if is_mixin(self._data) and get_nested(options):
                    self._data.read_from(provider, **options)
            else:
                self._data_stream = bytes()
                self.refresh()
        else:
            raise ProviderTypeError(self, provider)

    def patch(self, item, byte_order=BYTEORDER):
        """ Returns a memory :class:`Patch` for the given *item* that shall be
        patched in the data `source`.

        :param item: item to patch.

        :param byte_order: encoding :class:`Byteorder` for the item.
        """
        # Re-index the data object
        self.subscript()

        # Container?
        if is_container(item):
            # Incomplete container
            length = item.field_length()
            if length[1] is not 0:
                raise ContainerLengthError(item, length)

            # Empty container?
            field = item.first_field()
            if field is None:
                return None

            # Bad placed container
            index = field.index
            if index.bit is not 0:
                raise FieldIndexError(field, index)

            # Create a dummy byte array filled with zero bytes.
            # The dummy byte array is necessary because the length of
            # the buffer must correlate to the field indexes of the
            # appending fields.
            buffer = bytearray(b'q\x00' * index.byte)

            # Append the content mapped by the container fields to the buffer
            item.encode(buffer, index, byte_order=byte_order)

            # Content of the buffer mapped by the container fields
            content = buffer[index.byte:]

            # Not correct filled buffer!
            if len(content) != length[0]:
                raise BufferError(len(content), length[0])

            return Patch(content,
                         index.address,
                         byte_order,
                         length[0] * 8,
                         0,
                         False)
        # Field?
        elif is_field(item):
            # Field alignment
            group_size, group_offset = item.alignment

            # Bad aligned field?
            index = item.index
            if index.bit != group_offset:
                alignment = group_size, index.bit
                raise FieldGroupOffsetError(item, index, alignment)

            # Create a dummy byte array filled with zero bytes.
            # The dummy byte array is necessary because the length of
            # the buffer must correlate to the field index of the
            # appending field group.
            buffer = bytearray(b'\x00' * index.byte)

            # Append the content mapped by the field to the buffer
            item.encode(buffer, index, byte_order=byte_order)

            # Content of the buffer mapped by the field group
            content = buffer[index.byte:]

            # Not correct filled buffer!
            if len(content) != group_size:
                raise BufferError(len(content), group_size)

            # Patch size for the field in the content buffer
            patch_size, offset = divmod(item.bit_size, 8)
            if offset is not 0:
                inject = True
                patch_size += 1
            else:
                inject = False

            # Patch offset for the field in the content buffer
            patch_offset, field_offset = divmod(group_offset, 8)
            if field_offset is not 0:
                inject = True

            if byte_order is Byteorder.big:
                start = group_size - (patch_offset + patch_size)
                stop = group_size - patch_offset
            else:
                start = patch_offset
                stop = patch_offset + patch_size

            return Patch(content[start:stop],
                         index.address + start,
                         byte_order,
                         item.bit_size,
                         field_offset,
                         inject)
        else:
            raise MemberTypeError(self, item)

    def write_to(self, provider, item, byte_order=BYTEORDER):
        """ Writes via a data :class:`Provider` the :class:`Field` values of
        the given *item* to the data `source`.

        :param provider: data :class:`Provider`.

        :param item: item to write.

        :param byte_order: encoding :class:`Byteorder`.
        """
        # Create memory patch for the item to write
        patch = self.patch(item, byte_order)

        if patch is None:
            pass
        elif is_provider(provider):
            if patch.inject:
                # Unpatched content of the memory area in the data source to patch
                content = provider.read(patch.address, len(patch.buffer))

                # Decimal value of the memory area to patch
                value = int.from_bytes(content, byte_order.value)

                # Inject memory patch content
                bit_mask = ~((2 ** patch.bit_size - 1) << patch.bit_offset)
                bit_mask &= (2 ** (len(patch.buffer) * 8) - 1)
                value &= bit_mask
                value |= int.from_bytes(patch.buffer, byte_order.value)

                # Patched content for the memory area in the data source to patch
                buffer = value.to_bytes(len(patch.buffer), byte_order.value)

                provider.write(buffer, patch.address, len(buffer))
            else:
                provider.write(patch.buffer, patch.address, len(patch.buffer))
        else:
            raise ProviderTypeError(self, provider)

    @byte_order_option()
    @nested_option()
    def decode(self, buffer=bytes(), index=zero(), **options):
        """ Decodes sequential the bytes from the *buffer* starting at the begin
        of the *buffer* or with the given *index* by mapping the bytes to the
        *value* of the `Pointer` field in accordance with the decoding *byte order*
        of the *buffer* and the `Pointer` field.

        A specific *byte order* of the `Pointer` field overrules the decoding
        *byte order* of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the `Pointer` field.

        Optional the decoding of the *nested* :attr:`data` object of the
        `Pointer` field can be enabled.

        :param bytes buffer: bytestream.

        :param index: current read :class:`Index` within the *buffer*.

        :keyword byte_order: decoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` a `Pointer` field decodes its *nested*
            :attr:`data` object fields as well (chained method call).
            Each :class:`Pointer` field uses for the decoding of its *nested*
            :attr:`data` object its own :attr:`bytestream`.
        """
        # Field
        index = super().decode(buffer, index, **options)
        # Data Object
        if self._data and get_nested(options):
            options[Option.byteorder] = self.order
            self._data.decode(self._data_stream,
                              Index(0, 0,
                                    self.address, self.base_address,
                                    False),
                              **options)
        return index

    @byte_order_option()
    @nested_option()
    def encode(self, buffer=bytearray(), index=zero(), **options):
        """ Encodes sequential the bytes to the *buffer* starting at the begin
        of the *buffer* or with the given *index* by mapping the *value* of the
        `Pointer` field to the bytes in accordance with the encoding *byte order*
        of the *buffer* and the `Pointer` field.

        A specific *byte order* of the `Pointer` field overrules the encoding
        *byte order* of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the `Pointer` field.

        Optional the encoding of the *nested* :attr:`data` object of the
        `Pointer` field can be enabled.

        :param bytearray buffer: bytestream.

        :param index: current write :class:`Index` within the *buffer*.

        :keyword byte_order: encoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` a `Pointer` field encodes its *nested*
            :attr:`data` object fields as well (chained method call).
            Each :class:`Pointer` field uses for the encoding of its *nested*
            :attr:`data` object its own :attr:`bytestream`.
        """
        # Field
        index = super().encode(buffer, index, **options)
        # Data Object
        if self._data and get_nested(options):
            options[Option.byteorder] = self.order
            self._data_stream = bytearray()
            self._data.encode(self._data_stream,
                              Index(0, 0,
                                    self.address, self.base_address,
                                    False),
                              **options)
            self._data_stream = bytes(self._data_stream)
        return index

    def subscript(self):
        """ Indexes each :class:`Field` in the :attr:`data` object referenced
        by the `Pointer` field.
        """
        # Start index for the Data Object
        index = Index(0, 0, self.address, self.base_address, False)
        # Container
        if is_container(self._data):
            self._data.next_index(index, nested=True)
        # Pointer
        elif is_pointer(self._data):
            self._data.next_index(index)
            self._data.subscript()
        # Field
        elif is_field(self._data):
            self._data.next_index(index)

    def initialize(self, content):
        """ Initializes the `Pointer` field itself and the :class:`Field` items
        of the :attr:`data` object of the `Pointer` field with the *values*
        in the *content* dictionary.

        The ``['value']`` key in the *content* dictionary refers to the `Pointer`
        field itself and with the ``['data']`` key is the :attr:`data` object of
        the `Pointer` field referenced.

        :param dict content: a dictionary contains the :class:`Field` value for
            the `Pointer` field and the :class:`Field` values for each item
            in the :attr:`data` object of the `Pointer` field.
        """
        for name, value in content.items():
            if name is 'value':
                self.value = value
            elif name is 'data':
                # Container or Pointer
                if is_mixin(self._data):
                    self._data.initialize(value)
                # Field
                elif is_field(self._data):
                    self._data.value = value

    @nested_option()
    def field_indexes(self, index=zero(), **options):
        """ Returns an :class:`ordered dictionary <collections.OrderedDict>`
        with two keys.
        The ``['value']`` key contains the *index* of the `Pointer` field and
        the ``['data']`` key contains the *indexes* for each :class:`Field`
        in the :attr:`data` object of the `Pointer` field.

        :param index: optional start :class:`Index` of the `Pointer`.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            :attr:`data` object of the `Pointer` field lists their *nested*
            :attr:`~Pointer.data` object fields as well (chained method call).
        """
        self.next_index(index)

        indexes = OrderedDict()
        indexes['value'] = self._index
        # Container
        if is_container(self._data):
            indexes['data'] = self._data.field_indexes(
                Index(0, 0, self.address, self.base_address, False),
                **options)
        # Pointer
        elif is_pointer(self._data) and get_nested(options):
            indexes['data'] = self._data.field_indexes(
                Index(0, 0, self.address, self.base_address, False),
                **options)
        # Field
        elif is_field(self._data):
            self._data.next_index(Index(0, 0,
                                        self.address, self.base_address,
                                        False))
            indexes['data'] = self._data.index
        else:
            indexes['data'] = Index(0, 0,
                                    self.address, self.base_address,
                                    False)
        return indexes

    @nested_option()
    def field_types(self, **options):
        """ Returns an :class:`ordered dictionary <collections.OrderedDict>`
        with two keys.
        The ``['value']`` key contains the *type* of the `Pointer` field and
        the ``['data']`` key contains the *types* for each :class:`Field`
        in the :attr:`data` object of the `Pointer` field.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            :attr:`data` object of the `Pointer` field lists their *nested*
            :attr:`~Pointer.data` object fields as well (chained method call).
        """
        types = OrderedDict()
        types['value'] = self.name
        # Container
        if is_container(self._data):
            types['data'] = self._data.field_types(**options)
        # Pointer
        elif is_pointer(self._data) and get_nested(options):
            types['data'] = self._data.field_types(**options)
        # Field
        elif is_field(self._data):
            types['data'] = self._data.name
        else:
            types['data'] = None
        return types

    @nested_option()
    def field_values(self, **options):
        """ Returns an :class:`ordered dictionary <collections.OrderedDict>`
        with two keys.
        The ``['value']`` key contains the *value* of the `Pointer` field and
        the ``['data']`` key contains the *values* for each :class:`Field`
        in the :attr:`data` object of the `Pointer` field.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            :attr:`data` object of the `Pointer` field lists their *nested*
            :attr:`~Pointer.data` object fields as well (chained method call).
        """
        values = OrderedDict()
        values['value'] = self.value
        # Container
        if is_container(self._data):
            values['data'] = self._data.field_values(**options)
        # Pointer
        elif is_pointer(self._data) and get_nested(options):
            values['data'] = self._data.field_values(**options)
        # Field
        elif is_field(self._data):
            values['data'] = self._data.value
        else:
            values['data'] = self._data
        return values

    @nested_option()
    def field_items(self, root=str(), **options):
        """ Returns a **flat** list which contains the ``(path, item)`` tuples
        for each :class:`Field` of the `Pointer` field.

        :param str root: root path.

        :keyword bool nested: if `True` all :class:`Pointer` fields in the
            :attr:`data` object of the `Pointer` field lists their *nested*
            :attr:`~Pointer.data` object fields as well (chained method call).
        """
        items = list()
        # Field
        path = root if root else 'value'
        items.append((path, self))
        # Data Object
        path = '{0}.{1}'.format(root, 'data') if root else 'data'
        # Container
        if is_container(self._data):
            for field_item in self._data.field_items(path, **options):
                items.append(field_item)
        # Pointer
        elif is_pointer(self._data) and get_nested(options):
            for field_item in self._data.field_items(path, **options):
                items.append(field_item)
        # Field
        elif is_field(self._data):
            items.append((path, self._data))
        return items

    @nested_option(True)
    def blueprint(self, name=str(), **options):
        """ Returns the **blueprint** of a `Pointer` as an
        :class:`ordered dictionary <collections.OrderedDict>`.

        .. code-block:: python

            blueprint = {
                'address': self.index.address,
                'alignment': [self.alignment[0], self.alignment[1]],
                'class': self.__class__.__name__,
                'index': [self.index.byte, self.index.bit],
                'max': self.max(),
                'min': self.min(),
                'name': name if name else self.__class__.__name__,
                'order': self.byteorder.value,
                'size': self.bit_size,
                'type': Pointer.item_type.name,
                'value': self.value,
                'member': [self.data.blueprint()]
            }

        :param str name: optional name for the `Pointer` field.

        :keyword bool nested: if `True` a :class:`Pointer` field lists its
            *nested* :attr:`data` object fields as well (chained method call).
            Default is `True`.
        """
        obj = super().blueprint(name, **options)
        obj['class'] = self.__class__.__name__
        obj['name'] = name if name else self.__class__.__name__
        obj['type'] = Pointer.item_type.name
        if is_any(self._data) and get_nested(options):
            obj['member'] = list()
            obj['member'].append(self._data.blueprint('data', **options))
        return obj


class StructurePointer(Pointer):
    """ A `StructurePointer` field is a :class:`Pointer` which refers
    to a :class:`Structure`.

    :param template: template for the `data` object.
        The *template* must be a :class:`Structure` instance.

    :param int address: absolute address of the `data` object referenced by
        the `StructurePointer` field.

    :param byte_order: coding :class:`Byteorder` of the `bytestream`
        of the `StructurePointer` field.

    Example:

    >>> pointer = StructurePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    Structure()
    >>> pointer.size
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> len(pointer)
    0
    >>> [name for name in pointer.keys()]
    []
    >>> [member.value for member in pointer.values()]
    []
    >>> [(name, member.value) for name, member in pointer.items()]
    []
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'StructurePointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'StructurePointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff',
     'member': [{'class': 'Structure',
                 'name': 'data',
                 'size': 0,
                 'type': 'Structure',
                 'member': []}]}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': OrderedDict()}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', OrderedDict())])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', OrderedDict())])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      StructurePointer(index=Index(byte=0, bit=0,
                                   address=0, base_address=0,
                                   update=False),
                       alignment=(4, 0),
                       bit_size=32,
                       value='0xffffffff'))]
    >>> pprint(pointer.to_list(nested=True))
    [('StructurePointer.value', '0xffffffff')]
    >>> pprint(pointer.to_dict(nested=True))
    OrderedDict([('StructurePointer', OrderedDict([('value', '0xffffffff')]))])
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        if template is None:
            template = Structure()
        elif not is_structure(template):
            raise MemberTypeError(self, template)
        super().__init__(template, address, byte_order=byte_order)

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __getattr__(self, attr):
        return self._data[attr]

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()


class SequencePointer(Pointer):
    """ A `SequencePointer` field is a :class:`Pointer` field which
    refers to a :class:`Sequence`.

    A `SequencePointer` field is:

    *   *containable*: ``item in self`` returns `True` if *item* is part
        of the :class:`Sequence`.
    *   *sized*: ``len(self)`` returns the number of items in the
        :class:`Sequence`.
    *   *subscriptable* ``self[index]`` returns the *item* at the *index*
        of the :class:`Sequence`.
    *   *iterable* ``iter(self)`` iterates over the *items* of the
        :class:`Sequence`

    A `SequencePointer` field supports the usual methods for sequences:

    *   **Append** an item to the :class:`Sequence` via :meth:`append()`.
    *   **Insert** an item before the *index* into the :class:`Sequence`
        via :meth:`insert()`.
    *   **Extend** the :class:`Sequence` with items via :meth:`extend()`.
    *   **Clear** the :class:`Sequence` via :meth:`clear()`.
    *   **Pop** an item with the *index* from the :class:`Sequence`
        via :meth:`pop()`.
    *   **Remove** the first occurrence of an *item* from the
        :class:`Sequence` via :meth:`remove()`.
    *   **Reverse** all items in the :class:`Sequence` via :meth:`reverse()`.

    :param iterable: any *iterable* that contains items of :class:`Structure`,
        :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
        *iterable* is one of these instances itself then the *iterable* itself
        is appended to the :class:`Sequence`.

    :param int address: absolute address of the `data` object referenced by
        the `SequencePointer` field.

    :param byte_order: coding :class:`Byteorder` of the `bytestream`
        of the `SequencePointer` field.

    Example:

    >>> pointer = SequencePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    []
    >>> pointer.size
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> len(pointer)
    0
    >>> [item for item in pointer]
    []
    >>> pointer[:]
    []
    >>> pointer.append(Field())
    >>> pointer[0] # doctest: +NORMALIZE_WHITESPACE
    Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=(0, 0),
          bit_size=0,
          value=None)
    >>> len(pointer)
    1
    >>> pointer.pop() # doctest: +NORMALIZE_WHITESPACE
    Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=(0, 0),
          bit_size=0,
          value=None)
    >>> pointer.insert(0, Field())
    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    [Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=(0, 0),
           bit_size=0,
           value=None)]
    >>> pointer.remove(pointer[0])
    >>> pointer.data
    []
    >>> pointer.clear()
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'SequencePointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'SequencePointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff',
     'member': [{'class': 'Sequence',
                 'name': 'data',
                 'size': 0,
                 'type': 'Sequence',
                 'member': []}]}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': []}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', None)])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', [])])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      SequencePointer(index=Index(byte=0, bit=0,
                                  address=0, base_address=0,
                                  update=False),
                      alignment=(4, 0),
                      bit_size=32,
                      value='0xffffffff'))]
    >>> pprint(pointer.to_list(nested=True))
    [('SequencePointer.value', '0xffffffff')]
    >>> pprint(pointer.to_dict(nested=True))
    OrderedDict([('SequencePointer', OrderedDict([('value', '0xffffffff')]))])
    """

    def __init__(self, iterable=None, address=None, byte_order=BYTEORDER):
        super().__init__(Sequence(iterable), address, byte_order)

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __delitem__(self, index):
        del self._data[index]

    def append(self, item):
        """ Appends the *item* to the end of the :class:`Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        """
        self._data.append(item)

    def insert(self, index, item):
        """ Inserts the *item* before the *index* into the :class:`Sequence`.

        :param int index: :class:`Sequence` index.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        """
        self._data.insert(index, item)

    def pop(self, index=-1):
        """ Removes and returns the item at the *index* from the
        :class:`Sequence`.

        :param int index: :class:`Sequence` index.
        """
        return self._data.pop(index)

    def clear(self):
        """ Remove all items from the :class:`Sequence`."""
        self._data.clear()

    def remove(self, item):
        """ Removes the first occurrence of an *item* from the :class:`Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        """
        self._data.remove(item)

    def reverse(self):
        """ In place reversing of the :class:`Sequence` items."""
        self._data.reverse()

    def extend(self, iterable):
        """ Extends the :class:`Sequence` by appending items from the *iterable*.

        :param iterable: any *iterable* that contains items of :class:`Structure`,
            :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
            *iterable* is one of these instances itself then the *iterable* itself
            is appended to the :class:`Sequence`.
        """
        self._data.extend(iterable)


class ArrayPointer(SequencePointer):
    """ A `ArrayPointer` field is a :class:`SequencePointer` field which
    refers to a :class:`Array`.

    A `ArrayPointer` field adapts and extends a :class:`SequencePointer`
    field with the following features:

    *   **Append** a new :class:`Array` element to the :class:`Array`
        via :meth:`append()`.
    *   **Insert** a new :class:`Array` element before the *index*
        into the :class:`Array` via :meth:`insert()`.
    *   **Re-size** the :class:`Array` via :meth:`resize()`.

    :param template: template for the :class:`Array` element.
        The *template* can be any :class:`Field` instance or any *callable*
        that returns a :class:`Structure`, :class:`Sequence`, :class:`Array`
        or any :class:`Field` instance.

    :param int size: is the size of the :class:`Array` in number of
        :class:`Array` elements.

    :param int address: absolute address of the `data` object referenced by
        the `ArrayPointer` field.

    :param byte_order: coding :class:`Byteorder` of the `bytestream`
        of the `ArrayPointer` field.

    Example:

    >>> pointer = ArrayPointer(Byte)
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    []
    >>> pointer.size
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> len(pointer)
    0
    >>> [item for item in pointer]
    []
    >>> pointer[:]
    []
    >>> pointer.append()
    >>> pointer[0] # doctest: +NORMALIZE_WHITESPACE
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=(1, 0),
         bit_size=8,
         value='0x0')
    >>> len(pointer)
    1
    >>> pointer.pop() # doctest: +NORMALIZE_WHITESPACE
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=(1, 0),
         bit_size=8,
         value='0x0')
    >>> pointer.insert(0)
    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    [Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0')]
    >>> pointer.remove(pointer[0])
    >>> pointer.data
    []
    >>> pointer.resize(10)
    >>> len(pointer)
    10
    >>> pointer.clear()
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'ArrayPointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'ArrayPointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff',
     'member': [{'class': 'Array',
                 'name': 'data',
                 'size': 0,
                 'type': 'Array',
                 'member': []}]}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': []}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', None)])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', [])])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      ArrayPointer(index=Index(byte=0, bit=0,
                               address=0, base_address=0,
                               update=False),
                   alignment=(4, 0),
                   bit_size=32,
                   value='0xffffffff'))]
    >>> pprint(pointer.to_list(nested=True))
    [('ArrayPointer.value', '0xffffffff')]
    >>> pprint(pointer.to_dict(nested=True))
    OrderedDict([('ArrayPointer', OrderedDict([('value', '0xffffffff')]))])
    """

    def __init__(self, template, size=0, address=None, byte_order=BYTEORDER):
        super().__init__(address, byte_order=byte_order)
        self._data = Array(template, size)

    def append(self):
        """ Appends a new :class:`Array` element to the :class:`Array`."""
        self._data.append()

    def insert(self, index):
        """ Inserts a new :class:`Array` element before the *index*
        of the :class:`Array`.

        :param int index: :class:`Array` index.
        """
        self._data.insert(index)

    def resize(self, size):
        """ Re-sizes the :class:`Array` by appending new :class:`Array` elements
        or removing :class:`Array` elements from the end.

        :param int size: new size of the :class:`Array` in number of
            :class:`Array` elements.
        """
        if isinstance(self._data, Array):
            self._data.resize(size)


class StreamPointer(Pointer):
    """ A `StreamPointer` field is a :class:`Pointer` field which
    refers to a :class:`Stream` field.

    A `StreamPointer` field is:

    *   *containable*: ``item in self`` returns `True` if *item* is part
        of the :class:`Stream` field.
    *   *sized*: ``len(self)`` returns the length of the
        :class:`Stream` field.
    *   *subscriptable* ``self[index]`` returns the *byte* at the *index*
        of the :class:`Stream` field.
    *   *iterable* ``iter(self)`` iterates over the bytes of the
        :class:`Stream` field.

    :param int size: is the size of the :class:`Stream` field in bytes.

    :param int address: absolute address of the `data` object referenced by
        the `StreamPointer` field.

    Example:

    >>> pointer = StreamPointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    Stream(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=(0, 0),
           bit_size=0,
           value=b'')
    >>> pointer.size
    0
    >>> len(pointer)
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> pointer.encode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffffffff'
    >>> pointer.resize(10)
    >>> pointer.size
    10
    >>> len(pointer)
    10
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    b'4b6f6e466f6f2069732046756e'
    >>> hexlify(pointer.as_bytestream())
    b'00000000000000000000'
    >>> pointer.refresh()
    Index(byte=10, bit=0, address=4294967305, base_address=4294967295, update=False)
    >>> pointer.as_bytestream()
    bytearray(b'KonFoo is ')
    >>> [byte for byte in pointer]  # converts to int
    [75, 111, 110, 70, 111, 111, 32, 105, 115, 32]
    >>> [hex(byte) for byte in pointer]
    ['0x4b', '0x6f', '0x6e', '0x46', '0x6f', '0x6f', '0x20', '0x69', '0x73', '0x20']
    >>> pointer[5]  # converts to int
    111
    >>> 111 in pointer
    True
    >>> 0x0 in pointer
    False
    >>> pointer[:6]  # converts to bytes
    b'KonFoo'
    >>> pointer[3:6]  # converts to bytes
    b'Foo'
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'StreamPointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'StreamPointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff',
     'member': [{'address': 4294967295,
                 'alignment': [10, 0],
                 'class': 'Stream10',
                 'index': [0, 0],
                 'name': 'data',
                 'order': 'auto',
                 'size': 80,
                 'type': 'Field',
                 'value': '4b6f6e466f6f20697320'}]}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': Index(byte=0, bit=0, address=4294967295, base_address=4294967295, update=False)}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', 'Stream10')])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', b'4b6f6e466f6f20697320')])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      StreamPointer(index=Index(byte=0, bit=0,
                                address=0, base_address=0,
                                update=False),
                    alignment=(4, 0),
                    bit_size=32,
                    value='0xffffffff')),
     ('data',
      Stream(index=Index(byte=0, bit=0,
                         address=4294967295, base_address=4294967295,
                         update=False),
             alignment=(10, 0),
             bit_size=80,
             value=b'4b6f6e466f6f20697320'))]
    >>> pprint(pointer.to_list())
    [('StreamPointer.value', '0xffffffff'),
     ('StreamPointer.data', b'4b6f6e466f6f20697320')]
    >>> pprint(pointer.to_dict())
    {'StreamPointer': {'value': '0xffffffff',
                       'data': b'4b6f6e466f6f20697320'}}
    """

    def __init__(self, size=0, address=None):
        super().__init__(Stream(size), address)

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __iter__(self):
        return iter(self._data)

    def resize(self, size):
        """ Re-sizes the :class:`Stream` field by appending zero bytes or
        removing bytes from the end.

        :param int size: :class:`Stream` size in number of bytes.
        """
        if isinstance(self._data, Stream):
            self._data.resize(size)


class StringPointer(StreamPointer):
    """ A `StringPointer` field is a :class:`StreamPointer` field  which
    refers to a :class:`String` field.

    :param int size: is the *size* of the :class:`String` field in bytes.

    :param int address: absolute address of the `data` object referenced by
        the `StringPointer` field.

    Example:

    >>> pointer = StringPointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    String(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=(0, 0),
           bit_size=0,
           value='')
    >>> pointer.size
    0
    >>> len(pointer)
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> pointer.encode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffffffff'
    >>> pointer.resize(10)
    >>> pointer.size
    10
    >>> len(pointer)
    10
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    b'4b6f6e466f6f2069732046756e'
    >>> hexlify(pointer.as_bytestream())
    b'00000000000000000000'
    >>> pointer.refresh()
    Index(byte=10, bit=0, address=4294967305, base_address=4294967295, update=False)
    >>> pointer.as_bytestream()
    bytearray(b'KonFoo is ')
    >>> [byte for byte in pointer]  # converts to int
    [75, 111, 110, 70, 111, 111, 32, 105, 115, 32]
    >>> [chr(byte) for byte in pointer]  # converts to int
    ['K', 'o', 'n', 'F', 'o', 'o', ' ', 'i', 's', ' ']
    >>> chr(pointer[5])  # converts to int -> chr
    'o'
    >>> ord(' ') in pointer
    True
    >>> 0x0 in pointer
    False
    >>> pointer[:6]  # converts to bytes
    b'KonFoo'
    >>> pointer[3:6]  # converts to bytes
    b'Foo'
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'StringPointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'StringPointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff',
     'member': [{'address': 4294967295,
                 'alignment': [10, 0],
                 'class': 'String10',
                 'index': [0, 0],
                 'name': 'data',
                 'order': 'auto',
                 'size': 80,
                 'type': 'Field',
                 'value': 'KonFoo is '}]}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': Index(byte=0, bit=0, address=4294967295, base_address=4294967295, update=False)}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', 'String10')])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', 'KonFoo is ')])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      StringPointer(index=Index(byte=0, bit=0,
                                address=0, base_address=0,
                                update=False),
                    alignment=(4, 0),
                    bit_size=32,
                    value='0xffffffff')),
     ('data',
      String(index=Index(byte=0, bit=0,
                         address=4294967295, base_address=4294967295,
                         update=False),
             alignment=(10, 0),
             bit_size=80,
             value='KonFoo is '))]
    >>> pprint(pointer.to_list())
    [('StringPointer.value', '0xffffffff'), ('StringPointer.data', 'KonFoo is ')]
    >>> pprint(pointer.to_dict())
    {'StringPointer': {'value': '0xffffffff',
                       'data': 'KonFoo is '}}
    """

    def __init__(self, size=0, address=None):
        super().__init__(size=0, address=address)
        self._data = String(size)


class AutoStringPointer(StringPointer):
    """ A `AutoStringPointer` field is a :class:`StringPointer` field which
    refers to a auto-sized :class:`String` field.

    :param int address: absolute address of the `data` object referenced by
        the `AutoStringPointer` field.

    Example:

    >>> pointer = AutoStringPointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    String(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=(64, 0),
           bit_size=512,
           value='')
    >>> pointer.size
    64
    >>> len(pointer)
    64
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> pointer.encode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffffffff'
    >>> pointer.resize(10)
    >>> pointer.size
    10
    >>> len(pointer)
    10
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    b'4b6f6e466f6f2069732046756e'
    >>> hexlify(pointer.as_bytestream())
    b'00000000000000000000'
    >>> pointer.refresh()
    Index(byte=10, bit=0, address=4294967305, base_address=4294967295, update=False)
    >>> pointer.as_bytestream()
    bytearray(b'KonFoo is ')
    >>> [byte for byte in pointer]  # converts to int
    [75, 111, 110, 70, 111, 111, 32, 105, 115, 32]
    >>> [chr(byte) for byte in pointer]  # converts to int
    ['K', 'o', 'n', 'F', 'o', 'o', ' ', 'i', 's', ' ']
    >>> chr(pointer[5])  # converts to int -> chr
    'o'
    >>> ord(' ') in pointer
    True
    >>> 0x0 in pointer
    False
    >>> pointer[:6]  # converts to bytes
    b'KonFoo'
    >>> pointer[3:6]  # converts to bytes
    b'Foo'
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'AutoStringPointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'AutoStringPointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff',
     'member': [{'address': 4294967295,
                 'alignment': [10, 0],
                 'class': 'String10',
                 'index': [0, 0],
                 'name': 'data',
                 'order': 'auto',
                 'size': 80,
                 'type': 'Field',
                 'value': 'KonFoo is '}]}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': Index(byte=0, bit=0, address=4294967295, base_address=4294967295, update=False)}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', 'String10')])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', 'KonFoo is ')])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      AutoStringPointer(index=Index(byte=0, bit=0,
                                address=0, base_address=0,
                                update=False),
                        alignment=(4, 0),
                        bit_size=32,
                        value='0xffffffff')),
     ('data',
      String(index=Index(byte=0, bit=0,
                         address=4294967295, base_address=4294967295,
                         update=False),
             alignment=(10, 0),
             bit_size=80,
             value='KonFoo is '))]
    >>> pprint(pointer.to_list())
    [('AutoStringPointer.value', '0xffffffff'),
     ('AutoStringPointer.data', 'KonFoo is ')]
    >>> pprint(pointer.to_dict())
    {'AutoStringPointer': {'value': '0xffffffff',
                           'data': 'KonFoo is '}}
    """
    #: Block size in *bytes* to read for the :class:`String` field.
    BLOCK_SIZE = 64
    #: Maximal allowed address of the :class:`String` field.
    MAX_ADDRESS = 0xffffffff

    def __init__(self, address=None):
        super().__init__(size=AutoStringPointer.BLOCK_SIZE, address=address)

    @nested_option(True)
    def read_from(self, provider, null_allowed=False, **options):
        if self._data is None:
            pass
        elif is_provider(provider):
            if self._value < 0:
                pass
            elif null_allowed or self._value > 0:
                self._data_stream = bytes()
                self.resize(0)
                for address in range(self.address,
                                     AutoStringPointer.MAX_ADDRESS,
                                     AutoStringPointer.BLOCK_SIZE):
                    count = limiter(AutoStringPointer.BLOCK_SIZE,
                                    0,
                                    (AutoStringPointer.MAX_ADDRESS - address))
                    self._data_stream += provider.read(address, count)
                    self.resize(len(self) + count)
                    index = self.refresh()
                    # Incomplete data object
                    if index.bit != 0:
                        length = index.byte, index.bit
                        raise ContainerLengthError(self, length)
                    # Terminated?
                    if self.data.is_terminated():
                        self.resize(len(self.data.value) + 1)
                        break
            else:
                self._data_stream = bytes()
                self.resize(0)
                self.refresh()
        else:
            raise ProviderTypeError(self, provider)


class RelativePointer(Pointer):
    """ A `RelativePointer` field is a :class:`Pointer` field which refers
    to a `data` object relatively to a *base address* of a data
    :class:`Provider`.

    :param template: template for the `data` object referenced by the
        `RelativePointer` field.

    :param address: relative address of the `data` object referenced
        by the `RelativePointer` field.

    :param byte_order: coding :class:`Byteorder` of the `bytestream`
        of the `RelativePointer` field.

    Example:

    >>> pointer = RelativePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    >>> pointer.size
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> pointer.encode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffffffff'
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    b'4b6f6e466f6f2069732046756e'
    >>> pointer.as_bytestream()
    bytearray(b'')
    >>> pointer.refresh()
    Index(byte=0, bit=0, address=4294967295, base_address=0, update=False)
    >>> pointer.as_bytestream()
    bytearray(b'')
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'RelativePointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'RelativePointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff'}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': Index(byte=0, bit=0, address=4294967295, base_address=0, update=False)}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', None)])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', None)])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      RelativePointer(index=Index(byte=0, bit=0,
                                  address=0, base_address=0,
                                  update=False),
                      alignment=(4, 0),
                      bit_size=32,
                      value='0xffffffff'))]
    >>> pprint(pointer.to_list())
    [('RelativePointer.value', '0xffffffff')]
    >>> pprint(pointer.to_dict())
    OrderedDict([('RelativePointer', OrderedDict([('value', '0xffffffff')]))])
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template,
                         address=address,
                         byte_order=byte_order)

    @property
    def address(self):
        """ Returns the absolute address of the `data` object
        referenced by the `RelativePointer` field (read-only).
        """
        return self._value + self.base_address

    @property
    def base_address(self):
        """ Returns the base address of the data :class:`Provider` for the
        `data` object referenced by the `RelativePointer` field (read-only).
        """
        return self.index.base_address


class StructureRelativePointer(RelativePointer):
    """ A `StructureRelativePointer` field is a :class:`RelativePointer` which
    refers to a :class:`Structure`.

    :param template: template for the `data` object.
        The *template* must be a :class:`Structure` instance.

    :param address: relative address of the `data` object referenced
        by the `StructureRelativePointer` field.

    :param byte_order: coding :class:`Byteorder` of the `bytestream`
        of the `StructureRelativePointer` field.

    Example:

    >>> pointer = StructureRelativePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    Structure()
    >>> pointer.size
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> len(pointer)
    0
    >>> [name for name in pointer.keys()]
    []
    >>> [member.value for member in pointer.values()]
    []
    >>> [(name, member.value) for name, member in pointer.items()]
    []
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'StructureRelativePointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'StructureRelativePointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff',
     'member': [{'class': 'Structure',
                 'name': 'data',
                 'size': 0,
                 'type': 'Structure',
                 'member': []}]}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': OrderedDict()}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', OrderedDict())])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', OrderedDict())])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      StructureRelativePointer(index=Index(byte=0, bit=0,
                                           address=0, base_address=0,
                                           update=False),
                               alignment=(4, 0),
                               bit_size=32,
                               value='0xffffffff'))]
    >>> pprint(pointer.to_list(nested=True))
    [('StructureRelativePointer.value', '0xffffffff')]
    >>> pprint(pointer.to_dict(nested=True))
    {'StructureRelativePointer': OrderedDict([('value', '0xffffffff')])}
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        if template is None:
            template = Structure()
        elif not is_structure(template):
            raise MemberTypeError(self, template)
        super().__init__(template, address, byte_order=byte_order)

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __getattr__(self, attr):
        return self._data[attr]

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()


class SequenceRelativePointer(RelativePointer):
    """ A `SequenceRelativePointer` field is a :class:`RelativePointer` which
    refers to a :class:`Sequence`.

    A `SequenceRelativePointer` is:

    *   *containable*: ``item in self`` returns `True` if *item* is part
        of the :class:`Sequence`.
    *   *sized*: ``len(self)`` returns the number of items in the
        :class:`Sequence`.
    *   *subscriptable* ``self[index]`` returns the *item* at the *index*
        of the :class:`Sequence`.
    *   *iterable* ``iter(self)`` iterates over the *items* of the
        :class:`Sequence`

    A `SequenceRelativePointer` supports the usual methods:

    *   **Append** an item to the :class:`Sequence` via :meth:`append()`.
    *   **Insert** an item before the *index* into the :class:`Sequence`
        via :meth:`insert()`.
    *   **Extend** the :class:`Sequence` with items via :meth:`extend()`.
    *   **Clear** the :class:`Sequence` via :meth:`clear()`.
    *   **Pop** an item with the *index* from the :class:`Sequence`
        via :meth:`pop()`.
    *   **Remove** the first occurrence of an *item* from the
        :class:`Sequence` via :meth:`remove()`.
    *   **Reverse** all items in the :class:`Sequence` via :meth:`reverse()`.

    :param iterable: any *iterable* that contains items of :class:`Structure`,
        :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
        *iterable* is one of these instances itself then the *iterable* itself
        is appended to the :class:`Sequence`.

    :param address: relative address of the `data` object referenced
        by the `SequenceRelativePointer` field.

    :param byte_order: coding :class:`Byteorder` of the `bytestream`
        of the `SequenceRelativePointer` field.

    Example:

    >>> pointer = SequenceRelativePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    []
    >>> pointer.size
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> len(pointer)
    0
    >>> [item for item in pointer]
    []
    >>> pointer[:]
    []
    >>> pointer.append(Field())
    >>> pointer[0] # doctest: +NORMALIZE_WHITESPACE
    Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=(0, 0),
          bit_size=0,
          value=None)
    >>> len(pointer)
    1
    >>> pointer.pop() # doctest: +NORMALIZE_WHITESPACE
    Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=(0, 0),
          bit_size=0,
          value=None)
    >>> pointer.insert(0, Field())
    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    [Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=(0, 0),
           bit_size=0,
           value=None)]
    >>> pointer.remove(pointer[0])
    >>> pointer.data
    []
    >>> pointer.clear()
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'SequenceRelativePointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'SequenceRelativePointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff',
     'member': [{'class': 'Sequence',
                 'name': 'data',
                 'size': 0,
                 'type': 'Sequence',
                 'member': []}]}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': []}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', None)])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', [])])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      SequenceRelativePointer(index=Index(byte=0, bit=0,
                                          address=0, base_address=0,
                                          update=False),
                              alignment=(4, 0),
                              bit_size=32,
                              value='0xffffffff'))]
    >>> pprint(pointer.to_list(nested=True))
    [('SequenceRelativePointer.value', '0xffffffff')]
    >>> pprint(pointer.to_dict(nested=True))
    {'SequenceRelativePointer': OrderedDict([('value', '0xffffffff')])}
    """

    def __init__(self, iterable=None, address=None, byte_order=BYTEORDER):
        super().__init__(Sequence(iterable), address, byte_order)

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __delitem__(self, index):
        del self._data[index]

    def append(self, item):
        """ Appends the *item* to the end of the :class:`Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        """
        self._data.append(item)

    def insert(self, index, item):
        """ Inserts the *item* before the *index* into the :class:`Sequence`.

        :param int index: :class:`Sequence` index.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        """
        self._data.insert(index, item)

    def pop(self, index=-1):
        """ Removes and returns the item at the *index* from the
        :class:`Sequence`.

        :param int index: :class:`Sequence` index
        """
        return self._data.pop(index)

    def clear(self):
        """ Remove all items from the :class:`Sequence`."""
        self._data.clear()

    def remove(self, item):
        """ Removes the first occurrence of an *item* from the :class:`Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        """
        self._data.remove(item)

    def reverse(self):
        """ In place reversing of the :class:`Sequence` items."""
        self._data.reverse()

    def extend(self, iterable):
        """ Extends the :class:`Sequence` by appending items from the *iterable*.

        :param iterable: any *iterable* that contains items of :class:`Structure`,
            :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
            *iterable* is one of these instances itself then the *iterable* itself
            is appended to the :class:`Sequence`.
        """
        self._data.extend(iterable)


class ArrayRelativePointer(SequenceRelativePointer):
    """ A `ArrayRelativePointer` field is a :class:`SequenceRelativePointer`
    which refers to a :class:`Array`.

    A `ArrayRelativePointer` adapts and extends a :class:`SequenceRelativePointer`
    with the following features:

    *   **Append** a new :class:`Array` element to the :class:`Array`
        via :meth:`append()`.
    *   **Insert** a new :class:`Array` element before the *index*
        into the :class:`Array` via :meth:`insert()`.
    *   **Re-size** the :class:`Array` via :meth:`resize()`.

    :param template: template for the :class:`Array` element.
        The *template* can be any :class:`Field` instance or any *callable*
        that returns a :class:`Structure`, :class:`Sequence`, :class:`Array`
        or any :class:`Field` instance.

    :param int size: is the size of the :class:`Array` in number of
        :class:`Array` elements.

    :param address: relative address of the `data` object referenced
        by the `ArrayRelativePointer` field.

    :param byte_order: coding :class:`Byteorder` of the `bytestream`
        of the `ArrayRelativePointer` field.

    Example:

    >>> pointer = ArrayRelativePointer(Byte)
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    []
    >>> pointer.size
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> len(pointer)
    0
    >>> [item for item in pointer]
    []
    >>> pointer[:]
    []
    >>> pointer.append()
    >>> pointer[0] # doctest: +NORMALIZE_WHITESPACE
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=(1, 0),
         bit_size=8,
         value='0x0')
    >>> len(pointer)
    1
    >>> pointer.pop() # doctest: +NORMALIZE_WHITESPACE
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=(1, 0),
         bit_size=8,
         value='0x0')
    >>> pointer.insert(0)
    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    [Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=(1, 0),
          bit_size=8,
          value='0x0')]
    >>> pointer.remove(pointer[0])
    >>> pointer.data
    []
    >>> pointer.resize(10)
    >>> len(pointer)
    10
    >>> pointer.clear()
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'ArrayRelativePointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'ArrayRelativePointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff',
     'member': [{'class': 'Array',
                 'name': 'data',
                 'size': 0,
                 'type': 'Array',
                 'member': []}]}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': []}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', None)])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', [])])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      ArrayRelativePointer(index=Index(byte=0, bit=0,
                                       address=0, base_address=0,
                                       update=False),
                           alignment=(4, 0),
                           bit_size=32,
                           value='0xffffffff'))]
    >>> pprint(pointer.to_list(nested=True))
    [('ArrayRelativePointer.value', '0xffffffff')]
    >>> pprint(pointer.to_dict(nested=True))
    OrderedDict([('ArrayRelativePointer', OrderedDict([('value', '0xffffffff')]))])
    """

    def __init__(self, template, size=0, address=None, byte_order=BYTEORDER):
        super().__init__(address, byte_order=byte_order)
        self._data = Array(template, size)

    def append(self):
        """ Appends a new :class:`Array` element to the :class:`Array`."""
        self._data.append()

    def insert(self, index):
        """ Inserts a new :class:`Array` element before the *index*
        of the :class:`Array`.

        :param int index: :class:`Array` index.
        """
        self._data.insert(index)

    def resize(self, size):
        """ Re-sizes the :class:`Array` by appending new :class:`Array` elements
        or removing :class:`Array` elements from the end.

        :param int size: new size of the :class:`Array` in number of
            :class:`Array` elements.
        """
        if isinstance(self._data, Array):
            self._data.resize(size)


class StreamRelativePointer(RelativePointer):
    """ A `StreamRelativePointer` field is a :class:`RelativePointer` field
    which refers to a :class:`Stream` field.

    A `StreamRelativePointer` field is:

    *   *containable*: ``item in self`` returns `True` if *item* is part
        of the :class:`Stream` field.
    *   *sized*: ``len(self)`` returns the length of the
        :class:`Stream` field.
    *   *subscriptable* ``self[index]`` returns the *byte* at the *index*
        of the :class:`Stream` field.
    *   *iterable* ``iter(self)`` iterates over the bytes of the
        :class:`Stream` field.

    :param int size: is the size of the :class:`Stream` field in bytes.

    :param address: relative address of the `data` object referenced
        by the `StreamRelativePointer` field.

    Example:

    >>> pointer = StreamRelativePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    Stream(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=(0, 0),
           bit_size=0,
           value=b'')
    >>> pointer.size
    0
    >>> len(pointer)
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> pointer.encode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffffffff'
    >>> pointer.resize(10)
    >>> pointer.size
    10
    >>> len(pointer)
    10
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    b'4b6f6e466f6f2069732046756e'
    >>> hexlify(pointer.as_bytestream())
    b'00000000000000000000'
    >>> pointer.refresh()
    Index(byte=10, bit=0, address=4294967305, base_address=0, update=False)
    >>> pointer.as_bytestream()
    bytearray(b'KonFoo is ')
    >>> [byte for byte in pointer]  # converts to int
    [75, 111, 110, 70, 111, 111, 32, 105, 115, 32]
    >>> [hex(byte) for byte in pointer]
    ['0x4b', '0x6f', '0x6e', '0x46', '0x6f', '0x6f', '0x20', '0x69', '0x73', '0x20']
    >>> pointer[5]  # converts to int
    111
    >>> 111 in pointer
    True
    >>> 0x0 in pointer
    False
    >>> pointer[:6]  # converts to bytes
    b'KonFoo'
    >>> pointer[3:6]  # converts to bytes
    b'Foo'
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'StreamRelativePointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'StreamRelativePointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff',
     'member': [{'address': 4294967295,
                 'alignment': [10, 0],
                 'class': 'Stream10',
                 'index': [0, 0],
                 'name': 'data',
                 'order': 'auto',
                 'size': 80,
                 'type': 'Field',
                 'value': '4b6f6e466f6f20697320'}]}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': Index(byte=0, bit=0, address=4294967295, base_address=0, update=False)}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', 'Stream10')])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', b'4b6f6e466f6f20697320')])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      StreamRelativePointer(index=Index(byte=0, bit=0,
                                        address=0, base_address=0,
                                        update=False),
                            alignment=(4, 0),
                            bit_size=32,
                            value='0xffffffff')),
     ('data',
      Stream(index=Index(byte=0, bit=0,
                         address=4294967295, base_address=0,
                         update=False),
             alignment=(10, 0),
             bit_size=80,
             value=b'4b6f6e466f6f20697320'))]
    >>> pprint(pointer.to_list())
    [('StreamRelativePointer.value', '0xffffffff'),
     ('StreamRelativePointer.data', b'4b6f6e466f6f20697320')]
    >>> pprint(pointer.to_dict())
    {'StreamRelativePointer': {'value': '0xffffffff',
                               'data': b'4b6f6e466f6f20697320'}}
    """

    def __init__(self, size=0, address=None):
        super().__init__(Stream(size), address)

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def resize(self, size):
        """ Re-sizes the :class:`Stream` field by appending zero bytes or
        removing bytes from the end.

        :param int size: :class:`Stream` size in number of bytes.
        """
        if isinstance(self._data, Stream):
            self._data.resize(size)


class StringRelativePointer(StreamRelativePointer):
    """ A `StringRelativePointer` field is a :class:`StreamRelativePointer`
    which refers to a :class:`String` field.

    :param int size: is the *size* of the :class:`String` field in bytes.

    :param address: relative address of the `data` object referenced
        by the `StringRelativePointer` field.

    Example:

    >>> pointer = StringRelativePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    (4, 0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.next_index()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data # doctest: +NORMALIZE_WHITESPACE
    String(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=(0, 0),
           bit_size=0,
           value='')
    >>> pointer.size
    0
    >>> len(pointer)
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    b''
    >>> pointer.value
    '0x0'
    >>> pointer.decode(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.value = -0x1
    >>> pointer.value
    '0x0'
    >>> pointer.value = 0x100000000
    >>> pointer.value
    '0xffffffff'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> pointer.encode(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffffffff'
    >>> pointer.resize(10)
    >>> pointer.size
    10
    >>> len(pointer)
    10
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    b'4b6f6e466f6f2069732046756e'
    >>> hexlify(pointer.as_bytestream())
    b'00000000000000000000'
    >>> pointer.refresh()
    Index(byte=10, bit=0, address=4294967305, base_address=0, update=False)
    >>> pointer.as_bytestream()
    bytearray(b'KonFoo is ')
    >>> [byte for byte in pointer]  # converts to int
    [75, 111, 110, 70, 111, 111, 32, 105, 115, 32]
    >>> [chr(byte) for byte in pointer]  # converts to int
    ['K', 'o', 'n', 'F', 'o', 'o', ' ', 'i', 's', ' ']
    >>> chr(pointer[5])  # converts to int -> chr
    'o'
    >>> ord(' ') in pointer
    True
    >>> 0x0 in pointer
    False
    >>> pointer[:6]  # converts to bytes
    b'KonFoo'
    >>> pointer[3:6]  # converts to bytes
    b'Foo'
    >>> pprint(pointer.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'StringRelativePointer',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'StringRelativePointer',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Pointer',
     'value': '0xffffffff',
     'member': [{'address': 4294967295,
                 'alignment': [10, 0],
                 'class': 'String10',
                 'index': [0, 0],
                 'name': 'data',
                 'order': 'auto',
                 'size': 80,
                 'type': 'Field',
                 'value': 'KonFoo is '}]}
    >>> pprint(pointer.field_indexes())
    {'value': Index(byte=0, bit=0, address=0, base_address=0, update=False),
     'data': Index(byte=0, bit=0, address=4294967295, base_address=0, update=False)}
    >>> pprint(pointer.field_types())
    OrderedDict([('value', 'Pointer32'), ('data', 'String10')])
    >>> pprint(pointer.field_values())
    OrderedDict([('value', '0xffffffff'), ('data', 'KonFoo is ')])
    >>> pprint(pointer.field_items()) # doctest: +NORMALIZE_WHITESPACE
    [('value',
      StringRelativePointer(index=Index(byte=0, bit=0,
                                        address=0, base_address=0,
                                        update=False),
                            alignment=(4, 0),
                            bit_size=32,
                            value='0xffffffff')),
     ('data',
      String(index=Index(byte=0, bit=0,
                         address=4294967295, base_address=0,
                         update=False),
             alignment=(10, 0),
             bit_size=80,
             value='KonFoo is '))]
    >>> pprint(pointer.to_list())
    [('StringRelativePointer.value', '0xffffffff'),
     ('StringRelativePointer.data', 'KonFoo is ')]
    >>> pprint(pointer.to_dict())
    {'StringRelativePointer': {'value': '0xffffffff',
                               'data': 'KonFoo is '}}
    """

    def __init__(self, size=0, address=None):
        super().__init__(size=0, address=address)
        self._data = String(size)
