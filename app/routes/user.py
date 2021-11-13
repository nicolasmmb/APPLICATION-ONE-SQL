from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
#
from app.models.models import User
from app.schemas.schemas import UserCreate, UserUpdate, UserGet
from app.database.database import get_db
# Utils
from app.utils import utils
from app.utils import oauth
import time

router = APIRouter(
    prefix="/users",
    tags=['USERS']
)


@router.post('/create', response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        pass_hashed = utils.hash(password=user.senha)
        user.senha = pass_hashed
        new_user = User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__cause__))


@router.get('/get-all', status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__cause__))


@router.get('/get-by-id/{id}', response_model=UserGet, status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int, db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):

    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.put('/update/{id}', response_model=UserUpdate, status_code=status.HTTP_200_OK)
async def update_user_by_id(id: int, user: UserUpdate, db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):
    user_db = db.query(User).filter(User.id == id).first()

    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_db.nome = user.nome if user.nome else user_db.nome
    user_db.email = user.email if user.email else user_db.email
    user_db.cpf = user.cpf if user.cpf else user_db.cpf
    user_db.pis = user.pis if user.pis else user_db.pis
    user_db.senha = utils.hash(password=user.senha) if user.senha else user_db.senha
    db.commit()
    return user_db


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
async def delete_user_by_id(id: int, db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):
    user_db = db.query(User).filter(User.id == id)

    if not user_db.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_db.delete(synchronize_session=False)
    db.commit()
    return {"detail": "User deleted"}
