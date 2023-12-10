from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from blog import models, schemas


# TODO: create
def create_blog(request: schemas.Blog, db: Session, id):
    new_blog = models.Blog(title=request.title, body=request.body, id=id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# TODO: read
def get_all_blogs(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def get_one_blog(blog_id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'msg': f'Blog with the id {id} not exist.'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {blog_id} not exist.')
    return blog


# TODO: update
def update_blog(blog_id, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(blog_id == models.Blog.id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data {blog_id} is not available')
    else:
        blog.update(request.dict())
        db.commit()
        return f"blog {blog_id} update successful"


# TODO: delete
def delete_blog(blog_id: int, db: Session):
    data = db.query(models.Blog).filter(blog_id == models.Blog.id).first()
    print(not data)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog {blog_id} is not available')
    else:
        data.delete(synchronize_session=False)
        db.commit()
        return f"blog {blog_id} deleted successful"
