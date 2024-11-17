#!/usr/bin/env python
from pathlib import Path
import sys
from pyshortcuts import make_shortcut, uname, __file__

bindir = 'Scripts' if uname.startswith('win') else 'bin'

script = Path(sys.prefix, bindir, 'pyshortcut').resolve().as_posix()


iconfile = 'ladder.icns' if uname=='darwin' else 'shovel.ico'
icon = Path(Path(__file__).parent, 'icons', iconfile).absolute().as_posix()

scut = make_shortcut(f"{script} --wxgui", name='PyShortcuts',
                      icon=icon, terminal=False)

print("pyshortcuts GUI: %s" % scut.target)
