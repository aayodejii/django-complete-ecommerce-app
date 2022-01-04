from django.test import TestCase


from themall.tests.interface import *

""" 
Test Classes: 
"""

class ProductModelTest(TestCase, ProductInterface):
    
    def setUp(self):
        ProductInterface('Product One').create_product(offer_price=65210)
        ProductInterface('Product Two').create_product(price=5500)

    def test_get_absolute_url(self):
        product = ProductInterface('Product One').get_product()
        self.assertEqual(product.get_absolute_url(),'/product/product-one/')
    
    def test_price_difference_with_offer_price(self):
        product = ProductInterface('Product One').get_product()
        self.assertEqual(product.price_difference(), 4790)
    
    def test_price_difference_with_no_offer_price(self):
        product = ProductInterface('Product Two').get_product()
        self.assertEqual(product.price_difference(), 0)

    def test_set_price_with_offer_price(self):
        product = ProductInterface('Product One').get_product()
        self.assertEqual(product.set_price(product.quantity), 260840)


    def test_set_price_with_no_offer_price(self):
        product = ProductInterface('Product Two').get_product()
        self.assertEqual(product.set_price(product.quantity), 22000)
    
    def test_is_an_offer_expects_true(self):
        product = ProductInterface('Product One').get_product()
        self.assertTrue(product.is_an_offer())

    
    def test_is_an_offer_expects_false(self):
        product = ProductInterface('Product Two').get_product()
        self.assertFalse(product.is_an_offer())


class CustomerModelTest(TestCase, CustomerInterface, ProductInterface, OrderInterface):

    def setUp(self):
        product_1 = ProductInterface('Product One').create_product()
        product_2 = ProductInterface('Product Two').create_product()
        product_3 = ProductInterface('Product Three').create_product()
        product_4 = ProductInterface('Product Four').create_product()

        customer_1 = CustomerInterface.create_customer(email='john-paul@mail.ng', first_name='John')
        customer_2 = CustomerInterface.create_customer(email='james-doe@mail.ng', first_name='James', last_name='Doe', country='Nigeria', city='Akure', address='some where in planet earth', phone='08000000000')

        
        order = OrderInterface.create_order(customer=customer_1)
        
        OrderInterface.create_order_details(order, product_1)
        OrderInterface.create_order_details(order, product_2)
        OrderInterface.create_order_details(order, product_3)
    
	
       
    def test_profile_completed_expects_true(self):
        customer = Customer.objects.get(first_name='James')
        self.assertTrue(customer.profile_completed())
    
    def test_profile_completed_expects_false(self):
        customer = Customer.objects.get(first_name='John')
        self.assertFalse(customer.profile_completed())
 
    
    def test_can_review_expects_true(self):
        product = Product.objects.get(name='Product Three')
        customer = Customer.objects.get(first_name='John')
        self.assertTrue(customer.can_review(product))    
    
    def test_can_review_expects_false(self):
        product = Product.objects.get(name='Product Four')
        customer = Customer.objects.get(first_name='John')
        self.assertFalse(customer.can_review(product))


class OrderModelTest(TestCase, OrderInterface):
    def setUp(self):
        product_1 = ProductInterface('Product One').create_product(price=4000)
        product_2 = ProductInterface('Product Two').create_product(price=9000)
        product_3 = ProductInterface('Product Three').create_product(price=2000)
        product_4 = ProductInterface('Product Four').create_product(price=1000)

        customer = CustomerInterface.create_customer(email='john-paul@mail.ng', first_name='John')
        
        order = OrderInterface.create_order(customer)
        
        OrderInterface.create_order_details(order, product_1, product_1.price)
        OrderInterface.create_order_details(order, product_2, product_2.price)
        OrderInterface.create_order_details(order, product_3, product_3.price)
        OrderInterface.create_order_details(order, product_4, product_4.price)


    def test_get_total_price(self):
        order = OrderInterface.get_order('1-081120-094800')
        self.assertEqual(order.get_total_price(), 16000)

    

# class OrderDetailModelTest:
#     pass

#     def setUp(self):
#         pass

#     def test_most_purchased_product(self):
#         pass