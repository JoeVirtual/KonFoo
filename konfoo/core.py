# -*- coding: utf-8 -*-
"""
    core.py
    ~~~~~~~
    <Add description of the module here>.

    :copyright: (c) 2015 by Jochen Gerhaeusser.
    :license: BSD-style, see LICENSE for details
"""

import math
import struct
import copy
import time
import datetime
import calendar
from collections import Mapping, namedtuple, OrderedDict
from collections.abc import MutableSequence
from configparser import ConfigParser
from binascii import hexlify, unhexlify
import abc

from konfoo.enums import Enumeration

from konfoo.globals import ItemClass, Byteorder, BYTEORDER, \
    Option, get_byte_order, get_nested, get_field_types, verbose, \
    byte_order_option, field_types_option, nested_option, verbose_option, \
    limiter

from konfoo.providers import Provider

from konfoo.exceptions import OutOfRange, InvalidSize, BadAligned


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


def is_structure(obj):
    return isinstance(obj, Structure)


def is_mapping(obj):
    return isinstance(obj, Mapping)


def is_pointer(obj):
    return isinstance(obj, Pointer)


def is_mixin(obj):
    return is_container(obj) or is_pointer(obj)


#: Memory Patch
Patch = namedtuple('Patch', ['buffer', 'address', 'byteorder', 'bit_size', 'bit_offset', 'inject'])

#: Field index
Index = namedtuple('Index', ['byte', 'bit', 'address', 'base_address', 'update'])


def zero():
    return Index(0, 0, 0, 0, False)


