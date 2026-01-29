from fastapi import APIRouter, HTTPException, Depends
from house_app.database.models import Region
from house_app.database.schema import RegionInputSchema, RegionOutSchema
from house_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


region_router = APIRouter(prefix='/region', tags=['Region'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@region_router.post('/', response_model=RegionOutSchema)
async def create_region(region: RegionInputSchema, db: Session = Depends(get_db)):
    region_db = Region(**region.model_dump())
    db.add(region_db)
    db.commit()
    db.refresh(region_db)
    return region_db

@region_router.get('/', response_model=List[RegionOutSchema])
async def list_region(db: Session = Depends(get_db)):
     return db.query(Region).all()

@region_router.get('/{region_id}', response_model=RegionOutSchema)
async def detail_region(region_id: int, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)
    return region_db

@region_router.put('/{region_id}', response_model=dict)
async def update_region(region_id: int, region: RegionInputSchema,
                          db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    for region_key, region_value in region.model_dump().items():
        setattr(region_db, region_key, region_value)

    db.commit()
    db.refresh(region_db)
    return {'message': 'Категори озгорулду'}

@region_router.delete('/{region_id}', response_model=dict)
async def delete_region(region_id: int, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(detail="Мындай маалымат жок", status_code=400)

    db.delete(region_db)
    db.commit()
    return {'message': 'Категори озгорулду'}
