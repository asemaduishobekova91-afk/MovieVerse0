from site_app.database.models import (
    UserProfile,
    Follow,
    Post,
    PostContent,
    City,
    HashTag,
    PostLike,
    ReviewParent,
    Review,
    ReviewLike,
    Chat,
    Person,
    Message


)
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class FollowAdmin(ModelView, model=Follow):
    column_list = [Follow.following_id]

class PostAdmin(ModelView, model=Post):
    column_list = [Post.description]

class PostContentAdmin(ModelView, model=PostContent):
    column_list = [PostContent.content]

class CityAdmin(ModelView, model=City):
    column_list = [City.city_name]

class  HashTagAdmin(ModelView, model=HashTag):
    column_list = [HashTag.hashtag_name]

class PostLikeAdmin(ModelView, model=PostLike):
    column_list = [PostLike.post_id,]

class  ReviewAdmin(ModelView, model=Review):
    column_list = [Review.post_id, Review.comment]

class  ReviewParentAdmin(ModelView, model=ReviewParent):
    column_list = [ReviewParent.review_id]

class ReviewLikeAdmin(ModelView, model=ReviewLike):
    column_list = [ReviewLike.review_id]


class  ChatAdmin(ModelView, model=Chat):
    column_list = [Chat.id]

class  PersonAdmin(ModelView, model=Person):
    column_list = [Person.chat_id]

class  MessageAdmin(ModelView, model=Message):
    column_list = [Message.chat_id,
                   Message.text,
                   Message.image,
                   Message.video]
