from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oauth2

from ..database import get_db

router = APIRouter(
  tags=["Authentication"],
  prefix="/auth"
)

@router.post('/login', response_model=schemas.Token)
# def login(user_creds: schemas.Login,  db: Session = Depends(get_db)): # for json
def login(user_creds: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.email == user_creds.username).first()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail=f"Invalid Credentials"
    )
  
  is_pass_match = utils.verify_password(user_creds.password, user.password)
  if not is_pass_match:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail=f"Invalid Credentials"
    )

  # Create a token
  access_token = oauth2.create_access_token(data = {"user_id": user.id})
  return {"access_token": access_token, "token_type": "bearer"}
