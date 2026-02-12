# -----------
# Project : Openlibrary book fetcher with publick API
# Github : https://github.com/fathalishah2
# Purpose : Find books by their publish date(year)
# -----------

import requests
import csv
import os

# Configs
API_URL = "https://openlibrary.org/search.json"
HEADERS = {"User-Agent": "BookFetcher/1.0"}
MIN_YEAR = 2000
MAX_YEAR = 2026
TARGET_COUNT = 50

OUTPUT = "outputs"
os.makedirs(OUTPUT, exist_ok=True)
OUTPUT_F = os.path.join(OUTPUT, "books_after_2000.csv")
filtered_books = []
page = 1

# Loop until receiving TARGET_COUNT
while len(filtered_books) < TARGET_COUNT:
    params = {"q": "book", "limit": 100, "page": page, "sort": "new"}

    response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
    data = response.json()
    books_raw = data.get("docs", [])

    if not books_raw:
        break  # There is no more book!

    for book in books_raw:
        year = book.get("first_publish_year")
        if year and MIN_YEAR <= year <= MAX_YEAR:
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
