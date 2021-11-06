# from fastapi import status, HTTPException
# from fastapi.params import Depends
# from sqlalchemy.orm.session import Session

# from app.database import get_db
# from .main import app, cursor, conn
# from . import schemas

# # This file has routes manupulating db using sql queries

# # Create user using sql query
# @app.post("/users", status_code=status.HTTP_201_CREATED)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#   try:
#     cursor.execute("""INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *""", (
#       user.email, user.password
#     ))
#     new_user = cursor.fetchone()
#     conn.commit()
#     return new_user
#   except Exception as error:
#     print('Error: ', error)
#     raise HTTPException(
#       status_code=status.HTTP_400_BAD_REQUEST,
#       detail=f"Email already in use"
#     )

# @app.get('/users/{id}')
# def get_user(id: int):
#   cursor.execute("""SELECT * FROM users WHERE id = %s""", (
#     str(id)
#   ))
#   user = cursor.fetchone()
#   if not user:
#     raise HTTPException(
#       status_code=status.HTTP_400_BAD_REQUEST,
#       detail=f"User with id {id} not found"
#     )
#   del user['password']
#   return user
