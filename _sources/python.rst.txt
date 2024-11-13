.. _python_section:

Using `pyshortcuts`  from Python
-------------------------------------

Shortcuts can be created from a Python script with::

    from pyshortcuts import make_shortcut
    make_shortcut('/home/user/bin/myapp.py', name='MyApp', icon='/home/user/icons/myicon.ico')

.. function:: make_shortcut(script, name=None, description=None, icon=None, working_dir=None, folder=None, terminal=True, desktop=True,  startmenu=True, executable=None, noexe=False)

   create a desktop shortcut

   :param script: path to script, may include command-line arguments
   :type  script:   string
   :param name: name to display for shortcut [name of script]
   :type  name:   string or ``None``
   :param description: longer description of script [name]
   :type  description:   string or ``None``
   :param icon: filename for icon file [python icon]
   :type  icon:   string or ``None``
   :param working_dir: directory where to run the script in
   :type  working_dir:   string or ``None``
   :param folder: name of subfolder of Desktop for shortcut [None] (See Note 1)
   :type folder:   string or ``None``
   :param terminal: whether to run in a Terminal [True]
   :type terminal:   bool
   :param desktop: whether to add shortcut to Desktop [True]
   :type desktop:   bool
   :param start_menu: whether to add shortcut to Start Menu [True, except on macOS]
   :type start_menu:   bool
   :param executable: name of executable to use [this Python] (see Note 3)
   :type executable:   string or ``None``.
   :param noexe: whether to use no executable, so that the script is entire command  [False]
   :type noexe:   bool

Notes:

    1. `folder` will place shortcut in a subfolder of Desktop and/or Start Menu
    2. Start Menu does not exist for Darwin / MacOSX
    3. executable defaults to the Python executable used to make shortcut.



Making a shortcut for single python command
---------------------------------------------


A common request and simple use-case for `pyshortcuts` is to wrap a single
python command.  An example of this might look like this::

    import sys
    from pyshortcuts import make_shortcut

    pycmd = "_ -m pip install --upgrade pyshortcuts"

    make_shortcut(pycmd, name='Update Pyshortcuts')


Note that using `_` or `{}` as the command name will indicate that the
current Python executable should be be used. An example that includes
an icon is given in the examples folder.

The above could be done from the command line with::


   ~> pyshortcut -n "Update Pyshortcuts" "_ -m pip install pyshortcuts"
