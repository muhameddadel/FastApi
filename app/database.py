import time
import psycopg2
from psycopg2.extras import RealDictCursor

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:0506450922chaos@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='0506450922chaos', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("You connect to database successfully!")
        break
    except Exception as error:
        print(f"your connection to database faild because of {error} error..")
        time.sleep(1)
