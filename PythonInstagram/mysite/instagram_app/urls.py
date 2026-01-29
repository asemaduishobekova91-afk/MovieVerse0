from django.urls import path, include
from rest_framework import routers
from .views import (UserProfileViewSet, FollowViewSet, CityViewSet,
                    HashTagViewSet, PostContentViewSet,
                    PostLikeViewSet, ReviewViewSet, ReviewLikeViewSet,
                    PostListAPIView, PostDetailAPIView, RegisterView,
                    LogoutView, CustomLoginView, CreatePostAPIView)

router = routers.DefaultRouter()
router.register('users', UserProfileViewSet)
router.register('follow', FollowViewSet)
router.register('city', CityViewSet)
router.register('hashtag', HashTagViewSet)
router.register('post_content', PostContentViewSet)
router.register('post_like', PostLikeViewSet)
router.register('review', ReviewViewSet)
router.register('review_like', ReviewLikeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('post/', PostListAPIView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('create_post', CreatePostAPIView.as_view(), name='create_post')
    ]

