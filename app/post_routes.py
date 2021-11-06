from typing import List
from fastapi import status, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from app.database import get_db
from .main import app, cursor, conn
from . import schemas

# This file has routes manupulating db using sql queries

# Create user using sql query
@app.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
  cursor.execute("""SELECT * FROM posts """)
  posts = cursor.fetchall()
  return posts

@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
  cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (
    post.title, post.content, post.published
  ))
  new_post = cursor.fetchone()
  conn.commit()
  return new_post

@app.get('/posts/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
  cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
  post = cursor.fetchone()
  if not post:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Post with id: {id} doesn't exists"
    )
  return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
  deleted_post = cursor.fetchone()
  conn.commit()
  if not deleted_post:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Post with id: {id} doesn't exists"
    )
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
  cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (
    updated_post.title, updated_post.content, updated_post.published, str(id),
  ))
  updated_post_db = cursor.fetchone()
  conn.commit()
  return  updated_post_db