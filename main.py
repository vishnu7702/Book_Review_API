from fastapi import FastAPI, HTTPException, Depends, Request
import datetime
from pydantic import BaseModel
from connection import Session
from models import User_Credentials, Add_Books, Add_Reviews
from schema import User_Details,Adding_Books,Updating_Books,Adding_Reviews,Search_Books
import jwt
session = Session()
app = FastAPI()

from authentication import adding_expiry_jwt,get_headers,remove_bearer


# User Signing Up


@app.post("/sign_up")
async def sign_in_func(item: User_Details):
    try:
        username = item.user_name
        password = item.password
        check_username = session.query(User_Credentials).filter(
            User_Credentials.user_name == username).first()
        if check_username:
            return "User With This User Name Already Exist"
        elif check_username is None:
            add_user = User_Credentials(user_name=username, password=password)
            session.add(add_user)
            session.commit()
            return {"message": "SIGN UP SUCCESSFULL"}
    except Exception as e:
        return {"The error from signup-api is":e}


# User Logging In
@app.post("/login")
async def login(item: User_Details):
    try:
        username = item.user_name
        password = item.password
        check_login = session.query(User_Credentials).filter(
            User_Credentials.user_name == username).first()
        if check_login is None:
            raise HTTPException(status_code=403, detail="Invalid Credentials")
        else:
            database_user_name = check_login.user_name
            database_password = check_login.password
            if database_user_name != username or database_password != password:
                raise HTTPException(status_code=403, detail="Invalid Credentials")
            else:
                user_data = {"user_name": username}
                token = adding_expiry_jwt(user_data)
                return {"token": token}
    except Exception as e:
        return {"The error from login-api is":e}


# Adding Books
@app.post("/add_books")
async def to_add_books(item: Adding_Books, token_username: str = Depends(get_headers)):
    try:
        book_name = item.book_name
        author = item.author
        published_year = item.published_year
        if token_username is False:
            raise HTTPException(status_code=401, detail="Unauthorised")
        user_exist = session.query(User_Credentials).filter(
            User_Credentials.user_name == token_username).first()
        if user_exist:
            add_book = Add_Books(book_name=book_name,
                                author=author, published_year=published_year)
            session.add(add_book)
            session.commit()
            return f"{book_name} Book Added Successfully"
        else:
            raise HTTPException(status_code=401, detail="Unauthorised")
    except Exception as e:
        return {"The error from add_books-api is":e}

# Deleting Books


@app.delete("/delete_books/{book_id}")
async def to_delete_books(book_id: int, token_username: str = Depends(get_headers)):
    try:
        if token_username is False:
            raise HTTPException(status_code=401, detail="Unauthorised")
        user_exist = session.query(User_Credentials).filter(
            User_Credentials.user_name == token_username).first()
        if user_exist:
            book_to_delete = session.query(Add_Books).filter(
                Add_Books.book_id == book_id).first()
            if book_to_delete is None:
                return "No Books Found To Delete"
            else:
                database_book_name = book_to_delete.book_name
                session.delete(book_to_delete)
                session.commit()
                session.close()
                return f"Deleted {database_book_name} Book Successfully"
        else:
            raise HTTPException(status_code=401, detail="Unauthorised")
    except Exception as e:
        print("The error from delete-api is:",e)

# Viewing Books


@app.get("/view_books")
async def to_view_books(token_username: str = Depends(get_headers)):
    try:
        if token_username is False:
            raise HTTPException(status_code=401, detail="Unauthorised")
        user_exist = session.query(User_Credentials).filter(
            User_Credentials.user_name == token_username).first()
        if user_exist:
            display_all_books = session.query(
                Add_Books).order_by(Add_Books.book_id).all()
            my_books = {}
            for book in display_all_books:
                my_books[book.book_id] = book.book_name
            if my_books is None:
                return "No Books Found"
            else:
                return {"books": my_books}
        else:
            raise HTTPException(status_code=401, detail="Unauthorised")
    except Exception as e:
        return {"The error from view_books-api is":e}


