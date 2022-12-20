# -*- coding: utf-8 -*-
"""
core.py
~~~~~~~
Core classes.

:copyright: (c) 2015-2022 by Jochen Gerhaeusser.
:license: BSD, see LICENSE for details
"""
from __future__ import annotations

import abc
import calendar
import copy
import csv
import datetime
import ipaddress
import json
import math
import struct
import time
from configparser import ConfigParser
from operator import attrgetter
from typing import (
    Any, Callable,
    Iterable, Iterator,
    Literal,
    ItemsView, KeysView, ValuesView,
    Mapping, MutableSequence, NamedTuple, Type)

from .categories import Category
from .enums import Enumeration
from .exceptions import (
    ByteOrderTypeError, ByteOrderValueError,
    EnumTypeError, FactoryTypeError, MemberTypeError,
    ProviderTypeError, ContainerLengthError,
    FieldAddressError, FieldAlignmentError, FieldByteOrderError,
    FieldIndexError, FieldSizeError, FieldTypeError, FieldValueError,
    FieldValueEncodingError,
    FieldGroupByteOrderError, FieldGroupOffsetError, FieldGroupSizeError
)
from .globals import (
    ItemClass, Byteorder, BYTEORDER, clamp)
from .options import (
    Option,
    byte_order_option, get_byte_order, nested_option, get_nested,
    verbose_option, verbose
)
from .providers import Provider


def is_any(instance: Any) -> bool:
    return isinstance(instance, (Structure, Sequence, Field))


def is_provider(instance: Any) -> bool:
    return isinstance(instance, Provider)


def is_field(instance: Any) -> bool:
    return isinstance(instance, Field)


def is_container(instance: Any) -> bool:
    return isinstance(instance, (Sequence, Structure))


def is_sequence(instance: Any) -> bool:
    return isinstance(instance, Sequence)


def is_array(instance: Any) -> bool:
    return isinstance(instance, Array)


def is_structure(instance: Any) -> bool:
    return isinstance(instance, Structure)


def is_mapping(instance: Any) -> bool:
    return isinstance(instance, Mapping)


def is_pointer(instance: Any):
    return isinstance(instance, Pointer)


def is_mixin(instance: Any) -> bool:
    return is_container(instance) or is_pointer(instance)


class Patch(NamedTuple):
    """ The :class:`Patch` class contains the relevant information to patch a
    memory area of a `data source` accessed via a data :class:`Provider` by a
    :class:`Pointer` field.

    :param bytes buffer: byte stream for the memory area to patch within the
        data source. The byte stream contains the data of the patch item.
    :param int address: address of the memory area to patch in the data source.
    :param Byteorder byteorder: byte order of the memory area to patch in the
        data source.
    :param int bit_size: bit size of the patch item.
    :param int bit_offset: bit offset of the patch item within the memory area.
    :param bool inject: if :data:`True` the patch item must be injected into the
        memory area.
    """
    #: Byte stream for the memory area in the data source to patch.
    buffer: bytes
    #: Start address of the memory area in the data source to patch.
    address: int
    #: Byte order of the memory area in the data source to patch.
    byteorder: Byteorder
    #: Bit size of the patch item.
    bit_size: int
    #: Bit offset of the patch item within the memory area.
    bit_offset: int
    #: Indicate the patch item must be injected into the memory area or not.
    inject: bool = False


class Index(NamedTuple):
    """ The :class:`Index` class contains the relevant information of the
    location of a :class:`Field` in a `byte stream` and in a `data source`.
    The `byte stream` is normally provided by a :class:`Pointer` field. The
    `data source` is normally accessed via a data :class:`Provider` by a
    :class:`Pointer` field.

    :param int byte: byte offset of the :class:`Field` in the byte stream.
    :param int bit: bit offset of the :class:`Field` relative to its byte offset.
    :param int address: address of the :class:`Field` in the data source.
    :param int base_address: start address of the byte stream in the data source.
    :param bool update: if :data:`True` the byte stream needs to be updated.
    """
    #: Byte offset of the :class:`Field` in the byte stream.
    byte: int = 0
    #: Bit offset of the :class:`Field` relative to its byte offset.
    bit: int = 0
    #: Address of the :class:`Field` in the data source.
    address: int = 0
    #: Start address of the byte stream in the data source.
    base_address: int = 0
    #: Indicates the byte stream needs to be updated or not.
    update: bool = False


class Alignment(NamedTuple):
    """ The :class:`Alignment` class contains the location of the :class:`Field`
    within an aligned group of consecutive fields.

    :param int byte_size: size of the *field group* in bytes
        which the :class:`Field` is aligned to.
    :param int bit_offset: bit offset of the :class:`Field`
        within its aligned *field group*.
    """
    #: Size of the *field group* in bytes which the :class:`Field` is aligned to.
    byte_size: int = 0
    #: Bit offset of the :class:`Field` within its aligned *field group*.
    bit_offset: int = 0


class CustomizedJsonEncoder(json.JSONEncoder):
    """ Customized JSON encoder.
    """

    def default(self, instance):
        if isinstance(instance, Category):
            return instance.name

        return super().default(instance)


class Container:
    """ The :class:`Container` class is an *abstract interface* for all classes
    which can contain :class:`Field` items. Container classes are
    :class:`Structures <Structure>`,
    :class:`Sequences <Sequence>`,
    :class:`Arrays <Array>` and
    :class:`Pointers <Pointer>`.

    The :class:`Container` class provides core features to **view**, **save**
    and **load** the *attributes* of the :class:`Field` items in the `Container`.
    """

    @abc.abstractmethod
    def view_fields(self,
                    *attributes: str,
                    **options: Any) -> dict[str, Any] | list[Any]:
        """ Returns a container with the selected field *attribute* or with the
        dictionary of the selected field *attributes* for each :class:`Field`
        *nested* in the `Container`.

        The *attributes* of each :class:`Field` for containers *nested* in the
        `Container` are viewed as well (chained method call).

        :param str attributes: selected :class:`Field` attributes.
            Fallback is the field :attr:`~Field.value`.
        :keyword tuple[str, ...] fieldnames: sequence of dictionary keys for the
            selected field *attributes*. Defaults to ``(*attributes)``.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            `Container` views their referenced :attr:`~Pointer.data` object field
            attributes as well (chained method call).

        .. note::
            This abstract method must be implemented by a derived class.
        """
        pass

    @abc.abstractmethod
    def field_items(self,
                    path: str = str(),
                    **options: Any) -> list[tuple[str, Field]]:
        """ Returns a **flatten** list of ``('field path', field item)`` tuples
        for each :class:`Field` *nested* in the `Container`.

        :param str path: item path.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            :attr:`~Pointer.data` objects of all :class:`Pointer` fields in the
            `Container` list their referenced :attr:`~Pointer.data` object field
            items as well (chained method call).

        .. note::
            This abstract method must be implemented by a derived class.
        """
        return list()

    @nested_option()
    def to_list(self,
                *attributes: str,
                **options: Any) -> list[tuple[str, Any] |
                                        tuple[str, tuple[Any, ...]]]:
        """ Returns a **flatten** list of ``('field path', attribute)`` or
        ``('field path', tuple(attributes))`` tuples for each :class:`Field`
        *nested* in the `Container`.

        :param str attributes: selected :class:`Field` attributes.
            Fallback is the field :attr:`~Field.value`.
        :keyword str name: name of the `Container`.
            Default is the class name of the instance.
        :keyword bool chain: if :data:`True` the field *attributes* are chained
            to its field path. Defaults to ``False``.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            `Container` lists their referenced :attr:`~Pointer.data` object field
            attributes as well (chained method call).
        """

        # Name of the Container
        name = options.pop('name', self.__class__.__name__)

        fields = list()
        if attributes:
            field_getter = attrgetter(*attributes)
        else:
            field_getter = attrgetter('value')
        for item in self.field_items(**options):
            field_path, field = item
            if field_path.startswith('['):
                # Sequence
                field_path = f"{name}{field_path}"
            else:
                field_path = f"{name}.{field_path}"
            if options.get('chain', False) and len(attributes) > 1:
                fields.append((field_path, *field_getter(field)))
            else:
                fields.append((field_path, field_getter(field)))
        return fields

    @nested_option()
    def to_dict(self,
                *attributes: str,
                **options: Any) -> dict[str, Any | tuple[Any, ...]]:
        """ Returns a **flatten** :class:`dict` of ``{'field path': attribute}``
        or ``{'field path': tuple(attributes)}`` pairs for each :class:`Field`
        *nested* in the `Container`.

        :param str attributes: selected :class:`Field` attributes.
            Fallback is the field :attr:`~Field.value`.
        :keyword str name: name of the `Container`.
            Default is the class name of the instance.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            `Container` lists their referenced :attr:`~Pointer.data` object field
            attributes as well (chained method call).
        """
        # Name of the Container
        name = options.pop('name', self.__class__.__name__)
        # Save to file
        save = options.pop('save', False)

        fields = dict()
        fields[name] = dict()
        if attributes:
            field_getter = attrgetter(*attributes)
        else:
            field_getter = attrgetter('value')
        for item in self.field_items(**options):
            field_path, field = item
            if save and field_path.startswith('['):
                # Sequence element
                field_path = '_' + field_path
            fields[name][field_path] = field_getter(field)
        return fields

    @nested_option()
    def save(self,
             file: str,
             *attributes: str,
             **options: Any) -> None:
        """ Saves the selected field *attributes* for each :class:`Field`
        *nested* in the `Container` to an ``.ini`` *file*.

        :param str file: name and location of the ``.ini`` *file*.
        :param str attributes: selected :class:`Field` attributes.
            Fallback is the field :attr:`~Field.value`.
        :keyword str section: section in the ``.ini`` file to look for the
            :class:`Field` values of the `Container`. If no *section* is
            specified the class name of the instance is used.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            `Container` saves their referenced :attr:`~Pointer.data` object field
            attributes as well (chained method call).

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
        >>> foo.to_list(nested=True)
        [('Foo.stream', ''),
         ('Foo.float', 0.0),
         ('Foo.structure.decimal', 0),
         ('Foo.array[0]', '0x0'),
         ('Foo.array[1]', '0x0'),
         ('Foo.array[2]', '0x0'),
         ('Foo.pointer', '0x0')]
        >>> foo.to_json(nested=True)
        '{"stream": "",
          "float": 0.0,
          "structure": {"decimal": 0},
          "array": ["0x0", "0x0", "0x0"],
          "pointer": {"value": "0x0",
                      "data": null}}'
        >>> foo.save('foo.ini')

        File `foo.ini`:

        .. code-block:: ini

            [Foo]
            stream =
            float = 0.0
            structure.decimal = 0
            array[0] = 0x0
            array[1] = 0x0
            array[2] = 0x0
            pointer = 0x0
        """
        options['save'] = True
        parser = ConfigParser()
        parser.read_dict(self.to_dict(*attributes, **options))
        with open(file, 'w') as file_:
            parser.write(file_)
        file_.close()

    @nested_option()
    @verbose_option(True)
    def load(self,
             file: str,
             **options: Any) -> None:
        """ Loads the field *value* for each :class:`Field` *nested* in the
        `Container` from an ``.ini`` *file*.

        :param str file: name and location of the ``.ini`` file.
        :keyword str section: section in the ``.ini`` file to look-up the
            value for each :class:`Field` in the `Container`.
            If no *section* is specified the class name of the instance is used.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            `Container` load their referenced :attr:`~Pointer.data` object field
            values as well (chained method call).
        :keyword bool verbose: if :data:`True` the loading is executed in verbose
            mode.

        File `foo.ini`:

        .. code-block:: ini

            [Foo]
            stream =
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
        Foo.stream =
        Foo.float = 0.0
        Foo.structure.decimal = 0
        Foo.array[0] = 0x0
        Foo.array[1] = 0x0
        Foo.array[2] = 0x0
        Foo.pointer = 0x0
        >>> foo.to_list(nested=True)
        [('Foo.stream', ''),
         ('Foo.float', 0.0),
         ('Foo.structure.decimal', 0),
         ('Foo.array[0]', '0x0'),
         ('Foo.array[1]', '0x0'),
         ('Foo.array[2]', '0x0'),
         ('Foo.pointer', '0x0')]
        >>> foo.to_json(nested=True)
        '{"stream": "",
          "float": 0.0,
          "structure": {"decimal": 0},
          "array": ["0x0", "0x0", "0x0"],
          "pointer": {"value": "0x0",
                      "data": null}}'
        """
        section = options.pop('section', self.__class__.__name__)

        parser = ConfigParser()
        parser.read(file)

        if parser.has_section(section):
            verbose(options, f"[{section}]")

            for field_path, field in self.field_items(**options):
                if field_path.startswith('['):
                    # Sequence element
                    option = '_' + field_path
                else:
                    option = field_path
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
                        stream = bytes.fromhex(value.replace("'", ""))
                        # Auto size a zero sized stream field to the current length
                        if not field:
                            field.resize(len(stream))
                        field.value = stream
                    # Decimal fields
                    else:
                        field.value = parser.get(section, option)
                    if field_path.startswith('['):
                        verbose(options,
                                f"{section}{field_path} = {field.value}")
                    else:
                        verbose(options,
                                f"{section}.{field_path} = {field.value}")
        else:
            verbose(options, f"No section [{section}] found.")

    @nested_option()
    def to_json(self,
                *attributes: str,
                **options: Any) -> str:
        """ Returns the selected field *attributes* for each :class:`Field`
        *nested* in the `Container` as a JSON formatted string.

        The *attributes* of each :class:`Field` for containers *nested* in the
        `Container` are viewed as well (chained method call).

        :param str attributes: selected :class:`Field` attributes.
            Fallback is the field :attr:`~Field.value`.
        :keyword tuple[str, ...] fieldnames: sequence of dictionary keys for the
            selected field *attributes*. Defaults to ``(*attributes)``.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            `Container` views their referenced :attr:`~Pointer.data` object field
            attributes as well (chained method call).
        """
        nested = options.pop('nested', False)
        fieldnames = options.pop('fieldnames', attributes)
        if 'cls' in options.keys():
            return json.dumps(self.view_fields(*attributes,
                                               nested=nested,
                                               fieldnames=fieldnames),
                              **options)
        else:
            return json.dumps(self.view_fields(*attributes,
                                               nested=nested,
                                               fieldnames=fieldnames),
                              cls=CustomizedJsonEncoder,
                              **options)

    @nested_option()
    def write_json(self,
                   file: str,
                   *attributes: str,
                   **options: Any) -> None:
        """ Writes the selected field *attributes* for each :class:`Field`
        *nested* in the `Container` to a ``.json`` *file*.

        :param str file: name and location of the ``.json`` *file*.
        :param str attributes: selected :class:`Field` attributes.
            Fallback is the field :attr:`~Field.value`.
        :keyword tuple[str, ...] fieldnames: sequence of dictionary keys for the
            field *path* and the selected field *attributes*.
            Defaults to ``(*attributes)``.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            `Container` lists their referenced :attr:`~Pointer.data` object field
            attributes as well (chained method call).
        """
        content = self.to_json(*attributes, **options)
        with open(file, 'w', newline='') as file_:
            file_.write(content)

    @staticmethod
    def _get_fieldnames(*attributes: str,
                        **options: Any) -> list[str]:
        # Default dictionary keys
        keys = ['id']
        if attributes:
            keys.extend(attributes)
        else:
            keys.append('value')
        # Customized dictionary keys
        return options.get('fieldnames', keys)

    @nested_option()
    def to_csv(self,
               *attributes: str,
               **options: Any) -> list[dict[str, Any]]:
        """ Returns a **flatten** list of dictionaries containing the field
        *path* and the selected field *attributes* for each :class:`Field`
        *nested* in the `Container`.

        :param str attributes: selected :class:`Field` attributes.
            Fallback is the field :attr:`~Field.value`.
        :keyword str name: name of the `Container`.
            Default is the class name of the instance.
        :keyword tuple[str, ...] fieldnames: sequence of dictionary keys for
            the field *path* and the selected field *attributes*.
            Defaults to ``('id', *attributes)``.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            `Container` lists their referenced :attr:`~Pointer.data` object field
            attributes as well (chained method call).
        """
        keys = self._get_fieldnames(*attributes, **options)
        options['chain'] = True
        return [dict(zip(keys, field)) for field in
                self.to_list(*attributes, **options)]

    @nested_option()
    def write_csv(self,
                  file: str,
                  *attributes: str,
                  **options: Any) -> None:
        """ Writes the field *path* and the selected field *attributes* for each
        :class:`Field` *nested* in the `Container` to a ``.csv`` *file*.

        :param str file: name and location of the ``.csv`` *file*.
        :param str attributes: selected :class:`Field` attributes.
            Fallback is the field :attr:`~Field.value`.
        :keyword str name: name of the `Container`.
            Default is the class name of the instance.
        :keyword tuple[str, ...] fieldnames: sequence of dictionary keys for the
            field *path* and the selected field *attributes*.
            Defaults to ``('id', *attributes)``.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            `Container` lists their referenced :attr:`~Pointer.data` object field
            attributes as well (chained method call).
        """
        with open(file, 'w', newline='') as file_:
            fieldnames = self._get_fieldnames(*attributes, **options)
            writer = csv.DictWriter(file_, fieldnames)
            writer.writeheader()
            content = self.to_csv(*attributes, **options)
            for row in content:
                writer.writerow(row)


