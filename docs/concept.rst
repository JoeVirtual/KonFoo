.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from binascii import hexlify
    from konfoo import *


.. _introduction:

Introduction
============

**KonFoo** is a Python package for de-serializing *byte streams* into a meaningful
representation. KonFoo helps you to deserialize a *byte stream* retrievable
through a data :ref:`provider <provider>` to any kind of data source into a
meaningful representation by just declaring how the parts of a *byte stream*
should be represented, respectively mapped to :ref:`fields <field>`.

You can store the representation into an ``.ini`` file to analyse the *byte
stream* data.

The built-in deserialize hook ``deserialize(buffer=bytes(), index=Index(), **option)``
available for all `container`_ and `field`_ classes allows you to adapt even
expand or declare the representation during the de-serialization on the fly.

The built-in **deserializer** provided by the :ref:`pointer <pointer>` class
(called through the :meth:`Pointer.read_from` method) is able to follow even
nested absolute or relative pointers to retrieve the *byte stream* from the
data :ref:`provider <provider>` necessary for its referenced :ref:`data object
<data object>` and to de-serialize (map) it.

After de-serializing the *byte stream* provided by the data :ref:`provider
<provider>` the built-in **serializer** provided also by the :ref:`pointer
<pointer>` class (called through the :meth:`Pointer.write_to` method) is able
to transfer the manipulated values of any `container`_ or `field`_ in the
representation back to the data :ref:`provider <provider>` to write it into its
data source.

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

The mixin :ref:`pointer <pointer>` class has both features of the two base
classes and has an interface to a data :ref:`provider <provider>` to **read**
and **write** *byte streams* from and back to the data :ref:`provider <provider>`
for its referenced :ref:`data object <data object>` respectively its *byte
stream* `mapper`_.

The build-in **deserializer** and **serializer** unpacks and packs the *byte
stream* sequential to and from each `field`_ in the declared *byte stream*
`mapper`_.


.. _mapper:

Mapper
======

A *byte stream* `mapper`_ consists of a collection of `container`_ and `field`_
members, whereby the `container`_ members describe the structure and the `field`_
members describe the content of one or more memory areas in a *data source*.
The mix-in :ref:`pointer <pointer>` field serves in combination with a data
:ref:`provider <provider>` as an entry point to a *data source* for the *byte
stream* `mapper`_ to deserialize and serialize its *byte stream*.


.. _container:

Containers
==========

The role of a :class:`Container` is to describe the *structure* of one or more
memory areas in a *data source*. A `container`_ always needs one or more
`field`_ 's to describe the content of the memory area.


Overview
--------

Here is an overview of the different available `container`_ classes.

* :class:`Structure`
* :class:`Sequence`, :class:`Array`
* :class:`Pointer`, :class:`StructurePointer`, :class:`SequencePointer`,
  :class:`ArrayPointer`:class:`StreamPointer`, :class:`StringPointer`,
  :class:`AutoStringPointer`
* :class:`RelativePointer`, :class:`StructureRelativePointer`,
  :class:`SequenceRelativePointer`, :class:`ArrayRelativePointer`,
  :class:`StreamRelativePointer`, :class:`StringRelativePointer`


List field items
----------------

A `container`_ can list all its `field`_ items as a **flat** list in the form
of ``(field path, field item)`` tuples by calling its method
:meth:`~Container.field_items`.

    >>> container = Container()
    >>> container.field_items() # doctest: +NORMALIZE_WHITESPACE
    []


View field values
-----------------

A `container`_ can **view** the *value* of each `field`_ item as a **flat**
list in the form of ``(field path, field value)`` tuples by calling its method
:meth:`~Container.to_list`.

    >>> container.to_list() # doctest: +NORMALIZE_WHITESPACE
    []


A `container`_ can **view** the *value* of each `field`_ item as a **flat**
ordered dictionary in the form of ``{'field path': field value}`` pairs by
calling its method :meth:`~Container.to_dict`.

    >>> container.to_dict()  # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Container', OrderedDict())])


.. note::

    The class name of the instance is used for the root name as long as no
    *name* is given.


