#!/usr/bin/env python
from setuptools import setup
import sys

long_description = '''
Pyshortcuts helps developers and Python users to create desktop shortcuts
that will run python scripts and applications.

Pyshortcuts is cross-platform, supporting Windows, MacOS, and Linux each in
the way most natural for the OS.  On Windows, a Shortcut or Link is
created.  On Linux a ".desktop" file is created.  On MacOS, a minimal
Application is created.  In all cases, these shortcuts are put either
directly on the Desktop or in a folder on the Desktop of the current user.
That means that there is not need for elevated permission or writing to
system-level files (registry, /Applications, /usr/bin).  The user has
complete control to rename, move, or delete the shortcut after it is
created.  Shortcuts can have a custom icon (`.ico` files on Windows or
Linux, or `.icns` files on MacOS) specified, defaulting to a Python icon
included with the pyshortcuts module.

Pyshortcuts is pure python, has a small footprint and is very easy to
install and use either from a python script.  That is to say, it can easily
be part of a installation (or post-installation process) process for larger
packages.
'''

install_reqs = ['six']
if sys.platform.startswith('win'):
    install_reqs.append['pywin32']

setup(name='pyshortcuts',
      version='1.1',
      author='Matthew Newville',
      author_email='newville@cars.uchicago.edu',
      url='http://github.com/newville/pyshortcuts',
      license = 'OSI Approved :: MIT License',
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
      description='create desktop shortcuts for python scripts',
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
