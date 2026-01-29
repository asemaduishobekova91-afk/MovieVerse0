from fastapi import APIRouter, HTTPException, Depends
from site_app.database.models import Person
from site_app.database.schema import PersonInputSchema, PersonOutSchema
from site_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

person_router = APIRouter(prefix='/person', tags=['Person'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@person_router.post('/', response_model=PersonOutSchema)
async def create_person(person: PersonInputSchema, db: Session = Depends(get_db)):
    person_db = Person(**person.dict())
    db.add(person_db)
    db.commit()
    db.refresh(person_db)
    return person_db

@person_router.get('/', response_model=List[PersonOutSchema])
async def list_person(db: Session = Depends(get_db)):
    return db.query(Person).all()

@person_router.get('/{person_id}', response_model=PersonOutSchema)
async def detail_person(person_id: int, db: Session = Depends(get_db)):
    person_db = db.query(Person).filter(Person.id == person_id).first()
    if not person_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return person_db

@person_router.put('/{person_id}/', response_model=dict)
async def update_person(person_id: int, person: PersonInputSchema,
                          db: Session = Depends(get_db)):
    person_db = db.query(Person).filter(Person.id == person_id).first()
    if not person_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for person_key, person_value in person.dict().items():
        setattr(person_db, person_key, person_value)

    db.commit()
    db.refresh(person_db)
    return {'message': 'Категори озгорулду'}

@person_router.delete('/{person_id}/', response_model=dict)
async def delete_person(person_id: int, db: Session = Depends(get_db)):
    person_db = db.query(Person).filter(Person.id == person_id).first()
    if not person_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(person_db)
    db.commit()
    return {'message': 'Категори удалить болду'}
