from fastapi import status, HTTPException, Response, APIRouter
from typing import List, Optional
from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import current_user
from ..database import get_db
from .. import schemas, models, main, oauth2, config
from app import database

router = APIRouter(
  prefix="/posts",
  tags=["Posts"]
)

# Get all posts
# @router.get('/', response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
  # posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
  # return posts
  # LEFT JOIN query
  # select posts.*, Count(votes.post_id) as total_votes from posts left join votes on posts.id = votes.post_id where posts.id = 4 group by posts.id;
  posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
      models.Post.title.contains(search)
    ).offset(skip).limit(limit).all()

  return posts

# Create a post
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
  # new_post = models.Post(title=post.title, content=post.content, published=post.published)
  new_post = models.Post(owner_id=current_user.id, **post.dict()) # **{} is like a spread operator
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post


# Get latest post
# This handler should come first then the last one
@router.get('/latest')
def get_latest_post():
  database.cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""")
  latest_post = database.cursor.fetchone()
  print("LATEST_POST", latest_post)
  return latest_post


# Get post by id
# @router.get('/{id}', response_model=schemas.Post)
@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
  # post = db.query(models.Post).filter(models.Post.id == str(id)).one_or_none()
  post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == str(id)).one_or_none()
  if not post:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Post with id: {id} doesn't exists"
    )
  # is_owner = post.owner_id == current_user.id
  # if not is_owner:
  #   raise HTTPException(
  #     status_code=status.HTTP_403_FORBIDDEN,
  #     detail=f"unauthorized"
  #   )
  return post

# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
  # Relationship of post and user is remaining
  post_to_delete_query = db.query(models.Post).filter(models.Post.id == str(id))
  post_to_delete = post_to_delete_query.first()
  if not post_to_delete:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Post with id: {id} doesn't exists"
    )
  
  is_owner = post_to_delete.owner_id == current_user.id
  if not is_owner:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail=f"unauthorized"
    )
    
  post_to_delete_query.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
  post_query = db.query(models.Post).filter(models.Post.id == str(id))
  post = post_query.first()
  if not post:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Post with id: {id} doesn't exists"
    )
  
  is_owner = post.owner_id == current_user.id
  if not is_owner:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail=f"unauthorized"
    )

  post_query.update(updated_post.dict(), synchronize_session=False)
  db.commit()
  return post_query.first()
