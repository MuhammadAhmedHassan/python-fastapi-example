from fastapi import Depends, status, HTTPException, APIRouter, Body
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from .. import models, schemas, utils, main
from ..database import get_db

router = APIRouter(
  prefix="/users",
  tags=["Users"]
)

# USER specific routes
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  try:
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
  except IntegrityError as error:
    print(error)
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Email already in use"
    )

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == str(id)).first()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"User with id {id} not found"
    )
  return user
