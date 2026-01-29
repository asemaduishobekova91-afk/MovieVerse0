from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, Date,ForeignKey,Text, DateTime
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date
from datetime import datetime

class RoleChoices(str, PyEnum):
    Client = 'Client'
    Owner = 'Owner'

class RoomTypeChoices(str, PyEnum):
    Люкс = 'Люкс'
    Семейный = 'Семейный'
    Стандарт = 'Стандарт'
    Двухместный = 'Двухместный'


class RoomStatusChoices(str,PyEnum):
    занят = 'занят'
    забронирован = 'забронирован'
    свободен = 'свободен'

class UserProfile(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    phone_number: Mapped[Optional[str]] = mapped_column(String,nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices),default=RoleChoices.Client)
    date_registered: Mapped[date] = mapped_column(Date,default=datetime.today)
    bookings: Mapped[List["Booking"]] = relationship( "Booking", back_populates="user",
                                                    cascade="all, delete-orphan")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user",
                                                   cascade="all, delete-orphan")
    token_user: Mapped[List["RefreshToken"]] = relationship(back_populates="token_user",
                                                            cascade="all, delete-orphan")


    def __str__(self):
        return f'{self.first_name},{self.last_name}'

class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token_user: Mapped[UserProfile] = relationship(UserProfile,back_populates='token_user')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_name: Mapped[str] = mapped_column(String(30))
    country_image: Mapped[str] = mapped_column(String)
    cities: Mapped[List["City"]] = relationship("City", back_populates='country',
                                                cascade='all, delete-orphan')
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    hotel: Mapped["Hotel"] = relationship("Hotel", back_populates='countries')

    def __repr__(self):
        return f"{self.country_name}"

class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_name: Mapped[str] = mapped_column(String(60))
    hotel_stars: Mapped[int] = mapped_column(Integer)
    street: Mapped[str] = mapped_column(String(50))
    postal_code: Mapped[str] = mapped_column(String,nullable=False)
    countries: Mapped[List["Country"]] = relationship("Country", back_populates='hotel',
                                                cascade='all, delete-orphan')
    cities: Mapped[List["City"]] = relationship("City", back_populates='hotel',
                                                cascade='all, delete-orphan')
    hotel_images: Mapped[List["HotelImage"]] = relationship("HotelImage", back_populates='hotel',
                                                cascade='all, delete-orphan')
    rooms: Mapped[List["Room"]] = relationship("Room", back_populates='hotel',
                                                cascade='all, delete-orphan')
    bookings:  Mapped[List["Booking"]] = relationship("Booking", back_populates='hotel',
                                                cascade='all, delete-orphan')
    reviews:  Mapped[List["Review"]] = relationship("Review", back_populates='hotel',
                                                cascade='all, delete-orphan')

class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_name: Mapped[str] = mapped_column(String(30))
    city_image: Mapped[str] = mapped_column(String)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    country: Mapped[Country] = relationship(Country,back_populates='cities')
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    hotel: Mapped[Hotel] = relationship(Hotel, back_populates='cities')


class HotelImage(Base):
    __tablename__ = 'hotel_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_image: Mapped[str] = mapped_column(String)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    hotel: Mapped[Hotel] = relationship(Hotel, back_populates='hotel_images')

class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_name: Mapped[str] = mapped_column(String(50))
    room_number: Mapped[int] = mapped_column(Integer,nullable=False)
    price: Mapped[float] = mapped_column(Integer)
    room_type: Mapped[RoomTypeChoices] = mapped_column(Enum(RoomTypeChoices),default=RoomTypeChoices)
    room_status: Mapped[RoomStatusChoices] = mapped_column(Enum(RoomStatusChoices),default=RoomStatusChoices)
    description: Mapped[str] = mapped_column(Text)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    hotel: Mapped[Hotel] = relationship(Hotel, back_populates='rooms')
    room_images: Mapped[List["RoomImage"]] = relationship("RoomImage", back_populates='room',
                                                cascade='all, delete-orphan')
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates='room',
                                                cascade='all, delete-orphan')

class RoomImage(Base):
    __tablename__ = "room_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    room: Mapped[Room] = relationship(Room, back_populates='room_images')
    room_image: Mapped[str] = mapped_column(String)

class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='bookings')
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    hotel: Mapped[Hotel] = relationship(Hotel, back_populates='bookings')
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    room: Mapped[Room] = relationship(Room, back_populates='bookings')
    check_in: Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class Review(Base):
    __tablename__ = 'review'


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates="reviews")
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    hotel: Mapped[Hotel] = relationship(Hotel, back_populates='reviews')
    comment: Mapped[str] = mapped_column(Text)
    stars: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