class Container(metaclass=abc.ABCMeta):
    """The abstract `Container` class is a meta class for all classes which
    can contain `Field` items. Container classes are `Structures`, `Sequences`,
    `Arrays` and `Pointers`.

    The `Container` class provides core features to save, load and view the
    values of the `Field` items in a container class.


    """

    def field_items(self, root=str(), **options):
        """Returns a flat list which contains tuples in the form of
        ``(path, item)`` for each `Field` of a `Container`.

        .. note::

           This method must be overwritten by a derived class.

        :param str root: root path.

        :keyword bool nested: if `True` the `Fields` of the *nested* `data`
            objects of all `Pointer` fields in a `Container` are added to
            the list.
        """
        return list()

    @nested_option()
    @field_types_option()
    def to_list(self, name=str(), **options):
        """Returns a flat list which contains tuples in the form of
        ``(path, type, value)`` for each `Field` of a `Container`

        The type of the field is optional.

        :param str name: name of the `Container`.
            Default is the class name of the instance.

        :keyword bool nested: if `True` all `Pointer` fields of a `Container`
            lists their *nested* `data` object as well.

        :keyword bool field_types: if `True` the type of the `Field` is
            inserted into the tuple.
        """
        # Name of the `Container`
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
        """Returns a flat ordered dictionary which contains the
        `path`, `value` pairs for each `Field` of a `Container`.

        Returns a flat ordered dictionary of all `Field` values of a
        `Container`.

        :param str name: name of the `Container`.
            Default is the class name of the instance.

        :keyword bool nested: if `True` all `Pointer` fields of a `Container`
            lists their *nested* `data` object as well.

        :keyword bool field_types: if `True` the type of the `Field` is
            append to the end of path string with '|' as separator.
        """
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
    @verbose_option(True)
    def load(self, file, section=str(), **options):
        """Loads the `Field` values of a `Container` from an *INI file*.

        .. code-block:: ini

            [self.__class__.name]
            field =
            stream =
            structure.field =
            array[0] =
            array[1] =
            array[2] =
            pointer.value = 0
            pointer.data =

        :param str file: name and location of the *INI file*.

        :param str section: section in the INI *file* to look for the `Field`
            values of a `Container`. If no *section* is specified the class
            name of the instance is used.

        :keyword bool field_types: if `True` the type of the `Field` is
            append to the end of path string with '|' as separator.

        :keyword bool verbose: if `True` the loading is executed in verbose mode.
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
                    # Bool field
                    if field.is_bool():
                        field.value = parser.getboolean(section, option)
                    # Float field
                    elif field.is_float():
                        field.value = parser.getfloat(section, option)
                    # String field
                    elif field.is_string():
                        field.value = parser.get(section, option)
                    # Stream field
                    elif field.is_stream():
                        value = parser.get(section, option)
                        stream = unhexlify(value.replace("b'", '').
                                           replace("'", ""))
                        # Auto size a zero sized stream field to
                        # the current stream length
                        if not len(field):
                            field.resize(len(stream))
                        field.value = stream
                    # Decimal field
                    else:
                        field.value = parser.get(section, option)
                    verbose(options, "{0}.{1} = {2}".format(section, option, field.value))
        else:
            verbose(options, "No section [{0}] found.".format(section))

    @nested_option()
    @field_types_option()
    @verbose_option(True)
    def save(self, file, section=str(), **options):
        """Saves the `Field` values of a `Container` to a *INI file*.

        >>> class Foo(Structure):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.field = Field()
        ...         self.stream = Stream()
        ...         self.structure = Structure()
        ...         self.array = Array(Field, 3)
        ...         self.pointer = Pointer()

        .. code-block:: ini

            [self.__class__.name]
            field = ...
            stream = ...
            structure = ...
            array[0] = ...
            array[1] = ...
            array[2] = ...
            pointer.value = ...
            pointer.data = ...

        :param str file: name and location of the *INI file*.

        :param str section: section in the INI file to look for the `Field`
            values of a `Container`. If no *section* is specified the class
            name of the instance is used.

        :keyword bool nested: if `True` all `Pointer` fields of a `Container`
            stores all `Field` values for their *nested* `data` objects as well.

        :keyword bool field_types: if `True` the type of the `Field` is
            appended to its path string with the '|' sign as separator.

        :keyword bool verbose: if `True` the saving is executed in verbose mode.
        """
        parser = ConfigParser()
        parser.read_dict(self.to_dict(section, **options))
        with open(file, 'w') as handle:
            parser.write(handle)
        handle.close()


class Structure(OrderedDict, Container):
    """A `Structure` is a :class:`ordered dictionary <collections.OrderedDict>`
    whereby the dictionary `key` describes the name of a member of the
    `Structure` and the `value` of a dictionary `key` describes the type of
    a member of the `Structure`. Allowed members are `Structure`, `Sequence`,
    `Array` or `Field` instances.

    The `Structure` class extends the :class:`ordered dictionary
    <collections.OrderedDict>` from the Python standard module :mod:`collections`
    with the :class:`Container` class and attribute getter and setter for the
    `key`, `value` pairs to access and to assign  the members of a `Structure`
    easier, but this comes with the cost that the dictionary `keys` must be valid
    python attribute names.

    A `Structure` has additional methods for reading, decoding, encoding and
    viewing binary data:

    *   **Read** from a `Provider` the necessary bytes for each `data`
        object referenced by the `Pointer` fields in a `Structure`
        via :meth:`read()`.
    *   **Decode** the *field values* of a `Structure` from a byte stream
        via :meth:`decode()`.
    *   **Encode** the *field values* of a `Structure` to a byte stream
        via :meth:`encode()`.
    *   Get the **next index** after the last *field* of a `Structure`
        via :meth:`next_index()`.
    *   Get the **first field** of a `Structure`
        via :meth:`first_field()`.
    *   Get the accumulated **length** of all *fields* in a `Structure`
        via :meth:`field_length()`.
    *   View the **index** for each *field* in a `Structure`
        via :meth:`field_indexes()`.
    *   View the **type** for each *field* in a `Structure`
        via :meth:`field_types()`.
    *   View the **value** for each *field* in a `Structure`
        via :meth:`field_values()`.
    *   List the **item** and its path for each *field* in a `Structure`
        as a flat list via :meth:`field_items()`.
    *   Get a **blueprint** of a `Structure` and its items
        via :meth:`blueprint()`,
    """
    item_type = ItemClass.Structure

    def __init__(self, *args, **options):
        super().__init__(*args, **options)

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
            raise TypeError(name, item)

    def __getattr__(self, name):
        """Returns the field of the `Structure` member whose dictionary key
        is equal to the *name*.

        If the attribute *name* is in the namespace of the `Ordered Dictionary`
        base class then the base class is called instead.

        The `__getattr__` method is only called when the method
        `__getattribute__` raises an `AttributeError` exception.
        """
        if name.startswith('_OrderedDict__'):
            return super().__getattribute__(name)
        else:
            return self[name]

    def __setattr__(self, name, item):
        """Assigns the *item* to the member of the `Structure` whose dictionary
        key is equal to the *name*.

        If the attribute *name* is in the namespace of the `Ordered Dictionary`
        base class then the base class is called instead.
        """
        if name.startswith('_OrderedDict__'):
            return super().__setattr__(name, item)
        elif is_any(item):
            self[name] = item
        else:
            raise TypeError(name, item)

    @nested_option()
    def read(self, provider, **options):
        """All `Pointer` fields of a `Structure` read the necessary amount
        of bytes from the data *provider* for their *nested* `data` object
        fields.

        :param provider: data :class:`Provider`.

        :keyword bool nested: if `True` all :class:`Pointer` fields of a
            `Structure` reads their *nested* `data` object fields.
            A `Pointer` field stores the bytes for the *nested* `data`
            object in its own `bytestream`.
        """
        for item in self.values():
            # Container or Pointer
            if is_mixin(item):
                item.read(provider, **options)

    @byte_order_option()
    @nested_option()
    def decode(self, buffer=bytes(), index=zero(), **options):
        """Decodes sequential bytes from a *buffer* starting at the begin
        of the *buffer* or with a given *index* by mapping the bytes to the
        `Fields` of a `Structure` in accordance with the decoding `Byteorder`
        of the *buffer* and the `Field`.

        A specific coding byte order of a `Field` overrules the decoding
        byte order of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the last `Field`
        of the `Structure`.

        Optional the decoding of the `data` objects of all `Pointer` fields
        of a `Structure` can be enabled.

        :keyword byte_order: decoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` all :class:`Pointer` fields of a
            `Structure` decodes their *nested* `data` object fields as well.
            A `Pointer` field uses for the decoding of the *nested* `data`
            object its own `bytestream`.
        """
        for item in self.values():
            index = item.decode(buffer, index, **options)
        return index

    @byte_order_option()
    @nested_option()
    def encode(self, buffer=bytearray(), index=zero(), **options):
        """Encodes sequential bytes to a *buffer* starting at the begin of
        the *buffer* or with a given *index* by mapping the values of the
        `Fields` of a `Structure` to the bytes in accordance with the
        encoding `Byteorder` of the *buffer* and the `Field`.

        A specific coding byte order of a `Field` overrules the encoding
        byte order of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the last `Field`
        of the `Structure`.

        Optional the encoding of the *nested* `data` objects of all `Pointer`
        fields of a `Structure` can be enabled.

        :keyword byte_order: encoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` all :class:`Pointer` fields of a
            `Structure` encodes their *nested* `data` object as well.
            A `Pointer` field uses for the encoding of the *nested* `data`
            object its own `bytestream`.
        """
        for item in self.values():
            index = item.encode(buffer, index, **options)
        return index

    @nested_option()
    def next_index(self, index=zero(), **options):
        """Returns the `Index` after the last `Field` of a `Structure`.

        :param index: :class:`Index` for the first `Field` of a `Structure`.

        :keyword nested: if `True` all `Pointer` fields of a `Structure`
            indexes their *nested* `data` object as well.
        """
        for item in self.values():
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
                raise TypeError(index, item)
        return index

    def first_field(self):
        """Returns the first field of a `Structure` or `None` for an empty
        `Structure`.
        """
        for item in self.values():
            # Container
            if is_container(item):
                field = item.first_field()
                if field is not None:
                    return field
            # Field
            elif is_field(item):
                return item
            else:
                raise TypeError(item)
        return None

    def field_length(self):
        """Returns the length of a `Structure` as a tuple in the form of
        ``(number of bytes, remaining number of bits)``.
        """
        length = 0
        for item in self.values():
            # Container
            if is_container(item):
                byte_length, bit_length = item.field_length()
                length += bit_length + byte_length * 8
            # Field
            elif is_field(item):
                length += item.bit_size
            else:
                raise TypeError(divmod(length, 8), item)
        return divmod(length, 8)

    @nested_option()
    def field_indexes(self, index=zero(), **options):
        """Returns a ordered dictionary which contains the `name`, `index`
        pairs for each `Field` of the `Structure`.

        :param index: optional start :class:`Index` of the `Structure`.

        :keyword nested: if `True` all `Pointer` fields of a `Structure`
            lists their *nested* `data` object fields as well.
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
                raise TypeError(index, name, item)
        return indexes

    @nested_option()
    def field_types(self, **options):
        """Returns a ordered dictionary which contains the `name`, `type`
        pairs for each `Field` of a `Structure`.

        :keyword bool nested: if `True` all `Pointer` fields of a `Structure`
            lists their *nested* `data` object fields as well.
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
                raise TypeError(name, item)
        return types

    @nested_option()
    def field_values(self, **options):
        """Returns a ordered dictionary which contains the `name`, `value`
        pairs for each `Field` of a `Structure`.

        :keyword bool nested: if `True` all `Pointer` fields of a `Structure`
            lists their *nested* `data` object as well.
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
                raise TypeError(name, item)
        return values

    @nested_option()
    def field_items(self, root=None, **options):
        """Returns a flat list which contains tuples in the form of
        ``(path, item)`` for each `Field` of a `Structure`.

        :param str root: root path.

        :keyword bool nested: if `True` the `Fields` of the *nested* `data`
            objects of all `Pointer` fields in a `Structure` are added to
            the list.
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
                raise TypeError(path, item)
        return items

    @nested_option(True)
    def blueprint(self, name=str(), **options):
        """Returns the blue print of a `Structure` as an ordered dictionary
        including the blue prints of the nested fields.

        .. code-block:: python

            blueprint = {
                'class': self.__class__.__name__,
                'name': name if name else self.__class__.__name__,
                'size': len(self),
                'type': Structure.item_type.name
                'member': [
                    field.blueprint(member) for member, field in self.items()
                ]
            }

        :param str name: optional name for the `Structure`.

        :keyword bool nested: if `True` all `Pointer` fields of a `Structure`
            lists their *nested* `data` object fields as well.
        """
        members = list()
        obj = OrderedDict()
        obj['class'] = self.__class__.__name__
        obj['name'] = name if name else self.__class__.__name__
        obj['size'] = len(self)
        obj['type'] = Structure.item_type.name
        obj['member'] = members

        for member_name, item in self.items():
            if is_any(item):
                members.append(item.blueprint(member_name, **options))
            else:
                raise TypeError(member_name, item)
        return obj


class Sequence(MutableSequence, Container):
    """A `Sequence` contains

    A `Sequence` is:

    *   *containable*: ``item in self`` returns `True` if *item* is part
        of the `Sequence`.
    *   *sized*: ``len(self)`` returns the number of items in the `Sequence`.
    *   *subscriptable* ``self[index]`` returns the *item* at the *index*
        of the `Sequence`.
    *   *iterable* ``iter(self)`` iterates over the *items* of the `Sequence`

    A `Sequence` supports the usual methods:

    *   **Append** a item to a `Sequence`
        via :meth:`append()`.
    *   **Insert** a item before the *index* into a `Sequence`
        via :meth:`insert()`.
    *   **Extend** a `Sequence` with items
        via :meth:`extend()`.
    *   **Clear** a `Sequence`
        via :meth:`clear()`.
    *   **Pop** a item with the *index* from a `Sequence`
        via :meth:`pop()`.
    *   **Remove**  the first occurrence of an *item* from a `Sequence`
        via :meth:`remove()`.
    *   **Reverse** all items in a `Sequence`
        via :meth:`reverse()`.

    A `Sequence` has additional methods for reading, decoding, encoding and
    viewing binary data:

    *   **Read** from a `Provider` the necessary bytes for each `data`
        object referenced by the `Pointer` fields in a `Sequence`
        via :meth:`read()`.
    *   **Decode** the *field values* of a `Sequence` from a byte stream
        via :meth:`decode()`.
    *   **Encode** the *field values* of a `Sequence` to a byte stream
        via :meth:`encode()`.
    *   Get the **next index** after the last *field* of a `Sequence`
        via :meth:`next_index()`.
    *   Get the **first field** of a `Sequence`
        via :meth:`first_field()`.
    *   Get the accumulated **length** of all *fields* in a `Sequence`
        via :meth:`field_length()`.
    *   View the **index** for each *field* in a `Sequence`
        via :meth:`field_indexes()`.
    *   View the **type** for each *field* in a `Sequence`
        via :meth:`field_types()`.
    *   View the **value** for each *field* in a `Sequence`
        via :meth:`field_values()`.
    *   List the **item** and its path for each *field* in a `Sequence`
        as a flat list via :meth:`field_items()`.
    *   Get a **blueprint** of a `Sequence` and its items
        via :meth:`blueprint()`,

    :param iterable: any *iterable* that contains items of `Structure`,
        `Sequence`, `Array` or `Field` instances. If the *iterable* is one
        of these instances itself then the *iterable* itself is appended
        to the `Sequence`.
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
            for field in iterable:
                if not is_any(field):
                    raise TypeError(field)
                self.append(field)

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

    def __setitem__(self, index, field):
        if not is_any(field):
            raise TypeError(field)
        self._data[index] = field

    def __delitem__(self, index):
        del self._data[index]

    def __iter__(self):
        return iter(self._data)

    def append(self, item):
        """Appends the *item* to the end of the `Sequence`."""
        if not is_any(item):
            raise TypeError(item)
        self._data.append(item)

    def insert(self, index, item):
        """Inserts the *item* before the *index* into the `Sequence`.

        :param int index: `Sequence` index.
        :param item:
        """
        if not is_any(item):
            raise TypeError(item)
        self._data.insert(index, item)

    def pop(self, index=-1):
        """Removes and returns the item at the *index* from the `Sequence`."""
        return self._data.pop(index)

    def clear(self):
        """Remove all items from the `Sequence`."""
        self._data.clear()

    def remove(self, item):
        """Removes the first occurrence of an *item* from the `Sequence`."""
        self._data.remove(item)

    def reverse(self):
        """In place reversing of the `Sequence` items."""
        self._data.reverse()

    def extend(self, iterable):
        """Extends the `Sequence` by appending items from the *iterable*."""
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
            raise TypeError(iterable)

    @nested_option()
    def read(self, provider, **options):
        """All `Pointer` fields of a `Sequence` read the necessary amount of
        bytes from the data *provider* for their *nested* `data` object fields.

        :param provider: data :class:`Provider`.

        :keyword bool nested: if `True` all :class:`Pointer` fields of a
            `Sequence` reads their *nested* `data` object fields.
            A `Pointer` field stores the bytes for the *nested* `data`
            object in its own `bytestream`.
        """
        for item in iter(self):
            if is_container(item) or is_pointer(item):
                item.read(provider, **options)

    @byte_order_option()
    @nested_option()
    def decode(self, buffer=bytes(), index=zero(), **options):
        """Decodes sequential bytes from a *buffer* starting at the begin
        of the *buffer* or with a given *index* by mapping the bytes to the
        `Fields` of a `Sequence` in accordance with the decoding `Byteorder`
        of the *buffer* and the `Field`.

        A specific coding byte order of a `Field` overrules the decoding
        byte order of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the last `Field`
        of the `Sequence`.

        Optional the decoding of the *nested* `data` objects of all `Pointer`
        fields of a `Sequence` can be enabled.

        :keyword byte_order: decoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` all :class:`Pointer` fields of a
            `Sequence` decodes their *nested* `data` object fields as well.
            A `Pointer` field uses for the decoding of the *nested* `data`
            object its own `bytestream`.
        """
        for item in iter(self):
            index = item.decode(buffer, index, **options)
        return index

    @byte_order_option()
    @nested_option()
    def encode(self, buffer=bytearray(), index=zero(), **options):
        """Encodes sequential bytes to a *buffer* starting at the begin of
        the *buffer* or with a given *index* by mapping the values of the
        `Fields` of a `Sequence` to the bytes in accordance with the
        encoding `Byteorder` of the *buffer* and the `Field`.

        A specific coding byte order of a `Field` overrules the encoding
        byte order of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the last `Field`
        of the `Sequence`.

        Optional the encoding of the *nested* `data` objects of all `Pointer`
        fields of a `Sequence` can be enabled.

        :keyword byte_order: encoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` all :class:`Pointer` fields of a
            `Sequence` encodes their *nested* `data` object as well.
            A `Pointer` field uses for the encoding of the *nested* `data`
            object its own `bytestream`.
        """
        for item in iter(self):
            index = item.encode(buffer, index, **options)
        return index

    @nested_option()
    def next_index(self, index=zero(), **options):
        """Returns the `Index` after the last `Field` of a `Sequence`.

        :param index: :class:`Index` for the first `Field` of a `Sequence`.

        :keyword bool nested: if `True` all `Pointer` fields of a `Sequence`
            indexes their *nested* `data` object as well.
        """
        for item in iter(self):
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
                raise TypeError(index, item)
        return index

    def first_field(self):
        """Returns the first field of a `Sequence` or `None` for an empty
        `Sequence`.
        """
        for item in iter(self):
            # Container
            if is_container(item):
                field = item.first_field()
                if field is not None:
                    return field
            # Field
            elif is_field(item):
                return item
            else:
                raise TypeError(item)
        return None

    def field_length(self):
        """Returns the length of a `Sequence` as a tuple in the form of
        ``(number of bytes, remaining number of bits)``.
        """
        length = 0
        for item in iter(self):
            # Container
            if is_container(item):
                byte_length, bit_length = item.field_length()
                length += bit_length + byte_length * 8
            # Field
            elif is_field(item):
                length += item.bit_size
            else:
                raise TypeError(divmod(length, 8), item)
        return divmod(length, 8)

    @nested_option()
    def field_indexes(self, index=zero(), **options):
        """Returns a list which contains ``(name, index)`` tuples for each
        `Field` of a `Sequence`.

        :param index: optional start :class:`Index` of the `Sequence`.

        :keyword bool nested: if `True` all `Pointer` fields of a `Sequence`
            lists their *nested* `data` object fields as well.
        """
        indexes = list()
        for idx, item in enumerate(self):
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
                raise TypeError(index, idx, item)
        return indexes

    @nested_option()
    def field_types(self, **options):
        """Returns a list which contains ``(name, type)`` tuples for each
        `Field` of a `Sequence`.

        :keyword bool nested: if `True` all `Pointer` fields of a `Sequence`
            lists their *nested* `data` object fields as well.
        """
        types = list()
        for idx, item in enumerate(self):
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
                raise TypeError(idx, item)
            return types

    @nested_option()
    def field_values(self, **options):
        """Returns a list which contains ``(name, value)`` tuples for each
        `Field` of a `Sequence`.

        :keyword bool nested: if `True` all `Pointer` fields of a `Sequence`
            lists their *nested* `data` object as well.
        """
        values = list()
        for idx, item in enumerate(self):
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
                raise TypeError(idx, item)
        return values

    @nested_option()
    def field_items(self, root=str(), **options):
        """Returns a flat list which contains tuples in the form of
        ``(path, field)`` for each `Field` of a `Sequence`.

        :param str root: root path.

        :keyword bool nested: if `True` the `Fields` of the *nested* `data`
            objects of all `Pointer` fields in a `Sequence` are added to
            the list.
        """
        base = root if root else str()

        items = list()
        for idx, item in enumerate(self):
            path = "{0}[{1}]".format(base, str(idx)) if base else ".[{0}]".format(str(idx))
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
                raise TypeError(path, item)
        return items

    @nested_option(True)
    def blueprint(self, name=str(), **options):
        """Returns the blue print of a `Sequence` as an ordered dictionary
        including the blue prints of the nested fields.

        .. code-block:: python

            blueprint = {
                'class': self.__class__.__name__,
                'name': name if name else self.__class__.__name__,
                'size': len(self),
                'type': Sequence.item_type.name
                'member': [
                    field.blueprint('name[idx]') for idx, field in enumerate(self)
                ]
            }

        :param str name: optional name for the `Sequence`.

        :keyword bool nested: if `True` all `Pointer` fields of the `Sequence`
            lists their *nested* `data` object fields as well.
        """
        members = list()
        obj = OrderedDict()
        obj['class'] = self.__class__.__name__
        obj['name'] = name if name else self.__class__.__name__
        obj['size'] = len(self)
        obj['type'] = Sequence.item_type.name
        obj['member'] = members

        for idx, item in enumerate(self):
            if is_any(item):
                members.append(item.blueprint("{0}[{1}]".
                                              format(obj['name'], idx),
                                              **options))
            else:
                raise TypeError(idx, item)
        return obj


