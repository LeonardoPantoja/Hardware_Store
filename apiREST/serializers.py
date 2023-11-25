from rest_framework import serializers
from hardware_store.models import ProductCategory, Product


class ProductCategorySerializers(serializers.ModelSerializer):
    """API serializer for ProductCategory model"""
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
