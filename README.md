# pyshortcuts
creates desktop shortcuts for python scripts and applications.  This allows
users to click an desktop icon to run the application.

Pyshortcuts is cross-platform, supporting Windows, MacOS, and Linux each in
the way most natural for the OS.  On Windows, a shortcut is created.  On
Linux a ".desktop" file is created.  On MacOS, a minimal Application is
created.  In all cases, these are put on the Desktop for the current user
so that it does not require elevated permission or write to system-level
files (registry, /Applications, /usr/bin).  The user can then have complete
control of renaming, moving, or deleting the shortcut.

Pyshortcuts has a small footprint and is very easy to use either from a
python script (say as part of a setup.py installation) as with

```

from pyshortcuts import make_shortcut

make_shortcut('MyApp', 'application_script.py', 'My Application',
	'path/to/my_icon')

```

or by using  the `pyshortcut` command-line application, as with:


```
~> pyshortcut -n MyApp -i /home/icon.ico /home/bin/myapp.py

```
