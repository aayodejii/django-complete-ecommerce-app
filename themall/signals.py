from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from . models import Product, Order, OrderDetail

""" intially used to update qty from this level.... before i moved to  order level...."""
# @receiver (post_save, sender=OrderDetail)
# def update_total_quantity(sender, instance, created, **kwargs) :
# 	if created:

# 		get_quantity = Product.objects.get(name=instance.product)
# 		total_quantity = get_quantity.quantity

# 		new_quantity = total_quantity - int(instance.quantity)
# 		get_quantity.quantity = new_quantity
# 		get_quantity.save()


# @receiver (post_save, sender=Order)
# def update_quantity(sender, instance,  **kwargs) :
# 	instance.save()
	
	
# @receiver (post_save, sender=OrderDetail)
# def update_quantity(sender, instance,  **kwargs) :
# 	instance.save()


# @receiver (post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs) :
# 	if created:
# 		UserProfile.objects.create(user=instance)


# @receiver (post_save, sender=User)
# def save_profile(sender, instance,  **kwargs) :
# 	instance.profile.save()

def perform_some_action_on_login(sender, user, **kwargs):
	"""
	A signal receiver which performs some actions for
	the user logging in.
	"""
	...
	print('YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')

	# your code here
	
user_logged_in.connect(perform_some_action_on_login)



# @receiver (request, sender)

# def user_logged_in(sender):
#     print('YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')