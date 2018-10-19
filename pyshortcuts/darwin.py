#!/usr/bin/env python
"""
Create desktop shortcuts for Darwin / MacOS
"""
from __future__ import print_function
import os
import sys
import shutil

from .shortcut import Shortcut

def fix_anacondapy_pythonw(fname):
    """fix shebang line for scripts using anaconda python
    to use 'pythonw' instead of 'python'
    """
    # print(" fix anaconda py (%s) for %s" % (sys.prefix, script))
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

def make_shortcut(script, name=None, description=None, terminal=True,
                  folder=None, icon=None):
    """create minimal Mac App to run script

    Arguments
    ---------
    script      (str)  path to script to run.  This can include  command-line arguments
    name        (str or None) name to use for shortcut [defaults to script name]
    description (str or None) longer description of script [defaults to `name`]
    icon        (str or None) path to icon file [defaults to python icon]
    folder      (str or None) folder on Desktop to put shortcut [defaults to Desktop]
    terminal    (True or False) whether to run in a Terminal  [True]
    """
    scut = Shortcut(script, name=name, description=description, folder=folder, icon=icon)

    osascript = '%s %s' % (scut.full_script, scut.args)
    osascript = osascript.replace(' ', '\\ ')

    pyexe = sys.executable
    if 'Anaconda' in sys.version:
        pyexe = "{prefix:s}/python.app/Contents/MacOS/python".format(prefix=sys.prefix)
        fix_anacondapy_pythonw(scut.full_script)


    dest = scut.target
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    os.mkdir(os.path.join(dest, 'Contents'))
    os.mkdir(os.path.join(dest, 'Contents', 'MacOS'))
    os.mkdir(os.path.join(dest, 'Contents', 'Resources'))
    opts = dict(name=scut.name,
                desc=scut.description,
                script=scut.full_script,
                args=scut.args,
                prefix=sys.prefix,
                pyexe=pyexe,
                osascript=osascript)

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
export SCRIPT={script:s}
export ARGS='{args:s}'
"""
    text = "$PY $SCRIPT $ARGS"
    if terminal:
        text = """
osascript -e 'tell application "Terminal"
   do script "'${{PY}}\ {osascript:s}'"
end tell
'
"""

    with open(os.path.join(dest, 'Contents', 'Info.plist'), 'w') as fout:
        fout.write(info.format(**opts))

    ascript_name = os.path.join(dest, 'Contents', 'MacOS', scut.name)
    with open(ascript_name, 'w') as fout:
        fout.write(header.format(**opts))
        fout.write(text.format(**opts))
        fout.write("\n")

    os.chmod(ascript_name, 493) ## = octal 755 / rwxr-xr-x
    icon_dest = os.path.join(dest, 'Contents', 'Resources', scut.name + '.icns')
    shutil.copy(scut.icon, icon_dest)
