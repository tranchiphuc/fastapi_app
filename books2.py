from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book: 
    id: int
    title: str
    author: str
    description: str
    rating: float   
    published_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: float, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on creation", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(ge=1, le=5)
    published_date: int = Field(ge=2000, le=2030)
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }
    }    


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS

@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(rating: int = Query(ge=0, le=5)):
    result_books = []
    for book in BOOKS:
        if book.rating == rating:
            result_books.append(book)
    return result_books


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_new_book(book_request: BookRequest):
    book_without_id = Book(**book_request.model_dump())
    BOOKS.append(add_book_id(book_without_id))

def add_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book_by_id(book_request: BookRequest):
    for idx in range(len(BOOKS)):
        #print("idx=", idx, ", BOOK[idx].id=", BOOKS[idx].id, ", book_request.id=", book_request.id)
        if BOOKS[idx].id == book_request.id:
            BOOKS[idx] = book_request
            print("Update completed")
            return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.delete("/delete-book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id: int = Path(gt=0)):
    for idx in range(len(BOOKS)):
        if BOOKS[idx].id == book_id:
            BOOKS.pop(idx)
            return BOOKS
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")   
