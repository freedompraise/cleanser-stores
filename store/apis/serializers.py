from rest_framework import serializers
from store.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','price','country_of_origin','description','rating')
