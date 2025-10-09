from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Bookstore(BaseModel):
    id: int
    title: str
    author: str
    price: float
    in_stock: bool

books = [
    {
        "id": 1,
        "title": "The Love Hypothesis",
        "author": "Ali Hazelwood",
        "price": 399.00,
        "in_stock": True
    },
    {
        "id": 2,
        "title": "Verity",
        "author": "Colleen Hoover",
        "price": 499.00,
        "in_stock": False
    },
    {
        "id": 3,
        "title": "Beach Read",
        "author": "Emily Henry",
        "price": 429.00,
        "in_stock": True
    }
]

@app.get("/books")
def get_books():
    return {"message": "All books listed", "books": books}

@app.get("/books/atmost_price")
def get_books_atmost_price():
    atmost_price = []
    for b in books:
        if b["price"] < 500:
            atmost_price.append(b)
    return {"Books cheaper than 500": atmost_price}
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/{author}")
def get_book(author: str):
    for book in books:
        if book["author"] == author:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/count")
def get_books_count():
    total = len(books)
    return {"Count": total}




@app.get("/books/available")
def get_book_in_stock():
    available_bk = []
    for b in books:
        if b["in_stock"] == True:
            available_bk.append(b)
    return {"message": "Book retrived successfully", "books": available_bk}
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for b in books:
        if b["id"] == book_id:
            return {"message": "Book retrived successfully", "books": b}
    raise HTTPException(status_code=404, detail="Book not found")





@app.post("/books", status_code=201)
def add_book(book: Bookstore):
    books.append(book)
    return {"message": "New books created", "book": book}
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Bookstore):
    for i, b in enumerate(books):
        if b["id"] == book_id:
            b["price"] = book.price
            b["in_stock"] = book.in_stock
            return {"message": "Book updated successfully", "book": update_book}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id : int):
    for i, b in enumerate(books):
        if b["id"] == book_id:
            return {"message": "Book deleted successfully", "book": delete_book}
    raise HTTPException(status_code=404, detail="Book not found")

