from fastapi import FastAPI, Depends, status, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

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


@app.get('/blog', status_code=status.HTTP_200_OK)
def get_blog(db: Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog


@app.delete('/blog/{id}')
def delete_blog(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Blog).filter(id == models.Blog.id).delete(synchronize_session=False)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data {id} is not available')
    else:
        db.commit()
        return f"blog {id} deleted successful"


@app.put('/blog/{id}')
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    data = db.query(models.Blog).filter(id == models.Blog.id).update(request.dict())
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'data {id} is not available')
    else:
        db.commit()
        return f"blog {id} update successful"
