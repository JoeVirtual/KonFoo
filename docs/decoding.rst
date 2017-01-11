.. currentmodule:: konfoo

.. testsetup:: *

    from pprint import pprint
    from binascii import hexlify, unhexlify
    from konfoo import *

.. _decoding:

Decoding
========


Decoding Hook
-------------



Decoding Patterns
-----------------

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
            self.next_index()

        def decode(self, buffer=bytes(), index=zero(), **options):
            # Reset content field size on the fly.
            self.content.resize(0)
            # Decode complete structure.
            index = super().decode(buffer, index, **options)
            # Re-size content field on the fly.
            self.content.resize(self.length.value)
            # Decode the content field.
            index = self.content.decode(buffer, index, **options)
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
            self.next_index()

        def decode(self, buffer=bytes(), index=zero(), **options):
            # Decode length field first.
            index = self.length.decode(buffer, index, **options)
            # Check if content field size is incorrect.
            if self.length.value != len(self.content):
                # Re-size content field on the fly.
                self.content.resize(self.length.value)
                # Request a buffer update from the providing pointer on the fly.
                return index._replace(update=True)
            else:
                # Decode content field with correct size.
                return self.content.decode(buffer, index, **options)


Declaring on the fly
~~~~~~~~~~~~~~~~~~~~

