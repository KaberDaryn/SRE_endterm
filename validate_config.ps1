$ErrorActionPreference = "Continue"

Write-Host "=== Assignment 6 Pre-Deployment Validation ===" -ForegroundColor Cyan

$requiredFiles = @(
  "docker-compose.yml",
  "monitoring\prometheus\prometheus.yml",
  "monitoring\prometheus\alert_rules.yml",
  "nginx\default.conf",
  "frontend\.env",
  "user-service\.env",
  "product-service\.env",
  "order-service\.env"
)

$failed = 0

Write-Host "`n[1] Checking required files..." -ForegroundColor Yellow
foreach ($file in $requiredFiles) {
  if (Test-Path $file) {
    Write-Host "OK: $file" -ForegroundColor Green
  } else {
    Write-Host "MISSING: $file" -ForegroundColor Red
    $failed++
  }
}

Write-Host "`n[2] Checking running endpoints..." -ForegroundColor Yellow
$endpoints = @(
  "http://localhost:8081",
  "http://localhost:5000/health",
  "http://localhost:5001/health",
  "http://localhost:5002/health",
  "http://localhost:5003/health",
  "http://localhost:5002/api/products",
  "http://localhost:9090/-/ready"
)

foreach ($url in $endpoints) {
  try {
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 400) {
      Write-Host "OK: $url -> $($response.StatusCode)" -ForegroundColor Green
    } else {
      Write-Host "BAD: $url -> $($response.StatusCode)" -ForegroundColor Red
      $failed++
    }
  } catch {
    Write-Host "FAILED: $url -> $($_.Exception.Message)" -ForegroundColor Red
    $failed++
  }
}

Write-Host "`n[3] Checking Docker service status..." -ForegroundColor Yellow
docker compose ps

if ($failed -eq 0) {
  Write-Host "`nVALIDATION PASSED: configuration and endpoints are ready." -ForegroundColor Green
  exit 0
} else {
  Write-Host "`nVALIDATION FAILED: $failed issue(s) found." -ForegroundColor Red
  exit 1
}
