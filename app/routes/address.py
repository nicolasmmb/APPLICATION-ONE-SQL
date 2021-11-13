from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
#
from app.models.models import Address, User
from app.schemas.schemas import AddressCreate, AddressUpdate, AddressGet
from app.database.database import get_db
from app.routes import oauth
# Utils
from app.utils import utils
import time


router = APIRouter(
    prefix="/address",
    tags=['ADDRESS']
)


@router.post('/create', response_model=AddressCreate, status_code=status.HTTP_201_CREATED)
async def create_address(address: AddressCreate, db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):
    try:
        to_address_encode = address.dict().copy()
        to_address_encode.update({'user_id': user_data.id})

        new_address = Address(**to_address_encode)
        db.add(new_address)

        db.commit()
        db.refresh(new_address)

        return new_address
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__cause__))


@router.get('/get-all', status_code=status.HTTP_200_OK)
async def get_addresss(db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):
    try:
        address = db.query(Address).all()
        return address
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__cause__))


@router.get('/get-by-id/{id}', response_model=AddressGet, status_code=status.HTTP_200_OK)
async def get_address_by_id(id: int, db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):
    address = db.query(Address).filter(Address.id == id).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    return address


@router.put('/update/{id}', response_model=AddressUpdate, status_code=status.HTTP_200_OK)
async def update_address_by_id(id: int, address: AddressUpdate, db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):
    address_db = db.query(Address).filter(Address.id == id).first()
    if not address_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    address_db.pais = address.pais if address.pais else address_db.pais
    address_db.estado = address.estado if address.estado else address_db.estado
    address_db.municipio = address.municipio if address.municipio else address_db.municipio
    address_db.cep = address.cep if address.cep else address_db.cep
    address_db.rua = address.rua if address.rua else address_db.rua
    address_db.numero = address.numero if address.numero else address_db.numero
    address_db.complemento = address.complemento if address.complemento else address_db.complemento
    address_db.user_id = address.user_id if address.user_id else address_db.user_id

    db.commit()
    return address_db


@router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
async def delete_address_by_id(id: int, db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):
    address_db = db.query(Address).filter(Address.id == id)
    if not address_db.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    address_db.delete(synchronize_session=False)
    db.commit()

    return {"detail": "Address deleted"}


@router.get('/get-join/{id}', status_code=status.HTTP_200_OK)
def get_address_by_user_id(id: int, db: Session = Depends(get_db), user_data: any = Depends(oauth.get_user)):
    join = db.query(Address, User).join(User).filter(Address.user_id == id).all()
    return join
