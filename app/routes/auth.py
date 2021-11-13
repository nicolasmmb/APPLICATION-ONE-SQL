from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
###
from app.database import database
from app.schemas import schemas
from app.models import models
from app.utils import utils
###
import time
from app.utils import oauth

router = APIRouter(tags=['Authentication'])


@router.post('/login')
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.cpf == user_credentials.cpf).first()

    if not user_credentials.senha:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Password')

    if not user_credentials.cpf:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid CPF')

    if not user_credentials:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    if not utils.verify(user_credentials.senha, user.senha):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    auth = oauth.create_token({"user_id": user.id})

    return {
        "token": auth,
        "type": 'bearer'
    }
