import uvicorn
from fastapi import FastAPI

from blog import models
from blog.routers import blog, user, authentication
from blog.database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
