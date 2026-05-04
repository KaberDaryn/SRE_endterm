# Assignment 6 - SRE Automation and Capacity Planning

Student: Kaber Daryn

## Overview

This project demonstrates SRE automation, monitoring, alerting, capacity planning, and recovery for a containerized Python Flask microservices system.

## Technology Stack

- Docker Compose
- Nginx reverse proxy
- Python Flask frontend
- User Service
- Product Service
- Order Service
- PostgreSQL 15
- Prometheus
- Grafana
- cAdvisor
- node-exporter
- Terraform configuration

## Architecture

Validated request path:

User / Browser -> Nginx Reverse Proxy -> Flask Frontend -> Product Service -> PostgreSQL Product Database

Supporting services:

- User Service uses PostgreSQL User Database.
- Product Service uses PostgreSQL Product Database.
- Order Service uses PostgreSQL Orders Database.
- Prometheus scrapes application, host, and container metrics.
- Grafana visualizes Prometheus metrics.
- cAdvisor provides container-level metrics.
- node-exporter provides host-level metrics.

## Run

docker compose up -d --build

## Validate

.\validate_config.ps1

Expected result:

VALIDATION PASSED: configuration and endpoints are ready.

## Log inspection

.\check_logs_clean.ps1

Expected result:

LOG INSPECTION PASSED: no critical runtime errors found in application or monitoring services.

## PostgreSQL verification

Check PostgreSQL version:

docker exec -i cproduct_dbase psql -U cloudacademy -d product -c "SELECT version();"

Check product records:

docker exec -i cproduct_dbase psql -U cloudacademy -d product -c "SELECT id, name, slug, price, image FROM product;"

## Main endpoints

- Frontend through Nginx: http://localhost:8081
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- cAdvisor: http://localhost:8080
- Product API: http://localhost:5002/api/products

## Capacity test

docker cp capacity_matrix.py cfrontend-app:/tmp/capacity_matrix.py
docker exec cfrontend-app python /tmp/capacity_matrix.py

The PostgreSQL-backed stress test sustained 1,000/1,000 successful requests at concurrency 100 with 0.00% error rate.

## Alert rule validation

docker run --rm --entrypoint promtool -v ${PWD}\monitoring\prometheus:/etc/prometheus prom/prometheus:latest check rules /etc/prometheus/alert_rules.yml

Expected result:

SUCCESS: 11 rules found

## Self-healing validation

Order Service recovery was validated through a controlled failure-injection endpoint. Docker restart policy recovered the service, RestartCount increased from 0 to 1, and /health returned HTTP 200 after recovery.

## Final Report

Final Assignment 6 report:

- `docs/SRE_6_Kaber_Daryn.pdf`

Supporting evidence screenshots:

- `evidence/screenshots/`
