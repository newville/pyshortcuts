#!/usr/bin/env python
import os
from pyshortcuts import make_shortcut, platform, Shortcut, get_folders

root = os.path.abspath(os.path.join(__file__, '..', '..'))

folders = get_folders()

def test_shortcut():
    print("---folders:\n Home: {}\n Desktop: {}\n StartMenu: {}\n".format(
        folders.home, folders.desktop, folders.startmenu))

    script = os.path.join(root, 'examples', 'console_scripts', 'timer.py') + ' -u 0.25 -t 10'
    icon  = os.path.join(root, 'examples', 'icons', 'stopwatch')

    iext = 'ico'
    if platform.startswith('darwin'):
        iext = 'icns'

    icon = "%s.%s" % (icon, iext)
    scut = make_shortcut(script, name='Timer', icon=icon, folder=folders.desktop)
    assert isinstance(scut, Shortcut), 'it returns a shortcut instance'

    #raise err # force crash so we see manual print() debug statements

if __name__ == '__main__':
    test_shortcut()
