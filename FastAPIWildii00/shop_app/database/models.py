from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, Text, Boolean, DateTime
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date
from datetime import datetime

class StatusChoices(str,PyEnum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'


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
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.simple)
    date_registered: Mapped[date] = mapped_column(Date,default=datetime.today)
    reviews: Mapped[List["Review"]] = relationship( "Review", back_populates="user",
                                                    cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    category_image: Mapped[str] = mapped_column(String)
    category_name: Mapped[str] = mapped_column(String(20), unique=True)
    subcategories: Mapped[List["SubCategory"]] = relationship('SubCategory', back_populates='category',
                                                              cascade='all, delete-orphan')


class SubCategory(Base):
    __tablename__ = 'subcategory'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sub_category_name: Mapped[str] = mapped_column(String(50))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(Category,back_populates='subcategories')
    products: Mapped[List["Product"]] = relationship("Product",
                                                     cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey('subcategory.id'))
    subcategory: Mapped[SubCategory] = relationship(SubCategory, back_populates ="products")
    product_name: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Integer)
    article_number: Mapped[int] = mapped_column(Integer, unique=True)
    description: Mapped[str] = mapped_column(Text)
    video : Mapped[Optional[str]] = mapped_column(String, nullable=True)
    product_type: Mapped[bool] = mapped_column(Boolean)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)
    images: Mapped[List['ProductImage']] = relationship("ProductImage",
                                                      cascade="all, delete-orphan")
    product_reviews: Mapped[List['Review']] = relationship(back_populates='product_class',)


class ProductImage(Base):
    __tablename__ = 'product_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped[Product] = relationship(Product, back_populates ="images")


class Review(Base):
    __tablename__ = 'review'


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates="reviews")
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product_class: Mapped[Product] = relationship(Product, back_populates ="product_reviews")
    comment: Mapped[str] = mapped_column(Text)
    stars: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(Date, default=datetime.utcnow)


