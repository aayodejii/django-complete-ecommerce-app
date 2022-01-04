from django.db import models
# from themall.models import Customer

# Create your models here.




class Seller(models.Model):
	email = models.OneToOneField('themall.Customer', on_delete=models.CASCADE, to_field='email') 
	store_name = models.CharField(max_length=100) 
	slug = models.SlugField(max_length=100) 
	description = models.TextField(max_length=1000)

	def __str__(self):
		return self.email.__str__()