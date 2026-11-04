@echo off
cd /d "%~dp0"

echo Test 1: Minimal VFS
py -c "import zipfile as z; f=z.ZipFile('vfs_test_min.zip','w'); f.writestr('a.txt','Hello'); f.close()"

py -m src.main --vfs vfs_test_min.zip --script startup.txt

echo Test 2: Multiple files
py -c "import zipfile as z; f=z.ZipFile('vfs_test_multi.zip','w'); f.writestr('a','1'); f.writestr('b','2'); f.close()"

py -m src.main --vfs vfs_test_multi.zip --script startup.txt

pause