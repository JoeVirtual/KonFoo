.. currentmodule:: konfoo

.. testsetup:: *

    from konfoo import *

.. _container:

Containers
==========

The role of a :class:`Container` is to describe the *structure* of one or more
memory areas in a *data source*.

A `container`_ always needs one or more :ref:`fields <field>` to describe the
content of the memory area.

Overview
--------

The list below shows the available `container`_ classes.

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

A `container`_ can **view** the *attributes* of each :ref:`field <field>`
*nested* in the `container`_ by calling its method
:meth:`~Container.view_fields`.

The default attribute is the field :attr:`~Field.value`.

    >>> # Create an empty container.
    >>> container = Container()

    >>> # View the field values in the container.
    >>> container.view_fields()

.. note::

  The *attributes* of each :ref:`field <field>` for containers *nested* in the
  `container`_ are viewed as well (chained method call).

View as a JSON String
---------------------

A `container`_ can **view** the *attributes* of each :ref:`field <field>`
*nested* in the `container`_ as a **JSON** formatted string by calling its
method :meth:`~Container.to_json`.

The default attribute is the field :attr:`~Field.value`.

    >>> container.to_json()
    'null'

.. note::

  The *attributes* of each :ref:`field <field>` for containers *nested* in the
  `container`_ are viewed as well (chained method call).

List Field Items
----------------

A `container`_ can list all its :ref:`field <field>` items *nested* in the
`container`_ as a **flatten** list in the form of ``('field path', field item)``
tuples by calling its method :meth:`~Container.field_items`.

    >>> # List the field items in the container.
    >>> container.field_items()
    []

List Field Attributes
---------------------

A `container`_ can **list** the *attributes* of each :ref:`field <field>` item
*nested* in the `container`_ as a **flatten** list in the form of
``('field path', attribute)`` or ``('field path', list(attributes))`` tuples by
calling its method :meth:`~Container.to_list`.

The default attribute is the field :attr:`~Field.value`.

    >>> # List the field values in the container.
    >>> container.to_list()
    []

A `container`_ can **list** the *attributes* of each :ref:`field <field>` item
*nested* in the `container`_ as a **flatten** dictionary in the form of
``{'field path': attribute}`` or ``{'field path': list(attributes)}`` pairs
by calling its method :meth:`~Container.to_dict`.

The default attribute is the field :attr:`~Field.value`.

    >>> # List the field values in the container.
    >>> container.to_dict()
    {'Container': {}}

A `container`_ can **list** the *attributes* of each :ref:`field <field>` item
*nested* in the `container`_ as a **flatten** list of dictionaries containing
the field *path* and the selected field *attributes* by calling its method
:meth:`~Container.to_csv`.

The default attribute is the field :attr:`~Field.value`.

    >>> # List the field values in the container.
    >>> container.to_csv()
    []

.. note::

  The class name of the instance is used for the root name as long as no *name*
  is given.

Write Field Attributes
----------------------

A `container`_ can **write** the *attributes* of each :ref:`field <field>` item
*nested* in the `container`_ to a ``.csv`` file by calling its method
:meth:`~Container.write_csv`.

The default attribute is the field :attr:`~Field.value`.

    >>> # Save the field values to an '.csv' file.
    >>> container.write_csv("./_static/container.csv")

The generated ``.csv`` file for the container looks like this:

.. literalinclude:: ../_static/container.csv

.. note::

  The class name of the instance is used for the root name as long as no *name*
  is given.

Save Field Attributes
---------------------

A `container`_ can **save** the *attributes* of each :ref:`field <field>` item
*nested* in the `container`_ to an ``.ini`` file by calling its method
:meth:`~Container.save`.

The default attribute is the field :attr:`~Field.value`.

    >>> # Save the field values to an '.ini' file.
    >>> container.save("./_static/container.ini")

The generated ``.ini`` file for the container looks like this:

.. literalinclude:: ../_static/container.ini
   :language: ini

.. note::

  The class name of the instance is used for the section name as long as no
  *section* is given.

Load Field Values
-----------------

A `container`_ can **load** the *value* of each :ref:`field <field>` item
*nested* in the `container`_ from an ``.ini`` file by calling its method
:meth:`~Container.load`.

    >>> # Load the field values from an '.ini' file.
    >>> container.load("./_static/container.ini")
    [Container]

.. note::

  The class name of the instance is used for the section name as long as no
  *section* is given.
