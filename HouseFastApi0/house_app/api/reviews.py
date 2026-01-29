from fastapi import APIRouter, HTTPException, Depends
from house_app.database.models import Review
from house_app.database.schema import ReviewInputSchema, ReviewOutSchema
from house_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


reviews_router = APIRouter(prefix='/reviews', tags=['Reviews'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@reviews_router.post('/', response_model=ReviewOutSchema)
async def create_review(review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.model_dump())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@reviews_router.get('/', response_model=List[ReviewOutSchema])
async def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@reviews_router.get('/{review_id}', response_model=ReviewOutSchema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)
    return review_db


@reviews_router.put('/{review_id}', response_model=dict)
async def update_review(review_id: int, review: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for review_key, review_value in review.model_dump().items():
        setattr(review_db, review_key, review_value)

    db.commit()
    db.refresh(review_db)
    return {'message': 'Review ийгиликтүү жаңыртылды'}


@reviews_router.delete('/{review_id}', response_model=dict)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(review_db)
    db.commit()
    return {'message': 'Review ийгиликтүү өчүрүлдү'}
