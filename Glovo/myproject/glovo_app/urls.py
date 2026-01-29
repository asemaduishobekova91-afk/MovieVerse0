from .views import (UserProfileListAPIView,UserProfileDetailAPIView,CategoryListAPIView,CategoryDetailAPIView,
                    StoreListAPIView,StoreDetailAPIView,
                    OrderViewSet,StoreViewSet,
                    CourierProductViewSet,ReviewCreateAPIView, ReviewEditAPIView,OrderStatusListAPIView,
                    OrderStatusDetailAPIView,RegisterView,LoginView,LogoutView)


from rest_framework import routers
from django.urls import path,include

router = routers.SimpleRouter()

router.register(r'stores', StoreViewSet, basename='store')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'couriers', CourierProductViewSet, basename='courier')




urlpatterns =[
    path('', include(router.urls)),
    path('users/', UserProfileListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('store/', StoreListAPIView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store_detail'),
    path('review/create/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('review/create/<int:pk>/', ReviewEditAPIView.as_view(), name='review_edit'),
    path('order_status/', OrderStatusListAPIView.as_view(), name='order_list'),
    path('order_status/<int:pk>/', OrderStatusDetailAPIView.as_view(), name='order_detail'),

    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', LoginView.as_view(), name='login_list'),
    path('logout/', LogoutView.as_view(), name='logout_list'),
]