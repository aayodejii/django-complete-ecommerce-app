from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils.text import slugify

from django.forms import CharField

from .models import Order, OrderDetail, Customer, Product, ProductDetail, Image


def create_or_update_product(add_form, details_form, category, files,  *args, edit=None):
	name = add_form.cleaned_data.get('name')
	price = add_form.cleaned_data.get('price')
	quantity = add_form.cleaned_data.get('quantity')
	percent_off = add_form.cleaned_data.get('percent_off')
	if percent_off is not None:
		amount_off = percent_off / 100 * price
		offer_price = price - amount_off
	else:
		offer_price = None
	
	brand = details_form.cleaned_data.get('brand')
	description = details_form.cleaned_data.get('description')
	color = details_form.cleaned_data.get('color')
	size = details_form.cleaned_data.get('size')
	picture = details_form.cleaned_data.get('picture')
	url = slugify(name)
	
	if edit is not False:
	

		product = args[0]
		product.name = name
		product.price = price
		product.quantity = quantity
		product.offer_price = offer_price
		product.percent_off = percent_off
		product.category = category
		product.url = url
		print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
		product.save()
		# details_form.save() works toooo



		product.productdetail.product = name
		product.productdetail.description = description
		product.productdetail.brand = brand
		product.productdetail.color = color
		product.productdetail.size = size
		# product.productdetail.picture = picture
		product.productdetail.save()
		
		print("EXISTINGGGGGGGGGG PRODUCT")

		# product.productdetail.picture.save('myphoto.jpg', picture, save=True)

		
		
		for f in files:
			im = Image(product=product, picture=f)
			im.save()
			product.image_set.add(im)
			# product.image_set.add(im, bulk=False) works too

			

	else:
		new_product = Product(name=name, price=price, quantity=quantity, percent_off=percent_off,
							offer_price=offer_price, category=category, url=url)
		new_product.save()
		
		product = Product.objects.get(name=name)
		
		details = ProductDetail(id=product, product=name, brand=brand, description=description, size=size, color=color, picture=picture)
		
		for f in files:
			im = Image(product=product, picture=f)
			product.image_set.add(im, bulk=False)
	
	
		details.save()
		print("NEWWWWW PRODUCT")


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




