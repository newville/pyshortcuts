#!/usr/bin/env python
"""
Create desktop shortcuts for Darwin / MacOS
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
from collections import namedtuple

from .utils import  get_pyexe, get_homedir

def get_startmenu():
    "get start menu location"
    return ''

def get_desktop():
    "get desktop location"
    return Path(get_homedir(), 'Desktop').resolve().as_posix()

def get_folders():
    """get user-specific folders

    Returns:
    -------
    Named tuple with fields 'home', 'desktop', 'startmenu'

    Example:
    -------
    >>> from pyshortcuts import get_folders
    >>> folders = get_folders()
    >>> print("Home, Desktop, StartMenu ",
    ...       folders.home, folders.desktop, folders.startmenu)
    """
    UserFolders = namedtuple("UserFolders", ("home", "desktop", "startmenu"))
    return UserFolders(get_homedir(), get_desktop(), get_startmenu())


def make_shortcut(script, name=None, description=None, icon=None, working_dir=None,
                  folder=None, terminal=True, desktop=True,
                  startmenu=False, executable=None, noexe=False):
    """create shortcut

    Arguments:
    ---------
    script      (str) path to script, may include command-line arguments
    name        (str, None) name to display for shortcut [name of script]
    description (str, None) longer description of script [`name`]
    icon        (str, None) path to icon file [python icon]
    working_dir (str, None) directory where to run the script in
    folder      (str, None) subfolder of Desktop for shortcut [None] (See Note 1)
    terminal    (bool) whether to run in a Terminal [True]
    desktop     (bool) whether to add shortcut to Desktop [True]
    startmenu   (bool) whether to add shortcut to Start Menu [False] (See Note 2)
    executable  (str, None) name of executable to use [this Python] (see Note 3)
    noexe       (bool) whether to use no executable (script is entire command) [False]

    Notes:
    ------
    1. `folder` will place shortcut in a subfolder of Desktop and/or Start Menu
    2. Start Menu does not exist for Darwin / MacOSX
    3. executable defaults to the Python executable used to make shortcut.
    """
    if not desktop:
        return None

    userfolders = get_folders()
    if working_dir is None:
        working_dir = ''

    from .shortcut import shortcut

    print(f" A: {executable=} {noexe=}")
    scut = shortcut(script, userfolders, name=name, description=description,
                    working_dir=working_dir, folder=folder, icon=icon)

    if noexe:
        full_script =scut.script
        executable = ''
    else:
        full_script = scut.full_script
        if executable is None:
            executable = get_pyexe()
        print(f" B: {executable=} ")
        executable = Path(executable).as_posix()
        if Path(scut.full_script) == Path(executable):
            executable = ''
        print(f" C: {executable=} ")
        print(f" : {sys.executable=} / {executable=}")

    if not Path(scut.desktop_dir).exists():
        os.makedirs(scut.desktop_dir)

    osascript = f'{full_script} {scut.arguments}'
    osascript = osascript.replace(' ', '\\ ')

    dest = Path(scut.desktop_dir, scut.target).resolve().as_posix()

    if Path(dest).exists():
        shutil.rmtree(dest)

    os.mkdir(dest)
    os.mkdir(Path(dest, 'Contents'))
    os.mkdir(Path(dest, 'Contents', 'MacOS'))
    os.mkdir(Path(dest, 'Contents', 'Resources'))

    opts = {'name': scut.name,
            'desc': scut.description,
            'script': full_script,
            'workdir': scut.working_dir,
            'args': scut.arguments,
            'prefix': Path(sys.prefix).as_posix(),
            'exe': executable,
            'osascript': osascript}

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

    # Build command string
    if executable:
        cmd = f"{executable} {full_script} {scut.arguments}"
    else:
        cmd = f"{full_script} {scut.arguments}"

    # For GUI apps, create an Automator-style app that CrowdStrike trusts
    if not terminal:
        automator_dir = Path(dest, 'Contents', 'Resources')

        workflow = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>AMApplicationBuild</key>
    <string>523</string>
    <key>AMApplicationVersion</key>
    <string>2.10</string>
    <key>AMDocumentVersion</key>
    <string>2</string>
    <key>actions</key>
    <array>
        <dict>
            <key>action</key>
            <dict>
                <key>AMActionVersion</key>
                <string>1.0.2</string>
                <key>AMApplication</key>
                <array>
                    <string>Automator</string>
                </array>
                <key>AMParameterProperties</key>
                <dict>
                    <key>source</key>
                    <dict/>
                </dict>
                <key>AMProvides</key>
                <dict>
                    <key>Container</key>
                    <string>List</string>
                    <key>Types</key>
                    <array>
                        <string>com.apple.applescript.object</string>
                    </array>
                </dict>
                <key>ActionBundlePath</key>
                <string>/System/Library/Automator/Run Shell Script.action</string>
                <key>ActionName</key>
                <string>Run Shell Script</string>
                <key>ActionParameters</key>
                <dict>
                    <key>COMMAND_STRING</key>
                    <string>{cmd} &gt; /dev/null 2&gt;&amp;1 &amp;</string>
                    <key>CheckedForUserDefaultShell</key>
                    <true/>
                    <key>inputMethod</key>
                    <integer>0</integer>
                    <key>shell</key>
                    <string>/bin/bash</string>
                    <key>source</key>
                    <string></string>
                </dict>
                <key>BundleIdentifier</key>
                <string>com.apple.RunShellScript</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>'''

        workflow_path = Path(automator_dir, 'document.wflow').as_posix()
        with open(workflow_path, 'w') as f:
            f.write(workflow)

        # Update Info.plist for Automator app with stable bundle ID
        import hashlib
        # Create stable bundle ID based on app name and command
        bundle_id_base = f"{scut.name}-{hashlib.md5(cmd.encode()).hexdigest()[:8]}"

        info_automator = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>English</string>
    <key>CFBundleExecutable</key>
    <string>Application Stub</string>
    <key>CFBundleIconFile</key>
    <string>{scut.name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.pyshortcuts.{bundle_id_base}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>{scut.name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.5</string>
    <key>LSUIElement</key>
    <false/>
    <key>NSMainNibFile</key>
    <string>ApplicationStub</string>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
</dict>
</plist>'''

        with open(Path(dest, 'Contents', 'Info.plist'), 'w') as fout:
            fout.write(info_automator)

        # Copy Automator stub executable
        automator_stub_paths = [
            '/System/Library/CoreServices/Automator Application Stub.app/Contents/MacOS/Automator Application Stub',
            '/System/Library/CoreServices/Automator Launcher.app/Contents/MacOS/Automator Launcher',
        ]

        automator_stub = None
        for stub_path in automator_stub_paths:
            if Path(stub_path).exists():
                automator_stub = stub_path
                break

        if not automator_stub:
            raise FileNotFoundError(
                'Could not find Automator Application Stub. '
                'This may not be supported on your macOS version. '
                'Please use terminal=True.'
            )

        stub_dest = Path(dest, 'Contents', 'MacOS', 'Application Stub').as_posix()
        shutil.copy(automator_stub, stub_dest)

        icon_dest = Path(dest, 'Contents', 'Resources', scut.name + '.icns').as_posix()
        shutil.copy(scut.icon, icon_dest)
    else:
        # For terminal apps, use AppleScript to open Terminal
        with open(Path(dest, 'Contents', 'Info.plist'), 'w') as fout:
            fout.write(info.format(**opts))

        # Create AppleScript launcher
        cmd_escaped = cmd.replace('"', '\\"')
        text = ['#!/usr/bin/osascript',
                'tell application "Terminal"',
                f'    do script "{cmd_escaped}"',
                'end tell',
                '']

        ascript_name = Path(dest, 'Contents', 'MacOS', scut.name).as_posix()
        with open(ascript_name, 'w') as fout:
            fout.write('\n'.join(text))
        os.chmod(ascript_name, 0o755)

        icon_dest = Path(dest, 'Contents', 'Resources', scut.name + '.icns').as_posix()
        shutil.copy(scut.icon, icon_dest)

    # Remove quarantine attributes so macOS will launch the app
    try:
        subprocess.run(['xattr', '-cr', dest], capture_output=True, check=False)
    except Exception:
        pass

    # Try to ad-hoc sign to give it a stable code identity for TCC
    if not terminal:
        try:
            subprocess.run(['codesign', '--force', '--deep', '--sign', '-', dest],
                          capture_output=True, check=False)
        except Exception:
            pass

    return scut
