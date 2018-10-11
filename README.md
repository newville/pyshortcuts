# pyshortcuts

Pyshortcuts helps developers and Python users to create desktop shortcuts
that will run python scripts and applications.

Pyshortcuts is cross-platform, supporting Windows, MacOS, and Linux each in
the way most natural for the OS.  On Windows, a Shortcut is created.  On
Linux a ".desktop" file is created.  On MacOS, a minimal Application is
created.  In all cases, these shortcuts are put either directly on the
Desktop or in a folder on the Desktop of the current user.  That means that
require elevated permission or write to system-level files (registry,
/Applications, /usr/bin).  The user then has complete control to rename,
move, or delete the shortcut.

The shortcuts created by pyshortcuts can have custom icons (`.ico` files on
Windows or Linux, or `.icns` files on MacOS), defaulting to a Python icon.

Pyshortcuts has a small footprint and is very easy to use either from a
python script (say as part of a installation or post-installation process)
as with

```

from pyshortcuts import make_shortcut

make_shortcut('/home/user/bin/myapp.py', 'MyApp', icon='/home/user/icons/myicon.ico')

```

or by using  the `pyshortcut` for a command-line application as with:


```
~> pyshortcut -n MyApp -i /home/user/icons/myicon.icns -t "/home/user/bin/myapp.py -a"

```

The `pyshortcut` command line program has the following optional arguments:

  * `--version`           show program's version number and exit
  * `-h`, `--help`        show help message and exit
  * `-n link_name`, `--name=link_name`  name for shortcut link
  * `-i icon_name`, `--icon=icon_name`  name of icon file
  * `-f subfolder`, `--folder=subfolder` subfolder on desktop to put icon
  * `-t`, `--terminal`   run in a Terminal [False]


Note that running in the Terminal or command window is not set by default.
Many command-line tools will need this.
