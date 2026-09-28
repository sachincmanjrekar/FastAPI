from typing import Optional

from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: Optional[int] = Field(default=None)


    def __init__(self,id,title,author,description,rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Book ID not needed on create", default=None)
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=200)
    rating: int = Field(gt=0, lt=6)
    published_date: Optional[int] = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra":
            {"example":{
            "title":"A new book",
            "author": "codingwithsachin",
            "description":"A new book",
            "rating":1,
            "published_date":2000
        }}
    }



BOOKS = [
    Book(1, 'Computer Science Pro', 'coding with sachin', 'A very nice book', 5, published_date=2000),
    Book(2, 'Be Fast with FastAPI', 'coding with sachin', 'A great nice book', 5, published_date=2001),
    Book(3, 'Master Endpoints', 'coding with sachin', 'A awesome nice book', 5, published_date=2002),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, published_date=2003),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, published_date=2004),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, published_date=2005),

]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


# @app.post("/create-book")
# async def create_book(book_request: BookRequest):
#     print(type(book_request))
#     BOOKS.append(book_request)

# @app.post("/create-book")
# async def create_book(book_request: BookRequest):
#     new_book = Book(**book_request.dict())
#     print(type(new_book))
#     BOOKS.append(new_book)

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book(book_rating:int=Query(gt=0,lt=6)):
    b=[]
    query_book_rating = book_rating
    for book in BOOKS:
        if book.rating == book_rating:
            print("book rating is", book.rating)
            b.append(book)

    return b

# @app.post("/books/", status_code=status.HTTP_201_CREATED)
# async def create_book(book_title:str):
#     for book in BOOKS:
#         if book.title.casefold() == book_title.casefold():
#             return book

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_by_id(new_book))


def find_book_by_id(book: book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id+1
    else:
        book.id = 1

    return book

@app.put("/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book_by_id(updated_book: BookRequest):
    found=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == updated_book.id:
            BOOKS[i] = updated_book
            found=True
            print("book found")
            break

    if not found:
        print("Book not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/books/delete_book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_title(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break


@app.get("/books/find_book_by_date/{year}")
async def read_book(year:int):
    for book in BOOKS:
        if book.published_date == year:
            return book