class Structure(dict, Container):
    """ The :class:`Structure` is a :class:`dict` whereby the dictionary `key`
    describes the *name* of a *member* of the `Structure` and the `value` of the
    dictionary `key` describes the *type* of the *member*. Allowed *members* are
    :class:`Structure`, :class:`Sequence`, :class:`Array` or :class:`Field`
    instances.

    The :class:`Structure` class extends the :class:`dict` with the
    :class:`Container` interface and attribute getter and setter for the
    ``{'key': value}`` tuples to access and to assign the *members* of the
    `Structure` easier, but this comes with the trade-off that the dictionary
    `keys` must be valid Python attribute names.

    A `Structure` has additional methods to **read**, **deserialize**,
    **serialize** and **view** binary data:

    - **Read** from a :class:`Provider` the necessary bytes for each
      :attr:`~Pointer.data` object referenced by the :class:`Pointer` fields
      in the `Structure` via :meth:`read_from()`.
    - **Deserialize** the :attr:`~Field.value` for each :class:`Field`
      in the `Structure` from a byte stream via :meth:`deserialize()`.
    - **Serialize** the :attr:`~Field.value` for each :class:`Field`
      in the `Structure` to a byte stream via :meth:`serialize()`.
    - Indexes all fields in the `Structure`
      via :meth:`index_fields()`.
    - Get the **first** :class:`Field` in the `Structure`
      via :meth:`first_field()`.
    - Get the accumulated **size** of all fields in the `Structure`
      via :meth:`container_size()`.
    - View the selected *attributes* for each :class:`Field` in the `Structure`
      via :meth:`view_fields()`.
    - List the **path** to the field and the field **item** itself for each
      :class:`Field` in the `Structure` as a flatted list via :meth:`field_items()`.
    - Get the **metadata** of the `Structure` via :meth:`describe()`.
    """
    # Item type.
    item_type: ItemClass = ItemClass.Structure

    def __init__(self,
                 *args: Mapping | None,
                 **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def __bytes__(self) -> bytes:
        buffer = bytearray()
        self.serialize(buffer)
        return bytes(buffer)

    def __getitem__(self, key: str) -> Structure | Sequence | Field:
        return super().__getitem__(key)

    def __setitem__(self,
                    name: str,
                    item: Structure | Sequence | Field | Mapping):
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

    def __getattr__(self, name: str) -> Any:
        """ Returns the :class:`Field` of the `Structure` member whose
        dictionary key is equal to the *name*.

        If the attribute *name* is in the namespace of the `Structure` class
        then the base class is called instead.

        The `__getattr__` method is only called when the method
        `__getattribute__` raises an `AttributeError` exception.
        """
        # Namespace check for dict attribute
        if hasattr(Structure, name):
            return super().__getattribute__(name)
        try:
            return self[name]
        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__,}' object has not attribute '{name}'")

    def __setattr__(self,
                    name: str,
                    item: Structure | Sequence | Field) -> None:
        """ Assigns the *item* to the member of the `Structure` whose dictionary
        key is equal to the *name*.

        If the attribute *name* is in the namespace of the `Structure` base class
        then the base class is called instead.
        """
        # Attribute check
        if hasattr(Structure, name):
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
    def read_from(self,
                  provider: Provider,
                  **options: Any) -> None:
        """ All :class:`Pointer` fields in the `Structure` read the necessary
        number of bytes from the data :class:`Provider` for their referenced
        :attr:`~Pointer.data` object. Null pointer are ignored.

        :param Provider provider: data :class:`Provider`.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            :attr:`~Pointer.data` objects of all :class:`Pointer` fields in the
            `Structure` reads their referenced :attr:`~Pointer.data` object as
            well (chained method call).
            Each :class:`Pointer` field stores the bytes for its referenced
            :attr:`~Pointer.data` object in its :attr:`~Pointer.bytestream`.
        """
        for item in self.values():
            # Container or Pointer
            if is_mixin(item):
                item.read_from(provider, **options)

    @byte_order_option()
    @nested_option()
    def deserialize(self,
                    buffer: bytes = bytes(),
                    index: Index = Index(),
                    **options: Any) -> Index:
        """ De-serializes the `Structure` from the byte *buffer* starting at
        the beginning of the *buffer* or with the given *index* by mapping the
        bytes to the :attr:`~Field.value` for each :class:`Field` in the
        `Structure` in accordance with the decoding *byte order* for the
        de-serialization and the decoding :attr:`byte_order` of each
        :class:`Field` in the `Structure`.

        A specific decoding :attr:`~Field.byte_order` of a :class:`Field`
        overrules the decoding *byte order* for the de-serialization.

        Returns the :class:`Index` of the *buffer* after the last de-serialized
        :class:`Field` in the `Structure`.

        Optional the de-serialization of the referenced :attr:`~Pointer.data`
        objects of all :class:`Pointer` fields in the `Structure` can be
        enabled.

        :param bytes buffer: byte stream to de-serialize from.
        :param Index index: current read :class:`Index` within the *buffer* to
            de-serialize.
        :keyword byte_order: decoding byte order for the de-serialization.
        :type byte_order: Byteorder|Literal['auto', 'big', 'little']
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields of a
            `Structure` de-serialize their referenced :attr:`~Pointer.data`
            object as well (chained method call).
            Each :class:`Pointer` field uses for the de-serialization of its
            referenced  :attr:`~Pointer.data` object its own
            :attr:`~Pointer.bytestream`.
        """
        for item in self.values():
            index = item.deserialize(buffer, index, **options)
        return index

    @byte_order_option()
    @nested_option()
    def serialize(self,
                  buffer: bytearray = bytearray(),
                  index: Index = Index(),
                  **options: Any) -> Index:
        """ Serializes the `Structure` to the byte *buffer* starting at the
        beginning of the *buffer* or with the given *index* by mapping the
        :attr:`~Field.value` for each :class:`Field` in the `Structure` to the
        byte *buffer* in accordance with the encoding *byte order* for the
        serialization and the encoding :attr:`byte_order` of each :class:`Field`
        in the `Structure`.

        A specific encoding :attr:`~Field.byte_order` of a :class:`Field`
        overrules the encoding *byte order* for the serialization.

        Returns the :class:`Index` of the *buffer* after the last serialized
        :class:`Field` in the `Structure`.

        Optional the serialization of the referenced :attr:`~Pointer.data`
        objects of all :class:`Pointer` fields in the `Structure` can be
        enabled.

        :param bytearray buffer: byte stream to serialize to.
        :param Index index: current write :class:`Index` within the *buffer*.
        :keyword byte_order: encoding byte order for the serialization.
        :type byte_order: Byteorder|Literal['auto', 'big', 'little']
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields of a
            `Structure` serialize their referenced :attr:`~Pointer.data` object
            as well (chained method call).
            Each :class:`Pointer` field uses for the serialization of its
            referenced :attr:`~Pointer.data` object its own
            :attr:`~Pointer.bytestream`.
        """
        for item in self.values():
            index = item.serialize(buffer, index, **options)
        return index

    @nested_option()
    def index_fields(self,
                     index: Index = Index(),
                     **options: Any) -> Index:
        """ Indexes all fields in the `Structure` starting with the given
        *index* and returns the :class:`Index` after the last :class:`Field`
        in the `Structure`.

        :param Index index: start :class:`Index` for the first :class:`Field`
            in the `Structure`.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields of the
            `Structure` indexes their referenced :attr:`~Pointer.data` object
            fields as well (chained method call).
        """
        for name, item in self.items():
            # Container
            if is_container(item):
                index = item.index_fields(index, **options)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                index = item.index_field(index)
                item.index_data()
            # Field
            elif is_field(item):
                index = item.index_field(index)
            else:
                raise MemberTypeError(self, item, name, index)
        return index

    def container_size(self) -> tuple[int, int]:
        """ Returns the accumulated bit size of all fields in the `Structure` as
        a tuple in the form of ``(number of bytes, remaining number of bits)``.
        """
        length = 0
        for name, item in self.items():
            # Container
            if is_container(item):
                byte_length, bit_length = item.container_size()
                length += bit_length + byte_length * 8
            # Field
            elif is_field(item):
                length += item.bit_size
            else:
                raise MemberTypeError(self, item, name)
        return divmod(length, 8)

    def first_field(self) -> Field | None:
        """ Returns the first :class:`Field` in the `Structure`, or :data:`None`
        for an empty `Structure`.
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

    def initialize_fields(self,
                          content: dict[str, Any]) -> None:
        """ Initializes the :class:`Field` members in the `Structure` with
        the *values* in the *content* dictionary.

        :param dict[str, Any] content: a dictionary contains the :class:`Field`
            values for each member in the `Structure`.
        """
        for name, value in content.items():
            item = self[name]
            # Container or Pointer
            if is_mixin(item):
                item.initialize_fields(value)
            # Fields
            elif is_field(item):
                item.value = value
            else:
                raise MemberTypeError(self, item, name)

    @nested_option()
    def view_fields(self,
                    *attributes: str,
                    **options: Any) -> dict[str, Any]:
        """ Returns an :class:`dict` which contains the ``{'member name':
        field attribute}``, or the  ``{'member name': dict(field attributes)}``
        tuples for each :class:`Field` *nested* in the `Structure`.

        The *attributes* of each :class:`Field` for containers *nested* in the
        `Structure` are viewed as well (chained method call).

        :param str attributes: selected :class:`Field` attributes.
            Fallback is the field :attr:`~Field.value`.
        :keyword tuple[str, ...] fieldnames: sequence of dictionary keys for the
            selected field *attributes*. Defaults to ``(*attributes)``.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields nested
            in the `Structure` views their referenced :attr:`~Pointer.data`
            object field attributes as well (chained method call).
        """
        members = dict()
        for name, item in self.items():
            # Container
            if is_container(item):
                members[name] = item.view_fields(*attributes, **options)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                members[name] = item.view_fields(*attributes, **options)
            # Field
            elif is_field(item):
                if attributes:
                    field_getter = attrgetter(*attributes)
                else:
                    field_getter = attrgetter('value')
                if len(attributes) > 1:
                    fieldnames = options.get('fieldnames', attributes)
                    members[name] = dict(zip(fieldnames, field_getter(item)))
                else:
                    members[name] = field_getter(item)

        return members

    @nested_option()
    def field_items(self,
                    path: str = str(),
                    **options: Any) -> list[tuple[str, Field]]:
        """ Returns a **flatten** list of ``('field path', field item)`` tuples
        for each :class:`Field` *nested* in the `Structure`.

        :param str path: field path of the `Structure`.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            :attr:`~Pointer.data` objects of all :class:`Pointer` fields in the
            `Structure` list their referenced :attr:`~Pointer.data` object field
            items as well (chained method call).
        """
        parent = path if path else str()

        items = list()
        for name, item in self.items():
            item_path = f"{parent}.{name}" if parent else name
            # Container
            if is_container(item):
                for field in item.field_items(item_path, **options):
                    items.append(field)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                for field in item.field_items(item_path, **options):
                    items.append(field)
            # Field
            elif is_field(item):
                items.append((item_path, item))
            else:
                raise MemberTypeError(self, item, item_path)
        return items

    @nested_option(True)
    def describe(self,
                 name: str = str(),
                 **options: Any) -> dict[str, Any]:
        """ Returns the **metadata** of the `Structure` as a :class:`dict`.

        .. code-block:: python

            metadata = {
                'class': self.__class__.__name__,
                'name': name if name else self.__class__.__name__,
                'size': len(self),
                'type': Structure.item_type.name
                'member': [
                    item.describe(member) for member, item in self.items()
                ]
            }

        :param str name: optional name for the `Structure`.
            Fallback is the class name.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields of the
            `Structure` lists their referenced :attr:`~Pointer.data` object
            fields as well (chained method call). Default is :data:`True`.
        """
        members = list()
        metadata = dict()
        metadata['class'] = self.__class__.__name__
        metadata['name'] = name if name else self.__class__.__name__
        metadata['size'] = len(self)
        metadata['type'] = self.item_type.name
        metadata['member'] = members

        for member_name, item in self.items():
            # Container
            if is_container(item):
                members.append(item.describe(member_name, **options))
            # Pointer
            elif is_pointer(item) and get_nested(options):
                members.append(item.describe(member_name, **options))
            # Field
            elif is_field(item):
                members.append(item.describe(member_name, nested=False))
            else:
                raise MemberTypeError(self, item, member_name)
        return metadata


class Sequence(MutableSequence, Container):
    """ The :class:`Sequence` is a mutable sequence containing heterogeneous
    *items*, and is extended with the :class:`Container` interface.

    Allowed *items* are :class:`Structure`, :class:`Sequence`, :class:`Array`
    or :class:`Field` instances.

    A `Sequence` is:

    - *containable*: ``item`` in ``self`` returns :data:`True` if *item* is in
      the `Sequence`.
    - *sized*: ``len(self)`` returns the number of items in the `Sequence`.
    - *indexable* ``self[index]`` returns the *item* at the *index*
      of the `Sequence`.
    - *iterable* ``iter(self)`` iterates over the *items* in the `Sequence`

    A `Sequence` supports the usual methods for sequences:

    - **Append** an item to the `Sequence` via :meth:`append()`.
    - **Insert** an item before the *index* into the `Sequence`
      via :meth:`insert()`.
    - **Extend** the `Sequence` with items via :meth:`extend()`.
    - **Clear** the `Sequence` via :meth:`clear()`.
    - **Pop** an item with the *index* from the `Sequence` via :meth:`pop()`.
    - **Remove** the first occurrence of an *item* from the `Sequence`
      via :meth:`remove()`.
    - **Reverse** all items in the `Sequence` via :meth:`reverse()`.

    A `Sequence` has additional methods to **read**, **deserialize**,
    **serialize** and **view** binary data:

    - **Read** from a :class:`Provider` the necessary bytes for each
      :attr:`~Pointer.data` object referenced by the :class:`Pointer` fields
      in the `Sequence` via :meth:`read_from()`.
    - **Deserialize** the :attr:`~Field.value` for each :class:`Field`
      in the `Sequence` from a byte stream via :meth:`deserialize()`.
    - **Serialize** the :attr:`~Field.value` for each :class:`Field`
      in the `Sequence` to a byte stream via :meth:`serialize()`.
    - Indexes all fields in the `Sequence` via :meth:`index_fields()`.
    - Get the **first** :class:`Field`
      in the `Sequence` via :meth:`first_field()`.
    - Get the accumulated **size** of all fields in the `Sequence`
      via :meth:`container_size()`.

    - View the selected *attributes* for each :class:`Field`
      in the `Sequence` via :meth:`view_fields()`.
    - List the **path** to the field and the field **item** itself for each
      :class:`Field` in the `Sequence` as a flatted list via :meth:`field_items()`.
    - Get the **metadata** of the `Sequence` via :meth:`describe()`.

    :param iterable: any *iterable* that contains items of :class:`Structure`,
        :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
        *iterable* is one of these instances itself then the *iterable* itself
        is appended to the `Sequence`.
    :type iterable: Iterable[Structure|Sequence|Field]|Structure|Sequence|Field|None
    """
    # Item type.
    item_type: ItemClass = ItemClass.Sequence

    def __init__(self,
                 iterable: (Iterable[Structure | Sequence | Field] |
                            Structure | Sequence | Field | None) = None) -> None:
        # Data object
        self._data = []

        if iterable is None:
            pass
        elif is_any(iterable):
            self.append(iterable)
        else:
            for member, item in enumerate(iterable):
                if not is_any(item):
                    raise MemberTypeError(self, item, member=member)
                self.append(item)

    def __bytes__(self) -> bytes:
        buffer = bytearray()
        self.serialize(buffer)
        return bytes(buffer)

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return repr(self._data)

    def __contains__(self, key: Structure | Sequence | Field) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self,
                    index: int | slice) -> Structure | Sequence | Field | list:
        return self._data[index]

    def __setitem__(self,
                    index: int,
                    item: Structure | Sequence | Field) -> None:
        if not is_any(item):
            raise MemberTypeError(self, item, member=index)
        self._data[index] = item

    def __delitem__(self, index: int) -> None:
        del self._data[index]

    def __iter__(self) -> Iterator[Structure | Sequence | Field]:
        return iter(self._data)

    def append(self,
               item: Structure | Sequence | Field) -> None:
        """ Appends the *item* to the end of the `Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        :type item: Structure|Sequence|Field
        """
        if not is_any(item):
            raise MemberTypeError(self, item, member=len(self))
        self._data.append(item)

    def insert(self,
               index: int,
               item: Structure | Sequence | Field) -> None:
        """ Inserts the *item* before the *index* into the `Sequence`.

        :param int index: `Sequence` index.
        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        :type item: Structure|Sequence|Field
        """
        if not is_any(item):
            raise MemberTypeError(self, item, member=len(self))
        self._data.insert(index, item)

    def pop(self, index: int = -1) -> Structure | Sequence | Field:
        """ Removes and returns the item at the *index* from the `Sequence`.

        :param int index: `Sequence` index.
        """
        return self._data.pop(index)

    def clear(self) -> None:
        """ Remove all items from the `Sequence`."""
        self._data.clear()

    def remove(self, item: Structure | Sequence | Field) -> None:
        """ Removes the first occurrence of an *item* from the `Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        :type item: Structure|Sequence|Field
        """
        self._data.remove(item)

    def reverse(self) -> None:
        """ In place reversing of the `Sequence` items."""
        self._data.reverse()

    def extend(self,
               iterable: (Iterable[Structure | Sequence | Field] |
                          Structure | Sequence | Field)) -> None:
        """ Extends the `Sequence` by appending items from the *iterable*.

        :param iterable: any *iterable* that contains items of :class:`Structure`,
            :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
            *iterable* is one of these instances itself then the *iterable* itself
            is appended to the `Sequence`.
        :type iterable: Iterable[Structure|Sequence|Field]|Structure|Sequence|Field
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
        # Iterable
        elif isinstance(iterable, (set, tuple, list)):
            self._data.extend(Sequence(iterable))
        else:
            raise MemberTypeError(self, iterable, member=len(self))

    @nested_option()
    def read_from(self,
                  provider: Provider,
                  **options: Any) -> None:
        """ All :class:`Pointer` fields in the `Sequence` read the necessary
        number of bytes from the data :class:`Provider` for their referenced
        :attr:`~Pointer.data` object. Null pointer are ignored.

        :param Provider provider: data :class:`Provider`.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            :attr:`~Pointer.data` objects of all :class:`Pointer` fields in the
            `Sequence` reads their referenced :attr:`~Pointer.data` object as
            well (chained method call).
            Each :class:`Pointer` field stores the bytes for its referenced
            :attr:`~Pointer.data` object in its :attr:`~Pointer.bytestream`.
        """
        for item in iter(self):
            # Container or Pointer
            if is_mixin(item):
                item.read_from(provider, **options)

    @byte_order_option()
    @nested_option()
    def deserialize(self,
                    buffer: bytes = bytes(),
                    index: Index = Index(),
                    **options: Any) -> Index:
        """ De-serializes the `Sequence` from the byte *buffer* starting at
        the beginning of the *buffer* or with the given *index* by mapping the
        bytes to the :attr:`~Field.value` for each :class:`Field` in the
        `Sequence` in accordance with the decoding *byte order* for the
        de-serialization and the decoding :attr:`byte_order` of each
        :class:`Field` in the `Sequence`.

        A specific decoding :attr:`~Field.byte_order` of a :class:`Field`
        overrules the decoding *byte order* for the de-serialization.

        Returns the :class:`Index` of the *buffer* after the last de-serialized
        :class:`Field` in the `Sequence`.

        Optional the de-serialization of the referenced :attr:`~Pointer.data`
        objects of all :class:`Pointer` fields in the `Sequence` can be
        enabled.

        :param bytes buffer: byte stream to de-serialize from.
        :param Index index: current read :class:`Index` within the *buffer* to
            de-serialize.
        :keyword byte_order: decoding byte order for the de-serialization.
        :type byte_order: Byteorder|Literal['auto', 'big', 'little']
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields of a
            `Sequence` de-serialize their referenced :attr:`~Pointer.data`
            object as well (chained method call).
            Each :class:`Pointer` field uses for the de-serialization of its
            referenced :attr:`~Pointer.data` object its own
            :attr:`~Pointer.bytestream`.
        """
        for item in iter(self):
            index = item.deserialize(buffer, index, **options)
        return index

    @byte_order_option()
    @nested_option()
    def serialize(self,
                  buffer: bytearray = bytearray(),
                  index: Index = Index(),
                  **options: Any) -> Index:
        """ Serializes the `Sequence` to the byte *buffer* starting at the
        beginning of the *buffer* or with the given *index* by mapping the
        :attr:`~Field.value` for each :class:`Field` in the `Sequence` to the
        byte *buffer* in accordance with the encoding *byte order* for the
        serialization and the encoding :attr:`byte_order` of each :class:`Field`
        in the `Sequence`.

        A specific encoding :attr:`~Field.byte_order` of a :class:`Field`
        overrules the encoding *byte order* for the serialization.

        Returns the :class:`Index` of the *buffer* after the last serialized
        :class:`Field` in the `Sequence`.

        Optional the serialization of the referenced :attr:`~Pointer.data`
        objects of all :class:`Pointer` fields in the `Sequence` can be
        enabled.

        :param bytearray buffer: byte stream to serialize to.
        :param Index index: current write :class:`Index` within the *buffer*.
        :keyword byte_order: encoding byte order for the serialization.
        :type byte_order: Byteorder|Literal['auto', 'big', 'little']
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields of a
            `Sequence` serialize their referenced :attr:`~Pointer.data` object
            as well (chained method call).
            Each :class:`Pointer` field uses for the serialization of its
            referenced :attr:`~Pointer.data` object its own
            :attr:`~Pointer.bytestream`.
        """
        for item in iter(self):
            index = item.serialize(buffer, index, **options)
        return index

    @nested_option()
    def index_fields(self,
                     index: Index = Index(),
                     **options: Any) -> Index:
        """ Indexes all fields in the `Sequence` starting with the given
        *index* and returns the :class:`Index` after the last :class:`Field`
        in the `Sequence`.

        :param Index index: start :class:`Index` for the first :class:`Field`
            in the `Sequence`.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            `Sequence` indexes their referenced :attr:`~Pointer.data` object
            fields as well (chained method call).
        """
        for name, item in enumerate(self):
            # Container
            if is_container(item):
                index = item.index_fields(index, **options)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                index = item.index_field(index)
                item.index_data()
            # Field
            elif is_field(item):
                index = item.index_field(index)
            else:
                raise MemberTypeError(self, item, name, index)
        return index

    def container_size(self) -> tuple[int, int]:
        """ Returns the accumulated bit size of all fields in the `Sequence` as
        a tuple in the form of ``(number of bytes, remaining number of bits)``.
        """
        length = 0
        for name, item in enumerate(self):
            # Container
            if is_container(item):
                byte_length, bit_length = item.container_size()
                length += bit_length + byte_length * 8
            # Field
            elif is_field(item):
                length += item.bit_size
            else:
                raise MemberTypeError(self, item, name)
        return divmod(length, 8)

    def first_field(self) -> Field | None:
        """ Returns the first :class:`Field` in the `Sequence`, or :data:`None`
        for an empty `Sequence`.
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

    def initialize_fields(self, content: list[Any]) -> None:
        """ Initializes the :class:`Field` items in the `Sequence` with
        the *values* in the *content* list.

        :param list[Any] content: a list contains the :class:`Field` values for
            each item in the `Sequence`.
        """
        for name, pair in enumerate(zip(self, content)):
            item, value = pair
            # Container or Pointer
            if is_mixin(item):
                item.initialize_fields(value)
            # Fields
            elif is_field(item):
                item.value = value
            else:
                raise MemberTypeError(self, item, name)

    @nested_option()
    def view_fields(self,
                    *attributes: str,
                    **options: Any) -> list[Any]:
        """ Returns a list with the selected field *attribute* or a list with the
        dictionaries of the selected field *attributes* for each :class:`Field`
        *nested* in the `Sequence`.

        The *attributes* of each :class:`Field` for containers *nested* in the
        `Sequence` are viewed as well (chained method call).

        :param str attributes: selected :class:`Field` attributes.
            Fallback is the field :attr:`~Field.value`.
        :keyword tuple[str, ...] fieldnames: sequence of dictionary keys for the
            selected field *attributes*. Defaults to ``(*attributes)``.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields nested
            in the `Sequence` views their referenced :attr:`~Pointer.data` object
            field attributes as well (chained method call).
        """
        items = list()

        for index, item in enumerate(self):
            if is_container(item):
                # Container
                items.append(item.view_fields(*attributes, **options))
            elif is_pointer(item) and get_nested(options):
                # Pointer
                items.append(item.view_fields(*attributes, **options))
            elif is_field(item):
                # Field
                if attributes:
                    field_getter = attrgetter(*attributes)
                else:
                    field_getter = attrgetter('value')

                if len(attributes) > 1:
                    fieldnames = options.get('fieldnames', attributes)
                    items.append(dict(zip(fieldnames, field_getter(item))))
                else:
                    items.append(field_getter(item))
            else:
                raise MemberTypeError(self, item, index)
        return items

    @nested_option()
    def field_items(self,
                    path: str = str(),
                    **options: Any):
        """ Returns a **flatten** list of ``('field path', field item)`` tuples
        for each :class:`Field` *nested* in the `Sequence`.

        :param str path: field path of the `Sequence`.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            :attr:`~Pointer.data` objects of all :class:`Pointer` fields in
            the `Sequence` list their referenced :attr:`~Pointer.data` object
            field items as well (chained method call).
        """
        items = list()
        for index, item in enumerate(self):
            if path:
                item_path = f"{path}[{str(index)}]"
            else:
                item_path = f"[{str(index)}]"
            # Container
            if is_container(item):
                for field_item in item.field_items(item_path, **options):
                    items.append(field_item)
            # Pointer
            elif is_pointer(item) and get_nested(options):
                for field_item in item.field_items(item_path, **options):
                    items.append(field_item)
            # Field
            elif is_field(item):
                items.append((item_path, item))
            else:
                raise MemberTypeError(self, item, item_path)
        return items

    @nested_option(True)
    def describe(self,
                 name: str = str(),
                 **options: Any) -> dict[str, Any]:
        """ Returns the **metadata** of the `Sequence` as a :class:`dict`.

        .. code-block:: python

            metadata = {
                'class': self.__class__.__name__,
                'name': name if name else self.__class__.__name__,
                'size': len(self),
                'type': Sequence.item_type.name
                'member': [
                    item.describe('name[idx]') for idx, item in enumerate(self)
                ]
            }

        :param str name: optional name for the `Sequence`.
            Fallback is the class name.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            `Sequence` lists their referenced :attr:`~Pointer.data` object fields
            as well (chained method call). Default is :data:`True`.
        """
        members = list()
        metadata = dict()
        metadata['class'] = self.__class__.__name__
        metadata['name'] = name if name else self.__class__.__name__
        metadata['size'] = len(self)
        metadata['type'] = self.item_type.name
        metadata['member'] = members

        for member_name, item in enumerate(self):
            # Container
            if is_container(item):
                members.append(item.describe(
                    f"{metadata['name']}[{member_name}]", **options))
            # Pointer
            elif is_pointer(item) and get_nested(options):
                members.append(item.describe(
                    f"{metadata['name']}[{member_name}]", **options))
            # Field
            elif is_field(item):
                members.append(item.describe(
                    f"{metadata['name']}[{member_name}]", nested=False))
            else:
                raise MemberTypeError(self, item, member_name)
        return metadata


class Array(Sequence):
    """ The :class:`Array` is a :class:`Sequence` which contains *elements* of
    one type. The *template* for the *array element* can be any :class:`Field`
    instance or a *callable* (factory) which returns a :class:`Structure`,
    :class:`Sequence`, :class:`Array` or any :class:`Field` instance.

    A *callable template* (factory) is necessary to ensure that the internal
    constructor for the array element produces complete copies for each array
    element including the *nested* objects in the *template* for the array
    element.

    An `Array` of :class:`Pointer` fields should use a *callable* instead of
    assigning a :class:`Pointer` field instance directly as the array element
    *template* to ensure that the referenced :attr:`~Pointer.data` object of a
    :class:`Pointer` field is also complete copied for each array element.

    An `Array` adapts and extends a :class:`Sequence` with the following features:

    - **Append** a new *array element* to the `Array` via :meth:`append()`.
    - **Insert** a new *array element* before the *index* into the `Array`
      via :meth:`insert()`.
    - **Re-size** the `Array` via :meth:`resize()`.

    An `Array` replaces the ``'type'`` key of the :attr:`~Sequence.metadata`
    of a :class:`Sequence` with its own `item` type.

    :param template: template for the *array element*.
        The *template* can be any :class:`Field` instance or any *callable*
        that returns a :class:`Structure`, :class:`Sequence`, :class:`Array`
        or any :class:`Field` instance.
    :param int capacity: capacity of the `Array` in number of *array elements*.
    """
    # Item type.
    item_type: ItemClass = ItemClass.Array

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0) -> None:
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
        self.resize(capacity)

    def __create__(self):
        if is_field(self._template):
            # Field: Array element instance
            return copy.copy(self._template)
        else:
            # Callable: Array element factory
            return self._template()

    def append(self) -> None:
        """ Appends a new *array element* to the `Array`."""
        super().append(self.__create__())

    def insert(self, index: int) -> None:
        """ Inserts a new *array element* before the *index* of the `Array`.

        :param int index: `Array` index.
        """
        super().insert(index, self.__create__())

    def resize(self, capacity: int) -> None:
        """ Re-sizes the `Array` by appending new *array elements* or
        removing *array elements* from the end.

        :param int capacity: new capacity of the `Array` in number of
            *array elements*.
        """
        count = max(int(capacity), 0) - len(self)

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

    def initialize_fields(self,
                          content: list[Any]) -> None:
        """ Initializes the :class:`Field` elements in the `Array` with the
        *values* in the *content* list.

        If the *content* list is shorter than the `Array` then the *content*
        list is used as a rotating fill pattern for the :class:`Field` elements
        in the `Array`.

        :param list[Any] content: a list contains the :class:`Field` values for
            each element in the `Array` or one :class:`Field` value for all
            elements in the `Array`.
        """

        if isinstance(content, (list, tuple)):
            capacity = len(content)
            for i in range(0, len(self), capacity):
                for name, pair in enumerate(zip(self[i:i + capacity],
                                                content),
                                            start=i):
                    item, value = pair
                    if is_mixin(item):
                        # Container or Pointer
                        item.initialize_fields(value)
                    elif is_field(item):
                        # Fields
                        item.value = value
                    else:
                        raise MemberTypeError(self, item, name)
        else:
            for name, item in enumerate(self):
                if is_mixin(item):
                    # Container or Pointer
                    item.initialize_fields(content)
                elif is_field(item):
                    # Fields
                    item.value = content
                else:
                    raise MemberTypeError(self, item, name)


class Field:
    """ The :class:`Field` class is the *abstract class* for all field classes.

    A `Field` has a specific **name**, **bit size**, **byte order**, and can be
    **aligned to** other fields.

    A `Field` has methods to **unpack**, **pack**, **deserialize** and
    **serialize** its field **value** from and to a byte stream, and stores its
    location within the byte stream and the providing data source in its field
    **index**.

    :param int bit_size: is the *size* of a `Field` in bits.
    :param int align_to: aligns the `Field` to the number of bytes,
        can be between ``1`` and ``8``.
    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Field`.
        Default is :class:`~Byteorder.auto`.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']
    """
    # Item type.
    item_type: ItemClass = ItemClass.Field

    def __init__(self,
                 bit_size: int = 0,
                 align_to: int = 0,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__()
        # Field index
        self._index: Index = Index()
        # Field alignment
        self._align_to_byte_size: int = align_to
        self._align_to_bit_offset: int = 0
        # Field byte order
        self._byte_order: Byteorder = Byteorder.auto
        self.byte_order = byte_order
        # Field bit size
        self._bit_size = bit_size
        # Field value
        self._value = None

    def __str__(self) -> str:
        return (f"{self.name}"
                f"({self.index!s}, "
                f"{self.alignment!s}, "
                f"{self.bit_size!s}, "
                f"{self.value!s})")

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}"
                f"(index={self.index!r}, "
                f"alignment={self.alignment!r}, "
                f"bit_size={self.bit_size!r}, "
                f"value={self.value!r})")

    @property
    def alignment(self) -> Alignment:
        """ Returns the :class:`Alignment` of the `Field` (read-only)."""
        return Alignment(self._align_to_byte_size, self._align_to_bit_offset)

    @property
    def bit_size(self) -> int:
        """ Returns the size of the `Field` in bits (read-only)."""
        return self._bit_size

    @property
    def byte_order(self) -> Byteorder:
        """ :class:`Byteorder` used to decode and encode the :attr:`value`
        of the `Field`.
        """
        return self._byte_order

    @byte_order.setter
    def byte_order(self,
                   value: (Literal['auto', 'big', 'little'] |
                           Byteorder | str)) -> None:
        byte_order = value
        if isinstance(byte_order, str):
            byte_order = Byteorder.get_member(value)
            if not byte_order:
                raise ByteOrderValueError(self, self.index, value)
        if not isinstance(byte_order, Byteorder):
            raise ByteOrderTypeError(self, value)
        self._byte_order = byte_order

    @property
    def index(self) -> Index:
        """ :class:`Index` of the `Field`."""
        return self._index

    @index.setter
    def index(self, value: Index) -> None:
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
        if self.alignment.byte_size < group_size:
            raise FieldGroupSizeError(self, value,
                                      Alignment(group_size,
                                                self.alignment.bit_offset))

        # No Bit field?
        if not self.is_bit():
            # Set field alignment bit offset
            self._align_to_bit_offset = bit
        # Bad aligned field group?
        elif self.alignment.bit_offset != bit:
            raise FieldGroupOffsetError(self, value,
                                        Alignment(self.alignment.byte_size,
                                                  bit))

        # Invalid field address
        if address < 0:
            raise FieldAddressError(self, value, address)

        # Set field index
        self._index = Index(int(byte), int(bit),
                            int(address), int(base),
                            update)

    @property
    def name(self) -> str:
        """ Returns the type name of the `Field` (read-only)."""
        return self.item_type.name.capitalize() + str(self.bit_size)

    @property
    def value(self) -> Any:
        """ Field value."""
        return self._value

    @value.setter
    def value(self, x: Any) -> None:
        self._value = x

    @staticmethod
    def is_bit() -> bool:
        """ Returns ``False``."""
        return False

    @staticmethod
    def is_bool() -> bool:
        """ Returns ``False``."""
        return False

    @staticmethod
    def is_decimal() -> bool:
        """ Returns ``False``."""
        return False

    @staticmethod
    def is_float() -> bool:
        """ Returns ``False``."""
        return False

    @staticmethod
    def is_pointer() -> bool:
        """ Returns ``False``."""
        return False

    @staticmethod
    def is_stream() -> bool:
        """ Returns ``False``."""
        return False

    @staticmethod
    def is_string() -> bool:
        """ Returns ``False``."""
        return False

    @abc.abstractmethod
    @byte_order_option()
    def unpack(self,
               buffer: bytes = bytes(),
               index: Index = Index(),
               **options: Any) -> Any:
        """ Unpacks the field :attr:`value` from the *buffer* at the given
        *index* in accordance with the decoding *byte order* for the
        de-serialization and the :attr:`byte_order` and :attr:`alignment`
        of the `Field`.

        The specific decoding :attr:`byte_order` of the `Field` overrules the
        decoding *byte order* for the de-serialization.

        Returns the deserialized field :attr:`value`.

        :param bytes buffer: byte stream to unpack from.
        :param Index index: current read :class:`Index` within the *buffer*.
        :keyword byte_order: decoding byte order for the de-serialization.
        :type byte_order: Byteorder|Literal['auto', 'big', 'little']

        .. note:: This abstract method must be implemented by a derived class.
        """
        # Returns the deserialized field value.
        return None

    @abc.abstractmethod
    @byte_order_option()
    def pack(self,
             buffer: bytearray = bytearray(),
             **options: Any) -> bytes:
        """ Packs the field :attr:`value` to the *buffer* at the given *index*
        in accordance with the encoding *byte order* for the serialization and
        the :attr:`byte_order` and :attr:`alignment` of the `Field`.

        The specific encoding :attr:`byte_order` of the `Field` overrules the
        encoding *byte order* for the serialization.

        Returns the :class:`bytes` for the serialized field :attr:`value`.

        :param bytearray buffer: byte stream to pack to.
        :keyword byte_order: encoding byte order for the
            serialization.
        :type byte_order: Byteorder|Litreal['auto', 'big', 'little']

        .. note:: This abstract method must be implemented by a derived class.
        """
        # Returns the byte serialized field value.
        return bytes()

    @byte_order_option()
    @nested_option()
    def deserialize(self,
                    buffer: bytes = bytes(),
                    index: Index = Index(),
                    **options: Any) -> Index:
        """ De-serializes the `Field` from the byte *buffer* starting at the
        beginning of the *buffer* or with the given *index* by unpacking the
        bytes to the :attr:`value` of the `Field` in accordance with the
        decoding *byte order* for the de-serialization and the decoding
        :attr:`byte_order` of the `Field`.

        The specific decoding :attr:`byte_order` of the `Field` overrules the
        decoding *byte order* for the de-serialization.

        Returns the :class:`Index` of the *buffer* after the `Field`.

        Optional the de-serialization of the referenced :attr:`~Pointer.data`
        object of a :class:`Pointer` field can be enabled.

        :param bytes buffer: byte stream to de-serialize from.
        :param Index index: current read :class:`Index` within the *buffer* to
            de-serialize.
        :keyword byte_order: decoding byte order for the de-serialization.
        :type byte_order: Byteorder|Literal['auto', 'big', 'little']
        :keyword bool nested: if :data:`True` a :class:`Pointer` field
            de-serialize its referenced :attr:`~Pointer.data` object as well
            (chained method call).
            Each :class:`Pointer` field uses for the de-serialization of its
            referenced :attr:`~Pointer.data` object its own
            :attr:`~Pointer.bytestream`.
        """
        self.index = index
        self._value = self.unpack(buffer, index, **options)
        return self.index_field(index)

    @byte_order_option()
    @nested_option()
    def serialize(self,
                  buffer: bytearray = bytearray(),
                  index: Index = Index(),
                  **options: Any) -> Index:
        """ Serializes the `Field` to the byte *buffer* starting at the beginning
        of the *buffer* or with the given *index* by packing the :attr:`value`
        of the `Field` to the byte *buffer* in accordance with the encoding
        *byte order* for the serialization and the encoding :attr:`byte_order`
        of the `Field`.

        The specific encoding :attr:`byte_order` of the `Field` overrules the
        encoding *byte order* for the serialization.

        Returns the :class:`Index` of the *buffer* after the `Field`.

        Optional the serialization of the referenced :attr:`~Pointer.data` object
        of a :class:`Pointer` field can be enabled.

        :param bytearray buffer: byte stream to serialize to.
        :param Index index: current write :class:`Index` of the *buffer*.
        :keyword byte_order: encoding byte order for the serialization.
        :type byte_order: Byteorder|Literal['auto', 'big', 'little']
        :keyword bool nested: if :data:`True` a :class:`Pointer` field serializes
            its referenced :attr:`~Pointer.data` object as well
            (chained method call).
            Each :class:`Pointer` field uses for the encoding of its referenced
            :attr:`~Pointer.data` object its own :attr:`~Pointer.bytestream`.
        """
        self.index = index
        buffer += self.pack(buffer, **options)
        return self.index_field(index)

    def index_field(self,
                    index: Index = Index()) -> Index:
        """ Indexes the `Field` with the given *index* und returns the
        :class:`Index` after the `Field`.

        :param Index index: start :class:`Index` for the `Field`.
        """
        # Set field index
        # Note: Updates the field alignment offset as well
        self.index = index

        # Bit offset for the next field
        byte, bit, address, base, update = index
        bit += self.bit_size

        # Field group size
        group_size, offset = divmod(bit, 8)

        # End of field group?
        if self.alignment.byte_size == group_size:
            # Bad aligned field group?
            if offset != 0:
                raise FieldGroupSizeError(self, index,
                                          Alignment(group_size + 1,
                                                    self.alignment.bit_offset))
            else:
                # Move byte index for the next field group
                byte += self.alignment.byte_size
                # Reset bit offset for the next field group
                bit = 0
                # Move address for the next field group
                address += self.alignment.byte_size
        # Index for the next field
        return Index(byte, bit, address, base, update)

    @nested_option(True)
    def describe(self,
                 name: str = str(),
                 **options: Any) -> dict[str, Any]:
        """ Returns the **metadata** of a `Field` as a :class:`dict`.

        .. code-block:: python

            metadata = {
                'address': self.index.address,
                'alignment': [self.alignment.byte_size, self.alignment.bit_offset],
                'class': self.name,
                'index': [self.index.byte, self.index.bit],
                'name': name if name else self.name,
                'order': self.byte_order.value,
                'size': self.bit_size,
                'type': Field.item_type.name,
                'value': self.value
            }

        :param str name: optional name for the `Field`.
            Fallback is the class name.
        :keyword bool nested: if :data:`True` a :class:`Pointer` field lists its
            referenced :attr:`~Pointer.data` object fields as well
            (chained method call). Default is :data:`True`.
        """
        metadata = {
            'address': self.index.address,
            'alignment': list(self.alignment),
            'class': self.name,
            'order': self.byte_order.value,
            'index': [self.index.byte, self.index.bit],
            'name': name if name else self.name,
            'size': self.bit_size,
            'type': Field.item_type.name,
            'value': self.value
        }
        return dict(sorted(metadata.items()))


class Stream(Field):
    """ The :class:`Stream` field is a :class:`Field` with a variable *size*,
    and returns its field :attr:`value` as a hexadecimal string.

    Internally a `Stream` field uses a :class:`bytes` class to store the
    data of its field :attr:`value`.

    A `Stream` field is:

    - *containable*: ``item`` in ``self`` returns :data:`True` if *item* is part
      of the `Stream` field.
    - *sized*: ``len(self)`` returns the length of the `Stream` field.
    - *indexable* ``self[index]`` returns the *byte* at the *index*
      of the `Stream` field.
    - *iterable* ``iter(self)`` iterates over the bytes of the `Stream`
      field.

    :param int capacity: is the *capacity* of the `Stream` field in bytes.

    Example:

    >>> stream = Stream()
    >>> stream.is_stream()
    True
    >>> stream.name
    'Stream'
    >>> stream.alignment
    Alignment(byte_size=0, bit_offset=0)
    >>> stream.byte_order
    Byteorder.auto = 'auto'
    >>> stream.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> stream.index_field()
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> stream.bit_size
    0
    >>> len(stream)
    0
    >>> bool(stream)
    False
    >>> stream.value
    ''
    >>> bytes(stream)
    b''
    >>> stream.hex()
    ''
    >>> stream.resize(10)
    >>> stream.name
    'Stream10'
    >>> stream.alignment
    Alignment(byte_size=10, bit_offset=0)
    >>> stream.bit_size
    80
    >>> stream.index_field()
    Index(byte=10, bit=0, address=10, base_address=0, update=False)
    >>> stream.value
    '00000000000000000000'
    >>> stream.value = '0102030405'
    >>> stream.value
    '01020304050000000000'
    >>> stream.resize(15)
    >>> stream.value
    '010203040500000000000000000000'
    >>> stream.resize(10)
    >>> stream.value = '0102030405060708090a0b0c'
    >>> stream.value
    '0102030405060708090a'
    >>> stream.hex()
    '0102030405060708090a'
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
    >>> stream[5:].hex()  # converts to bytes
    '060708090a'
    >>> stream.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Stream

    def __init__(self, capacity: int = 0) -> None:
        super().__init__()
        # Field value
        self._value: bytes = bytes()
        # Stream size
        self.resize(capacity)

    def __bytes__(self) -> bytes:
        return bytes(self._value)

    def __contains__(self, key: int | bytes) -> bool:
        return key in self._value

    def __len__(self) -> int:
        return len(self._value)

    def __getitem__(self, key: int | slice) -> int | bytes:
        return self._value[key]

    def __iter__(self) -> Iterator[int]:
        return iter(self._value)

    @property
    def name(self) -> str:
        """ Returns the type name of the `Stream` field (read-only)."""
        capacity = len(self)
        if capacity > 0:
            return self.item_type.name.capitalize() + str(capacity)
        else:
            return self.item_type.name.capitalize()

    @property
    def value(self) -> str:
        """ Field value as a lowercase hexadecimal encoded string."""
        return self._value.hex()

    @value.setter
    def value(self, stream: str | bytes | bytearray) -> None:
        self._value = self.to_stream(stream, encoding='hex')

    def hex(self) -> str:
        """ Returns a string containing two hexadecimal digits for each byte
        in the :attr:`value` of the `Stream` field.
        """
        return self._value.hex()

    @staticmethod
    def is_stream() -> bool:
        """ Returns :data:`True`."""
        return True

    def to_stream(self,
                  value: str | bytes | bytearray,
                  encoding: Literal['ascii', 'hex'] = 'hex') -> bytes:
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
    def unpack(self,
               buffer: bytes = bytes(),
               index: Index = Index(),
               **options: Any) -> bytes:
        # Bad placed field
        if index.bit:
            raise FieldIndexError(self, index)

        # Content of the buffer mapped by the field
        offset = self.index.byte
        size = offset + len(self)
        bytestream = buffer[offset:size]
        bytestream += b'\x00' * max(len(self) - len(bytestream), 0)
        return bytestream

    @byte_order_option()
    def pack(self,
             buffer: bytearray = bytearray(),
             **options: Any) -> bytes:
        # Bad placed field
        if self.index.bit:
            raise FieldIndexError(self, self.index)
        return self._value

    def resize(self, capacity: int) -> None:
        """ Re-sizes the `Stream` field by appending zero bytes or
        removing bytes from the end.

        :param int capacity: `Stream` capacity in number of bytes.
        """
        count = max(int(capacity), 0) - len(self)

        if count == 0:
            pass
        elif -count == len(self):
            self._value = bytes()
        elif count > 0:
            self._value += b'\x00' * count
        else:
            self._value = self._value[:count]
        capacity = len(self)
        self._bit_size = capacity * 8
        self._align_to_byte_size = capacity


class String(Stream):
    """ The :class:`String` field is a :class:`Stream` field with a variable
    *size*, and returns its field :attr:`value` as a zero-terminated ASCII
    string.

    A `String` field is:

    - *containable*: ``item`` in ``self`` returns :data:`True` if *item* is part
      of the `String` field.
    - *sized*: ``len(self)`` returns the length of the `String` field.
    - *indexable* ``self[index]`` returns the *byte* at the *index*
      of the `String` field.
    - *iterable* ``iter(self)`` iterates over the bytes of the `String`
      field.

    :param int capacity: is the *capacity* of the `String` field in bytes.

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
    Alignment(byte_size=0, bit_offset=0)
    >>> string.byte_order
    Byteorder.auto = 'auto'
    >>> string.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> string.index_field()
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> string.bit_size
    0
    >>> len(string)
    0
    >>> bool(string)
    False
    >>> string.value
    ''
    >>> bytes(string)
    b''
    >>> string.hex()
    ''
    >>> string.resize(10)
    >>> string.name
    'String10'
    >>> string.alignment
    Alignment(byte_size=10, bit_offset=0)
    >>> string.bit_size
    80
    >>> string.index_field()
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
    >>> string.hex()
    '4b6f6e466f6f20697320'
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
    >>> string.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.String

    @property
    def value(self) -> str:
        """ Field value as an ascii encoded string."""
        length = self._value.find(b'\x00')
        if length >= 0:
            return self._value[:length].decode('ascii')
        else:
            return self._value.decode('ascii')

    @value.setter
    def value(self, string: str | bytes | bytearray) -> None:
        self._value = self.to_stream(string, encoding='ascii')

    @staticmethod
    def is_string() -> bool:
        """ Returns :data:`True`."""
        return True

    def is_terminated(self) -> bool:
        """ Returns :data:`True` if the `String` field is zero-terminated."""
        return self._value.find(b'\x00') >= 0


class Float(Field):
    """ The :class:`Float` field is a :class:`Field` with a fix *size* of four
    bytes, and returns its field :attr:`value` as a single precision float.

    Internally a `Float` field uses a :class:`float` class to store the
    data of its field :attr:`~Float.value`.

    A `Float` field extends the :attr:`~Field.metadata` of a :class:`Field`
    with a ``'max'`` and ``'min'`` key for its maximum and minimum possible
    field :attr:`.value`.

    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Float` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> real = Float()
    >>> real.is_float()
    True
    >>> real.name
    'Float32'
    >>> real.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> real.byte_order
    Byteorder.auto = 'auto'
    >>> real.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> real.index_field()
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
    >>> bytes(real)
    b'\\x00\\x00\\x00\\x00'
    >>> int(real)
    0
    >>> float(real)
    0.0
    >>> bool(real)
    False
    >>> real.value = 0x10
    >>> real.value
    16.0
    >>> real.value = -3.4028234663852887e+38
    >>> real.value
    -3.4028234663852886e+38
    >>> real.value = 3.4028234663852887e+38
    >>> real.value
    3.4028234663852886e+38
    >>> real.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Float

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=32, align_to=4, byte_order=byte_order)
        # Field value
        self._value: float = float()

    def __bytes__(self) -> bytes:
        if self.byte_order is Byteorder.big:
            return struct.pack('>f', self._value)
        elif self.byte_order is Byteorder.little:
            return struct.pack('<f', self._value)
        elif BYTEORDER is Byteorder.big:
            return struct.pack('>f', self._value)
        else:
            return struct.pack('<f', self._value)

    def __bool__(self) -> bool:
        return bool(self._value)

    def __int__(self) -> int:
        return int(self._value)

    def __float__(self) -> float:
        return float(self._value)

    @property
    def value(self) -> float:
        """ Field value as a single precision floating-point number."""
        return float(self._value)

    @value.setter
    def value(self, x: int | float | bool) -> None:
        self._value = self.to_float(x)

    @staticmethod
    def is_float() -> bool:
        """ Returns :data:`True`."""
        return True

    def to_float(self, value: int | float | bool) -> float:
        return clamp(float(value), self.min(), self.max())

    @staticmethod
    def epsilon() -> float:
        return 2 ** -24

    @staticmethod
    def smallest() -> float:
        """ Returns the smallest normalized field *value* of the `Float` field."""
        return 2 ** -126

    @staticmethod
    def max() -> float:
        """ Returns the maximal possible field *value* of the `Float` field."""
        return (2 - 2 ** -23) * 2 ** 127

    @staticmethod
    def min() -> float:
        """ Returns the minimal possible field *value* of the `Float` field."""
        return -Float.max()

    @byte_order_option()
    def unpack(self,
               buffer: bytes = bytes(),
               index: Index = Index(),
               **options: Any) -> float:
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
        size = offset + self.alignment.byte_size
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
    def pack(self,
             buffer: bytearray = bytearray(),
             **options: Any) -> bytes:
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

    def describe(self,
                 name: str = str(),
                 **options: Any) -> dict[str, Any]:
        metadata = super().describe(name, **options)
        metadata['max'] = self.max()
        metadata['min'] = self.min()
        return dict(sorted(metadata.items()))


