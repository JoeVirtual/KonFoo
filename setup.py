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

KonF'00'
========

|Doc Status| |Build Status| |PyPI| |License| |Python|

KonFoo is a Python Package for creating byte stream mappers in a declarative
way with as little code as necessary to help fighting the confusion with the
foo of the all too well-known memory dumps or hexadecimal views of binary
data.

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
    keywords='binary data deserialize serialize parsing decoding encoding',
    packages=['konfoo'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[],
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
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Scientific/Engineering :: Visualization',
    ]
)
