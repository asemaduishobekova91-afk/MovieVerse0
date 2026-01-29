from .db import Base
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime


class RoleCHOICES(str, PyEnum):
    seller = 'seller'
    buyer = 'buyer'


class UserProfile(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False,)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[RoleCHOICES] = mapped_column(String, Enum(RoleCHOICES), default=RoleCHOICES.buyer)
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_registered: Mapped[date] = mapped_column(Date, default=date.today)

    review_author: Mapped[List['Review']] = relationship( 'Review', back_populates='author',
        foreign_keys='Review.author_id',
        cascade='all, delete-orphan'
    )

    review_seller: Mapped[List['Review']] = relationship('Review',
                                                         back_populates='seller_review',foreign_keys='Review.seller_id',
                                                         cascade='all, delete-orphan'
    )

    pro_seller: Mapped[List['Property']] = relationship(back_populates='seller_pro',
                                                        cascade='all, delete-orphan'
    )

    token_user: Mapped[List['RefreshToken']] = relationship( 'RefreshToken',back_populates='token_user',
                                                             cascade='all, delete-orphan'
    )


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='token_user')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Region(Base):
    __tablename__ = 'region'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region_name: Mapped[str] = mapped_column(String)

    pro_region: Mapped[List['Property']] = relationship(back_populates='region_pro',
                                                        cascade='all, delete-orphan')
    city_region: Mapped[List['City']] = relationship(back_populates='region',
                                                     cascade='all, delete-orphan')


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region_id: Mapped[int] = mapped_column(ForeignKey('region.id'))
    title: Mapped[str] = mapped_column(String(100))

    city_district: Mapped[List['District']] = relationship(back_populates='city',
                                                           cascade='all, delete-orphan')
    region: Mapped[Region] = relationship(Region, back_populates='city_region')
    pro_city: Mapped[List['Property']] = relationship(back_populates='city_pro',
                                                      cascade='all, delete-orphan')

    def str(self):
        return self.title


class District(Base):
    __tablename__ = 'district'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    title: Mapped[str] = mapped_column(String)

    city: Mapped[City] = relationship(City, back_populates='city_district')
    pro_district: Mapped[List['Property']] = relationship(back_populates='district_pro',
                                                          cascade='all, delete-orphan')

    def str(self):
        return self.title


class TypeChoices(str, PyEnum):
    apartments = 'apartments'
    house = 'house'
    plot = 'plot'
    room = 'room'


class ConditionChoices(str, PyEnum):
    Euro = 'Euro'
    good = 'good'
    average = 'average'
    not_completed = 'not completed'


class Property(Base):
    __tablename__ = 'property'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    photo: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    type: Mapped[TypeChoices] = mapped_column(String, Enum(TypeChoices))
    region_id: Mapped[int] = mapped_column(ForeignKey('region.id'))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    district_id: Mapped[int] = mapped_column(ForeignKey('district.id'))
    address: Mapped[str] = mapped_column(String)
    area: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    rooms: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)
    total_floors: Mapped[int] = mapped_column(Integer)
    condition: Mapped[ConditionChoices] = mapped_column(String, Enum(ConditionChoices))
    documents: Mapped[bool] = mapped_column(Boolean, default=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    crated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    region_pro: Mapped[Region] = relationship(Region, back_populates='pro_region')
    city_pro: Mapped[City] = relationship(City, back_populates='pro_city')
    district_pro: Mapped[District] = relationship(District, back_populates='pro_district')

    seller_pro: Mapped[UserProfile] = relationship(UserProfile, back_populates='pro_seller')  # ✅ совпало

    image_pro: Mapped[List['Image']] = relationship('Image', back_populates='property_images',
                                                    cascade='all, delete-orphan')


class Image(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String)
    property_id: Mapped[int] = mapped_column(ForeignKey('property.id'))
    property_images: Mapped[Property] = relationship(Property, back_populates='image_pro')


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    author: Mapped[UserProfile] = relationship(UserProfile, back_populates='review_author', foreign_keys=[author_id])
    seller_review: Mapped[UserProfile] = relationship(UserProfile, back_populates='review_seller', foreign_keys=[seller_id])