class Double(Field):
    """ The :class:`Double` field is a :class:`Field` with a fix *size* of eight
    bytes, and returns its field :attr:`value` as a double precision float.

    Internally a `Double` field uses a :class:`float` class to store the
    data of its field :attr:`~Float.value`.

    A `Double` field extends the :attr:`~Field.metadata` of a :class:`Field`
    with a ``'max'`` and ``'min'`` key for its maximum and minimum possible
    field :attr:`.value`.

    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Double` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> double = Double()
    >>> double.is_float()
    True
    >>> double.name
    'Double64'
    >>> double.alignment
    Alignment(byte_size=8, bit_offset=0)
    >>> double.byte_order
    Byteorder.auto = 'auto'
    >>> double.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> double.index_field()
    Index(byte=8, bit=0, address=8, base_address=0, update=False)
    >>> double.bit_size
    64
    >>> double.min()
    -1.7976931348623157e+308
    >>> double.max()
    1.7976931348623157e+308
    >>> double.smallest()
    2.2250738585072014e-308
    >>> double.epsilon()
    1.1102230246251565e-16
    >>> double.value
    0.0
    >>> bytes(double)
    b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
    >>> int(double)
    0
    >>> float(double)
    0.0
    >>> bool(double)
    False
    >>> double.value = 0x10
    >>> double.value
    16.0
    >>> double.value = -1.7976931348623158e+308
    >>> double.value
    -1.7976931348623157e+308
    >>> double.value = 1.7976931348623158e+308
    >>> double.value
    1.7976931348623157e+308
    >>> double.describe()
    {'address': 0,
     'alignment': [8, 0],
     'class': 'Double64',
     'index': [0, 0],
     'max': 1.7976931348623157e+308,
     'min': -1.7976931348623157e+308,
     'name': 'Double64',
     'order': 'auto',
     'size': 64,
     'type': 'Field',
     'value': 1.7976931348623157e+308}
    """
    # Item type.
    item_type: ItemClass = ItemClass.Double

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=64, align_to=8, byte_order=byte_order)
        # Field value
        self._value: float = float()

    def __bytes__(self) -> bytes:
        if self.byte_order is Byteorder.big:
            return struct.pack('>d', self._value)
        elif self.byte_order is Byteorder.little:
            return struct.pack('<d', self._value)
        elif BYTEORDER is Byteorder.big:
            return struct.pack('>d', self._value)
        else:
            return struct.pack('<d', self._value)

    def __bool__(self) -> bool:
        return bool(self._value)

    def __int__(self) -> int:
        return int(self._value)

    def __float__(self) -> float:
        return float(self._value)

    @property
    def value(self) -> float:
        """ Field value as a double precision floating-point number."""
        return float(self._value)

    @value.setter
    def value(self, x: int | float | bool) -> None:
        self._value = self.to_float(x)

    @staticmethod
    def is_float() -> bool:
        """ Returns :data:`True`."""
        return True

    def to_float(self, value: int | float | bool) -> float:
        return clamp(float(value), self.min(), self.max())

    @staticmethod
    def epsilon() -> float:
        return 2 ** -53

    @staticmethod
    def smallest() -> float:
        """ Returns the smallest normalized field *value* of the `Double` field.
        """
        return 2 ** -1022

    @staticmethod
    def max() -> float:
        """ Returns the maximal possible field *value* of the `Double` field."""
        return (2 - 2 ** -52) * 2 ** 1023

    @staticmethod
    def min() -> float:
        """ Returns the minimal possible field *value* of the `Double` field."""
        return -Double.max()

    @byte_order_option()
    def unpack(self,
               buffer: bytes = bytes(),
               index: Index = Index(),
               **options: Any) -> float:
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
        size = offset + self.alignment.byte_size
        content = buffer[offset:size]

        # Not enough content!
        if len(content) != 8:
            return float()

        # Unpack the content from the buffer
        if byte_order is Byteorder.big:
            return struct.unpack('>d', content)[0]
        else:
            return struct.unpack('<d', content)[0]

    @byte_order_option()
    def pack(self,
             buffer=bytearray(),
             **options: Any) -> bytes:
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
            return struct.pack('>d', self._value)
        else:
            return struct.pack('<d', self._value)

    def describe(self,
                 name: str = str(),
                 **options) -> dict[str, Any]:
        metadata = super().describe(name, **options)
        metadata['max'] = self.max()
        metadata['min'] = self.min()
        return dict(sorted(metadata.items()))


