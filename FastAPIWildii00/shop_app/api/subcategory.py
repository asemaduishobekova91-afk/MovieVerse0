from fastapi import APIRouter, HTTPException, Depends
from database.models import SubCategory
from database.schema import SubCategoryInputSchema,SubCategoryOutSchema
from database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

subcategory_router = APIRouter(prefix='/subcategory', tags=['SubCategory'])

async def det_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@subcategory_router.post('/',response_model=SubCategoryOutSchema)
async def create_subcategory(subcategory: SubCategoryInputSchema, db: Session = Depends(det_db)):
    subcategory_db = SubCategory(**subcategory.dict())
    db.add(subcategory_db)
    db.commit()
    db.refresh(subcategory_db)
    return subcategory_db

@subcategory_router.get('/',response_model=List[SubCategoryOutSchema])
async def list_subcategory(db: Session = Depends(det_db)):
    return db.query(SubCategory).all()

@subcategory_router.get('/{subcategory_id}',response_model=SubCategoryOutSchema)
async def detail_subcategory(subcategory_id: int ,db: Session = Depends(det_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id==subcategory_id).first()
    if not subcategory_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return subcategory_db

