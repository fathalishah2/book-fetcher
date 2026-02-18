# -----------
# Project : Openlibrary book fetcher with publick API
# Github : https://github.com/fathalishah2
# Purpose : Find books by their publish date(year)
# -----------

import requests
import csv
import os
from typing import List, Dict, Any

# Configs
API_URL: str = "https://openlibrary.org/search.json"
HEADERS: Dict[str, str] = {"User-Agent": "BookFetcher/1.0"}
MIN_YEAR: int = 2000
MAX_YEAR: int = 2026
TARGET_COUNT: int = 50

OUTPUT: str = "outputs"
os.makedirs(OUTPUT, exist_ok=True)
OUTPUT_F: str = os.path.join(OUTPUT, "books_after_2000.csv")

filtered_books: List[Dict[str, Any]] = []
page: int = 1

# Loop until receiving TARGET_COUNT
while len(filtered_books) < TARGET_COUNT:
    params: Dict[str, Any] = {
        "q": "book", 
        "limit": 100, 
        "page": page, 
        "sort": "new"
        }

    response: requests.Response = requests.get(
        API_URL, 
        params=params, 
        headers=HEADERS, 
        timeout=10
        )
    
    data: Dict[str, Any] = response.json()
    books_raw: List[Dict[str, Any]] = data.get("docs", [])

    if not books_raw:
        break  # There is no more book!

    for book in books_raw:
        year: int | None = book.get("first_publish_year")

        if isinstance(year, int) and MIN_YEAR <= year <= MAX_YEAR:
            filtered_books.append(
                {
                    "title": book.get("title", "N/A"),
                    "author": ", ".join(book.get("author_name", [])),
                    "publish_year": year,
                }
            )
            if len(filtered_books) >= TARGET_COUNT:
                break

    page += 1

# Saving
with open(OUTPUT_F, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "author", "publish_year"])
    writer.writeheader()
    writer.writerows(filtered_books[:TARGET_COUNT])

print(
    f"{len(filtered_books[:TARGET_COUNT])} after {MIN_YEAR} saved in {os.path.abspath(OUTPUT_F)}!"
)
