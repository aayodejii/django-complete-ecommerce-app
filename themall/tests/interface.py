from django.utils.text import slugify

from themall.models import Product, Category, Customer, Order, OrderDetail



class ParentInterface:
    class ProductInterface:
        pass   
    class OrderInterface:
        pass   
    class CustomerInterface:
        pass

""" 
Interface Classes: Help to implement certain accessor methods that can be used to perform common operations,
such as creating and retrieving object model instances. 
"""

class ProductInterface:
    """
    Helps to implements a getter and a setter method for working with Product model, it accepts a 
    single argument(name of product).
    """
    def __init__(self, name):
        self.name = name # product name
        self.category, bl = Category.objects.get_or_create(name='Test Category', description='testing...') #product category
    
   
    def create_product(self, price=70000, quantity=4, offer_price=None):
        """
        Creates a Product instance using the supplied keyword argument(s), if non is given the default parameters are used.
        """
        product = Product.objects.create(name=self.name, price=price, quantity=quantity, offer_price=offer_price, category=self.category, url=slugify(self.name))
        
        return product


    def get_product(self): 
        """
        returns the product instance.
        """
        product = Product.objects.get(name=self.name) 
        return product



class CustomerInterface:

    def create_customer(email=None, first_name=None, last_name=None, country=None, city=None, address=None, phone=None):
        """
        Creates a Customer instance, every arguments is 'None' by default, but email is required.
        """
        customer = Customer.objects.create(email=email, first_name=first_name, last_name=last_name, country=country, city=city, address=address, phone=phone)
       
        return customer

        

class OrderInterface:
    """
    Helps to implements accessor methods for working with Order model.
    """
    
    def create_order(customer, date='2020-11-08', order_num='1-081120-094800'):
        """
        creates and returns an order object - 'customer'(must be a customer instance) argument is required, if 'no order_num' is
        given, '1-081120-094800' will be used as the default. Every other parameter is hardcoded.
        """
        order = Order.objects.create(order_num=order_num, customer=customer, date=date, status='paid-order')

        return order
        

    def create_order_details(order_num, product, price=0):
        """
        creates and returns an order detail object - it takes two required arguments:
        'order_num' - must be an order instance.
        'product' - must be a product instance.
        'price' is 0 by default. Every other parameter is hardcoded.
        """
        order_detail = OrderDetail.objects.create(order_num=order_num, product=product, price=price, bill_date='2020-11-08', ship_date='2020-11-08')

        return order_detail

    def get_order(order_num):
        """
        returns an order instance, only one argument(order_num) is required.
        """
        order = Order.objects.get(order_num=order_num)
        return order

