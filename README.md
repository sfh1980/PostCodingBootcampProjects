# UpTime - System Tray Uptime Monitor

## Purpose

UpTime is a lightweight Windows system tray application that displays your computer's uptime (how long the system has been running since the last boot) in the system tray area next to the clock. It provides a quick, always-visible way to monitor system uptime without opening Task Manager or using command line tools.

### Key Features
- **Real-time uptime display** - Shows hours, minutes, and seconds since last boot
- **System tray integration** - Appears next to the clock in the Windows system tray
- **Automatic startup** - Can be configured to start automatically when Windows boots
- **Silent operation** - Runs in the background with no visible windows
- **Cross-user support** - Works for all users on the computer
- **Easy deployment** - Single executable installer for easy distribution

### Use Cases
- **System administrators** monitoring server uptime
- **IT professionals** tracking system stability
- **Power users** who want to monitor their system's uptime
- **Troubleshooting** - quickly checking if a system has been rebooted recently
- **System maintenance** - tracking time between maintenance windows

## File Structure and Purpose

### Core Application Files

#### `main.py`
**Purpose**: The original, standalone UpTime application
- Contains the core system tray functionality
- Creates the "Up" icon with large, visible text
- Implements uptime calculation using `psutil`
- Handles system tray menu and tooltip updates
- **Use case**: Direct execution or building standalone executable

#### `simple_self_installer.py`
**Purpose**: Self-installing version that combines installation logic with the UpTime application
- Contains all functionality from `main.py` plus installation capabilities
- Handles Windows registry setup for Programs and Features
- Creates startup shortcuts for all users
- Generates uninstaller script
- **Use case**: Creating the final distribution executable

### Build and Distribution Files

#### `build_self_installer.py`
**Purpose**: PyInstaller build script for creating the self-installing executable
- Configures PyInstaller with correct parameters
- Includes necessary hidden imports for Windows COM automation
- Creates single-file executable with no console window
- **Use case**: Building the final `UpTime_Installer.exe`

#### `requirements.txt`
**Purpose**: Python dependency list for development and building
- `pillow` - Image creation for system tray icon
- `psutil` - System information (boot time, uptime calculation)
- `pystray` - System tray integration
- `pyinstaller` - Executable creation
- `pywin32` - Windows COM automation for shortcuts
- **Use case**: Setting up development environment

### Installation and Setup Files

#### `setup_startup_folder.ps1`
**Purpose**: PowerShell script for manual startup configuration
- Creates shortcut in user's Windows Startup folder
- No administrator privileges required
- Simple, user-specific installation
- **Use case**: Manual installation or testing

#### `install_uptime.ps1`
**Purpose**: Automated installer script with user prompts
- Installs to Program Files directory
- Creates startup shortcut
- Provides user feedback and options
- **Use case**: Semi-automated installation

#### `uninstall_uptime.ps1`
**Purpose**: Clean removal of UpTime installation
- Removes startup shortcuts
- Deletes installation files
- Cleans up registry entries
- **Use case**: Uninstalling manual installations

### Documentation

#### `README.md`
**Purpose**: This file - comprehensive documentation
- Installation instructions
- Troubleshooting guide
- File explanations
- Development notes

## Installation Methods

### Method 1: Self-Installing Executable (Recommended for Distribution)

**Best for**: Distributing to multiple computers or users

1. **Build the installer:**
   ```powershell
   python build_self_installer.py
   ```

2. **Distribute and install:**
   - Copy `dist/UpTime_Installer.exe` to target computer
   - Right-click → "Run as Administrator"
   - Installation completes automatically

