# -*- coding: utf-8 -*-
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

    > pip install konfoo

Links
-----
* `website <http://github.com/JoeVirtual/KonFoo/>`_
* `documentation <http://konfoo.readthedocs.org>`_
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
    author_email='jochen_privat@gmx.de',
    url='http://github.com/JoeVirtual/KonFoo',
    description='A declarative byte stream mapping engine.',
    long_description=__doc__,
    packages=['konfoo'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 1 - Planning',
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
        'Topic :: Software Development',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Scientific/Engineering :: Visualization',
    ]
)
