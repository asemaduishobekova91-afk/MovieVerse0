from .models import Category,Product
from rest_framework import serializers

class CategorySeriaLazer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Category
        fields = ['id','category_name']


class ProductSeriaLazer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'