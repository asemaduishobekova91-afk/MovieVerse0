from fastapi import APIRouter, HTTPException, Depends
from house_app.database.models import UserProfile
from house_app.database.schema import UserProfileInputSchema, UserProfileOutSchema
from house_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


users_router = APIRouter(prefix='/users', tags=['Users'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.post('/', response_model=UserProfileOutSchema)
async def create_users(users: UserProfileInputSchema, db: Session = Depends(get_db)):
    users_db = UserProfile(**users.model_dump())
    db.add(users_db)
    db.commit()
    db.refresh(users_db)
    return users_db

@users_router.get('/', response_model=List[UserProfileOutSchema])
async def list_users(db: Session = Depends(get_db)):
     return db.query(UserProfile).all()

@users_router.get('/{users_id}', response_model=UserProfileOutSchema)
async def detail_users(users_id: int, db: Session = Depends(get_db)):
    users_db = db.query(UserProfile).filter(UserProfile.id == users_id).first()
    if not users_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)
    return users_db

@users_router.put('/{users_id}', response_model=dict)
async def update_users(users_id: int, users: UserProfileInputSchema,
                          db: Session = Depends(get_db)):
    users_db = db.query(UserProfile).filter(UserProfile.id == users_id).first()
    if not users_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for users_key, users_value in users.model_dump().items():
        setattr(users_db, users_key, users_value)

    db.commit()
    db.refresh(users_db)
    return {'message': 'Категори озгорулду'}

@users_router.delete('/{users_id}', response_model=dict)
async def delete_users(users_id: int, db: Session = Depends(get_db)):
    users_db = db.query(UserProfile).filter(UserProfile.id == users_id).first()
    if not users_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(users_db)
    db.commit()
    return {'message': 'Категори озгорулду'}
