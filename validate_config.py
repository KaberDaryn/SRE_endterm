#!/usr/bin/env python
import socket
import sys
import requests

def check_connectivity(host, port, service_name):
    try:
        socket.create_connection((host, port), timeout=3)
        print(f"✓ {service_name} ({host}:{port}) - OK")
        return True
    except Exception as e:
        print(f"✗ {service_name} ({host}:{port}) - FAILED: {e}")
        return False

def check_health_endpoint(url, service_name):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            print(f"✓ {service_name} health endpoint - OK")
            return True
        else:
            print(f"✗ {service_name} health endpoint - Status {r.status_code}")
            return False
    except Exception as e:
        print(f"✗ {service_name} health endpoint - FAILED: {e}")
        return False

def main():
    print("=== Configuration Validation ===\n")
    
    all_ok = True
    
    # Check databases
    print("[1] Database Connectivity:")
    all_ok &= check_connectivity("cuser_dbase", 5432, "User DB")
    all_ok &= check_connectivity("cproduct_dbase", 5432, "Product DB")
    all_ok &= check_connectivity("corder_dbase", 5432, "Order DB")
    
    # Check service ports
    print("\n[2] Service Ports:")
    all_ok &= check_connectivity("cfrontend-app", 5000, "Frontend App")
    all_ok &= check_connectivity("cuser-service", 5001, "User Service")
    all_ok &= check_connectivity("cproduct-service", 5002, "Product Service")
    all_ok &= check_connectivity("corder-service", 5003, "Order Service")
    
    # Check health endpoints
    print("\n[3] Health Endpoints:")
    all_ok &= check_health_endpoint("http://cfrontend-app:5000/health", "Frontend /health")
    all_ok &= check_health_endpoint("http://cuser-service:5001/health", "User Service /health")
    all_ok &= check_health_endpoint("http://cproduct-service:5002/health", "Product Service /health")
    all_ok &= check_health_endpoint("http://corder-service:5003/health", "Order Service /health")
    
    # Check metrics endpoints
    print("\n[4] Metrics Endpoints:")
    all_ok &= check_health_endpoint("http://cfrontend-app:5000/metrics", "Frontend /metrics")
    all_ok &= check_health_endpoint("http://cuser-service:5001/metrics", "User Service /metrics")
    all_ok &= check_health_endpoint("http://cproduct-service:5002/metrics", "Product Service /metrics")
    all_ok &= check_health_endpoint("http://corder-service:5003/metrics", "Order Service /metrics")
    
    # Check monitoring stack
    print("\n[5] Monitoring Stack:")
    all_ok &= check_connectivity("prometheus", 9090, "Prometheus")
    all_ok &= check_connectivity("grafana", 3000, "Grafana")
    all_ok &= check_connectivity("node-exporter", 9100, "Node Exporter")
    
    print("\n" + "="*40)
    if all_ok:
        print("✓ ALL CHECKS PASSED")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
