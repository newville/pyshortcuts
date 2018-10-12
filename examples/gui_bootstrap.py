#!/usr/bin/env python
import os
import sys
from pyshortcuts import make_shortcut, platform

bindir = 'bin'
if platform.startswith('win'):
    bindir = 'Scripts'

make_shortcut("%s --wxgui" % os.path.join(sys.prefix, bindir, 'pyshortcut'),
              name='PyShortcut', terminal=False)
