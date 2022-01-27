# KonF'00'

[![status](https://img.shields.io/pypi/status/konfoo.svg)](https://pypi.org/project/konfoo)
[![docs](https://readthedocs.org/projects/konfoo/badge/?version=latest)](https://konfoo.readthedocs.io)
[![pypi](https://img.shields.io/pypi/v/konfoo.svg)](https://pypi.org/project/konfoo)
[![python](https://img.shields.io/pypi/pyversions/konfoo.svg)](https://docs.python.org/3/)
[![license](https://img.shields.io/pypi/l/konfoo.svg)](https://github.com/JoeVirtual/KonFoo/blob/master/LICENSE)
[![downloads](https://img.shields.io/pypi/dm/konfoo.svg)](https://pypistats.org/packages/konfoo)
[![binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/joevirtual/konfoo/master?labpath=notebooks)

**KonFoo** is a Python Package for creating byte stream mappers in a declarative
way with as little code as necessary to help fighting the confusion with the
foo of the all well-known memory dumps or hexadecimal views of binary data.

It comes with sensible defaults out of the box.

It aims to make the process of reading, de-serializing, viewing, serializing
and writing binary data from and back to a data provider as easy as possible.

**KonFoo** in points:

* declarative way to describe the mapping of binary data to Python types
* declarative classes to read, deserialize, view, serialize and write binary
  data from and back to a data source
* easy adjustable byte stream provider bridge to any kind of data source
* nesting of classes
* adaptable classes on the fly while reading/de-serializing binary data
* easy syntax for accessing nested fields
* view the mapped binary data as a JSON string
* list the mapped binary data as a flat list or dictionary
* write the mapped binary data to a `.json` file
* write the mapped binary data to a `.csv` file
* save the mapped binary data to an `.ini` file
* load the mapped binary data from an `.ini` file
* easy creatable nested metadata dictionaries of the members of a byte stream
  mapper
* metadata converter to the `flare.json` format to visualise the mapper with
  [d3.js](https://d3js.org).

## Table of Contents
[Back to top]: #table-of-contents

1. [Project Status](#project-status)
2. [Project Structure](#project-structure)
3. [Getting Started](#getting-started)
	- [Dependencies](#dependencies)
	- [Installation](#installation)
	- [Usage](#usage)
4. [Development](#development)
	- [Getting the Source](#getting-the-source)
	- [Building a Distribution](#building-a-distribution)
	- [Building the Documentation](#building-the-documentation)
5. [Release Process](#release-process)
	- [Versioning](#versioning)
6. [Documentation](#documentation)
7. [License](#license)
8. [Authors](#authors)

## Project Status

This [project] is stable and active. Feedback is always welcomed!

**[Back to top](#table-of-contents)**

## Project Structure

The [project] is organized in sub-folders.

- `assets/`: Project assets
- `binder/`: Binder configuration
- `docs/`: [Sphinx] documentation
- `notebooks/`: [Jupyter] notebooks
- `src/konfoo/`: Package sources

**[Back to top](#table-of-contents)**

## Getting Started

### Dependencies

The `KonFoo` package requires at least [Python] 3.6, otherwise no other packages
are required.

### Installation

To install the package from [PyPi] using [pip]

```shell
> pip install konfoo
```

**[Back to top](#table-of-contents)**

### Usage

Read the documentation on "[Read The Docs]".

**[Back to top](#table-of-contents)**

## Development

### Getting the Source

This [project] is hosted on [github].
You can clone the [project]  directly using this command:

```shell
> git clone https://github.com/JoeVirtual/KonFoo.git
```

### Building a Distribution

To build local a distribution of this [project], use this command:

```shell
> make build
```

The generated the distribution artifacts can be found in the `./dist` folder
of the cloned [project] on your machine.

### Building the Documentation

Building the documentation requires [Sphinx], the [Furo] theme, and the
[Sphinx] extension [sphinx-copybutton].

```shell
> pip install sphinx
> pip install furo
> pip install sphinx-copybutton
```

To build local the documentation of this [project], use this command:

```shell
> make docs
```

The generated HTML documentation artifact can be found in the
`./docs/_build/html` folder of the cloned [project] on your machine.

**[Back to top](#table-of-contents)**

## Release Process

### Versioning

This project uses [Semantic Versioning].
For a list of available versions, see the [repository tag list].

**[Back to top](#table-of-contents)**

## Documentation

The documentation for the latest repository build is hosted on the
[GitHub Pages] of the [project].

The documentations of the [project] **releases** are hosted on [Read The Docs].

**[Back to top](#table-of-contents)**

## Contributing

If you are interested to contribute code or documentation to the [project],
please take a look at the [contributing guidelines](CONTRIBUTING.md) for details
on our development process.

**[Back to top](#table-of-contents)**

## License

The [project] is licensed under the revised [3-Clause BSD License].

See [LICENSE](LICENSE).

**[Back to top](#table-of-contents)**

## Authors

* Jochen Gerhaeusser

See also the list of [contributors] who participated in this [project].

**[Back to top](#table-of-contents)**

[Semantic Versioning]: https://semver.org
[3-Clause BSD License]: https://opensource.org/licenses/BSD-3-Clause
[Python]: https://www.python.org
[PyPi]: https://pypi.org
[pip]: https://pip.pypa.io
[Sphinx]: https://pypi.org/project/sphinx
[Furo]: https://pypi.org/project/furo
[sphinx-copybutton]: https://pypi.org/project/sphinx-copybutton
[Jupyter]: https://jupyter.org
[github]: https://github.com
[project]: https://github.com/JoeVirtual/KonFoo
[repository tag list]: https://github.com/JoeVirtual/KonFoo/releases
[contributors]: https://github.com/JoeVirtual/KonFoo/graphs/contributors
[GitHub Pages]: https://joevirtual.github.io/KonFoo/
[Read The Docs]: https://konfoo.readthedocs.io
