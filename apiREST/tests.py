from django.test import TestCase
from rest_framework import serializers
from .serializers import ProductCategorySerializers, ProductSerializers
from hardware_store.models import ProductCategory, Product


class TestProductCategorySerializers(TestCase):

    def setUp(self):
        self.category_data = {
            'name': 'Electronics',
            'description': 'A category for electronic products'
        }

    def test_valid_serialization(self):
        serializer = ProductCategorySerializers(data=self.category_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, self.category_data)

    def test_invalid_serialization(self):
        self.category_data['name'] = ''
        serializer = ProductCategorySerializers(data=self.category_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

        
class TestProductSerializers(TestCase):

    def setUp(self):
        self.category = ProductCategory.objects.create(name='Electronics', description='A category for electronic products')
        self.product_data = {
            'name': 'iPhone 12',
            'description': 'A powerful smartphone from Apple',
            'price': 999.99,
            'image': 'Test image',
            'category': self.category.id
        }

    # def test_valid_serialization(self):
    #     serializer = ProductSerializers(data=self.product_data)
    #     self.assertTrue(serializer.is_valid())
    #     self.assertEqual(serializer.validated_data, self.product_data)

    def test_invalid_serialization(self):
        self.product_data['name'] = ''
        serializer = ProductSerializers(data=self.product_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
