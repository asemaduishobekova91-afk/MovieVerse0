from fastapi import APIRouter, HTTPException, Depends
from shop_app.database.models import HotelImage
from shop_app.database.schema import HotelImageInputSchema, HotelImageOutSchema
from shop_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


hotel_image_router = APIRouter(prefix='/hotel_image', tags=['hotel_image'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@hotel_image_router.post('/', response_model=HotelImageOutSchema)
async def create_hotel_image(hotel_image: HotelImageInputSchema, db: Session = Depends(get_db)):
    hotel_image_db = HotelImage(**hotel_image.dict())
    db.add(hotel_image_db)
    db.commit()
    db.refresh(hotel_image_db)
    return hotel_image_db

@hotel_image_router.get('/', response_model=List[HotelImageOutSchema])
async def list_hotel_image(db: Session = Depends(get_db)):
     return db.query(HotelImage).all()

@hotel_image_router.get('/{hotel_image_id}', response_model=HotelImageOutSchema)
async def detail_hotel_image(hotel_image_id: int, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)
    return hotel_image_db

@hotel_image_router.put('/{hotel_image_id}', response_model=dict)
async def update_hotel_image(hotel_image_id: int, hotel_image: HotelImageInputSchema,
                          db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for hotel_image_key, hotel_image_value in hotel_image.dict().items():
        setattr(hotel_image_db, hotel_image_key, hotel_image_value)

    db.commit()
    db.refresh(hotel_image_db)
    return {'message': 'Категори озгорулду'}

@hotel_image_router.delete('/{hotel_image_id}', response_model=dict)
async def delete_hotel_image(hotel_image_id: int, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(hotel_image_db)
    db.commit()
    return {'message': 'Категори озгорулду'}