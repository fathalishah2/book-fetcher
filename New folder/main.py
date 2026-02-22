from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel, Field

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Pydantic Model
# -----------------------------
class Book(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    author: str
    publisher: str


# -----------------------------
# In-memory database
# -----------------------------
books_db = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "publisher": "Scribner"},
    {"id": 2, "title": "1984", "author": "George Orwell", "publisher": "Secker & Warburg"},
    {"id": 3, "title": "The Hobbit", "author": "J.R.R. Tolkien", "publisher": "Allen & Unwin"},
    {"id": 4, "title": "Principles", "author": "Ray Dalio", "publisher": "Simon & Schuster"},
]

next_id = len(books_db) + 1


# -----------------------------
# Root
# -----------------------------
@app.get("/")
def read_root():
    return {"message": "Hello World!"}


@app.get("/hello/{name}")
def say_hello(name: str) -> dict:
    return {"message": f"Hello {name}!"}


# -----------------------------
# POST - Add Book
# -----------------------------
@app.post("/books")
def add_book(book: Book):
    global next_id

    new_book = {
        "id": next_id,
        **book.model_dump()
    }

    books_db.append(new_book)
    next_id += 1

    return {"message": "Book added successfully", "book": new_book}


# -----------------------------
# GET - Search Books + Pagination
# -----------------------------
@app.get("/search-books/")
def search_books(
    q: Optional[str] = Query(None, min_length=3, max_length=100),
    skip: int = 0,
    limit: int = 10,
):
    # اگر چیزی سرچ نشد → کل کتاب‌ها با pagination
    if not q:
        return {
            "total": len(books_db),
            "count": len(books_db[skip: skip + limit]),
            "items": books_db[skip: skip + limit],
        }

    query = q.lower()

    results = [
        book for book in books_db
        if (
            query in book["title"].lower()
            or query in book["author"].lower()
            or query in book["publisher"].lower()
        )
    ]

    paginated = results[skip: skip + limit]

    return {
        "total": len(results),
        "count": len(paginated),
        "items": paginated,
    }