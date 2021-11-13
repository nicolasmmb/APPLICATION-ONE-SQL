from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.database.database import Base


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, nullable=False)
    pais = Column(String(64), nullable=False)
    estado = Column(String(64), nullable=False)
    municipio = Column(String(64), nullable=False)
    cep = Column(String(8), nullable=False)
    rua = Column(String(96), nullable=False)
    numero = Column(Integer, nullable=False)
    complemento = Column(String(255), nullable=False)
    # Foreign Keys
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String(96), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    pis = Column(String(11), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

    #TODO: REMOVE
    def __repr__(self):
        return '<Users %r>' % self.nome
    
    
