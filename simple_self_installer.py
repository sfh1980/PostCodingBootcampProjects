import os
import sys
import shutil
import winreg
import subprocess
import threading
import time
import base64
from pathlib import Path
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import psutil

# Installation paths
INSTALL_DIR = r"C:\Program Files\UpTime"
UNINSTALLER_NAME = "UninstallUpTime.exe"
REGISTRY_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\UpTime"

def create_uptime_image():
    """Create the UpTime system tray icon"""
    icon_size = 128
    image = Image.new('RGB', (icon_size, icon_size), "white")
    draw = ImageDraw.Draw(image)
    text = "Up"
    font_size = 92
    
    font_options = [
        "arial.ttf",
        "arial.ttc", 
        "segoeui.ttf",
        "calibri.ttf",
        "tahoma.ttf"
    ]
    
    font = None
    try:
        from PIL import ImageFont
        for font_name in font_options:
            try:
                font = ImageFont.truetype(font_name, font_size)
                break
            except:
                continue
    except:
        pass
    
    if font is None:
        try:
            font = ImageFont.load_default()
            font_size = 48
        except:
            font = None
    
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
    else:
        bbox = draw.textbbox((0, 0), text)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((icon_size - text_width) // 2, (icon_size - text_height) // 2)
    draw.text(position, text, fill="black", font=font)
    
    final_size = 64
    image = image.resize((final_size, final_size), Image.Resampling.LANCZOS)
    return image

def get_uptime():
    """Get current system uptime"""
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"Uptime: {hours}h {minutes}m {seconds}s"

def update_tooltip(icon):
    """Update the tooltip with current uptime"""
    while True:
        icon.title = get_uptime()
        time.sleep(1)

def on_exit(icon, item):
    """Exit the application"""
    icon.stop()

def run_uptime_app():
    """Run the UpTime system tray application"""
    icon = pystray.Icon(
        "uptime",
        create_uptime_image(),
        "Uptime",
        menu=pystray.Menu(
            item('Exit', on_exit)
        )
    )
    threading.Thread(target=update_tooltip, args=(icon,), daemon=True).start()
    icon.run()

def create_uninstaller():
    """Create a simple uninstaller script"""
    uninstaller_script = f'''import os
import sys
import winreg
import shutil

def uninstall():
    install_dir = r"{INSTALL_DIR}"
    registry_key = r"{REGISTRY_KEY}"
    
    # Remove startup shortcuts for all users
    startup_folders = [
        os.path.expandvars(r"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"),
        os.path.expandvars(r"%ALLUSERSPROFILE%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    ]
    
    for startup_folder in startup_folders:
        shortcut_path = os.path.join(startup_folder, "UpTime.lnk")
        if os.path.exists(shortcut_path):
            try:
                os.remove(shortcut_path)
            except:
                pass
    
    # Remove installation directory
    if os.path.exists(install_dir):
        try:
            shutil.rmtree(install_dir)
        except:
            pass
    
    # Remove registry entry
    try:
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, registry_key)
    except:
        pass

if __name__ == "__main__":
    uninstall()
'''
    
    uninstaller_path = os.path.join(INSTALL_DIR, "uninstall.py")
    with open(uninstaller_path, 'w') as f:
        f.write(uninstaller_script)

def setup_registry():
    """Set up registry entries for Programs and Features"""
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_KEY)
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "UpTime")
        winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "1.0")
        winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "UpTime")
        winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, os.path.join(INSTALL_DIR, "uninstall.py"))
        winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, INSTALL_DIR)
        winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, os.path.join(INSTALL_DIR, "UpTime.exe"))
        winreg.SetValueEx(key, "EstimatedSize", 0, winreg.REG_DWORD, 15000)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Warning: Could not set up registry: {e}")

def setup_startup():
    """Set up startup for all users"""
    try:
        # All Users startup folder
        all_users_startup = os.path.expandvars(r"%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs\Startup")
        shortcut_path = os.path.join(all_users_startup, "UpTime.lnk")
        
        # Create shortcut using WScript.Shell
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = os.path.join(INSTALL_DIR, "UpTime.exe")
        shortcut.WorkingDirectory = INSTALL_DIR
        shortcut.WindowStyle = 7
        shortcut.save()
    except Exception as e:
        print(f"Warning: Could not set up startup: {e}")

def install():
    """Main installation function"""
    print("Installing UpTime...")
    
    # Check if already installed
    if os.path.exists(INSTALL_DIR):
        print("Error: UpTime is already installed!")
        print("Please uninstall the existing version first.")
        input("Press Enter to exit...")
        return False
    
    # Create installation directory
    try:
        os.makedirs(INSTALL_DIR, exist_ok=True)
    except Exception as e:
        print(f"Error: Could not create installation directory: {e}")
        print("Try running as Administrator.")
        input("Press Enter to exit...")
        return False
    
    # Copy the current executable to installation directory
    current_exe = sys.executable
    target_exe = os.path.join(INSTALL_DIR, "UpTime.exe")
    
    try:
        shutil.copy2(current_exe, target_exe)
    except Exception as e:
        print(f"Error: Could not copy executable: {e}")
        input("Press Enter to exit...")
        return False
    
    # Create uninstaller
    create_uninstaller()
    
    # Set up registry
    setup_registry()
    
    # Set up startup
    setup_startup()
    
    print("UpTime installed successfully!")
    print(f"Installation location: {INSTALL_DIR}")
    print("UpTime will start automatically for all users.")
    
    return True

def main():
    """Main function - determine if this is installer or runtime"""
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        # This is the installer mode
        if install():
            # Start the application after installation
            run_uptime_app()
    else:
        # This is the runtime mode (normal UpTime app)
        run_uptime_app()

if __name__ == "__main__":
    main() 