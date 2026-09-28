from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

BOOKS = [{'title': "Title One", 'author':'author one', 'category':'science'},
         {'title': "Title Two", 'author':'author one', 'category':'science'},
         {'title': "Title Three", 'author':'author Three', 'category':'history'},
         {'title': "Title Four", 'author':'author Four', 'category':'math'},
         {'title': "Title Five", 'author':'author Five', 'category':'math'},
         {'title': "Title Six", 'author':'author Six', 'category':'math'}]


@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/mybook")
async def read_all_books():
    return {"book_title": "My Book"}

#PATH PARAMETR
@app.get("/books/{book_title}")
async def read_book(book_title:str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return book

#QUERY PARAMATER
@app.get("/books/")
async def read_category(category:str):
    books_to_return = []
    for book in BOOKS:
        if book['category'].casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/books_by_author_query/")
async def read_book(author:str):
    b=[]
    for book in BOOKS:
        if book['author'].casefold() == author.casefold():
            b.append(book)
    return b


#PATH AND QUERY PARAMETER
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author:str, category:str):
    books_to_return = []
    for book in BOOKS:
        if book['category'].casefold() == category.casefold() and book['author'].casefold() == book_author.casefold():
            books_to_return.append(book)

    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == book_title.casefold():
            BOOKS.pop(i)
            break



@app.get("/books/books_by_author_path/{author}")
async def read_book(author:str):
    b=[]
    for book in BOOKS:
        if book['author'].casefold() == author.casefold():
            b.append(book)
    return b

