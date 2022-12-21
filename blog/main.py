from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List

from blog import schemas, models
from blog.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    # return {'title': request.title, 'body': request.body}


@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_blog(db: Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog


# for getting a single blog
@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_single_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'msg': f'Blog with the id {id} not exist.'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} not exist.')
    return blog


# for deleting a blog
@app.delete('/blog/{id}')
def delete_blog(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Blog).filter(id == models.Blog.id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data {id} is not available')
    else:
        data.delete(synchronize_session=False)
        db.commit()
        return f"blog {id} deleted successful"


@app.put('/blog/{id}')
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    data = db.query(models.Blog).filter(id == models.Blog.id)
    if not data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data {id} is not available')
    else:
        data.update(request.dict())
        db.commit()
        return f"blog {id} update successful"
