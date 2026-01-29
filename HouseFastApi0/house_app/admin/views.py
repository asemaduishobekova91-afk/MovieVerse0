from house_app.database.models import (
    UserProfile,
    Region,
    City,
    District,
    Property,
    Image,
    Review,
)
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class RegionAdmin(ModelView, model=Region):
    column_list = [Region.region_name]


class CityAdmin(ModelView, model=City):
    column_list = [City.id, City.title]


class DistrictAdmin(ModelView, model=District):
    column_list = [District.id]


class PropertyAdmin(ModelView, model=Property):
    column_list = [
        Property.id,
        Property.title,
        Property.photo,
        Property.type,
    ]


class ImageAdmin(ModelView, model=Image):
    column_list = [Image.image]


class ReviewAdmin(ModelView, model=Review):
    column_list = [
        Review.comment,
        Review.rating,
        Review.created_at
    ]
