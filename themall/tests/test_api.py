import datetime

from django.test import TestCase

from themall.utils.api.order import create_order_number
from themall.tests.interface import *

class ApiTest(TestCase):
    def setUp(self):
        customer = CustomerInterface.create_customer(email='john-paul@mail.ng', first_name='John')
        date_str = datetime.date(2020,11,8).strftime('%d%m%y')
        time_str = datetime.time(20,11,8).strftime('%H%M%S')
        order_num = str(1) + '-' + date_str + '-' + time_str
        order = OrderInterface.create_order(customer=customer, order_num='1-081120-201108')
        order2 = OrderInterface.create_order(customer=customer, order_num='2-081120-201208')
     
       
    
    def test_create_order_number_when_last_order_was_in_the_past(self):
        time_str = datetime.datetime.now().strftime('%H%M%S')
        date_str = datetime.datetime.now().strftime('%d%m%y')
        order_num = str(1) + '-' + date_str + '-' + time_str
        self.assertEqual(create_order_number(), order_num)


    
    def test_create_order_number_when_last_order_is_today(self):
        customer = Customer.objects.get(id=1)
        today = datetime.date.today()  # current time

        date_str = datetime.datetime.now().strftime('%d%m%y')
        time_str = datetime.datetime.now().strftime('%H%M%S')
        order_num = str(1) + '-' + date_str + '-' + time_str
        OrderInterface.create_order(customer,today, order_num)
        order_num = str(2) + '-' + date_str + '-' + time_str
        OrderInterface.create_order(customer, today, order_num)
        order_num = str(3) + '-' + date_str + '-' + time_str
        self.assertEqual(create_order_number(), order_num)


    def test_create_order_number_with_no_previous_order(self):
        Order.objects.all().delete()
        time_str = datetime.datetime.now().strftime('%H%M%S')
        date_str = datetime.datetime.now().strftime('%d%m%y')
        order_num = str(1) + '-' + date_str + '-' + time_str
        self.assertEqual(create_order_number(), order_num) 
