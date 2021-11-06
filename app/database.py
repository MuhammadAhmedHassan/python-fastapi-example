# from psycopg2.extras import RealDictCursor
# import time
# import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database>"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Connection to database, if fails, it will retry after 5 secs
# while True:
#   try:
#     conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="root", cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('\nSuccessfully connected to database\n')
#     break
#   except Exception as error:
#     print('error connecting to database')
#     print('ERROR: ', error)
#     time.sleep(5)
