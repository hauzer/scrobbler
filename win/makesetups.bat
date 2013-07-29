@echo off

set projectdir=..
set cxscript=setup.py
set isccscript=setup.iss
set setupsdir=setups

set python32dir=C:\Python33x86
set python64dir=C:\Python33

set python32=%python32dir%\python.exe
set python64=%python64dir%\python.exe
set python=%python64%

rem http://stackoverflow.com/questions/2323292/windows-batch-assign-output-of-a-program-to-a-variable
for /f %%i in ('%python% getversion.py') do set version=%%i
for /f %%i in ('%python% getfrozenfile.py') do set frozen_file=%%i

set win32filesdir=build\exe.win32-3.3
set win64filesdir=build\exe.win-amd64-3.3

set iscc="C:\Program Files (x86)\Inno Setup 5\iscc.exe"
set isscdefines=/dMyAppVersion=%version% /dProjectDir=%projectdir% /dFrozenFile=%frozen_file%
set isscflags=%isscdefines% /o%setupsdir%
set iscc32flags=%isscflags% /dSourceFilesDir=%win32filesdir% /fscrobbler-%version%-32bit
set iscc64flags=%isscflags% /dSourceFilesDir=%win64filesdir% /fscrobbler-%version%-64bit


del /F /Q %setupsdir%

del /F /Q %win32filesdir%
%python32% %cxscript% build
rem http://stackoverflow.com/questions/210201/how-to-create-empty-text-file-from-a-batch-file
type nul > %win32filesdir%\%frozen_file%
%iscc% %iscc32flags% %isccscript%

del /F /Q %win64filesdir%
%python64% %cxscript% build
type nul > %win64filesdir%\%frozen_file%
%iscc% %iscc64flags% %isccscript%
