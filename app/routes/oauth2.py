from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
###
from app.configs.config import TokenConfig
from app.schemas.schemas import TokenData
from app.database.database import get_db
from app.models.models import User
###
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def create_token(data: dict):
    encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(TokenConfig.get_token_config()['TOKEN_EXPIRE_MINUTES']))
    encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        encode,
        TokenConfig.get_token_config()['SECRET_KEY'],
        algorithm=TokenConfig.get_token_config()['ALGORITHM']
    )
    return encoded_jwt


def decode_token(token: str, exeption):
    try:
        print('>>> TOKEN: ' + token)
        decode = jwt.decode(
            token,
            TokenConfig.get_token_config()['SECRET_KEY'],
            algorithms=TokenConfig.get_token_config()['ALGORITHM']
        )
        user_id = decode.get('user_id')

        if not id:
            raise exeption

        token_data = TokenData(user_id=user_id)

    except JWTError:
        raise exeption

    except AssertionError as a:
        print(a)

    return token_data


def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Unauthorized',
        headers={
            'WWW-Authenticate': 'Bearer',
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    token = decode_token(token, exeption)
    user_id = db.query(User).filter(User.id == token.user_id).first()
    return user_id
