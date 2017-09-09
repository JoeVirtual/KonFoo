# KonF'00'

[![Docs](https://readthedocs.org/projects/konfoo/badge/?version=latest)](http://konfoo.readthedocs.org/en/latest/)
[![Build](https://travis-ci.org/JoeVirtual/KonFoo.svg?branch=master)](https://travis-ci.org/JoeVirtual/KonFoo)
[![PyPi](https://img.shields.io/pypi/v/KonFoo.svg)](https://pypi.python.org/pypi/KonFoo)

KonFoo is a Python Package for creating byte stream mappers in a declarative
way with as little code as necessary to help fighting the confusion with the
foo of the all well-known memory dumps or hexadecimal views of binary data.

It comes with sensible defaults out of the box.

It aims to make the process of reading, decoding (deserializing), viewing, 
encoding (serializing) and writing binary data from and back to a data provider 
as easy as possible.

KonFoo in points:

-   declarative way to describe the mapping of binary data
-   declarative classes to map, read, decode/deserialize, encode/serialize
    and write binary data from and back to a data source
-   easy adjustable data provider bridge to any kind of data source
-   nesting of classes
-   adaptable classes on the fly while reading/decoding binary data
-   easy syntax for accessing nested fields
-   loadable mapping content including nested data from an INI file
-   savable mapping content including nested data to an INI file
-   easy creatable blueprint of a mapper
-   blueprint converter to JSON to visualise the mapper with 
    [d3.js](https://d3js.org).

This library is far away from stable but it works so far.
Feedback is very welcomed!


## Installation

To install the library from [PyPi](https://pypi.python.org/pypi) through 
[pip](https://pip.pypa.io) simply run

    pip install konfoo
    

To install the library manually download the source package from 
[github](https://github.com/JoeVirtual/KonFoo) and simply run the `setup.py` 
script within the package.

    python setup.py install


## Dependencies

The library has no external dependencies.


## Building the Documentation

Requires [sphinx](http://www.sphinx-doc.org) and the theme 
[read the docs](https://github.com/snide/sphinx_rtd_theme),
which are available through pip.

    pip install sphinx
    pip install sphinx_rtd_theme
    
Then it's a simple matter of running `make docs` in the package folder or
in the `docs` folder with `make html`. The generated html documentation can be
found in the `./docs/_build/html` folder of the source package.