class Decimal(Field):
    """ The :class:`Decimal` field is a :class:`Field` with a variable *size*
    and returns its field :attr:`value` as a decimal number.

    Internally a `Decimal` field uses an :class:`int` class to store the
    data of its field :attr:`value`.

    A `Decimal` field extends the :attr:`~Field.metadata` of a :class:`Field`
    with a ``'max'`` and ``'min'`` key for its maximum and minimum possible
    field :attr:`value` and a ``'signed'`` key to mark the decimal number as
    signed or unsigned.

    :param int bit_size: is the *size* of the `Decimal` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Decimal` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Decimal` field aligns itself
        to the next matching byte size according to the *size* of the
        `Decimal` field.
    :param bool signed: if :data:`True` the `Decimal` field is signed otherwise
        unsigned.
    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Decimal` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> unsigned = Decimal(16)
    >>> unsigned.is_decimal()
    True
    >>> unsigned.name
    'Decimal16'
    >>> unsigned.alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> unsigned.byte_order
    Byteorder.auto = 'auto'
    >>> unsigned.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> unsigned.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unsigned.bit_size
    16
    >>> unsigned.signed
    False
    >>> unsigned.min()
    0
    >>> unsigned.max()
    65535
    >>> unsigned.value
    0
    >>> bytes(unsigned)
    b'\\x00\\x00'
    >>> int(unsigned)
    0
    >>> float(unsigned)
    0.0
    >>> hex(unsigned)
    '0x0'
    >>> bin(unsigned)
    '0b0'
    >>> oct(unsigned)
    '0o0'
    >>> bool(unsigned)
    False
    >>> unsigned.as_signed()
    0
    >>> unsigned.as_unsigned()
    0
    >>> unsigned.deserialize(bytes.fromhex('0080'))
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
    >>> unsigned.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ffff'
    >>> unsigned.describe()
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
    Alignment(byte_size=2, bit_offset=0)
    >>> signed.byte_order
    Byteorder.auto = 'auto'
    >>> signed.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> signed.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> signed.bit_size
    16
    >>> signed.signed
    True
    >>> signed.min()
    -32768
    >>> signed.max()
    32767
    >>> signed.value
    0
    >>> bytes(signed)
    b'\\x00\\x00'
    >>> int(signed)
    0
    >>> float(signed)
    0.0
    >>> hex(signed)
    '0x0'
    >>> bin(signed)
    '0b0'
    >>> oct(signed)
    '0o0'
    >>> bool(signed)
    False
    >>> signed.deserialize(bytes.fromhex('00c0'))
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
    >>> signed.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ff7f'
    >>> signed.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Decimal

    def __init__(self,
                 bit_size: int,
                 align_to: int | None = None,
                 signed: bool = False,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(byte_order=byte_order)
        # Field signed?
        self._signed = bool(signed)
        # Field alignment, Field bit size
        if align_to:
            self._set_alignment(group_size=align_to)
            self._set_bit_size(bit_size)
        else:
            self._set_bit_size(bit_size, auto_align=True)
        # Field value
        self._value: int = int()

    def __bytes__(self) -> bytes:
        size, offset = self.alignment
        value = self.as_unsigned() << offset
        if self.byte_order in (Byteorder.big, Byteorder.little):
            return value.to_bytes(size, self.byte_order.value)
        else:
            return value.to_bytes(size, BYTEORDER.value)

    def __bool__(self) -> bool:
        return bool(self._value)

    def __int__(self) -> int:
        return int(self._value)

    def __index__(self) -> int:
        return int(self._value)

    def __float__(self) -> float:
        return float(self._value)

    @property
    def value(self) -> int:
        """ Field value as a decimal number."""
        return int(self._value)

    @value.setter
    def value(self, x: str | int | float | bool) -> None:
        self._value = self.to_decimal(x)

    @property
    def signed(self) -> bool:
        """ Returns :data:`True` if the `Decimal` field is signed."""
        return self._signed

    @signed.setter
    def signed(self, value: bool) -> None:
        self._signed = bool(value)
        self._value = self._cast(self._value,
                                 self.min(), self.max(),
                                 self._signed)

    @staticmethod
    def is_decimal() -> bool:
        """ Returns :data:`True`."""
        return True

    def to_decimal(self,
                   value: str | int | float | bool,
                   encoding: Literal['ascii'] | None = None) -> int:
        if isinstance(value, str):
            if encoding is None:
                decimal = int(value, 0)
            elif encoding == 'ascii':
                decimal = ord(value[:1])
            else:
                raise FieldValueEncodingError(self, self.index, encoding)
        else:
            decimal = int(value)
        return clamp(decimal, self.min(), self.max())

    def _set_alignment(self,
                       group_size: int,
                       bit_offset: int = 0,
                       auto_align: bool = False) -> None:
        """ Sets the alignment of the ``Decimal`` field.

        :param int group_size: size of the aligned `Field` group in bytes,
            can be between ``1`` and ``8``.
        :param int bit_offset: bit offset of the `Decimal` field within the
            aligned `Field` group, can be between ``0`` and ``63``.
        :param bool auto_align: if :data:`True` the `Decimal` field aligns itself
            to the next matching byte size according to the *size* of the
            `Decimal` field.
        """
        # Field alignment offset
        field_offset = int(bit_offset)

        # Auto alignment
        if auto_align:
            # Field alignment size
            field_size, bit_offset = divmod(field_offset, 8)
            if bit_offset != 0:
                field_size += 1
            field_size = max(field_size, 1)
        # No auto alignment
        else:
            # Field alignment size
            field_size = int(group_size)

        # Field alignment
        alignment = Alignment(field_size, field_offset)

        # Invalid field alignment size
        if field_size not in range(1, 8):
            raise FieldAlignmentError(self, self.index, alignment)

        # Invalid field alignment offset
        if not (0 <= field_offset <= 63):
            raise FieldAlignmentError(self, self.index, alignment)

        # Invalid field alignment
        if field_offset >= field_size * 8:
            raise FieldAlignmentError(self, self.index, alignment)

        # Set field alignment
        self._align_to_byte_size = alignment.byte_size
        self._align_to_bit_offset = alignment.bit_offset

    def _set_bit_size(self,
                      size: int,
                      step: int = 1,
                      auto_align: bool = False) -> None:
        """ Sets the *size* of the `Decimal` field.

        :param int size: is the *size* of the `Decimal` field in bits,
            can be between ``1`` and ``64``.
        :param int step: is the minimal required step *size* for the `Decimal`
            field in bits.
        :param bool auto_align: if :data:`True` the `Decimal` field aligns itself
            to the next matching byte size according to the *size* of the
            `Decimal` field.
        """
        # Field size
        bit_size = int(size)

        # Invalid field size
        if bit_size % step != 0 or not (1 <= bit_size <= 64):
            raise FieldSizeError(self, self.index, bit_size)

        # Field group size
        group_size, offset = divmod(bit_size, 8)
        # Auto alignment
        if auto_align:
            if offset != 0:
                self._align_to_byte_size = group_size + 1
            else:
                self._align_to_byte_size = group_size
        # Invalid field alignment
        elif group_size > self.alignment.byte_size:
            raise FieldAlignmentError(self, self.index,
                                      Alignment(group_size,
                                                self.alignment.bit_offset))
        # Set field size
        self._bit_size = bit_size

    def _cast(self,
              value: int,
              minimum: int,
              maximum: int,
              signed: bool) -> int:
        # Sign conversion
        if minimum <= value <= maximum:
            return value
        elif signed:
            return value | ~self.bit_mask()
        else:
            return value & self.bit_mask()

    def _max(self, signed: bool) -> int:
        # Maximal possible field value
        if signed:
            return 2 ** (self._bit_size - 1) - 1
        else:
            return 2 ** self._bit_size - 1

    def _min(self, signed: bool) -> int:
        # Minimal possible field value
        if signed:
            return -2 ** (self._bit_size - 1)
        else:
            return 0

    def bit_mask(self) -> int:
        return 2 ** self._bit_size - 1

    def max(self) -> int:
        """ Returns the maximal possible field *value* of the `Decimal` field.
        """
        return self._max(self._signed)

    def min(self) -> int:
        """ Returns the minimal possible field *value* of the `Decimal` field.
        """
        return self._min(self._signed)

    def as_unsigned(self) -> int:
        """ Returns the field *value* of the `Decimal` field
        as an unsigned integer.
        """
        return self._cast(self._value,
                          self._min(False), self._max(False),
                          False)

    def as_signed(self) -> int:
        """ Returns the field *value* of the `Decimal` field
        as a signed integer.
        """
        return self._cast(self._value,
                          self._min(True), self._max(True),
                          True)

    @byte_order_option()
    def unpack(self,
               buffer: bytes = bytes(),
               index: Index = Index(),
               **options: Any) -> int:
        # Content of the buffer mapped by the field group
        offset = index.byte
        size = offset + self.alignment.byte_size
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
            value = int.from_bytes(value.to_bytes(field_size,
                                                  byte_order.value),
                                   self.byte_order.value)

        # Limit field value
        if value > self.max():
            value |= ~self.bit_mask()
        return value

    @byte_order_option()
    def pack(self,
             buffer: bytearray = bytearray(),
             **options: Any) -> bytes:
        # Field value
        value = clamp(self._value, self.min(), self.max())
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
            value = int.from_bytes(value.to_bytes(field_size,
                                                  self.byte_order.value),
                                   byte_order.value)

        # Shift the field value to its field group offset
        value <<= self.index.bit

        # Content for the buffer mapped by the field group
        offset = self.index.byte
        size = offset + self.alignment.byte_size
        if len(buffer) == size:
            # Map the field value into the existing field group content of the buffer
            view = memoryview(buffer)
            value |= int.from_bytes(buffer[offset:size], byte_order.value)
            view[offset:size] = value.to_bytes(self.alignment.byte_size,
                                               byte_order.value)
            return bytes()
        else:
            # Extent the buffer with the field group content and the field value
            return value.to_bytes(self.alignment.byte_size, byte_order.value)

    def describe(self,
                 name: str = str(),
                 **options: Any) -> dict[str, Any]:
        metadata = super().describe(name, **options)
        metadata['max'] = self.max()
        metadata['min'] = self.min()
        metadata['signed'] = self.signed
        return dict(sorted(metadata.items()))


class Bit(Decimal):
    """ The :class:`Bit` field is an unsigned :class:`Decimal` with a *size* of
    one bit, and returns its field :attr:`value` as an unsigned integer number.

    :param int number: is the bit offset of the `Bit` field within the
        aligned bytes, can be between ``0`` and ``63``.
    :param int|None align_to: aligns the `Bit` field to the number of bytes,
        can be between ``1`` and ``8``.

    Example:

    >>> bit = Bit(0)
    >>> bit.is_decimal()
    True
    >>> bit.is_bit()
    True
    >>> bit.name
    'Bit'
    >>> bit.alignment
    Alignment(byte_size=1, bit_offset=0)
    >>> bit.byte_order
    Byteorder.auto = 'auto'
    >>> bit.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> bit.index_field()
    Index(byte=0, bit=1, address=0, base_address=0, update=False)
    >>> bit.bit_size
    1
    >>> bit.signed
    False
    >>> bit.min()
    0
    >>> bit.max()
    1
    >>> bit.value
    0
    >>> bit.signed
    False
    >>> bit.value
    0
    >>> bytes(bit)
    b'\\x00'
    >>> int(bit)
    0
    >>> float(bit)
    0.0
    >>> hex(bit)
    '0x0'
    >>> bin(bit)
    '0b0'
    >>> oct(bit)
    '0o0'
    >>> bool(bit)
    False
    >>> bit.as_signed()
    0
    >>> bit.as_unsigned()
    0
    >>> bit.deserialize(bytes.fromhex('01'))
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
    >>> bit.serialize(bytestream)
    Index(byte=0, bit=1, address=0, base_address=0, update=False)
    >>> bytestream.hex()
    '01'
    >>> bit.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Bit

    def __init__(self,
                 number: int,
                 align_to: int | None = None) -> None:
        super().__init__(bit_size=1, align_to=align_to)
        # Field alignment
        if align_to:
            self._set_alignment(group_size=align_to,
                                bit_offset=number)
        else:
            self._set_alignment(group_size=0,
                                bit_offset=number,
                                auto_align=True)

    @property
    def name(self) -> str:
        """ Returns the type name of the `Bit` field (read-only)."""
        return self.item_type.name.capitalize()

    @staticmethod
    def is_bit() -> bool:
        """ Returns :data:`True`."""
        return True


class Byte(Decimal):
    """ The :class:`Byte` field is an unsigned :class:`Decimal` field with a
    *size* of one byte, and returns its field :attr:`value` as a lowercase
    hexadecimal string prefixed with ``0x``.

    :param int|None align_to: aligns the `Byte` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Byte` field aligns itself
        to the next matching byte size according to the *size* of the
        `Byte` field.

    Example:

    >>> byte = Byte()
    >>> byte.is_decimal()
    True
    >>> byte.name
    'Byte'
    >>> byte.alignment
    Alignment(byte_size=1, bit_offset=0)
    >>> byte.byte_order
    Byteorder.auto = 'auto'
    >>> byte.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> byte.index_field()
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> byte.bit_size
    8
    >>> byte.signed
    False
    >>> byte.min()
    0
    >>> byte.max()
    255
    >>> byte.value
    '0x0'
    >>> bytes(byte)
    b'\\x00'
    >>> int(byte)
    0
    >>> float(byte)
    0.0
    >>> hex(byte)
    '0x0'
    >>> bin(byte)
    '0b0'
    >>> oct(byte)
    '0o0'
    >>> bool(byte)
    False
    >>> byte.as_signed()
    0
    >>> byte.as_unsigned()
    0
    >>> byte.deserialize(bytes.fromhex('20'))
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
    >>> byte.serialize(bytestream)
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> bytestream.hex()
    'ff'
    >>> byte.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Byte

    def __init__(self,
                 align_to: int | None = None) -> None:
        super().__init__(bit_size=8, align_to=align_to)

    @property
    def name(self) -> str:
        """ Returns the type name of the `Byte` field (read-only)."""
        return self.item_type.name.capitalize()

    @property
    def value(self) -> str:
        """ Field value as a lowercase hexadecimal string prefixed with ``0x``.
        """
        return hex(self._value)

    @value.setter
    def value(self, x: str | int | float | bool) -> None:
        self._value = self.to_decimal(x)


class Char(Decimal):
    """ The :class:`Char` field is an unsigned :class:`Decimal` field with a
    *size* of one byte, and returns its field :attr:`value` as a unicode string
    character.

    :param int|None align_to: aligns the `Char` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Char` field aligns itself
        to the next matching byte size according to the *size* of the
        `Char` field.

    Example:

    >>> char = Char()
    >>> char.is_decimal()
    True
    >>> char.name
    'Char'
    >>> char.alignment
    Alignment(byte_size=1, bit_offset=0)
    >>> char.byte_order
    Byteorder.auto = 'auto'
    >>> char.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> char.index_field()
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> char.bit_size
    8
    >>> char.signed
    False
    >>> char.min()
    0
    >>> char.max()
    255
    >>> char.value
    '\\x00'
    >>> bytes(char)
    b'\\x00'
    >>> ord(char.value)
    0
    >>> int(char)
    0
    >>> float(char)
    0.0
    >>> hex(char)
    '0x0'
    >>> bin(char)
    '0b0'
    >>> oct(char)
    '0o0'
    >>> bool(char)
    False
    >>> char.as_signed()
    0
    >>> char.as_unsigned()
    0
    >>> char.deserialize(bytes.fromhex('41'))
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
    >>> char.serialize(bytestream)
    Index(byte=1, bit=0, address=1, base_address=0, update=False)
    >>> bytestream.hex()
    '46'
    >>> char.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Char

    def __init__(self,
                 align_to: int | None = None) -> None:
        super().__init__(bit_size=8, align_to=align_to)

    @property
    def name(self) -> str:
        """ Returns the type name of the `Char` field (read-only)."""
        return self.item_type.name.capitalize()

    @property
    def value(self) -> str:
        """ Field value as a unicode string character."""
        return chr(self._value)

    @value.setter
    def value(self, x: str | int | float) -> None:
        self._value = self.to_decimal(x, encoding='ascii')


class Signed(Decimal):
    """ The :class:`Signed` field is a signed :class:`Decimal` field with a
    variable *size*, and returns its field :attr:`value` as a signed integer
    number.

    :param int bit_size: is the *size* of the `Signed` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Signed` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Signed` field aligns itself
        to the next matching byte size according to the *size* of the
        `Signed` field.
    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Signed` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> signed = Signed(16)
    >>> signed.is_decimal()
    True
    >>> signed.name
    'Signed16'
    >>> signed.alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> signed.byte_order
    Byteorder.auto = 'auto'
    >>> signed.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> signed.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> signed.bit_size
    16
    >>> signed.signed
    True
    >>> signed.min()
    -32768
    >>> signed.max()
    32767
    >>> signed.value
    0
    >>> bytes(signed)
    b'\\x00\\x00'
    >>> int(signed)
    0
    >>> float(signed)
    0.0
    >>> hex(signed)
    '0x0'
    >>> bin(signed)
    '0b0'
    >>> oct(signed)
    '0o0'
    >>> bool(signed)
    False
    >>> signed.as_signed()
    0
    >>> signed.as_unsigned()
    0
    >>> signed.deserialize(bytes.fromhex('00c0'))
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
    >>> signed.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ff7f'
    >>> signed.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Signed

    def __init__(self,
                 bit_size: int,
                 align_to: int | None = None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size, align_to, True, byte_order)


