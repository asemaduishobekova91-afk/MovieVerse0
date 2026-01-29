from fastapi import APIRouter, HTTPException, Depends
from site_app.database.models import PostContent
from site_app.database.schema import PostContentInputSchema, PostContentOutSchema
from site_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

post_content_router = APIRouter(prefix='/post_content', tags=['PostContent'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@post_content_router.post('/', response_model=PostContentOutSchema)
async def create_post_content(profile: PostContentInputSchema, db: Session = Depends(get_db)):
    post_content_db = PostContent(**profile.dict())
    db.add(post_content_db)
    db.commit()
    db.refresh(post_content_db)
    return post_content_db

@post_content_router.get('/', response_model=List[PostContentOutSchema])
async def list_post_content(db: Session = Depends(get_db)):
    return db.query(PostContent).all()

@post_content_router.get('/{post_content_id}', response_model=PostContentOutSchema)
async def detail_post_content(post_content_id: int, db: Session = Depends(get_db)):
    post_content_db = db.query(PostContent).filter(PostContent.id == post_content_id).first()
    if not post_content_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return post_content_db

@post_content_router.put('/{post_content_id}/', response_model=dict)
async def update_post_content(post_content_id: int, post_content: PostContentInputSchema,
                          db: Session = Depends(get_db)):
    post_content_db = db.query(PostContent).filter(PostContent.id == post_content_id).first()
    if not post_content_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for post_content_key, post_content_value in post_content.dict().items():
        setattr(post_content_db, post_content_key, post_content_value)

    db.commit()
    db.refresh(post_content_db)
    return {'message': 'Категори озгорулду'}

@post_content_router.delete('/{post_content_id}/', response_model=dict)
async def delete_post_content(profile_id: int, db: Session = Depends(get_db)):
    post_content_db = db.query(PostContent).filter(PostContent.id == profile_id).first()
    if not post_content_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(post_content_db)
    db.commit()
    return {'message': 'Категори удалить болду'}
