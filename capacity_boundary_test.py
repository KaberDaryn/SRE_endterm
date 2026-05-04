import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

URLS = [
    "http://localhost:5000/health",
    "http://user-api:5001/health",
    "http://product-api:5002/health",
    "http://order-api:5003/health",
    "http://product-api:5002/api/products",
]

TESTS = [
    {"name": "boundary-60", "concurrency": 60, "requests_per_url": 120},
    {"name": "boundary-70", "concurrency": 70, "requests_per_url": 140},
    {"name": "boundary-80", "concurrency": 80, "requests_per_url": 160},
    {"name": "boundary-90", "concurrency": 90, "requests_per_url": 180},
]

SLO_P95_SECONDS = 0.300
SLO_ERROR_RATE = 1.0

def hit(url):
    start = time.time()
    try:
        r = requests.get(url, timeout=5)
        return url, r.status_code, time.time() - start, None
    except Exception as e:
        return url, None, time.time() - start, str(e)

def percentile(values, p):
    values = sorted(values)
    idx = int(len(values) * p)
    if idx >= len(values):
        idx = len(values) - 1
    return values[idx]

print("=== Assignment 6 Capacity Boundary SLO Test ===")
print("SLO assumption: p95 < 0.300s and error rate < 1.00%")

for test in TESTS:
    print(f"\n=== Capacity Boundary Test: {test['name']} ===")
    start = time.time()
    tasks = []

    with ThreadPoolExecutor(max_workers=test["concurrency"]) as executor:
        for url in URLS:
            for _ in range(test["requests_per_url"]):
                tasks.append(executor.submit(hit, url))
        results = [task.result() for task in as_completed(tasks)]

    total_time = time.time() - start
    total = len(results)
    failed = sum(1 for _, status, _, err in results if status != 200 or err is not None)
    success = total - failed
    latencies = [r[2] for r in results]
    rps = total / total_time
    avg = sum(latencies) / len(latencies)
    p95 = percentile(latencies, 0.95)
    p99 = percentile(latencies, 0.99)
    error_rate = failed / total * 100

    print(f"Concurrency: {test['concurrency']}")
    print(f"Total requests: {total}")
    print(f"Successful requests: {success}")
    print(f"Failed requests: {failed}")
    print(f"Error rate: {error_rate:.2f}%")
    print(f"Approx RPS: {rps:.2f}")
    print(f"Average latency: {avg:.4f}s")
    print(f"P95 latency: {p95:.4f}s")
    print(f"P99 latency: {p99:.4f}s")

    if p95 <= SLO_P95_SECONDS and error_rate < SLO_ERROR_RATE:
        print("SLO result: PASS")
    else:
        print("SLO result: FAIL")
