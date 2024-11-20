from django_filters import  FilterSet
from .models import *


class StoreFilterSet(FilterSet):
    class Meta:
        model = Store
        fields = {
            'store_name': ['exact'],

        }


class ProductFilterSet(FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name': ['exact'],
            'price': ['gt', 'lt']

        }