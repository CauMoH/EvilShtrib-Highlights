@echo off
:loop
"C:\Program Files (x86)\Steam\steam.exe" -silent
if %ERRORLEVEL% equ 42 goto loop
