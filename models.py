from sqlalchemy import String, Integer, Column, Text, ForeignKey
from sqlalchemy.orm import declarative_base, Relationship

Base = declarative_base()


class User_Credentials(Base):
    __tablename__ = "user_data"
    user_name = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)


class Add_Books(Base):
    __tablename__ = "add_books"
    book_id = Column(Integer, autoincrement=True,
                     primary_key=True, nullable=False)
    book_name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published_year = Column(Integer, nullable=False)


class Add_Reviews(Base):
    __tablename__ = "reviews_to_books"
    id = Column(Integer, primary_key=True, nullable=False)
    review = Column(Text, nullable=False)
    book_id = Column(Integer, nullable=False)
