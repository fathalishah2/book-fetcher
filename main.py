# -----------
#Created by: fathalishah2 in github
# -----------
import requests
import csv
import os
from typing import List, Dict
# ----------------------
# ----Configuration---
# --------------------
API_URL = "https://openlibrary.org/search.json"
LIMIT = 50
MIN_YEAR = "1900"
OUTPUT_FILE = "output/books.csv"

# User-Agent برای اطمینان از پاسخ API
HEADERS = {
    "User-Agent": "bookfetcher/1.0 (mhdifathali@gmail.com)"
}
# ----------------------

def fetch_books(api_url: str, query: str, limit: int) -> List[Dict]:
    """
    Fetch books from OpenLibrary API based on a general query.
    """
    params = {
        "q": query,
        "limit": limit
    }

    response = requests.get(api_url, params=params, headers=HEADERS, timeout=25)
    response.raise_for_status()

    data = response.json()
    return data.get("docs", [])

def filter_books_by_year(books: List[Dict], min_year: int) -> List[Dict]:
    """
    Filter books published after a specific year.
    """
    filtered = []

    for book in books:
        years = book.get("publish_year", [])
        recent_years = [year for year in years if year > min_year]

        if recent_years:
            filtered.append({
                "title": book.get("title", "N/A"),
                "author": ", ".join(book.get("author_name", [])),
                "publish_year": max(recent_years)
            })

    return filtered

def save_to_csv(books: List[Dict], filename: str) -> None:
    """
    Save book data into a CSV file.
    """
    if not books:
        print("No books to save.")
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    fieldnames = ["title", "author", "publish_year"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)


def main():
    try:
        # کوئری عمومی که همیشه نتیجه می‌دهد
        query = "book"

        books = fetch_books(API_URL, query, LIMIT)

        filtered_books = filter_books_by_year(books, MIN_YEAR)
        save_to_csv(filtered_books, OUTPUT_FILE)

        print(f"Saved {len(filtered_books)} books published after {MIN_YEAR}.")

    except requests.RequestException as e:
        print(f"API Error: {e}")


if __name__ == "__main__":
    main()
