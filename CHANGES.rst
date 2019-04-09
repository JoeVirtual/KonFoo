Changelog
=========

Here you can see the full list of changes between each KonFoo release.

Version 1.1.dev1 (Unreleased)
-----------------------------

Enhancements
~~~~~~~~~~~~

* Extended methods :meth:`Structure.view_fields`, :meth:`Sequence.view_fields`
  and :meth:`Pointer.view_fields` with keyword `fieldnames` to support customized
  fieldnames for the selected field *attributes*.
* Extended method :meth:`Container.to_json` with keyword `fieldnames` to support
  customized fieldnames for the selected field *attributes*.


Backward-incompatible Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Maintenance
~~~~~~~~~~~


Bug Fixes
~~~~~~~~~

* Fixed the :class:`Structure` class that the built-in :func:`help` function works
  correctly on an instance of :class:`Structure`.
* Fixed :class:`Structure` to raise the correct :class:`AttributeError` exception
  instead of an :class:`KeyError` exception when an unknown attribute is accessed.


Version 1.0 (Released 2019-01-02)
---------------------------------

* First release.
