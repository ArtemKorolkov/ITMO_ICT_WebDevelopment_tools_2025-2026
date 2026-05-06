import multiprocessing as mp
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
    return (start + end) * (end - start + 1) // 2


def main() -> None:
    ranges = split_ranges(MAX_N, WORKERS)

    started_at = time.perf_counter()
    with mp.Pool(processes=WORKERS) as pool:
        parts = pool.starmap(calculate_sum, ranges)

    total = sum(parts)
    elapsed = time.perf_counter() - started_at

    print(f"multiprocessing total: {total}")
    print(f"multiprocessing elapsed: {elapsed:.6f} sec")


if __name__ == "__main__":
    main()
