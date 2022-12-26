from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.dao import user
from blog.database import get_db
from blog.hashing import Hash

router = APIRouter(
    prefix='/user',
    tags=['users']
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_user(db: Session = Depends(get_db)):
    return user.get_all_users(db)


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(request, db)


@router.get('/{user_id}', response_model=schemas.ShowUser)
def get_one_user(user_id: int, db: Session = Depends(get_db)):
    return user.get_one_user(user_id, db)


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user.delete_user(user_id, db)