class Array(Sequence):
    """A `Array` is a :class:`Sequence` which contains *elements* of one type.
    The *template* for the `Array` element can be any `Field` instance or a
    callable which returns a `Structure`, `Sequence`, `Array` or any `Field`
    instance.

    The constructor method is necessary to ensure that the internal constructor
    for the `Array` element produces complete copies for each `Array` element
    including the *nested* objects in the *template* for the `Array` element.

    A `Array` of `Pointer` should use a constructor method instead of assigning
    a `Pointer` instance directly as the `Array` element *template* to ensure
    that the *nested* `data` object of a `Pointer` is also complete copied for
    each `Array` element.

    A `Array` adapts and extends a `Sequence` with the following features:

    *   **Append** a new `Array` element to a `Array`
        via :meth:`append()`.
    *   **Insert** a new `Array` element before the *index* into a `Array`
        via :meth:`insert()`.
    *   **Re-size** a `Array`
        via :meth:`resize()`.

    :param template: template for the `Array` element.
        The *template* can be any `Field` instance or any *callable* that
        returns a `Structure`, `Sequence`, `Array` or any `Field` instance.

    :param int size: size of the `Array` in number of `Array` elements.
    """
    item_type = ItemClass.Array

    def __init__(self, template, size=0):
        super().__init__()

        # Template for the array elements.
        if is_field(template):
            self._template = template
        elif callable(template) and is_any(template()):
            self._template = template
        else:
            raise TypeError(template)

        # Create array
        self.resize(size)

    def __create__(self):
        if isinstance(self._template, Field):
            return copy.copy(self._template)
        else:
            return self._template()

    def append(self):
        """Appends a new `Array` element to the `Array`."""
        super().append(self.__create__())

    def insert(self, index):
        """Inserts a new `Array` element before the *index* of the `Array`.

        :param int index: `Array` index.
        """
        super().insert(index, self.__create__())

    def resize(self, size):
        """Re-sizes the `Array` by appending new `Array` elements or
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


class Field(metaclass=abc.ABCMeta):
    """The abstract `Field` class is the meta class for all field classes.

    A `Field` class

    :param int bit_size: is the *size* of the `Field` in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the `Field` to the number of bytes,
        can be between *1* and *8*.

    :param byte_order: coding :class:`Byteorder` of the `Field`.
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
        """Field alignment as a tuple in the form of
        ``(aligns to bytes, bit offset within the aligned bytes)``
        """
        return self._align_to_byte_size, self._align_to_bit_offset

    @property
    def bit_size(self):
        """Field size in bits."""
        return self._bit_size

    @property
    def byte_order(self):
        """Field coding :class:`Byteorder`."""
        return self._byte_order

    @byte_order.setter
    def byte_order(self, value):
        if not isinstance(value, Byteorder):
            raise TypeError(value)
        self._byte_order = value

    @property
    def index(self):
        """Field :class:`Index`."""
        return self._index

    @index.setter
    def index(self, value):
        byte, bit, address, base, update = value
        if byte < 0 or bit < 0 or bit > 64:
            raise ValueError(value)
        size, offset = self.alignment
        length, remainder = divmod(self.bit_size + bit, 8)
        if remainder:
            length += 1
        if length > size:
            raise ValueError(value)
        if self.is_bit():
            if offset != bit:
                raise ValueError(value)
        else:
            self._align_to_bit_offset = bit
        if address < 0:
            raise ValueError(value)
        self._index = Index(int(byte), int(bit), int(address), int(base), update)

    @property
    def name(self):
        """Field type."""
        return self.item_type.name.capitalize() + str(self.bit_size)

    @property
    def value(self):
        """Field value."""
        return self._value

    @value.setter
    def value(self, x):
        self._value = x

    @staticmethod
    def is_bit():
        """Returns `False`."""
        return False

    @staticmethod
    def is_bool():
        """Returns `False`."""
        return False

    @staticmethod
    def is_decimal():
        """Returns `False`."""
        return False

    @staticmethod
    def is_float():
        """Returns `False`."""
        return False

    @staticmethod
    def is_pointer():
        """Returns `False`."""
        return False

    @staticmethod
    def is_stream():
        """Returns `False`."""
        return False

    @staticmethod
    def is_string():
        """Returns `False`."""
        return False

    @byte_order_option()
    def unpack(self, buffer=bytes(), index=zero(), **options):
        """Unpacks the bytes and bits from a *buffer* starting at the given
        *index* by mapping the bytes and bits to the `Field` value in
        accordance with the decoding `Byteorder` of the *buffer* and the
        `Field`.

        A specific coding byte order of a `Field` overrules the decoding
        byte order of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the `Field`.

        :keyword byte_order: decoding :class:`Byteorder` of the *buffer*.

        .. note::

           This is method must be overwritten by a derived class.
        """
        return index

    @byte_order_option()
    def pack(self, buffer=bytearray(), **options):
        """Packs the bytes and bits for a *buffer* starting at the *index*
        of the `Field` by mapping the value of the `Field` to bytes in
        accordance with the encoding `Byteorder` of the *buffer* and the
        `Field`.

        A specific coding byte order of a `Field` overrules the encoding
        byte order of the *buffer*.

        Returns the encoded bytes for its field value.

        :keyword byte_order: encoding :class:`Byteorder` of the *buffer*.

        .. note::

           This method must be overwritten by a derived class.
        """
        return bytes()

    @byte_order_option()
    @nested_option()
    def decode(self, buffer=bytes(), index=zero(), **options):
        """Decodes sequential bytes from a *buffer* starting at the begin
        of the *buffer* or with a given *index* by mapping the bytes to the
        value of the `Field` in accordance with the decoding `Byteorder` of
        the *buffer* and the `Field`.

        A specific coding byte order of a `Field` overrules the decoding
        byte order of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the `Field`.

        Optional the decoding of the *nested* `data` object of a `Pointer`
        field can be enabled.

        :keyword byte_order: decoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` a :class:`Pointer` field decodes its
            *nested* `data` object fields as well.
            A `Pointer` field uses for the decoding of the *nested* `data`
            object its own `bytestream`
        """
        self.index = index
        self._value = self.unpack(buffer, index, **options)
        return self.next_index(index)

    @byte_order_option()
    @nested_option()
    def encode(self, buffer=bytearray(), index=zero(), **options):
        """Encodes sequential bytes to a *buffer* starting at the begin of
        the *buffer* or with a given *index* by mapping the value of the
        `Field` to the bytes in accordance with the encoding `Byteorder` of
        the *buffer* and the `Field`.

        A specific coding byte order of a `Field` overrules the encoding
        byte order of the *buffer*.

        Returns the :class:`Index` of the *buffer* after the `Field`.

        Optional the encoding of the *nested* `data` object of a `Pointer`
        field can be enabled.

        :keyword byte_order: encoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` a :class:`Pointer` field encodes its
            *nested* `data` object fields as well.
            A `Pointer` field uses for the encoding of the *nested* `data`
            object its own `bytestream`
        """
        self.index = index
        buffer += self.pack(buffer, **options)
        return self.next_index(index)

    def next_index(self, index=zero()):
        """Returns the `Index` after the `Field`.

        :param index: start :class:`Index` for the `Field`.
        """
        self.index = index
        byte, bit, address, base, update = index
        bit += self.bit_size
        byte_length, bit_length = divmod(bit, 8)
        if byte_length == self._align_to_byte_size:
            if bit_length is 0:
                byte += self._align_to_byte_size
                bit = 0
                address += self._align_to_byte_size
            else:
                raise IndexError(index, byte_length, bit_length)
        return Index(byte, bit, address, base, update)

    @nested_option(True)
    def blueprint(self, name=str(), **options):
        """Returns the blue print of a `Field` as an ordered dictionary.

        .. code-block:: python

            blueprint = {
                'address': self.index.address,
                'alignment': [self.alignment[0], self.alignment[1]],
                'class': self.name,
                'index': [self.index.byte, self.index.bit],
                'name': name if name else self.name,
                'order': self.byteorder.value,
                'size': self.bit_size,
                'type': 'field',
                'value': self.value
            }
        """
        obj = {
            'address': self.index.address,
            'alignment': [self.alignment[0], self.alignment[1]],
            'class': self.name,
            'order': self.byte_order.value,
            'index': [self.index.byte, self.index.bit],
            'name': name if name else self.name,
            'size': self.bit_size,
            'type': 'field',
            'value': self.value
        }
        return OrderedDict(sorted(obj.items()))


