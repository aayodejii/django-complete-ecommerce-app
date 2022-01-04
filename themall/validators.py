from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Customer


def validate_email(value):

        # if Customer.objects.get(email=value).exist()
        # raise ValidationError(_('ooooo'))
  

    return value





def validate_phone(value):
    expected_value = 11
    first_three = ('070', '080', '090', '081')
    if len(value) < expected_value or not value.isnumeric() or not value.startswith(first_three):

        raise ValidationError(_('Please Enter a valid phone number'))
    # if not value.isnumeric():
    #     raise ValidationError(_('Please Enter a valid phone number oooo'))
 
    return value


def validate_name(value):
    if not value.isalpha():
        raise ValidationError(_('Please Enter a valid name'))

