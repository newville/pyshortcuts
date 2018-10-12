import time
import os
import sys
import wx

is_wxPhoenix = 'phoenix' in wx.PlatformInfo
if is_wxPhoenix:
    PyDeadObjectError = RuntimeError
else:
    from wx._core import PyDeadObjectError

import wx.lib.filebrowsebutton as filebrowse

from pyshortcuts import make_shortcut
from pyshortcuts.shortcut import Shortcut, fix_filename
from pyshortcuts.utils import platform, get_homedir

PY_FILES = "Python scripts (*.py)|*.py"
ALL_FILES = "All files (*.*)|*.*"
ICO_FILES = "Icon files (*.ico)|*.ico"
ICNS_FILES = "Mac Icon files (*.icns)|*.icns"

CEN = wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL
LEFT = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL
RIGHT = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL
ALL_CEN =  wx.ALL|CEN
ALL_LEFT =  wx.ALL|LEFT
ALL_RIGHT =  wx.ALL|RIGHT

FONTSIZE = 11
if platform == 'linux':
    FONTSIZE = 10

class ShortcutFrame(wx.Frame):
    def __init__(self):

        wx.Frame.__init__(self, None, -1, 'Pyshortcuts Creator',
                          style=wx.DEFAULT_FRAME_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)
        self.SetTitle('Pyshortcuts Creator')

        self.SetFont(wx.Font(FONTSIZE, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        menu = wx.Menu()
        menu_exit = menu.Append(-1, "Q&uit", "Exit")

        menuBar = wx.MenuBar()
        menuBar.Append(menu, "&File");
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.onExit, menu_exit)
        self.Bind(wx.EVT_CLOSE, self.onExit)

        panel      = wx.Panel(self)

        opts = dict(size=(175, -1))
        lab_script = wx.StaticText(panel, label='  Python Script:', **opts)
        lab_args  = wx.StaticText(panel, label='  Command-line Arguments:', **opts)
        lab_name  = wx.StaticText(panel, label='  Shortcut Name:', **opts)
        lab_desc  = wx.StaticText(panel, label='  Description:', **opts)
        lab_icon  = wx.StaticText(panel, label='  Icon File:', **opts)
        lab_folder = wx.StaticText(panel, label='  Desktop SubFolder:', **opts)
        lab_opts  = wx.StaticText(panel, label='  Options:', **opts)

        opts['size'] = (400, -1)

        sopts = dict(size=(400, -1), style=wx.TE_PROCESS_ENTER)

        self.txt_script = wx.TextCtrl(panel, value='', **sopts)
        self.txt_args = wx.TextCtrl(panel, value='', **opts)
        self.txt_name = wx.TextCtrl(panel, value='', **sopts)
        self.txt_desc = wx.TextCtrl(panel, value='', **opts)
        self.txt_icon = wx.TextCtrl(panel, value='', **opts)
        self.txt_folder= wx.TextCtrl(panel, value='', **opts)

        self.txt_script.Bind(wx.EVT_TEXT_ENTER, self.onScriptEnter)
        self.txt_name.Bind(wx.EVT_TEXT_ENTER, self.onNameEnter)

        self.opt_terminal = wx.CheckBox(panel, label='Run in Terminal?',
                                        size=(200, -1))
        self.opt_terminal.SetValue(1)

        btn_script = wx.Button(panel, -1, label='Browse', size=(100, -1))
        btn_script.Bind(wx.EVT_BUTTON, self.onBrowseScript)

        btn_icon = wx.Button(panel, -1, label='Browse', size=(100, -1))
        btn_icon.Bind(wx.EVT_BUTTON, self.onBrowseIcon)

        btn_folder = wx.Button(panel, -1, label='Browse', size=(100, -1))
        btn_folder.Bind(wx.EVT_BUTTON, self.onBrowseFolder)

        sizer = wx.GridBagSizer(5, 5)

        irow = 0
        sizer.Add(wx.StaticLine(self, size=(650, 4)), (irow, 0), (1, 3), ALL_CEN)

        irow += 1
        sizer.Add(lab_script,      (irow, 0), (1, 1), ALL_LEFT)
        sizer.Add(self.txt_script, (irow, 1), (1, 1), ALL_LEFT)
        sizer.Add(btn_script,      (irow, 2), (1, 1), ALL_RIGHT)

        irow += 1
        sizer.Add(lab_args,       (irow, 0), (1, 1), ALL_LEFT)
        sizer.Add(self.txt_args,  (irow, 1), (1, 1), ALL_LEFT)

        irow += 1
        sizer.Add(lab_name,       (irow, 0), (1, 1), ALL_LEFT)
        sizer.Add(self.txt_name,  (irow, 1), (1, 1), ALL_LEFT)

        irow += 1
        sizer.Add(lab_desc,       (irow, 0), (1, 1), ALL_LEFT)
        sizer.Add(self.txt_desc,  (irow, 1), (1, 1), ALL_LEFT)

        irow += 1
        sizer.Add(lab_icon,       (irow, 0), (1, 1), ALL_LEFT)
        sizer.Add(self.txt_icon,  (irow, 1), (1, 1), ALL_LEFT)
        sizer.Add(btn_icon,       (irow, 2), (1, 1), ALL_RIGHT)

        irow += 1
        sizer.Add(lab_folder,      (irow, 0), (1, 1), ALL_LEFT)
        sizer.Add(self.txt_folder, (irow, 1), (1, 1), ALL_LEFT)
        sizer.Add(btn_folder,      (irow, 2), (1, 1), ALL_RIGHT)

        irow += 1
        sizer.Add(lab_opts,         (irow, 0), (1, 1), ALL_LEFT)
        sizer.Add(self.opt_terminal, (irow, 1), (1, 1), ALL_LEFT)

        irow += 1
        sizer.Add(wx.StaticLine(self, size=(650, 4)), (irow, 0), (1, 3), ALL_CEN)

        btn_create = wx.Button(panel, label='Create Shortcut',  size=(175, -1))
        btn_create.Bind(wx.EVT_BUTTON, self.onCreate)

        btn_savepy = wx.Button(panel, label='Save Python Code', size=(175, -1))
        btn_savepy.Bind(wx.EVT_BUTTON, self.onSavePy)


        bsizer = wx.BoxSizer(wx.HORIZONTAL)
        bsizer.Add(btn_create, 1,  ALL_LEFT, 3)
        bsizer.Add(btn_savepy, 1,  ALL_LEFT, 3)

        irow += 1
        sizer.Add(bsizer, (irow, 0), (1, 3), ALL_LEFT)

        panel.SetSizer(sizer)
        sizer.Fit(panel)

        fsizer = wx.BoxSizer(wx.VERTICAL)
        fsizer.Add(panel, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER|wx.EXPAND)
        fsizer.Fit(self)
        self.Refresh()

    def onBrowseScript(self, event=None):
        wildcards = "%s|%s" % (PY_FILES, ALL_FILES)

        dlg = wx.FileDialog(self, message='Select Python Script file',
                            wildcard=wildcards,
                            style=wx.FD_OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            path = os.path.abspath(dlg.GetPath())
            self.txt_script.SetValue(path)

            _, name = os.path.split(path)
            name = fix_filename(name)
            if name.endswith('.py'):
                name = name[:-3]

            txt_name = self.txt_name.GetValue().strip()
            if len(txt_name) < 1:
                self.txt_name.SetValue(name)

            txt_desc = self.txt_desc.GetValue().strip()
            if len(txt_desc) < 1:
                self.txt_desc.SetValue(name)
        dlg.Destroy()


    def onBrowseIcon(self, event=None):

        wildcards = "%s|%s" % (ICO_FILES, ALL_FILES)
        if platform.startswith('darwin'):
            wildcards = "%s|%s" % (ICNS_FILES, ALL_FILES)

        dlg = wx.FileDialog(self, message='Select Icon file',
                            wildcard=wildcards,
                            style=wx.FD_OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            path = os.path.abspath(dlg.GetPath())
            self.txt_icon.SetValue(path)
        dlg.Destroy()


    def onBrowseFolder(self, event=None):
        defdir = self.txt_folder.GetValue()
        if defdir in ('', 'Desktop'):
            defdir = os.path.join(get_homedir(), 'Desktop')
        dlg = wx.DirDialog(self,
                           message='Select Folder for Shortcut',
                           defaultPath=defdir,
                           style = wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            folder = os.path.abspath(dlg.GetPath())
            desktop = os.path.join(get_homedir(), 'Desktop')
            if folder.startswith(desktop):
                folder.replace(desktop, '')
                if folder.startswith('/'):
                    folder = folder[1:]
            self.txt_folder.SetValue(folder)
        dlg.Destroy()


    def onScriptEnter(self, event=None):
        path = self.txt_script.GetValue()

        _, name = os.path.split(path)
        name = fix_filename(name)
        if name.endswith('.py'):
            name = name[:-3]

        txt_name = self.txt_name.GetValue().strip()
        if len(txt_name) < 1:
            self.txt_name.SetValue(name)

        txt_desc = self.txt_desc.GetValue().strip()
        if len(txt_desc) < 1:
            self.txt_desc.SetValue(name)


    def onNameEnter(self, event=None):
        name = self.txt_name.GetValue()
        txt_desc = self.txt_desc.GetValue().strip()
        if len(txt_desc) < 1:
            self.txt_desc.SetValue(name)

    def make_Shortcut(self):
        script = self.txt_script.GetValue() or None
        args = self.txt_args.GetValue() or None
        name = self.txt_name.GetValue() or None
        desc = self.txt_desc.GetValue() or None
        icon = self.txt_icon.GetValue() or None
        folder = self.txt_folder.GetValue() or None

        if script is None:
            dlg = wx.MessageDialog(self, "script required",
                                   style=wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return

        if folder is not None:
            desktop = os.path.join(get_homedir(), 'Desktop')
            if folder.startswith(desktop):
                folder.replace(desktop, '')
                if folder.startswith('/'):
                    folder = folder[1:]

        if args is not None:
            script = "%s %s" % (script, args)

        return Shortcut(script, name=name, description=desc,
                        folder=folder, icon=icon)

    def onCreate(self, event=None):
        scut = self.make_Shortcut()
        script = "%s %s" % (scut.script, scut.args)

        make_shortcut(script.strip(),
                      name=scut.name,
                      description=scut.description,
                      folder=scut.folder,
                      icon=scut.icon,
                      terminal=self.opt_terminal.IsChecked())


    def onSavePy(self, event=None):
        scut = self.make_Shortcut()
        script = "%s %s" % (scut.script, scut.args)

        opts = dict(script=script.strip(),
                    name=scut.name,
                    desc=scut.description,
                    folder=scut.folder,
                    icon=scut.icon,
                    terminal=repr(self.opt_terminal.IsChecked()))

        buff = ['#!/usr/bin/env python',
                'from pyshortcuts import make_shortcut',
                """make_shortcut('{script:s}',
        name='{name:s}',
        description='{desc:s}',
        folder='{folder:s}',
        icon='{icon:s}',
        terminal={terminal:s})""".format(**opts),
                '']

        wildcards = "%s|%s" % (PY_FILES, ALL_FILES)
        dlg = wx.FileDialog(self, message='Save Python script for creating shortcut',
                            defaultFile='make_shortcut.py',
                            wildcard=wildcards,
                            style=wx.FD_SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = os.path.abspath(dlg.GetPath())
            with open(path, 'w') as fh:
                fh.write('\n'.join(buff))





    def onAbout(self, event):
        dlg = wx.MessageDialog(self, "pyshortcuts Graphical User Interface",
                               style=wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def onExit(self, event):
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    ShortcutFrame().Show(True)
    app.MainLoop()
