from modeltranslation.translator import register, TranslationOptions
from .models import Region, City, District, Property


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('region_name',)


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('district_name',)


@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'address', 'documents')
