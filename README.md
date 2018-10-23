[![Build Status](https://travis-ci.com/newville/pyshortcuts.svg?branch=master)](https://travis-ci.com/newville/pyshortcuts)
[![Build status](https://ci.appveyor.com/api/projects/status/ro3b3ytjjjrkhun6/branch/master?svg=true)](https://ci.appveyor.com/project/newville/pyshortcuts/branch/master)

# pyshortcuts


Pyshortcuts helps developers and Python users create desktop shortcuts
that will run python scripts and applications.

Pyshortcuts is cross-platform, supporting Windows, MacOS, and Linux each in the way that
is most natural for the OS. On Windows, a Shortcut or Link is created. On MacOS, a minimal
but compplete Application is created. On Linux a ".desktop" file is created. For all OSes,
the shortcut is put either directly on the Desktop or in a folder on the Desktop of the
current user. This means that there is no  need for elevated permission and no writing to
system-level files (registry, /Applications, /usr/bin).  After the shortcut has been created,
the user has complete control to rename, move, or delete it.  Shortcuts can have a custom
icon (`.ico` files on Windows or Linux, or `.icns` files on MacOS) specified, defaulting to
a Python icon included with pyshortcuts.

Pyshortcuts is pure python, has a small footprint and is very easy to install
and use either from a python script.  That is to say, it can easily be part of
a installation (or post-installation process) process for larger packages.

## installation

To install `pyshortcuts`, use

```
pip install pyshortcuts
```

or

```
conda install -c gsecars pyshortcuts
```

Pyshortcut requires the pywin32 package on Windows. This should be
installed automatically with either of the above install methods.

In order to use the pyshortcut GUI, the wxPython package is required.

## usage from Python

Shortcuts can be created from a Python script as with

```python

from pyshortcuts import make_shortcut

make_shortcut('/home/user/bin/myapp.py', name='MyApp',
                        icon='/home/user/icons/myicon.ico')
```

The arguments to `make_shortcut` are:

  * `script`      (str)  path to script to run. This can include command-line arguments
  * `name`        (str or None)  name to use for shortcut [defaults to script name]
  * `description` (str or None)  longer description of script [defaults to `name`]
  * `icon`        (str or None) path to icon file [defaults to python icon]
  * `folder`      (str or None) folder on Desktop to put shortcut [defaults to Desktop]
  * `terminal`    (True or False) whether to run in a Terminal [True]

##  `pyshortcut` command-line program

pyshortcuts installs a `pyshortcut` command-line program for creating a shortcut.
From a shell or Command window with PATH set to include python programs and scripts,
a command to create a shortcut might look like:

```
~> pyshortcut -n MyApp -i /home/user/icons/myicon.icns  /home/user/bin/myapp.py
```

To include command-line options for the script, put them in double quotes

```
~> pyshortcut -n MyApp -i /home/user/icons/myicon.icns "/home/user/bin/myapp.py  -t 10"
```

The `pyshortcut` command line program has the following optional arguments:

  * `--version`        show program's version number and exit
  * `-h`, `--help`     show help message and exit
  * `-n link_name`, `--name=link_name`  name for shortcut link
  * `-i icon_name`, `--icon=icon_name`  name of icon file
  * `-f subfolder`, `--folder=subfolder` subfolder on desktop to put icon
  * `-t`, `--terminal` run script in a Terminal Window [True]
  * `-g`, `--gui`      run script as a GUI, with no Terminal Window [False]
  * `-w`, `--wxgui`    run GUI version of pyshortcut

Note that running in the Terminal is True by default.  For GUI applications
the extra Terminal or Command Window may be unwanted, and can be disabled with the
`-g` or `--gui` option.


## `pyshortcut` GUI

In addition to the `pyshortcut` command-line program, there is a GUI that provides
a simple form to help the user browse for script, icons, and set options before
creating a shortcut or generating an example Python script to create the shortcut.

![PyShortcut Screenshot](doc/pyshortcutgui_screenshot.png)

This can be launched from the command line with

```
~> pyshortcut --wxgui
```

That may be the sort of script that you might want to be able to launch by clicking
on a desktop shortcut. We have just the tool to do that! This script (which is
included as `gui_bootstrap.py` in the `examples` folder) will create a dekstop
shortcut that launches the pyshortcut GUI:

```python
#!/usr/bin/env python
import os
import sys
from pyshortcuts import make_shortcut, platform

bindir = 'bin'
if platform.startswith('win'):
    bindir = 'Scripts'

make_shortcut("%s --wxgui" % os.path.join(sys.prefix, bindir, 'pyshortcut'),
              name='PyShortcut', terminal=False)
```
