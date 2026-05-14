# SRE End-Term Project
## End-to-End SRE Implementation for a Distributed Microservices System
**Student:** Kaber Daryn | **Group:** SE-2430

---

## Architecture

```
User -> Nginx (8081)
         |
   Flask Frontend (5000)
         |
   +----------+----------+---------+--------------+------------+
   |          |          |         |              |            |
User API  Product API  Order API  Notification  Payment API
(5001)    (5002)       (5003)     API (5004)    (5005)
   |          |          |         |              |
  DB         DB         DB        DB             DB
 (PG)       (PG)       (PG)      (PG)           (PG)

Observability: Prometheus(9090) -> Grafana(3000)
               node-exporter(9100) + cAdvisor(8080)
```

---

## Services (6 Microservices)

| Service          | Port | Role                        |
|------------------|------|-----------------------------|
| Frontend         | 5000 | Flask web UI                |
| User API         | 5001 | Auth & user management      |
| Product API      | 5002 | Product catalog             |
| Order API        | 5003 | Order processing            |
| Notification API | 5004 | Email/alert simulation      |
| Payment API      | 5005 | Payment handling simulation |
| Nginx            | 8081 | Reverse proxy               |
| Prometheus       | 9090 | Metrics collection          |
| Grafana          | 3000 | Dashboards (admin/admin123) |

---

## Method 1 — Docker Compose

```bash
docker compose up -d --build
docker compose ps
```

Stop:
```bash
docker compose down -v
```

Seed product data:
```bash
docker exec cproduct-service python seed.py
```

---

## Method 2 — Docker Swarm

```bash
# Initialize Swarm
docker swarm init

# Build images
docker build -t sre-frontend:latest ./frontend
docker build -t sre-user-service:latest ./user-service
docker build -t sre-product-service:latest ./product-service
docker build -t sre-order-service:latest ./order-service
docker build -t sre-notification-service:latest ./notification-service
docker build -t sre-payment-service:latest ./payment-service

# Deploy stack
docker stack deploy -c docker-compose.swarm.yml sre-app
docker service ls

# Scale a service
docker service scale sre-app_order-api=3
```

---

## Method 3 — Kubernetes

```bash
# Start minikube
minikube start

# Load images
minikube image load sre-user-service:latest
minikube image load sre-product-service:latest
minikube image load sre-order-service:latest
minikube image load sre-notification-service:latest
minikube image load sre-payment-service:latest

# Apply manifests
kubectl apply -f kubernetes/

# Verify
kubectl get all -n sre-microservices

# Open Grafana
minikube service grafana -n sre-microservices
```

---

## Method 4 — Ansible

```bash
cd ansible/
# Edit inventory.ini with your VM IP
ansible-playbook -i inventory.ini playbook.yml
```

---

## Terraform (IaC)

```bash
cd terraform/
cp terraform.tfvars.example terraform.tfvars
# Fill in terraform.tfvars

terraform init
terraform plan
terraform apply
```

---

## Incident Simulation

```bash
# Crash Order Service
curl http://localhost:5003/crash

# Observe automatic recovery (Docker restart policy)
docker inspect corder-service | grep RestartCount

# Verify health after recovery
curl http://localhost:5003/health
```

Automated rollback tool:
```bash
python rollback.py --status
python rollback.py --auto
python rollback.py --service order-api
```

---

## SLI / SLO

| SLI          | SLO      | Window  |
|--------------|----------|---------|
| Availability | >= 99%   | 30 days |
| Latency p95  | <= 200ms | 30 days |
| Error rate   | <= 1%    | 30 days |
| Success rate | >= 99%   | 30 days |

---

## GitHub Repository

[https://github.com/KaberDaryn/SRE-endterm](https://github.com/KaberDaryn/SRE-endterm)
