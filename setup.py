"""
KonF'00'
~~~~~~~~

KonFoo is a Python Package for creating byte stream mappers in a declarative
way with as little code as necessary to help fighting the confusion with the
foo of the all too well-known memory dumps or hexadecimal views of binary
data.

Setup
-----

.. code:: bash
    $ pip install KonFoo

Links
-----
* `website <http://github.com/JoeVirtual/KonFoo/>`_
* `documentation <http://github.com/JoeVirtual/KonFoo/master/docs/>`_
* `development version
  <http://github.com/JoeVirtual/KonFoo/master>`_


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
    author_email='jochen.gerhaeusser@freenet.de',
    url='http://github.com/JoeVirtual/KonFoo',
    description='A declarative byte stream mapping engine.',
    long_description=__doc__,
    packages=['konfoo'],
    install_requires=[],
    classifiers=[
        'License :: BSD License',
        'Programming Language :: Python :: 3',
    ]
)
