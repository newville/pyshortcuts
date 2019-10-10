[![Build Status](https://travis-ci.com/newville/pyshortcuts.svg?branch=master)](https://travis-ci.com/newville/pyshortcuts)
[![Build status](https://ci.appveyor.com/api/projects/status/ro3b3ytjjjrkhun6/branch/master?svg=true)](https://ci.appveyor.com/project/newville/pyshortcuts/branch/master)
[![Version](https://img.shields.io/pypi/v/pyshortcuts.svg)](https://pypi.org/project/pyshortcuts)
[![Downloads](https://img.shields.io/pypi/dm/pyshortcuts.svg)](https://pypi.org/project/pyshortcuts)


# pyshortcuts


Pyshortcuts helps Python developers and users create shortcuts that will
run python scripts and other applications.  The shortcuts created can go
onto the users desktop or into the Start Menu (for systems with Start
Menus) or both.

Pyshortcuts works on Windows, MacOS, and Linux in the way that is most
natural for each OS.  That is, on Windows, a Shortcut Link is created and
placed on the users Desktop and in the Start Menu. On MacOS, a minimal but
complete Application is created and placed on the users Desktop.  On Linux
a ".desktop" file is created and placed on the users Desktop (if that
exists) and in $HOME/.local/share/applications (if that exists), which will
often get presented in a Start Menu for windowing desktop themes that use a
Start Menu.  On all platforms, the shortcuts created on the Deskop or Start
Menu can be put either directly on the Desktop / Start Menu or in a folder
on the Desktop / Start Menu.

Special attention is given to Anaconda Python.  On Windows, this means the
program linked to by the shortcut will be run in an Anaconda environment,
explicitly selecting the "base" environment even if that has not been
explicitly set.  On MacOS, the shortcut will make sure to use the
`python.app` application so that GUI programs will be able to draw to
properly draw to the screen.

By writing only to the users Desktop or application folder that gets read
by the Start Menu, there is no need for elevated permission and no writing
to system-level files (registry entries, /Applications, /usr/bin, etc).
After the shortcut has been created, the user has complete control to
rename, move, or delete it.  Shortcuts can have a custom icon (`.ico` files
on Windows or Linux, or `.icns` files on MacOS) specified, defaulting to a
Python icon included with pyshortcuts.

Pyshortcuts is pure python, small, easy to install, and easy to use from a
python script.   This means that Pyshortcuts can be made part of an
installation (or post-installation process) process for larger packages.

## installation

To install `pyshortcuts`, use

```
pip install pyshortcuts
```

or

```
conda install -c gsecars pyshortcuts
```

On Windows, pyshortcuts requires the pywin32 package. This should be installed
automatically with either of the above install methods.

In order to use the pyshortcut GUI, the wxPython package is required.

## usage from Python

Shortcuts can be created from a Python script with

```python

from pyshortcuts import make_shortcut

make_shortcut('/home/user/bin/myapp.py', name='MyApp',
                        icon='/home/user/icons/myicon.ico')
```

The arguments to the `make_shortcut` function are:

  * `script`      (str) command to script to run. This can include command-line arguments
  * `name`        (str or None) name to use for shortcut [defaults to script name]
  * `description` (str or None) longer description of script [defaults to `name`]
  * `icon`        (str or None) path to icon file [defaults to python icon]
  * `folder`      (str or None) folder on Desktop to put shortcut [defaults to Desktop]
  * `terminal`    (bool) whether to run in a Terminal [True]
  * `desktop`  ((bool) whether to add shortcut to Desktop [True]
  * `startmenu`   (bool) whether to add shortcut to Start Menu [True]
  * `executable`  (str or None) name of executable to use [this Python]

Note that the Start Menu does not exist for MacOSX.

The `executable` defaults to the version of Python executable used to make shortcut.


##  `pyshortcut` command-line program

pyshortcuts also installs a `pyshortcut` command-line program for creating a shortcut.
From a shell or Command window with PATH set to include python programs and scripts,
a command to create a shortcut might look like:

```
~> pyshortcut -n MyApp -i /home/user/icons/myicon.icns  /home/user/bin/myapp.py
```

To include command-line options for the script, put them in double quotes

```
~> pyshortcut -n MyApp -i /home/user/icons/myicon.icns "/home/user/bin/myapp.py  -t 10"
```

The `pyshortcut` command line program has a form of

```
pyshortcut [-h] [-v] [-n NAME] [-i ICON] [-f FOLDER] [-e EXE] [-t] [-g] [-d] [-s] [-w] [scriptname]
```

where `scriptname` is the name of the script.  To include arguments to that
script, enclose the script name and arguments in quotes (double quotes on
Windows).


There are several optional arguments:



with the following optional arguments:

  * `-h`, `--help`      show help message and exit
  * `-v`, `--version`   show program's version number and exit
  * `-n NAME`, `--name=NAME` name for shortcut
  * `-i ICON`, `--icon=ICON` name of icon file
  * `-f FOLDER`, `--folder=Folder` subfolder on desktop to put icon
  * `-e EXE`, `--executable EXE`     name of executable to use (python)

  * `-t`, `--terminal` run script in a Terminal Window [True]
  * `-g`, `--gui`      run script as a GUI, with no Terminal Window [False]
  * `-d`,` --desktop`         create desktop shortcut [True]
  * `-s`, `--startmenu`       create Start Menu shortcut [True]
  * `-w`, `--wxgui`    run GUI version of pyshortcut

Note that running in the Terminal is True by default, which means that each
time the shortcut is used to lauch the program, a new Terminal or Command
window will be created for it.  For many command-line applications, this is
approprate.  The extra Terminal or Command window may be unwanted for some GUI
applications, and can be disabled with the `-g` or `--gui` option.


## `pyshortcut` GUI

In addition to the `pyshortcut` command-line program, there is a GUI that provides
a simple form to help the user browse for script and icons, and set options before
creating a shortcut or generating an example Python script to create the shortcut.

![PyShortcut Screenshot](doc/pyshortcutgui_screenshot.png)

This can be launched from the command line with

```
~> pyshortcut --wxgui
```

Of course, that command might be the sort of command you might want to be able
to launch by clicking on a desktop shortcut.  We have just the tool for
that. This script (included as `gui_bootstrap.py` in the `examples` folder)
will create a desktop shortcut that launches the pyshortcut GUI:

```python
#!/usr/bin/env python
import os
import sys
from pyshortcuts import make_shortcut, platform

bindir = 'bin'
if platform.startswith('win'):
    bindir = 'Scripts'

scut = make_shortcut(
    "%s --wxgui" % os.path.join(sys.prefix, bindir, 'pyshortcut'),
    name='PyShortcut', terminal=False
)

print("pyshortcuts GUI: %s" % scut.target)
```

That is, running

```
~> python setup.py install
~> python examples/gui_bootstrap.py
```

will give you a desktop shortcut that launches a GUI application for turning
Python scripts into desktop shortcuts.
