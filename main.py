from fastapi import FastAPI

from database.config import engine
from database.models import Base
from routers import health, posts

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def hello_world():
    return {"hello": "world!"}


app.include_router(health.router, tags=["health"])
app.include_router(posts.router, tags=["posts"])
