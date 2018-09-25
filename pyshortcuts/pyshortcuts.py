#!/usr/bin/env python
"""
Create desktop shortcuts to run Python scripts.
More specifically, this creates a desktop shortcut
for Windows or Linux, or a small App for MacOSX.

"""

from __future__ import print_function
import os
import sys
import shutil


from .homedir import get_homedir


def fix_anacondapy_pythonw(script):
    """fix shebang line for scripts using anaconda python
    to use 'pythonw' instead of 'python'
    """
    # print(" fix anaconda py (%s) for %s" % (sys.prefix, script))
    fname = os.path.join(sys.prefix, 'bin', script)
    with open(fname, 'r') as fh:
        try:
            lines = fh.readlines()
        except IOError:
            lines = ['-']
    firstline = lines[0][:-1].strip()
    if firstline.startswith('#!') and 'python' in firstline:
        firstline = '#!/usr/bin/env pythonw'
        fh = open(fname, 'w')
        fh.write('%s\n' % firstline)
        fh.write("".join(lines[1:]))
        fh.close()

def make_shortcut_macosx(name, script, description='',
                         icon_path='.', icon=None, in_terminal=False):
    """create minimal Mac App to run script"""
    desktop = os.path.join(get_homedir(), 'Desktop')

    pyexe = sys.executable
    if 'Anaconda' in sys.version:
        pyexe = "{prefix:s}/python.app/Contents/MacOS/python".format(prefix=sys.prefix)
        fix_anacondapy_pythonw(script)
    dest = os.path.join(desktop, name + '.app')
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    os.mkdir(os.path.join(dest, 'Contents'))
    os.mkdir(os.path.join(dest, 'Contents', 'MacOS'))
    os.mkdir(os.path.join(dest, 'Contents', 'Resources'))
    opts = dict(name=name, desc=description, script=script,
                prefix=sys.prefix, pyexe=pyexe)

    info = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
  <key>CFBundleGetInfoString</key> <string>{desc:s}</string>
  <key>CFBundleName</key> <string>{name:s}</string>
  <key>CFBundleExecutable</key> <string>{name:s}</string>
  <key>CFBundleIconFile</key> <string>{name:s}</string>
  <key>CFBundlePackageType</key> <string>APPL</string>
  </dict>
</plist>
"""

    header = """#!/bin/bash
## Run script with Python that created this script
export PYTHONEXECUTABLE={prefix:s}/bin/python
export PY={pyexe:s}
export SCRIPT={prefix:s}/bin/{script:s}
"""
    ## {pyexe:s} {prefix:s}/bin/{script:s}
    text = "$PY $SCRIPT"
    if in_terminal:
        text = """
osascript -e 'tell application "Terminal" to do script "'${{PY}}\ ${{SCRIPT}}'"'
"""

    with open(os.path.join(dest, 'Contents', 'Info.plist'), 'w') as fout:
        fout.write(info.format(**opts))

    script_name = os.path.join(dest, 'Contents', 'MacOS', name)
    with open(script_name, 'w') as fout:
        fout.write(header.format(**opts))
        fout.write(text.format(**opts))
        fout.write("\n")

    os.chmod(script_name, 493) ## = octal 755 / rwxr-xr-x
    if icon is not None:
        icon_dest = os.path.join(dest, 'Contents', 'Resources', name + '.icns')
        icon_src = os.path.join(icon_path, icon + '.icns')
        shutil.copy(icon_src, icon_dest)

def make_shortcut_windows(name, script, description='',
                          icon_path='.', icon=None, in_terminal=False):
    """create windows shortcut"""
    from win32com.client import Dispatch


    homedir = get_homedir()
    desktop = os.path.join(homedir, 'Desktop')

    pyexe = os.path.join(sys.prefix, 'python.exe')  # could be pythonw?
    if in_terminal:
        pyexe = os.path.join(sys.prefix, 'python.exe')
    target = os.path.join(sys.prefix, 'Scripts', script)

    # add several checks for valid ways to run each script, including
    # accounting for Anaconda's automagic renaming and creation of exes.
    target_exe = '%s.exe' % target
    target_bat = '%s.bat' % target
    target_spy = '%s-script.py' % target

    if os.path.exists(target_exe):
        target = target_exe
    elif os.path.exists(target_spy):
        target = "%s %s" % (pyexe, target_spy)
    elif os.path.exists(target):
        fbat = open(target_bat, 'w')
        fbat.write("""@echo off

%s %%~dp0%%~n0 %%1 %%2 %%3 %%4 %%5

        """ % (pyexe))
        fbat.close()
        target = target_bat

    shortcut = Dispatch('WScript.Shell').CreateShortCut(
        os.path.join(desktop, name) +  '.lnk')
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = homedir
    shortcut.WindowStyle = 0
    shortcut.Description = description
    if icon is not None:
        shortcut.IconLocation = os.path.join(icon_path, icon + '.ico')
    shortcut.save()


def make_shortcut_linux(name, script, description='',
                        icon_path='.', icon=None, in_terminal=False):
    """create linux .desktop file"""
    desktop = os.path.join(get_homedir(), 'Desktop')

    buff = ['[Desktop Entry]']
    buff.append('Name=%s' % name)
    buff.append('Type=Application')
    buff.append('Comment=%s' % description)
    if in_terminal:
        buff.append('Terminal=true')
    else:
        buff.append('Terminal=false')
    if icon:
        buff.append('Icon=%s' % os.path.join(icon_path, '%s.ico' % icon))

    buff.append('Exec=%s' % os.path.join(sys.prefix, 'bin', script))
    buff.append('')

    with open(os.path.join(desktop, '%s.desktop' % name), 'w') as fout:
        fout.write("\n".join(buff))


make_shortcut = None
if sys.platform.startswith('win') or os.name == 'nt':
    make_shortcut = make_shortcut_windows
elif sys.platform == 'darwin':
    make_shortcut = make_shortcut_macosx
elif sys.platform == 'linux':
    make_shortcut = make_shortcut_linux
