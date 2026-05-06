import asyncio
import os
import time
from datetime import datetime
from typing import List

import aiohttp
import asyncpg
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL", "postgresql://postgres:123@localhost/time_manager_db")
URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://docs.python.org/3/library/asyncio.html",
    "https://fastapi.tiangolo.com",
    "https://www.postgresql.org",
    "https://httpbin.org/html",
]
CONCURRENCY = 3


def extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "No title"


async def parse_and_save(
    url: str, session: aiohttp.ClientSession, pool: asyncpg.Pool, sem: asyncio.Semaphore
) -> None:
    async with sem:
        async with session.get(url, timeout=15) as response:
            response.raise_for_status()
            html = await response.text()

    title = extract_title(html)
    slug = f"lr2-async-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
    value = (title[:200] + " " + slug).strip()[:255]

    async with pool.acquire() as conn:
        await conn.execute("INSERT INTO tag (name) VALUES ($1)", value)
    print(f"[asyncio] saved: {url} -> {title}")


async def main() -> None:
    started_at = time.perf_counter()
    sem = asyncio.Semaphore(CONCURRENCY)
    pool = await asyncpg.create_pool(DB_URL, min_size=1, max_size=CONCURRENCY)

    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [parse_and_save(url, session, pool, sem) for url in URLS]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for url, result in zip(URLS, results):
                if isinstance(result, Exception):
                    print(f"[asyncio] error for {url}: {result}")
    finally:
        await pool.close()

    elapsed = time.perf_counter() - started_at
    print(f"[asyncio] elapsed: {elapsed:.3f} sec")


if __name__ == "__main__":
    asyncio.run(main())
