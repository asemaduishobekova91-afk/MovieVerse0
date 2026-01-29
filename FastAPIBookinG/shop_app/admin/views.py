from shop_app.database.models import (
    UserProfile,
    Country,
    Hotel,
    City,
    HotelImage,
    Room,
    RoomImage,
    Booking,
    Review,
)
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class CountryAdmin(ModelView, model=Country):
    column_list = [Country.country_name, Country.country_image]

class HotelAdmin(ModelView, model=Hotel):
    column_list = [Hotel.id, Hotel.hotel_name, Hotel.hotel_stars]

class CityAdmin(ModelView, model=City):
    column_list = [City.id, City.city_name, City.city_image]

class  HotelImageAdmin(ModelView, model= HotelImage):
    column_list = [HotelImage.hotel_image]

class RoomAdmin(ModelView, model=Room):
    column_list = [
        Room.id,
        Room.room_name,
        Room.room_number,
        Room.room_type,
        Room.room_status,
    ]

class  RoomImageAdmin(ModelView, model=RoomImage):
    column_list = [RoomImage.room_image]

class  BookingAdmin(ModelView, model=Booking):
    column_list = [Booking.id]

class  ReviewAdmin(ModelView, model= Review):
    column_list = [
        Review.comment,
        Review.stars,
        Review.created_date,
    ]
