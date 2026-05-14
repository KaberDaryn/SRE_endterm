#!/usr/bin/env python3
"""
SRE End-Term Project — Automated Incident Response & Rollback
Student: Kaber Daryn | SE-2430

Usage:
    python rollback.py --service order-api
    python rollback.py --service order-api --action restart
    python rollback.py --all
    python rollback.py --status
"""
import subprocess
import sys
import time
import argparse
from datetime import datetime

SERVICES = {
    "frontend":     {"container": "cfrontend-app",       "port": 5000, "health": "/health"},
    "user-api":     {"container": "cuser-service",       "port": 5001, "health": "/health"},
    "product-api":  {"container": "cproduct-service",    "port": 5002, "health": "/health"},
    "order-api":    {"container": "corder-service",      "port": 5003, "health": "/health"},
    "notification": {"container": "cnotification-service","port": 5004, "health": "/health"},
    "payment-api":  {"container": "cpayment-service",    "port": 5005, "health": "/health"},
}


def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    prefix = {"INFO": "✓", "WARN": "⚠", "ERROR": "✗", "ACTION": "→"}.get(level, "•")
    print(f"[{ts}] {prefix} {msg}")


def run(cmd, capture=True):
    r = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    return r.stdout.strip(), r.returncode


def check_health(service_name):
    info = SERVICES[service_name]
    out, rc = run(f'docker inspect --format="{{{{.State.Health.Status}}}}" {info["container"]}')
    return out.strip('"'), rc


def get_restart_count(service_name):
    info = SERVICES[service_name]
    out, _ = run(f'docker inspect --format="{{{{.RestartCount}}}}" {info["container"]}')
    try:
        return int(out)
    except ValueError:
        return -1


def restart_service(service_name):
    info = SERVICES[service_name]
    log(f"Restarting {service_name} ({info['container']})...", "ACTION")
    _, rc = run(f"docker restart {info['container']}")
    if rc == 0:
        log(f"{service_name} restart triggered", "INFO")
        time.sleep(10)
        return wait_for_healthy(service_name)
    else:
        log(f"Failed to restart {service_name}", "ERROR")
        return False


def wait_for_healthy(service_name, timeout=60):
    log(f"Waiting for {service_name} to become healthy...", "INFO")
    for i in range(timeout // 5):
        status, _ = check_health(service_name)
        if status == "healthy":
            log(f"{service_name} is healthy ✓", "INFO")
            return True
        if status == "unhealthy":
            log(f"{service_name} is unhealthy after restart", "WARN")
            return False
        time.sleep(5)
    log(f"{service_name} health check timed out", "WARN")
    return False


def rollback_service(service_name):
    log(f"=== ROLLBACK: {service_name} ===", "ACTION")
    before = get_restart_count(service_name)
    log(f"RestartCount before: {before}", "INFO")

    success = restart_service(service_name)

    after = get_restart_count(service_name)
    log(f"RestartCount after:  {after}", "INFO")

    if success:
        log(f"ROLLBACK SUCCESS — {service_name} recovered", "INFO")
    else:
        log(f"ROLLBACK FAILED — manual intervention needed for {service_name}", "ERROR")
    return success


def print_status():
    log("=== SERVICE STATUS ===", "INFO")
    print(f"{'Service':<20} {'Container':<25} {'Health':<12} {'Restarts'}")
    print("-" * 70)
    for name, info in SERVICES.items():
        health, _ = check_health(name)
        restarts = get_restart_count(name)
        icon = "✓" if health == "healthy" else ("⚠" if health == "starting" else "✗")
        print(f"{name:<20} {info['container']:<25} {icon} {health:<10} {restarts}")


def detect_issues():
    issues = []
    for name in SERVICES:
        health, _ = check_health(name)
        restarts = get_restart_count(name)
        if health == "unhealthy":
            issues.append((name, f"unhealthy (restarts={restarts})"))
        elif restarts >= 3:
            issues.append((name, f"restart loop (count={restarts})"))
    return issues


def main():
    parser = argparse.ArgumentParser(description="SRE Automated Rollback Tool")
    parser.add_argument("--service", help="Service name to rollback")
    parser.add_argument("--action", choices=["restart", "rollback"], default="rollback")
    parser.add_argument("--all", action="store_true", help="Check and fix all services")
    parser.add_argument("--status", action="store_true", help="Show service status")
    parser.add_argument("--auto", action="store_true", help="Auto-detect and fix issues")
    args = parser.parse_args()

    if args.status:
        print_status()
        return

    if args.auto:
        log("=== AUTO INCIDENT DETECTION ===", "ACTION")
        issues = detect_issues()
        if not issues:
            log("All services healthy — no action needed", "INFO")
        else:
            log(f"Found {len(issues)} issue(s):", "WARN")
            for svc, reason in issues:
                log(f"  {svc}: {reason}", "WARN")
                rollback_service(svc)
        return

    if args.all:
        log("=== ROLLING RESTART ALL SERVICES ===", "ACTION")
        for name in SERVICES:
            rollback_service(name)
            time.sleep(5)
        print_status()
        return

    if args.service:
        if args.service not in SERVICES:
            log(f"Unknown service: {args.service}. Available: {list(SERVICES.keys())}", "ERROR")
            sys.exit(1)
        rollback_service(args.service)
        return

    # Default: show status + auto-detect
    print_status()
    print()
    issues = detect_issues()
    if issues:
        log(f"Detected {len(issues)} issue(s). Run with --auto to fix.", "WARN")


if __name__ == "__main__":
    main()
