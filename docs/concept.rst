.. currentmodule:: konfoo

.. _introduction:

Introduction
============

.. _concept:

Concept
-------

KonFoo is based on defining or declaring *byte stream mapper* through classes.
KonFoo has two abstract base classes the :class:`Field` class and the
:class:`Container` class.

A :class:`Field` holds the value of a area in a byte stream which the `Field`
maps and knows how to unpack and pack its value from and to a byte stream.

A :class:`Container` holds `Field` and/or `Container` classes and knows how to
view, save and load the values of the `Field` items in a `Container` class.

The mixin :class:`Pointer` class has both features of the two base classes and
has an interface to a data :class:`Provider` to read and write byte streams
from and back to the data `Provider` for its referenced *byte stream mapper*.

The build-in decoding and encoding engine unpacks and packs the byte stream
sequential to and from each `Field` in the declared *byte stream mapper*.

How does a *byte stream mapper* look like.
Let's us begin with defining or declaring a template for one.
