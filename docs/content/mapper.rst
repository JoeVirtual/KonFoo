.. _mapper:

Mapper
======

A *byte stream* `mapper`_ consists of a collection of :ref:`container <container>`
and :ref:`field <field>` members, whereby the :ref:`container <container>` members
describe the structure, and the :ref:`field <field>` members describe the content
of one or more memory areas in a *data source*.

The mix-in :ref:`pointer <pointer>` field serves in combination with a *byte
stream* :ref:`provider <provider>` as an **entry point** to a *data source* for
the *byte stream* `mapper`_ to deserialize and serialize its *byte stream*.
