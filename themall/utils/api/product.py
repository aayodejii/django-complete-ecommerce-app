from django.conf import settings
from django.utils.text import slugify

from themall.models import Image, Product, ProductDetail, OrderDetail


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
		details.save()
		# if settings.SELLER:
		# 	new_product.seller = 
		
		product = Product.objects.get(name=name)
		
		details = ProductDetail(id=product, product=name, brand=brand, description=description, size=size, color=color, picture=picture)
		
		for f in files:
			im = Image(product=product, picture=f)
			product.image_set.add(im, bulk=False)
	
	
	

		print("NEWWWWW PRODUCT")




def most_purchased_product():
	p_list = []
	p_dict = {}
	most_purchased =[]

	try:
		details = OrderDetail.objects.all()
		for order in details:
			p_list.append(str(order.product))


		p_dict = p_dict.fromkeys(p_list,0)
		for item in p_list:
			p_dict.update({item: (p_dict.get(item)+1)})

		
		max_value = max(p_dict.values())
		print("max value " + str(max_value))
		min_value = 2
		# keys = p_dict.key()
		# p_range = max_value - min_value
		
		for key,value in p_dict.items():
			if not value < min_value :
				product = Product.objects.get(name=key)
				most_purchased.append(product)
		return most_purchased
		
	except ValueError:
		return 'No value yet'
		

   
		


def out_of_stock():
	products = Product.objects.filter(quantity=0)
	count = products.count()

	return (count, products)