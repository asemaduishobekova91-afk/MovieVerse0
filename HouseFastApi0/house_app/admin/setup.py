from .views import (
    UserProfileAdmin,
    RegionAdmin,
    CityAdmin,
    DistrictAdmin,
    PropertyAdmin,
    ImageAdmin,
    ReviewAdmin,
)
from fastapi import FastAPI
from sqladmin import Admin
from house_app.database.db import engine

def setup_admin(shop_app: FastAPI):
    admin = Admin(shop_app,engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(RegionAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(DistrictAdmin)
    admin.add_view(PropertyAdmin)
    admin.add_view(ImageAdmin)
    admin.add_view(ReviewAdmin)
