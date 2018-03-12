# -*- coding: utf-8 -*-
"""
.. |Doc Status| image:: https://readthedocs.org/projects/konfoo/badge/?version=latest
    :target: http://konfoo.readthedocs.io/en/latest/?badge=latest
.. |Build Status| image:: https://travis-ci.org/JoeVirtual/KonFoo.svg?branch=master
    :target: https://travis-ci.org/JoeVirtual/KonFoo
.. |PyPI| image:: https://img.shields.io/pypi/v/KonFoo.svg
    :target: https://pypi.python.org/pypi/KonFoo/
.. |License| image:: https://img.shields.io/pypi/l/KonFoo.svg
    :target: https://pypi.python.org/pypi/KonFoo
.. |Python| image:: https://img.shields.io/pypi/pyversions/KonFoo.svg
    :target: https://pypi.python.org/pypi/KonFoo
.. |Binder| image:: https://mybinder.org/badge.svg
    :target: https://mybinder.org/v2/gh/JoeVirtual/KonFoo/master?filepath=notebooks

KonF'00'
========

|Doc Status| |Build Status| |PyPI| |License| |Python| |Binder|

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
- easy adjustable data provider bridge to any kind of data source
- nesting of classes
- adaptable classes on the fly while reading/de-serializing binary data
- easy syntax for accessing nested fields
- loadable mapping content including nested data from an ``.ini`` file
- savable mapping content including nested data to an ``.ini`` file
- easy creatable blueprint of a mapper
- blueprint converter to JSON to visualise the mapper with
  `d3.js <https://d3js.org>`_.

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

import re
import ast

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('konfoo/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='KonFoo',
    version=version,
    license='BSD',
    author='Jochen Gerhaeusser',
    author_email='jochen_privat@gmx.de',
    url='http://github.com/JoeVirtual/KonFoo',
    download_url='http://github.com/JoeVirtual/KonFoo/zipball/master#egg=konfoo-dev',
    description='A declarative byte stream mapping engine.',
    long_description=__doc__,
    keywords='byte binary data deserialize serialize parse decode encode unpack pack',
    packages=['konfoo'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[],
    python_requires='>=3.4',
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Testing',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Scientific/Engineering :: Visualization',
    ]
)
