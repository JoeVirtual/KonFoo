# KonF'00'

KonFoo is a Python package for fighting the confusion with the foo of
the all too well-known memory dumps or binary data in a declarative way
with as little code as necessary.

It's configurable but comes with sensible defaults out of the box.

It aims to make the process of reading, decoding, viewing, encoding and
writing binary data from and back to a data source as easy as possible.

KonFoo in points:

- declarative way to describe the mapping of binary data
- declarative templates to map, read, decode, encode and write binary data
- nesting of templates
- adaptable templates on the fly while reading/decoding binary data
- easy syntax for accessing nested template fields
- loadable template content including the nested data from an INI file
- savable template content including the nested data to an INI file
- template conversion to a json styled python dictionary
- adapter to provide a JSON file to view the declared structure with
  the d3.js java script library

This library is far away from stable but it works so far. Feedback is very welcomed!
