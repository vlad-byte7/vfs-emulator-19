@echo off
cd /d "%~dp0"

echo Test 1: Error in startup script
py -m src.main --vfs filesystem.zip --script startup_error.txt

echo Test 2: Missing startup script
py -m src.main --vfs filesystem.zip --script missing.txt

echo Test 3: Unknown argument
py -m src.main --unknown

pause