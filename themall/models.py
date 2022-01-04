from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
# from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager

# from seller.models import Seller

# class Store(models.Model):
# 	name = models.CharField(max_length=60,)



class Product(models.Model):
	if settings.SELLER:
		seller = models.ForeignKey('seller.Seller',  on_delete=models.CASCADE, to_field='email')
	
	name = models.CharField(max_length=50, unique=True)
	quantity = models.IntegerField()
	price = models.CharField(max_length=50)
	percent_off =models.IntegerField(blank=True, null=True)
	offer_price = models.IntegerField(blank=True, null=True)
	category = models.ForeignKey('Category', on_delete=models.CASCADE, to_field='name')
	url = models.SlugField()
	# rating = models.ForeignKey('Rating', on_delete=models.CASCADE, to_field='star')
	rating = models.FloatField(default=0, blank=True, null=True)
	rated_times = models.IntegerField(default=0, blank=True, null=True)
	sum_rated = models.IntegerField(default=0, blank=True, null=True)
	link = models.ManyToManyField(
	'Customer',
	through='Review',
	through_fields=('product', 'customer')
	)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		# url = 'product/' + slugify(self.name)
		return "/product/%s/" % self.url
		# return url
		# return reverse('themall.views.product', args=[str(self.name)])

	def price_difference(self):
		if self.offer_price:
			difference = int(self.price) - self.offer_price
		else:
			difference = 0
		return difference

	def set_price(self, quantity):
		if self.offer_price is not None:
			price = int(self.offer_price) * int(quantity)
		else:
			price = int(self.price) * int(quantity)
		
		return price

	def is_an_offer(self):
		if self.offer_price is not None:
			offer = True
		else:
			offer = False
		return offer 


		
class ProductDetail(models.Model):
	id = models.OneToOneField(Product, primary_key=True, on_delete=models.CASCADE, to_field='id', db_column='id')
	product = models.CharField(max_length=200)
	picture = models.ImageField(upload_to='product-images', blank=True, null=True,  default='product-images/bright-bulb-color.jpg', max_length=100)
	description = models.TextField(max_length=250)
	brand = models.CharField(max_length=50)
	size = models.IntegerField()
	color = models.CharField(max_length=20)



	#this approah works for a single image model
	# def save(self, *args, **kwargs):
	# 	try:
	# 		this = ProductDetail.objects.get(id=self.id)
	# 		if this.picture != self.picture:
	# 			this.picture.delete(save=False)
	# 	except:
	# 		pass
	# 	super().save(*args, **kwargs)

	def __str__(self):
		return self.product.__str__()


