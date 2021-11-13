from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint


class UserCreate(BaseModel):
    nome: str
    email: str
    cpf: str
    pis: str
    senha: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None
    pis: Optional[str] = None
    senha: Optional[str] = None

    class Config:
        orm_mode = True


class UserGet(BaseModel):
    id: int
    nome: str
    email: str
    cpf: str
    pis: str
    senha: str

    class Config:
        orm_mode = True


### ADDRESS ###
class AddressCreate(BaseModel):
    pais: str
    estado: str
    municipio: str
    cep: str
    rua: str
    numero: int
    complemento: str
    user_id: int

    class Config:
        orm_mode = True


class AddressUpdate(BaseModel):
    pais: Optional[str] = None
    estado: Optional[str] = None
    municipio: Optional[str] = None
    cep: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[int] = None
    complemento: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True


class AddressGet(BaseModel):
    id: int
    pais: str
    estado: str
    municipio: str
    cep: str
    rua: str
    numero: int
    complemento: str
    #user_id: Optional[int]

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    cpf: str
    senha: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
    type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    user_id: Optional[str] = None
