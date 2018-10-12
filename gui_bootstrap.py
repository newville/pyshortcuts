#!/usr/bin/env python

import os
import sys
from pyshortcuts import make_shortcut
make_shortcut("%s -g" % os.path.join(sys.exec_prefix, 'bin', 'pyshortcut'),
              name='PyShortcut', terminal=False)
