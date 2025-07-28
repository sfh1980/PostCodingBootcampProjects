import PyInstaller.__main__
import os

# Build the self-installing executable
PyInstaller.__main__.run([
    'simple_self_installer.py',
    '--onefile',
    '--windowed',  # No console window
    '--name=UpTime_Installer',
    '--hidden-import=win32com.client',
    '--hidden-import=win32com',
    '--hidden-import=win32api',
    '--hidden-import=win32con',
    '--distpath=dist',
    '--workpath=build',
    '--specpath=build'
])

print("Self-installing UpTime executable created!")
print("File: dist/UpTime_Installer.exe")
print("This single file will install UpTime and start it automatically.")
print("Run it as Administrator to install for all users.") 