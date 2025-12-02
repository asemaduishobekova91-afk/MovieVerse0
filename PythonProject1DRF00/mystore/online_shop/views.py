from .models import Category,Product
from .serializers import CategorySeriaLazer,ProductSeriaLazer
from rest_framework import viewsets

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class =CategorySeriaLazer

class ProductViewSet(viewsets.ModelViewSet):
    queryset =Product.objects.all()
    serializer_class = ProductSeriaLazer
    