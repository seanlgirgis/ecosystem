# Ecosystem Environment Setup
# Run this before working on the project: . .\env_setter.ps1

param(
    [switch]$Install,
    [switch]$Update,
    [switch]$Reset
)

$ErrorActionPreference = "Stop"

# Configuration
$ProjectName = "ecosystem"
$VenvPath = "C:\py_venv\$ProjectName"
$FallbackVenv = "C:\py_venv\clawbot"  # Already has dependencies
$ProjectPath = "C:\ecosystem"
$PythonVersion = "3.12"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Ecosystem Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if ecosystem venv exists, fallback to clawbot if not
if (-not (Test-Path "$VenvPath\Scripts\python.exe")) {
    if (Test-Path "$FallbackVenv\Scripts\python.exe") {
        Write-Host "Note: Using fallback venv at $FallbackVenv" -ForegroundColor Yellow
        Write-Host "      Run with -Install to create $ProjectName venv" -ForegroundColor Yellow
        Write-Host ""
        $VenvPath = $FallbackVenv
    }
}

# Function to find Python
function Find-Python {
    $pythonPaths = @(
        "C:\Python312\python.exe"
        "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python312\python.exe"
        "C:\Program Files\Python312\python.exe"
    )
    
    foreach ($path in $pythonPaths) {
        if (Test-Path $path) {
            return $path
        }
    }
    
    # Fallback to PATH
    $pythonInPath = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pythonInPath) {
        return $pythonInPath.Source
    }
    
    return $null
}

# Handle Reset
if ($Reset) {
    Write-Host "Resetting virtual environment..." -ForegroundColor Yellow
    if (Test-Path $VenvPath) {
        Remove-Item -Path $VenvPath -Recurse -Force
        Write-Host "  Removed existing venv at $VenvPath" -ForegroundColor Green
    }
    $Install = $true
}

# Create venv if doesn't exist (and Install requested)
if ($Install -and -not (Test-Path $VenvPath)) {
    Write-Host "Creating virtual environment at $VenvPath..." -ForegroundColor Yellow
    
    $pythonExe = Find-Python
    if (-not $pythonExe) {
        Write-Error "Python $PythonVersion not found. Please install Python $PythonVersion"
        return
    }
    
    Write-Host "Using Python: $pythonExe"
    & $pythonExe -m venv $VenvPath
    Write-Host "  Created virtual environment" -ForegroundColor Green
}

# Check venv exists
if (-not (Test-Path $VenvPath)) {
    Write-Error "Virtual environment not found at $VenvPath"
    Write-Host "Run with -Install flag to create it: . .\env_setter.ps1 -Install"
    return
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$activateScript = Join-Path $VenvPath "Scripts\Activate.ps1"

if (-not (Test-Path $activateScript)) {
    Write-Error "Activate script not found at $activateScript. Venv may be corrupted."
    Write-Host "Run with -Reset flag to recreate: . .\env_setter.ps1 -Reset"
    return
}

# Dot-source the activate script
& $activateScript

# Verify activation
if ($env:VIRTUAL_ENV -ne $VenvPath) {
    Write-Error "Failed to activate virtual environment"
    return
}

Write-Host "  Activated: $env:VIRTUAL_ENV" -ForegroundColor Green

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install/Update requirements
$requirementsFile = Join-Path $ProjectPath "requirements.txt"

if (($Install -or $Update) -and (Test-Path $requirementsFile)) {
    Write-Host "Installing requirements from requirements.txt..." -ForegroundColor Yellow
    pip install -r $requirementsFile
    Write-Host "  Requirements installed" -ForegroundColor Green
} else {
    Write-Host "Use -Install or -Update to refresh requirements" -ForegroundColor Gray
}

# Environment info
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Environment Ready!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Python:    $(python --version)"
Write-Host "Venv:      $env:VIRTUAL_ENV"
Write-Host "Project:   $ProjectPath"
Write-Host ""
Write-Host "Available commands:"
Write-Host "  python C:\ecosystem\test_secondbrain.py  - Run tests"
Write-Host "  pip list                                  - Show packages"
Write-Host "  .\scripts\install.ps1                     - Full installation"
Write-Host "  .\scripts\start_all.ps1                  - Start services"
Write-Host ""

# Set project root as working directory if not already
if ((Get-Location).Path -ne $ProjectPath) {
    Set-Location $ProjectPath
    Write-Host "Changed directory to: $ProjectPath"
}

# Show usage hint
Write-Host "Usage flags:" -ForegroundColor DarkGray
Write-Host "  -Install  : Create venv and install requirements" -ForegroundColor DarkGray
Write-Host "  -Update   : Update packages from requirements.txt" -ForegroundColor DarkGray
Write-Host "  -Reset    : Recreate venv from scratch" -ForegroundColor DarkGray
