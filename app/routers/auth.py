from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .. import models
from .. schema import UserLogin
from .. utils import verfiy
from .. database import get_db


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalied Credentials")
    
    if not verfiy(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalied Credentials")
    
    return {'token': "the fuckin token"}