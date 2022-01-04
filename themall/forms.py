from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

# from phonenumber_field.formfields import PhoneNumberField
# from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Product, ProductDetail, Category, Customer, Review
from .validators import validate_phone, validate_name, validate_email




class ManageCategory(ModelForm):
	name = forms.CharField(max_length=50, widget=forms.TextInput(
			attrs = {
				'class' : 'form-control',
				'placeholder' : 'Category',
					
					
			}

	))		
	description = forms.CharField(max_length=500, required=False, widget=forms.Textarea(
			attrs = {
				'class' : 'form-control',
				'placeholder' : 'Description, please try to be explicit',
					
			}

	))	

	class Meta:
		model = Category
		fields = '__all__'

class ManageProduct(ModelForm):
	name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
		attrs = {
			'class' : 'form-control no-radius',
			'placeholder' : 'Product'
		}
	))
	quantity = forms.IntegerField(widget=forms.NumberInput(
		attrs = {
			'class' : 'form-control no-radius',
			'placeholder' : 'Quantity',
			'min' : 0,
		}
	))
	price = forms.IntegerField(widget=forms.NumberInput(
		attrs = {
			'class' : 'form-control no-radius',
			'placeholder' : 'Price'
		}
	))
	percent_off = forms.IntegerField(required=False, widget=forms.NumberInput(
		attrs = {
			'class' : 'form-control  no-radius',
			'placeholder' : 'Percent Off'
		}
	))
	# category = forms.CharField( disabled=True, widget=forms.TextInput(
	# 	attrs = {
	# 		'class' : 'form-control',
	# 		'placeholder' : 'Category'
	# 	}
	# ))	
	# category = forms.ModelChoiceField(queryset=Category.objects.all(), disabled=True, widget=forms.Select(
	# 	attrs = {
	# 		'class' : 'form-control',
	# 		'placeholder' : 'Category'
	# 	}
	# ))
	# seller = forms.ModelChoiceField(queryset=Customer.objects.all(), widget=forms.Select(
	# 	attrs = {
	# 		'class' : 'form-control',
	# 		'placeholder' : 'Seller',
	# 	}
	# ))
	offer_price = forms.IntegerField(required=False, disabled=True, widget=forms.NumberInput(
		attrs = {
			'class' : 'form-control no-radius',
			'placeholder' : 'Offer Price'
		}
	))

	class Meta:
		model = Product
		fields = [
			'name',
			'quantity',
			'price',
			'percent_off',
			'offer_price',
			# 'category',
		]

class ManageProductDetail(ModelForm):
	# product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(
	# 	attrs = {
	# 		'class' : 'form-control',
	# 		'placeholder' : 'Product'
	# 	}
	# ))	
	description = forms.CharField(max_length=150, widget=forms.Textarea(
		attrs = {
			'class' : 'form-control  no-radius',
			'placeholder' : 'Product Details here... please be descriptive as possible'
		}
	))
	brand = forms.CharField(max_length=150, widget=forms.TextInput(
		attrs = {
			'class' : 'form-control no-radius',
			'placeholder' : 'Brand'
		}
	))
	color = forms.CharField(max_length=150, widget=forms.TextInput(
		attrs = {
			'class' : 'form-control no-radius',
			'placeholder' : 'Color'
		}
	))	
	size = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
		attrs = {
			'class' : 'form-control no-radius',
			'placeholder' : 'Size'
		}
	))
	picture = forms.ImageField(widget=forms.FileInput(
		attrs = {
			'class' : 'custom-file-input no-radius',
			'multiple' : True,
		}
	))
	class Meta:
		model = ProductDetail
		fields = [
			# 'product',
			'description',
			'brand', 
			'color',
			'size',
			'picture',

		]


class AddToCart(forms.Form):
	order = forms.CharField(max_length=150, required = False, widget = forms.HiddenInput(
			attrs = {
							
			}
	))	
	quantity = forms.CharField(widget = forms.NumberInput(
			attrs = {
				'min' : 1,
				'max' :100,
				# 'max' : Product.objects.filter(name=initial).count(),
				'class' : 'form-control no-radius',
				'placeholder' : 'Quantity',		
					
			}
	))	

