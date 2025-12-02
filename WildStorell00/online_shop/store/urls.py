from django.urls import path, include
from .views import (UserProfileViewSet,CategorylistAPIView,CategoryDetailAPIView,
                    SubCategoryListAPIView,SubCategoryDetailAPIView,
                   ProductListAPIView,ProductDetailAPIView,ProductImageViewset,ReviewViewset)

from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'user', UserProfileViewSet)
router.register(r'images', ProductImageViewset)
router.register(r'review', ReviewViewset)

urlpatterns =[
    path('',include(router.urls)),
    path('category/', CategorylistAPIView.as_view(),name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('sub_category/', SubCategoryListAPIView.as_view(), name='sub_category_list'),
    path('sub_category/<int:pk>/',SubCategoryDetailAPIView.as_view(), name='sub_category_detail'),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail')

]