from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Date, ForeignKey, Text,DateTime
from datetime import date,datetime
from typing import List, Optional


class UserProfile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[Optional[str]] = mapped_column(nullable=True)
    age: Mapped[Optional[int]] = mapped_column(nullable=True)
    user_photo: Mapped[Optional[str]] = mapped_column(nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    is_official: Mapped[bool] = mapped_column(Boolean, default=False)
    user_network: Mapped[Optional[str]] = mapped_column(nullable=True)
    date_registered: Mapped[date] = mapped_column(Date, default=date.today)

    post = relationship("Post", back_populates="author")
    reviews = relationship("Review", back_populates="author")
    post_likes = relationship("PostLike", back_populates="user")
    review_likes = relationship("ReviewLike", back_populates="user")
    token_user: Mapped[List["RefreshToken"]] = relationship(back_populates="token_user",
                                                            cascade="all, delete-orphan")

class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    token_user: Mapped[UserProfile] = relationship(UserProfile,back_populates='token_user')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)



class Follow(Base):
    __tablename__ = 'follow'

    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    following_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))


class Post(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    description: Mapped[str] = mapped_column(Text)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    author = relationship("UserProfile", back_populates="post")
    cities = relationship("City", back_populates="post", cascade="all, delete-orphan")
    hashtags = relationship("HashTag", back_populates="post", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="post")
    likes = relationship("PostLike", back_populates="post")
    contents = relationship("PostContent", back_populates="post")
class PostContent(Base):
    __tablename__ = 'post_content'

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    content: Mapped[Optional[str]] = mapped_column(nullable=True)

    post = relationship("Post", back_populates="contents")


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    city_name: Mapped[str] = mapped_column(String(30))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    post = relationship("Post", back_populates="cities")


class HashTag(Base):
    __tablename__ = 'hash_tag'

    id: Mapped[int] = mapped_column(primary_key=True)
    hashtag_name: Mapped[str] = mapped_column(String(30))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    post = relationship("Post", back_populates="hashtags")



class PostLike(Base):
    __tablename__ = 'post_like'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    user = relationship("UserProfile", back_populates="post_likes")
    post = relationship("Post", back_populates="likes")


class ReviewParent(Base):
    __tablename__ = 'review_parent'

    id: Mapped[int] = mapped_column(primary_key=True)
    review_id: Mapped[int] = mapped_column(ForeignKey('review.id'))

    review = relationship("Review", back_populates="parents")

class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    comment: Mapped[str] = mapped_column(Text)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    post = relationship("Post", back_populates="reviews")
    author = relationship("UserProfile", back_populates="reviews")

    likes = relationship(
        "ReviewLike",
        back_populates="review",
        cascade="all, delete-orphan"
    )
    parents = relationship("ReviewParent", back_populates="review", cascade="all, delete-orphan")

class ReviewLike(Base):
    __tablename__ = 'review_like'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    review_id: Mapped[int] = mapped_column(ForeignKey('review.id'))

    user = relationship("UserProfile", back_populates="review_likes")
    review = relationship("Review", back_populates="likes")


class Chat(Base):
    __tablename__ = 'chat'

    id: Mapped[int] = mapped_column(primary_key=True)

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    persons = relationship("Person", back_populates="chat", cascade="all, delete-orphan")


class Person(Base):
    __tablename__ = 'person'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chat.id'))
    username: Mapped[str] = mapped_column(String(50), unique=True)

    chat = relationship("Chat", back_populates="persons")


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chat.id'))
    text: Mapped[str] = mapped_column(Text)
    image: Mapped[Optional[str]] = mapped_column(nullable=True)
    video: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    chat = relationship("Chat", back_populates="messages")
