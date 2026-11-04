@echo off
cd /d "%~dp0"

echo Test: Nested VFS

py -c "import zipfile as z; f=z.ZipFile('vfs_test_deep.zip','w'); f.writestr('a/b/c/main.py','print(1)'); f.close()"

py -m src.main --vfs vfs_test_deep.zip --script startup.txt

echo Test: Startup script error

py -m src.main --vfs vfs_test_deep.zip --script startup_error.txt

pause