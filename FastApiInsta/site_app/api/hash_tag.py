from fastapi import APIRouter, HTTPException, Depends
from site_app.database.models import HashTag
from site_app.database.schema import HashTagInputSchema, HashTagOutSchema
from site_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

hash_tag_router = APIRouter(prefix='/hash_tag', tags=['HashTag'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@hash_tag_router.post('/', response_model=HashTagOutSchema)
async def create_hash_tag(hash_tag: HashTagInputSchema, db: Session = Depends(get_db)):
    hash_tag_db = HashTag(**hash_tag.dict())
    db.add(hash_tag_db)
    db.commit()
    db.refresh(hash_tag_db)
    return hash_tag_db

@hash_tag_router.get('/', response_model=List[HashTagOutSchema])
async def list_hash_tag(db: Session = Depends(get_db)):
    return db.query(HashTag).all()

@hash_tag_router.get('/{hash_tag_id}', response_model=HashTagOutSchema)
async def detail_hash_tag(hash_tag_id: int, db: Session = Depends(get_db)):
    hash_tag_db = db.query(HashTag).filter(HashTag.id == hash_tag_id).first()
    if not hash_tag_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return hash_tag_db

@hash_tag_router.put('/{hash_tag_id}/', response_model=dict)
async def update_hash_tag(hash_tag_id: int, hash_tag: HashTagInputSchema,
                          db: Session = Depends(get_db)):
    hash_tag_db = db.query(HashTag).filter(HashTag.id == hash_tag_id).first()
    if not hash_tag_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for hash_tag_key, hash_tag_value in hash_tag.dict().items():
        setattr(hash_tag_db, hash_tag_key, hash_tag_value)

    db.commit()
    db.refresh(hash_tag_db)
    return {'message': 'Категори озгорулду'}

@hash_tag_router.delete('/{hash_tag_id}/', response_model=dict)
async def delete_hash_tag(hash_tag_id: int, db: Session = Depends(get_db)):
    hash_tag_db = db.query(HashTag).filter(HashTag.id == hash_tag_id).first()
    if not hash_tag_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(hash_tag_db)
    db.commit()
    return {'message': 'Категори удалить болду'}
