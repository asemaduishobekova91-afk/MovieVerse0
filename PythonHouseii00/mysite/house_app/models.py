from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)

    RoleChoices = (
        ('seller', 'seller'),
        ('buyer', 'buyer')
    )
    role = models.CharField(max_length=20, choices=RoleChoices, default='buyer')
    date_register = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Region(models.Model):
    region_name = models.CharField(max_length=54)

    def __str__(self):
        return self.region_name


class City(models.Model):
    region_name = models.ForeignKey(Region,on_delete=models.CASCADE,related_name='cities' )
    city_name = models.CharField(max_length=32)

    def __str__(self):
        return self.city_name


class District(models.Model):
    district_name = models.CharField(max_length=54)
    city = models.ForeignKey(City, on_delete=models.CASCADE,related_name='districts'  )

    def __str__(self):
        return self.district_name


class Property(models.Model):
    title = models.CharField(max_length=54)
    description = models.TextField()

    PROPERTY_CHOICES = (
        ('Дом', 'Дом'),
        ('Квартира', 'Квартира'),
        ('Коммерческая недвижимость', 'Коммерческая недвижимость'),
        ('Комната', 'Комната'),
        ('Участок', 'Участок'),
        ('Дача', 'Дача'),
    )
    property_type = models.CharField(choices=PROPERTY_CHOICES,max_length=65,default='Дом')
    region_name = models.ForeignKey(Region,on_delete=models.CASCADE,related_name='properties' )
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='properties')
    address = models.CharField(max_length=64)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.PositiveIntegerField(null=True, blank=True)
    rooms = models.PositiveIntegerField()
    floor = models.IntegerField(null=True, blank=True)
    total_floors = models.IntegerField(null=True, blank=True)

    CONDITION_CHOICES = (
        ('под самоотделку', 'под самоотделку'),
        ('евроремонт', 'евроремонт'),
        ('хорошее', 'хорошее'),
        ('среднее', 'среднее'),
        ('не достроено', 'не достроено'),
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=65)
    documents = models.TextField(blank=True)
    seller = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='properties'  )

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    image = models.ImageField(upload_to='property_image/')
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='images')

    def __str__(self):
        return self.property.title


class Review(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='reviews_written' )
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='reviews_received' )
    property = models.ForeignKey(Property,on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField( choices=[(i, str(i)) for i in range(1, 11)],null=True,blank=True)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating}'
