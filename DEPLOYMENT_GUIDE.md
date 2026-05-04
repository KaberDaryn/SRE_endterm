# Deployment Guide - Assignment 6

## Prerequisites

- Docker Desktop
- PowerShell
- Internet access for pulling Docker images
- Project directory: python-flask-microservices

## Start the stack

docker compose up -d --build

## Verify containers

docker compose ps

Expected:
- application services healthy
- PostgreSQL databases healthy
- Prometheus running
- Grafana running
- Nginx running
- cAdvisor and node-exporter running

## Validate system

.\validate_config.ps1

Expected:
VALIDATION PASSED: configuration and endpoints are ready.

## Inspect logs

.\check_logs_clean.ps1

Expected:
LOG INSPECTION PASSED: no critical runtime errors found in application or monitoring services.

## Main URLs

Frontend through Nginx:
http://localhost:8081

Prometheus:
http://localhost:9090

Grafana:
http://localhost:3000

cAdvisor:
http://localhost:8080

Product API:
http://localhost:5002/api/products

## PostgreSQL verification

docker exec -i cproduct_dbase psql -U cloudacademy -d product -c "SELECT version();"
docker exec -i cproduct_dbase psql -U cloudacademy -d product -c "SELECT id, name, slug, price, image FROM product;"

## Capacity test

docker cp capacity_matrix.py cfrontend-app:/tmp/capacity_matrix.py
docker exec cfrontend-app python /tmp/capacity_matrix.py

## Alert rules validation

docker run --rm --entrypoint promtool -v ${PWD}\monitoring\prometheus:/etc/prometheus prom/prometheus:latest check rules /etc/prometheus/alert_rules.yml

## Self-healing demo

.\self_healing_postgres_demo.ps1
