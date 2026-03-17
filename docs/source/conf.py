# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import subprocess


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'gearpy'
project_copyright = '2024 - 2026, Andrea Blengino'
author = 'Andrea Blengino'
release = subprocess.run(
    'git describe --tags'.split(),
    stdout=subprocess.PIPE
).stdout.decode('utf-8').strip().split('-')[0]


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'myst_parser',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton'
]

sourse_suffix = {
    '.rst': 'restrusturedtext',
    '.md': 'markdown',
}

myst_enable_extensions = [
    'dollarmath',
]

templates_path = ['_templates']
exclude_patterns = []

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None)
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['custom.css']
add_module_names = False
html_title = 'gearpy'
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
suppress_warnings = ['myst.header']