class Stream(Field):
    """A `Stream` field is a :class:`Field` with a variable *size* and
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

    :param int size: is the *size* of the field in bytes.

    Example:

    >>> from pprint import pprint
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
     'type': 'field',
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
        size = len(self)
        if size > 0:
            return self.item_type.name.capitalize() + str(size)
        else:
            return self.item_type.name.capitalize()

    @property
    def value(self):
        return hexlify(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_stream(x, encoding='hex')

    @staticmethod
    def is_stream():
        """Returns `True`."""
        return True

    def to_stream(self, value, encoding='hex'):
        if isinstance(value, str):
            if encoding == 'hex':
                bytestream = unhexlify(value)
            elif encoding == 'ascii':
                bytestream = value.encode('ascii')
            else:
                raise LookupError(encoding)
        elif isinstance(value, (bytearray, bytes)):
            bytestream = bytes(value)
        else:
            raise TypeError(value)
        bytestream = bytestream[:len(self)]
        bytestream += b'\x00' * max(len(self) - len(bytestream), 0)
        return bytestream

    @byte_order_option()
    def unpack(self, buffer=bytes(), index=zero(), **options):
        # Bad aligned field
        if index.bit:
            raise IndexError(index)

        offset = self.index.byte
        size = offset + len(self)
        return buffer[offset:size]

    @byte_order_option()
    def pack(self, buffer=bytearray(), **options):
        # Bad aligned field
        if self.index.bit:
            raise IndexError(self.index)

        return self._value

    def resize(self, size):
        """Re-sizes the `Stream` field by appending zero bytes or
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
    """A `String` field is a :class:`Stream` field with a variable *size* and
    returns its field *value* as a zero terminated ascii encoded string.

    A `String` field is:

    *   *containable*: ``item in self`` returns `True` if *item* is part
        of the `String` field.
    *   *sized*: ``len(self)`` returns the length of the `String` field.
    *   *subscriptable* ``self[index]`` returns the *byte* at the *index*
        of the `String` field.
    *   *iterable* ``iter(self)`` iterates over the bytes of the `String`
        field.

    Example:

    >>> from pprint import pprint
    >>> string = String()
    >>> string.is_stream()
    True
    >>> string.is_string()
    True
    >>> string.name
    'String'
    >>> string.alignment
    (0, 0)
    >>> string.byte_order
    Byteorder.auto = 'auto'
    >>> string.index
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
    >>> chr(string[5])  # converts to int
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
     'type': 'field',
     'value': 'KonFoo is '}
    """
    item_type = ItemClass.String

    @property
    def value(self):
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
        """Returns `True`."""
        return True


