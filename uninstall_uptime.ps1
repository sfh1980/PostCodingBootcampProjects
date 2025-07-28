# UpTime Uninstaller Script
# This script removes UpTime from the computer

param(
    [string]$InstallPath = ""
)

# Default installation path
if ($InstallPath -eq "") {
    $InstallPath = "$env:PROGRAMFILES\UpTime"
}

Write-Host "UpTime Uninstaller" -ForegroundColor Red
Write-Host "==================" -ForegroundColor Red

# Check if UpTime is installed
if (-not (Test-Path $InstallPath)) {
    Write-Host "UpTime is not installed at $InstallPath" -ForegroundColor Yellow
    exit 0
}

# Remove startup shortcut
Write-Host "Removing startup shortcut..." -ForegroundColor Yellow
$StartupFolder = [Environment]::GetFolderPath("Startup")
$ShortcutPath = "$StartupFolder\UpTime.lnk"
if (Test-Path $ShortcutPath) {
    Remove-Item $ShortcutPath -Force
    Write-Host "Startup shortcut removed." -ForegroundColor Green
}

# Remove installation directory
Write-Host "Removing installation files..." -ForegroundColor Yellow
try {
    Remove-Item $InstallPath -Recurse -Force
    Write-Host "Installation files removed." -ForegroundColor Green
} catch {
    Write-Host "Error removing files. Try running as Administrator." -ForegroundColor Red
    exit 1
}

Write-Host "UpTime has been successfully uninstalled!" -ForegroundColor Green
Write-Host "The application will no longer start automatically." -ForegroundColor Green 