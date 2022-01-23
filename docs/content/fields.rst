.. currentmodule:: konfoo

.. testsetup:: *

    from konfoo import *

.. _field:

Fields
======

The role of a :class:`Field` is to map a specific content area of a *byte stream*.

A `field`_ is always placed in a :ref:`container <container>` except from a
:ref:`pointer <pointer>` field which is the **entry point** for a
:ref:`mapper <mapper>` to connect the attached :ref:`data object <data object>`
via a *byte stream* :ref:`provider <provider>` to a *data source* to retrieve
the required *byte stream* for the :ref:`mapper <mapper>` .

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

The list below shows the available `field`_ classes.

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

A `field`_ has a type :attr:`~Field.name`.

The `field name`_ consists of the name of the `field`_ base class and its
`field size`_ to describe the kind of the `field`_.

    >>> # Field name.
    >>> field.name
    'Field0'

.. _field size:

Size
----

A `field`_ has a :attr:`~Field.bit_size`.

The `field size`_ defines the size of the content area of a *byte stream* that
the `field`_ map.

    >>> # Field bit size.
    >>> field.bit_size
    0

.. _field value:

Value
-----

A `field`_ has a :attr:`~Field.value`.

The `field value`_ represents the content area of a *byte stream* that the
`field`_ map.

    >>> # Field value.
    >>> field.value

.. _field index:

Index
-----

A `field`_ has an :attr:`~Field.index`.

The `field index`_ contains the location of the `field`_ in a *byte stream* and
in the providing *data source*.

The `field index`_ is automatically calculated by the built-in deserializer and
serializer from the start point of the *byte stream* and the start address of
the *byte stream* in the providing *data source*.

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

A `field`_ has an :attr:`~Field.alignment`.

The `field alignment`_ contains the location of the `field`_ within an *aligned*
group of consecutive fields.

The order how the consecutive fields are declared in a :ref:`container <container>`
defines the order how the consecutive fields are aligned to each other.

The ``bit offset`` of the `field alignment`_ is automatically calculated by the
built-in deserializer and serializer.

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

  A `field`_ aligns it self to the next matching byte size when the `field size`_
  matches not full bytes and no `field alignment`_ is given.

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

.. note::

   The `field alignment`_ works only for the :class:`Decimal` `field`_ classes.

.. _field byte order:

Byte order
----------

A `field`_ defines its own decoding/encoding :attr:`~Field.byte_order`.

The default `field byte order`_ is :class:`~Byteorder.auto` it means that the
`field`_ use the byte order which the *byte stream* :ref:`mapper <mapper>`
defines to :attr:`~Field.unpack` and :attr:`~Field.pack` the required bytes and
bits for its `field value`_ from and to the *byte stream*.

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
