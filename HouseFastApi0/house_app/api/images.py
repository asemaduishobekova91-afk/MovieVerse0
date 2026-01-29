from fastapi import APIRouter, HTTPException, Depends
from house_app.database.models import Image
from house_app.database.schema import ImageInputSchema, ImageOutSchema
from house_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


images_router = APIRouter(prefix='/images', tags=['Images'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@images_router.post('/', response_model=ImageOutSchema)
async def create_image(image: ImageInputSchema, db: Session = Depends(get_db)):
    image_db = Image(**image.model_dump())
    db.add(image_db)
    db.commit()
    db.refresh(image_db)
    return image_db


@images_router.get('/', response_model=List[ImageOutSchema])
async def list_images(db: Session = Depends(get_db)):
    return db.query(Image).all()


@images_router.get('/{image_id}', response_model=ImageOutSchema)
async def detail_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(Image).filter(Image.id == image_id).first()
    if not image_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)
    return image_db


@images_router.put('/{image_id}', response_model=dict)
async def update_image(image_id: int, image: ImageInputSchema, db: Session = Depends(get_db)):
    image_db = db.query(Image).filter(Image.id == image_id).first()
    if not image_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for image_key, image_value in image.model_dump().items():
        setattr(image_db, image_key, image_value)

    db.commit()
    db.refresh(image_db)
    return {'message': 'Image ийгиликтүү жаңыртылды'}


@images_router.delete('/{image_id}', response_model=dict)
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(Image).filter(Image.id == image_id).first()
    if not image_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(image_db)
    db.commit()
    return {'message': 'Image ийгиликтүү өчүрүлдү'}
