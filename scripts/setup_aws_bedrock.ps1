# AWS Bedrock Setup Script
# Configures AWS profile "study" for Bedrock API access

param(
    [switch]$Verify,
    [switch]$Test
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AWS Bedrock Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$AWSProfile = "study"
$Region = "us-east-1"  # Bedrock available here

# Check AWS CLI
Write-Host "[1] Checking AWS CLI..." -ForegroundColor Yellow
$awsVersion = aws --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "AWS CLI not installed. Install from: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html"
    return
}
Write-Host "  AWS CLI: $awsVersion" -ForegroundColor Green

# Check profile exists
Write-Host "`n[2] Checking AWS profile '$AWSProfile'..." -ForegroundColor Yellow
$profiles = aws configure list-profiles 2>&1
if ($profiles -notcontains $AWSProfile) {
    Write-Error "Profile '$AWSProfile' not found!"
    Write-Host "Available profiles: $profiles"
    Write-Host "`nTo create profile 'study', run:"
    Write-Host "  aws configure --profile study"
    Write-Host "  # Enter your AWS Access Key ID, Secret Key, region: us-east-1"
    return
}
Write-Host "  Profile '$AWSProfile' found" -ForegroundColor Green

# Verify Bedrock access
Write-Host "`n[3] Verifying Bedrock access..." -ForegroundColor Yellow
try {
    $models = aws bedrock list-foundation-models --profile $AWSProfile --region $Region --output json 2>&1 | ConvertFrom-Json
    $modelCount = $models.modelSummaries.Count
    Write-Host "  Success! Found $modelCount models" -ForegroundColor Green
    
    # Show available models
    Write-Host "`n  Available models:" -ForegroundColor DarkGray
    $models.modelSummaries | Where-Object { $_.modelId -like "*kimi*" -or $_.modelId -like "*claude*" -or $_.modelId -like "*llama*" } | 
        Select-Object -First 10 | 
        ForEach-Object { Write-Host "    - $($_.modelId)" -ForegroundColor DarkGray }
} catch {
    Write-Error "Failed to access Bedrock: $_"
    Write-Host "`nCommon issues:"
    Write-Host "  - Profile credentials expired"
    Write-Host "  - Bedrock not enabled in AWS console"
    Write-Host "  - Wrong region (try us-east-1 or us-west-2)"
    return
}

# Create config for ecosystem
Write-Host "`n[4] Creating ecosystem config..." -ForegroundColor Yellow
$envContent = @"
# AWS Bedrock Configuration
AWS_PROFILE=$AWSProfile
AWS_REGION=$Region
AWS_BEDROCK_ENABLED=true

# Primary model (Kimi K2.5 on Bedrock)
DEFAULT_MODEL=amazon-bedrock/moonshot.kimi-k2-thinking
FALLBACK_MODEL=amazon-bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0

# Cost tracking
ENABLE_COST_TRACKING=true
COST_ALERT_THRESHOLD=10.00
"@

$envPath = "C:\ecosystem\.env"
if (Test-Path $envPath) {
    Write-Host "  .env exists - appending AWS config" -ForegroundColor Yellow
    Add-Content -Path $envPath -Value "`n`n# Added by setup_aws_bedrock.ps1`n$envContent"
} else {
    Set-Content -Path $envPath -Value $envContent
}
Write-Host "  Config saved to $envPath" -ForegroundColor Green

# Test inference
if ($Test) {
    Write-Host "`n[5] Testing Bedrock inference..." -ForegroundColor Yellow
    
    $testPayload = @{
        modelId = "amazon-bedrock/moonshot.kimi-k2-thinking"
        messages = @(
            @{ role = "user"; content = "Say 'AWS Bedrock is working' and nothing else." }
        )
    } | ConvertTo-Json -Depth 3
    
    try {
        # Note: Actual invoke requires proper JSON formatting for Bedrock
        Write-Host "  Test payload prepared (manual test needed)" -ForegroundColor Yellow
        Write-Host "  Run: aws bedrock-runtime invoke-model ..." -ForegroundColor DarkGray
    } catch {
        Write-Warning "Test failed: $_"
    }
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  AWS Bedrock Ready!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Profile:     $AWSProfile"
Write-Host "Region:      $Region"
Write-Host "Credits:     ~`$199 available"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Test with: .\scripts\test_bedrock.ps1"
Write-Host "  2. Check costs: aws ce get-cost-and-usage --profile $AWSProfile"
Write-Host ""
