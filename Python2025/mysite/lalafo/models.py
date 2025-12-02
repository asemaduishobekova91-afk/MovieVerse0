from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True)

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    phone_number = PhoneNumberField()
    descrioption = models.TextField
    product_type = models.BooleanField
    created_date = models.DateTimeField(auto_now_add=True)


