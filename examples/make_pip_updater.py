#!/usrb/bin/env python

"""
This example shows how to make a shortcut that runs a single python command

Here, the comand to run is
     python -m pip install --upgrade pyshortcuts

to update to the latest version of this library.

"""
import os
import sys
from pyshortcuts import make_shortcut, platform

pycmd = f"{sys.executable} -m pip install --upgrade pyshortcuts"

iconfile = 'shovel.icns' if platform.startswith('darwin') else 'shovel.ico'
icon = os.path.abspath(os.path.join(os.getcwd(), 'icons', iconfile))

make_shortcut(pycmd, name='Update Pyshortcuts', icon=icon)
