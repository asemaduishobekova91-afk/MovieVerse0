from fastapi import APIRouter, HTTPException, Depends
from site_app.database.models import Post
from site_app.database.schema import PostInputSchema, PostOutSchema
from site_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

post_router = APIRouter(prefix='/post', tags=['Post'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@post_router.post('/', response_model= PostOutSchema)
async def create_post(follow: PostInputSchema, db: Session = Depends(get_db)):
    post_db = Post(**follow.dict())
    db.add(post_db)
    db.commit()
    db.refresh(post_db)
    return post_db

@post_router.get('/', response_model=List[PostOutSchema])
async def list_post(db: Session = Depends(get_db)):
    return db.query(Post).all()

@post_router.get('/{post_id}', response_model= PostOutSchema)
async def detail_post(post_id: int, db: Session = Depends(get_db)):
    post_db = db.query(Post).filter(Post.id == post_id).first()
    if not post_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return post_db

@post_router.put('/{post_id}/', response_model=dict)
async def update_post(post_id: int, post: PostInputSchema,
                          db: Session = Depends(get_db)):
    post_db = db.query(Post).filter(Post.id == post_id).first()
    if not post_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for post_key, post_value in post.dict().items():
        setattr(post_db, post_key, post_value)

    db.commit()
    db.refresh(post_db)
    return {'message': 'Категори озгорулду'}

@post_router.delete('/{post_id}/', response_model=dict)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_db = db.query(Post).filter(Post.id == post_id).first()
    if not post_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(post_db)
    db.commit()
    return {'message': 'Категори удалить болду'}
