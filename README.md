# KonF'00'

[![Docs](https://readthedocs.org/projects/konfoo/badge/?version=latest)](http://konfoo.readthedocs.org/en/latest/)
[![Build](https://travis-ci.org/JoeVirtual/KonFoo.svg?branch=master)](https://travis-ci.org/JoeVirtual/KonFoo)

KonFoo is a Python Package for creating byte stream mappers in a declarative
way with as little code as necessary to help fighting the confusion with the
foo of the all well-known memory dumps or hexadecimal views of binary data.

It comes with sensible defaults out of the box.

It aims to make the process of reading, decoding, viewing, encoding and
writing binary data from and back to a data provider as easy as possible.

KonFoo in points:

-   declarative way to describe the mapping of binary data
-   declarative template classes to map, read, decode, encode and write binary data
-   nesting of template classes
-   adaptable template classes on the fly while reading/decoding binary data
-   easy syntax for accessing nested template fields
-   loadable template content including the nested data from an INI file
-   savable template content including the nested data to an INI file
-   creatable blueprints from a template class
-   blueprint converter to JSON to visualise templates with *d3.js*.

This library is far away from stable but it works so far.
Feedback is very welcomed!
