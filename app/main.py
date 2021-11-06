# To create virtual environment
# py -3 -m name <any_name>
# And this virtual environment is isolated only to this project
# ---------------
# To start our app
# uvicorn main:app --reload
# OR
# uvicorn app.main:app --reload

# In python 'package' is just a fancy name for foler/dir
# but every package will have __init__.py file, to show
# that this folder is python package.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware
# from . import models
# from .database import engine
# from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
  # "http://localhost.tiangolo.com",
  # "https://localhost.tiangolo.com",
  # "http://localhost",
  # "http://localhost:8080",
  # "https://www.google.com",
  "*"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Root route
@app.get('/')
async def root():
  return {"message": "Hello world"}
  
# Routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
  