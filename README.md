### 📚 OpenLibrary Book Fetcher
A Python script that fetches 50 valid books published after 2000 from the [OpenLibrary API](https://openlibrary.org/).

## Features
-  Fetches books with pagination (auto continues until 50 books)
-  Filters real publication years (2000–2026)
-  Saves output as CSV in outputs/ directory
-  Clean code with error handling
-  Python 3.8+

## You can modify these variables according to your needs:
- MIN_YEAR
- MAX_YEAR
- TARGET_COUNT

## Installation
1. Clone the repository:
git clone https://github.com/fathalishah2/book-fetcher.git
cd openlibrary-book-fetcher
2. Install dependencies:
pip install -r requirements.txt

## Usage
Run the script:
python main.py
Output will be saved in:
outputs/books_after_2000.csv

# Example Output
| Title | Author | Publish Year |
|-------|--------|--------------|
| Atomic Habits | James Clear | 2018 |
| ... | ... | ... |

# 🛠️ Requirements
- Python 3.8+
- requests

# 📄 License
MIT

## 👨‍💻 Author
(https://github.com/fathalishah2)
