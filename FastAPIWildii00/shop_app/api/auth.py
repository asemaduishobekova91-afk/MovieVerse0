from fastapi import APIRouter, HTTPException, Depends
from shop_app.database.db import SessionLocal
from shop_app.database.db import UserProfile
from shop_app.database.schema import UserProfileInputSchema,UserProfileOutSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.util import deprecated

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


@auth_router.post('/register/',response_model=dict)
async def register(user: UserProfileInputSchema, db: Session = Depends(det_db)):
   user_db = db.query(UserProfile).filter(UserProfile.username==user.username).first()
   email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
   if user_db or email_db :
         raise HTTPException(detail='Мындай username же почта бар экен', status_code=400)

   hash_password = get_password_hash(user.password)
   user_data = UserProfile(
       first_name=user.first_name,
       last_name=user.last_name,
       username=user.username,
       email=user.email,
       age=user.age,
       phone_number=user.phone_number,
       password=hash_password

   )
   db.add(user_data)
   db.commit()
   db.refresh(user_data)
   return{'message': "сиз регистрация болдунуз"}

@auth_router.post('/login/',response_model=dict)
