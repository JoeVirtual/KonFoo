.. currentmodule:: konfoo

.. testsetup:: *

    from konfoo import *


.. _de-serializing:

De-Serializing
==============

The de-serialization of a *byte stream* by a *byte stream* :ref:`mapper <mapper>`
is not considered independent from the :ref:`reading <reading>` of the *byte stream*.

Therefore the :meth:`deserialize` method of the *byte stream* :ref:`mapper <mapper>`
is not called directly during the de-serialization process. The :meth:`deserialize`
method is called by the :ref:`pointer <pointer>` during the :ref:`reading <reading>`
of the *byte stream* where the *byte stream* :ref:`mapper <mapper>` is attached to.


De-Serializing Hook
-------------------

The :meth:`~Field.deserialize` method which every :ref:`field <field>` and
:ref:`container <container>` has allows to hook in the reading/de-serialization
process at a certain point of the *byte stream* to adapt the *byte stream*
:ref:`mapper<mapper>` and to control the :ref:`reading <reading>` of the
:ref:`byte stream <data object byte stream>` by the providing
:ref:`pointer <pointer>`.


    >>> class OPCString(Structure):
    ...
    ...     def __init__(self):
    ...         super().__init__()
    ...         # Length of the string
    ...         self.length = Decimal16()
    ...         # Content of the string
    ...         self.content = String()
    ...         self.index_fields()
    ...
    ...     def deserialize(self, buffer=bytes(), index=Index(), **options):
    ...         # Deserialize length field first.
    ...         index = self.length.deserialize(buffer, index, **options)
    ...         # Check if content field size is incorrect.
    ...         if int(self.length) != len(self.content):
    ...             # Re-size content field on the fly.
    ...             self.content.resize(int(self.length))
    ...             # Deserialize content field with new size.
    ...             index = self.content.deserialize(buffer, index, **options)
    ...             # Request a buffer update from the providing pointer on the fly.
    ...             # note: Starts the deserialization for the byte stream mapper again.
    ...             return index._replace(update=True)
    ...         else:
    ...             # Deserialize content field with correct size.
    ...             return self.content.deserialize(buffer, index, **options)

    >>> # Create an instance of the empty OPC string
    >>> string = OPCString()
    >>> # List the field values of the OPC string.
    >>> string.to_list()
    [('OPCString.length', 0),
     ('OPCString.content', '')]
    >>> # List the field values of the OPC string as a CSV list.
    >>> string.to_csv()
    [{'id': 'OPCString.length', 'value': 0},
     {'id': 'OPCString.content', 'value': ''}]
    >>> # View the OPC string field values as a JSON string.
    >>> string.to_json()
    '{"length": 0, "content": ""}'
    >>> # Size of the OPC string.
    >>> string.container_size()
    (2, 0)

    >>> # Deserialize the empty OPC string
    >>> string.deserialize(bytes.fromhex('0f004b6f6e466f6f206973202746756e27'))
    Index(byte=17, bit=0, address=17, base_address=0, update=True)
    >>> # Size of the OPC string.
    >>> string.container_size()
    (17, 0)

    >>> # Deserialize the filled OPC string
    >>> string.deserialize(bytes.fromhex('0f004b6f6e466f6f206973202746756e27'))
    Index(byte=17, bit=0, address=17, base_address=0, update=False)
    >>> # Size of the OPC string.
    >>> string.container_size()
    (17, 0)

    >>> # List the field values of the OPC string.
    >>> string.to_list()
    [('OPCString.length', 15),
     ('OPCString.content', "KonFoo is 'Fun'")]
    >>> # List the field values of the OPC string as a CSV list.
    >>> string.to_csv()
    [{'id': 'OPCString.length', 'value': 15},
     {'id': 'OPCString.content', 'value': "KonFoo is 'Fun'"}]
    >>> # View the OPC string field values as a JSON string.
    >>> string.to_json()
    '{"length": 15, "content": "KonFoo is \'Fun\'"}'