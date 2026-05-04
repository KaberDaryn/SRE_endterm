import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

TESTS = [
    {"name": "baseline", "concurrency": 5, "requests_per_url": 50},
    {"name": "medium", "concurrency": 20, "requests_per_url": 100},
    {"name": "high", "concurrency": 50, "requests_per_url": 150},
    {"name": "stress", "concurrency": 100, "requests_per_url": 200},
]

URLS = [
    "http://localhost:5000/health",
    "http://user-api:5001/health",
    "http://product-api:5002/health",
    "http://order-api:5003/health",
    "http://product-api:5002/api/products",
]

def hit(url):
    start = time.time()
    try:
        r = requests.get(url, timeout=5)
        latency = time.time() - start
        return url, r.status_code, latency, None
    except Exception as e:
        latency = time.time() - start
        return url, None, latency, str(e)

def percentile(values, p):
    values = sorted(values)
    index = int(len(values) * p)
    if index >= len(values):
        index = len(values) - 1
    return values[index]

def run_test(test):
    tasks = []
    start_all = time.time()

    with ThreadPoolExecutor(max_workers=test["concurrency"]) as executor:
        for url in URLS:
            for _ in range(test["requests_per_url"]):
                tasks.append(executor.submit(hit, url))
        results = [task.result() for task in as_completed(tasks)]

    total_time = time.time() - start_all
    total_requests = len(results)
    success = sum(1 for _, status, _, err in results if status == 200 and err is None)
    failed = total_requests - success
    latencies = [lat for _, _, lat, _ in results]
    avg_latency = sum(latencies) / len(latencies)
    p95 = percentile(latencies, 0.95)
    p99 = percentile(latencies, 0.99)
    rps = total_requests / total_time
    error_rate = (failed / total_requests) * 100

    print(f"\n=== Capacity Test: {test['name']} ===")
    print(f"Concurrency: {test['concurrency']}")
    print(f"Total requests: {total_requests}")
    print(f"Successful requests: {success}")
    print(f"Failed requests: {failed}")
    print(f"Error rate: {error_rate:.2f}%")
    print(f"Total time: {total_time:.2f}s")
    print(f"Approx RPS: {rps:.2f}")
    print(f"Average latency: {avg_latency:.4f}s")
    print(f"P95 latency: {p95:.4f}s")
    print(f"P99 latency: {p99:.4f}s")

    print("\nPer endpoint:")
    for url in URLS:
        subset = [r for r in results if r[0] == url]
        ok = sum(1 for _, status, _, err in subset if status == 200 and err is None)
        subset_latencies = [r[2] for r in subset]
        avg = sum(subset_latencies) / len(subset_latencies)
        ep95 = percentile(subset_latencies, 0.95)
        ep99 = percentile(subset_latencies, 0.99)
        print(f"{url}: {ok}/{len(subset)} successful, avg={avg:.4f}s, p95={ep95:.4f}s, p99={ep99:.4f}s")

def main():
    print("=== Assignment 6 Capacity Planning Matrix ===")
    print("This is a controlled local load simulation, not a production benchmark.")
    for test in TESTS:
        run_test(test)

if __name__ == "__main__":
    main()
