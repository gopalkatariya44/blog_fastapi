from fastapi import FastAPI

from blog import models
from blog.routers import blog, user
from blog.database import engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
