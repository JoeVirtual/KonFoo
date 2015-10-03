.. image:: _static/logo.png
   :align: right
   :alt: Logo


Welcome to the KonF'00' Documentation
=====================================

KonFoo is a Python Package for creating byte stream mappers in a declarative
way with as little code as necessary to help fighting the confusion with the
foo of the all well-known memory dumps or hexadecimal views of binary data.

It comes with sensible defaults out of the box.

It aims to make the process of reading, decoding, viewing, encoding and
writing binary data from and back to a data provider as easy as possible.

KonFoo in points:

-   declarative way to describe the mapping of binary data
-   declarative template classes to map, read, decode, encode and write
    binary data
-   nesting of template classes
-   adaptable template classes on the fly while decoding binary data
-   easy syntax for accessing nested template fields
-   loadable template content including nested data from an INI file
-   savable template content including nested data to an INI file
-   creatable blueprints from a template class
-   blueprint converter to JSON to visualise templates with *d3.js*.


You can get the library directly from PyPI::

    pip install konfoo


Examples
---------

Examples of KonFoo can be found in the documentation as well
as in the GitHub repository together with readme files:

*   ``d3``: `d3
    <https://github.com/JoeVirtual/KonFoo/tree/master/examples/d3>`_


Documentation Contents
----------------------

This part of the documentation guides you through all of the library's
usage patterns.

.. toctree::
   :maxdepth: 2

   concept


API Reference
-------------

If you are looking for information on a specific function, class, or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 4

   api

Miscellaneous Pages
-------------------

.. toctree::
   :maxdepth: 2

   changelog
   upgrading
   license


