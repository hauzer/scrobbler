@echo off

set version=1.0.2
set projectdir=..
set cxscript=setup.py
set isccscript=setup.iss
set setupsdir=setups

set python32dir=C:\Python33x86
set python64dir=C:\Python33

set python32=%python32dir%\python.exe
set python64=%python64dir%\python.exe

set win32filesdir=build\exe.win32-3.3
set win64filesdir=build\exe.win-amd64-3.3

set iscc="C:\Program Files (x86)\Inno Setup 5\iscc.exe"
set isscflags=/dMyAppVersion=%version% /dProjectDir=%projectdir% /o%setupsdir%
set iscc32flags=%isscflags% /dSourceFilesDir=%win32filesdir% /fscrobbler-%version%-32bit
set iscc64flags=%isscflags% /dSourceFilesDir=%win64filesdir% /fscrobbler-%version%-64bit


del /F /Q %setupsdir%

del /F /Q %win32filesdir%
%python32% %cxscript% build
%iscc% %iscc32flags% %isccscript%

del /F /Q %win64filesdir%
%python64% %cxscript% build
%iscc% %iscc64flags% %isccscript%
