# Start All Ecosystem Services
# Launches Qdrant, Ollama, and ClawBot

param(
    [switch]$Detach,
    [switch]$SkipDocker,
    [switch]$SkipBot
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Ecosystem Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = "C:\ecosystem"

# 1. Start Docker services (Qdrant + Ollama)
if (-not $SkipDocker) {
    Write-Host "[1/3] Starting Docker services..." -ForegroundColor Yellow
    docker-compose -f "$ProjectRoot\docker-compose.yml" up -d
    
    Write-Host "      Waiting for services to be ready..."
    Start-Sleep -Seconds 5
    
    # Health check
    try {
        $qdrantHealth = Invoke-RestMethod -Uri "http://localhost:6333/healthz" -Method GET
        Write-Host "      Qdrant: Running" -ForegroundColor Green
    } catch {
        Write-Warning "Qdrant health check failed. Check logs: docker-compose logs qdrant"
    }
    
    try {
        $ollamaHealth = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method GET
        Write-Host "      Ollama: Running" -ForegroundColor Green
    } catch {
        Write-Warning "Ollama health check failed. Check logs: docker-compose logs ollama"
    }
} else {
    Write-Host "[1/3] Skipping Docker (as requested)" -ForegroundColor Gray
}

Write-Host ""

# 2. Activate virtual environment
Write-Host "[2/3] Activating virtual environment..." -ForegroundColor Yellow
$VenvPath = "C:\py_venv\ecosystem"
if (Test-Path "$VenvPath\Scripts\Activate.ps1") {
    & "$VenvPath\Scripts\Activate.ps1"
    Write-Host "      Virtual environment activated" -ForegroundColor Green
} else {
    Write-Warning "Virtual environment not found at $VenvPath"
    Write-Host "        Run: .\scripts\install.ps1"
}

Write-Host ""

# 3. Start ClawBot (if not skipped)
if (-not $SkipBot) {
    Write-Host "[3/3] Starting ClawBot..." -ForegroundColor Yellow
    # TODO: Implement actual bot startup
    Write-Host "      ClawBot start not yet implemented (Stage 7)" -ForegroundColor Yellow
} else {
    Write-Host "[3/3] Skipping ClawBot (as requested)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Services Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Dashboards:"
Write-Host "  Qdrant: http://localhost:6333/dashboard"
Write-Host ""
Write-Host "Commands:"
Write-Host "  docker-compose logs -f    # View all logs"
Write-Host "  docker-compose down       # Stop all services"
Write-Host ""
