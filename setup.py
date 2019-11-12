#!/usr/bin/env python
from setuptools import setup
import sys
import os
try:
	import git
except ModuleNotFoundError:
	print("E: gitpython is missing. Please Install it to enable versioning or manually set version in setup.py")

long_description = '''

pyshortcuts-max helps developers and Python users to create shortcuts on a
Users Desktop or Start Menu that will run python scripts and applications.

pyshortcuts-max is cross-platform, supporting Windows, MacOS, and Linux each in
the way most natural for the OS.  On Windows, a Shortcut or Link is
created.  On Linux a ".desktop" file is created.  On MacOS, a minimal
Application is created.  In all cases, the shortcuts are put either
directly on the Desktop or Start Menu , or in a folder on the Desktop or
Start Menu of the current user.  That means that there is not need for
elevated permission or writing to system-level files (registry,
/Applications, /usr/bin).  The user has complete control to rename, move,
or delete the shortcut after it is created.  Shortcuts can have a custom
icon (`.ico` files on Windows or Linux, or `.icns` files on MacOS)
specified, defaulting to a Python icon included with the pyshortcuts-max
module.

pyshortcuts-max is pure python, has a small footprint and is very easy to
install and use either from a python script.  That is to say, it can easily
be part of a installation (or post-installation process) process for larger
packages.
'''


try:
	repo = git.Repo(search_parent_directories=True)
	sha = repo.head.object.hexsha
	this_directory = path.abspath(path.dirname(__file__))
	__version__ = repo.git.describe("--tags")
except NameError:
	print("Manual Versioning, not suggested")
	__version__ = 2.0

	
install_reqs = ['six']
if sys.platform.startswith('win'):
    install_reqs.append('pywin32')




setup(name='pyshortcuts-max',
      version=__version__,
      author='Srevin Saju',
      author_email='srevin03@gmail.com',
      url='http://github.com/newville/pyshortcuts-max',
      license = 'OSI Approved :: MIT License',
      python_requires='>=3.5.*',
      description='create desktop and Start Menu shortcuts for python scripts',
      long_description=long_description,
      packages=['pyshortcutsmax'],
      install_requires=install_reqs,
      classifiers=[
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
      package_data={'pyshortcutsmax': ['icons/*']},
      entry_points={'console_scripts' : [
		'pyshortcuts=pyshortcutsmax.__init__:shortcut_cli']}
      )
