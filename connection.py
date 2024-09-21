from models import Base
from dotenv import load_dotenv
import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
load_dotenv()

db_name = os.getenv("DB_NAME")
user_name = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
token_time=os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES")
secret_key=os.getenv("SECRET_KEY")


db_url = f"postgresql+psycopg2://{user_name}:{password}@{host}:{port}/{db_name}"

engine = create_engine(db_url)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
