from pydantic import BaseModel,EmailStr
from typing import Optional
from .models import RoleChoices,RoomTypeChoices,RoomStatusChoices
from datetime import date,datetime


class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str]
    age: Optional[int]

class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    role: RoleChoices
    password: str
    phone_number: Optional[str]
    age: Optional[int]
    date_registered: date


class CountryInputSchema(BaseModel):
    country_name: str
    country_image: str
    hotel_id: int

class  CountryOutSchema(BaseModel):
    id: int
    country_name: str
    country_image: str
    hotel_id: int

class HotelInputSchema(BaseModel):
    hotel_name: str
    hotel_stars: int
    street: str
    postal_code: str

class HotelOutSchema(BaseModel):
    id: int
    hotel_name: str
    hotel_stars: int
    street: str
    postal_code: str



class HotelImageInputSchema(BaseModel):
    hotel_image: str
    hotel_id: int

class HotelImageOutSchema(BaseModel):
    id: int
    hotel_image: str
    hotel_id: int



class CityInputSchema(BaseModel):
    city_name: str
    city_image: str
    country_id: int
    hotel_id: int

class CityOutSchema(BaseModel):
    id: int
    city_name: str
    city_image: str
    country_id: int
    hotel_id: int


class RoomInputSchema(BaseModel):
    room_name: str
    room_number: int
    price: float
    room_type: RoomTypeChoices
    room_status: RoomStatusChoices
    description: str
    hotel_id: int


class RoomOutSchema(BaseModel):
    id: int
    room_name: str
    room_number: int
    price: float
    room_type: RoomTypeChoices
    room_status: RoomStatusChoices
    description: str
    hotel_id: int

class RoomImageInputSchema(BaseModel):
    room_id: int
    room_image: str


class RoomImageOutSchema(BaseModel):
    id: int
    room_id: int
    room_image: str


class BookingInputSchema(BaseModel):
    user_id: int
    hotel_id: int
    room_id: int


class BookingOutSchema(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    room_id: int

class ReviewInputSchema(BaseModel):
    user_id: int
    hotel_id: int
    comment: str
    stars: int


class ReviewOutSchema(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    comment: str
    stars: int


