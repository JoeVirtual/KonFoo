.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from binascii import hexlify
    from konfoo import *


.. _introduction:

Introduction
============

**KonFoo** is a Python package for de-serializing *byte streams* into a meaningful
representation. KonFoo helps you to deserialize a *byte stream* retrievable through
a *byte stream* :ref:`provider <provider>` to any kind of data source into a
meaningful representation by just declaring how the parts of a *byte stream*
should be represented, respectively mapped to :ref:`fields <field>`.

You can store the representation into an ``.ini`` file to analyse the *byte
stream* data.

The built-in deserialize hook ``deserialize(buffer=bytes(), index=Index(), **option)``
available for all `container`_ and `field`_ classes allows you to adapt even
expand or declare the representation during the de-serialization process on the fly.

The built-in **deserializer** provided by the :ref:`pointer <pointer>` class
(called through the :meth:`Pointer.read_from` method) is able to follow even nested
absolute or relative pointers to retrieve the *byte stream* from the *byte stream*
:ref:`provider <provider>` necessary for its referenced :ref:`data object <data object>`
and to de-serialize (map) it.

After de-serializing the *byte stream* provided by the *byte stream* :ref:`provider
<provider>` the built-in **serializer** provided also by the :ref:`pointer <pointer>`
class (called through the :meth:`Pointer.write_to` method) is able to transfer the
manipulated values of any `container`_ or `field`_ in the representation back to the
*byte stream* :ref:`provider <provider>` to write it into its data source.

Concept
=======

KonFoo is based on defining or declaring a *byte stream* `mapper`_ (representation)
through classes. KonFoo has two abstract base classes the `container`_ class and
the `field`_ class.

A `container`_ contains `field`_ and/or `container`_ classes and knows how to
**view**, **save** and **load** the *values* of the `field`_ **items** within
the `container`_.

A `field`_ represents the *value* of a content area in a *byte stream* which
the `field`_ maps and knows how to **unpack** and **pack** its *value* from and
to a *byte stream*.

The mixin :ref:`pointer <pointer>` class has both features of the two base classes
and has an interface to a *byte stream* :ref:`provider <provider>` to **read**
and **write** *byte streams* from and back to the *byte stream*
:ref:`provider <provider>` for its referenced :ref:`data object <data object>`
respectively its *byte stream* `mapper`_.

The built-in **deserializer** and **serializer** unpacks and packs the *byte stream*
sequential to and from each `field`_ in the declared *byte stream* `mapper`_.


.. _mapper:

Mapper
======

A *byte stream* `mapper`_ consists of a collection of `container`_ and `field`_
members, whereby the `container`_ members describe the structure and the `field`_
members describe the content of one or more memory areas in a *data source*.
The mix-in :ref:`pointer <pointer>` field serves in combination with a *byte stream*
:ref:`provider <provider>` as an entry point to a *data source* for the *byte
stream* `mapper`_ to deserialize and serialize its *byte stream*.


.. _container:

Containers
==========

The role of a :class:`Container` is to describe the *structure* of one or more
memory areas in a *data source*. A `container`_ always needs one or more
:ref:`fields <field>` to describe the content of the memory area.


Overview
--------

Here is an overview of the different available `container`_ classes.

* :class:`Structure`
* :class:`Sequence`, :class:`Array`
* :class:`Pointer`, :class:`StructurePointer`, :class:`SequencePointer`,
  :class:`ArrayPointer`, :class:`StreamPointer`, :class:`StringPointer`,
  :class:`AutoStringPointer`
* :class:`RelativePointer`, :class:`StructureRelativePointer`,
  :class:`SequenceRelativePointer`, :class:`ArrayRelativePointer`,
  :class:`StreamRelativePointer`, :class:`StringRelativePointer`

View Field Attributes
---------------------

A `container`_ can **view** the *attributes* of each `field`_ *nested* in the
`container`_ by calling its method :meth:`~Container.view_fields`.
Default attribute is the field :attr:`~Field.value`.

    >>> # Create an empty container.
    >>> container = Container()
    >>> # View the field values in the container.
    >>> container.view_fields()

.. note::
    The *attributes* of each `field`_ for containers *nested* in the `container`_
    are viewed as well (chained method call).

View as a JSON String
---------------------

A `container`_ can **view** the *attributes* of each `field`_ *nested* in the
`container`_ as a **JSON** formatted string by calling its method
:meth:`~Container.to_json`.
Default attribute is the field :attr:`~Field.value`.

    >>> container.to_json()
    'null'

.. note::
    The *attributes* of each `field`_ for containers *nested* in the `container`_
    are viewed as well (chained method call).


List Field Items
----------------

A `container`_ can list all its `field`_ items *nested* in the `container`_
as a **flatten** list in the form of ``('field path', field item)`` tuples
by calling its method :meth:`~Container.field_items`.

    >>> # List the field items in the container.
    >>> container.field_items()
    []


