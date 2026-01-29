from fastapi import APIRouter, HTTPException, Depends
from site_app.database.models import PostLike
from site_app.database.schema import PostLikeInputSchema, PostLikeOutSchema
from site_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

post_like_router = APIRouter(prefix='/post_like', tags=['PostLike'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@post_like_router.post('/', response_model=PostLikeOutSchema)
async def create_post_like(post_like: PostLikeInputSchema, db: Session = Depends(get_db)):
    post_like_db = PostLike(**post_like.dict())
    db.add(post_like_db)
    db.commit()
    db.refresh(post_like_db)
    return post_like_db

@post_like_router.get('/', response_model=List[PostLikeOutSchema])
async def list_post_like(db: Session = Depends(get_db)):
    return db.query(PostLike).all()

@post_like_router.get('/{post_like_id}', response_model=PostLikeOutSchema)
async def detail_post_like(post_like_id: int, db: Session = Depends(get_db)):
    post_like_db = db.query(PostLike).filter(PostLike.id == post_like_id).first()
    if not post_like_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return post_like_db

@post_like_router.put('/{post_like_id}/', response_model=dict)
async def update_post_like(post_like_id: int, post_like: PostLikeInputSchema,
                          db: Session = Depends(get_db)):
    post_like_db = db.query(PostLike).filter(PostLike.id == post_like_id).first()
    if not post_like_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for post_like_key, post_like_value in post_like.dict().items():
        setattr(post_like_db, post_like_key, post_like_value)

    db.commit()
    db.refresh(post_like_db)
    return {'message': 'Категори озгорулду'}

@post_like_router.delete('/{post_like_id}/', response_model=dict)
async def delete_post_like(post_like_id: int, db: Session = Depends(get_db)):
    post_like_db = db.query(PostLike).filter(PostLike.id == post_like_id).first()
    if not post_like_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(post_like_db)
    db.commit()
    return {'message': 'Категори удалить болду'}
