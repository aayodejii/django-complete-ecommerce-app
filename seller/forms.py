from django import forms
from django.forms import ModelForm

from .models import Seller


class SellerRegistrationForm(ModelForm):
    store_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs = {
            'class' : 'form-control',
        }
    ))
    description = forms.CharField(max_length=2000, widget=forms.Textarea(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Please describe your store -.....'
        }
    ))


    class Meta:
        model = Seller
        fields = [
            'store_name',
            'description',
        ]