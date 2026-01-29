from .views import (
    UserProfileAdmin,
    FollowAdmin,
    PostAdmin,
    PostContentAdmin,
    CityAdmin,
    HashTagAdmin,
    PostLikeAdmin,
    ReviewAdmin,
    ReviewParentAdmin,
    ReviewLikeAdmin,
ChatAdmin,PersonAdmin,
MessageAdmin

)
from fastapi import FastAPI
from sqladmin import Admin
from site_app.database.db import engine

def setup_admin(shop_app: FastAPI):
    admin = Admin(shop_app,engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(FollowAdmin)
    admin.add_view(PostAdmin)
    admin.add_view(PostContentAdmin)
    admin.add_view(CityAdmin)
    admin.add_view( HashTagAdmin)
    admin.add_view(PostLikeAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(ReviewParentAdmin)
    admin.add_view(ReviewLikeAdmin)
    admin.add_view(ChatAdmin)
    admin.add_view(PersonAdmin)
    admin.add_view(MessageAdmin)
