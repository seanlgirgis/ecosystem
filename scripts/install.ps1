# Ecosystem Installation Script
# Sets up virtual environment and installs dependencies

param(
    [string]$VenvPath = "C:\py_venv\ecosystem",
    [string]$PythonVersion = "3.12"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Ecosystem Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "Python not found. Please install Python $PythonVersion"
    exit 1
}

Write-Host "Python found: $(python --version)"

# Create virtual environment
if (Test-Path $VenvPath) {
    Write-Host "Virtual environment already exists at $VenvPath"
} else {
    Write-Host "Creating virtual environment at $VenvPath..."
    python -m venv $VenvPath
}

# Activate and install dependencies
Write-Host "Installing dependencies..."
& "$VenvPath\Scripts\Activate.ps1"

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements (create requirements.txt first)
$requirementsContent = @"
# Core dependencies
qdrant-client>=1.7.0
ollama>=0.1.0
python-dotenv>=1.0.0
pydantic>=2.0.0

# Telegram
python-telegram-bot>=20.0

# Utilities
requests>=2.31.0
numpy>=1.24.0
"@

Set-Content -Path "$PSScriptRoot\..\requirements.txt" -Value $requirementsContent
pip install -r "$PSScriptRoot\..\requirements.txt"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Copy .env.example to .env and fill in your API keys"
Write-Host "  2. Start Qdrant: docker-compose up -d qdrant"
Write-Host "  3. Start Ollama: docker-compose up -d ollama"
Write-Host "  4. Run: .\scripts\start_all.ps1"
Write-Host ""
