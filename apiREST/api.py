from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from hardware_store.models import ProductCategory, Product
from .serializers import ProductCategorySerializers, ProductSerializers


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductCategorySerializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializers