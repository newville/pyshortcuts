@set _prompt=%prompt%
@prompt $g$s
@echo.
@echo --- Creating timer.bat with current python.exe path
python -c "import sys;print(r'{} %%~dp0\timer.py'.format(sys.executable))" > ..\examples\console_scripts\timer.bat
@echo.
@echo --- Creating shortcut to timer.bat
call pyshortcut -n "Timer bat" -i ..\examples\icons\stopwatch.ico -f Shortcuts ..\examples\console_scripts\timer.bat 
@echo.
@echo --- Look in Startmenu and Desktop\Shortcuts for launcher link
@echo.
@pause
@prompt=%_prompt%
