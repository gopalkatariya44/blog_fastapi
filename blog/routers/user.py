from typing import List
from fastapi import APIRouter,Depends, status, HTTPException
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.database import get_db
from blog.hashing import Hash

router = APIRouter()


@router.get('/user', tags=['users'], status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='users not available')
    else:
        return users


@router.post('/user', tags=['users'], response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,
                           email=request.email,
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{id}', tags=['users'], response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the {id} is not available")
    else:
        return user


@router.delete('/user/{id}', tags=['users'])
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user {id} is not available')
    else:
        user.delete(synchronize_session=False)
        db.commit()
        return f"user {id} deleted successful"
