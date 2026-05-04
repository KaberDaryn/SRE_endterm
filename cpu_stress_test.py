import time
import math
from concurrent.futures import ThreadPoolExecutor

DURATION_SECONDS = 30
WORKERS = 4

def cpu_work(worker_id):
    end = time.time() + DURATION_SECONDS
    counter = 0
    while time.time() < end:
        counter += math.sqrt(counter % 100000 + 1)
    return worker_id, counter

print("=== Controlled CPU Stress Test ===")
print(f"Duration: {DURATION_SECONDS}s")
print(f"Workers: {WORKERS}")
print("Target: generate CPU pressure for SRE capacity evidence")

with ThreadPoolExecutor(max_workers=WORKERS) as executor:
    results = list(executor.map(cpu_work, range(WORKERS)))

print("CPU stress test completed")
for worker_id, counter in results:
    print(f"worker={worker_id}, result={counter}")
