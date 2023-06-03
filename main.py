from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    boolean: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "Hello title", "content": "Hello content", "id": 1}, {"title": "Hello titlee", "content": "Hello contentt", "id": 2}]


@app.get("/")
@app.get("/login")
def root():
    return {"message": "Hello"}


@app.get("/posts")
def get_posts():
    return {'data': my_posts}


@app.post('/posts')
def create_post(post: Post):
    print(post.title)
    print(post.content)
    print(post.boolean)
    print(post.rating)
    return {'post': post}