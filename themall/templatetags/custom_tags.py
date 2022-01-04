from django import template
from django.core.exceptions import ObjectDoesNotExist
 
from themall.models import Order, OrderDetail

register = template.Library()


""" this filter works except on Anonymous users, the tag below is a better version """
# @register.filter(name='cart_item')
# def cart_item(user):
# 	item = 0

# 	try:
# 		order = Order.objects.get(customer=user, status ='still-shopping').order_num

# 	# total_orders = OrderDetail.objects.filter(order_num=order).count()
# 		total_orders = OrderDetail.objects.filter(order_num=order)
# 		for order in total_orders:
			
# 			quantity = order.quantity
# 			item = quantity + item

# 	except ObjectDoesNotExist:
# 		item = 0
# 	# return total_orders
# 	return item


# @register.simple_tag
# def rating(product, star)



@register.simple_tag 
def cart_item(key, user): 
	item = 0
	try:
		order = Order.objects.get(customer=user, status ='still-shopping').order_num
	except (ObjectDoesNotExist, TypeError):
		try:
			order = Order.objects.get(session_key=key, status ='still-shopping').order_num
		except ObjectDoesNotExist:
			item = 0
			order = None
	if order is not None:
		total_orders = OrderDetail.objects.filter(order_num=order)
		for order in total_orders:	
			quantity = order.quantity
			item = quantity + item
	
	return item


@register.simple_tag 
def ip_user(ip): 
	try:
		# user = 'jesse_darrell@yahoo.com'
		# user = request.user.get_username()
		use = Customer.objects.get(ip_address=ip)

	except ObjectDoesNotExist:
		use = ''
	return use

	