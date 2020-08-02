Changelog
=========

Here you can see the full list of changes between each KonFoo release.


Version 2.0 (Unreleased)
------------------------

Enhancements
~~~~~~~~~~~~

* Using :class:`dict` instead of :class:`~collections.OrderedDict` to improve
  readability.
* Add method :meth:`Container.write_json` to write to a ``.json`` file.

Incompatible Changes
~~~~~~~~~~~~~~~~~~~~

* Drop support for Python 3.5


Version 1.1 (Released 2019-10-27)
---------------------------------

Enhancements
~~~~~~~~~~~~

* Add a :class:`Double` field class to map a double precision float value
  within a byte stream.
* Extend methods :meth:`Structure.view_fields`, :meth:`Sequence.view_fields`
  and :meth:`Pointer.view_fields` with keyword `fieldnames` to support customized
  fieldnames for the selected field *attributes*.
* Extend method :meth:`Container.to_json` with keyword `fieldnames` to support
  customized fieldnames for the selected field *attributes*.

Bug Fixes
~~~~~~~~~

* Fix syntax warnings to support Python 3.8 correctly.
* Fix :class:`Structure` to raise the correct :class:`AttributeError` exception
  instead of a :class:`KeyError` exception when an unknown attribute is accessed.
* Fix the :class:`Structure` class that the built-in :func:`help` function works
  correctly on an instance of :class:`Structure`.


Version 1.0 (Released 2019-01-02)
---------------------------------

* First release.
