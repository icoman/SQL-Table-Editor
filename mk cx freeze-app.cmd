@echo off

rem
rem may need vc_redist_x86-2008
rem and also vcredist_x86-runtime-2010
rem

SET DIR=SqlEdit
rd %DIR% /s /q
c:\Python27\python c:\Python27\Scripts\cxfreeze --base-name=Win32GUI -OO -c -s --install-dir=%DIR% main.py

copy *.rsrc.py %DIR%\ 
copy *.ico %DIR%\
rd /s /q %DIR%\tcl
rd /s /q %DIR%\tk
del %DIR%\tcl*.*
del %DIR%\tk*.*


pause