Save field values
-----------------

A `container`_ can **save** the *value* of each `field`_ item to an INI file
by calling its method :meth:`~Container.save`.

    >>> container.save("_static/container.ini")

.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


Load field values
-----------------

A `container`_ can **load** the *value* of each `field`_ item from an INI file
by calling its method :meth:`~Container.load`.

    >>> container.load("_static/container.ini")
    [Container]


.. note::

    The class name of the instance is used for the section name as long as no
    *section* is given.


.. _field:

Fields
======

The role of a :class:`Field` is to map a specific content area of a *byte stream*.
A `field`_ is always placed in a `container`_ expect from a :ref:`pointer <pointer>`
field which is the entry point for a `mapper`_ to connect the attached :ref:`data
object <data object>` via a data :ref:`provider <provider>` to a *data source* to
retrieve the required *byte stream* for the `mapper`_.


    >>> field = Field()
    >>> field # doctest: +NORMALIZE_WHITESPACE
    Field(index=Index(byte=0, bit=0,
                      address=0, base_address=0,
                      update=False),
          alignment=(0, 0),
          bit_size=0,
          value=None)


Overview
--------

Here is an overview of the different available `field`_ classes.

* :class:`Stream`, :class:`String`
* :class:`Float`
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

    >>> field.name
    'Field0'


.. _field size:

Size
----

A `field`_ has a :attr:`~Field.bit_size`. The `field size`_ defines the size of
the content area of a *byte stream* that the `field`_ map.

    >>> field.bit_size
    0

.. _field value:

Value
-----

A `field`_ has a :attr:`~Field.value`. The `field value`_ represents the content
area of a *byte stream* that the `field`_ map.

    >>> field.value


.. _field index:

Index
-----

A `field`_ has an :attr:`~Field.index`. The `field index`_ contains the location
of the `field`_ in a *byte stream* and in the providing *data source*. The `field
index`_ is automatically calculated by the build-in deserializer and serializer
from the start point of the *byte stream* and the start address of the *byte
stream* in the providing *data source*.

    >>> field.index
    Index(byte=0, bit=0, address=0, base_address=0, update=False)


.. _field alignment:

Alignment
---------

A `field`_ has an :attr:`~Field.alignment`. The `field alignment`_ contains the
location of the `field`_ within an *aligned* group of consecutive fields. The
order how the consecutive fields are declared in a `container`_ defines the
order how the consecutive fields are aligned to each other. The ``bit offset``
of the `field alignment`_ is automatically calculated by the build-in
deserializer and serializer.

    >>> # field alignment
    >>> byte_size, bit_offset = field.alignment
    >>> field.alignment
    (0, 0)


A `field`_ can be *aligned to* a group of consecutive fields by using the
``align_to`` argument of the :class:`Field` class to describe an **atomic**
content part of a *byte stream* with more than one `field`_.

    >>> Decimal(15).alignment
    (2, 0)
    >>> Bool(1, align_to=2).alignment
    (2, 0)

.. note::

    A `field`_ aligns it self to the next matching byte size when the
    `field size`_ matches not full bytes and no `field alignment`_ is given.

For example to describe an **atomic** 16-bit value in a *byte stream* with
more than one `field`_ can be achieved like this:

    >>> aligned = Structure()
    >>> # First 15 bits of a 16-bit value.
    >>> aligned.size = Decimal(15, 2)
    >>> # Last bit of a 16-bit value.
    >>> aligned.flag = Bool(1, 2)
    >>> aligned.index_fields()
    Index(byte=2, bit=0, address=2, base_address=0, update=False)
    >>> # Display alignment of the size field.
    >>> aligned.size.alignment
    (2, 0)
    >>> # Display alignment of the flag field.
    >>> aligned.flag.alignment
    (2, 15)


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
    >>> ambivalent # doctest: +NORMALIZE_WHITESPACE
    Enum(index=Index(byte=0, bit=0,
                  address=0, base_address=0,
                  update=False),
      alignment=(1, 0),
      bit_size=2,
      value='error')
