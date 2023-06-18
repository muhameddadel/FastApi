from typing import List, Optional

from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2
from .. schema import *
from .. utils import hash
from .. database import  get_db


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[PostVotesJoin])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM POSTS """)
    # posts = cursor.fetchall()

    # posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    query_posts = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(
            models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    return [{"post": post, "votes": votes} for post, votes in query_posts]





@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" insert into posts (title, content, published) values (%s, %s, %s) returning * """, 
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Posts(user_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{id}', response_model=PostVotesJoin)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" select * from posts where id = %s """, (str(id)))
    # post = cursor.fetchone()
    query_post = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(
            models.Posts.id).filter(models.Posts.id==id).first()

    if not query_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} dose not found")
    
    # print(query_post)
    # print(query_post[0])
    # print(query_post[1])

    post = query_post[0]
    votes = query_post[1]

    return {"post": post, "votes": votes}


@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" delete from posts where id = %s returning * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Posts).filter(models.Posts.id==id)
    
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} dose not exist")

    if deleted_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not autherize to perform this action")

    deleted_post.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning * """, 
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Posts).filter(models.Posts.id==id)
    
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} dose not exist")

    if updated_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not autherize to perform this action")
    
    updated_post.update(post.dict())
    db.commit()

    return updated_post.first()