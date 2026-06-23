from fastapi import FastAPI, Body

app = FastAPI()


     

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")
async def get_all_books():
    return BOOKS


   
@app.get("/books/title/{book_title}")
async def get_book_title(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
    return {"NULL": "No book founded"}

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# Get all books from a specific author using path or query parameters
@app.get("/books/byauthor/")
async def get_book_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}")
async def read_author_category_by_query(book_author: str, category: str):
    find_books = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold() and \
        book.get("category").casefold() == category.casefold():
            find_books.append(book) 
    return find_books
    

@app.get("/books/{dymanic_param}")
async def get_dynamic_param(dynamic_param: str):
    return {"dynamic_param" : dynamic_param}

@app.post("/books/create_book")
async def create_new_book(new_book=Body()):
    BOOKS.append(new_book)
    return 

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book
            break
    return 

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
    return BOOKS