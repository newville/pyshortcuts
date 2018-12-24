#!/usr/bin/env python
import os
from pyshortcuts import make_shortcut, platform

def test_shortcut():
    script = os.path.join('..', 'examples', 'console_scripts', 'timer.py') + ' -u 0.25 -t 10'
    icon  = os.path.join('..', 'examples', 'icons', 'stopwatch')

    iext = 'ico'
    if platform.startswith('darwin'):
        iext = 'icns'

    icon = "%s.%s" % (icon, iext)
    make_shortcut(script, name='Timer', icon=icon)

if __name__ == '__main__':
    test_shortcut()