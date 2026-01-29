from fastapi import APIRouter, HTTPException, Depends
from house_app.database.models import District
from house_app.database.schema import DistrictInputSchema, DistrictOutSchema
from house_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


district_router = APIRouter(prefix='/district', tags=['District'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@district_router.post('/', response_model=DistrictOutSchema)
async def create_district(
    district: DistrictInputSchema,
    db: Session = Depends(get_db)
):
    district_db = District(**district.model_dump())
    db.add(district_db)
    db.commit()
    db.refresh(district_db)
    return district_db


@district_router.get('/', response_model=List[DistrictOutSchema])
async def list_districts(db: Session = Depends(get_db)):
    return db.query(District).all()


@district_router.get('/{district_id}', response_model=DistrictOutSchema)
async def detail_district(district_id: int, db: Session = Depends(get_db)):
    district_db = db.query(District).filter(District.id == district_id).first()
    if not district_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)
    return district_db


@district_router.put('/{district_id}', response_model=dict)
async def update_district(
    district_id: int,
    district: DistrictInputSchema,
    db: Session = Depends(get_db)
):
    district_db = db.query(District).filter(District.id == district_id).first()
    if not district_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for district_key, district_value in district.model_dump().items():
        setattr(district_db, district_key, district_value)

    db.commit()
    db.refresh(district_db)
    return {'message': 'Район ийгиликтүү жаңыртылды'}


@district_router.delete('/{district_id}', response_model=dict)
async def delete_district(district_id: int, db: Session = Depends(get_db)):
    district_db = db.query(District).filter(District.id == district_id).first()
    if not district_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(district_db)
    db.commit()
    return {'message': 'Район ийгиликтүү өчүрүлдү'}
