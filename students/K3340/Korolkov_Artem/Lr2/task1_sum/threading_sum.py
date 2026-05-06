import threading
import time
from typing import List, Tuple

MAX_N = 10_000_000_000_000
WORKERS = 8


def split_ranges(limit: int, parts: int) -> List[Tuple[int, int]]:
    chunk = limit // parts
    ranges: List[Tuple[int, int]] = []
    start = 1
    for idx in range(parts):
        end = start + chunk - 1
        if idx == parts - 1:
            end = limit
        ranges.append((start, end))
        start = end + 1
    return ranges


def calculate_sum(start: int, end: int) -> int:
    # Sum for [start, end] via arithmetic progression formula.
    return (start + end) * (end - start + 1) // 2


def worker(start: int, end: int, result: List[int], index: int) -> None:
    result[index] = calculate_sum(start, end)


def main() -> None:
    ranges = split_ranges(MAX_N, WORKERS)
    result = [0] * WORKERS
    threads = []

    started_at = time.perf_counter()
    for idx, (start, end) in enumerate(ranges):
        thread = threading.Thread(target=worker, args=(start, end, result, idx))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    total = sum(result)
    elapsed = time.perf_counter() - started_at

    print(f"threading total: {total}")
    print(f"threading elapsed: {elapsed:.6f} sec")


if __name__ == "__main__":
    main()