class Unsigned(Decimal):
    """ The :class:`Unsigned` field is an unsigned :class:`Decimal` field with
    a variable *size*, and returns its field :attr:`value` as a lowercase
    hexadecimal string prefixed with ``0x``.

    :param int bit_size: is the *size* of the `Unsigned` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Unsigned` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Unsigned` field aligns itself
        to the next matching byte size according to the *size* of the
        `Unsigned` field.
    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Unsigned` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> unsigned = Unsigned(16)
    >>> unsigned.is_decimal()
    True
    >>> unsigned.name
    'Unsigned16'
    >>> unsigned.alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> unsigned.byte_order
    Byteorder.auto = 'auto'
    >>> unsigned.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> unsigned.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unsigned.bit_size
    16
    >>> unsigned.signed
    False
    >>> unsigned.min()
    0
    >>> unsigned.max()
    65535
    >>> unsigned.value
    '0x0'
    >>> bytes(unsigned)
    b'\\x00\\x00'
    >>> int(unsigned)
    0
    >>> float(unsigned)
    0.0
    >>> hex(unsigned)
    '0x0'
    >>> bin(unsigned)
    '0b0'
    >>> oct(unsigned)
    '0o0'
    >>> bool(unsigned)
    False
    >>> unsigned.as_signed()
    0
    >>> unsigned.as_unsigned()
    0
    >>> unsigned.deserialize(bytes.fromhex('00c0'))
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
    >>> unsigned.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ffff'
    >>> unsigned.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Unsigned

    def __init__(self,
                 bit_size: int,
                 align_to: int | None = None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size, align_to, False, byte_order)

    @property
    def value(self) -> str:
        """ Field value as a lowercase hexadecimal string prefixed with ``0x``.
        """
        return hex(self._value)

    @value.setter
    def value(self, x: str | int | float | bool) -> None:
        self._value = self.to_decimal(x)


class Bitset(Decimal):
    """ The :class:`Bitset` field is an unsigned :class:`Decimal` field with a
    variable *size* and returns its field :attr:`value` as a binary string
    prefixed with ``0b``.

    :param int bit_size: is the *size* of the `Bitset` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Bitset` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Bitset` field aligns itself
        to the next matching byte size according to the *size* of the
        `Bitset` field.
    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Bitset` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> bitset = Bitset(16)
    >>> bitset.is_decimal()
    True
    >>> bitset.name
    'Bitset16'
    >>> bitset.alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> bitset.byte_order
    Byteorder.auto = 'auto'
    >>> bitset.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> bitset.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bitset.bit_size
    16
    >>> bitset.signed
    False
    >>> bitset.min()
    0
    >>> bitset.max()
    65535
    >>> bitset.value
    '0b0000000000000000'
    >>> bytes(bitset)
    b'\\x00\\x00'
    >>> int(bitset)
    0
    >>> float(bitset)
    0.0
    >>> hex(bitset)
    '0x0'
    >>> bin(bitset)
    '0b0'
    >>> oct(bitset)
    '0o0'
    >>> bool(bitset)
    False
    >>> bitset.as_signed()
    0
    >>> bitset.as_unsigned()
    0
    >>> bitset.deserialize(bytes.fromhex('f00f'))
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
    >>> bitset.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ffff'
    >>> bitset.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Bitset

    def __init__(self,
                 bit_size: int,
                 align_to: int | None = None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size, align_to, False, byte_order)

    @property
    def value(self) -> str:
        """ Field value as a binary string prefixed with ``0b``."""
        return f"{self._value:#0{self.bit_size + 2}b}"

    @value.setter
    def value(self, x: str | int | float | bool) -> None:
        self._value = self.to_decimal(x)


class Bool(Decimal):
    """ The :class:`Bool` field is an unsigned :class:`Decimal` field with a
    variable *size*, and returns its field :attr:`value` as a boolean value.

    :param int bit_size: is the *size* of the `Bool` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Bool` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Bool` field aligns itself
        to the next matching byte size according to the *size* of the
        `Bool` field.
    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Bool` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> boolean = Bool(16)
    >>> boolean.is_decimal()
    True
    >>> boolean.is_bool()
    True
    >>> boolean.name
    'Bool16'
    >>> boolean.alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> boolean.byte_order
    Byteorder.auto = 'auto'
    >>> boolean.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> boolean.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> boolean.bit_size
    16
    >>> boolean.signed
    False
    >>> boolean.min()
    0
    >>> boolean.max()
    65535
    >>> boolean.value
    False
    >>> bytes(boolean)
    b'\\x00\\x00'
    >>> int(boolean)
    0
    >>> float(boolean)
    0.0
    >>> hex(boolean)
    '0x0'
    >>> bin(boolean)
    '0b0'
    >>> oct(boolean)
    '0o0'
    >>> bool(boolean)
    False
    >>> boolean.as_signed()
    0
    >>> boolean.as_unsigned()
    0
    >>> boolean.deserialize(bytes.fromhex('0f00'))
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
    >>> boolean.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ffff'
    >>> boolean.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Bool

    def __init__(self,
                 bit_size: int,
                 align_to: int | None = None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size, align_to, False, byte_order)

    @property
    def value(self) -> bool:
        """ Field value as a boolean value, :data:`True` or ``False``."""
        return bool(self._value)

    @value.setter
    def value(self, x: bool | int | float | str) -> None:
        self._value = self.to_decimal(x)

    @staticmethod
    def is_bool() -> bool:
        """ Returns :data:`True`."""
        return True


class Enum(Decimal):
    """ The :class:`Enum` field is an unsigned :class:`Decimal` field with a
    variable *size*, and returns its field :attr:`value` as an unsigned integer
    number.

    If an :class:`Enumeration` is available and a member matches the integer
    number then the member name string is returned otherwise the integer number
    is returned.

    :param int bit_size: is the *size* of the `Enum` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Enum` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Enum` field aligns itself
        to the next matching byte size according to the *size* of the
        `Enum` field.
    :param enumeration: :class:`Enumeration` definition of the `Enum` field.
    :type enumeration: Type[Enumeration]|None
    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Enum` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> enum = Enum(16, enumeration=ItemClass)
    >>> enum.is_decimal()
    True
    >>> enum.name
    'Enum16'
    >>> enum.alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> enum.byte_order
    Byteorder.auto = 'auto'
    >>> enum.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> enum.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> enum.bit_size
    16
    >>> enum.signed
    False
    >>> bytes(enum)
    b'\\x00\\x00'
    >>> enum.min()
    0
    >>> enum.max()
    65535
    >>> enum.value
    0
    >>> int(enum)
    0
    >>> float(enum)
    0.0
    >>> hex(enum)
    '0x0'
    >>> bin(enum)
    '0b0'
    >>> oct(enum)
    '0o0'
    >>> bool(enum)
    False
    >>> enum.as_signed()
    0
    >>> enum.as_unsigned()
    0
    >>> enum.deserialize(bytes.fromhex('2800'))
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
    >>> enum.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ffff'
    >>> enum.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Enum

    def __init__(self,
                 bit_size: int,
                 align_to: int | None = None,
                 enumeration: Type[Enumeration] | None = None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size, align_to, False, byte_order)
        # Field enumeration class
        if enumeration is None:
            self._enum: Type[Enumeration] | None = None
        elif issubclass(enumeration, Enumeration):
            self._enum: Type[Enumeration] | None = enumeration
        else:
            raise EnumTypeError(self, enumeration)

    @property
    def value(self) -> int | str:
        """ Field value as an enum name string.
        Fall back is an unsigned integer number.
        """
        if self._enum and issubclass(self._enum, Enumeration):
            name = self._enum.get_name(self._value)
            if name:
                return name
        return self._value

    @value.setter
    def value(self, x: str | int | Enumeration) -> None:
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
    """ The :class:`Scaled` field is a signed :class:`Decimal` field with a
    variable *size*, and returns its scaled field :attr:`value` as a
    floating-point number.

    The scaled field *value* is:

        ``(unscaled field value / scaling base) * scaling factor``

    The unscaled field *value* is:

        ``(scaled field value / scaling factor) * scaling base``

    The scaling base is:

        ``2 ** (field size - 1) / 2``

    A `Scaled` field extends the :attr:`~Field.metadata` of a :class:`Decimal`
    with a ``'scale'`` key for its scaling factor.

    :param float|int scale: scaling factor of the `Scaled` field.
    :param int bit_size: is the *size* of the `Scaled` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Scaled` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Scaled` field aligns itself
        to the next matching byte size according to the *size* of the
        `Scaled` field.
    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Scaled` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> scaled = Scaled(100, 16)
    >>> scaled.is_decimal()
    True
    >>> scaled.name
    'Scaled16'
    >>> scaled.alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> scaled.byte_order
    Byteorder.auto = 'auto'
    >>> scaled.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> scaled.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> scaled.scale
    100.0
    >>> scaled.scaling_base()
    16384.0
    >>> scaled.bit_size
    16
    >>> scaled.signed
    True
    >>> scaled.min()
    -32768
    >>> scaled.max()
    32767
    >>> scaled.value
    0.0
    >>> bytes(scaled)
    b'\\x00\\x00'
    >>> int(scaled)
    0
    >>> float(scaled)
    0.0
    >>> hex(scaled)
    '0x0'
    >>> bin(scaled)
    '0b0'
    >>> oct(scaled)
    '0o0'
    >>> bool(scaled)
    False
    >>> scaled.as_signed()
    0
    >>> scaled.as_unsigned()
    0
    >>> scaled.deserialize(bytes.fromhex('0040'))
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
    >>> scaled.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ff7f'
    >>> scaled.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Scaled

    def __init__(self,
                 scale: float | int,
                 bit_size: int,
                 align_to: int | None = None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size, align_to, True, byte_order)
        # Field scaling factor
        self._scale: float = float(scale)

    def __float__(self) -> float:
        return self.value

    @property
    def value(self) -> float:
        """ Field value as a floating-point number."""
        return self.as_float(self._value)

    @value.setter
    def value(self, x: float | int) -> None:
        self._value = self.to_scaled(x)

    def as_float(self, value: int) -> float:
        return (value / self.scaling_base()) * self.scale

    def to_scaled(self, value: float | int) -> int:
        return self.to_decimal((float(value) / self.scale) *
                               self.scaling_base())

    @property
    def scale(self) -> float:
        """ Scaling factor of the `Scaled` field."""
        return self._scale

    @scale.setter
    def scale(self, value: float | int) -> None:
        self._scale = float(value)

    def scaling_base(self):
        """ Returns the scaling base of the `Scaled` field."""
        return 2 ** (self.bit_size - 1) / 2

    def describe(self,
                 name: str = str(),
                 **options: Any) -> dict[str, Any]:
        metadata = super().describe(name, **options)
        metadata['scale'] = self.scale
        return dict(sorted(metadata.items()))


class Fraction(Decimal):
    """ The :class:`Fraction` field is an unsigned :class:`Decimal` field with
    a variable *size*, and returns its fractional field :attr:`value` as a
    floating-point number.

    A fractional number is bitwise encoded and has up to three bit parts for
    this task.

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
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Fraction` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Fraction` field aligns itself
        to the next matching byte size according to the *size* of the
        `Fraction` field.
    :param bool signed: if :data:`True` the `Fraction` field is signed otherwise
        unsigned.
    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Fraction` field
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> unipolar = Fraction(2, 16)
    >>> unipolar.is_decimal()
    True
    >>> unipolar.name
    'Fraction2.16'
    >>> unipolar.alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> unipolar.byte_order
    Byteorder.auto = 'auto'
    >>> unipolar.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> unipolar.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unipolar.bit_size
    16
    >>> unipolar.signed
    False
    >>> unipolar.min()
    0
    >>> unipolar.max()
    65535
    >>> unipolar.value
    0.0
    >>> bytes(unipolar)
    b'\\x00\\x00'
    >>> int(unipolar)
    0
    >>> float(unipolar)
    0.0
    >>> hex(unipolar)
    '0x0'
    >>> bin(unipolar)
    '0b0'
    >>> oct(unipolar)
    '0o0'
    >>> bool(unipolar)
    False
    >>> unipolar.as_signed()
    0
    >>> unipolar.as_unsigned()
    0
    >>> unipolar.deserialize(bytes.fromhex('0080'))
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
    >>> unipolar.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ffff'
    >>> unipolar.describe()
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
    Alignment(byte_size=2, bit_offset=0)
    >>> bipolar.byte_order
    Byteorder.auto = 'auto'
    >>> bipolar.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> bipolar.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bipolar.bit_size
    16
    >>> bipolar.signed
    False
    >>> bipolar.min()
    0
    >>> bipolar.max()
    65535
    >>> bipolar.value
    0.0
    >>> bytes(bipolar)
    b'\\x00\\x00'
    >>> int(bipolar)
    0
    >>> float(bipolar)
    0.0
    >>> hex(bipolar)
    '0x0'
    >>> bin(bipolar)
    '0b0'
    >>> oct(bipolar)
    '0o0'
    >>> bool(bipolar)
    False
    >>> bipolar.as_signed()
    0
    >>> bipolar.as_unsigned()
    0
    >>> bipolar.deserialize(bytes.fromhex('0040'))
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
    >>> bipolar.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ff7f'
    >>> bipolar.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Fraction

    def __init__(self,
                 bits_integer: int,
                 bit_size: int,
                 align_to: int | None = None,
                 signed: bool = False,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size, align_to, False, byte_order)
        # Number of bits of the integer part of the fraction number
        self._bits_integer: int = clamp(int(bits_integer), 1, self._bit_size)
        # Fraction number signed?
        if self._bit_size <= 1:
            self._signed_fraction: bool = False
        else:
            self._signed_fraction: bool = bool(signed)

    def __float__(self) -> float:
        return self.value

    @property
    def name(self) -> str:
        """ Returns the type name of the `Fraction` field (read-only)."""
        return (f"{self.item_type.name.capitalize()}"
                f"{self._bits_integer}.{self.bit_size}")

    @property
    def value(self) -> float:
        """ Field value as a floating-point number."""
        return self.as_float(self._value)

    @value.setter
    def value(self, x: float | int) -> None:
        self._value = self.to_fraction(x)

    def as_float(self, value: int) -> float:
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

    def to_fraction(self, value: float | int) -> int:
        normalized = float(value) / 100.0
        bits_fraction = max(self.bit_size - self._bits_integer, 0)
        if self._signed_fraction:
            integer = abs(int(normalized)) << max(bits_fraction, 0)
            fraction = int(
                math.fabs(normalized - int(normalized)) * 2 ** bits_fraction)
            if normalized < 0:
                mask = 2 ** (self.bit_size - 1)
            else:
                mask = 0
            decimal = clamp(integer | fraction, 0, 2 ** (self.bit_size - 1) - 1)
            decimal |= mask
        else:
            normalized = max(normalized, 0)
            integer = int(normalized) << max(bits_fraction, 0)
            fraction = int((normalized - int(normalized)) * 2 ** bits_fraction)
            decimal = clamp(integer | fraction, 0, 2 ** self.bit_size - 1)
        return self.to_decimal(decimal)

    def describe(self,
                 name: str = str(),
                 **options: Any) -> dict[str, Any]:
        metadata = super().describe(name, **options)
        metadata['signed'] = self._signed_fraction
        return dict(sorted(metadata.items()))


