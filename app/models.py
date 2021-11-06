from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean, DateTime, Integer, String
from .database import Base

class Post(Base):
  __tablename__ = "posts"
  id=Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
  title=Column(String, nullable=False)
  content=Column(String, nullable=False)
  published=Column(Boolean, 
    # default=True # not this using the following instead
    server_default='TRUE',
    nullable=False
  )
  created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

  owner_id = Column(Integer, ForeignKey(
    "users.id", ondelete='CASCADE'
  ), nullable=False)

  owner = relationship("User")


class User(Base):
  __tablename__ = "users"
  id=Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
  email=Column(String, nullable=False, index=True, unique=True)
  password=Column(String, nullable=False)
  created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
  updated_at=Column(DateTime(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))

class Vote(Base):
  __tablename__ = "votes"
  user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False, index=True)
  post_id=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False, index=True)