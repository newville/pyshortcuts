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
~> pyshortcut -n MyApp -i myicon -p /home/user/icons -t "/home/user/bin/myapp.py -a"

```


The `pyshortcut` command-line program has the following optional arguments:


  *  `-n NAME` or `--name=NAME` name to show for the shortcut.
  *  `-i ICON` or `--icon=ICON` name of icon  (file with `.ico` or `.icns`  extension).
  *  `-p PATH` or `--path=PATH` path to icon file.
  *  `-t`            run in terminal mode instead of GUI mode.