class Bipolar(Fraction):
    """ The :class:`Bipolar` field is a signed :class:`Fraction` field with a
    variable *size*, and returns its fractional field :attr:`value` as a
    floating-point number.

    :param int bits_integer: number of bits for the integer part of the
        fraction number, can be between *1* and the *size* of the
        `Bipolar` field.
    :param int bit_size: is the *size* of the `Bipolar` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Bipolar` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Bipolar` field aligns itself
        to the next matching byte size according to the *size* of the
        `Bipolar` field.
    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Bipolar` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> bipolar = Bipolar(2, 16)
    >>> bipolar.is_decimal()
    True
    >>> bipolar.name
    'Bipolar2.16'
    >>> bipolar.alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> bipolar.byte_order
    Byteorder.auto = 'auto'
    >>> bipolar.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> bipolar.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bipolar.bit_size
    16
    >>> bipolar.signed
    False
    >>> bipolar.min()
    0
    >>> bipolar.max()
    65535
    >>> bipolar.value
    0.0
    >>> bytes(bipolar)
    b'\\x00\\x00'
    >>> int(bipolar)
    0
    >>> float(bipolar)
    0.0
    >>> hex(bipolar)
    '0x0'
    >>> bin(bipolar)
    '0b0'
    >>> oct(bipolar)
    '0o0'
    >>> bool(bipolar)
    False
    >>> bipolar.as_signed()
    0
    >>> bipolar.as_unsigned()
    0
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
    >>> bipolar.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ff7f'
    >>> bipolar.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Bipolar

    def __init__(self,
                 bits_integer: int,
                 bit_size: int,
                 align_to: int | None = None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bits_integer, bit_size, align_to, True, byte_order)


class Unipolar(Fraction):
    """ The :class:`Unipolar` field is an unsigned :class:`Fraction` field with
    a variable *size*, and returns its fractional field :attr:`value` as a
    floating-point number.

    :param int bits_integer: number of bits for the integer part of the
        fraction number, can be between *1* and the *size* of the
        `Unipolar` field.
    :param int bit_size: is the *size* of the `Unipolar` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Unipolar` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Unipolar` field aligns itself
        to the next matching byte size according to the *size* of the
        `Unipolar` field.
    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Unipolar` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> unipolar = Unipolar(2, 16)
    >>> unipolar.is_decimal()
    True
    >>> unipolar.name
    'Unipolar2.16'
    >>> unipolar.alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> unipolar.byte_order
    Byteorder.auto = 'auto'
    >>> unipolar.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> unipolar.index_field()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> unipolar.bit_size
    16
    >>> unipolar.signed
    False
    >>> unipolar.min()
    0
    >>> unipolar.max()
    65535
    >>> unipolar.value
    0.0
    >>> bytes(unipolar)
    b'\\x00\\x00'
    >>> int(unipolar)
    0
    >>> float(unipolar)
    0.0
    >>> hex(unipolar)
    '0x0'
    >>> bin(unipolar)
    '0b0'
    >>> oct(unipolar)
    '0o0'
    >>> bool(unipolar)
    False
    >>> unipolar.as_signed()
    0
    >>> unipolar.as_unsigned()
    0
    >>> unipolar.deserialize(bytes.fromhex('0080'))
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
    >>> unipolar.serialize(bytestream)
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> bytestream.hex()
    'ffff'
    >>> unipolar.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Unipolar

    def __init__(self,
                 bits_integer: int,
                 bit_size: int,
                 align_to: int | None = None,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bits_integer, bit_size, align_to, False, byte_order)


class Datetime(Decimal):
    """ The :class:`Datetime` field is an unsigned :class:`Decimal` field with
    a fix *size* of four bytes, and returns its field :attr:`value` as an UTC
    datetime string in the ISO format ``YYYY-mm-dd HH:MM:SS``.

    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `Datetime` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> datetime = Datetime()
    >>> datetime.is_decimal()
    True
    >>> datetime.name
    'Datetime32'
    >>> datetime.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> datetime.byte_order
    Byteorder.auto = 'auto'
    >>> datetime.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> datetime.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> datetime.bit_size
    32
    >>> datetime.signed
    False
    >>> datetime.min()
    0
    >>> datetime.max()
    4294967295
    >>> datetime.value
    '1970-01-01 00:00:00'
    >>> bytes(datetime)
    b'\\x00\\x00\\x00\\x00'
    >>> int(datetime)
    0
    >>> float(datetime)
    0.0
    >>> hex(datetime)
    '0x0'
    >>> bin(datetime)
    '0b0'
    >>> oct(datetime)
    '0o0'
    >>> bool(datetime)
    False
    >>> datetime.as_signed()
    0
    >>> datetime.as_unsigned()
    0
    >>> datetime.deserialize(bytes.fromhex('ffffffff'))
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
    >>> datetime.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> bytestream.hex()
    'ffffffff'
    >>> datetime.describe()
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
    # Item type.
    item_type: ItemClass = ItemClass.Datetime

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=32, byte_order=byte_order)

    @property
    def value(self) -> str:
        """ Field value as an UTC datetime string in the ISO format
        ``YYYY-mm-dd HH:MM:SS``"""
        return str(datetime.datetime.utcfromtimestamp(self._value))

    @value.setter
    def value(self, x: int | str) -> None:
        try:
            self._value = self.to_decimal(x)
        except (TypeError, ValueError):
            self._value = self.to_timestamp(x)

    def to_timestamp(self, value: str) -> int:
        decimal = calendar.timegm(time.strptime(value, "%Y-%m-%d %H:%M:%S"))
        return self.to_decimal(decimal)


class IPv4Address(Decimal):
    """ The :class:`IPv4Address` field is an unsigned :class:`Decimal` field with a fix
    *size* of four bytes and returns its field :attr:`value` as an IPv4 address
    formatted string.

    :param byte_order: byte order used to unpack and pack the :attr:`value`
        of the `IPv4Address` field.
    :type byte_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> ipv4 = IPv4Address()
    >>> ipv4.is_decimal()
    True
    >>> ipv4.name
    'Ipaddress32'
    >>> ipv4.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> ipv4.byte_order
    Byteorder.auto = 'auto'
    >>> ipv4.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> ipv4.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> ipv4.bit_size
    32
    >>> ipv4.signed
    False
    >>> ipv4.min()
    0
    >>> ipv4.max()
    4294967295
    >>> ipv4.value
    '0.0.0.0'
    >>> bytes(ipv4)
    b'\\x00\\x00\\x00\\x00'
    >>> int(ipv4)
    0
    >>> float(ipv4)
    0.0
    >>> hex(ipv4)
    '0x0'
    >>> bin(ipv4)
    '0b0'
    >>> oct(ipv4)
    '0o0'
    >>> bool(ipv4)
    False
    >>> ipv4.as_signed()
    0
    >>> ipv4.as_unsigned()
    0
    >>> ipv4.deserialize(bytes.fromhex('ffffffff'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> ipv4.value
    '255.255.255.255'
    >>> ipv4.value = '192.168.0.0'
    >>> ipv4.value
    '192.168.0.0'
    >>> ipv4.value = '255.255.255.255'
    >>> ipv4.value
    '255.255.255.255'
    >>> bytestream = bytearray()
    >>> bytestream
    bytearray(b'')
    >>> ipv4.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> bytestream.hex()
    'ffffffff'
    >>> ipv4.describe()
    {'address': 0,
     'alignment': [4, 0],
     'class': 'Ipaddress32',
     'index': [0, 0],
     'max': 4294967295,
     'min': 0,
     'name': 'Ipaddress32',
     'order': 'auto',
     'signed': False,
     'size': 32,
     'type': 'Field',
     'value': '255.255.255.255'}
    """
    # Item type.
    item_type: ItemClass = ItemClass.IPAddress

    def __init__(self,
                 byte_order: (Literal['auto', 'big', 'little'] |
                              Byteorder) = 'auto') -> None:
        super().__init__(bit_size=32, byte_order=byte_order)

    @property
    def value(self) -> str:
        """ Field value as an IPv4 address formatted string."""
        return str(ipaddress.IPv4Address(self._value))

    @value.setter
    def value(self, x: str | int) -> None:
        self._value = int(ipaddress.IPv4Address(x))


class Pointer(Decimal, Container):
    """ The :class:`Pointer` field is an unsigned :class:`Decimal` field with a
    *size* of four bytes, and returns its field :attr:`value` as a hexadecimal
    string.

    A `Pointer` field refers absolutely to a :attr:`data` object of a data
    :class:`Provider`.

    The `Pointer` class extends the :class:`Decimal` field with the
    :class:`Container` interface for its referenced :attr:`data` object.

    A `Pointer` field has additional features to **read**, **write**,
    **deserialize**, **serialize** and **view** binary data:

    - **Deserialize** the :attr:`~Field.value` for each :class:`Field`
      in the :attr:`data` object referenced by the `Pointer` field from
      a byte stream via :meth:`deserialize_data`.
    - **Serialize** the :attr:`~Field.value` for each :class:`Field`
      in the :attr:`data` object referenced by the `Pointer` field to a
      byte stream via :meth:`serialize_data`.
    - **Indexes** each :class:`Field` in the :attr:`data` object
      referenced by the `Pointer` field via :meth:`index_data`.
    - **Read** from a :class:`Provider` the necessary bytes for the :attr:`data`
      object referenced by the `Pointer` field via :meth:`read_from`.
    - **Write** to a :class:`Provider` the necessary bytes for the
      :attr:`data` object referenced by the `Pointer` field
      via :meth:`write_to`.
    - Get the accumulated **size** of all fields in the :attr:`data` object
      referenced by the `Pointer` field via :attr:`data_size`.
    - Indexes the `Pointer` field and each :class:`Field` in the :attr:`data`
      object referenced by the `Pointer` field via :meth:`index_fields`.
    - View the selected *attributes* of the `Pointer` field and for each
      :class:`Field` in the :attr:`data` object referenced by the `Pointer`
      field via :meth:`view_fields`.
    - List the **path** to the field and the field **item** for the `Pointer`
      field and for each :class:`Field` in the :attr:`data` object referenced by
      the `Pointer` field as a flatted list via :meth:`field_items`.
    - Get the **metadata** of the `Pointer` field via :meth:`describe`.

    :param template: template for the :attr:`data` object
        referenced by the `Pointer` field.
    :type template: Structure|Sequence|Field|None
    :param int|None address: absolute address of the :attr:`data` object
        referenced by the `Pointer` field.
    :param data_order: byte order used to unpack and pack the :attr:`data` object
        referenced by the `Pointer` field.
    :type data_order: Byteorder|Literal['big', 'little']
    :param int bit_size: is the *size* of the `Pointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Pointer` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Pointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `Pointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `Pointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = Pointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    >>> pointer.data_size
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.value
    '0xc000'
    >>> pointer.value = 0x4000
    >>> pointer.value
    '0x4000'
    >>> pointer.initialize_fields({'value': 0x8000})
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
    >>> pointer.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> bytestream.hex()
    'ffffffff'
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    '4b6f6e466f6f2069732046756e'
    >>> pointer.serialize_data()
    b''
    >>> pointer.deserialize_data()
    Index(byte=0, bit=0, address=4294967295, base_address=4294967295, update=False)
    >>> pointer.serialize_data()
    b''
    >>> pointer.describe()
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
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': None}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": null}'
    >>> pointer.field_items()
    [('field',
      Pointer(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
              alignment=Alignment(byte_size=4, bit_offset=0),
              bit_size=32,
              value='0xffffffff'))]
    >>> pointer.to_list()
    [('Pointer.field', '0xffffffff')]
    >>> pointer.to_dict()
    {'Pointer': {'field': '0xffffffff'}}
    """
    # Item type of a Pointer field.
    item_type: ItemClass = ItemClass.Pointer

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(bit_size=bit_size,
                         align_to=align_to,
                         byte_order=field_order)
        # Field value
        if address:
            self.value = address
        # Data object
        self._data = self.data = template
        # Data objects bytestream
        self._data_stream: bytes = bytes()
        # Data objects byte order
        self._data_byte_order = self.data_byte_order = data_order

    @property
    def address(self) -> int:
        """ Returns the *data source* address of the :attr:`data` object
        referenced by the `Pointer` field (read-only).
        """
        return self._value

    @property
    def base_address(self) -> int:
        """ Returns the *data source* base address of the :attr:`data` object
        referenced by the `Pointer` field (read-only).
        """
        return self._value

    @property
    def bytestream(self) -> str:
        """ Byte stream of the `Pointer` field for the referenced :attr:`data`
        object. Returned as a lowercase hexadecimal encoded string.
        """
        return self._data_stream.hex()

    @bytestream.setter
    def bytestream(self,
                   value: bytes | bytearray | str) -> None:
        if isinstance(value, str):
            self._data_stream = bytes.fromhex(value)
        elif isinstance(value, (bytearray, bytes)):
            self._data_stream = bytes(value)
        else:
            raise FieldTypeError(self, self.index, value)

    @property
    def data(self) -> Structure | Sequence | Field | None:
        """ `Data` object referenced by the `Pointer` field."""
        return self._data

    @data.setter
    def data(self, value: Structure | Sequence | Field | None) -> None:
        if value is None:
            self._data = None
        elif is_any(value):
            self._data = value
        else:
            raise MemberTypeError(self, value, 'data')

    @property
    def data_byte_order(self) -> Byteorder:
        """ :class:`Byteorder` used to deserialize and serialize the :attr:`data`
        object referenced by the `Pointer` field.
        """
        return self._data_byte_order

    @data_byte_order.setter
    def data_byte_order(self,
                        value: (Literal['little', 'big'],
                                Byteorder | str)) -> None:
        byte_order = value

        if isinstance(value, str):
            byte_order = Byteorder.get_member(value)
            if not byte_order:
                raise ByteOrderValueError(self, self.index, value)

        if not isinstance(byte_order, Byteorder):
            raise ByteOrderTypeError(self, value)

        if byte_order not in (Byteorder.big, Byteorder.little):
            raise FieldByteOrderError(self, self.index, byte_order.value)
        self._data_byte_order = byte_order

    @property
    def data_size(self) -> int:
        """ Returns the size of the :attr:`data` object in bytes (read-only)."""
        # Container
        if is_container(self._data):
            byte_length, bit_length = self._data.container_size()
            return byte_length + math.ceil(bit_length / 8)
        # Field
        elif is_field(self._data):
            return math.ceil(self._data.bit_size / 8)
        else:
            return 0

    @property
    def value(self) -> str:
        """ Field value as a lowercase hexadecimal string prefixed with ``0x``."""
        return hex(self._value)

    @value.setter
    def value(self, x: int | str) -> None:
        self._value = self.to_decimal(x)

    @staticmethod
    def is_pointer() -> bool:
        """ Returns :data:`True`."""
        return True

    def is_null(self) -> bool:
        """ Returns :data:`True` if the `Pointer` field points to zero."""
        return self._value == 0

    def deserialize_data(self,
                         buffer: bytes = bytes(),
                         byte_order: (Literal['big', 'little'] |
                                      Byteorder | None) = None) -> Index:
        """ De-serializes the :attr:`data` object referenced by the `Pointer`
        field from the byte *buffer* by mapping the bytes to the
        :attr:`~Field.value` for each :class:`Field` in the :attr:`data` object
        in accordance with the decoding *byte order* for the de-serialization
        and the decoding :attr:`byte_order` of each :class:`Field` in the
        :attr:`data` object.

        A specific decoding :attr:`byte_order` of a :class:`Field` in
        the :attr:`data` object overrules the decoding *byte order* for the
        de-serialization.

        Returns the :class:`Index` of the *buffer* after the last de-serialized
        :class:`Field` in the :attr:`data` object.

        :param bytes buffer: byte stream. Default is the internal
            :attr:`bytestream` of the `Pointer` field.
        :keyword byte_order: decoding byte order for the de-serialization.
            Default is the :attr:`data_byte_order` of the `Pointer` field.
        :type byte_order: Byteorder|Literal['big', 'little']
        """
        index = Index(0, 0, self.address, self.base_address, False)
        if self._data:
            if byte_order not in ('big', 'little',
                                  Byteorder.big, Byteorder.little):
                byte_order = self.data_byte_order
            index = self._data.deserialize(buffer or self._data_stream,
                                           index,
                                           nested=False,
                                           byte_order=byte_order)
        return index

    def serialize_data(self,
                       byte_order: (Literal['big', 'little'] |
                                    Byteorder | None) = None) -> bytes:
        """ Serializes the :attr:`data` object referenced by the `Pointer` field
        to bytes by mapping the :attr:`~Field.value` for each :class:`Field`
        in the :attr:`data` object to a number of bytes in accordance with the
        encoding *byte order* for the serialization and the encoding
        :attr:`byte_order` of each :class:`Field` in the :attr:`data` object.

        A specific encoding :attr:`~Field.byte_order` of a :class:`Field` in
        the :attr:`data` object overrules the encoding *byte order* for the
        serialization.

        Returns a number of bytes for the serialized :attr:`data` object
        referenced by the `Pointer` field.

        :keyword byte_order: encoding byte order for the serialization.
            Default is the :attr:`data_byte_order` of the `Pointer` field.
        :type byte_order: Byteorder|Literal['big', 'little']
        """
        if self._data is None:
            return bytes()
        if byte_order not in ('big', 'little',
                              Byteorder.big, Byteorder.little):
            byte_order = self.data_byte_order
        buffer = bytearray()
        self._data.serialize(buffer,
                             Index(0, 0,
                                   self.address, self.base_address,
                                   False),
                             byte_order=byte_order)
        return bytes(buffer)

    def index_data(self) -> None:
        """ Indexes each :class:`Field` in the :attr:`data` object referenced
        by the `Pointer` field.
        """
        # Start index for the Data Object
        index = Index(0, 0, self.address, self.base_address, False)
        # Container
        if is_container(self._data):
            self._data.index_fields(index, nested=True)
        # Pointer
        elif is_pointer(self._data):
            self._data.index_field(index)
            self._data.index_data()
        # Field
        elif is_field(self._data):
            self._data.index_field(index)

    @nested_option(True)
    def read_from(self,
                  provider: Provider,
                  null_allowed: bool = False,
                  **options: Any) -> None:
        """ Reads from the data :class:`Provider` the necessary number of bytes
        for the :attr:`data` object referenced by the `Pointer` field.

        A `Pointer` field stores the binary data read from the data
        :class:`Provider` in its :attr:`bytestream`.

        :param Provider provider: data :class:`Provider`.
        :param bool null_allowed: if :data:`True` read access of address zero
            (Null) is allowed.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            :attr:`data` object of the `Pointer` field reads their referenced
            :attr:`~Pointer.data` object fields as well (chained method call).
            Each `Pointer` field stores the bytes for its referenced
            :attr:`data` object in its :attr:`bytestream`.
        """
        if self._data is None:
            pass
        elif is_provider(provider):
            if self._value < 0:
                pass
            elif null_allowed or self._value > 0:
                while True:
                    self.bytestream = provider.read(self.address,
                                                    self.data_size)
                    index = self.deserialize_data()
                    # Incomplete data object
                    if index.bit != 0:
                        length = index.byte, index.bit
                        raise ContainerLengthError(self, length)
                    if not index.update:
                        break
                if is_mixin(self._data) and get_nested(options):
                    self._data.read_from(provider, **options)
            else:
                self.bytestream = bytes()
                self.deserialize_data()
        else:
            raise ProviderTypeError(self, provider)

    def patch(self,
              item: Structure | Sequence | Field,
              byte_order: (Literal['big', 'little'] |
                           Byteorder) = BYTEORDER) -> Patch | None:
        """ Returns a memory :class:`Patch` for the given *item* that shall be
        patched in the `data source`.

        :param item: item to patch.
        :type item: Structure|Sequence|Field
        :param byte_order: encoding :class:`Byteorder` for the item.
        :type byte_order: Byteorder|Literal['big', 'little']
        """
        # Re-index the data object
        self.index_data()

        if is_container(item):
            length = item.container_size()
            if length[1] != 0:
                # Incomplete container
                raise ContainerLengthError(item, length)

            field = item.first_field()
            if field is None:
                # Empty container?
                return None

            index = field.index
            if index.bit != 0:
                # Bad placed container
                raise FieldIndexError(field, index)

            # Create a dummy byte array filled with zero bytes.
            # The dummy byte array is necessary because the length of
            # the buffer must correlate to the field indexes of the
            # appending fields.
            buffer = bytearray(b'\x00' * index.byte)

            # Append to the buffer the content mapped by the container fields
            item.serialize(buffer, index, byte_order=byte_order)

            # Content of the buffer mapped by the container fields
            content = buffer[index.byte:]

            if len(content) != length[0]:
                # Not correct filled buffer!
                raise BufferError(len(content), length[0])

            return Patch(content,
                         index.address,
                         byte_order,
                         length[0] * 8,
                         0,
                         False)
        elif is_field(item):
            # Field index
            index = item.index
            # Field alignment
            alignment = item.alignment

            if index.bit != alignment.bit_offset:
                # Bad aligned field?
                raise FieldGroupOffsetError(
                    item, index, Alignment(alignment.byte_size, index.bit))

            # Create a dummy byte array filled with zero bytes.
            # The dummy byte array is necessary because the length of
            # the buffer must correlate to the field index of the
            # appending field group.
            buffer = bytearray(b'\x00' * index.byte)

            # Append to the buffer the content mapped by the field
            item.serialize(buffer, index, byte_order=byte_order)

            # Content of the buffer mapped by the field group
            content = buffer[index.byte:]

            if len(content) != alignment.byte_size:
                # Not correct filled buffer!
                raise BufferError(len(content), alignment.byte_size)

            # Patch size in bytes for the field in the content buffer
            patch_size, bit_offset = divmod(item.bit_size, 8)
            if bit_offset != 0:
                inject = True
                patch_size += 1
            else:
                inject = False

            # Patch offset in bytes for the field in the content buffer
            patch_offset, bit_offset = divmod(alignment.bit_offset, 8)
            if bit_offset != 0:
                inject = True

            if byte_order is Byteorder.big:
                start = alignment.byte_size - (patch_offset + patch_size)
                stop = alignment.byte_size - patch_offset
            else:
                start = patch_offset
                stop = patch_offset + patch_size

            return Patch(content[start:stop],
                         index.address + start,
                         byte_order,
                         item.bit_size,
                         bit_offset,
                         inject)
        else:
            raise MemberTypeError(self, item)

    def write_to(self,
                 provider: Provider,
                 item: Structure | Sequence | Field,
                 byte_order: Byteorder = BYTEORDER) -> None:
        """ Writes via a data :class:`Provider` the :class:`Field` values of
        the given *item* to the `data source`.

        :param Provider provider: data :class:`Provider`.
        :param item: item to write.
        :type item: Structure|Sequence|Field
        :param Byteorder byte_order: encoding byte order of the *item*
            to write.
        """
        # Create memory patch for the item to write
        patch = self.patch(item, byte_order)

        if patch is None:
            pass
        elif is_provider(provider):
            if patch.inject:
                # Unpatched content of the memory area in the data source to modify
                content = provider.read(patch.address, len(patch.buffer))

                # Decimal value of the memory area to patch
                value = int.from_bytes(content, byte_order.value)

                # Inject memory patch content
                bit_mask = ~((2 ** patch.bit_size - 1) << patch.bit_offset)
                bit_mask &= (2 ** (len(patch.buffer) * 8) - 1)
                value &= bit_mask
                value |= int.from_bytes(patch.buffer, byte_order.value)

                # Patched content for the memory area in the data source
                buffer = value.to_bytes(len(patch.buffer), byte_order.value)

                provider.write(buffer, patch.address, len(buffer))
            else:
                provider.write(patch.buffer, patch.address, len(patch.buffer))
        else:
            raise ProviderTypeError(self, provider)

    @byte_order_option()
    @nested_option()
    def deserialize(self,
                    buffer: bytes = bytes(),
                    index: Index = Index(),
                    **options: Any) -> Index:
        """ De-serializes the `Pointer` field from the byte *buffer* starting
        at the beginning of the *buffer* or with the given *index* by mapping
        the bytes to the :attr:`value` of the `Pointer` field in accordance with
        the decoding *byte order* for the de-serialization and the decoding
        :attr:`byte_order` of the `Pointer` field.

        The specific decoding :attr:`byte_order` of the `Pointer` field
        overrules the decoding *byte order* for the de-serialization.

        Returns the :class:`Index` of the *buffer* after the `Pointer` field.

        Optional the de-serialization of the referenced :attr:`data` object of
        the `Pointer` field can be enabled.

        :param bytes buffer: byte stream to de-serialize from.
        :param Index index: current read :class:`Index` within the *buffer* to
            de-serialize.
        :keyword byte_order: decoding byte order for the de-serialization.
        :type byte_order: Byteorder|Literal['auto', 'big', 'little']
        :keyword bool nested: if :data:`True` a `Pointer` field de-serialize its
            referenced :attr:`data` object as well (chained method call).
            Each :class:`Pointer` field uses for the de-serialization of its
            referenced :attr:`data` object its own :attr:`bytestream`.
        """
        # Field
        index = super().deserialize(buffer, index, **options)
        # Data Object
        if self._data and get_nested(options):
            options[str(Option.byte_order.value)] = self.data_byte_order
            self._data.deserialize(self._data_stream,
                                   Index(0, 0,
                                         self.address, self.base_address,
                                         False),
                                   **options)
        return index

    @byte_order_option()
    @nested_option()
    def serialize(self,
                  buffer: bytearray = bytearray(),
                  index: Index = Index(),
                  **options: Any) -> Index:
        """ Serializes the `Pointer` field to the byte *buffer* starting at the
        beginning of the *buffer* or with the given *index* by mapping the
        :attr:`value` of the `Pointer` field to the byte *buffer* in accordance
        with the encoding *byte order* for the serialization and the encoding
        :attr:`byte_order` of the `Pointer` field.

        The specific encoding :attr:`byte_order` of the `Pointer` field
        overrules the encoding *byte order* for the serialization.

        Returns the :class:`Index` of the *buffer* after the `Pointer` field.

        Optional the serialization of the referenced :attr:`data` object of the
        `Pointer` field can be enabled.

        :param bytearray buffer: byte stream to serialize to.
        :param Index index: current write :class:`Index` within the *buffer*.
        :keyword byte_order: encoding byte order for the serialization.
        :type byte_order: Byteorder|Literal['auto', 'big', 'little']
        :keyword bool nested: if :data:`True` a `Pointer` field serializes its
            referenced :attr:`data` object as well (chained method call).
            Each :class:`Pointer` field uses for the serialization of its
            referenced :attr:`data` object its own :attr:`bytestream`.
        """
        # Field
        index = super().serialize(buffer, index, **options)
        # Data Object
        if self._data and get_nested(options):
            options[str(Option.byte_order.value)] = self.data_byte_order
            self._data_stream = bytearray()
            self._data.serialize(self._data_stream,
                                 Index(0, 0,
                                       self.address, self.base_address,
                                       False),
                                 **options)
            self._data_stream = bytes(self._data_stream)
        return index

    def initialize_fields(self,
                          content: dict[str, Any]) -> None:
        """ Initializes the `Pointer` field itself and the :class:`Field` items
        in the :attr:`data` object referenced by the `Pointer` field with the
        *values* in the *content* dictionary.

        The ``['value']`` key in the *content* dictionary refers to the `Pointer`
        field itself and the ``['data']`` key refers to the :attr:`data` object
        referenced by the `Pointer` field.

        :param dict[str, Any] content: a dictionary contains the
            :class:`~Field.value` for the `Pointer` field and the
            :class:`~Field.value` for each :class:`Field` in the
            :attr:`data` object referenced by the `Pointer` field.
        """
        for name, value in content.items():
            if name == 'value':
                self.value = value
            elif name == 'data':
                # Container or Pointer
                if is_mixin(self._data):
                    self._data.initialize_fields(value)
                # Field
                elif is_field(self._data):
                    self._data.value = value

    @nested_option()
    def index_fields(self,
                     index: Index = Index(),
                     **options: Any) -> Index:
        """ Indexes the `Pointer` field and the :attr:`data` object referenced
        by the `Pointer` field starting with the given *index* and returns the
        :class:`Index` after the `Pointer` field.

        :param Index index: :class:`Index` for the `Pointer` field.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            :attr:`data` object referenced by the `Pointer` field indexes their
            referenced :attr:`~Pointer.data` object fields as well
            (chained method call).
        """
        index = self.index_field(index)

        # Container
        if is_container(self._data):
            self._data.index_fields(Index(0, 0,
                                          self.address, self.base_address,
                                          False),
                                    **options)
        # Pointer
        elif is_pointer(self._data) and get_nested(options):
            self._data.index_fields(Index(0, 0,
                                          self.address, self.base_address,
                                          False),
                                    **options)
        # Field
        elif is_field(self._data):
            self._data.index_field(Index(0, 0,
                                         self.address, self.base_address,
                                         False))
        return index

    @nested_option()
    def view_fields(self,
                    *attributes: str,
                    **options: Any) -> dict[str, Any]:
        """ Returns a :class:`dict` which contains the selected field
        *attributes* of the `Pointer` field itself extended with a ``['data']``
        key which contains the selected field *attribute* or the dictionaries of
        the selected field *attributes* for each :class:`Field` *nested* in the
        :attr:`data` object referenced by the `Pointer` field.

        The *attributes* of each :class:`Field` for containers *nested* in the
        :attr:`data` object referenced by the `Pointer` field are viewed as well
        (chained method call).

        :param str attributes: selected :class:`Field` attributes.
            Fallback is the field :attr:`~Field.value`.
        :keyword tuple[str, ...] fieldnames: sequence of dictionary keys for the
            selected field *attributes*. Defaults to ``(*attributes)``.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            :attr:`data` object referenced by the `Pointer` field views their
            referenced :attr:`~Pointer.data` object field attributes as well
            (chained method call).
        """
        items = dict()

        # Pointer field
        if attributes:
            field_getter = attrgetter(*attributes)
        else:
            field_getter = attrgetter('value')

        if len(attributes) > 1:
            for key, value in zip(attributes, field_getter(self)):
                items[key] = value
        else:
            items['value'] = field_getter(self)

        # Data object
        if is_container(self._data):
            # Container
            items['data'] = self._data.view_fields(*attributes, **options)
        elif is_pointer(self._data) and get_nested(options):
            # Pointer
            items['data'] = self._data.view_fields(*attributes, **options)
        elif is_field(self._data):
            # Field
            if attributes:
                field_getter = attrgetter(*attributes)
            else:
                field_getter = attrgetter('value')
            if len(attributes) > 1:
                fieldnames = options.get('fieldnames', attributes)
                items['data'] = dict(zip(fieldnames, field_getter(self._data)))
            else:
                items['data'] = field_getter(self._data)
        else:
            # None
            items['data'] = self._data
        return items

    @nested_option()
    def field_items(self,
                    path: str = str(),
                    **options: Any) -> list[tuple[str, Field]]:
        """ Returns a **flatten** list of ``('field path', field item)`` tuples
        for the `Pointer` field itself and for each :class:`Field` *nested* in the
        :attr:`data` object referenced by the `Pointer` field.

        :param str path: path of the `Pointer` field.
        :keyword bool nested: if :data:`True` all :class:`Pointer` fields in the
            :attr:`data` object referenced by the `Pointer` field lists their
            referenced :attr:`~Pointer.data` object field items as well
            (chained method call).
        """
        items = list()
        # Field
        items.append((path if path else 'field', self))
        # Data Object
        data_path = f"{path}.data" if path else 'data'
        # Container
        if is_container(self._data):
            for field_item in self._data.field_items(data_path, **options):
                items.append(field_item)
        # Pointer
        elif is_pointer(self._data) and get_nested(options):
            for field_item in self._data.field_items(data_path, **options):
                items.append(field_item)
        # Field
        elif is_field(self._data):
            items.append((data_path, self._data))
        return items

    @nested_option(True)
    def describe(self,
                 name: str = str(),
                 **options: Any) -> dict[str, Any]:
        """ Returns the **metadata** of a `Pointer` as a :class:`dict`.

        .. code-block:: python

            metadata = {
                'address': self.index.address,
                'alignment': [self.alignment.byte_size, self.alignment.bit_offset],
                'class': self.__class__.__name__,
                'index': [self.index.byte, self.index.bit],
                'max': self.max(),
                'min': self.min(),
                'name': name if name else self.__class__.__name__,
                'order': self.byte_order.value,
                'size': self.bit_size,
                'type': Pointer.item_type.name,
                'value': self.value,
                'member': [self.data.describe()]
            }

        :param str name: optional name for the `Pointer` field.
            Fallback is the class name.
        :keyword bool nested: if :data:`True` a :class:`Pointer` field lists its
            referenced :attr:`data` object fields as well (chained method call).
            Default is :data:`True`.
        """
        metadata = super().describe(name, **options)
        metadata['class'] = self.__class__.__name__
        metadata['name'] = name if name else self.__class__.__name__
        metadata['type'] = Pointer.item_type.name
        if is_any(self._data) and get_nested(options):
            metadata['member'] = list()
            metadata['member'].append(self._data.describe('data', **options))
        return metadata


class StructurePointer(Pointer):
    """ The :class:`StructurePointer` field is a :class:`Pointer` which refers
    to a :class:`Structure`.

    :param template: template for the :attr:`data` object
        referenced by the `Pointer` field.
        The *template* must be a :class:`Structure` instance.
    :type template: Structure|None
    :param int|None address: absolute address of the :attr:`data` object
        referenced by the `Pointer` field.
    :param data_order: byte order used to unpack and pack the :attr:`data` object
        referenced by the `Pointer` field.
    :type data_order: Byteorder|Literal['big', 'little']
    :param int bit_size: is the *size* of the `Pointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Pointer` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Pointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `Pointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `Pointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = StructurePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    {}
    >>> pointer.data_size
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer.describe()  #doctest: +SKIP
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
     'member': [
        {'class': 'Structure',
         'name': 'data',
         'size': 0,
         'type': 'Structure',
         'member': []}
     ]}
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': {}}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": {}}'
    >>> pointer.field_items()
    [('field',
      StructurePointer(index=Index(byte=0, bit=0,
                                   address=0, base_address=0,
                                   update=False),
                       alignment=Alignment(byte_size=4, bit_offset=0),
                       bit_size=32,
                       value='0xffffffff'))]
    >>> pointer.to_list(nested=True)
    [('StructurePointer.field', '0xffffffff')]
    >>> pointer.to_dict(nested=True)
    {'StructurePointer': {'field': '0xffffffff'}}
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        if template is None:
            template = Structure()
        elif not is_structure(template):
            raise MemberTypeError(self, template)
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: str) -> Structure | Sequence | Field:
        return self._data[key]

    def __iter__(self) -> Iterator[Structure | Sequence | Field]:
        return iter(self._data)

    def __getattr__(self, attr: str) -> Any:
        return self._data[attr]

    def items(self) -> ItemsView[str, Structure | Sequence | Field]:
        return self._data.items()

    def keys(self) -> KeysView[str]:
        return self._data.keys()

    def values(self) -> ValuesView[Structure | Sequence | Field]:
        return self._data.values()


class SequencePointer(Pointer):
    """ The :class:`SequencePointer` field is a :class:`Pointer` field which
    refers to a :class:`Sequence`.

    A `SequencePointer` field is:

    - *containable*: ``item`` in ``self`` returns :data:`True` if *item* is part
      of the referenced :class:`Sequence`.
    - *sized*: ``len(self)`` returns the number of items in the referenced
      :class:`Sequence`.
    - *indexable* ``self[index]`` returns the *item* at the *index* of the
      referenced :class:`Sequence`.
    - *iterable* ``iter(self)`` iterates over the *items* of the referenced
      :class:`Sequence`

    A `SequencePointer` field supports the usual methods for sequences:

    - **Append** an item to the referenced :class:`Sequence`
      via :meth:`append()`.
    - **Insert** an item before the *index* into the referenced :class:`Sequence`
      via :meth:`insert()`.
    - **Extend** the referenced :class:`Sequence` with items
      via :meth:`extend()`.
    - **Clear** the referenced :class:`Sequence` via :meth:`clear()`.
    - **Pop** an item with the *index* from the referenced :class:`Sequence`
      via :meth:`pop()`.
    - **Remove** the first occurrence of an *item* from the referenced
      :class:`Sequence` via :meth:`remove()`.
    - **Reverse** all items in the referenced :class:`Sequence`
      via :meth:`reverse()`.

    :param iterable: any *iterable* that contains items of :class:`Structure`,
        :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
        *iterable* is one of these instances itself then the *iterable* itself
        is appended to the :class:`Sequence`.
    :type iterable: Iterable[Structure|Sequence|Field]|Structure|Sequence|Field|None
    :param int|None address: absolute address of the :attr:`data` object
        referenced by the `Pointer` field.
    :param data_order: byte order used to unpack and pack the :attr:`data` object
        referenced by the `Pointer` field.
    :type data_order: Byteorder|Literal['big', 'little']
    :param int bit_size: is the *size* of the `Pointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Pointer` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Pointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `Pointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `Pointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = SequencePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    []
    >>> pointer.data_size
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer).hex()
    '00000000'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer[0]
    Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=Alignment(byte_size=0, bit_offset=0),
          bit_size=0,
          value=None)
    >>> len(pointer)
    1
    >>> pointer.pop()
    Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=Alignment(byte_size=0, bit_offset=0),
          bit_size=0,
          value=None)
    >>> pointer.insert(0, Field())
    >>> pointer.data
    [Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=Alignment(byte_size=0, bit_offset=0),
           bit_size=0,
           value=None)]
    >>> pointer.remove(pointer[0])
    >>> pointer.data
    []
    >>> pointer.clear()
    >>> pointer.describe()  #doctest: +SKIP
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
     'member': [
        {'class': 'Sequence',
         'name': 'data',
         'size': 0,
         'type': 'Sequence',
         'member': []}
     ]}
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': []}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": []}'
    >>> pointer.field_items()
    [('field',
      SequencePointer(index=Index(byte=0, bit=0,
                                  address=0, base_address=0,
                                  update=False),
                      alignment=Alignment(byte_size=4, bit_offset=0),
                      bit_size=32,
                      value='0xffffffff'))]
    >>> pointer.to_list(nested=True)
    [('SequencePointer.field', '0xffffffff')]
    >>> pointer.to_dict(nested=True)
    {'SequencePointer': {'field': '0xffffffff'}}
    """

    def __init__(self,
                 iterable: (Iterable[Structure | Sequence | Field] |
                            Structure | Sequence | Field | None) = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=Sequence(iterable),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)

    def __contains__(self,
                     key: Structure | Sequence | Field) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self,
                    index: int | slice) -> Structure | Sequence | Field | list:
        return self._data[index]

    def __setitem__(self,
                    index: int,
                    item: Structure | Sequence | Field) -> None:
        self._data[index] = item

    def __delitem__(self,
                    index: int) -> None:
        del self._data[index]

    def append(self, item: Structure | Sequence | Field) -> None:
        """ Appends the *item* to the end of the :class:`Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        :type item: Structure|Sequence|Field
        """
        self._data.append(item)

    def insert(self,
               index: int,
               item: Structure | Sequence | Field) -> None:
        """ Inserts the *item* before the *index* into the :class:`Sequence`.

        :param int index: :class:`Sequence` index.
        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        :type item: Structure|Sequence|Field
        """
        self._data.insert(index, item)

    def pop(self,
            index: int = -1) -> Structure | Sequence | Field:
        """ Removes and returns the item at the *index* from the
        :class:`Sequence`.

        :param int index: :class:`Sequence` index.
        """
        return self._data.pop(index)

    def clear(self) -> None:
        """ Remove all items from the :class:`Sequence`."""
        self._data.clear()

    def remove(self,
               item: Structure | Sequence | Field) -> None:
        """ Removes the first occurrence of an *item* from the :class:`Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        :type item: Structure|Sequence|Field
        """
        self._data.remove(item)

    def reverse(self) -> None:
        """ In place reversing of the :class:`Sequence` items."""
        self._data.reverse()

    def extend(self, iterable: (Iterable[Structure | Sequence | Field] |
                                Structure | Sequence | Field)) -> None:
        """ Extends the :class:`Sequence` by appending items from the *iterable*.

        :param iterable: any *iterable* that contains items of :class:`Structure`,
            :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
            *iterable* is one of these instances itself then the *iterable* itself
            is appended to the :class:`Sequence`.
        :type iterable: Iterable[Structure|Sequence|Field]|Structure|Sequence|Field
        """
        self._data.extend(iterable)


class ArrayPointer(SequencePointer):
    """ The :class:`ArrayPointer` field is a :class:`SequencePointer` field
    which refers to a :class:`Array`.

    An `ArrayPointer` field adapts and extends a :class:`SequencePointer`
    field with the following features:

    - **Append** a new :class:`Array` element to the referenced :class:`Array`
      via :meth:`append()`.
    - **Insert** a new :class:`Array` element before the *index*
        into the referenced :class:`Array` via :meth:`insert()`.
    - **Re-size** the referenced :class:`Array` via :meth:`resize()`.

    :param template: template for the :class:`Array` element.
        The *template* can be any :class:`Field` instance or any *callable*
        that returns a :class:`Structure`, :class:`Sequence`, :class:`Array`
        or any :class:`Field` instance.
    :type template: Callable|Structure|Sequence|Field
    :param int capacity: is the capacity of the :class:`Array` in number of
        :class:`Array` elements.
    :param int|None address: absolute address of the :attr:`data` object
        referenced by the `Pointer` field.
    :param data_order: byte order used to unpack and pack the :attr:`data` object
        referenced by the `Pointer` field.
    :type data_order: Byteorder|Literal['big', 'little']
    :param int bit_size: is the *size* of the `Pointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Pointer` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Pointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `Pointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `Pointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = ArrayPointer(Byte)
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    []
    >>> pointer.data_size
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer[0]
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=Alignment(byte_size=1, bit_offset=0),
         bit_size=8,
         value='0x0')
    >>> len(pointer)
    1
    >>> pointer.pop()
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=Alignment(byte_size=1, bit_offset=0),
         bit_size=8,
         value='0x0')
    >>> pointer.insert(0)
    >>> pointer.data
    [Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=Alignment(byte_size=1, bit_offset=0),
          bit_size=8,
          value='0x0')]
    >>> pointer.remove(pointer[0])
    >>> pointer.data
    []
    >>> pointer.resize(10)
    >>> len(pointer)
    10
    >>> pointer.clear()
    >>> pointer.describe()  #doctest: +SKIP
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
     'member': [
        {'class': 'Array',
         'name': 'data',
         'size': 0,
         'type': 'Array',
         'member': []}
     ]}
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': []}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": []}'
    >>> pointer.field_items()
    [('field',
      ArrayPointer(index=Index(byte=0, bit=0,
                               address=0, base_address=0,
                               update=False),
                   alignment=Alignment(byte_size=4, bit_offset=0),
                   bit_size=32,
                   value='0xffffffff'))]
    >>> pointer.to_list(nested=True)
    [('ArrayPointer.field', '0xffffffff')]
    >>> pointer.to_dict(nested=True)
    {'ArrayPointer': {'field': '0xffffffff'}}
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)
        self._data: Array = Array(template, capacity)

    def append(self) -> None:
        """ Appends a new :class:`Array` element to the :class:`Array`."""
        self._data.append()

    def insert(self, index: int) -> None:
        """ Inserts a new :class:`Array` element before the *index*
        of the :class:`Array`.

        :param int index: :class:`Array` index.
        """
        self._data.insert(index)

    def resize(self, capacity: int) -> None:
        """ Re-sizes the :class:`Array` by appending new :class:`Array` elements
        or removing :class:`Array` elements from the end.

        :param int capacity: new capacity of the :class:`Array` in number of
            :class:`Array` elements.
        """
        if isinstance(self._data, Array):
            self._data.resize(capacity)


class StreamPointer(Pointer):
    """ The :class:`StreamPointer` field is a :class:`Pointer` field which
    refers to a :class:`Stream` field.

    A `StreamPointer` field is:

    - *containable*: ``item`` in ``self`` returns :data:`True` if *item* is part
      of the referenced :class:`Stream` field.
    - *sized*: ``len(self)`` returns the length of the referenced
      :class:`Stream` field.
    - *indexable* ``self[index]`` returns the *byte* at the *index*
      of the referenced  :class:`Stream` field.
    - *iterable* ``iter(self)`` iterates over the bytes of the referenced
      :class:`Stream` field.

    :param int capacity: is the *capacity* of the :class:`Stream` field in bytes.
    :param int|None address: absolute address of the :attr:`data` object
        referenced by the `Pointer` field.
    :param int bit_size: is the *size* of the `Pointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Pointer` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Pointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `Pointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `Pointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = StreamPointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    Stream(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=Alignment(byte_size=0, bit_offset=0),
           bit_size=0,
           value='')
    >>> pointer.data_size
    0
    >>> len(pointer)
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> bytestream.hex()
    'ffffffff'
    >>> pointer.resize(10)
    >>> pointer.data_size
    10
    >>> len(pointer)
    10
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    '4b6f6e466f6f2069732046756e'
    >>> pointer.serialize_data().hex()
    '00000000000000000000'
    >>> pointer.deserialize_data()
    Index(byte=10, bit=0, address=4294967305, base_address=4294967295, update=False)
    >>> pointer.serialize_data()
    b'KonFoo is '
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
    >>> b'KonFoo' in pointer
    True
    >>> pointer[:6]  # converts to bytes
    b'KonFoo'
    >>> pointer[3:6]  # converts to bytes
    b'Foo'
    >>> pointer.describe()  #doctest: +SKIP
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
     'member': [
        {'address': 4294967295,
         'alignment': [10, 0],
         'class': 'Stream10',
         'index': [0, 0],
         'name': 'data',
         'order': 'auto',
         'size': 80,
         'type': 'Field',
         'value': '4b6f6e466f6f20697320'}
     ]}
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': '4b6f6e466f6f20697320'}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": "4b6f6e466f6f20697320"}'
    >>> pointer.field_items()
    [('field',
      StreamPointer(index=Index(byte=0, bit=0,
                                address=0, base_address=0,
                                update=False),
                    alignment=Alignment(byte_size=4, bit_offset=0),
                    bit_size=32,
                    value='0xffffffff')),
     ('data',
      Stream(index=Index(byte=0, bit=0,
                         address=4294967295, base_address=4294967295,
                         update=False),
             alignment=Alignment(byte_size=10, bit_offset=0),
             bit_size=80,
             value='4b6f6e466f6f20697320'))]
    >>> pointer.to_list()
    [('StreamPointer.field', '0xffffffff'),
     ('StreamPointer.data', '4b6f6e466f6f20697320')]
    >>> pointer.to_dict()
    {'StreamPointer': {'field': '0xffffffff', 'data': '4b6f6e466f6f20697320'}}
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=None,
                         address=address,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)
        self._data: Stream = Stream(capacity)

    def __contains__(self, key: int | bytes) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int | slice) -> int | bytes:
        return self._data[index]

    def __iter__(self) -> Iterator[int]:
        return iter(self._data)

    def resize(self, capacity: int) -> None:
        """ Re-sizes the :class:`Stream` field by appending zero bytes or
        removing bytes from the end.

        :param int capacity: :class:`Stream` capacity in number of bytes.
        """
        if isinstance(self._data, Stream):
            self._data.resize(capacity)


class StringPointer(StreamPointer):
    """ The :class:`StringPointer` field is a :class:`StreamPointer` field
    which refers to a :class:`String` field.

    :param int capacity: is the *capacity* of the :class:`String` field in bytes.
    :param int|None address: absolute address of the :attr:`data` object
        referenced by the `Pointer` field.
    :param int bit_size: is the *size* of the `Pointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Pointer` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Pointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `Pointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `Pointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = StringPointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    String(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=Alignment(byte_size=0, bit_offset=0),
           bit_size=0,
           value='')
    >>> pointer.data_size
    0
    >>> len(pointer)
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> bytestream.hex()
    'ffffffff'
    >>> pointer.resize(10)
    >>> pointer.data_size
    10
    >>> len(pointer)
    10
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    '4b6f6e466f6f2069732046756e'
    >>> pointer.serialize_data().hex()
    '00000000000000000000'
    >>> pointer.deserialize_data()
    Index(byte=10, bit=0, address=4294967305, base_address=4294967295, update=False)
    >>> pointer.serialize_data()
    b'KonFoo is '
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
    >>> pointer.describe()  #doctest: +SKIP
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
     'member': [
        {'address': 4294967295,
         'alignment': [10, 0],
         'class': 'String10',
         'index': [0, 0],
         'name': 'data',
         'order': 'auto',
         'size': 80,
         'type': 'Field',
         'value': 'KonFoo is '}
     ]}
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': 'KonFoo is '}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": "KonFoo is "}'
    >>> pointer.field_items()
    [('field',
      StringPointer(index=Index(byte=0, bit=0,
                                address=0, base_address=0,
                                update=False),
                    alignment=Alignment(byte_size=4, bit_offset=0),
                    bit_size=32,
                    value='0xffffffff')),
     ('data',
      String(index=Index(byte=0, bit=0,
                         address=4294967295, base_address=4294967295,
                         update=False),
             alignment=Alignment(byte_size=10, bit_offset=0),
             bit_size=80,
             value='KonFoo is '))]
    >>> pointer.to_list()
    [('StringPointer.field', '0xffffffff'),
     ('StringPointer.data', 'KonFoo is ')]
    >>> pointer.to_dict()
    {'StringPointer': {'field': '0xffffffff', 'data': 'KonFoo is '}}
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=0,
                         address=address,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)
        self._data: String = String(capacity)


class AutoStringPointer(StringPointer):
    """ The :class:`AutoStringPointer` field is a :class:`StringPointer` field
    which refers to an auto-sized :class:`String` field.

    :param int|None address: absolute address of the :attr:`data` object
        referenced by the `Pointer` field.
    :param int bit_size: is the *size* of the `Pointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `Pointer` field to the number of bytes,
        can be between ``1`` and ``8``.
        If no field *alignment* is set the `Pointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `Pointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `Pointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = AutoStringPointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    String(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=Alignment(byte_size=64, bit_offset=0),
           bit_size=512,
           value='')
    >>> pointer.data_size
    64
    >>> len(pointer)
    64
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> bytestream.hex()
    'ffffffff'
    >>> pointer.resize(10)
    >>> pointer.data_size
    10
    >>> len(pointer)
    10
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    '4b6f6e466f6f2069732046756e'
    >>> pointer.serialize_data().hex()
    '00000000000000000000'
    >>> pointer.deserialize_data()
    Index(byte=10, bit=0, address=4294967305, base_address=4294967295, update=False)
    >>> pointer.serialize_data()
    b'KonFoo is '
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
    >>> pointer.describe()  #doctest: +SKIP
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
     'member': [
        {'address': 4294967295,
         'alignment': [10, 0],
         'class': 'String10',
         'index': [0, 0],
         'name': 'data',
         'order': 'auto',
         'size': 80,
         'type': 'Field',
         'value': 'KonFoo is '}
     ]}
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': 'KonFoo is '}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": "KonFoo is "}'
    >>> pointer.field_items()
    [('field',
      AutoStringPointer(index=Index(byte=0, bit=0,
                                address=0, base_address=0,
                                update=False),
                        alignment=Alignment(byte_size=4, bit_offset=0),
                        bit_size=32,
                        value='0xffffffff')),
     ('data',
      String(index=Index(byte=0, bit=0,
                         address=4294967295, base_address=4294967295,
                         update=False),
             alignment=Alignment(byte_size=10, bit_offset=0),
             bit_size=80,
             value='KonFoo is '))]
    >>> pointer.to_list()
    [('AutoStringPointer.field', '0xffffffff'),
     ('AutoStringPointer.data', 'KonFoo is ')]
    >>> pointer.to_dict()
    {'AutoStringPointer': {'field': '0xffffffff', 'data': 'KonFoo is '}}
    """
    #: Block size in *bytes* to read for the :class:`String` field.
    BLOCK_SIZE = 64
    #: Maximal allowed address of the :class:`String` field.
    MAX_ADDRESS = 0xffffffff

    def __init__(self,
                 address: int | None = None,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=AutoStringPointer.BLOCK_SIZE,
                         address=address,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)

    @nested_option(True)
    def read_from(self,
                  provider: Provider,
                  null_allowed: bool = False,
                  **options: Any) -> None:
        if self._data is None:
            pass
        elif is_provider(provider):
            if self._value < 0:
                pass
            elif null_allowed or self._value > 0:
                self._data_stream = bytes()
                self.resize(0)
                for address in range(self.address,
                                     self.MAX_ADDRESS,
                                     self.BLOCK_SIZE):
                    count = clamp(self.BLOCK_SIZE,
                                  0,
                                  (self.MAX_ADDRESS - address))
                    self._data_stream += provider.read(address, count)
                    self.resize(len(self) + count)
                    index = self.deserialize_data()
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
                self.deserialize_data()
        else:
            raise ProviderTypeError(self, provider)


class RelativePointer(Pointer):
    """ The :class:`RelativePointer` field is a :class:`Pointer` field which
    references its :attr:`data` object relative to a **base address** in the
    *data source*.

    .. important::

        The :attr:`base_address` of a `RelativePointer` is defined by the field
        :attr:`~Field.index` of the `RelativePointer` field.

    :param template: template for the :attr:`data` object
        referenced by the `RelativePointer` field.
    :type template: Structure|Sequence|Field|None
    :param int|None address: relative address of the :attr:`data` object
        referenced by the `RelativePointer` field.
    :param data_order: byte order used to unpack and pack the :attr:`data` object
        referenced by the `RelativePointer` field.
    :type data_order: Byteorder|Literal['big', 'little']
    :param int bit_size: is the *size* of the `RelativePointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `RelativePointer` field to the number
        of bytes, can be between ``1`` and ``8``.
        If no field *alignment* is set the `RelativePointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `RelativePointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `RelativePointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = RelativePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    >>> pointer.data_size
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> bytestream.hex()
    'ffffffff'
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    '4b6f6e466f6f2069732046756e'
    >>> pointer.serialize_data()
    b''
    >>> pointer.deserialize_data()
    Index(byte=0, bit=0, address=4294967295, base_address=0, update=False)
    >>> pointer.serialize_data()
    b''
    >>> pointer.describe()
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
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': None}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": null}'
    >>> pointer.field_items()
    [('field',
      RelativePointer(index=Index(byte=0, bit=0,
                                  address=0, base_address=0,
                                  update=False),
                      alignment=Alignment(byte_size=4, bit_offset=0),
                      bit_size=32,
                      value='0xffffffff'))]
    >>> pointer.to_list()
    [('RelativePointer.field', '0xffffffff')]
    >>> pointer.to_dict()
    {'RelativePointer': {'field': '0xffffffff'}}
    """

    def __init__(self,
                 template: Structure | Sequence | Field | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)

    @property
    def address(self) -> int:
        """ Returns the *data source* address of the :attr:`data` object
        referenced by the `RelativePointer` field (read-only).
        """
        return self._value + self.base_address

    @property
    def base_address(self) -> int:
        """ Returns the *data source* base address of the :attr:`data` object
        relative referenced by the `RelativePointer` field (read-only).
        """
        return self.index.base_address


class StructureRelativePointer(RelativePointer):
    """ The :class:`StructureRelativePointer` field is a :class:`RelativePointer`
    which refers to a :class:`Structure`.

    :param template: template for the :attr:`data` object
        referenced by the `RelativePointer` field.
        The *template* must be a :class:`Structure` instance.
    :type template: Structure|None
    :param int|None address: relative address of the :attr:`data` object
        referenced by the `RelativePointer` field.
    :param data_order: byte order used to unpack and pack the :attr:`data` object
        referenced by the `RelativePointer` field.
    :type data_order: Byteorder|Literal['big', 'little']
    :param int bit_size: is the *size* of the `RelativePointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `RelativePointer` field to the number
        of bytes, can be between ``1`` and ``8``.
        If no field *alignment* is set the `RelativePointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `RelativePointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `RelativePointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = StructureRelativePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    {}
    >>> pointer.data_size
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer.describe()  #doctest: +SKIP
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
     'member': [
        {'class': 'Structure',
         'name': 'data',
         'size': 0,
         'type': 'Structure',
         'member': []}
     ]}
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': {}}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": {}}'
    >>> pointer.field_items()
    [('field',
      StructureRelativePointer(index=Index(byte=0, bit=0,
                                           address=0, base_address=0,
                                           update=False),
                               alignment=Alignment(byte_size=4, bit_offset=0),
                               bit_size=32,
                               value='0xffffffff'))]
    >>> pointer.to_list(nested=True)
    [('StructureRelativePointer.field', '0xffffffff')]
    >>> pointer.to_dict(nested=True)
    {'StructureRelativePointer': {'field': '0xffffffff'}}
    """

    def __init__(self,
                 template: Structure | None = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        if template is None:
            template = Structure()
        elif not is_structure(template):
            raise MemberTypeError(self, template)
        super().__init__(template=template,
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: str) -> Structure | Sequence | Field:
        return self._data[key]

    def __iter__(self) -> Iterator[Structure | Sequence | Field]:
        return iter(self._data)

    def __getattr__(self, attr: str) -> Any:
        return self._data[attr]

    def items(self) -> ItemsView[str, Structure | Sequence | Field]:
        return self._data.items()

    def keys(self) -> KeysView[str]:
        return self._data.keys()

    def values(self) -> ValuesView[Structure | Sequence | Field]:
        return self._data.values()


class SequenceRelativePointer(RelativePointer):
    """ The :class:`SequenceRelativePointer` field is a :class:`RelativePointer`
    which refers to a :class:`Sequence`.

    A `SequenceRelativePointer` is:

    - *containable*: ``item`` in ``self`` returns :data:`True` if *item* is part
      of the referenced :class:`Sequence`.
    - *sized*: ``len(self)`` returns the number of items in the referenced
      :class:`Sequence`.
    - *indexable* ``self[index]`` returns the *item* at the *index*
      of the referenced :class:`Sequence`.
    - *iterable* ``iter(self)`` iterates over the *items* of the referenced
      :class:`Sequence`

    A `SequenceRelativePointer` supports the usual methods:

    - **Append** an item to the referenced :class:`Sequence`
      via :meth:`append()`.
    - **Insert** an item before the *index* into the referenced :class:`Sequence`
      via :meth:`insert()`.
    - **Extend** the referenced :class:`Sequence` with items
      via :meth:`extend()`.
    - **Clear** the referenced :class:`Sequence` via :meth:`clear()`.
    - **Pop** an item with the *index* from the referenced :class:`Sequence`
      via :meth:`pop()`.
    - **Remove** the first occurrence of an *item* from the referenced
      :class:`Sequence` via :meth:`remove()`.
    - **Reverse** all items in the referenced :class:`Sequence`
      via :meth:`reverse()`.

    :param iterable: any *iterable* that contains items of :class:`Structure`,
        :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
        *iterable* is one of these instances itself then the *iterable* itself
        is appended to the :class:`Sequence`.
    :type iterable: Iterable[Structure|Sequence|Field]|Structure|Sequence|Field
    :param int|None address: relative address of the :attr:`data` object
        referenced by the `RelativePointer` field.
    :param data_order: byte order used to unpack and pack the :attr:`data` object
        referenced by the `RelativePointer` field.
    :type data_order: Byteorder|Literal['big', 'little']
    :param int bit_size: is the *size* of the `RelativePointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `RelativePointer` field to the number
        of bytes, can be between ``1`` and ``8``.
        If no field *alignment* is set the `RelativePointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `RelativePointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `RelativePointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = SequenceRelativePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    []
    >>> pointer.data_size
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer[0]
    Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=Alignment(byte_size=0, bit_offset=0),
          bit_size=0,
          value=None)
    >>> len(pointer)
    1
    >>> pointer.pop()
    Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=Alignment(byte_size=0, bit_offset=0),
          bit_size=0,
          value=None)
    >>> pointer.insert(0, Field())
    >>> pointer.data
    [Field(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=Alignment(byte_size=0, bit_offset=0),
           bit_size=0,
           value=None)]
    >>> pointer.remove(pointer[0])
    >>> pointer.data
    []
    >>> pointer.clear()
    >>> pointer.describe()  #doctest: +SKIP
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
     'member': [
        {'class': 'Sequence',
         'name': 'data',
         'size': 0,
         'type': 'Sequence',
         'member': []}
     ]}
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': []}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": []}'
    >>> pointer.field_items()
    [('field',
      SequenceRelativePointer(index=Index(byte=0, bit=0,
                                          address=0, base_address=0,
                                          update=False),
                              alignment=Alignment(byte_size=4, bit_offset=0),
                              bit_size=32,
                              value='0xffffffff'))]
    >>> pointer.to_list(nested=True)
    [('SequenceRelativePointer.field', '0xffffffff')]
    >>> pointer.to_dict(nested=True)
    {'SequenceRelativePointer': {'field': '0xffffffff'}}
    """

    def __init__(self,
                 iterable: (Iterable[Structure | Sequence | Field] |
                            Structure | Sequence | Field | None) = None,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=Sequence(iterable),
                         address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)

    def __contains__(self,
                     key: Structure | Sequence | Field) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self,
                    index: int | slice) -> Structure | Sequence | Field | list:
        return self._data[index]

    def __setitem__(self,
                    index: int,
                    item: Structure | Sequence | Field) -> None:
        self._data[index] = item

    def __delitem__(self,
                    index: int) -> None:
        del self._data[index]

    def append(self,
               item: Structure | Sequence | Field) -> None:
        """ Appends the *item* to the end of the :class:`Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        :type item: Structure|Sequence|Field
        """
        self._data.append(item)

    def insert(self,
               index: int,
               item: Structure | Sequence | Field) -> None:
        """ Inserts the *item* before the *index* into the :class:`Sequence`.

        :param int index: :class:`Sequence` index.
        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        :type item: Structure|Sequence|Field
        """
        self._data.insert(index, item)

    def pop(self,
            index: int = -1) -> Structure | Sequence | Field:
        """ Removes and returns the item at the *index* from the
        :class:`Sequence`.

        :param int index: :class:`Sequence` index.
        """
        return self._data.pop(index)

    def clear(self) -> None:
        """ Remove all items from the :class:`Sequence`."""
        self._data.clear()

    def remove(self,
               item: Structure | Sequence | Field) -> None:
        """ Removes the first occurrence of an *item* from the :class:`Sequence`.

        :param item: any :class:`Structure`, :class:`Sequence`, :class:`Array`
            or :class:`Field` instance.
        :type item: Structure|Sequence|Field
        """
        self._data.remove(item)

    def reverse(self) -> None:
        """ In place reversing of the :class:`Sequence` items."""
        self._data.reverse()

    def extend(self, iterable: (Iterable[Structure | Sequence | Field] |
                                Structure | Sequence | Field)) -> None:
        """ Extends the :class:`Sequence` by appending items from the *iterable*.

        :param iterable: any *iterable* that contains items of :class:`Structure`,
            :class:`Sequence`, :class:`Array` or :class:`Field` instances. If the
            *iterable* is one of these instances itself then the *iterable* itself
            is appended to the :class:`Sequence`.
        :type iterable: Iterable[Structure|Sequence|Field]|Structure|Sequence|Field
        """
        self._data.extend(iterable)


class ArrayRelativePointer(SequenceRelativePointer):
    """ The :class:`ArrayRelativePointer` field is a
    :class:`SequenceRelativePointer` which refers to a :class:`Array`.

    An `ArrayRelativePointer` adapts and extends a :class:`SequenceRelativePointer`
    with the following features:

    - **Append** a new :class:`Array` element to the :class:`Array`
      via :meth:`append()`.
    - **Insert** a new :class:`Array` element before the *index*
      into the :class:`Array` via :meth:`insert()`.
    - **Re-size** the :class:`Array` via :meth:`resize()`.

    :param template: template for the :class:`Array` element.
        The *template* can be any :class:`Field` instance or any *callable*
        that returns a :class:`Structure`, :class:`Sequence`, :class:`Array`
        or any :class:`Field` instance.
    :param int capacity: is the capacity of the :class:`Array` in number of
        :class:`Array` elements.
    :param int|None address: relative address of the :attr:`data` object
        referenced by the `RelativePointer` field.
    :param data_order: byte order used to unpack and pack the :attr:`data` object
        referenced by the `RelativePointer` field.
    :type data_order: Byteorder|Literal['big', 'little']
    :param int bit_size: is the *size* of the `RelativePointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `RelativePointer` field to the number
        of bytes, can be between ``1`` and ``8``.
        If no field *alignment* is set the `RelativePointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `RelativePointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `RelativePointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = ArrayRelativePointer(Byte)
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    []
    >>> pointer.data_size
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer[0]
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=Alignment(byte_size=1, bit_offset=0),
         bit_size=8,
         value='0x0')
    >>> len(pointer)
    1
    >>> pointer.pop()
    Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
         alignment=Alignment(byte_size=1, bit_offset=0),
         bit_size=8,
         value='0x0')
    >>> pointer.insert(0)
    >>> pointer.data
    [Byte(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
          alignment=Alignment(byte_size=1, bit_offset=0),
          bit_size=8,
          value='0x0')]
    >>> pointer.remove(pointer[0])
    >>> pointer.data
    []
    >>> pointer.resize(10)
    >>> len(pointer)
    10
    >>> pointer.clear()
    >>> pointer.describe()  #doctest: +SKIP
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
     'member': [
        {'class': 'Array',
         'name': 'data',
         'size': 0,
         'type': 'Array',
         'member': []}
     ]}
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': []}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": []}'
    >>> pointer.field_items()
    [('field',
      ArrayRelativePointer(index=Index(byte=0, bit=0,
                                       address=0, base_address=0,
                                       update=False),
                           alignment=Alignment(byte_size=4, bit_offset=0),
                           bit_size=32,
                           value='0xffffffff'))]
    >>> pointer.to_list(nested=True)
    [('ArrayRelativePointer.field', '0xffffffff')]
    >>> pointer.to_dict(nested=True)
    {'ArrayRelativePointer': {'field': '0xffffffff'}}
    """

    def __init__(self,
                 template: Callable | Structure | Sequence | Field,
                 capacity: int = 0,
                 address: int | None = None,
                 data_order: (Literal['big', 'little'] |
                              Byteorder) = BYTEORDER,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(address=address,
                         data_order=data_order,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)
        self._data = Array(template, capacity)

    def append(self) -> None:
        """ Appends a new :class:`Array` element to the :class:`Array`."""
        self._data.append()

    def insert(self, index: int) -> None:
        """ Inserts a new :class:`Array` element before the *index*
        of the :class:`Array`.

        :param int index: :class:`Array` index.
        """
        self._data.insert(index)

    def resize(self, capacity: int) -> None:
        """ Re-sizes the :class:`Array` by appending new :class:`Array` elements
        or removing :class:`Array` elements from the end.

        :param int capacity: new capacity of the :class:`Array` in number of
            :class:`Array` elements.
        """
        if isinstance(self._data, Array):
            self._data.resize(capacity)


class StreamRelativePointer(RelativePointer):
    """ The :class:`StreamRelativePointer` field is a :class:`RelativePointer`
    field which refers to a :class:`Stream` field.

    A `StreamRelativePointer` field is:

    - *containable*: ``item`` in ``self`` returns :data:`True` if *item* is part
      of the referenced :class:`Stream` field.
    - *sized*: ``len(self)`` returns the length of the referenced
      :class:`Stream` field.
    - *indexable* ``self[index]`` returns the *byte* at the *index* of the
      referenced :class:`Stream` field.
    - *iterable* ``iter(self)`` iterates over the bytes of the referenced
      :class:`Stream` field.

    :param int capacity: is the *capacity* of the :class:`Stream` field in bytes.
    :param int|None address: relative address of the :attr:`data` object
        referenced by the `RelativePointer` field.
    :param int bit_size: is the *size* of the `RelativePointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `RelativePointer` field to the number
        of bytes, can be between ``1`` and ``8``.
        If no field *alignment* is set the `RelativePointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `RelativePointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `RelativePointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = StreamRelativePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.data
    Stream(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=Alignment(byte_size=0, bit_offset=0),
           bit_size=0,
           value='')
    >>> pointer.data_size
    0
    >>> len(pointer)
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> bytestream.hex()
    'ffffffff'
    >>> pointer.resize(10)
    >>> pointer.data_size
    10
    >>> len(pointer)
    10
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    '4b6f6e466f6f2069732046756e'
    >>> pointer.serialize_data().hex()
    '00000000000000000000'
    >>> pointer.deserialize_data()
    Index(byte=10, bit=0, address=4294967305, base_address=0, update=False)
    >>> pointer.serialize_data()
    b'KonFoo is '
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
    >>> pointer.describe()  #doctest: +SKIP
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
     'member': [
        {'address': 4294967295,
         'alignment': [10, 0],
         'class': 'Stream10',
         'index': [0, 0],
         'name': 'data',
         'order': 'auto',
         'size': 80,
         'type': 'Field',
         'value': '4b6f6e466f6f20697320'}
     ]}
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': '4b6f6e466f6f20697320'}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": "4b6f6e466f6f20697320"}'
    >>> pointer.field_items()
    [('field',
      StreamRelativePointer(index=Index(byte=0, bit=0,
                                        address=0, base_address=0,
                                        update=False),
                            alignment=Alignment(byte_size=4, bit_offset=0),
                            bit_size=32,
                            value='0xffffffff')),
     ('data',
      Stream(index=Index(byte=0, bit=0,
                         address=4294967295, base_address=0,
                         update=False),
             alignment=Alignment(byte_size=10, bit_offset=0),
             bit_size=80,
             value='4b6f6e466f6f20697320'))]
    >>> pointer.to_list()
    [('StreamRelativePointer.field', '0xffffffff'),
     ('StreamRelativePointer.data', '4b6f6e466f6f20697320')]
    >>> pointer.to_dict()
    {'StreamRelativePointer': {'field': '0xffffffff', 'data': '4b6f6e466f6f20697320'}}
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(template=None,
                         address=address,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)
        self._data: Stream = Stream(capacity)

    def __contains__(self, key: int | bytes) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: int | slice) -> int | bytes:
        return self._data[key]

    def __iter__(self) -> Iterator[int]:
        return iter(self._data)

    def resize(self, capacity: int) -> None:
        """ Re-sizes the :class:`Stream` field by appending zero bytes or
        removing bytes from the end.

        :param int capacity: :class:`Stream` capacity in number of bytes.
        """
        if isinstance(self._data, Stream):
            self._data.resize(capacity)


