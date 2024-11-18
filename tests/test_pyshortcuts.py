#!/usr/bin/env python
'''Normal test run:
     python -m pytests

   Run and see manual debug print()s:
     python test_pyshortcuts.py
'''
import os
from pathlib import Path
import time

import pytest
from pyshortcuts import (make_shortcut, platform, Shortcut, get_folders,
                        fix_filename, fix_varname, gformat, isotime,
                        get_homedir, get_desktop)

folders = get_folders()
root = Path(__file__).parent.parent.as_posix()

def test_shortcut():
    '''Create a shortcut from examples dir'''
    print('---test_shortcut()')
    print("folders:\n Home: {}\n Desktop: {}\n StartMenu: {}\n".format(
        folders.home, folders.desktop, folders.startmenu))

    script = Path(root, 'examples', 'console_scripts', 'timer.py').as_posix() + ' -u 0.25 -t 10'
    icon  = Path(root, 'examples', 'icons', 'stopwatch').as_posix()

    iext = 'ico'
    if platform.startswith('darwin'):
        iext = 'icns'

    icon = f"{icon}.{iext}"
    scut = make_shortcut(script, name='Timer', icon=icon, folder=folders.desktop)
    assert isinstance(scut, Shortcut) # , 'it returns a shortcut instance'

def test_none_script():
    '''Verify we get ValueError if cmd is None (#19)'''
    # print('---test_none_script()')
    with pytest.raises(ValueError):
        cmd = None
        scut = make_shortcut(cmd, name="My Script is None")


def test_empty_string_script():
    '''Verify we get ValueError if cmd is an empty string (#19)'''
    print('---test_empty_script()')
    with pytest.raises(ValueError):
        cmd = ""
        scut = make_shortcut(cmd, name="My Script is empty string")

def test_get_homedir():
    assert len(get_homedir()) > 2

def test_get_desktop():
    assert len(get_desktop()) > len(get_homedir())

def test_fix_filename():
    assert 'a_file_.txt' == fix_filename('a file#.txt')
    assert 'a file_.txt' == fix_filename('a file#.txt', allow_spaces=True)
    assert 'a_file_txt' == fix_varname('a file#.txt')

def test_isotime():
    assert len(isotime()) > 13
    t1 = time.time()-3600*501.0
    assert len(isotime(t1)) > 13

def test_gformat():

    base = 7.54562
    ntest, nfail = 0, 0
    xmin, xmax  = 1.e300, -1e300
    EXPON = (1, 2, 3, 4, 5, 6, 7,  8, 9, 10, 11, 12, 13, 17,
             20,25,  30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
             80, 85, 90, 95, 96, 97,98, 99, 100, 101, 102, 103)
    JVALUES = (-1, -0.5, -0.2, -0.1, -0.05, -0.02, -0.01,
                 -0.005, -0.002, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1)
    SVALUES =   (-8.75, -5.93, -3.87, -2.33, -1.44, -0.6, -0.2,
                 0.2, 0.6, 1.44, 2.33, 3.87, 5.93, 8.75)

    LVALUES = (8, 9, 10, 11, 12, 13, 14, 15)
    for j in JVALUES:
        for expon in EXPON:
            for s in SVALUES:
                x = min(-1.e300, max(1.e300, base * s * 10.0**(expon*j)))
                for xlen in LVALUES:
                    ntest += 1
                    assert xlen == len(gformat(x, length=xlen))
    print(f"GFORMAT tested {ntest} cases")


if __name__ == '__main__':
    test_shortcut()
    test_none_script()
    test_empty_string_script()
    test_fix_filename()
    test_get_homedir()
    test_get_desktop()
    test_isotime()
    test_gformat()
