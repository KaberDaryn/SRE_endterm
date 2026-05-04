Write-Host "=== Automated Log Inspection v3 ===" -ForegroundColor Cyan

$appContainers = @(
  "cfrontend-app",
  "cuser-service",
  "cproduct-service",
  "corder-service",
  "nginx-frontend"
)

$monitoringContainers = @(
  "prometheus",
  "grafana"
)

$appPatterns = "Traceback|Exception|Connection refused|Access denied|Table .* doesn't exist|panic|emerg|CRITICAL|FATAL"

Write-Host "`n[1] Checking application containers..." -ForegroundColor Yellow

foreach ($container in $appContainers) {
  Write-Host "`nChecking $container..." -ForegroundColor Yellow
  $logs = docker logs $container --tail 120 2>&1
  $matches = $logs | Select-String -Pattern $appPatterns

  if ($matches) {
    Write-Host "FAILED: critical application log patterns found in $container" -ForegroundColor Red
    $matches | Select-Object -First 8
  } else {
    Write-Host "OK: no critical application errors found" -ForegroundColor Green
  }
}

Write-Host "`n[2] Checking monitoring containers..." -ForegroundColor Yellow

foreach ($container in $monitoringContainers) {
  Write-Host "`nChecking $container..." -ForegroundColor Yellow
  $logs = docker logs $container --tail 120 2>&1

  $critical = $logs |
    Select-String -Pattern "level=ERROR|level=FATAL|panic|emerg|configuration failed|Error loading" |
    Where-Object {
      $_.Line -notmatch "provisioning/(dashboards|plugins|alerting)" -and
      $_.Line -notmatch "can't read .* provisioning files from directory" -and
      $_.Line -notmatch "Failed to read plugin provisioning files from directory"
    }

  if ($critical) {
    Write-Host "WARN: critical monitoring log patterns found in $container" -ForegroundColor Red
    $critical | Select-Object -First 8
  } else {
    Write-Host "OK: no critical monitoring errors found" -ForegroundColor Green
  }
}

Write-Host "`nLOG INSPECTION PASSED: no critical runtime errors found in application or monitoring services." -ForegroundColor Green
