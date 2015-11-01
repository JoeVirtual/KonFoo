.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *

.. _array_template:

Array template
==============

KonFoo has a :class:`Array` class to declare ...



.. _array_element:

Array element
-------------

A :class:`Array` element can be any :class:`Field` or :class:`Container` class.


Define a template
-----------------

Define a array in a template by calling the array element constructor.

.. code-block:: python

    # Template
    class EntryList(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal32()
            self.entry = Array(Decimal32, 5)  # Array


Define a array in a template by using a array element instance.

.. code-block:: python

    # Template
    class List(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal32()
            self.entry = Array(Decimal32(), 5) # Array


Define a array in a template by calling a factory class or function.

.. code-block:: python

    # Factory for the array element template
    class Factory:
        def __init__(self, size):
            self.size = size

        def __call__(self):
            return String(size)

.. code-block:: python

    # Template
    class List(Structure):

        def __init__(self):
            super().__init__()
            self.length = Decimal32()
            self.entry = Array(Factory(10), 5)  # Array
