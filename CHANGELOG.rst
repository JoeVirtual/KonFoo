Change Log
**********

These are the enhancements, breaking changes and bug fixes of note between each
release.

.. _v2.1.0:

`2.1.0`_ - 2022-01-27
=====================

.. _2.1.0: https://github.com/JoeVirtual/KonFoo/compare/v2.0...v2.1.0

Enhancements
------------

* Refactor repository and documentation structure
* Change documentation theme

.. _v2.0.0:

`2.0.0`_ - 2020-08-02
=====================

.. _2.0.0: https://github.com/JoeVirtual/KonFoo/compare/v1.1...v2.0

Enhancements
------------

* Use :class:`dict` instead of :class:`~collections.OrderedDict` to improve
  readability.
* Add method :meth:`Container.write_json` to write to a ``.json`` file.

Breaking Changes
----------------

* Drop support for Python 3.5

.. _v1.1.0:

`1.1.0`_ - 2019-10-27
=====================

.. _1.1.0: https://github.com/JoeVirtual/KonFoo/compare/v1.0...v1.1

Enhancements
------------

* Add a :class:`Double` field class to map a double precision float value
  within a byte stream.
* Extend methods :meth:`Structure.view_fields`, :meth:`Sequence.view_fields`
  and :meth:`Pointer.view_fields` with keyword `fieldnames` to support customized
  fieldnames for the selected field *attributes*.
* Extend method :meth:`Container.to_json` with keyword `fieldnames` to support
  customized fieldnames for the selected field *attributes*.

Bug Fixes
---------

* Fix syntax warnings to support Python 3.8 correctly.
* Fix :class:`Structure` to raise the correct :class:`AttributeError` exception
  instead of a :class:`KeyError` exception when an unknown attribute is accessed.
* Fix the :class:`Structure` class that the built-in :func:`help` function works
  correctly on an instance of :class:`Structure`.

.. _v1.0.0:

`1.0.0`_ - 2019-01-02
=====================

.. _1.0.0: https://github.com/JoeVirtual/KonFoo/compare

* First stable release.
