# PowerShell script to set up UpTime in Windows Startup folder
# This method doesn't require Administrator privileges

param(
    [string]$ExePath = ""
)

# Get the current directory
$CurrentDir = Get-Location
$ExePath = if ($ExePath -eq "") { "$CurrentDir\dist\UpTime.exe" } else { $ExePath }

# Check if executable exists
if (-not (Test-Path $ExePath)) {
    Write-Host "Error: UpTime.exe not found at $ExePath" -ForegroundColor Red
    Write-Host "Please build the executable first by running: python build_exe.py" -ForegroundColor Yellow
    exit 1
}

# Get the startup folder path
$StartupFolder = [Environment]::GetFolderPath("Startup")

# Create shortcut in startup folder
$ShortcutPath = "$StartupFolder\UpTime.lnk"
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $ExePath
$Shortcut.WorkingDirectory = Split-Path $ExePath
$Shortcut.WindowStyle = 7  # Minimized window style
$Shortcut.Description = "UpTime System Tray Application"
$Shortcut.Save()

Write-Host "Successfully created UpTime startup shortcut!" -ForegroundColor Green
Write-Host "Shortcut location: $ShortcutPath" -ForegroundColor Green
Write-Host "The application will now start automatically when you log in." -ForegroundColor Green
Write-Host "To test it now, you can double-click the shortcut or run: $ExePath" -ForegroundColor Yellow 