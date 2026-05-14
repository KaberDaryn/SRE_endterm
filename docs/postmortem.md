# Postmortem: Order Service Failure
**Date:** May 14, 2026
**Author:** Kaber Daryn | SE-2430
**Severity:** SEV-2 (Partial service degradation)
**Status:** Resolved

---

## 1. Incident Summary

The Order Service became unavailable due to a controlled failure injection via the `/crash` endpoint, simulating a real-world process crash. Docker's restart policy (`unless-stopped`) automatically recovered the service within ~39 seconds. No data was lost.

---

## 2. Impact Assessment

| Component | Impact |
|-----------|--------|
| Order Service | Unavailable for ~39 seconds |
| Order creation | Failed during outage window |
| Other services | Unaffected (fault isolation) |
| Database | Unaffected |
| Monitoring | Active throughout (Prometheus continued scraping) |

**Blast radius:** Single service. All other 5 microservices remained healthy.

---

## 3. Timeline

| Time (UTC+5) | Event |
|-------------|-------|
| 05:47:46 | Crash triggered via `curl http://localhost:5003/crash` |
| 05:47:46 | Order Service process exited |
| 05:47:46 | Docker detected container stop, restart policy triggered |
| 05:47:47 | Container restart initiated |
| 05:47:56 | PostgreSQL health check passed |
| 05:48:06 | Order Service returned HTTP 200 on `/health` |
| 05:48:06 | `RestartCount` incremented to 1 |
| 05:48:06 | **Incident resolved** — full recovery confirmed |

**Total downtime: ~20 seconds**

---

## 4. Root Cause Analysis

**Primary cause:** Simulated process crash via `/crash` endpoint (test instrumentation).

**In a real scenario, equivalent causes would include:**
- Application panic / unhandled exception
- OOM kill by kernel
- Misconfigured database connection string
- Missing environment variable at startup

**Contributing factors:**
- No redundant replicas in Docker Compose setup (single instance)
- No circuit breaker to gracefully handle downstream failures

---

## 5. Detection

| Method | Detection Time |
|--------|---------------|
| Docker health check | ~10 seconds |
| Prometheus `up` metric dropped to 0 | ~15 seconds |
| Manual health check | Immediate |

Alert rule `OrderServiceDown` would fire after 1 minute sustained outage.

---

## 6. Recovery

Recovery was fully automated via Docker restart policy:

```yaml
restart: unless-stopped
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5003/health"]
  interval: 20s
  timeout: 5s
  retries: 3
```

**Manual verification:**
```bash
docker inspect corder-service | grep RestartCount
# "RestartCount": 1

curl http://localhost:5003/health
# {"service":"order-service","status":"healthy"}
```

---

## 7. Lessons Learned

### What went well
- Automatic restart policy worked correctly
- Recovery was fast (~20 seconds)
- Other services were completely unaffected
- Prometheus continued monitoring throughout
- Health endpoint confirmed recovery immediately

### What could be improved
- Add **multiple replicas** in Docker Swarm / Kubernetes for zero-downtime recovery
- Implement **circuit breaker** in services calling Order API
- Add **Alertmanager** with PagerDuty/Slack notifications
- Reduce health check interval from 20s to 10s for faster detection

---

## 8. Action Items

| Action | Owner | Priority | Status |
|--------|-------|----------|--------|
| Deploy Order Service with 2+ replicas in Swarm | SRE Team | HIGH | Planned |
| Add Alertmanager notification routing | SRE Team | HIGH | Planned |
| Implement circuit breaker pattern | Dev Team | MEDIUM | Backlog |
| Reduce health check interval to 10s | SRE Team | LOW | Planned |
| Add `/crash` guard for production builds | Dev Team | HIGH | Backlog |

---

## 9. SLO Impact

| SLO | Target | During Incident | Status |
|-----|--------|-----------------|--------|
| Availability | >= 99% | ~99.95% (20s/30d) | Within budget |
| Latency p95 | <= 200ms | N/A (service down) | N/A |
| Error rate | <= 1% | 100% for 20s | Within 30-day budget |

**Error budget consumed:** 20 seconds out of 43,200 minutes (30 days) = **0.000772%**
Remaining error budget: **99.22%** of monthly budget.
