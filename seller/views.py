from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.text import slugify

from themall.models import Customer, Product
from .models import Seller
from .forms import SellerRegistrationForm



@login_required
def store_registration(request):
    if request.user.is_authenticated:
        user = Customer.objects.get(email=request.user)

    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)

        if form.is_valid():
            store_name = form.cleaned_data['store_name']
            description = form.cleaned_data['description']
            slug = slugify(store_name)

            try:
                Seller.objects.get(email=user)
                messages.error(request, 'Sorry! You have a store already.')
            except Seller.DoesNotExist:      
                seller = Seller(email=user, store_name=store_name, description=description, slug=slug)
                seller.save()
                user.is_seller = True
                user.save()
                return redirect('customer')
                messages.success(request, 'Congratulations! You\'re now a seller.')
    else:
        form = SellerRegistrationForm()

    context = {
        'form' : form,
    }

    return render(request, 'become-a-seller.html',context)




def store(request):
    product = Product.objects.filter(seller='e.manuel_07@yahoo.com')
    seller = Seller.objects.filter(email=request.user)
    # product = Product.objects.filter(seller=seller)

    context ={
        'product' : product,

    }
    return render(request, 'store.html', context)
