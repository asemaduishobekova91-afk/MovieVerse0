from .views import (
    UserProfileAdmin,
    CountryAdmin,
    HotelAdmin,
    CityAdmin,
    HotelImageAdmin,
    RoomAdmin,
    RoomImageAdmin,
    BookingAdmin,
    ReviewAdmin,
)
from fastapi import FastAPI
from sqladmin import Admin
from shop_app.database.db import engine

def setup_admin(shop_app: FastAPI):
    admin = Admin(shop_app,engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CountryAdmin)
    admin.add_view(HotelAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(HotelImageAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(RoomImageAdmin)
    admin.add_view(BookingAdmin)
    admin.add_view(ReviewAdmin)