class Image(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	picture = models.ImageField(upload_to='product-images', default='bright-bulb-color.jpg', max_length=100)
	default = models.BooleanField(default=False)
	

	
		

	def __str__(self):
		return self.product.__str__()

	def default(self):
		return self.images.filter(default=True).first()

class Customer(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email address'), unique=True)
	phone = models.CharField(_('phone'), max_length=11, null=True, blank=False)
	# phone = PhoneNumberField(_('phone'), blank=True, null=True)
	first_name = models.CharField(_('first name'), max_length=35, null=True, blank=False)
	last_name = models.CharField(_('last name'), max_length=35, null=True, blank=False)
	city = models.CharField(_('city'), max_length=50, null=True, blank=False)
	country = models.CharField(_('country'), max_length=30, null=True, blank=False)
	address = models.CharField(_('address'), max_length=180, null=True, blank=False)
	wish_list = models.ManyToManyField(
		Product,
		through='WishList' ,
		through_fields=('customer', 'product')
		)
	# ip_address = models.GenericIPAddressField(_('ip_address'), max_length=18, unique=True)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	is_active = models.BooleanField(_('active'), default=True)
	is_staff = models.BooleanField(_('staff'), default=False)
	if settings.SELLER:
		is_seller = models.BooleanField(_('seller'), default=False)
	# avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['city', 'country']

	class Meta:
		verbose_name = _('customer')
		verbose_name_plural = _('customers')

	def get_full_name(self):
		'''
		Returns the first_name plus the last_name of the Customer, with a space in between.
		'''
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		'''
		Returns the short name of the Customer.
		'''
		return self.first_name

	def send_mail(self, subject, message, from_email=None, **kwargs):
		'''
		Sends an email to the Customer.
		'''
		send_mail(subject, message, from_email, [self.email], **kwargs)

	def profile_completed(self):
		if self.first_name and self.last_name and self.address and self.city and self.country and self.phone != None:
			return True
		else:
			return False

	def can_review(self, product):
		can_review = False
		check =	Product.objects.filter(order__customer=self, order__status='paid-order')
		for item in check:
			if item.name == product.name:
				can_review = True
				return can_review
				# break
		return can_review






class Category(models.Model):
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField(max_length=250)

	class Meta:
		verbose_name = _('category')
		verbose_name_plural = _('categories')


	def __str__(self):
		return self.name


class SubCategory(models.Model):
	pass

class WishList(models.Model):
	customer = models.ForeignKey(Customer, to_field='email', db_column='email', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		# str = '%s wish to buy %s' %(self.customer, self.product)
		return self.product.__str__()

class Review(models.Model):
	customer = models.ForeignKey(Customer, to_field='email', db_column='email', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	review = models.TextField(max_length=300)
	rating = models.FloatField()



	def __str__(self):
		return self.review[:25].__str__() +'...'


class Order(models.Model):
	order_num = models.CharField(unique=True, max_length=20)
	customer = models.ForeignKey(Customer, to_field='email',  null=True, blank=True,  on_delete=models.CASCADE)
	date = models.DateField()
	status = models.CharField(max_length=15)
	session_key = models.CharField(max_length=32)
	link = models.ManyToManyField(
		Product,
		through='OrderDetail' ,
		through_fields=('order_num', 'product')
		)
	
		
	def __str__(self):
		# info = '%s - %s' %(self.order_num, self.customer) 
		return self.order_num.__str__()
	
	def get_total_price(self):
		price = int()
		order = self.order_num
		details = OrderDetail.objects.filter(order_num=order)
		for detail in details:
			price += detail.price
		return price

	



class OrderDetail(models.Model):
	order_num = models.ForeignKey(Order, on_delete=models.CASCADE, to_field='order_num', db_column='order_num')
	product = models.ForeignKey(Product, on_delete=models.CASCADE,  to_field='id', db_column='product')
	quantity = models.IntegerField(default=1)
	price = models.IntegerField()
	offer =models.BooleanField(default=False) #change to FK.. or
	bill_date = models.DateField()
	ship_date = models.DateField()

	def __str__(self):
		return self.order_num.__str__()



	

	
class CustomerSession(models.Model):
	session_key = models.CharField(max_length=37)

	def __str__(self):
		return self.session_key.__str__()
class Person(models.Model):
	SHIRT_SIZES = (
		('S', 'Small'),
		('M', 'Medium'),
		('L', 'Large'),
	)
	name = models.CharField(max_length=60)
	shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

	def __str__(self):
		return self.name

# class Person(models.Model):
# 	name = models.CharField(max_length=50, unique=True)
	
# 	def __str__(self):
# 		return self.name
		
# class Group(models.Model):
# 	name = models.CharField(max_length=128, unique=True)
# 	members = models.ManyToManyField(
# 		Person,
#         through='Membership',
#         through_fields=('group', 'person'),
#     )
# 	def __str__(self):
# 		return self.name
		
# class Membership(models.Model):
# 	group = models.ForeignKey(Group, db_column='group', to_field='name', on_delete=models.CASCADE)
# 	person = models.ForeignKey(Person, db_column='name', to_field='name', on_delete=models.CASCADE)
# 	inviter = models.ForeignKey(Person, db_column='inviter', to_field='name', on_delete=models.CASCADE, related_name="membership_invites",)
# 	invite_reason = models.CharField(max_length=64)

# 	def __str__(self):
# 		return self.person.__str__()



#divider
