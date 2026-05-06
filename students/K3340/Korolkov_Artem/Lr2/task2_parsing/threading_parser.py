import os
import threading
import time
from datetime import datetime
from typing import List

import psycopg2
import requests
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
THREADS = 3


def chunkify(items: List[str], chunks: int) -> List[List[str]]:
    result = [[] for _ in range(chunks)]
    for idx, value in enumerate(items):
        result[idx % chunks].append(value)
    return [chunk for chunk in result if chunk]


def extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "No title"


def parse_and_save(url: str, conn) -> None:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    title = extract_title(response.text)
    slug = f"lr2-thread-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
    value = (title[:200] + " " + slug).strip()[:255]

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO tag (name) VALUES (%s)", (value,))
    conn.commit()
    print(f"[threading] saved: {url} -> {title}")


def worker(urls: List[str]) -> None:
    conn = psycopg2.connect(DB_URL)
    try:
        for url in urls:
            try:
                parse_and_save(url, conn)
            except Exception as exc:
                print(f"[threading] error for {url}: {exc}")
    finally:
        conn.close()


def main() -> None:
    groups = chunkify(URLS, THREADS)
    jobs = []
    started_at = time.perf_counter()

    for group in groups:
        job = threading.Thread(target=worker, args=(group,))
        job.start()
        jobs.append(job)

    for job in jobs:
        job.join()

    elapsed = time.perf_counter() - started_at
    print(f"[threading] elapsed: {elapsed:.3f} sec")


if __name__ == "__main__":
    main()
