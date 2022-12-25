from typing import List
from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.database import engine, SessionLocal
from blog.hashing import Hash

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', tags=['blogs'], status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    # return {'title': request.title, 'body': request.body}


@app.get('/blog', tags=['blogs'], status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_blog(db: Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog


# for getting a single blog
@app.get('/blog/{id}', tags=['blogs'], status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_single_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'msg': f'Blog with the id {id} not exist.'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} not exist.')
    return blog


# for deleting a blog
@app.delete('/blog/{id}', tags=['blogs'])
def delete_blog(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Blog).filter(id == models.Blog.id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data {id} is not available')
    else:
        data.delete(synchronize_session=False)
        db.commit()
        return f"blog {id} deleted successful"


@app.put('/blog/{id}', tags=['blogs'])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(id == models.Blog.id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data {id} is not available')
    else:
        blog.update(request.dict())
        db.commit()
        return f"blog {id} update successful"


# Users endpoint

@app.get('/user', tags=['users'], status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='users not available')
    else:
        return users


@app.post('/user', tags=['users'], response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,
                           email=request.email,
                           password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', tags=['users'], response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the {id} is not available")
    else:
        return user


@app.delete('/user/{id}', tags=['users'])
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user {id} is not available')
    else:
        user.delete(synchronize_session=False)
        db.commit()
        return f"user {id} deleted successful"
