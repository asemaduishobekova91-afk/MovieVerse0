from .models import (UserProfile,Categoty,SubCategory,Product,
                     ProductImage,Review,Cart,CartItem
                     )

from rest_framework import serializers

class UserProfileSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CategoryListSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = Categoty
        fields =['id', 'category_image','category_name']

class SubCategoryListSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [ 'id', 'sub_category_name' ]

class CategoryDetailSeriaLizer(serializers.ModelSerializer):
    sub_categories = SubCategoryListSeriaLizer(many=True, read_only=True)

    class Meta:
        model = Categoty
        fields = ['category_name','sub_categories']

class ProductImageSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductlistSeriaLizer(serializers.ModelSerializer):
    product_images = ProductImageSeriaLizer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'subcategory', 'product_name', 'price','product_images']



class SubCategoryDetailSeriaLizer(serializers.ModelSerializer):
    products = ProductlistSeriaLizer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['sub_category_name', 'products']

class ProductDetailSeriaLizer(serializers.ModelSerializer):
    product_images = ProductImageSeriaLizer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['product_name', 'subcategory','price','product_images','video','article_number',
                  'description', 'created_date']


class  ReviewSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CartSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'