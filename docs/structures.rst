.. _structures:

Structures
==========

.. currentmodule:: konfoo

Structures ...


Declaring
---------

Example:

.. code-block:: python

    class Identifier(Structure):

        def __init__(self):
            super().__init__()
            self.version = Byte(4)
            self.id = Unsigned(8, 4)
            self.length = Decimal(8, 4)
            self.module = Char(4)


Nesting
-------

Example:

.. code-block:: python

    class Header(Structure):

        def __init__(self):
            super().__init__()
            self.info = Identifier()
