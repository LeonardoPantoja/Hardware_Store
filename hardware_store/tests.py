from django.test import TestCase
from .models import Product, ProductCategory

# Create your tests here.


def create_category(name: str, description: str) -> ProductCategory:
    return ProductCategory.objects.create(name=name, description=description)


def create_product(name: str, image: str, stock: int,
                   price: float, category: ProductCategory) -> Product:

    return Product.objects.create(name=name, image=image, stock=stock, price=price, category_id=category)


class ProductTest(TestCase):
    """"""

    def test_is_avalible_with_stock(self):
        """"""
        category = create_category('is_avalible_with_stock', 'test_category')
        product = create_product(
            'has_stock', 'test_image', 10, 100.27, category)
        self.assertIs(product.is_availible(), True)

    def test_is_avalible_with_no_stock(self):
        """"""
        category = create_category(
            'is_avalible_with_no_stock', 'test_category')
        product = create_product(
            'has_no_stock', 'test_image', 0, 100.27, category)
        self.assertIs(product.is_availible(), False)

    def test_is_avalible_with_negative_stock(self):
        """"""
        category = create_category(
            'is_avalible_with_negative_stock', 'test_category')
        product = create_product('has_negative_stock',
                                 'test_image', -8, 100.27, category)
        self.assertIs(product.is_availible(), False)
