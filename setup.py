#!/usr/bin/env python
from setuptools import setup

long_description = '''
Pyshortcuts creates desktop shortcuts for python scripts and applications
to allow a user to click on a desk

Pyshortcuts is cross-platform, supporting Windows, MacOS, and Linux each in
the way most natural for the OS.  On Windows, a shortcut is created.  On
Linux a ".desktop" file is created.  On MacOS, a minimal Application is
created.  In all cases, these are put on the Desktop for the current user
so that it does not require elevated permission or write to system-level
files (registry, /Applications, /usr/bin).  The user can then have complete
control of renaming, moving, or deleting the shortcut.
'''

setup(name='pyshortcuts',
      version='1.0',
      author='Matthew Newville',
      author_email='newville@cars.uchicago.edu',
      url='http://github.com/newville/pyshortcuts',
      license='BSD',
      description='create desktop shortcuts for python scripts',
      long_description=long_description,
      packages=['pyshortcuts'],
      classifiers=[
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
      entry_points = {'console_scripts' : ['pyshortcuts = pyshortcuts:shortcut_cli']}
      )