List Field Attributes
---------------------

A `container`_ can **list** the *attributes* of each `field`_ item *nested* in the
`container`_ as a **flatten** list in the form of ``('field path', attribute)`` or
``('field path', list(attributes))`` tuples by calling its method
:meth:`~Container.to_list`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values in the container.
    >>> container.to_list()
    []


A `container`_ can **list** the *attributes* of each `field`_ item *nested* in the
`container`_ as a **flatten** ordered dictionary in the form of
``{'field path': attribute}`` or ``{'field path': list(attributes)}`` pairs
by calling its method :meth:`~Container.to_dict`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values in the container.
    >>> container.to_dict()
    OrderedDict([('Container', OrderedDict())])


A `container`_ can **list** the *attributes* of each `field`_ item *nested* in the
`container`_ as a **flatten** list of dictionaries containing the field *path* and
the selected field *attributes* by calling its method :meth:`~Container.to_csv`.
Default attribute is the field :attr:`~Field.value`.

    >>> # List the field values in the container.
    >>> container.to_csv()
    []

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Write Field Attributes
----------------------

A `container`_ can **write** the *attributes* of each `field`_ item *nested* in the
`container`_ to a ``.csv`` file by calling its method :meth:`~Container.write_csv`.
Default attribute is the field :attr:`~Field.value`.

    >>> # Save the field values to an '.csv' file.
    >>> container.write_csv("_static/container.csv")

The generated ``.csv`` file for the container looks like this:

.. literalinclude:: _static/container.csv

.. note::
    The class name of the instance is used for the root name as long as no
    *name* is given.


Save Field Attributes
---------------------

A `container`_ can **save** the *attributes* of each `field`_ item *nested* in the
`container`_ to an ``.ini`` file by calling its method :meth:`~Container.save`.
Default attribute is the field :attr:`~Field.value`.

    >>> # Save the field values to an '.ini' file.
    >>> container.save("_static/container.ini")

The generated ``.ini`` file for the container looks like this:

.. literalinclude:: _static/container.ini
    :language: ini

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.


Load Field Values
-----------------

A `container`_ can **load** the *value* of each `field`_ item *nested* in the
`container`_ from an ``.ini`` file by calling its method :meth:`~Container.load`.

    >>> # Load the field values from an '.ini' file.
    >>> container.load("_static/container.ini")
    [Container]

.. note::
    The class name of the instance is used for the section name as long as no
    *section* is given.


.. _field:

Fields
======

The role of a :class:`Field` is to map a specific content area of a *byte stream*.
A `field`_ is always placed in a `container`_ except from a :ref:`pointer <pointer>`
field which is the entry point for a `mapper`_ to connect the attached
:ref:`data object <data object>` via a *byte stream* :ref:`provider <provider>` to
a *data source* to retrieve the required *byte stream* for the `mapper`_.

    >>> # Create a field.
    >>> field = Field()
    >>> # Display the field.
    >>> field
    Field(index=Index(byte=0, bit=0,
                      address=0, base_address=0,
                      update=False),
          alignment=Alignment(byte_size=0, bit_offset=0),
          bit_size=0,
          value=None)


Overview
--------

Here is an overview of the different available `field`_ classes.

* :class:`Stream`, :class:`String`
* :class:`Float`, :class:`Double`
* :class:`Decimal` :class:`Bit`, :class:`Byte`, :class:`Char`, :class:`Signed`,
  :class:`Unsigned`, :class:`Bitset`, :class:`Bool`, :class:`Enum`,
  :class:`Scaled`, :class:`Fraction`, :class:`Bipolar`, :class:`Unipolar`,
  :class:`Datetime`, :class:`IPv4Address`
* :class:`Pointer`, :class:`StructurePointer`, :class:`SequencePointer`,
  :class:`ArrayPointer`:class:`StreamPointer`, :class:`StringPointer`,
  :class:`AutoStringPointer`
* :class:`RelativePointer`, :class:`StructureRelativePointer`,
  :class:`SequenceRelativePointer`, :class:`ArrayRelativePointer`,
  :class:`StreamRelativePointer`, :class:`StringRelativePointer`


.. _field name:

Name
----

A `field`_ has a type :attr:`~Field.name`. The `field name`_ consists of the
name of the `field`_ base class and its `field size`_ to describe the kind of
the `field`_.

    >>> # Field name.
    >>> field.name
    'Field0'


.. _field size:

Size
----

A `field`_ has a :attr:`~Field.bit_size`. The `field size`_ defines the size of
the content area of a *byte stream* that the `field`_ map.

    >>> # Field bit size.
    >>> field.bit_size
    0

.. _field value:

Value
-----

