# UpTime Installer Script
# This script installs UpTime on a new computer

param(
    [string]$InstallPath = ""
)

# Default installation path
if ($InstallPath -eq "") {
    $InstallPath = "$env:PROGRAMFILES\UpTime"
}

Write-Host "UpTime Installer" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green

# Check if UpTime.exe exists in current directory
$ExePath = ".\dist\UpTime.exe"
if (-not (Test-Path $ExePath)) {
    Write-Host "Error: UpTime.exe not found at $ExePath" -ForegroundColor Red
    Write-Host "Please build the executable first using: pyinstaller --onefile --windowed --name=UpTime main.py" -ForegroundColor Yellow
    exit 1
}

# Create installation directory
Write-Host "Creating installation directory: $InstallPath" -ForegroundColor Yellow
try {
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
} catch {
    Write-Host "Error creating directory. Try running as Administrator." -ForegroundColor Red
    exit 1
}

# Copy executable to installation directory
$TargetExe = "$InstallPath\UpTime.exe"
Write-Host "Copying UpTime.exe to installation directory..." -ForegroundColor Yellow
Copy-Item $ExePath $TargetExe -Force

# Set up startup
Write-Host "Setting up automatic startup..." -ForegroundColor Yellow
$StartupFolder = [Environment]::GetFolderPath("Startup")
$ShortcutPath = "$StartupFolder\UpTime.lnk"

# Create shortcut in startup folder
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetExe
$Shortcut.WorkingDirectory = $InstallPath
$Shortcut.WindowStyle = 7  # Minimized window style
$Shortcut.Description = "UpTime System Tray Application"
$Shortcut.Save()

Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host "UpTime will start automatically when you log in." -ForegroundColor Green
Write-Host "Installation location: $InstallPath" -ForegroundColor Green
Write-Host "To test now, run: $TargetExe" -ForegroundColor Yellow

# Ask if user wants to start the application now
$StartNow = Read-Host "Would you like to start UpTime now? (y/n)"
if ($StartNow -eq "y" -or $StartNow -eq "Y") {
    Write-Host "Starting UpTime..." -ForegroundColor Yellow
    Start-Process $TargetExe
} 