from django.core.exceptions import ObjectDoesNotExist

from themall.models import Order, OrderDetail, Customer

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
