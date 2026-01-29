from fastapi import APIRouter, HTTPException, Depends
from site_app.database.db import SessionLocal
from site_app.database.models import UserProfile, RefreshToken
from site_app.database.schema import UserProfileInputSchema,UserProfileOutSchema,UserLoginSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from site_app.config import (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_LIFETIME,
                             REFRESH_TOKEN_LIFETIME)
from datetime import timedelta, datetime
from jose import jwt
from typing import Optional


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')
auth_router = APIRouter(prefix='/auth', tags=['Auth'])

async def det_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow()+ timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_LIFETIME)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@auth_router.post('/register/',response_model=dict)
async def register(profile: UserProfileInputSchema, db: Session = Depends(det_db)):
   profile_db = db.query(UserProfile).filter(UserProfile.username==profile.username).first()
   email_db = db.query(UserProfile).filter(UserProfile.email == profile.email).first()
   if profile_db or email_db :
         raise HTTPException(detail='Мындай username же почта бар экен', status_code=400)

   hash_password = get_password_hash(profile.password)
   profile_data = UserProfile(
       first_name=profile.first_name,
       last_name=profile.last_name,
       username=profile.username,
       email=profile.email,
       age=profile.age,
       phone_number=profile.phone_number,
       password=hash_password

   )
   db.add(profile_data)
   db.commit()
   db.refresh(profile_data)
   return{'message': "сиз регистрация болдунуз"}

@auth_router.post("/login", response_model=dict)
async def login(profile: UserLoginSchema, db: Session = Depends(det_db)):
    profile_db = db.query(UserProfile).filter(UserProfile.username == profile.username).first()
    if not profile_db or not verify_password(profile.password, profile_db.password):
        raise HTTPException(detail='Сиз жазган маалымат туура эмеc', status_code=400)

    access_token = create_access_token({"sub": profile_db.username})
    refresh_token = create_refresh_token({"sub": profile_db.username})

    token_db = RefreshToken(user_id=profile_db.id, token=refresh_token)
    db.add = (token_db)
    db.commit()



    return {'access_token': access_token, 'refresh_token': refresh_token, "token_type": "Bearer"}


@auth_router.post("/logout")
async def logout(refresh_token: str , db: Session = Depends(det_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail='Маалымат туура эмеc')

    db.delete(stored_token)
    db.commit()

    return {'message': "Вышли"}

@auth_router.post("/refresh")
async def logout(refresh_token: str , db: Session = Depends(det_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail='Маалымат туура эмеc')


    access_token = create_access_token({"sub": stored_token.id})
    return {'access_token': access_token, "token_type": "Bearer"}