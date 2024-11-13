[![Build status](https://github.com/newville/pyshortcuts/actions/workflows/test-ubuntu.yml/badge.svg)](https://github.com/newville/pyshortcuts/actions/workflows/test-ubuntu.yml)
[![Build status](https://github.com/newville/pyshortcuts/actions/workflows/test-windows.yml/badge.svg)](https://github.com/newville/pyshortcuts/actions/workflows/test-windows.yml)
[![Build status](https://github.com/newville/pyshortcuts/actions/workflows/test-macos.yml/badge.svg)](https://github.com/newville/pyshortcuts/actions/workflows/test-macos.yml)
[![Version](https://img.shields.io/pypi/v/pyshortcuts)](https://pypi.org/project/pyshortcuts)
[![Downloads]( https://img.shields.io/pypi/dm/pyshortcuts?color=red)](https://pypi.org/project/pyshortcuts)


Install `pyshortcuts` with

```
pip install pyshortcuts
```


Full documentation is at: [Pyshortcuts Documentation](https://newville.github.io/pyshortcuts/)



# Table of contents

1. [Pyshortcuts Overview](#about)
1. [Installation](#installation)
2. [Usage from Python](#frompytho)
3. [`pyshortcut` command-line program](#cli)
4. [Making a shortcut for single python command](#pycmd)
5. [Note for running wxPython GUIs on macOS with Anaconda Python](#wxapps_macos)
6. [`pyshortcut` graphical user interface](#wxgui)

## Pyshortcuts Overview <a name="about"></a>

Pyshortcuts helps Python developers and users create shortcuts that will run
python scripts and other applications.  The shortcuts created can go onto the
users desktop or into the Start Menu (for systems with Start Menus) or both.
Pyshortcuts gives a consistent interface for building shortcuts that run on
Windows, macOS, and Linux in the way that is most natural for each OS.

On Windows, a Shortcut Link is created and placed on the users Desktop and in
the Start Menu. On macOS, a minimal but complete Application is created and
placed on the users Desktop.  On Linux a ".desktop" file is created and placed
on the users Desktop (if that exists) and in $HOME/.local/share/applications
(if that exists), which will often get presented in a Start Menu for windowing
desktop themes that use a one.  On all platforms, the shortcuts created on the
Deskop or Start Menu can be put either directly onto the Desktop / Start Menu
or in a sub-folder of the Desktop / Start Menu.  Shortcuts can have a custom
icon (`.ico` files on Windows or Linux, or `.icns` files on macOS) specified,
defaulting to a Python icon included with pyshortcuts.


By writing only to the users Desktop or application folder that gets read by
the Start Menu, there is no need for elevated permission and no writing to
system-level files (registry entries, /Applications, /usr/bin, etc).  After the
shortcut has been created, the end user has complete control to rename, move,
or delete it.

Pyshortcuts is pure python, small, readily installed, and easy to use from a
the command-line or from Python scripts.  This means that Pyshortcuts can be
made part of an installation (or post-installation process) process for larger
packages.

Special attention is given to Anaconda Python on Windows.  For that
environment, the shortcut created will be sure to run in an Anaconda
environment, explicitly selecting the "base" environment even if that has not
been explicitly set by the user.

## installation <a name="installation"></a>

To install `pyshortcuts`, use

```
pip install pyshortcuts
```

On Windows, pyshortcuts requires the pywin32 package and will be installed
if needed. There are no depenendencies on macOS or Linux.

In order to use the pyshortcut GUI, the wxPython package is required.

## Usage from Python <a name="frompython"></a>

Shortcuts can be created from a Python script with

```python

from pyshortcuts import make_shortcut

make_shortcut('/home/user/bin/myapp.py', name='MyApp', icon='/home/user/icons/myicon.ico')
```

The arguments to the `make_shortcut` function are:

  * `script`      (str) scipt or command to be run. This can include command-line arguments
  * `name`        (str or None) name to use for shortcut [defaults to script name]
  * `description` (str or None) longer description of script [defaults to `name`]
  * `icon`        (str or None) path to icon file [defaults to python icon]
  * `folder`      (str or None) folder on Desktop to put shortcut [defaults to Desktop]
  * `terminal`    (bool) whether to run in a Terminal [True]
  * `desktop`  ((bool) whether to add shortcut to Desktop [True]
  * `startmenu`   (bool) whether to add shortcut to Start Menu [True]
  * `executable`  (str or None) name of executable to use [this Python]

Note that the Start Menu does not exist for macOSX.

The `executable` defaults to the version of Python executable used to make shortcut.


##  `pyshortcut` command-line program <a name="cli"></a>

Pyshortcuts installs a `pyshortcut` command-line program for creating a shortcut.
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
  * `-b`, `--bootstrap`   create a desktop shortcut to run GUI version of pyshortcut

Note that running in the Terminal is True by default, which means that each
time the shortcut is used to launch the application, a new Terminal or Command
window will be created for it.  For many command-line applications, this is
appropriate.  The extra Terminal or Command window may be unwanted for some GUI
applications, and can be disabled with the `-g` or `--gui` option.

## Making a shortcut for single python command <a name="pycmd"></a>

A common request and simple use-case for `pyshortcuts` is to wrap a single
python command.  An example of this might look like this:

```
import sys
from pyshortcuts import make_shortcut

pycmd = "_ -m pip install --upgrade pyshortcuts"

make_shortcut(pycmd, name='Update Pyshortcuts')
```

Note that using `_` or `{}` as the command name will indicate that the
current Python executable should be be used. An example that includes
an icon is given in the examples folder.

The above could be done from the command line with

```
~> pyshortcut -n "Update Pyshortcuts" "_ -m pip install pyshortcuts"
```

## Note for running wxPython GUIs on macOS with Anaconda Python <a name="wxapps_macos"></a>

If your application uses wxPython and you are running with Anaconda Python on
macOS, you may experience problems that your application does not start.  If
you try to run your script from the command line, you may see the following
error message:


```
~> python my_wxpython_app.py
This program needs access to the screen. Please run with a
Framework build of python, and only when you are logged in
on the main display of your Mac.
```


If you do see that, it can be fixed and your script run properly by adding

```
import wx
wx.PyApp.IsDisplayAvailable = lambda _: True
```

in your script before runnig your starting the `wxPython` `mainloop` event handler.



## `pyshortcut` GUI <a name="wxgui"></a>

In addition to the `pyshortcut` command-line program, there is a small GUI
application that provides a simple form to help the user browse for script
and icons, and set options before creating a shortcut or generating an
example Python script to create the shortcut.

![PyShortcut Screenshot](doc/pyshortcutgui_screenshot.png)

This requires the `wxPython` package which can be installed using `pip` or
`conda` but is not automatically installed when installing `pyshortcuts`.
This application can be launched from the command line with

```
~> pyshortcut --wxgui
```

Of course, that command might be the sort of command you might want to be able
to launch by clicking on a desktop shortcut.  We have just the tool for that!  Doing

```
~> pyshortcut --bootstrap
```

will create a desktop shortcut with an icon of a ladder that will launch
the pyshortcut GUI.  This essentially runs


```python
#!/usr/bin/env python
import os
import sys
from pyshortcuts import make_shortcut, platform

bindir = 'Scripts' if platform.startswith('win') else 'bin'
pyshortcut = os.path.normpath(os.path.join(sys.prefix, bindir, 'pyshortcut'))
scut = make_shortcut(f"{pyshortcut:s} --wxgui", name='PyShortcut', terminal=False)
```

The ladder icon was made by Left Martinez, and downloaded from
(https://www.iconfinder.com/iconsets/free-construction-tools)
