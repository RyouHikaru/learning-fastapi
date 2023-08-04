from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=11)
    published_date: int = Field(gt=1899, lt=2024)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "No Longer Human",
                "author": "Dazai Osamu",
                "description": "A book about being disqualified as a human being",
                "rating": 9,
                "published_date": 2020
            }
        }


BOOKS = [
    Book(1, "Computer Science for Dummies", "RyouHikaru",
         "An easy to read book about CS", 10, 2018),
    Book(2, "Learn Java", "RyouHikaru", "Learn Java the easiest way", 8, 2019),
    Book(3, "React + Redux Ready!", "Tapioca",
         "Tutorials for React and Redux", 6, 2022),
    Book(4, "Tailwind makes the Wind", "Suijei",
         "A guide on how to use Tailwind CSS", 8, 2022),
    Book(5, "Node vs. Python for Newbies", "Orcha",
         "Comparing best backend programming language", 9, 2023),
    Book(6, "Calculation for CS", "Tapioca",
         "A Mathematical book for CS students", 7, 2020),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    """
    Read all books.

    Returns:
        books: All books
    """
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(gt=0)):
    """
    Read book by ID.

    Args:
        book_id (str): ID of the book

    Returns:
        book: The book matching the ID
    """
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(
        status_code=404, detail="Book with id of {} not found".format(book_id))


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=11)):
    """
    Read books by rating.

    Args:
        book_rating (str): Rating of the book

    Returns:
        books_to_return: The books matching the rating
    """
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/published-date/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=1899, lt=2024)):
    """
    Read books by published date.

    Args:
        published_date (str): Published date of the book

    Returns:
        books_to_return: The books matching the published date
    """
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    """
    Add a new book.

    Args:
        book_request (BookRequest): Request for adding a book
    """
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put("/books/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    """
    Update a book.

    Args:
        book (BookRequest): Request for updating a book

    Raises:
        HTTPException: Request book ID is not found
    """
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True

    if not book_changed:
        raise HTTPException(
            status_code=404, detail="Book with id of {} not found".format(book.id))


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    """
    Delete a book.

    Args:
        book_id (int): ID of book to be deleted

    Raises:
        HTTPException: Request book ID is not found
    """
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(
            status_code=404, detail="Book with id of {} not found".format(book_id))


def find_book_id(book: Book):
    """
    Generate unique book id.

    Args:
        book (Book): Book to be added

    Returns:
        book: Book with updated ID
    """
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
