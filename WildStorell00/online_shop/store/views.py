from .serializers import (UserProfileSeriaLizer,CategoryListSeriaLizer,
                          CategoryDetailSeriaLizer,
                          SubCategoryListSeriaLizer, SubCategoryDetailSeriaLizer,ProductlistSeriaLizer,
                          ProductDetailSeriaLizer,

                          ProductImageSeriaLizer,ReviewSeriaLizer,CartSeriaLizer,
                          CartItemSeriaLizer)

from .models import (UserProfile,Categoty,SubCategory,Product,
                     ProductImage,Review,Cart,CartItem)
from  rest_framework import viewsets,generics
from  django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSeriaLizer

class CategorylistAPIView(generics.ListAPIView):
    queryset = Categoty.objects.all()
    serializer_class = CategoryListSeriaLizer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Categoty.objects.all()
    serializer_class = CategoryDetailSeriaLizer

class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryListSeriaLizer

class SubCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryDetailSeriaLizer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductlistSeriaLizer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = [' product_name']
    ordering_fields = [' price',' created_date']

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSeriaLizer

class ProductImageViewset(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class =ProductImageSeriaLizer


class ReviewViewset(viewsets.ModelViewSet):
    queryset =Review .objects.all()
    serializer_class = ReviewSeriaLizer