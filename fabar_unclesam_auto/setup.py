import sys
from cx_Freeze import setup, Executable

# base = None
# if (sys.platform  == "win32"):
#     base = "Win32GUI"

 
# setup(
#     name='Unclesam FBAR Automation',
#     version='2.0.1',
#     author='HyeonUk',
#     description = 'Unclesam FBAR Automation',
#     executables = [Executable(script="main.py",base = base,icon = "unclesam_icon2.ico",targetName="build.exe")]
# )

setup(
    name='Unclesam FBAR Automation',
    version='2.0.1',
    author='HyeonUk',
    description = 'Unclesam FBAR Automation',
    executables = [Executable(script="main.py",base = "Win32GUI",icon = "unclesam_icon2.ico",targetName="build.exe")]
)
