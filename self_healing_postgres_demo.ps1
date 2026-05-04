$ErrorActionPreference = "Continue"

Write-Host "=== PostgreSQL Self-Healing Demo: Order Service ===" -ForegroundColor Cyan

Write-Host "`n[1] Adding controlled crash endpoint if missing." -ForegroundColor Yellow

$routesFile = "order-service\application\order_api\routes.py"

if (-not (Select-String -Path $routesFile -Pattern "def order_crash" -Quiet)) {
@"

# SRE controlled failure-injection endpoint for Assignment 6 self-healing demo.
# This is not a production business endpoint.
import os

@order_api_blueprint.route('/crash', methods=['GET'])
def order_crash():
    os._exit(1)
"@ | Add-Content $routesFile

  Write-Host "OK: crash endpoint added" -ForegroundColor Green
} else {
  Write-Host "OK: crash endpoint already exists" -ForegroundColor Green
}

Write-Host "`n[2] Rebuilding and force-recreating Order Service." -ForegroundColor Yellow
docker compose up -d --build --force-recreate order-api

Write-Host "`nWaiting for service health." -ForegroundColor Yellow
Start-Sleep -Seconds 30

docker compose ps order-api

Write-Host "`n[3] State before controlled crash." -ForegroundColor Yellow
docker inspect -f 'Before={{.State.Status}} RestartPolicy={{.HostConfig.RestartPolicy.Name}} RestartCount={{.RestartCount}}' corder-service

Write-Host "`n[4] Triggering controlled application crash through /crash." -ForegroundColor Yellow
curl.exe http://localhost:5003/crash

Write-Host "`nWaiting for Docker restart policy to recover the service." -ForegroundColor Yellow
Start-Sleep -Seconds 40

Write-Host "`n[5] State after recovery." -ForegroundColor Yellow
docker compose ps order-api
docker inspect -f 'After={{.State.Status}} RestartPolicy={{.HostConfig.RestartPolicy.Name}} RestartCount={{.RestartCount}}' corder-service

Write-Host "`n[6] Health verification after recovery." -ForegroundColor Yellow
curl.exe -i http://localhost:5003/health

Write-Host "`nPOSTGRESQL SELF-HEALING DEMO COMPLETED" -ForegroundColor Green
