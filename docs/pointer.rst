.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *

.. _pointer_declaration:

Pointer declaration
===================

KonFoo has a :class:`Pointer` class to reference ...
The :class:`RelativePointer` ...

KonFoo provides specialized pointers for :class:`Structures <StructurePointer>`,
:class:`Sequences <SequencePointer>`, :class:`Arrays <ArrayPointer>`,
:class:`Streams <StreamPointer>`  and :class:`Strings <StringPointer>` which have
additional features for their referenced data objects.


.. _create_pointer:

Create a pointer declaration
----------------------------

Define a mapper template.

.. code-block:: python

    # Structure declaration
    class Container(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal32()
            self.item = Pointer()
            self.next_index()

Define a reference of a mapper template.

.. code-block:: python

    # Referenced structure declaration
    class ContainerPointer(StructurePointer):

        def __init__(self, address=None):
            super().__init__(Container(), address)  # <- Structure declaration

Declare a mapper instance.

    >>> mapper = Structure()
    >>> mapper.size = Decimal32()
    >>> mapper.item = Pointer()
    >>> pprint(mapper.to_dict(nested=True)) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Structure', OrderedDict([('size', 0),
                                            ('item', '0x0')]))])

Declare a reference of the mapper instance via a pointer.

    >>> pointer = Pointer(mapper)
    >>> pprint(pointer.to_dict(nested=True))
    {'Pointer': {'value': '0x0',
                 'data.size': 0,
                 'data.item': '0x0'}}

Declare a reference of the mapper instance via a specialized pointer for
structures.

    >>> pointer = StructurePointer(mapper)
    >>> pprint(pointer.to_dict(nested=True))
    {'StructurePointer': {'value': '0x0',
                          'data.size': 0,
                          'data.item': '0x0'}}

.. _nested_reference:

Nesting a pointer declaration
-----------------------------

Define a mapper template with a nested pointer.

.. code-block:: python

    # Structure declaration
    class Container(Structure):

        def __init__(self):
            super().__init__()
            self.size = Decimal32()
            self.item = Pointer(Stream())  # nested pointer

Declare a mapper instance with a nested pointer.

    >>> mapper = Structure()
    >>> mapper.size = Decimal32()
    >>> mapper.item = Pointer(Stream())
    >>> pprint(mapper.to_dict(nested=True)) # doctest: +NORMALIZE_WHITESPACE
    {'Structure': OrderedDict([('size', 0),
                               ('item', '0x0'),
                               ('item.data', b'')])}
