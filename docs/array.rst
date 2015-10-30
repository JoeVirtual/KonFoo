.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *

.. _array_declaration:

Array declaration
=================

KonFoo has a :class:`Array` class to declare ...


A `Array` element can be any :class:`Field`  or :class:`Container` class.


Declare a array with a array element declaration
------------------------------------------------

Define a array element template.

.. code-block:: python

    #  Declaration for a array element
    class Element(Structure):

        def __init__(self):
            super().__init__()
            self.id = Decimal16()
            self.name = String(10)


Declare a array in a mapper by calling the array element constructor.

.. code-block:: python

    # Structure declaration
    class EntryList(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal32()
            self.entry = Array(Element, 5)  # Array declaration


.. _factorized_array:

Declare a array with a array element factory
--------------------------------------------

Define a factory for a array element template.

.. code-block:: python

    # Factory for a array element declaration
    class ElementFactory:
        def __init__(self, size):
            self.size = size

        def __call__(self):
            return String(size)


Declare a array in a mapper by using a array element factory.

.. code-block:: python

    # Structure declaration
    class List(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal32()
            self.entry = Array(ElementFactory(10), 5)  # Array declaration


Declare a array with a array element instance
---------------------------------------------

Declare a array in mapper by using a array element instance.

.. code-block:: python

    # Structure declaration
    class List(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal32()
            self.entry = Array(String(10), 5)  # Array declaration
