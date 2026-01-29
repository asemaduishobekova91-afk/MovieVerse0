from fastapi import APIRouter, HTTPException, Depends
from shop_app.database.models import Room
from shop_app.database.schema import  RoomInputSchema, RoomOutSchema
from shop_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


room_router = APIRouter(prefix='/room', tags=['room'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@room_router.post('/', response_model=RoomOutSchema)
async def create_room(room: RoomInputSchema, db: Session = Depends(get_db)):
    room_db = Room(**room.dict())
    db.add(room_db)
    db.commit()
    db.refresh(room_db)
    return room_db

@room_router.get('/', response_model=List[RoomOutSchema])
async def list_room(db: Session = Depends(get_db)):
     return db.query(Room).all()

@room_router.get('/{room_id}', response_model=RoomOutSchema)
async def detail_room(room_id: int, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)
    return room_db

@room_router.put('/{room_id}', response_model=dict)
async def update_room(room_id: int, room: RoomInputSchema,
                          db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for room_key, room_value in room.dict().items():
        setattr(room_db, room_key, room_value)

    db.commit()
    db.refresh(room_db)
    return {'message': 'Категори озгорулду'}

@room_router.delete('/{room_id}', response_model=dict)
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    room_db = db.query(Room).filter(Room.id == room_id).first()
    if not room_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(room_db)
    db.commit()
    return {'message': 'Категори озгорулду'}