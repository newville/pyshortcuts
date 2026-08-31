#
# pyshortcuts documentation build configuration file

from datetime import date

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon',
              'sphinx.ext.mathjax', 'sphinx.ext.intersphinx',
              'sphinx_copybutton', "sphinx_design"]

intersphinx_mapping = {'py': ('https://docs.python.org/3/', None)}

templates_path = ['_templates']

source_suffix = {'.rst': 'restructuredtext'}
source_encoding = 'utf-8'

master_doc = 'index'

# General information about the project.
project = u'pyshortcuts'
copyright = f'{date.today().year}, Matthew Newville, The University of Chicago'


import pyshortcuts
release = pyshortcuts.__version__.split('+', 1)[0]

add_function_parentheses = True
add_module_names = True

pygments_style = 'sphinx'


html_theme = 'breeze'
html_theme_options = {"external_links": ["https://github.com/newville/pyshortcuts"]}

html_title = 'PyShortcuts: cross-platform desktop shortcuts'
html_short_title =  'PyShortcuts: create desktop shortcuts'

html_static_path = ['_static']

html_sidebars = {'index': ['indexsidebar.html','searchbox.html']}

html_show_sourcelink = True
html_logo = "_static/ladder.png"
