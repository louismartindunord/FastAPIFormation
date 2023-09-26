from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


# En utilisant le parametre Basemodel en verifie que les données entrées correspondes/
class BookRequest(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=1, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    # to provide extra information or metadata about the data expected
    class Config:
        schema_extra = {
            "example": {
                "title": "a new book",
                "author": "codingwithrobie",
                "description": "a new description",
                "rating": 5,
                "published_date": 2023,
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2022),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5, 2010),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5, 2021),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2012),
    Book(5, "HP2", "Author 2", "Book Description", 3, 2019),
    Book(6, "HP3", "Author 3", "Book Description", 1, 2016),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/books/by_rating")
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
            return books_to_return


# Indent automatiquement l'id rentré dans l'api
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


# Inputs are checked  by the BookRequest class and if they are fitting get in BOOKS
@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    book_dict = book_request.dict()
    new_book = Book(**book_dict)
    BOOKS.append(find_book_id(new_book))


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in enumerate(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/books/by_published_date")
async def read_book_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    book_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            book_to_return.append(book)
    return book_to_return
