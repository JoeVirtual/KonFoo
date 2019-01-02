# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options.
# For a full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config
import datetime
import doctest
import os
import sys

on_rtd = os.environ.get('READTHEDOCS') == 'True'
if not on_rtd:
    import sphinx_rtd_theme

    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('.'))

# -- Project information -----------------------------------------------------

# General information about the project.
project = 'KonFoo'
copyright = '2015-{}, Jochen Gerhäußer'.format(datetime.datetime.utcnow().year)
author = 'Jochen Gerhäußer'

# The short X.Y version.
version = '1.0'
# The full version, including alpha/beta/rc tags.
release = '1.0'

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
# See the documentation for a list of builtin themes.
#
# html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'sticky_navigation': True,
    'collapse_navigation': False,
    'display_version': True,
    'navigation_depth': 4,
    'prev_next_buttons_location': 'both',
}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The name for this set of Sphinx documents.
# If None, it defaults to "<project> v<release> documentation".
html_title = 'KonFoo'

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = True

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'KonFoo'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc,
     'KonFoo.tex',
     'KonFoo Documentation',
     'Jochen Gerhäußer',
     'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc,
     'konfoo',
     'KonFoo Documentation',
     [author],
     1)
]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc,
     'KonFoo',
     'KonFoo Documentation',
     author,
     'KonFoo',
     'One line description of project.',
     'Miscellaneous'),
]

# -- Extension configuration -------------------------------------------------

# -- Options for AutoDoc ------------------------------------------------------

autodoc_member_order = 'bysource'
autodoc_inherit_docstrings = True

# -- Options for ExtLinks -----------------------------------------------------

extlinks = {
    'issue': ('https://github.com/JoeVirtual/KonFoo/issues/%s', 'issue ')
}

# -- Options for InterSphinx --------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.7', None)
}

# -- Options for Doctest ------------------------------------------------------

doctest_default_flags = doctest.ELLIPSIS | doctest.IGNORE_EXCEPTION_DETAIL | doctest.NORMALIZE_WHITESPACE