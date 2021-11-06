from fastapi import status, HTTPException, Response, APIRouter
from typing import List, Optional
from fastapi.params import Depends
import sqlalchemy
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import current_user
from ..database import get_db
from .. import schemas, models, main, oauth2

router = APIRouter(
  prefix="/vote",
  tags=["Vote"]
)
  
# Create vote
@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
  try:
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if (vote.dir == schemas.VoteEnum.up_vote):
      if found_vote:
        raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail=f"user {current_user.id} has already voted on post with id {vote.post_id}"
        )
      new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
      db.add(new_vote)
      db.commit()
      # db.refresh(new_vote) # no need to send vote back
      return {"message": "Successfully added vote"}
  
    # Down Vote functionality needs to modify table
    # elif (vote.dir == schemas.VoteEnum.down_vote):
    #   if not found_vote:
    #     raise HTTPException(
    #       status_code=status.HTTP_404_NOT_FOUND,
    #       detail=f"user {current_user.id} has not voted on post with id {id}"
    #     )
      
    #   print('down vote')
    else:
      if not found_vote:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"vote on post with id {vote.post_id} does not exists"
        )
      vote_query.delete(synchronize_session=False)
      db.commit()
      return {"message": "Successfully deleted vote"}
  except sqlalchemy.exc.IntegrityError as error:
    print(error)
    print('TYPE OF ERROR', type(error))
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"post with id {vote.post_id} does not exists"
    )
    