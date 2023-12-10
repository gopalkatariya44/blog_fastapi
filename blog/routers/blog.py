from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from blog import schemas, models, oauth2
from blog.dao import blog
from blog.database import get_db


router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_blog(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all_blogs(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create_blog(request, db, current_user.id)
    # return {'title': request.title, 'body': request.body}


# for getting a single blog
@router.get('/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_one_blog(blog_id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_one_blog(blog_id, db)


# for deleting a blog
@router.delete('/{blog_id}')
def delete_blog(blog_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete_blog(blog_id, db)


@router.put('/{blog_id}')
def update_blog(blog_id, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update_blog(blog_id, request, db)
