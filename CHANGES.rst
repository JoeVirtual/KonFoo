Changelog
=========

Here you can see the full list of changes between each KonFoo release.

Version 1.1a0 (Unreleased)
--------------------------

Enhancements
~~~~~~~~~~~~

* Added a new :class:`Double` field class to map a double precision float value
  within a byte stream.
* Extended methods :meth:`Structure.view_fields`, :meth:`Sequence.view_fields`
  and :meth:`Pointer.view_fields` with keyword `fieldnames` to support customized
  fieldnames for the selected field *attributes*.
* Extended method :meth:`Container.to_json` with keyword `fieldnames` to support
  customized fieldnames for the selected field *attributes*.

Bug Fixes
~~~~~~~~~

* Fixed warnings to support Python 3.8.
* Fixed :class:`Structure` to raise the correct :class:`AttributeError` exception
  instead of a :class:`KeyError` exception when an unknown attribute is accessed.
* Fixed the :class:`Structure` class that the built-in :func:`help` function works
  correctly on an instance of :class:`Structure`.


Version 1.0 (Released 2019-01-02)
---------------------------------

* First release.
