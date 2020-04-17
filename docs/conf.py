# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath(''))

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'hoverxref.extension',
    'notfound.extension',
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]
# -- Project information -----------------------------------------------------

project = 'Zero to DataDog'
copyright = '2020, Blaise Pabon'
author = 'Blaise Pabon'
release = '2020-04'

# -- General configuration ---------------------------------------------------
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = "yummy_sphinx_theme"
html_static_path = ['_static']
