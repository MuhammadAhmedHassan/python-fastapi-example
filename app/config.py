from pydantic import BaseSettings

class Settings(BaseSettings):
  # pydantic models variables are case insensitive
  database_hostname : str
  database_port : str
  database_password : str
  database_name : str
  database_username : str
  secret_key : str
  algorithm : str
  access_token_expire_minutes : int
  DATABASE_URL: str
  db_url: str
  ALEMBIC_DATABASE_URL: str
  class Config:
    env_file = ".env"

settings = Settings()