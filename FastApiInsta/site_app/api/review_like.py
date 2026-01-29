from fastapi import APIRouter, HTTPException, Depends
from site_app.database.models import ReviewLike
from site_app.database.schema import ReviewLikeInputSchema, ReviewLikeOutSchema
from site_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

review_like_router = APIRouter(prefix='/review_like', tags=['ReviewLike'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_like_router.post('/', response_model=ReviewLikeOutSchema)
async def create_review_like(review_like: ReviewLikeInputSchema, db: Session = Depends(get_db)):
    review_like_db = ReviewLike(**review_like.dict())
    db.add(review_like_db)
    db.commit()
    db.refresh(review_like_db)
    return review_like_db

@review_like_router.get('/', response_model=List[ReviewLikeOutSchema])
async def list_review_like(db: Session = Depends(get_db)):
    return db.query(ReviewLike).all()

@review_like_router.get('/{review_like_id}', response_model=ReviewLikeOutSchema)
async def detail_review_like(review_like_id: int, db: Session = Depends(get_db)):
    review_like_db = db.query(ReviewLike).filter(ReviewLike.id == review_like_id).first()
    if not review_like_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return review_like_db

@review_like_router.put('/{review_like_id}/', response_model=dict)
async def update_review_like(review_like_id: int, review_like: ReviewLikeInputSchema,
                          db: Session = Depends(get_db)):
    review_like_db = db.query(ReviewLike).filter(ReviewLike.id == review_like_id).first()
    if not review_like_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for review_like_key, review_like_value in review_like.dict().items():
        setattr(review_like_db, review_like_key, review_like_value)

    db.commit()
    db.refresh(review_like_db)
    return {'message': 'Категори озгорулду'}

@review_like_router.delete('/{review_like_id}/', response_model=dict)
async def delete_review_like(review_like_id: int, db: Session = Depends(get_db)):
    review_like_db = db.query(ReviewLike).filter(ReviewLike.id == review_like_id).first()
    if not review_like_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(review_like_db)
    db.commit()
    return {'message': 'Категори удалить болду'}
