#!/usr/bin/env python
import os
from pyshortcuts import make_shortcut, platform, shortcut

root = os.path.abspath(os.path.join(__file__, '..', '..'))


def test_shortcut():
    script = os.path.join(root, 'examples', 'console_scripts', 'timer.py') + ' -u 0.25 -t 10'
    icon  = os.path.join(root, 'examples', 'icons', 'stopwatch')

    iext = 'ico'
    if platform.startswith('darwin'):
        iext = 'icns'

    icon = "%s.%s" % (icon, iext)
    scut = make_shortcut(script, name='Timer', icon=icon)
    assert isinstance(scut, shortcut.Shortcut), 'it returns a shortcut instance'

if __name__ == '__main__':
    test_shortcut()
