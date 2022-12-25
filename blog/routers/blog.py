from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.database import get_db

router = APIRouter()


@router.get('/blog', tags=['blogs'], status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_blog(db: Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog


@router.post('/blog', tags=['blogs'], status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    # return {'title': request.title, 'body': request.body}


# for getting a single blog
@router.get('/blog/{id}', tags=['blogs'], status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_single_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'msg': f'Blog with the id {id} not exist.'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} not exist.')
    return blog


# for deleting a blog
@router.delete('/blog/{id}', tags=['blogs'])
def delete_blog(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Blog).filter(id == models.Blog.id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data {id} is not available')
    else:
        data.delete(synchronize_session=False)
        db.commit()
        return f"blog {id} deleted successful"


@router.put('/blog/{id}', tags=['blogs'])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(id == models.Blog.id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data {id} is not available')
    else:
        blog.update(request.dict())
        db.commit()
        return f"blog {id} update successful"
