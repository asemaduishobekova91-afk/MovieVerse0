from django_filters import FilterSet
from .models import Store,Product

class StoreFilter(FilterSet):
    class Meta:
        model = Store
        fields = {
            'category_name': ['exact']
        }

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'price': ['gt', 'lt']
        }