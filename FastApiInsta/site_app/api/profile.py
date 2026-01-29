from fastapi import APIRouter, HTTPException, Depends
from site_app.database.models import UserProfile
from site_app.database.schema import UserProfileInputSchema, UserProfileOutSchema
from site_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

profile_router = APIRouter(prefix='/profile', tags=['Profile'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@profile_router.post('/', response_model=UserProfileOutSchema)
async def create_profile(profile: UserProfileInputSchema, db: Session = Depends(get_db)):
    profile_db = UserProfile(**profile.dict())
    db.add(profile_db)
    db.commit()
    db.refresh(profile_db)
    return profile_db

@profile_router.get('/', response_model=List[UserProfileOutSchema])
async def list_profile(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()

@profile_router.get('/{profile_id}', response_model=UserProfileOutSchema)
async def detail_profile(profile_id: int, db: Session = Depends(get_db)):
    profile_db = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return profile_db

@profile_router.put('/{profile_id}/', response_model=dict)
async def update_profile(profile_id: int, profile: UserProfileInputSchema,
                          db: Session = Depends(get_db)):
    profile_db = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for profile_key, profile_value in profile.dict().items():
        setattr(profile_db, profile_key, profile_value)

    db.commit()
    db.refresh(profile_db)
    return {'message': 'Категори озгорулду'}

@profile_router.delete('/{profile_id}/', response_model=dict)
async def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    profile_db = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(profile_db)
    db.commit()
    return {'message': 'Категори удалить болду'}
