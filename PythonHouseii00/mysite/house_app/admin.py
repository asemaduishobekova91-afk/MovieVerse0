from django.contrib import admin
from .models import (UserProfile,Region,City,District,Property,PropertyImage,Review)
from modeltranslation.admin import TranslationAdmin

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'role', 'phone_number')
    list_filter = ('role',)
    search_fields = ('username', 'first_name', 'last_name')



@admin.register(Region)
class RegionAdmin(TranslationAdmin):
    list_display = ('id', 'region_name')
    search_fields = ('region_name',)


@admin.register(City)
class CityAdmin(TranslationAdmin):
    list_display = ('id', 'city_name', 'region_name')
    list_filter = ('region_name',)
    search_fields = ('city_name',)


@admin.register(District)
class DistrictAdmin(TranslationAdmin):
    list_display = ('id', 'district_name', 'city')
    list_filter = ('city',)
    search_fields = ('district_name',)



class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(TranslationAdmin):
    list_display = (
        'id',
        'title',
        'property_type',
        'price',
        'rooms',
        'city',
        'seller'
    )
    list_filter = (
        'property_type',
        'condition',
        'city',
        'region_name'
    )
    search_fields = ('title', 'description', 'address')
    inlines = [PropertyImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'seller', 'property', 'rating', 'created_date')
    list_filter = ('rating', 'created_date')
    search_fields = ('comment',)
