import time
import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

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


@app.get("/posts")
def get_posts():
    return {'data': my_posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000)
    my_posts.append(post_dict)
    return {'post': post_dict}


@app.get('/posts/{id}')
def get_post(id: int):
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} do not found")

    return {'post_detail': post}


@app.delete('/posts/{id}')
def delete_post(id: int):
    index = find_post_index(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} dose not exist")
    
    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} dose not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {'data': post_dict}