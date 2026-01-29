from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from .models import RoleCHOICES, TypeChoices, ConditionChoices


class UserProfileInputSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_number: Optional[str]
    avatar: Optional[str]


class UserProfileOutSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    role: RoleCHOICES
    phone_number: Optional[str]
    avatar: Optional[str]
    date_registered: date


class UserLoginSchema(BaseModel):
    username: str
    password: str


class RegionInputSchema(BaseModel):
    region_name: str


class RegionOutSchema(BaseModel):
    id: int
    region_name: str


class CityInputSchema(BaseModel):
    region_id: int
    title: str


class CityOutSchema(BaseModel):
    id: int
    region_id: int
    title: str


class DistrictInputSchema(BaseModel):
    city_id: int
    title: str


class DistrictOutSchema(BaseModel):
    id: int
    city_id: int
    title: str


class PropertyInputSchema(BaseModel):
    title: str
    photo: str
    description: str
    type: TypeChoices

    region_id: int
    city_id: int
    district_id: int

    address: str
    area: int
    price: int
    rooms: int
    floor: int
    total_floors: int

    condition: ConditionChoices
    documents: bool
    seller_id: int


class PropertyOutSchema(BaseModel):
    id: int
    title: str
    photo: str
    description: str
    type: TypeChoices

    region_id: int
    city_id: int
    district_id: int

    address: str
    area: int
    price: int
    rooms: int
    floor: int
    total_floors: int
    condition: ConditionChoices
    documents: bool
    seller_id: int
    crated_date: datetime


class ImageInputSchema(BaseModel):
    image: str
    property_id: int


class ImageOutSchema(BaseModel):
    id: int
    image: str
    property_id: int


class ReviewInputSchema(BaseModel):
    author_id: int
    seller_id: int
    rating: int
    comment: str


class ReviewOutSchema(BaseModel):
    id: int
    author_id: int
    seller_id: int
    rating: int
    comment: str
    created_at: datetime