# Updating Books
@app.patch("/update_books/{book_id}")
async def to_update_books(book_id: int, item: Updating_Books, token_username: str = Depends(get_headers)):
    try:
        if token_username is False:
            raise HTTPException(status_code=401, detail="Unauthorised")
        updated_book_name = item.update_book_name
        updated_author = item.update_author
        updated_published_year = item.update_published_year

        user_exist = session.query(User_Credentials).filter(
            User_Credentials.user_name == token_username).first()
        if user_exist:
            book_to_update = session.query(Add_Books).filter(
                Add_Books.book_id == book_id).first()
            if book_to_update is None:
                return "No Book Found"
            else:
                database_book_name = book_to_update.book_name
                if updated_book_name is not None:
                    book_to_update.book_name = updated_book_name
                if updated_author is not None:
                    book_to_update.author = updated_author
                if updated_published_year is not None:
                    book_to_update.published_year = updated_published_year
                session.commit()
                return f"Updated {database_book_name} Book Successfully"
        else:
            raise HTTPException(status_code=401, detail="Unauthorised")
    except Exception as e:
        return {"The error from update_books-api is":e}
    

# Review Management
# Adding Reviews To A Specific Book


@app.post("/add_review/{book_id}")
async def to_add_review(book_id: int, item: Adding_Reviews, token_username: str = Depends(get_headers)):
    try:
        review = item.review
        if token_username is False:
            raise HTTPException(status_code=401, detail="Unauthorised")
        user_exist = session.query(User_Credentials).filter(
            User_Credentials.user_name == token_username).first()
        if user_exist:
            check_books = session.query(Add_Books).filter(
                Add_Books.book_id == book_id).first()
            if not check_books:
                return "No Book Found To Give Review"
            else:
                database_bookname = check_books.book_name
                add_review = Add_Reviews(review=review, book_id=book_id)
                session.add(add_review)
                session.commit()
                return f"Review For {database_bookname} Book Added Successfully"

        else:
            raise HTTPException(status_code=401, detail="Unauthorised")
    except Exception as e:
        return {"The error from add_review-api is":e}
# Viewing Reviews For A Specific Book


@app.get("/view_reviews/{book_id}")
async def to_view_reviews(book_id: int, token_username: str = Depends(get_headers)):
    try:
        if token_username is False:
            raise HTTPException(status_code=401, detail="Unauthorised")
        user_exist = session.query(User_Credentials).filter(
            User_Credentials.user_name == token_username).first()
        if user_exist:
            check_review = session.query(Add_Reviews).filter(
                Add_Reviews.book_id == book_id).all()
            if not check_review:
                return "No Reviews Found For This Book"
            else:
                reviews_dict = {}
                counter = 1
                for reviews in check_review:
                    reviews_dict[f"review {counter}"] = reviews.review
                    counter = counter+1
                return reviews_dict

        else:
            raise HTTPException(status_code=401, detail="Unauthorised")
    except Exception as e:
        return {"The error from view_reviews-api is":e}


# Searching Books
@app.get("/search_books")
async def to_search_books(item: Search_Books, token_username: str = Depends(get_headers)):
    try:
        if token_username is False:
            raise HTTPException(status_code=401, detail="Unauthorised")
        book_name = item.book_name
        author = item.author
        published_year = item.published_year
        user_exist = session.query(User_Credentials).filter(
            User_Credentials.user_name == token_username).first()
        if user_exist:
            books_list = {}
            counter = 1
            if book_name is not None:
                book_data = session.query(Add_Books).filter(
                    Add_Books.book_name == book_name).all()
                for book in book_data:
                    books_list[f"Book{counter}"] = book.book_name, book.author, book.published_year
                    counter = counter+1
            if author is not None:
                book_data = session.query(Add_Books).filter(
                    Add_Books.author == author).all()
                for book in book_data:
                    books_list[f"Book{counter}"] = book.book_name, book.author, book.published_year
                    counter = counter+1
            if published_year is not None:
                book_data = session.query(Add_Books).filter(
                    Add_Books.published_year == published_year).all()
                for book in book_data:
                    books_list[f"Book{counter}"] = book.book_name, book.author, book.published_year
                    counter = counter+1
            if books_list:
                final_dict = {}
                for key, value in books_list.items():
                    if value not in final_dict.values():
                        final_dict[key] = value
                return final_dict
            else:
                return "No Books Found"
    except Exception as e:
        return {"The error from search_books-api is":e}
