import os
import sys
from pathlib import Path
import subprocess

# Ensure pip is up to date and install required packages
cur_path = Path(sys.path[0])

# Create the shortcut for the DNS changer
shortcut_path = Path.home() / "Desktop" / "DNS Changer.lnk"
target = str(cur_path / "main.py")
icon_path = str(cur_path / "icon" / "dns-logo.ico")  # Ensure you have a .ico file for Windows

# Create a batch file to run the DNS changer with elevated privileges
batch_file_content = f'''@echo off
powershell -Command "Start-Process python -ArgumentList '{target}' -Verb runAs"
'''

batch_file_path = cur_path / "dns_changer.bat"
with open(batch_file_path, 'w') as batch_file:
    batch_file.write(batch_file_content)

# Create a shortcut
try:
    import winshell
    from win32com.client import Dispatch

    shell = Dispatch('WScript.Shell')
    # shortcut = shell.CreateShortCut(str(shortcut_path))
    # shortcut.Targetpath = str(batch_file_path)
    # shortcut.WorkingDirectory = str(cur_path)
    # shortcut.IconLocation = icon_path
    # shortcut.save()
except ImportError:
    print("Please install the required modules: winshell, pypiwin32")

print('------------------\nInstalled successfully\nRun "DNS Changer" from the Desktop')

# Ensure you have winshell and pypiwin32 installed
subprocess.run([sys.executable, "-m", "pip", "install", "winshell", "pypiwin32"])
