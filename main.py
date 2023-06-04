from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    boolean: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "Hello title", "content": "Hello content", "id": 1}, {"title": "Hello titlee", "content": "Hello contentt", "id": 2}]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

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
def get_post(id: int, response: Response):
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} do not found")

    return {'post_detail': post}