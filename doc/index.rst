.. pyshortcuts documentation master file,

PyShortcuts: create desktop shortcuts
================================================

.. _numpy: https://numpy.org/
.. _numpy_financial: https://numpy.org/numpy-financial/


Pyshortcuts helps Python developers and users create Desktop Shortcuts or links
that will launch a python script and other applications.  The shortcuts created
can go onto the user's desktop or into the Start Menu (for systems with Start
Menus) or both.  Pyshortcuts gives a consistent interface for building
shortcuts for Windows, macOS, and Linux with a result that is most natural for
each OS.

On **Windows**, a Shortcut Link is created and placed on the users Desktop and
in the Start Menu. Special attention is given to Anaconda Python on Windows.
For that environment, the shortcut created will be sure to run in an Anaconda
environment, explicitly selecting the "base" environment even if that has not
been explicitly set by the user.

On **macOS**, a minimal but complete Application is created and
placed on the users Desktop.

On **Linux**, a ".desktop" file is created and placed on the users Desktop (if
that exists) and in $HOME/.local/share/applications (if that exists), which
will often get presented in a Start Menu for windowing desktop themes that use
a one.

On all platforms, the shortcuts created on the Desktop or Start Menu can be put
either directly onto the Desktop / Start Menu or in a sub-folder of the Desktop
/ Start Menu.  Shortcuts can have a custom icon (`.ico` files on Windows or
Linux, or `.icns` files on macOS) specified, defaulting to a Python icon
included with pyshortcuts.

Pyshortcuts writes only to the users Desktop or application folder that gets
read by the Start Menu.  It does not require elevated permission, and does not
write to system-level files (registry entries, /Applications, /usr/bin, etc).
After the shortcut has been created, the end user has permission to rename,
move, or delete it.

Pyshortcuts is pure python, has minimal dependencies, is readily installed, and
easy to use from a the command-line or from Python scripts.  This means that
Pyshortcuts can be made part of an installation (or post-installation process)
process for larger packages.


Pyshortcuts also provides a number of :ref:`utility_funcs` for working with Paths
and filenames that may be of general use.


Contents
-----------------

.. toctree::
   :maxdepth: 2

   install
   pyshortcut_app
   python
   utilities