class StringRelativePointer(StreamRelativePointer):
    """ The :class:`StringRelativePointer` field is a
    :class:`StreamRelativePointer` field which refers to a :class:`String` field.

    :param int capacity: is the *capacity* of the :class:`String` field in bytes.
    :param int|None address: relative address of the :attr:`data` object
        referenced by the `RelativePointer` field.
    :param int bit_size: is the *size* of the `RelativePointer` field in bits,
        can be between ``1`` and ``64``.
    :param int|None align_to: aligns the `RelativePointer` field to the number
        of bytes, can be between ``1`` and ``8``.
        If no field *alignment* is set the `RelativePointer` field aligns itself
        to the next matching byte size according to the *size* of the
        `RelativePointer` field.
    :param field_order: byte order used to unpack and pack the :attr:`value`
        of the `RelativePointer` field.
    :type field_order: Byteorder|Literal['auto', 'big', 'little']

    Example:

    >>> pointer = StringRelativePointer()
    >>> pointer.is_decimal()
    True
    >>> pointer.is_pointer()
    True
    >>> pointer.name
    'Pointer32'
    >>> pointer.alignment
    Alignment(byte_size=4, bit_offset=0)
    >>> pointer.byte_order
    Byteorder.auto = 'auto'
    >>> pointer.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> pointer.index_field()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.bit_size
    32
    >>> pointer.signed
    False
    >>> pointer.min()
    0
    >>> pointer.max()
    4294967295
    >>> pointer.base_address
    0
    >>> pointer.address
    0
    >>> pointer.is_null()
    True
    >>> pointer.as_signed()
    0
    >>> pointer.as_unsigned()
    0
    >>> pointer.data
    String(index=Index(byte=0, bit=0, address=0, base_address=0, update=False),
           alignment=Alignment(byte_size=0, bit_offset=0),
           bit_size=0,
           value='')
    >>> pointer.data_size
    0
    >>> len(pointer)
    0
    >>> pointer.data_byte_order
    Byteorder.little = 'little'
    >>> pointer.bytestream
    ''
    >>> pointer.value
    '0x0'
    >>> bytes(pointer)
    b'\\x00\\x00\\x00\\x00'
    >>> int(pointer)
    0
    >>> float(pointer)
    0.0
    >>> hex(pointer)
    '0x0'
    >>> bin(pointer)
    '0b0'
    >>> oct(pointer)
    '0o0'
    >>> bool(pointer)
    False
    >>> pointer.deserialize(bytes.fromhex('00c0'))
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
    >>> pointer.serialize(bytestream)
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> bytestream.hex()
    'ffffffff'
    >>> pointer.resize(10)
    >>> pointer.data_size
    10
    >>> len(pointer)
    10
    >>> pointer.bytestream = b'KonFoo is Fun'
    >>> pointer.bytestream
    '4b6f6e466f6f2069732046756e'
    >>> pointer.serialize_data().hex()
    '00000000000000000000'
    >>> pointer.deserialize_data()
    Index(byte=10, bit=0, address=4294967305, base_address=0, update=False)
    >>> pointer.serialize_data()
    b'KonFoo is '
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
    >>> pointer.describe()  #doctest: +SKIP
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
     'member': [
        {'address': 4294967295,
         'alignment': [10, 0],
         'class': 'String10',
         'index': [0, 0],
         'name': 'data',
         'order': 'auto',
         'size': 80,
         'type': 'Field',
         'value': 'KonFoo is '}
     ]}
    >>> pointer.index_fields()
    Index(byte=4, bit=0, address=4, base_address=0, update=False)
    >>> pointer.view_fields()
    {'value': '0xffffffff', 'data': 'KonFoo is '}
    >>> pointer.to_json()
    '{"value": "0xffffffff", "data": "KonFoo is "}'
    >>> pointer.field_items()
    [('field',
      StringRelativePointer(index=Index(byte=0, bit=0,
                                        address=0, base_address=0,
                                        update=False),
                            alignment=Alignment(byte_size=4, bit_offset=0),
                            bit_size=32,
                            value='0xffffffff')),
     ('data',
      String(index=Index(byte=0, bit=0,
                         address=4294967295, base_address=0,
                         update=False),
             alignment=Alignment(byte_size=10, bit_offset=0),
             bit_size=80,
             value='KonFoo is '))]
    >>> pointer.to_list()
    [('StringRelativePointer.field', '0xffffffff'),
     ('StringRelativePointer.data', 'KonFoo is ')]
    >>> pointer.to_dict()
    {'StringRelativePointer': {'field': '0xffffffff', 'data': 'KonFoo is '}}
    """

    def __init__(self,
                 capacity: int = 0,
                 address: int | None = None,
                 bit_size: int = 32,
                 align_to: int | None = None,
                 field_order: (Literal['auto', 'big', 'little'] |
                               Byteorder) = 'auto') -> None:
        super().__init__(capacity=0,
                         address=address,
                         bit_size=bit_size,
                         align_to=align_to,
                         field_order=field_order)
        self._data: String = String(capacity)
