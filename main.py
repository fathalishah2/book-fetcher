# -----------
#Created by: fathalishah2 in github
# -----------

import requests
import csv
import os
from typing import List, Dict


# -----config
API_P = "Insert your API link from OpenLibrary!!"
QUERY = "python"
LIMIT = 50
MIN_Y = 2000 #you can change it, it's for filtering books!
OUTPU_F = "output/books.csv" #Where you want save it?
# -----------

def fetch_books(api_p: str, query: str, limit: int) -> List[Dict]:
    """
    Fetch books from OpenLibrary API
    """
    params = {
        "q" : query,
        "limit" : limit
    }
    response = requests.get(api_p, params=params, timeout=9)
    response.raise_for_status() #notif erors when request failed

    data = response.json()
    return data.get("docs", [])

def filter_books_year(books: List[Dict], min_y: int) -> List[Dict]:

    filtered = []
    
    for book in books:
        publish_y = book.get("first_pub_year")

        if publish_y and publish_y > min_y :
            filtered.append({
                "title": book.get("title"),
                "author": ",".join(book.get("author_name", [])),
                "publish_y": publish_y
            })
    return filtered

def save_to_csv(books: List[Dict], filename: str) -> None:
    if not books:
        print("No books to save :(")
        return
    os.makedirs(os.path.dirname(filename), exits_ok = True)

    fieldnames = ["title", "author", "publish_y"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

def main():
    try:
        books = fetch_books(API_P, QUERY, LIMIT)
        filtered_books = filter_books_year(books, MIN_Y)
        save_to_csv(filtered_books, OUTPU_F)
        print(f"I find {len(filtered_books)} books after {MIN_Y}")

    except requests.RequestException as e:
        print(f"API EROR: {e}")

if __name__ == "__main__":
    main()