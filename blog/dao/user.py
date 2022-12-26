from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from blog import schemas, models
from blog.hashing import Hash


# TODO: create
def create_user(request: schemas.User, db: Session):
    new_user = models.User(name=request.name,
                           email=request.email,
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# TODO: read
def get_all_users(db: Session):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='users not available')
    else:
        return users


def get_one_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the {user_id} is not available")
    else:
        return user


# TODO: delete
def delete_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user {user_id} is not available')
    else:
        user.delete(synchronize_session=False)
        db.commit()
        return f"user {user_id} deleted successful"
