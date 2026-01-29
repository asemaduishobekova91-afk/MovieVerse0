from fastapi import APIRouter, HTTPException, Depends
from site_app.database.models import ReviewParent
from site_app.database.schema import ReviewParentInputSchema, ReviewParentOutSchema
from site_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

review_parent_router = APIRouter(prefix='/review_parent', tags=['Review_parent'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_parent_router.post('/', response_model=ReviewParentOutSchema)
async def create_review_parent(review_parent: ReviewParentInputSchema, db: Session = Depends(get_db)):
    review_parent_db = ReviewParent(**review_parent.dict())
    db.add(review_parent_db)
    db.commit()
    db.refresh(review_parent_db)
    return review_parent_db

@review_parent_router.get('/', response_model=List[ReviewParentOutSchema])
async def list_review_parent(db: Session = Depends(get_db)):
    return db.query(ReviewParent).all()

@review_parent_router.get('/{review_parent_id}', response_model=ReviewParentOutSchema)
async def detail_review_parent(review_parent_id: int, db: Session = Depends(get_db)):
    review_parent_db = db.query(ReviewParent).filter(ReviewParent.id == review_parent_id).first()
    if not review_parent_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return review_parent_db

@review_parent_router.put('/{review_parent_id}/', response_model=dict)
async def update_review_parent(review_parent_id: int, review_parent: ReviewParentInputSchema,
                          db: Session = Depends(get_db)):
    review_parent_db = db.query(ReviewParent).filter(ReviewParent.id == profile_id).first()
    if not review_parent_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for review_parent_key, review_parent_value in review_parent.dict().items():
        setattr(review_parent_db, review_parent_key, review_parent_value)

    db.commit()
    db.refresh(review_parent_db)
    return {'message': 'Категори озгорулду'}

@review_parent_router.delete('/{review_parent_id}/', response_model=dict)
async def delete_review_parent(review_parent_id: int, db: Session = Depends(get_db)):
    review_parent_db = db.query(ReviewParent).filter(ReviewParent.id == review_parent_id).first()
    if not review_parent_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(review_parent_db)
    db.commit()
    return {'message': 'Категори удалить болду'}
