# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import subprocess

sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'gearpy'
copyright = '2024, Andrea Blengino'
author = 'Andrea Blengino'
release = subprocess.run(['git', 'describe', '--tags'], stdout = subprocess.PIPE).stdout.decode('utf-8')

if not release.startswith('v') or not release.endswith('\n') or '-' in release or release.count('.') != 2:
    raise ValueError(f"Invalid release name {release}.")


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'm2r2', 'sphinx.ext.intersphinx', 'sphinx_copybutton']

templates_path = ['_templates']
exclude_patterns = []

intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
                       'pandas': ('https://pandas.pydata.org/docs/', None),
                       'matplotlib': ('https://matplotlib.org/stable/', None)}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['custom.css']
add_module_names = False
html_title = 'gearpy'
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
