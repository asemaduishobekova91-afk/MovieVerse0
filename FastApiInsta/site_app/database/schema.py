from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import date,datetime


class UserProfileInputSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: str | None = None
    age: int | None = None
    user_network: str | None = None

class UserProfileOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
    age: Optional[int]
    user_photo: str
    bio: str
    is_official: bool
    user_network: Optional[str]
    date_registered: date

class UserLoginSchema(BaseModel):
    username: str
    password: str



class FollowInputSchema(BaseModel):
    following_id: int


class FollowOutSchema(BaseModel):
    id: int
    follower_id: int
    following_id: int


class PostInputSchema(BaseModel):
    description: str


class PostOutSchema(BaseModel):
    id: int
    user_id: int
    description: str
    created_date: date

class PostContentInputSchema(BaseModel):
    content: str


class PostContentOutSchema(BaseModel):
    id: int
    content: str



class CityInputSchema(BaseModel):
    city_name: str


class CityOutSchema(BaseModel):
    id: int
    city_name: str
    post_id: int


class HashTagInputSchema(BaseModel):
    hashtag_name: str


class HashTagOutSchema(BaseModel):
    id: int
    hashtag_name: str
    post_id: int


class PostLikeInputSchema(BaseModel):
    post_id: int


class PostLikeOutSchema(BaseModel):
    id: int
    user_id: int
    post_id: int


class ReviewInputSchema(BaseModel):
    post_id: int
    comment: str


class ReviewOutSchema(BaseModel):
    id: int
    user_id: int
    post_id: int
    comment: str
    created_date: date

class ReviewParentInputSchema(BaseModel):
    review_id: int

class ReviewParentOutSchema(BaseModel):
    id: int
    review_id: int


class ReviewLikeInputSchema(BaseModel):
    review_id: int

class ReviewLikeOutSchema(BaseModel):
    id: int
    user_id: int
    review_id: int



class ChatInputSchema(BaseModel):
     pass

class ChatOutSchema(BaseModel):
    id: int


class PersonInputSchema(BaseModel):
    chat_id: int

class PersonOutSchema(BaseModel):
    id: int
    chat_id: int
    username: str

class MessageInputSchema(BaseModel):
    chat_id: int
    text: str
    image: Optional[str]
    video: Optional[str]

class MessageOutSchema(BaseModel):
    id: int
    chat_id: int
    text: str
    image: Optional[str]
    video: Optional[str]
    created_date: date

