from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import IntEnum, Enum

# Response model
class UserOut(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime
  updated_at: datetime
  class Config:
    orm_mode = True

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True
  # rating: Optional[int] = None

class PostCreate(PostBase):
  pass

# Response model
class Post(PostBase):
  id: int
  created_at: datetime
  owner_id: int
  owner: UserOut
  class Config:
    orm_mode = True

class PostOut(BaseModel):
  Post: Post
  votes: int
  class Config:
    orm_mode = True


# Create user model
class UserCreate(BaseModel):
  email: EmailStr
  password: str

# Login user model
class Login(BaseModel):
  email: EmailStr
  password: str

# Login Response
class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[str] = None

# class VoteEnum(IntEnum):
#   up_vote = 1
#   remove_vote = 0
#   down_vote = -1

class VoteEnum(Enum):
  up_vote = "up_vote"
  remove_vote = "remove_vote"
  # down_vote = "down_vote"

class Vote(BaseModel):
  post_id: int
  dir: VoteEnum