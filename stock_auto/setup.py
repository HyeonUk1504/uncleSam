import sys
from cx_Freeze import setup, Executable

if (sys.platform  == "win32"):
    base = "Win32GUI"

 
setup(
    name='Demo',
    version='0.0.1',
    author='HyeonUk',
    description = 'Demo',
    executables = [Executable(script="main.py",base = "Win32GUI",icon = "bob.ico",targetName="build.exe")]
)
 