class Float(Field):
    """A `Float` field is a :class:`Field` with a fix *size* of four bytes
    and returns its field *value* as a single float.

    Internally a `Float` field uses a :class:`float` class to store the
    data of its field *value*.

    A `Float` field extends the :meth:`blueprint` method with a ``max`` and
    ``min`` key for its maximum and minimum possible field value.

    Example:

    >>> from pprint import pprint
    >>> float = Float()
    >>> float.is_float()
    True
    >>> float.name
    'Float32'
    >>> float.alignment
    (4, 0)
    >>> float.byte_order
    Byteorder.auto = 'auto'
    >>> float.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> float.bit_size
    32
    >>> float.min()
    -3.4028234663852886e+38
    >>> float.max()
    3.4028234663852886e+38
    >>> float.smallest()
    1.1754943508222875e-38
    >>> float.epsilon()
    5.960464477539063e-08
    >>> float.value
    0.0
    >>> float.value = 0x10
    >>> float.value
    16.0
    >>> float.value = -3.4028234663852887e+38
    >>> float.value
    -3.4028234663852886e+38
    >>> float.value = 3.4028234663852887e+38
    >>> float.value
    3.4028234663852886e+38
    >>> pprint(float.blueprint())
    {'address': 0,
     'alignment': [4, 0],
     'class': 'Float32',
     'index': [0, 0],
     'max': 3.4028234663852886e+38,
     'min': -3.4028234663852886e+38,
     'name': 'Float32',
     'order': 'auto',
     'size': 32,
     'type': 'field',
     'value': 3.4028234663852886e+38}
    """
    item_type = ItemClass.Float

    def __init__(self):
        super().__init__()
        # Field alignment
        self._align_to_byte_size = 4
        # Field bit size
        self._bit_size = 32
        # Field value
        self._value = float()

    @property
    def value(self):
        return float(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_float(x)

    @staticmethod
    def is_float():
        """Returns `True`."""
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
        """Returns the maximal possible field value."""
        return (1 - Float.epsilon()) * 2 ** 128

    @staticmethod
    def min():
        """Returns the minimal possible field value."""
        return -(1 - Float.epsilon()) * 2 ** 128

    @byte_order_option()
    def unpack(self, buffer=bytes(), index=zero(), **options):
        # Bad aligned field
        if index.bit:
            raise IndexError(index)

        # A coding byte order of a field overrules
        # the coding byte order of a buffer
        byte_order = get_byte_order(options)
        if self.byte_order is not Byteorder.auto:
            byte_order = self.byte_order

        # No data enough bytes for the field in the bytestream
        offset = index.byte
        size = offset + self._align_to_byte_size
        bytestream = buffer[offset:size]
        if len(bytestream) != 4:
            return float()

        if byte_order is Byteorder.big:
            return struct.unpack('>f', bytestream)[0]
        else:
            return struct.unpack('<f', bytestream)[0]

    @byte_order_option()
    def pack(self, buffer=bytearray(), **options):
        # Bad aligned field
        if self.index.bit:
            raise IndexError(self.index)

        # A coding byte order of a field overrules
        # the coding byte order of a buffer
        byte_order = get_byte_order(options)
        if self.byte_order is not Byteorder.auto:
            byte_order = self.byte_order

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
    """A `Decimal` field is a :class:`Field` with a variable *size*
    and returns its field value as a integer number.

    Internally a `Decimal` field uses a :class:`int` class to store the
    data of its field *value*.

    A `Decimal` field extends its :meth:`blueprint` method with a ``max`` and
    ``min`` key for its maximum and minimum possible field value.

    :param int bit_size: is the *size* of the field in bits,
        can be between *1* and *64*.

    :param int align_to: aligns the field to the number of bytes,
        can be between *1* and *8*. If no field *alignment* is set the a
        `Decimal` field aligns itself to the next matching byte size
        corresponding to the field *size*.

    :param bool signed: if `True` the decimal number is signed otherwise unsigned.

    Example:

    >>> from pprint import pprint
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
    >>> unsigned.decode(unhexlify('0080'))
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
     'type': 'field',
     'value': 65535}

    Example:

    >>> from pprint import pprint
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
    >>> signed.decode(unhexlify('00c0'))
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
     'type': 'field',
     'value': 32767}
    """
    item_type = ItemClass.Decimal

    def __init__(self, bit_size, align_to=None, signed=False):
        super().__init__()
        # Field signed?
        self._signed = bool(signed)
        # Field alignment and field bit size
        if align_to:
            self._set_alignment(byte_size=align_to)
            self._set_bit_size(bit_size)
        else:
            self._set_bit_size(bit_size, auto_align=True)
        # Field value
        self._value = int()

    @property
    def value(self):
        return int(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)

    @property
    def signed(self):
        """Field signed."""
        return self._signed

    @signed.setter
    def signed(self, value):
        self._signed = bool(value)

    @staticmethod
    def is_decimal():
        """Returns `True`."""
        return True

    def to_decimal(self, value, encoding=None):
        if isinstance(value, str):
            if encoding is None:
                decimal = int(value, 0)
            elif encoding == 'ascii':
                decimal = ord(value[:1])
            else:
                raise LookupError(encoding)
        else:
            decimal = int(value)
        return limiter(decimal, self.min(), self.max())

    def _set_alignment(self, byte_size, bit_offset=0, auto_align=False):
        bit = int(bit_offset)
        # Auto alignment? -> align to field size
        if auto_align:
            byte, remainder = divmod(bit, 8)
            if remainder is not 0:
                byte += 1
            byte = max(byte, 1)
        # No auto alignment
        else:
            byte = int(byte_size)

        # Not allowed alignment size?
        if byte not in (1, 2, 3, 4, 5, 6, 7, 8):
            raise OutOfRange(self, byte)

        # Field size is out of range?
        if bit < 0 or bit > 63:
            raise OutOfRange(self, bit)

        # Bad aligned field?
        if bit >= byte * 8:
            raise BadAligned(self, byte, bit)

        # Set field alignment
        self._align_to_byte_size = byte
        self._align_to_bit_offset = bit

    def _set_bit_size(self, size, step=1, auto_align=False):
        bit_size = int(size)
        # Field size is not a multiple of step?
        if bit_size % step != 0:
            raise InvalidSize(self, bit_size, step)

        # Field size is out of range?
        if bit_size < 1 or bit_size > 64:
            raise OutOfRange(self, bit_size)

        byte_size, bit_offset = divmod(bit_size, 8)
        # Auto alignment? -> align to field size
        if auto_align:
            if bit_offset is not 0:
                self._align_to_byte_size = byte_size + 1
            else:
                self._align_to_byte_size = byte_size
        # Bad aligned?
        elif byte_size > self._align_to_byte_size:
            raise BadAligned(self, self._align_to_byte_size, byte_size)
        # Set field size
        self._bit_size = bit_size

    def bit_mask(self):
        return 2 ** self._bit_size - 1

    def max(self):
        """Returns the maximal possible field value."""
        if self._signed:
            return 2 ** (self._bit_size - 1) - 1
        else:
            return 2 ** self._bit_size - 1

    def min(self):
        """Returns the minimal possible field value."""
        if self._signed:
            return -2 ** (self._bit_size - 1)
        else:
            return 0

    @byte_order_option()
    def unpack(self, buffer=bytes(), index=zero(), **options):
        offset = index.byte
        size = offset + self._align_to_byte_size
        bytestream = buffer[offset:size]

        byte_order = get_byte_order(options)

        value = int.from_bytes(bytestream, byte_order.value)
        value >>= index.bit
        value &= self.bit_mask()

        byte, bit = divmod(self.bit_size, 8)

        if self.byte_order is Byteorder.auto:
            # No specific field byte order
            pass
        elif self.byte_order is byte_order:
            # Field byte order matches the
            # decoding byte order of the buffer
            pass
        elif byte < 1:
            # Byte order not relevant for one byte
            pass
        elif bit != 0:
            # Bad aligned field
            raise BadAligned(self, byte, bit)
        elif byte == 1:
            # Byte order not relevant for field's with one byte
            pass
        else:
            value = int.from_bytes(value.to_bytes(byte, byte_order.value),
                                   self.byte_order.value)

        if value > self.max():
            value |= ~self.bit_mask()
        return value

    @byte_order_option()
    def pack(self, buffer=bytearray(), **options):
        byte_order = get_byte_order(options)

        value = limiter(self._value, self.min(), self.max())
        value &= self.bit_mask()
        byte, bit = divmod(self.bit_size, 8)

        if self.byte_order is Byteorder.auto:
            pass
        elif self.byte_order is byte_order:
            pass
        elif byte < 1:
            pass
        elif bit != 0:
            raise BadAligned(self, byte, bit)
        elif byte == 1:
            pass
        else:
            # Create value by taking care of the different byte order's
            value = int.from_bytes(value.to_bytes(byte, self.byte_order.value),
                                   byte_order.value)

        # Shift value to bit offset
        value <<= self.index.bit

        offset = self.index.byte
        size = offset + self._align_to_byte_size
        # Mapping field value into aligned bytes of the buffer
        if len(buffer) == size:
            view = memoryview(buffer)
            value |= int.from_bytes(buffer[offset:size], byte_order.value)
            view[offset:size] = value.to_bytes(self._align_to_byte_size, byte_order.value)
            return bytes()
        # Extend field value with the aligned bytes
        else:
            return value.to_bytes(self._align_to_byte_size, byte_order.value)

    def blueprint(self, name=None, **options):
        obj = super().blueprint(name, **options)
        obj['max'] = self.max()
        obj['min'] = self.min()
        obj['signed'] = self.signed
        return OrderedDict(sorted(obj.items()))


class Bit(Decimal):
    """A `Bit` field is an unsigned :class:`Decimal` with a *size* of
    one bit and returns its field *value* as an unsigned integer number.

    :param int number: is the bit offset of the field within the aligned
        bytes, can be between *0* and *63*.

    Example:

    >>> from pprint import pprint
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
    >>> bit.signed
    False
    >>> bit.value
    0
    >>> bit.decode(unhexlify('01'))
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
     'type': 'field',
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
        return self.item_type.name.capitalize()

    @staticmethod
    def is_bit():
        """Returns `True`."""
        return True


class Byte(Decimal):
    """A `Byte` field is an unsigned :class:`Decimal` field with a *size* of
    one byte and returns its field *value* as a hexadecimal encoded string.

    Example:

    >>> from pprint import pprint
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
    >>> byte.decode(unhexlify('20'))
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
     'type': 'field',
     'value': '0xff'}
    """
    item_type = ItemClass.Byte

    def __init__(self, align_to=None):
        super().__init__(bit_size=8, align_to=align_to)

    @property
    def name(self):
        return self.item_type.name.capitalize()

    @property
    def value(self):
        return hex(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)


class Char(Decimal):
    """A `Char` field is an unsigned :class:`Decimal` field with a *size* of
    one byte and returns its field *value* as a unicode encoded string.

    Example:

    >>> from pprint import pprint
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
    >>> char.decode(unhexlify('41'))
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
     'type': 'field',
     'value': 'F'}
    """
    item_type = ItemClass.Char

    def __init__(self, align_to=None):
        super().__init__(bit_size=8, align_to=align_to)

    @property
    def name(self):
        return self.item_type.name.capitalize()

    @property
    def value(self):
        return chr(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x, encoding='ascii')


class Signed(Decimal):
    """A `Signed` field is a signed :class:`Decimal` field with a variable
    *size* and returns its field *value* as a signed integer number.

    Example:

    >>> from pprint import pprint
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
    >>> signed.decode(unhexlify('00c0'))
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
     'type': 'field',
     'value': 32767}
    """
    item_type = ItemClass.Signed

    def __init__(self, bit_size, align_to=None):
        super().__init__(bit_size, align_to, signed=True)


class Unsigned(Decimal):
    """A `Unsigned` field is an unsigned :class:`Decimal` field with a
    variable *size* and returns its field *value* as a hexadecimal encoded
    string.

    Example:

    >>> from pprint import pprint
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
    >>> unsigned.decode(unhexlify('00c0'))
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
     'type': 'field',
     'value': '0xffff'}
    """
    item_type = ItemClass.Unsigned

    def __init__(self, bit_size, align_to=None):
        super().__init__(bit_size, align_to)

    @property
    def value(self):
        return hex(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)


class Bitset(Decimal):
    """A `Bitset` field is an unsigned :class:`Decimal` field with a variable
    *size* and returns its field *value* as a binary encoded string.

    :param byte_order: coding :class:`Byteorder` of a `Bitset` field.

    Example:

    >>> from pprint import pprint
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
    >>> bitset.decode(unhexlify('f00f'))
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
     'type': 'field',
     'value': '0b1111111111111111'}
    """
    item_type = ItemClass.Bitset

    def __init__(self, bit_size, align_to=None, byte_order=Byteorder.auto):
        super().__init__(bit_size, align_to)
        # Field byte order
        self.byte_order = byte_order

    @property
    def value(self):
        return '{0:#0{1}b}'.format(self._value, self.bit_size + 2)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)


class Bool(Decimal):
    """A `Bool` field is an unsigned :class:`Decimal` field with a variable
    *size* and returns its field *value* as a boolean.

    Example:

    >>> from pprint import pprint
    >>> bool = Bool(16)
    >>> bool.is_decimal()
    True
    >>> bool.is_bool()
    True
    >>> bool.name
    'Bool16'
    >>> bool.alignment
    (2, 0)
    >>> bool.byte_order
    Byteorder.auto = 'auto'
    >>> bool.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> bool.bit_size
    16
    >>> bool.min()
    0
    >>> bool.max()
    65535
    >>> bool.signed
    False
    >>> bool.value
    False
    >>> bool.decode(unhexlify('0f00'))
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bool.value
    True
    >>> bool.value = False
    >>> bool.value
    False
    >>> bool.value = -1
    >>> bool.value
    False
    >>> bool.value = 0x10000
    >>> bool.value
    True
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> bool.encode(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> hexlify(bytestream)
    b'ffff'
    >>> pprint(bool.blueprint())
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
     'type': 'field',
     'value': True}
    """
    item_type = ItemClass.Bool

    def __init__(self, bit_size, align_to=None):
        super().__init__(bit_size, align_to)

    @property
    def value(self):
        return bool(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)

    @staticmethod
    def is_bool():
        """Returns `True`."""
        return True


class Enum(Decimal):
    """A `Enum` field is an unsigned :class:`Decimal` field with a variable
    *size* and returns its field *value* as a integer number.

    If an *enumeration* is available and a member matches the integer number
    then the member name string is returned otherwise the integer number is
    returned.

    :param enumeration: :class:`Enumeration` definition of the field.

    Example:

    >>> from pprint import pprint
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
    >>> enum.decode(unhexlify('2800'))
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
     'type': 'field',
     'value': 65535}
    """
    item_type = ItemClass.Enum

    def __init__(self, bit_size, align_to=None, enumeration=None):
        super().__init__(bit_size, align_to)
        # Field enumeration class
        if enumeration is None:
            self._enum = None
        elif issubclass(enumeration, Enumeration):
            self._enum = enumeration
        else:
            raise TypeError(enumeration)

    @property
    def value(self):
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
                        raise ValueError(x)
                else:
                    raise ValueError(x)
        else:
            decimal = x
        self._value = self.to_decimal(decimal)


class Scaled(Decimal):
    """A `Scaled` field is a signed :class:`Decimal` field with a variable
    *size* and returns its scaled field *value* as a float.

    The scaled field *value* is:
        ``(unscaled field value / scaling base) * scaling factor``

    The unscaled field *value* is:
        ``(scaled field value / scaling factor) * scaling base``

    The scaling base is:
        ``2 ** (field size - 1) / 2``

    A `Scaled` field extends the :meth:`blueprint` method with a ``scale`` key
    for its scaling factor.

    :param float scale: scaling factor of the field.

    Example:

    >>> from pprint import pprint
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
    >>> scaled.decode(unhexlify('0040'))
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
     'type': 'field',
     'value': 199.993896484375}
    """
    item_type = ItemClass.Scaled

    def __init__(self, scale, bit_size, align_to=None):
        super().__init__(bit_size, align_to, signed=True)
        # Field scaling factor
        self._scale = float(scale)

    @property
    def value(self):
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
        """Field scaling factor."""
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = float(value)

    def scaling_base(self):
        """Field scaling base."""
        return 2 ** (self.bit_size - 1) / 2

    def blueprint(self, name=None, **options):
        obj = super().blueprint(name, **options)
        obj['scale'] = self.scale
        return OrderedDict(sorted(obj.items()))


class Fraction(Decimal):
    """A `Fraction` field is an unsigned :class:`Decimal` field with a
    variable *size* and returns its fractional field *value* as a float.

    A fractional number is bitwise encoded and has up to three bit
    parts for this task.

    The first part are the bits for the fraction part of a fractional number.
    The number of bits for the fraction part is derived from the *bit size*
    of the field and the required bits for the other two parts.
    The fraction part is always smaller than one.

    The second part are the *bits* for the *integer* part of a fractional
    number.

    The third part is the bit for the sign of a *signed* fractional
    number. Only a *signed* fractional number posses this bit.

    A fractional number is multiplied by hundred.

    :param int bits_integer: number of bits for the integer part of the
        fraction number, can be between *1* and the field *size*.

    :param bool signed: if `True` the fraction number is signed otherwise
        unsigned.

    Example:

    >>> from pprint import pprint
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
    >>> unipolar.decode(unhexlify('0080'))
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
     'type': 'field',
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
    >>> bipolar.decode(unhexlify('0040'))
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
     'type': 'field',
     'value': 199.993896484375}
    """
    item_type = ItemClass.Fraction

    def __init__(self, bits_integer, bit_size, align_to=None, signed=False):
        super().__init__(bit_size, align_to)
        # Number of bits of the integer part of the fraction number
        self._bits_integer = limiter(int(bits_integer), 1, self._bit_size)
        # Fraction number signed?
        if self._bit_size <= 1:
            self._signed_fraction = False
        else:
            self._signed_fraction = bool(signed)

    @property
    def name(self):
        return self.item_type.name.capitalize() + str(self._bits_integer) + '.' + str(self.bit_size)

    @property
    def value(self):
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
            decimal = limiter(integer | fraction,
                              0, 2 ** (self.bit_size - 1) - 1)
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
    """A `Bipolar` field is a signed :class:`Fraction` field with a variable
    *size* and returns its fractional field value as a float.

    Example:

    >>> from pprint import pprint
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
     'type': 'field',
     'value': 199.993896484375}
    """
    item_type = ItemClass.Bipolar

    def __init__(self, bits_integer, bit_size, align_to=None):
        super().__init__(bits_integer, bit_size, align_to, True)


class Unipolar(Fraction):
    """A `Unipolar` field is an unsigned :class:`Fraction` field with a variable
    *size* and returns its fractional field *value* as a float.

    Example:

    >>> from pprint import pprint
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
    >>> unipolar.decode(unhexlify('0080'))
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
     'type': 'field',
     'value': 399.993896484375}
    """
    item_type = ItemClass.Unipolar

    def __init__(self, bits_integer, bit_size, align_to=None):
        super().__init__(bits_integer, bit_size, align_to, False)


class Datetime(Decimal):
    """A `Datetime` field is an unsigned :class:`Decimal` field with a fix
    *size* of four bytes and returns its field *value* as a UTC datetime
    encoded string in the format *YYYY-mm-dd HH:MM:SS*.

    Example:

    >>> from pprint import pprint
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
    >>> datetime.decode(unhexlify('ffffffff'))
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
     'type': 'field',
     'value': '2106-02-07 06:28:15'}
    """
    item_type = ItemClass.Datetime

    def __init__(self):
        super().__init__(bit_size=32)

    @property
    def value(self):
        return str(datetime.datetime.utcfromtimestamp(self._value))

    @value.setter
    def value(self, x):
        self._value = self.to_timestamp(x)

    def to_timestamp(self, value):
        decimal = calendar.timegm(time.strptime(value, "%Y-%m-%d %H:%M:%S"))
        return self.to_decimal(decimal)


class Pointer(Decimal, Container):
    """A `Pointer` field is an unsigned :class:`Decimal` field with a *size* of
    four bytes and returns its field *value* as a hexadecimal encoded string.

    A `Pointer` field refers absolutely to a `data` object of a data `Provider`.

    The `Pointer` class extends the :class:`Decimal` field with the
    :class:`Container` class for its nested *data object*.

    A `Pointer` provides additional features:

    *   **Read** from a `Provider` the necessary amount of bytes for
        the nested `data` object of the `Pointer` via :meth:`read()`.
    *   Get the **next index** after the last *field* of a `Structure`
        via :meth:`next_index()`.
    *   View the **index** for each *field* in a `Structure`
        via :meth:`field_indexes()`.
    *   View the **type** for each *field* in a `Structure`
        via :meth:`field_types()`.
    *   View the **value** for each *field* in a `Structure`
        via :meth:`field_values()`.
    *   List the **item** and its path for each *field* in a `Structure`
        as a flat list via :meth:`field_items()`.
    *   Get a **blueprint** of a `Structure` and its items
        via :meth:`blueprint()`,

    :param template: template for the `data` object referenced by the pointer.

    :param int address: absolute address of the `data` object referenced by
        the pointer.

    :param byte_order: coding :class:`Byteorder` of the `data` object
        referenced by the pointer.

    Example:

    >>> from pprint import pprint
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
    >>> pointer.bit_size
    32
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.signed
    False
    >>> pointer.address
    0
    >>> pointer.base_address
    0
    >>> pointer.data
    >>> pointer.size
    0
    >>> pointer.order
    Byteorder.little = 'little'
    >>> pointer.value
    '0x0'
    >>> pointer.decode(unhexlify('00c0'))
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
     'type': 'pointer',
     'value': '0xffffffff'}
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
        """`Data` objects absolute address."""
        return self._value

    @property
    def base_address(self):
        """Data `Provider` base address."""
        return self._value

    @property
    def bytestream(self):
        """`Data` objects bytestream."""
        return hexlify(self._data_stream)

    @bytestream.setter
    def bytestream(self, value):
        if isinstance(value, str):
            self._data_stream = unhexlify(value)
        elif isinstance(value, (bytearray, bytes)):
            self._data_stream = bytes(value)
        else:
            raise TypeError(value)

    @property
    def data(self):
        """`Data` object referenced by the pointer."""
        return self._data

    @data.setter
    def data(self, value):
        if value is None:
            self._data = None
        elif isinstance(value, (Sequence, Structure, Field)):
            self._data = value
        else:
            raise TypeError(value)

    @property
    def order(self):
        """`Data` objects coding :class:`Byteorder`."""
        return self._data_byte_order

    @order.setter
    def order(self, value):
        if not isinstance(value, Byteorder):
            raise TypeError(value)
        if value.value not in (Byteorder.big.value, Byteorder.little.value):
            raise ValueError(value.value)
        self._data_byte_order = value

    @property
    def size(self):
        """`Data` objects size in bytes."""
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
        """Field value."""
        return hex(self._value)

    @value.setter
    def value(self, x):
        self._value = self.to_decimal(x)

    @staticmethod
    def is_pointer():
        """Returns `True`."""
        return True

    def refresh(self):
        """Refresh the `Fields` of the `data` object with the internal `bytestream`
        and returns the `Index` of the `bytestream` after the last `Field` of the
        `data` object.
        """
        return self._data.decode(self._data_stream,
                                 Index(0, 0, self.address, self.base_address, False),
                                 nested=False,
                                 byte_order=self.order)

    def as_bytestream(self):
        buffer = bytearray()
        if self._data:
            self._data.encode(buffer,
                              Index(0, 0, self.address, self.base_address, False),
                              byte_order=self.order)
        return buffer

    @nested_option(True)
    def read(self, provider, null_allowed=False, **options):
        """Reads from the data *provider* the necessary amount of bytes for
        the nested `data` object of a `Pointer` field.

        A `Pointer` field has its own `bytestream` to store the binary data
        from the data *provider*.

        :param provider: data :class:`Provider`.

        :param bool null_allowed: if `True` read access of address zero (null)
            is allowed.

        :keyword bool nested: if `True` all `Pointer` fields of the `data`
            object of a `Pointer` reads their *nested* `data` object fields.
            A `Pointer` field stores the bytes for the *nested* `data`
            object in its own `bytestream`.
        """
        if self._data is not None:
            if is_provider(provider):
                if self._value < 0:
                    pass
                elif null_allowed or self._value > 0:
                    update = True
                    while update:
                        self.bytestream = provider.read(self.address, self.size)
                        index = self.refresh()
                        if index.bit != 0:
                            raise IndexError(index)
                        update = index.update
                    if is_mixin(self._data) and get_nested(options):
                        self._data.read(provider, False, **options)
                else:
                    self._data_stream = bytes()
                    self.refresh()
            else:
                raise TypeError(provider)

    def patch(self, item, byte_order=BYTEORDER):
        """Returns a memory :class:`Patch` for the values of the referenced
        *item*.

        :param item: item to patch.

        :keyword byte_order: encoding :class:`Byteorder` for the item.
        """
        # Re-index the data object
        self.subscript()

        # Container?
        if is_container(item):
            byte_length, bits = item.field_length()
            # Bad aligned container
            if bits != 0:
                raise BadAligned(byte_length, bits)

            # Empty container?
            field = item.first_field()
            if field is None:
                return None

            # Bad aligned field
            index = field.index
            if index.bit != 0:
                raise BadAligned(index)

            # Create a dummy byte array filled with zero bytes.
            # The dummy byte array is necessary because the length of
            # the *buffer* must correlate to the field indexes of the
            # appending fields.
            buffer = bytearray(b'q\x00' * index.byte)

            # Append field values of the container to the byte array
            item.encode(buffer, index, byte_order=byte_order)

            # Get container byte stream filled with the field values
            buffer = buffer[index.byte:]

            # Not correct filled container byte stream!
            if len(buffer) != byte_length:
                raise BufferError(len(buffer), byte_length)

            return Patch(buffer, index.address, byte_order, byte_length * 8, 0, False)
        # Field?
        elif is_field(item):
            byte_length, bit_offset = item.alignment
            index = item.index
            # Bad aligned field?
            if index.bit != bit_offset:
                raise BadAligned(index)

            # Create a dummy byte array filled with zero bytes.
            # The dummy byte array is necessary because the length of
            # the *buffer* must correlate to the field index of the
            # appending field.
            buffer = bytearray(b'\x00' * index.byte)

            # Append field value of the field to the byte array
            item.encode(buffer, index, byte_order=byte_order)

            # Get field byte stream filled with the field value
            buffer = buffer[index.byte:]

            # Not correct filled field byte stream!
            if len(buffer) != byte_length:
                raise BufferError(len(buffer), byte_length)

            byte_size, bits = divmod(item.bit_size, 8)
            if bits != 0:
                inject = True
                byte_size += 1
            else:
                inject = False

            byte_offset, bit_offset = divmod(bit_offset, 8)
            if bit_offset != 0:
                inject = True

            if byte_order is Byteorder.big:
                buffer = buffer[byte_length - byte_offset - byte_size:byte_length - byte_offset]
                address = index.address + byte_length - byte_offset - byte_size
            else:
                buffer = buffer[byte_offset:byte_offset + byte_size]
                address = index.address + byte_offset

            return Patch(buffer, address, byte_order, item.bit_size, bit_offset, inject)
        else:
            raise TypeError(item)

    def write(self, provider, item, byte_order=BYTEORDER):
        """Writes the values of the referenced *item* to a data *provider*.

        :param provider: data :class:`Provider`.

        :param item: item to write.

        :param byte_order: encoding :class:`Byteorder`.
        """
        patch = self.patch(item, byte_order)

        if patch is None:
            return patch

        if isinstance(provider, Provider):
            if patch.inject:
                stream = provider.read(patch.address, len(patch.buffer))

                value = int.from_bytes(stream, byte_order.value)

                bit_mask = ~((2 ** patch.bit_size - 1) << patch.bit_offset)
                bit_mask &= (2 ** (len(patch.buffer) * 8) - 1)
                value &= bit_mask
                value |= int.from_bytes(patch.buffer, byte_order.value)

                stream = value.to_bytes(len(patch.buffer), byte_order.value)

                provider.write(stream, patch.address, len(stream))
            else:
                provider.write(patch.buffer, patch.address, len(patch.buffer))
        else:
            raise TypeError(provider)

    @byte_order_option()
    @nested_option()
    def decode(self, buffer=bytes(), index=zero(), **options):
        """Decodes sequential the bytes from a *buffer* starting at the begin
        of the *buffer* or with a given *index* by mapping the bytes to the
        value of the `Pointer` by considering the decoding `Byteorder` of the
        *buffer* and the `Pointer`.

        Returns the :class:`Index` of the *buffer* after the `Pointer`.

        Optional the decoding of the *nested* `data` object of a `Pointer`
        field can be enabled.

        :keyword byte_order: decoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` a :class:`Pointer` field decodes its
            *nested* `data` object fields as well.
            A `Pointer` field uses for the decoding of the *nested* `data`
            object its own `bytestream`.
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
        """Encodes sequential the bytes to a *buffer* starting at the begin
        of the *buffer* or with a given *index* by mapping the value of the
        `Pointer` to the bytes by considering the encoding `Byteorder` of the
        *buffer* and the `Pointer`.

        Returns the :class:`Index` of the *buffer* after the `Pointer`.

        Optional the encoding of the *nested* `data` object of a `Pointer`
        field can be enabled.

        :keyword byte_order: encoding :class:`Byteorder` of the *buffer*.

        :keyword bool nested: if `True` a :class:`Pointer` field encodes its
            *nested* `data` object fields as well.
            A `Pointer` field uses for the encoding of the *nested* `data`
            object its own `bytestream`
        """
        # Field
        index = super().encode(buffer, index, **options)
        # Data Object
        if self._data and get_nested(options):
            options[Option.byteorder] = self.order
            self._data_stream = bytearray()
            self._data.encode(self._data_stream,
                              Index(0, 0, self.address, self.base_address, False),
                              **options)
            self._data_stream = bytes(self._data_stream)
        return index

    def subscript(self):
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

    @nested_option()
    def field_indexes(self, index=zero(), **options):
        """Returns a ordered dictionary with two keys.
        The ``['value']`` key contains the field *index* of the `Pointer` and
        the ``['data']`` key contains the field *indexes* of the `data` object
        of a `Pointer`.

        :keyword bool nested: if `True` all `Pointer` fields of the `data`
            object of a `Pointer` lists their *nested* `data` object fields
            as well.
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
            self._data.next_index(Index(0, 0, self.address, self.base_address, False))
            indexes['data'] = self._data.index
        else:
            indexes['data'] = Index(0, 0, self.address, self.base_address, False)
        return indexes

    @nested_option()
    def field_types(self, **options):
        """Returns a ordered dictionary with two keys.
        The ``['value']`` key contains the field *type* of the `Pointer` and
        the ``['data']`` key contains the field *types* of the `data` object
        of a `Pointer`.

        :keyword bool nested: if `True` all `Pointer` fields of the `data`
            object of a `Pointer` lists their *nested* `data` object fields
            as well.
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
        """Returns a ordered dictionary with two keys.
        The ``['value']`` key contains the field *value* of the `Pointer` and
        the ``['data']`` key contains the field *values* of the `data` object
        of a `Pointer`.

        :keyword bool nested: if `True` all `Pointer` fields of the `data`
            object of a `Pointer` lists their *nested* `data` object fields
            as well.
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
        """Returns a flat list which contains tuples in the form of
        ``(path, item)`` for each `Field` of a `Pointer`.

        :param str root: root path.

        :keyword bool nested: if `True` all `Pointer` fields of the `data`
            object of a `Pointer` lists their *nested* `data` object fields
            as well.

        :keyword bool nested: if `True` the `Fields` of the *nested* `data`
            objects of all `Pointer` fields in the *nested* `data` object
            of a `Pointer` are added to the list.
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
        """Returns the blue print of a `Pointer` as an ordered dictionary
        including the blue prints of the nested fields.

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
                'type': 'field',
                'value': self.value,
                'member': list(members)
            }

        :param str name: optional name for the `Pointer`.

        :keyword bool nested: if `True` all `Pointer` fields of a `Pointer`
            lists their *nested* `data` object fields as well.
        """
        obj = super().blueprint(name, **options)
        obj['class'] = self.__class__.__name__
        obj['name'] = name if name else self.__class__.__name__
        obj['type'] = 'pointer'
        if is_any(self._data):
            obj['member'] = list()
            obj['member'].append(self._data.blueprint(None, **options))
        return obj


class StructurePointer(Pointer):
    """A `StructurePointer` field is a :class:`Pointer` which refers
    to a :class:`Structure`.

    :param template: template for the `data` object.
        The *template* must be a `Structure` instance.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        if template is None:
            template = Structure()
        elif not isinstance(template, Structure):
            raise TypeError(template)
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
    """A `SequencePointer` field is a :class:`Pointer` which refers
    to a :class:`Sequence`.

    A `SequencePointer` is:

    *   *containable*: ``item in self`` returns `True` if *item* is part
        of the `Sequence`.
    *   *sized*: ``len(self)`` returns the number of items in the `Sequence`.
    *   *subscriptable* ``self[index]`` returns the *item* at the *index*
        of the `Sequence`.
    *   *iterable* ``iter(self)`` iterates over the *items* of the `Sequence`

    A `SequencePointer` supports the usual methods:

    *   **Append** a item to a `Sequence`
        via :meth:`append()`.
    *   **Insert** a item before the *index* into a `Sequence`
        via :meth:`insert()`.
    *   **Extend** a `Sequence` with items
        via :meth:`extend()`.
    *   **Clear** a `Sequence`
        via :meth:`clear()`.
    *   **Pop** a item with the *index* from a `Sequence`
        via :meth:`pop()`.
    *   **Remove**  the first occurrence of an *item* from a `Sequence`
        via :meth:`remove()`.
    *   **Reverse** all items in a `Sequence`
        via :meth:`reverse()`.

    :param iterable: any *iterable* that contains items of `Structure`,
        `Sequence`, `Array` or `Field` instances. If the *iterable* is one
        of these instances itself then the *iterable* itself is appended
        to the `Sequence`.
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
        """Appends the *item* to the end of the `Sequence`."""
        self._data.append(item)

    def insert(self, index, item):
        """Inserts the *item* before the *index* into the `Sequence`.

        :param int index: `Sequence` index.
        :param item:
        """
        self._data.insert(index, item)

    def pop(self, index=-1):
        """Removes and returns the item at the *index* from the `Sequence`."""
        return self._data.pop(index)

    def clear(self):
        """Remove all items from the `Sequence`."""
        self._data.clear()

    def remove(self, item):
        """Removes the first occurrence of an *item* from the `Sequence`."""
        self._data.remove(item)

    def reverse(self):
        """In place reversing of the `Sequence` items."""
        self._data.reverse()

    def extend(self, iterable):
        """Extends the `Sequence` by appending items from the *iterable*."""
        self._data.extend(iterable)


class ArrayPointer(SequencePointer):
    """A `ArrayPointer` field is a :class:`SequencePointer` which refers
    to a :class:`Array`.

    :param template: template for the `Array` element.
        The *template* can be any `Field` instance or any *callable* that
        returns a `Structure`, `Sequence`, `Array` or any `Field` instance.

    :param int size: is the size of the `Array` in number of `Array` elements.
    """

    def __init__(self, template, size=0, address=None, byte_order=BYTEORDER):
        super().__init__(address, byte_order=byte_order)
        self._data = Array(template, size)

    def append(self):
        """Appends a new `Array` element to the `Array`."""
        self._data.append()

    def insert(self, index):
        """Inserts a new `Array` element before the *index* of the `Array`.

        :param int index: `Array` index.
        """
        self._data.insert(index)

    def resize(self, size):
        """Re-sizes the `Array` by appending new `Array` elements or
        removing `Array` elements from the end.

        :param int size: new size of the `Array` in number of `Array`
            elements.
        """
        if isinstance(self._data, Array):
            self._data.resize(size)


class StreamPointer(Pointer):
    """A `StreamPointer` field is a :class:`Pointer` which refers
    to a :class:`Stream` field.

    A `StreamPointer` field is:

    *   *containable*: ``item in self`` returns `True` if *item* is part
        of the `Stream` field.
    *   *sized*: ``len(self)`` returns the length of the `Stream` field.
    *   *subscriptable* ``self[index]`` returns the *byte* at the *index*
        of the `Stream` field.
    *   *iterable* ``iter(self)`` iterates over the bytes of the `Stream`
        field.

    :param int size: is the size of the `Stream` field in bytes.
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
        """Re-sizes the `Stream` field by appending zero bytes or
        removing bytes from the end.

        :param int size: `Stream` size in number of bytes.
        """
        if isinstance(self._data, Stream):
            self._data.resize(size)


