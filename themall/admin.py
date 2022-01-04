from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from . models import Category, Product, ProductDetail, Order, OrderDetail, Customer, Person, WishList, Review #Seller
from . forms import SignUpForm, UpdateInfoForm

from seller.models import Seller



class CustomerAdmin(UserAdmin):
    add_form = SignUpForm
    form = UpdateInfoForm
    model = Customer
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(WishList)
admin.site.register(Review)
admin.site.register(ProductDetail)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Seller)


admin.site.register(Person)
# admin.site.register(Membership)
# admin.site.register(Group)
