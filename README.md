**[Installation](#installation)** |
**[Dependencies](#dependencies)** |
**[Documentation](#documentation)**

# KonF'00'

[![Docs](https://readthedocs.org/projects/konfoo/badge/?version=latest)](https://konfoo.readthedocs.io)
[![Build](https://travis-ci.org/JoeVirtual/KonFoo.svg?branch=master)](https://travis-ci.org/JoeVirtual/KonFoo)
[![PyPi](https://img.shields.io/pypi/v/KonFoo.svg)](https://pypi.org/project/KonFoo)
![Lisence](https://img.shields.io/pypi/l/KonFoo.svg)
![Python](https://img.shields.io/pypi/pyversions/KonFoo.svg)
![Status](https://img.shields.io/pypi/status/KonFoo.svg)
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/JoeVirtual/KonFoo/master?filepath=notebooks)

KonFoo is a Python Package for creating byte stream mappers in a declarative
way with as little code as necessary to help fighting the confusion with the
foo of the all well-known memory dumps or hexadecimal views of binary data.

It comes with sensible defaults out of the box.

It aims to make the process of reading, de-serializing, viewing, serializing 
and writing binary data from and back to a data provider as easy as possible.

KonFoo in points:

* declarative way to describe the mapping of binary data to Python types
* declarative classes to read, deserialize, view, serialize and write binary 
  data from and back to a data source
* easy adjustable byte stream provider bridge to any kind of data source
* nesting of classes
* adaptable classes on the fly while reading/de-serializing binary data
* easy syntax for accessing nested fields
* view the mapped binary data as a JSON string
* list the mapped binary data as a flatten list or dictionary
* write the mapped binary data to a `.csv` file
* save the mapped binary data to an `.ini` file
* load the mapped binary data from an `.ini` file
* easy creatable nested metadata dictionaries of the members of a byte stream mapper
* metadata converter to the `flare.json` format to visualise the mapper with 
  [d3.js](https://d3js.org).

This library is stable. Feedback is very welcomed!


## Installation

To install the library from [PyPi](https://pypi.org) through 
[pip](https://pip.pypa.io) simply run

    pip install konfoo
    

To install the library manually download the source package from 
[github](https://github.com/JoeVirtual/KonFoo) and simply run the `setup.py` 
script within the package.

    python setup.py install


## Dependencies

The library has no external dependencies.


## Documentation

Read the documentation on [ReadTheDocs](https://konfoo.readthedocs.io).

### Building the Documentation

Requires [sphinx](http://www.sphinx-doc.org) and the theme 
[read the docs](https://github.com/snide/sphinx_rtd_theme),
which are available through pip.

    pip install sphinx
    pip install sphinx_rtd_theme
    
Then it's a simple matter of running `make docs` in the package folder or
in the `docs` folder with `make html`. The generated html documentation can be
found in the `./docs/_build/html` folder of the source package.
