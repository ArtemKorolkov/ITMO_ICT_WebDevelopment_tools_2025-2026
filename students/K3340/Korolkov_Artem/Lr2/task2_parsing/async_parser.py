import asyncio
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List

import aiohttp
import asyncpg
from bs4 import BeautifulSoup
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env", override=True)

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
    url: str,
    session: aiohttp.ClientSession,
    pool: asyncpg.Pool,
    sem: asyncio.Semaphore,
    tag_column: str,
) -> None:
    async with sem:
        async with session.get(url, timeout=15) as response:
            response.raise_for_status()
            html = await response.text()

    title = extract_title(html)
    slug = f"lr2-async-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
    value = (title[:200] + " " + slug).strip()[:255]

    async with pool.acquire() as conn:
        await conn.execute(f"INSERT INTO tag ({tag_column}) VALUES ($1)", value)
    print(f"[asyncio] saved: {url} -> {title}")


async def create_pool_with_retry(db_url: str, attempts: int = 3) -> asyncpg.Pool:
    last_exc: Exception | None = None
    urls_to_try = [db_url]
    if "localhost" in db_url:
        urls_to_try.append(db_url.replace("localhost", "127.0.0.1"))

    for try_url in urls_to_try:
        for attempt in range(1, attempts + 1):
            try:
                return await asyncpg.create_pool(
                    try_url,
                    min_size=1,
                    max_size=CONCURRENCY,
                    timeout=10,
                    command_timeout=20,
                )
            except Exception as exc:
                last_exc = exc
                print(
                    f"[asyncio] db connect attempt {attempt}/{attempts} failed for {try_url}: {exc}"
                )
                await asyncio.sleep(1)

    raise RuntimeError(
        "Could not connect to PostgreSQL. Check DB_URL, PostgreSQL service status, and network access."
    ) from last_exc


async def detect_tag_column(pool: asyncpg.Pool) -> str:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = 'tag'
            """
        )
    available = {row["column_name"] for row in rows}
    if "name" in available:
        return "name"
    if "title" in available:
        return "title"

    fallback = sorted(col for col in available if col != "id")
    if fallback:
        chosen = fallback[0]
        print(f"[asyncio] using fallback column '{chosen}' in table 'tag'")
        return chosen

    async with pool.acquire() as conn:
        await conn.execute("ALTER TABLE tag ADD COLUMN name VARCHAR(255)")
    print("[asyncio] created missing column 'name' in table 'tag'")
    return "name"


async def main() -> None:
    started_at = time.perf_counter()
    sem = asyncio.Semaphore(CONCURRENCY)
    pool = await create_pool_with_retry(DB_URL)
    tag_column = await detect_tag_column(pool)

    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [parse_and_save(url, session, pool, sem, tag_column) for url in URLS]
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
