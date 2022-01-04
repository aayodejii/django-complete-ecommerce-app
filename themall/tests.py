from django.test import TestCase

from themall.models import Product, Category


class ProductTest(TestCase):
    name = 'Test Product'

    def set_up(self):
        category = Category(name='Test Category', description='testing')
        category.save()
        # category = Category.objects.create(name='Test Category', description='testing')

        # Product.objects.create(name='Test Product', price=70001, quantity=15, offer_price=65210, category=category, url='test-product')
        p = Product(name=name, price=70001, quantity=15, offer_price=65210, category=category, url='test-product')
        print(p)
        p.save()

    def test_price_difference(self):
        product = Product.objects.get(id=2)
        self.assertEqual(product.price_difference(), 4790)


