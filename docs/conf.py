# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import datetime
import doctest
import os
import sys

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../src'))

# -- Project information -----------------------------------------------------

project = 'KonFoo'
author = 'Jochen Gerhaeusser'
copyright = f"2015-{datetime.datetime.utcnow().year}, {author}"
version = '2.1.0'
release = '2.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    "sphinx_copybutton"
]
master_doc = 'index'
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
# pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
html_static_path = ['_static']
html_theme_options = {
    "light_css_variables": {
    },
    "dark_css_variables": {
    },
}
html_title = f'{project} {release}'
html_logo = './_static/images/logo.png'
# html_favicon = './_static/images/favicon.ico'
html_show_sourcelink = True
html_baseurl = 'https://konfoo.readthedocs.io'
show_navbar_depth = 3

# -- Extension configuration -------------------------------------------------

# -- Options for AutoDoc ------------------------------------------------------

autodoc_member_order = 'bysource'
autodoc_inherit_docstrings = True

# -- Options for ExtLinks -----------------------------------------------------

extlinks = {
    'issue': ('https://github.com/JoeVirtual/konfoo/issues/%s', 'issue ')
}

# -- Options for InterSphinx --------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.10', None)
}

# -- Options for Doctest ------------------------------------------------------

doctest_default_flags = doctest.ELLIPSIS | \
                        doctest.IGNORE_EXCEPTION_DETAIL | \
                        doctest.NORMALIZE_WHITESPACE