A `field`_ has a :attr:`~Field.value`. The `field value`_ represents the content
area of a *byte stream* that the `field`_ map.

    >>> # Field value.
    >>> field.value


.. _field index:

Index
-----

A `field`_ has an :attr:`~Field.index`. The `field index`_ contains the location
of the `field`_ in a *byte stream* and in the providing *data source*. The `field
index`_ is automatically calculated by the built-in deserializer and serializer
from the start point of the *byte stream* and the start address of the *byte
stream* in the providing *data source*.

    >>> # Field index.
    >>> field.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)
    >>> # Field index: byte offset of the field in the byte stream.
    >>> field.index.byte
    0
    >>> # Field index: bit offset of the field relative to its byte offset.
    >>> field.index.bit
    0
    >>> # Field index: memory address of the field in the data source.
    >>> field.index.address
    0
    >>> # Field index: start address of the byte stream in the data source.
    >>> field.index.base_address
    0
    >>> # Field index: update request for the byte stream.
    >>> field.index.update
    False


.. _field alignment:

Alignment
---------

A `field`_ has an :attr:`~Field.alignment`. The `field alignment`_ contains the
location of the `field`_ within an *aligned* group of consecutive fields. The
order how the consecutive fields are declared in a `container`_ defines the
order how the consecutive fields are aligned to each other. The ``bit offset``
of the `field alignment`_ is automatically calculated by the built-in
deserializer and serializer.

    >>> # Field alignment.
    >>> field.alignment
    Alignment(byte_size=0, bit_offset=0)
    >>> byte_size, bit_offset = field.alignment
    >>> # Field alignment: byte size of the aligned field group.
    >>> byte_size
    0
    >>> # Field alignment: bit offset of the field in its field group.
    >>> bit_offset
    0

A `field`_ can be *aligned to* a group of consecutive fields by using the
``align_to`` argument of the :class:`Field` class to describe an **atomic**
content part of a *byte stream* with more than one `field`_.

    >>> Decimal(15).alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> Bool(1, align_to=2).alignment
    Alignment(byte_size=2, bit_offset=0)

.. note::
    A `field`_ aligns it self to the next matching byte size when the
    `field size`_ matches not full bytes and no `field alignment`_ is given.

For example to describe an **atomic** 16-bit value in a *byte stream* with
more than one `field`_ can be achieved like this:

    >>> # Create an empty structure for the atomic 16-bit value.
    >>> atomic = Structure()
    >>> # Add field for the first 15 bits of an atomic 16-bit value.
    >>> atomic.size = Decimal(15, 2)
    >>> # Add field for the last bit of an atomic 16-bit value.
    >>> atomic.flag = Bool(1, 2)
    >>> # Index the fields of the atomic 16-bit value.
    >>> atomic.index_fields()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> # Display alignment of the size field.
    >>> atomic.size.alignment
    Alignment(byte_size=2, bit_offset=0)
    >>> # Display alignment of the flag field.
    >>> atomic.flag.alignment
    Alignment(byte_size=2, bit_offset=15)


.. note:: The `field alignment`_ works only for the :class:`Decimal` `field`_
          classes.


.. _field byte order:

Byte order
----------

A `field`_ defines its own decoding/encoding :attr:`~Field.byte_order`. The
default `field byte order`_ is :class:`~Byteorder.auto` it means that
the `field`_ use the byte order which the *byte stream* `mapper`_ defines to
:attr:`~Field.unpack` and :attr:`~Field.pack` the required bytes and bits for
its `field value`_ from and to the *byte stream*.

    >>> # Field byte order.
    >>> field.byte_order
    Byteorder.auto = 'auto'
    >>> # Field byte order value.
    >>> field.byte_order.value
    'auto'


.. _enumeration:

Enumeration
-----------

The *name* instead of the *value* of an enumeration can be displayed with the
:class:`Enum` `field`_ class by assigning an :class:`Enumeration` class to the
:class:`Enum` `field`_.

For example to describe a 2-bit ambivalent enumeration by an :class:`Enum`
`field`_ can be achieved like this:

    >>> # Define the enumeration class.
    >>> class Validity(Enumeration):
    ...     error = 0
    ...     correct = 1
    ...     forced = 2
    ...     undefined = 3
    >>> # Create an enum field and assign an enumeration to the field.
    >>> ambivalent = Enum(2, enumeration=Validity)
    >>> # Display the value of the field.
    >>> ambivalent.value
    'error'
    >>> # Returns the field value as an integer.
    >>> int(ambivalent)
    0
    >>> # Display the field.
    >>> ambivalent
    Enum(index=Index(byte=0, bit=0,
                     address=0, base_address=0,
                     update=False),
         alignment=Alignment(byte_size=1, bit_offset=0),
         bit_size=2,
         value='error')
