from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, load_only
#
from app.models.models import Address, User
from app.schemas.schemas import UserCreate, UserUpdate, UserGet
from app.database.database import get_db
# Utils
from app.utils import utils
from app.utils import oauth
import time

router = APIRouter(
    prefix="/users",
    # tags=['USERS']
)

fields = [User.id, User.nome, User.email, User.cpf, User.pis]


@router.post('/create', response_model=UserCreate, status_code=status.HTTP_201_CREATED, tags=['USERS'])
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


@router.get('/get-all/', status_code=status.HTTP_200_OK, tags=['USERS'])
async def get_users(db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user), limit: int = None):

    try:
        if limit:
            users = db.query(User).limit(limit).values(*fields)
        else:
            users = db.query(User).values(*fields)
        return users

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__cause__))


@router.get('/get-by-id/{id}', status_code=status.HTTP_200_OK, tags=['USERS'])
async def get_user_by_id(id: int, db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):

    user = db.query(User).filter(User.id == id).values(*fields)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.get('/get-my-info',  status_code=status.HTTP_200_OK, tags=['USER-AUTO'])
async def get_my_complete_user_info(db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):

    join = db.query(User, Address).join(Address).filter(User.id == user_data.id).values(*fields, Address)

    if not join:
        user = db.query(User).filter(User.id == user_data.id).values(*fields, *Address)
        return user

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found - User")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found - Joins")

    return join


@router.get('/get-complete-info', status_code=status.HTTP_200_OK, tags=['USERS'])
def get_users_with_address_associated(db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user), limit: int = None):
    try:
        if limit:
            join = join = db.query(User, Address).join(Address).limit(limit).values(*fields, Address)
        else:
            join = join = db.query(User, Address).join(Address).values(*fields, Address)
        return join
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__cause__))


@router.patch('/update/{id}', response_model=UserUpdate, status_code=status.HTTP_200_OK, tags=['USERS'])
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


@router.patch('/update-my-user', response_model=UserUpdate, status_code=status.HTTP_200_OK, tags=['USER-AUTO'])
async def update_my_user(user: UserUpdate, db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):

    user_db = db.query(User).filter(User.id == user_data.id).first()

    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_db.nome = user.nome if user.nome else user_db.nome
    user_db.email = user.email if user.email else user_db.email
    user_db.cpf = user.cpf if user.cpf else user_db.cpf
    user_db.pis = user.pis if user.pis else user_db.pis
    user_db.senha = utils.hash(password=user.senha) if user.senha else user_db.senha

    db.commit()
    return user_db


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK, tags=['USERS'])
async def delete_user_by_id(id: int, db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):
    user_db = db.query(User).filter(User.id == id)

    if not user_db.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_db.delete(synchronize_session=False)
    db.commit()
    return {"detail": "User deleted"}


@router.delete('/delete-my-user', status_code=status.HTTP_200_OK, tags=['USER-AUTO'])
async def delete_user_by_id(db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):
    user_db = db.query(User).filter(User.id == user_data.id)

    if not user_db.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_db.delete(synchronize_session=False)
    db.commit()
    return {"detail": "User deleted"}
