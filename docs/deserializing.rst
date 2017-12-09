.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from konfoo import *


.. _de-serializing:

De-Serializing
==============


De-Serializing Hook
-------------------



De-Serializing Patterns
-----------------------

Resizing on the fly
~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :emphasize-lines: 13, 17

    class OPCString(Structure):

        def __init__(self):
            super().__init__()
            # Length of the string
            self.length = Decimal16()
            # Content of the string
            self.content = String()
            self.index_fields()

        def deserialize(self, buffer=bytes(), index=Index(), **options):
            # Reset content field size on the fly.
            self.content.resize(0)
            # Deserialize complete structure.
            index = super().deserialize(buffer, index, **options)
            # Re-size content field on the fly.
            self.content.resize(int(self.length))
            # Deserialize the content field.
            index = self.content.deserialize(buffer, index, **options)
            return index

Updating on the fly
~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :emphasize-lines: 15, 19

    class OPCString(Structure):

        def __init__(self):
            super().__init__()
            # Length of the string
            self.length = Decimal16()
            # Content of the string
            self.content = String()
            self.index_fields()

        def deserialize(self, buffer=bytes(), index=Index(), **options):
            # Deserialize length field first.
            index = self.length.deserialize(buffer, index, **options)
            # Check if content field size is incorrect.
            if int(self.length) != len(self.content):
                # Re-size content field on the fly.
                self.content.resize(int(self.length))
                # Request a buffer update from the providing pointer on the fly.
                return index._replace(update=True)
            else:
                # Deserialize content field with correct size.
                return self.content.deserialize(buffer, index, **options)


Declaring on the fly
~~~~~~~~~~~~~~~~~~~~

