# -*- coding: utf-8 -*-
"""
.. |Doc Status| image:: https://readthedocs.org/projects/konfoo/badge/?version=latest
    :target: http://konfoo.readthedocs.io/en/latest/?badge=latest
.. |Build Status| image:: https://travis-ci.org/JoeVirtual/KonFoo.svg?branch=master
    :target: https://travis-ci.org/JoeVirtual/KonFoo
.. |PyPI| image:: https://img.shields.io/pypi/v/KonFoo.svg
    :target: https://pypi.org/project/KonFoo
.. |License| image:: https://img.shields.io/pypi/l/KonFoo.svg
    :target: https://pypi.org/project/KonFoo
.. |Python| image:: https://img.shields.io/pypi/pyversions/KonFoo.svg
    :target: https://pypi.org/project/KonFoo
.. |Status| image:: https://img.shields.io/pypi/status/KonFoo.svg
    :target: https://pypi.org/project/KonFoo
.. |Binder| image:: https://mybinder.org/badge.svg
    :target: https://mybinder.org/v2/gh/JoeVirtual/KonFoo/master?filepath=notebooks

KonF'00'
========

|Doc Status| |Build Status| |PyPI| |License| |Python| |Status| |Binder|

KonFoo is a Python Package for creating byte stream mappers in a declarative
way with as little code as necessary to help fighting the confusion with the
foo of the all too well-known memory dumps or hexadecimal views of binary
data.

It comes with sensible defaults out of the box.

It aims to make the process of reading, de-serializing, viewing, serializing
and writing binary data from and back to a data provider as easy as possible.

KonFoo in points:

- declarative way to describe the mapping of binary data to Python types
- declarative classes to read, deserialize, serialize and write binary data
  from and back to a data source
- easy adjustable byte stream provider bridge to any kind of data source
- nesting of classes
- adaptable classes on the fly while reading/de-serializing binary data
- easy syntax for accessing nested fields
- view the mapped binary data as a JSON string
- list the mapped binary data as a flatten list or dictionary
- write the mapped binary data to a ``.csv`` file
- save the mapped binary data to an ``.ini`` file
- load the mapped binary data from an ``.ini`` file
- easy creatable nested metadata dictionaries of the members of a byte stream mapper
- metadata converter to the ``flare.json`` format to visualise the mapper with
  `d3.js <https://d3js.org>`_.


Example
-------

A short example how to define a byte stream mapper.

>>> from konfoo import *

>>> class Identifier(Structure):
...     def __init__(self):
...         super().__init__()
...         self.version = Byte(align_to=4)
...         self.id = Unsigned(8, align_to=4)
...         self.length = Decimal(8, align_to=4)
...         self.module = Char(align_to=4)
...         self.index_fields()
>>> class HeaderV1(Structure)
...     def __init__(self):
...         super().__init__()
...         self.type = Identifier()
>>> class HeaderV2(HeaderV1)
...     def __init__(self):
...         super().__init__()
...         self.size = Decimal(16)
>>> header = HeaderV2()
>>> header.to_list()
[('Structure.type.version', '0x0'),
 ('Structure.type.id', '0x0'),
 ('Structure.type.length', 0),
 ('Structure.type.module', '\x00'),
 ('Structure.size', 0)]
>>> header.type.to_csv()
[{'id': 'Identifier.version', 'value': '0x0'},
 {'id': 'Identifier.id', 'value': '0x0'},
 {'id': 'Identifier.length', 'value': 0},
 {'id': 'Identifier.module', 'value': '\x00'}]
>>> header.to_json()
'{"type": {"version": "0x0", "id": "0x0", "length": 0, "module": "\\u0000"},
  "size": 0}'
>>> header.deserialize(bytes.fromhex('0102094610'))
>>> header.to_json()
'{"type": {"version": "0x1", "id": "0x2", "length": 9, "module": "F"},
  "size": 16}'
>>> bytes(header).hex()
'0102094610'

>>> header = Structure(
...     type=Structure(version=Byte(4),
...                    id=Unsigned(8, 4),
...                    length=Decimal(8, 4),
...                    module=Char(4)),
...     size=Decimal(16))
>>> header.to_list()
[('Structure.type.version', '0x0'),
 ('Structure.type.id', '0x0'),
 ('Structure.type.length', 0),
 ('Structure.type.module', '\x00'),
 ('Structure.size', 0)]
>>> header.type.to_csv()
[{'id': 'Structure.version', 'value': '0x0'},
 {'id': 'Structure.id', 'value': '0x0'},
 {'id': 'Structure.length', 'value': 0},
 {'id': 'Structure.module', 'value': '\x00'}]
>>> header.to_json()
'{"type": {"version": "0x0", "id": "0x0", "length": 0, "module": "\\u0000"},
  "size": 0}'
>>> header.deserialize(bytes.fromhex('0102094610'))
>>> header.to_json()
'{"type": {"version": "0x1", "id": "0x2", "length": 9, "module": "F"},
  "size": 16}'
>>> bytes(header).hex()
'0102094610'


Installing
----------

.. code-block:: bash

    > pip install konfoo

Links
-----

* `Code <http://github.com/JoeVirtual/KonFoo/>`_
* `Documentation <http://konfoo.readthedocs.io>`_
* `Development version
  <http://github.com/JoeVirtual/KonFoo/zipball/master#egg=konfoo-dev>`_

"""

import io
import os
import re

from setuptools import setup


def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def version(path):
    """ Obtain the package version from a python file e.g. pkg/__init__.py

    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


VERSION = version('konfoo/__init__.py')


setup(
    name='KonFoo',
    version=VERSION,
    license='BSD',
    author='Jochen Gerhaeusser',
    author_email='jochen_privat@gmx.de',
    url='http://github.com/JoeVirtual/KonFoo',
    download_url='http://github.com/JoeVirtual/KonFoo/zipball/master#egg=konfoo-dev',
    description='A declarative byte stream mapping engine.',
    long_description=__doc__,
    keywords='binary data deserialize serialize parse decode encode unpack pack',
    packages=['konfoo'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[],
    python_requires='>=3.5',
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Testing',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Scientific/Engineering :: Visualization',
    ]
)