class OrderForm(forms.Form):
	order = forms.CharField(max_length=150, required=False, widget=forms.HiddenInput(
			attrs = {
						
			}
	))	

class DeleteForm(forms.Form):
	remove = forms.CharField(max_length=15, required=False, initial=False, widget=forms.HiddenInput(
			attrs = {
						
			}

	))	
	
class UpdateForm(forms.Form):
	quantity = forms.IntegerField(widget=forms.NumberInput(
			attrs = {
					'id' : 'updateQty',
					'class' : 'form-control-sm update',
					'min' : 1,
					'max-width' : '40px',
					'border' : 0,
					'display' : 'inline-block',
					'size' : 2
			}

	))	
	
class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=120, widget=forms.EmailInput(
		attrs = {
			'placeholder' : 'Email',
			'class' : 'form-control no-radius',

			
			}
	))
	password1 = forms.CharField(max_length=120, widget=forms.PasswordInput(
		attrs = {
			'placeholder' : 'Password',
			'class' : 'form-control no-radius',

			
			}
	))
	password2 = forms.CharField(max_length=120, widget=forms.PasswordInput(
		attrs = {
			'placeholder' : 'Confirm Password',
			'class' : 'form-control no-radius',

			
			}
	))


	class Meta:
		model = Customer
		fields = [
			'email',
			'password1',
			'password2',
		]

class LoginForm(forms.Form):
	email = forms.CharField(widget=forms.TextInput(
			attrs = {
					'class' : 'form-control no-radius' ,
					'placeholder' : 'Email'
			}

	))	
	password = forms.CharField(widget=forms.PasswordInput(
			attrs = {
					'class' : 'form-control no-radius' ,
					'placeholder' : 'Password'
			}

	))


class UpdateInfoForm(ModelForm):
	email = forms.EmailField(validators=[validate_email], widget=forms.TextInput(
			attrs = {
					'class' : 'form-control no-radius',
					'placeholder' : 'Email',
			}

	))
	# phone = PhoneNumberField(required=False, widget=forms.TextInput(
	# 		attrs = {
	# 				'placeholder': 'Phone',
	# 				'class' : 'form-control no-radius',

			
	# 		}
	# ))	
	phone = forms.CharField(max_length=11, validators=[validate_phone], widget=forms.TextInput(
			attrs = {
					'placeholder': 'Phone',
					'class' : 'form-control no-radius',

			
			}
	))	
	first_name = forms.CharField(validators=[validate_name], widget=forms.TextInput(
			attrs = {
					'class' : 'form-control no-radius',
					'placeholder' : 'First Name',
					'autofocus' : True,

			}

	))
	last_name = forms.CharField(validators=[validate_name], widget=forms.TextInput(
			attrs = {
					'class' : 'form-control no-radius',
					'placeholder' : 'Last Name',

			}

	))
	address = forms.CharField(widget=forms.TextInput(
			attrs = {
					'class' : 'form-control no-radius',
					'placeholder' : 'Full Address',

			}

	))
	city = forms.CharField(widget=forms.TextInput(
			attrs = {
					'class' : 'form-control no-radius',
					'placeholder' : 'City',

			}

	))
	country = forms.CharField(widget=forms.TextInput(
			attrs = {
					'class' : 'form-control no-radius',
					'placeholder' : 'Country',
			}

	))

	class Meta:
		model = Customer
		fields = [
			'email',
			'first_name',
			'last_name',
			'phone',
			'city',
			'country',
			'address',
		]

class ReviewForm(ModelForm):
	star = [
		(1, '1 of 5 '),
		(2, '2 of 5 '),
		(3, '3 of 5 '),
		(4, '4 of 5 '),
		(5, '5 of 5 '),
	]
	review = forms.CharField(widget=forms.Textarea(
			attrs = {
					'class' : 'form-control no-radius' ,
					'placeholder' : 'What do you think about this product?'
			}
	
	))	
	rating = forms.ChoiceField(choices=star, widget=forms.Select(
			attrs = {
					'class' : 'form-control no-radius' ,
			}
	
	))

	class Meta:
		model = Review
		fields = [
			'review',
			'rating',
		]


