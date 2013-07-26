@echo off

set version=1.0.2
set projectdir=..
set pyscript=%projectdir%\scrobbler.py
set isccscript=setup.iss

set python32dir=C:\Python33x86
set python64dir=C:\Python33

set python32=%python32dir%\python.exe
set python64=%python64dir%\python.exe

set cxfreeze32=%python32dir%\Scripts\cxfreeze
set cxfreeze64=%python64dir%\Scripts\cxfreeze

set win32filesdir=win32setupfiles
set win64filesdir=win64setupfiles

set cxfreeze32flags=--target-dir=%win32filesdir%
set cxfreeze64flags=--target-dir=%win64filesdir%

set setupsdir=winsetups
set iscc="C:\Program Files (x86)\Inno Setup 5\iscc.exe"
set isscflags=/dMyAppVersion=%version% /dProjectDir=%projectdir% /o%setupsdir%
set iscc32flags=%isscflags% /dSourceFilesDir=%win32filesdir% /fscrobbler-%version%-32bit
set iscc64flags=%isscflags% /dSourceFilesDir=%win64filesdir% /fscrobbler-%version%-64bit


del /F /Q %setupsdir%

del /F /Q %win32filesdir%
%python32% %cxfreeze32% %cxfreeze32flags% %pyscript%
%iscc% %iscc32flags% %isccscript%

del /F /Q %win64filesdir%
%python64% %cxfreeze64% %cxfreeze64flags% %pyscript%
%iscc% %iscc64flags% %isccscript%
