# Fix Python Permission Issues Script
# This script must be run as Administrator

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Fixing Python permission issues..." -ForegroundColor Green

# Get current username
$username = $env:USERNAME
Write-Host "Current user: $username" -ForegroundColor Cyan

# Python installation path
$pythonPath = "C:\Python312"

# Check if Python directory exists
if (-not (Test-Path $pythonPath)) {
    Write-Host "Python directory not found at $pythonPath" -ForegroundColor Red
    exit 1
}

Write-Host "Python directory found: $pythonPath" -ForegroundColor Green

try {
    # Grant full control to the current user for Python installation
    Write-Host "Granting full control permissions to $username..." -ForegroundColor Yellow
    icacls "$pythonPath" /grant "${username}:(OI)(CI)(F)" /T

    # Specifically grant permissions to Scripts directory
    Write-Host "Granting permissions to Scripts directory..." -ForegroundColor Yellow
    icacls "$pythonPath\Scripts" /grant "${username}:(OI)(CI)(F)" /T

    # Grant permissions to Lib\site-packages
    Write-Host "Granting permissions to site-packages directory..." -ForegroundColor Yellow
    icacls "$pythonPath\Lib\site-packages" /grant "${username}:(OI)(CI)(F)" /T

    Write-Host "Permissions updated successfully!" -ForegroundColor Green

    # Test pip installation
    Write-Host "Testing pip installation..." -ForegroundColor Yellow
    
    # Try installing a simple package to test
    $testResult = & python -m pip install wheel 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Pip is now working correctly!" -ForegroundColor Green
        Write-Host "You can now install packages without the --user flag." -ForegroundColor Green
    } else {
        Write-Host "WARNING: There may still be some issues. Error output:" -ForegroundColor Yellow
        Write-Host $testResult -ForegroundColor Red
    }

} catch {
    Write-Host "ERROR: Failed to update permissions" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Write-Host "`nPermission fix completed!" -ForegroundColor Green
Write-Host "You can now use 'python -m pip install <package>' without --user flag." -ForegroundColor Cyan
pause
