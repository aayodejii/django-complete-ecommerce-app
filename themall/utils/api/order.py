import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.text import slugify
from django.forms import CharField

from themall.models import Order, OrderDetail, Customer, Product, ProductDetail, Image


def create_order_number():

    ''' this try block retrieves the last order number if there is one so it can generate an order
    number by incrementing the last one on the last one  '''

    try:
        last_order_date = Order.objects.latest('id').date
        last_order_num = str(Order.objects.latest('id').order_num) #last order number
        # remove_id = last_order_num.strftime("%d%m%y")[-6:]
        remove_date = int(last_order_num[:-14]) #this value is what will be incremented

    except ObjectDoesNotExist:
        last_order_date = ''
        last_order_num = ''
        # remove_id = ''
        remove_date = ''

    total_orders = Order.objects.count()  # count total orders

    today = datetime.date.today()  # current time

    ''' this if block is responsible for creating the order number depending on the situation, it basically
    concatenates 'remove date' value to present date and time '''
    time_str = datetime.datetime.now().strftime('%H%M%S')
    date_str = datetime.datetime.now().strftime("%d%m%y")
    
    if total_orders == 0:
        order_num = str(1) + '-' + date_str + '-' + time_str

    elif last_order_date == today:
        order_num = str(1 + remove_date) + '-' + date_str + '-' + time_str


    elif last_order_date < today:
        order_num = str(1) + '-' + date_str + '-' + time_str

    
    return order_num


def create_new_order(request, order_num, user, session_key, date, status, product, quantity, price, offer):

	if user == '':
		new_order = Order(order_num=order_num, session_key=session_key, date=date, status=status)
	else:
		new_order = Order(order_num=order_num, customer=user, session_key=session_key, date=date, status=status)
	new_order.save()

	order_get = Order.objects.get(order_num=order_num)

	create_detail = OrderDetail(order_num=order_get, product=product, quantity=quantity, price=price,
								offer=offer, bill_date=date, ship_date=date)
	create_detail.save()
	messages.info(request, '%s has been added to cart' % product)



def update_cart(request, form):


	""" --- before calling login method ---
		1. check whether user has item(s) in cart
		2. get the current session key, use it as a look up for the order
		3. if cart is !empty: add the user instance(email field to the order)
		3. if cart is !empty and user has some items i: add the user instance(email field to the order)

		3.when you get the order update the email before calling login 
	"""

	session_key = request.session.session_key
	if	Order.objects.filter(session_key=session_key).exists():
		# pow()
		# if Order.objects.get(session_key=session_key).customer is not None:
		anonymous_orders = Order.objects.get(session_key=session_key)
		last_order = Order.objects.filter(customer=form.cleaned_data['email']).last()
		if last_order is not None: #1
			""" if you can't find another useful implementation for this if block, remove #1, & #2
			it will still work that way except you can't tell if the user is new or old customer  """
			if last_order.status == 'still-shopping':
				anonymous_details = OrderDetail.objects.filter(order_num=anonymous_orders.order_num)
				details = OrderDetail.objects.filter(order_num=last_order.order_num)
				for anonymous_order in anonymous_details:
					if Order.objects.filter(orderdetail__order_num=anonymous_order.order_num, orderdetail__product=anonymous_order.product).exists():
						try:
							p = OrderDetail.objects.get(order_num=last_order.order_num, product=anonymous_order.product)
							p.quantity += anonymous_order.quantity
							p.price += anonymous_order.price
							p.save()

							anonymous_order.delete()
						except ObjectDoesNotExist:
					
							anonymous_order.order_num = last_order
							anonymous_order.save()
				anonymous_orders.delete()


			else:
				#old customer
				customer = Customer.objects.get(email=form.cleaned_data['email'])
				anonymous_orders.customer = customer
				anonymous_orders.save()
		else: #2
			# new customer
			customer = Customer.objects.get(email=form.cleaned_data['email'])
			anonymous_orders.customer = customer
			anonymous_orders.save()

