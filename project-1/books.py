from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Book1", "author": "Nicolas Cage", "category": "Science"},
    {"title": "Book2", "author": "Donny Smith", "category": "Science"},
    {"title": "Book3", "author": "Pain Cage", "category": "History"},
    {"title": "Book4", "author": "Steven Cage", "category": "Math"},
    {"title": "Book5", "author": "Donny Smith", "category": "Math"},
    {"title": "Book6", "author": "Robert Will", "category": "Math"}
]


@app.get("/books")
async def read_all_books():
    """
    Read all books.

    Returns:
        books: All books
    """
    return BOOKS


@app.get("/books/{book_title}")
async def read_books_by_title(book_title: str):
    """
    Read books by title.

    Args:
        book_title (str): Title of the book

    Returns:
        book: The book matching the title
    """
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def read_books_by_category(category: str):
    """
    Read books by category as query parameter.

    Args:
        category (str): Category of the book

    Returns:
        books: The books matching the category
    """
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def read_books_by_author_and_category(book_author: str, category: str):
    """
    Read books by author as path parameter and category as query parameter.

    Args:
        book_author (str): Author of the book
        category (str): Category of the book

    Returns:
        books: The books matching the criteria
    """
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold() and \
                book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    """
    Add a new book.

    Args:
        new_book (book): New book to be added
    """
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    """
    Update a book.

    Args:
        updated_book (book): Contents of updated book
    """
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_boos/{book_title}")
async def delete_book(book_title: str):
    """
    Delete a book.

    Args:
        book_title (str): Title of the book to be deleted
    """
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


@app.get("/books/authors/{author}")
async def read_books_by_author(author: str):
    """
    Ready books by author.

    Args:
        author (str): Author of the book

    Returns:
        books: The books matching the author
    """
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return
