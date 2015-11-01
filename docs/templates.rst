.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from binascii import hexlify
    from konfoo import *

.. _template:

Templates
=========


.. _template_member:

Member
------



.. _field_byte_order:

Byte order
----------

Each :class:`Field` defines its own decoding/encoding byte order. The default
byte order of a field is :class:`~Byteorder.auto` this means that the field use
the byte order which the byte stream defines to unpack and pack the required
bytes and bits for its field value from and to the byte stream.


.. _field_alignment:

Alignment
---------

:class:`Fields <Field>` can be aligned to each other ...


.. _field_enumeration:

Enumerations
------------



.. _blueprint:

Blueprints
----------
