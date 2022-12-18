from fastapi import FastAPI, Depends, status
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
    db.query(models.Blog).filter(id == models.Blog.id).delete(synchronize_session=False)
    db.commit()
    return f"blog {id} deleted successful"

