#!/usr/bin/env python
import os
from pyshortcuts import make_shortcut, platform

def test_shortcut():
    script = os.path.join('..', 'examples', 'console_scripts', 'timer.py')
    icon  = os.path.join('..', 'examples', 'icons', 'stopwatch')

    iext = 'ico'
    if platform.startswith('darwin'):
        iext = 'icns'

    icon = "%s.%s" % (icon, iext)
    print("script : ", script )
    make_shortcut(script, name='Timer', icon=icon)

if __name__ == '__main__':
    test_shortcut()
