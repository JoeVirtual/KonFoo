.. _introduction:

Introduction
============

**KonFoo** is a Python package for de-serializing *byte streams* into a meaningful
representation.

**KonFoo** helps you to deserialize a *byte stream* retrievable through a
*byte stream* :ref:`provider <provider>` to any kind of data source into a
meaningful representation by just declaring how the parts of a *byte stream*
should be represented, respectively mapped to :ref:`fields <field>`.

You can store the representation into an ``.ini`` file to analyse the
*byte stream* data.

The built-in deserialize hook ``deserialize(buffer=bytes(), index=Index(), **option)``
available for all :ref:`container <container>` and :ref:`field <field>` classes
allows you to adapt even expand or declare the representation during the
de-serialization process on the fly.

The built-in **deserializer** provided by the :ref:`pointer <pointer>` class
(called through the :meth:`Pointer.read_from` method) is able to follow even
nested absolute or relative pointers to retrieve the *byte stream* from the
*byte stream* :ref:`provider <provider>` necessary for its referenced
:ref:`data object <data object>` and to de-serialize (map) it.

After de-serializing the *byte stream* provided by the *byte stream*
:ref:`provider <provider>` the built-in **serializer** provided also by the
:ref:`pointer <pointer>` class (called through the :meth:`Pointer.write_to` method)
is able to transfer the manipulated values of any :ref:`container <container>`
or :ref:`field <field>` in the representation back to the *byte stream*
:ref:`provider <provider>` to write it into its data source.
