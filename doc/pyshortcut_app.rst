.. _pyshortcut_app:

The `pyshortcut` command-line program
----------------------------------------------

Pyshortcuts installs a command-line program `pyshortcut` to build shortcuts.
If wxPython is installed, this can also be used to launch a Graphical User
Interface application for build shortcuts.


From a shell or Command window with PATH set to include python programs and
scripts, a command to create a shortcut might look like::


    ~> pyshortcut -n MyApp -i /home/user/icons/myicon.icns  /home/user/bin/myapp.py


To include command-line options for the script, put them in double quotes::


    ~> pyshortcut -n MyApp -i /home/user/icons/myicon.icns "/home/user/bin/myapp.py  -t 10"


The `pyshortcut` command line program has a form of::


    pyshortcut [-h] [-v] [-n NAME] [-i ICON] [-f FOLDER] [-e EXE] [-t] [-g] [-d] [-s] [-w] [scriptname]

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



The `pyshortcut` GUI
---------------------------

In addition to the `pyshortcut` command-line program, there is a small GUI
application that provides a simple form to help the user browse for script
and icons, and set options before creating a shortcut or generating an
example Python script to create the shortcut.

This requires the `wxPython` package which can be installed using `pip` or
`conda` but is not automatically installed when installing `pyshortcuts`.
This application can be launched from the command line with::

    ~> pyshortcut --wxgui

which will show a form like

  .. image:: _static/pyshortcutgui_screenshot.png
     :width: 85 %

for building shortcuts.

Of course, that command might be the sort of command you might want to be able
to launch by clicking on a desktop shortcut.  We have just the tool for that!  Doing::


    ~> pyshortcut --bootstrap

will create a desktop shortcut with an icon of a ladder that will launch
the pyshortcut GUI.  This essentially runs::


    #!/usr/bin/env python
    import os
    import sys
    from pyshortcuts import make_shortcut, platform

    bindir = 'Scripts' if platform.startswith('win') else 'bin'
    pyshortcut = os.path.normpath(os.path.join(sys.prefix, bindir, 'pyshortcut'))
    scut = make_shortcut(f"{pyshortcut:s} --wxgui", name='PyShortcut', terminal=False)


The ladder icon was made by Left Martinez, and downloaded from
(https://www.iconfinder.com/iconsets/free-construction-tools)



Note for running wxPython GUIs on macOS with Anaconda Python
------------------------------------------------------------

If your application uses wxPython and you are running with Anaconda Python on
macOS, you may experience problems that your application does not start.  If
you try to run your script from the command line, you may see the following
error message::


    ~> python my_wxpython_app.py
    This program needs access to the screen. Please run with a
    Framework build of python, and only when you are logged in
    on the main display of your Mac.


If you do see that, it can be fixed and your script run properly by adding::

    import wx
    wx.PyApp.IsDisplayAvailable = lambda _: True

in your script before running your starting the `wxPython` `mainloop` event handler.