class StringPointer(StreamPointer):
    """A `StringPointer` field is a :class:`StreamPointer` which refers
    to a :class:`String` field.

    :param int size: is the *size* of the `String` field in bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size=0, address=address)
        self._data = String(size)


class RelativePointer(Pointer):
    """A `RelativePointer` field is a :class:`Pointer` field which refers to
    a `data` object relatively to a base address of a data `Provider`.

    :param template: template for the `data` object referenced by the
        pointer.

    :param address: relative address of the `data` object referenced
        by the pointer.

    :param byte_order: coding :class:`Byteorder` of the `data` object
        referenced by the pointer.
    """

    def __init__(self, template=None, address=None, byte_order=BYTEORDER):
        super().__init__(template=template,
                         address=address,
                         byte_order=byte_order)

    @property
    def address(self):
        """`Data` objects absolute address."""
        return self._value + self.base_address

    @property
    def base_address(self):
        """Data `Provider` base address."""
        return self.index.base_address


class StreamRelativePointer(RelativePointer):
    """A `StreamRelativePointer` field is a :class:`RelativePointer` field
    which refers to a :class:`Stream` field.

    A `StreamRelativePointer` field is:

    *   *containable*: ``item in self`` returns `True` if *item* is part
        of the `Stream` field.
    *   *sized*: ``len(self)`` returns the length of the `Stream` field.
    *   *subscriptable* ``self[index]`` returns the *byte* at the *index*
        of the `Stream` field.
    *   *iterable* ``iter(self)`` iterates over the bytes of the `Stream`
        field.

    :param int size: is the size of the `Stream` field in bytes.
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
        if isinstance(self._data, Stream):
            self._data.resize(size)


class StringRelativePointer(StreamRelativePointer):
    """A `StringRelativePointer` field is a :class:`StreamRelativePointer`
    which refers to a :class:`String` field.

    :param int size: is the *size* of the `String` field in bytes.
    """

    def __init__(self, size=0, address=None):
        super().__init__(size=0, address=address)
        self._data = String(size)
