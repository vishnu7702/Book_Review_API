from pydantic import BaseModel


class User_Details(BaseModel):
    user_name: str
    password: str

# BASE MODEL FOR ADDING BOOKS


class Adding_Books(BaseModel):
    book_name: str
    author: str
    published_year: int


# BASE MODEL FOR UPDATING BOOKS


class Updating_Books(BaseModel):
    update_book_name: str = None
    update_user_name: str = None
    update_author: str = None
    update_published_year: int = None
# BASE MODEL FOR ADDING REVIEWS


class Adding_Reviews(BaseModel):
    review: str

# BASE MODEL FOR SEARCHING BOOKS BY AUTHOR,BOOK NAME AND YEAR


class Search_Books(BaseModel):
    book_name: str = None
    author: str = None
    published_year: int = None
