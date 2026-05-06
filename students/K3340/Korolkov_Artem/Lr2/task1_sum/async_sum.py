import asyncio
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


async def calculate_sum_async(start: int, end: int) -> int:
    await asyncio.sleep(0)
    return calculate_sum(start, end)


async def main() -> None:
    ranges = split_ranges(MAX_N, WORKERS)

    started_at = time.perf_counter()
    tasks = [calculate_sum_async(start, end) for start, end in ranges]
    parts = await asyncio.gather(*tasks)
    total = sum(parts)
    elapsed = time.perf_counter() - started_at

    print(f"asyncio total: {total}")
    print(f"asyncio elapsed: {elapsed:.6f} sec")


if __name__ == "__main__":
    asyncio.run(main())
