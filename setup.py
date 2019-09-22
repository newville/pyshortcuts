#!/usr/bin/env python
from setuptools import setup
import sys
import os

long_description = '''

Pyshortcuts helps developers and Python users to create shortcuts on a
Users Desktop or Start Menu that will run python scripts and applications.

Pyshortcuts is cross-platform, supporting Windows, MacOS, and Linux each in
the way most natural for the OS.  On Windows, a Shortcut or Link is
created.  On Linux a ".desktop" file is created.  On MacOS, a minimal
Application is created.  In all cases, the shortcuts are put either
directly on the Desktop or Start Menu , or in a folder on the Desktop or
Start Menu of the current user.  That means that there is not need for
elevated permission or writing to system-level files (registry,
/Applications, /usr/bin).  The user has complete control to rename, move,
or delete the shortcut after it is created.  Shortcuts can have a custom
icon (`.ico` files on Windows or Linux, or `.icns` files on MacOS)
specified, defaulting to a Python icon included with the pyshortcuts
module.

Pyshortcuts is pure python, has a small footprint and is very easy to
install and use either from a python script.  That is to say, it can easily
be part of a installation (or post-installation process) process for larger
packages.
'''

install_reqs = ['six']
if sys.platform.startswith('win'):
    install_reqs.append('pywin32')

version = '1.4'
here, s = os.path.split(__file__)
with open(os.path.join(here, 'pyshortcuts', '__init__.py'), 'r') as fh:
    text = fh.readlines()
    for line in text:
        line = line[:-1].strip()
        if line.startswith('__version'):
            words = line.split('=')
            version = words[1].strip()
            if version.startswith("'") and version.endswith("'"):
                version = version[1:-1]
            break

setup(name='pyshortcuts',
      version=version,
      author='Matthew Newville',
      author_email='newville@cars.uchicago.edu',
      url='http://github.com/newville/pyshortcuts',
      license = 'OSI Approved :: MIT License',
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
      description='create desktop and Start Menu shortcuts for python scripts',
      long_description=long_description,
      packages=['pyshortcuts'],
      install_requires=install_reqs,
      classifiers=[
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
      package_data={'pyshortcuts': ['icons/*']},
      entry_points={'console_scripts' : ['pyshortcut = pyshortcuts:shortcut_cli']}
      )
