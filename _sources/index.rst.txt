.. currentmodule:: konfoo

.. |status| image:: https://img.shields.io/pypi/status/konfoo.svg
   :target: https://pypi.org/project/konfoo
.. |docs| image:: https://readthedocs.org/projects/konfoo/badge/?version=latest
   :target: https://konfoo.readthedocs.io
.. |pypi| image:: https://img.shields.io/pypi/v/konfoo.svg
   :target: https://pypi.org/project/konfoo
.. |python| image:: https://img.shields.io/pypi/pyversions/konfoo.svg
   :target: https://docs.python.org/3
.. |license| image:: https://img.shields.io/pypi/l/konfoo.svg
   :target: https://github.com/JoeVirtual/konfoo/blob/master/LICENSE
.. |downloads| image:: https://img.shields.io/pypi/dm/konfoo.svg
   :target: https://pypistats.org/packages/konfoo
.. |binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/JoeVirtual/konfoo/master?labpath=notebooks

.. _d3js: https://d3js.org/

|status| |docs| |pypi| |python| |license| |downloads|

Welcome to the KonF'00' Documentation
=====================================

|binder|

**KonFoo** is a Python Package for creating byte stream mappers in a declarative
way with as little code as necessary to help fighting the confusion with the
foo of the all well-known memory dumps or hexadecimal views of binary data.

It comes with sensible defaults out of the box.

It aims to make the process of reading, de-serializing, viewing, serializing
and writing binary data from and back to a *byte stream* provider as easy as
possible.

**KonFoo** in points:

* declarative way to describe the mapping of binary data to Python types
* declarative classes to read, deserialize, view, serialize and write binary
  data from and back to a data source
* easy adjustable *byte stream* provider bridge to any kind of data source
* nesting of classes
* adaptable classes on the fly while reading/de-serializing binary data
* easy syntax for accessing nested fields
* view the mapped binary data as a JSON string
* list the mapped binary data as a flatten list or dictionary
* write the mapped binary data to a ``.json`` file
* write the mapped binary data to a ``.csv`` file
* save the mapped binary data to an ``.ini`` file
* load the mapped binary data from an ``.ini`` file
* easy creatable nested metadata dictionaries of the members of a byte stream mapper
* metadata converter to the ``flare.json`` format to visualise the mapper with `d3js`_.

**KonFoo** runs on `Python 3.6 <https://www.python.org/>`_ or higher.

You can get the latest version of **KonFoo** directly from GitHub:

    `KonFoo @ github <https://github.com/JoeVirtual/KonFoo/>`_

You can get the library directly from PyPI:

.. code-block:: console

    > pip install konfoo

.. toctree::
   :caption: Content
   :maxdepth: 2
   :hidden:

   content/intro
   content/concept
   content/mapper
   content/containers
   content/fields

.. toctree::
   :maxdepth: 2
   :caption: Containers
   :hidden:

   containers/structure
   containers/sequence
   containers/array


.. toctree::
   :maxdepth: 2
   :caption: Pointers
   :hidden:

   pointers/index

.. toctree::
   :maxdepth: 2
   :caption: Providers
   :hidden:

   providers/index

.. toctree::
   :maxdepth: 2
   :caption: Bytestream
   :hidden:

   bytestream/reading
   bytestream/writing
   bytestream/deserializing

.. toctree::
   :maxdepth: 4
   :caption: Reference
   :hidden:

   api/index

.. toctree::
   :maxdepth: 2
   :caption: Annex
   :hidden:

   annex/changelog
   annex/license
   annex/contributing

.. toctree::
   :maxdepth: 1
   :caption: Indexes
   :hidden:

   genindex
