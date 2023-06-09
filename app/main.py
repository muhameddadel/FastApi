import time
import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from sqlalchemy.orm import session

from . import models
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='0506450922chaos', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("You connect to database successfully!")
        break
    except Exception as error:
        print(f"your connection to database faild because of {error} error..")
        time.sleep(1)

my_posts = [{"title": "Hello title", "content": "Hello content", "id": 1}, {"title": "Hello titlee", "content": "Hello contentt", "id": 2}]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post


def find_post_index(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i

@app.get("/")
@app.get("/login")
def root():
    return {"message": "Hello"}

@app.get('/sqlalchemy')
def test_posts(db: SessionLocal = Depends(get_db)):
    return {'status': "success"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM POSTS """)
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" insert into posts (title, content, published) values (%s, %s, %s) returning * """, 
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {'post': new_post}


@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute(""" select * from posts where id = %s """, (str(id)))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} dose not found")

    return {'post_detail': post}


@app.delete('/posts/{id}')
def delete_post(id: int):
    cursor.execute(""" delete from posts where id = %s returning * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} dose not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning * """, 
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} dose not exist")

    return {'data': updated_post}