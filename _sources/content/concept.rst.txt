.. _concept:

Concept
=======

**KonFoo** is based on defining or declaring a *byte stream*
:ref:`mapper <mapper>` (representation) through classes.

**KonFoo** has two abstract base classes the :ref:`container <container>` class
and the :ref:`field <field>` class.

A :ref:`container <container>` contains :ref:`field <field>` and/or
:ref:`container <container>` classes and knows how to **view**, **save** and
**load** the *values* of the :ref:`field <field>` **items** within the
:ref:`container <container>`.

A :ref:`field <field>` represents the *value* of a content area in a *byte
stream* which the :ref:`field <field>` maps and knows how to **unpack** and
**pack** its *value* from and to a *byte stream*.

The mix-in :ref:`pointer <pointer>` class has both features of the two base
classes and has an interface to a *byte stream* :ref:`provider <provider>` to
**read** and **write** *byte streams* from and back to the *byte stream*
:ref:`provider <provider>` for its referenced :ref:`data object <data object>`,
respectively its *byte stream* :ref:`mapper <mapper>`.

The built-in **deserializer** and **serializer** unpacks and packs the
*byte stream* sequential to and from each :ref:`field <field>` in the declared
*byte stream* :ref:`mapper <mapper>`.
