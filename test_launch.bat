@echo off
cd /d "%~dp0"

echo Test 1: No arguments
py -m src.main

echo Test 2: VFS path
py -m src.main --vfs filesystem.zip

echo Test 3: Startup script
py -m src.main --script startup.txt

echo Test 4: Both arguments
py -m src.main --vfs filesystem.zip --script startup.txt

pause