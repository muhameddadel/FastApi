from typing import List

from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .. import models
from .. schema import *
from .. utils import hash
from .. database import  get_db


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM POSTS """)
    # posts = cursor.fetchall()
    posts = db.query(models.Posts).all()

    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" insert into posts (title, content, published) values (%s, %s, %s) returning * """, 
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{id}', response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" select * from posts where id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Posts).filter(models.Posts.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} dose not found")

    return post


@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" delete from posts where id = %s returning * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Posts).filter(models.Posts.id==id)
    
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} dose not exist")

    deleted_post.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning * """, 
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Posts).filter(models.Posts.id==id)
    
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} dose not exist")

    updated_post.update(post.dict())
    db.commit()

    return updated_post.first()