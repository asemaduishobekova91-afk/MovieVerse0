from django_filters import FilterSet
from .models import Property


class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'region_name': ['exact'],
            'city': ['exact'],
            'seller': ['exact'],
            'property_type': ['exact'],
            'condition': ['exact'],
            'price': ['lt', 'gt', 'lte', 'gte'],
            'area': ['lt', 'gt', 'lte', 'gte'],
            'rooms': ['exact', 'gte', 'lte'],
            'floor': ['exact', 'gte', 'lte'],
            'total_floors': ['exact', 'gte', 'lte'],
        }