**What happens:**
- Installs to `C:\Program Files\UpTime\`
- Sets up startup for all users
- Creates uninstaller
- Adds to Programs and Features
- Starts UpTime immediately

### Method 2: Manual Installation (Development/Testing)

**Best for**: Development, testing, or single-user installation

1. **Build executable:**
   ```powershell
   pyinstaller --onefile --windowed --name=UpTime main.py
   ```

2. **Set up startup:**
   ```powershell
   .\setup_startup_folder.ps1
   ```

### Method 3: Automated Script Installation

**Best for**: IT administrators or automated deployment

```powershell
.\install_uptime.ps1
```

## Troubleshooting Guide

### Application Won't Start

**Symptoms**: No system tray icon appears, application exits immediately

**Possible Causes and Solutions:**

1. **Missing Dependencies**
   - **Check**: Look for error messages in console
   - **Solution**: Install requirements: `pip install -r requirements.txt`

2. **Antivirus Blocking**
   - **Check**: Check antivirus quarantine or logs
   - **Solution**: Add exception for UpTime executable
   - **Prevention**: Sign the executable with a code signing certificate

3. **Python Runtime Issues**
   - **Check**: Try running `python main.py` directly
   - **Solution**: Ensure Python 3.7+ is installed and in PATH

4. **System Tray Not Visible**
   - **Check**: Look in hidden icons section of system tray
   - **Solution**: Click "Show hidden icons" and drag UpTime to visible area

### Icon Not Visible or Too Small

**Symptoms**: Can't see the "Up" text in system tray

**Solutions:**
1. **Check system tray settings** - ensure icons are not hidden
2. **Look in hidden icons section** - click the arrow in system tray
3. **Adjust Windows display scaling** - try 100% scaling
4. **Rebuild with larger font** - modify `font_size` in `create_uptime_image()`

### Uptime Display Issues

**Symptoms**: Wrong uptime shown, tooltip not updating

**Solutions:**
1. **Check system time** - ensure system clock is correct
2. **Restart application** - close and reopen UpTime
3. **Check for multiple instances** - ensure only one UpTime is running

### Installation Problems

**Symptoms**: Installer fails, startup not working

**Solutions:**

1. **Administrator Privileges**
   - **Error**: "Access denied" or "Permission denied"
   - **Solution**: Right-click installer → "Run as Administrator"

2. **Already Installed**
   - **Error**: "UpTime is already installed"
   - **Solution**: Uninstall existing version first

3. **Startup Not Working**
   - **Check**: Look in `%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs\Startup`
   - **Solution**: Manually run `setup_startup_folder.ps1`

4. **Registry Issues**
   - **Error**: "Could not set up registry"
   - **Solution**: Run as Administrator, check Windows permissions

### Performance Issues

**Symptoms**: High CPU usage, system slowdown

**Solutions:**
1. **Check for multiple instances** - use Task Manager to find duplicates
2. **Reduce update frequency** - modify `time.sleep(1)` in `update_tooltip()`
3. **Monitor system resources** - check if other applications are causing issues

### Uninstallation Problems

**Symptoms**: Can't uninstall, leftover files

**Solutions:**
1. **Use Programs and Features** - Control Panel → Programs and Features
2. **Manual cleanup** - delete `C:\Program Files\UpTime\`
3. **Remove startup shortcuts** - delete from Startup folders
4. **Registry cleanup** - remove `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\UpTime`

## Development and Customization

### Adding Features

**Common modifications:**

1. **Change icon appearance:**
   - Modify `create_uptime_image()` function
   - Adjust `font_size`, `icon_size`, or text content

2. **Add more system information:**
   - Import additional `psutil` modules
   - Modify `get_uptime()` to include CPU, memory, etc.

3. **Change update frequency:**
   - Modify `time.sleep(1)` in `update_tooltip()`

4. **Add system tray menu items:**
   - Modify the `pystray.Menu()` in `run_uptime_app()`

### Building Custom Versions

1. **Standalone version:**
   ```powershell
   pyinstaller --onefile --windowed --name=UpTime main.py
   ```

2. **Self-installing version:**
   ```powershell
   python build_self_installer.py
   ```

3. **Debug version (with console):**
   ```powershell
   pyinstaller --onefile --name=UpTime main.py
   ```

### Testing

**Recommended testing workflow:**

1. **Development testing:**
   ```powershell
   python main.py
   ```

2. **Standalone executable testing:**
   ```powershell
   .\dist\UpTime.exe
   ```

3. **Installation testing:**
   - Test on clean Windows installation
   - Test with different user accounts
   - Test uninstallation process

## System Requirements

- **Operating System**: Windows 10/11 (Windows 7+ may work)
- **Python**: 3.7 or higher (for development)
- **Memory**: Minimal (typically <10MB RAM)
- **Disk Space**: <50MB for installation
- **Permissions**: Administrator for installation, user for runtime

## Security Considerations

- **Code signing**: Consider signing the executable for enterprise deployment
- **Antivirus**: May trigger false positives due to system tray integration
- **Permissions**: Requires system access for uptime calculation
- **Registry access**: Creates entries for proper Windows integration

## Support and Maintenance

### Logging
- Application currently has no logging
- Consider adding logging for troubleshooting
- Use Windows Event Log for enterprise environments

### Updates
- Manual update process (replace executable)
- Consider adding auto-update functionality
- Version checking in registry

### Distribution
- Single executable for easy distribution
- MSI package for enterprise deployment
- Chocolatey/Scoop packages for developers 