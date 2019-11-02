#!/usr/bin/env python
'''Normal test run:
     python -m pytests

   Run and see manual debug print()s:
     python test_pyshortcuts.py
'''
import os
import pytest
from pyshortcuts import make_shortcut, platform, Shortcut, get_folders

folders = get_folders()
root = os.path.abspath(os.path.join(__file__, '..', '..'))

def test_shortcut():
    '''Create a shortcut from examples dir'''
    print('---test_shortcut()')
    print("folders:\n Home: {}\n Desktop: {}\n StartMenu: {}\n".format(
        folders.home, folders.desktop, folders.startmenu))

    script = os.path.join(root, 'examples', 'console_scripts', 'timer.py') + ' -u 0.25 -t 10'
    icon  = os.path.join(root, 'examples', 'icons', 'stopwatch')

    iext = 'ico'
    if platform.startswith('darwin'):
        iext = 'icns'

    icon = "%s.%s" % (icon, iext)
    scut = make_shortcut(script, name='Timer', icon=icon, folder=folders.desktop)
    assert isinstance(scut, Shortcut), 'it returns a shortcut instance'

def test_none_script():
    '''Verify we get ValueError if cmd is None (#19)'''
    print('---test_none_script()')
    with pytest.raises(ValueError):
        cmd = None
        scut = make_shortcut(cmd, name="My Script is None")
    print('OK')

def test_empty_string_script():
    '''Verify we get ValueError if cmd is an empty string (#19)'''
    print('---test_empty_script()')
    with pytest.raises(ValueError):
        cmd = ""
        scut = make_shortcut(cmd, name="My Script is empty string")
    print('OK')

if __name__ == '__main__':
    test_shortcut()
    test_none_script()
    test_empty_string_script()
