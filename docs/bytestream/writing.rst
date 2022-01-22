.. currentmodule:: konfoo

.. testsetup:: *

    from konfoo import *

.. _writing:

Writing
=======


Create the Byte Stream Provider
-------------------------------

First, create the *byte stream* :ref:`provider <provider>` to access the
*data source*.

    >>> # Create the byte stream provider for the data source.
    >>> provider = FileProvider('./_static/writing.bin')
    >>> provider.cache
    bytearray(b"\x0f\x00KonFoo is \'Fun\'")

.. note::
    We use here a :class:`FileProvider` but you can write your own
    :ref:`provider <provider>` class to access any kind of *data source*.


Create the Byte Stream Mapper
-----------------------------

Second, create the *byte stream* :ref:`mapper <mapper>` for the *binary data*
to be mapped in the *data source*.

    >>> # Create the byte stream mapper.
    >>> mapper = Structure(length = Decimal16(), content = String(15))


Create the Byte Stream Writer
-----------------------------

Third, create a *writer* for the *byte stream* :ref:`mapper <mapper>` to the
*data source* by attaching the *byte stream* :ref:`mapper <mapper>` to the
:ref:`data object <data object>` of a :ref:`pointer <pointer>` field.

    >>> # Create the byte stream writer.
    >>> writer = Pointer(mapper)
    >>> # List the field values of the pointer and data object.
    >>> writer.to_list()
    [('Pointer.field', '0x0'),
     ('Pointer.data.length', 0),
     ('Pointer.data.content', '')]
    >>> # List the field values of the pointer and data object as a CSV list.
    >>> writer.to_csv()
    [{'id': 'Pointer.field', 'value': '0x0'},
     {'id': 'Pointer.data.length', 'value': 0},
     {'id': 'Pointer.data.content', 'value': ''}]
    >>> # View the pointer and data object field values as a JSON string.
    >>> writer.to_json()
    '{"value": "0x0",
      "data": {"length": 0, "content": ""}}'


Read from the Data Source
-------------------------

Fourth, **read** the required :ref:`byte stream <data object byte stream>` for the
:ref:`data object <data object>` attached to the :ref:`pointer <pointer>` field with
the *byte stream* :ref:`provider <provider>` **from** the *data source* by calling
the method :meth:`~Pointer.read_from` of the :ref:`pointer <pointer>` field.

    >>> # Read from the provider the byte stream
    >>> writer.read_from(provider, null_allowed=True)
    >>> bytes.fromhex(writer.bytestream)
    b"\x0f\x00KonFoo is 'Fun'"

    >>> # List the field values of the data object.
    >>> writer.data.to_list()
    [('Structure.length', 15),
     ('Structure.content', "KonFoo is 'Fun'")]
    >>> # List the field values of the data object as a CSV list.
    >>> writer.data.to_csv()
    [{'id': 'Structure.length', 'value': 15},
     {'id': 'Structure.content', 'value': "KonFoo is 'Fun'"}]
    >>> # View the data object field values as a JSON string.
    >>> writer.data.to_json()
    '{"length": 15, "content": "KonFoo is \'Fun\'"}'


Write to the Data Source
------------------------

Fifth, **write** the field :ref:`value <field value>` of any :ref:`field <field>`
of the :ref:`data object <data object>` attached to a :ref:`pointer <pointer>`
**to** a *data source* with the *byte stream* :ref:`provider <provider>` by
calling method :meth:`~Pointer.write_to`.

    >>> writer.data.length.value = 0x0f00
    >>> # Write to the provider the bytes represented by the field.
    >>> writer.write_to(provider, writer.data.length)
    >>> provider.cache
    bytearray(b"\x00\x0fKonFoo is \'Fun\'")
    >>> bytes.fromhex(writer.bytestream)
    b"\x0f\x00KonFoo is 'Fun'"


or **write** the field :ref:`values <field value>` of any :ref:`container <container>`
of the :ref:`data object <data object>` attached to a :ref:`pointer <pointer>`
**to** a *data source* with the *byte stream* :ref:`provider <provider>` by
calling method :meth:`~Pointer.write_to`.

    >>> writer.data.length.value = 14
    >>> writer.data.content.value = 'Konfoo is Fun'
    >>> # Write to the provider the bytes represented by the container.
    >>> writer.write_to(provider, writer.data)
    >>> provider.cache
    bytearray(b'\x0e\x00Konfoo is Fun\x00\x00')
    >>> bytes.fromhex(writer.bytestream)
    b"\x0f\x00KonFoo is 'Fun'"
