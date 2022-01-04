import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sessions.models import Session
# from django.core import serializers
# from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt


from .models import Product, ProductDetail, Order, OrderDetail, Category, Customer, CustomerSession, WishList, Review
from .forms import AddToCart, OrderForm, ManageProduct, ManageProductDetail, SignUpForm, LoginForm, UpdateInfoForm, ReviewForm, ManageCategory, DeleteForm, UpdateForm

# from utils import  update_cart, create_or_update_product
from .utils.api.order import create_order_number, create_new_order
from .utils.api.product import create_or_update_product, most_purchased_product, out_of_stock
from .utils.api.cart import update_cart

from seller.models import Seller 


def formtester(request):
    return render(request, 'formtester.html')

# async def current_datetime(request):  
#     await asyncio.sleep(-105.5)
#     now = datetime.datetime.now()
#     html = '<html><body>It is now %s.</body></html>' % now
#     return HttpResponse(html)

def base_template(request):
    pass

def ajax_home(request):

    return render(request, 'ajaxhome.html', {})

def ajax_test(request):
    result = Category.objects.all()
    data = []
    for item in result:
    
        category = {
                'name': item.name,
                'desc': item.description
            }
        data.append(category)
    
    return JsonResponse(data, safe=False)

    # return render(request, 'ajaxtest.html', {})
     

def search(request):
    q = request.GET.get('q')
    query = Product.objects.filter(name__icontains=q)
    return render(request, 'search.html', {'query' : query})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = Customer.objects.create_user(email=email, password=password)
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            
            update_cart(request, form)

            auth.login(request, user)
            return redirect ('home')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                update_cart(request, form)
                auth.login(request, user)

                # reverse('home',)
                # return redirect(reverse('home',)) #4 find how to redirect appr.
            else:
                messages.info(request, 'Incorrect, check your inputs!,')
    else:
        if request.user.is_authenticated:
            return redirect('home') #improve
        form = LoginForm()

    return render(request, 'login.html', {'form' : form,})


def logout(request):

    request.session['name'] = 'username'
    request.session['key'] = request.session.session_key
    p_old = request.session.session_key
    session = CustomerSession(session_key=p_old)
    session.save()
    auth.logout(request)


    return redirect('home')

@login_required
def customer_info(request):	
    orders = Order.objects.filter(customer=request.user.get_username())
    context = {
        'orders' : orders,

    }

    return render(request, 'profile.html', context)


@login_required
def customer_info_edit(request):
    if request.method == 'POST':
            form = UpdateInfoForm(request.POST, instance=request.user)

            if form.is_valid():
                form.save() 
                messages.success(request, f' Your account has been updated! ')
                return redirect('customer')
    else:
            form = UpdateInfoForm(instance=request.user)

    context = {
                'form' : form,

            }

    return render(request, 'editprofile.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user.get_username())

    context = {
        'orders': orders,
    }

    return render (request, 'orderhistory.html', context,)



def home(request):

    # all_items = Product.objects.all()
    # most_purchased_product = most_purchased_product(); #why is it not getting assigned
    categories = Category.objects.all()
    
    context = {
        # 'all_items' : all_items,
        # 'most_purchased_product' : most_purchased_product,
    }

    for category in categories:
        key = (str(category) + "_items").lower()
        query = Product.objects.filter(category=category)
        context.update({key:query})
    
    context.update({'most_purchased_product' :most_purchased_product()})


    return render(request, 'mall.html', context)


def product(request, url):



    """ use this session variable to set viewed product/ or cookies/storage """
    request.session['name'] = 'username'
    request.session['password'] = 'password123'
    session_key = request.session.session_key

    """ this try block is responsible for displaying the actual product and associated information.... """
    try:
        product = Product.objects.get(url=url)
    except Product.DoesNotExist:
        raise Http404("Product does not exist...make explicit")


    if request.user.is_authenticated:
            user_str = request.user.get_username()
            user = Customer.objects.get(email=user_str)
        
            can_review = user.can_review(product)

    else:
        user = ''
        can_review = False
    

        

    ''' when a user attempts to add a product to cart  '''
    if request.method == 'POST':
        order_form = AddToCart(request.POST)
        review_form = Review(request.POST)

        if order_form.is_valid():
            quantity = order_form.cleaned_data.get('quantity')
            
            if product.quantity == 0:
                messages.info(request, 'Sorry! %s is out of stock' % product)
                return render(request, 'product.html', {'product': product, 'order_form': order_form, })

            elif product.quantity < int(quantity):
                messages.info(request, 'Sorry! only %s unit(s) are left' % product.quantity)
                return render(request, 'product.html', {'product': product, 'order_form': order_form, })

            order_num = create_order_number()
            
            date = datetime.datetime.now()

            ''' this if block checks if the product has an offer price, else set the standard price '''
        
            price = product.set_price(quantity)
            offer = product.is_an_offer()

        

            status = 'still-shopping'  # logic later #2
            
            if Order.objects.filter(customer=user) or Order.objects.filter(session_key=session_key):
                try:
                    user_last_order = Order.objects.get(session_key=session_key)  # check the status of the user last order
                except ObjectDoesNotExist:
                    user_last_order = Order.objects.filter(customer=user).last() 

                ''' if the status is still-shopping, create a corresponding other detail '''
                if user_last_order.status == 'still-shopping':
                    # pow()
                    user_last_order_num = user_last_order.order_num

                    if Order.objects.filter(orderdetail__order_num=user_last_order_num,
                                            orderdetail__product=product).exists():
                        p = OrderDetail.objects.get(order_num=user_last_order_num, product=product)
                        p.quantity = quantity
                        p.price = price
                        p.save()
                        
                        messages.info(request, '%s quantity has been updated' % product)
            
                    else:
                        add_more = OrderDetail(order_num=user_last_order, product=product, quantity=quantity, price=price,
                                            offer=offer, bill_date=date, ship_date=date)
                        add_more.save()
                        messages.info(request, '%s has been added to cart' % product)


                elif user_last_order.status == 'paid-order': #3
                    user = user_last_order.customer
                
                    create_new_order(request, order_num, user, session_key, date, status, product, quantity, price, offer)


                # elif user_last_order.status == 'cancelled:

            else:
                #1 anonmous user
                create_new_order(request, order_num, user, session_key, date, status, product, quantity, price, offer)
                
                messages.info(request, 'First TimeR!')


    else:
        order_form = AddToCart()
        review_form = ReviewForm()

    context = {
        'product': product,
        'order_form': order_form,
        'review_form': review_form, 
        'can_review': can_review
    }


    return render(request, 'product.html', context)

@csrf_exempt
def rating(request, product, star):

    product = Product.objects.get(name=product)
    if product.rating is not None:

        rated = product.rated_times
        sum_rated = product.sum_rated
    else:
        rated = 0
        sum_rated = 0
    # new_rating = float(str(Rating.objects.get(star=star)))
    new_rating = float(star)
    rating = (sum_rated + new_rating)/(rated + 1)
    # rating = Rating.objects.get(star=int(rating))
    product.rating = rating
    product.rated_times += 1
    product.sum_rated += star
    product.save()
    messages.info(request, 'Thanks for your response!') #is not returning msg
    


    # return redirect('product', url=product.url)
    return render(request, 'product.html', {'product': product, })


def review(request, product):
    # if request.method == 'POST':
    product = Product.objects.get(name=product)

    review_form = ReviewForm(request.POST)
    if review_form.is_valid():
        review = review_form.cleaned_data.get('review')
        rating = review_form.cleaned_data.get('rating')
        customer = Customer.objects.get(email=request.user.get_username())
        if Review.objects.filter(product=product, customer=customer).exists():
            messages.info(request, 'you cant')
            return redirect('product', url=product.url)

        else:

            data = Review(product=product, review=review, rating=rating, customer=customer)
            data.save()


            if product.rating !=0:

                rated = product.rated_times
                sum_rated = product.sum_rated
            else:
                rated = 0
                sum_rated = 0
            new_rating = float(rating)
            rating_calc = (sum_rated + new_rating)/(rated + 1)
            product.rating = rating_calc
            product.rated_times += 1
            product.sum_rated += int(rating)
            product.save()
            messages.info(request, 'Thanks for your response!')

    return redirect('product', url=product.url)

    # return render(request, 'product.html', {'product': product, })

                


def wishlist(request, product):	
    product = Product.objects.get(url=product)

    if request.user.is_authenticated:
        customer = Customer.objects.get(email=request.user.get_username())

        try:
            get_wish = WishList.objects.get(customer=customer, product=product)
            messages.info(request, '%s is already in your Wishlist' %product.name)
            return redirect('product', url=product.url)

        except ObjectDoesNotExist:
            wish = WishList(customer=customer, product=product)
            wish.save()
            messages.info(request, '%s has been added to your Wishlist' %product.name)
    else:
        messages.info(request, 'You need to be logged-in')

    return redirect('product', url=product.url)

@csrf_exempt
def remove_wish(request, customer, product):
    customer = Customer.objects.get(email=customer)
    product = Product.objects.get(name=product)
    
    wish = WishList.objects.get(customer=customer, product=product)
    wish.delete()
    messages.info(request, '%s has been removed from your Wishlist' %product.name)
    
    return render(request, 'viewproducts.html')





def category(request, name):
    category = Product.objects.filter(category=name).all()


    return render (request, 'category.html', {'items' : category})

def cart(request):



    session_key = request.session.session_key
    
    """
    1. if user is auth. check if he has orders in cart, if true display
    2. try: use session key as look up, if exist display
    3. except
    
    """
    if request.user.is_authenticated:
        user = request.user.get_username()
        try:
            active_order = Order.objects.get(customer=user, status='still-shopping')
            active_orders = OrderDetail.objects.filter(order_num=active_order.order_num)

        except ObjectDoesNotExist:
            active_order = ''
            active_orders = ''
    else:
        try:
            active_order = Order.objects.get(session_key=session_key, status='still-shopping')
            product_ordered = OrderDetail.objects.filter(order_num=active_order.order_num)
            active_orders = product_ordered.all()

        except ObjectDoesNotExist:
            active_order = ''
            active_orders = ''

    if request.method == 'POST':

        order_form = OrderForm(request.POST)
        update_form = UpdateForm(request.POST)
        if request.user.is_authenticated:
            if order_form.is_valid():
                op = request.user.get_full_name()
                # pow()
                if request.user.profile_completed():

                    update_order = Order.objects.get(customer=request.user.get_username(), status='still-shopping')		
                    product = OrderDetail.objects.filter(order_num=update_order)
                    
                    for items in product:
                        item = items.product
                        quantity = items.quantity
                        get_quantity = Product.objects.get(name=item)
                        total_quantity = get_quantity.quantity
                        new_quantity = total_quantity - int(quantity)
                        get_quantity.quantity = new_quantity
                        get_quantity.save()

                    update_order.status = 'paid-order'
                    update_order.session_key = ''
                    update_order.save()

                    messages.info(request, 'Your order has been made,... It will be delivered... ')
                    return redirect('cart')

                else:
                    
                    messages.info(request, 'You need to provide your contact details')
                    return redirect('editinfo')

        else:
            messages.info(request, 'You need to login before you can check out')
            return redirect('login')
    
    else:

        order_form = OrderForm()
        update_form = UpdateForm()


    context = {
        'order_form': order_form,
        'active_orders': active_orders,
        'active_order': active_order,
        'update_form' : update_form
    }

    return render(request, 'cart.html', context)

def cart_remove_item(request, order_num, product):
    
    item = OrderDetail.objects.get(order_num=order_num, product=product)

    if request.method == 'POST':
        data ={'remove': True}
        delete_form = DeleteForm(data)
        delete = delete_form['remove'].data
        
        if delete is True:
            item.delete()
            return redirect('cart')

    return render (request, 'cart.html', {})


def cart_update_quantity(request, order_num, product):
    item = OrderDetail.objects.get(order_num=order_num, product=product)


    if request.method == 'POST':
        update_form = UpdateForm(request.POST)
        
        if update_form.is_valid():
            product = Product.objects.get(name=item.product)
            quantity = update_form.cleaned_data.get('quantity')

            price = product.set_price(quantity)

            if quantity > product.quantity:				
                messages.error(request, 'Sorry! only %s unit left' %product.quantity)
            
                return redirect('cart')
                
            item.quantity = quantity
            item.price = price
            item.save()
            messages.success(request, 'Updated...')

            return redirect('cart')

    return render (request, 'cart.html', {})




@permission_required('themall.change_category', raise_exception=True)
def admin_dashboard(request):
    all_category = Category.objects.all()
    oos_count, oos_products = out_of_stock()
    total_products = Product.objects.count()

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    today = datetime.date.today()
    start_date = datetime.date(2020, 7, 18)
    end_date = datetime.date(2020, 7, 18)
    recent_orders = Order.objects.filter(date__range=(yesterday, today))
    solo = settings.SELLER
    context = {
        'recent': recent_orders,
        'all_category' : all_category,
        'oos_count' : oos_count, 
        'total_products' : total_products,
        'solo': solo,

    }

    return render(request, 'dashboard.html', context)

@permission_required('themall.change_category', raise_exception=True)
def admin_manage_order(request):
    total_orders = Order.objects.count()

    orders = Order.objects.all()
    paginator = Paginator(orders, 7) # Show 25 orders per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ra = range(2,page_obj.paginator.num_pages)

    context = {
        'total_orders': total_orders,
        'orders': orders,
        'page_obj': page_obj,
        'ra': ra,
    
    }

    return render(request, 'manageorders.html', context)


@permission_required('themall.change_category', raise_exception=True)
def admin_order_details(request, order_num):
    order = Order.objects.get(order_num=order_num)
    details = OrderDetail.objects.filter(order_num=order_num).all()
    
    try:
        customer_info = Customer.objects.get(email=order.customer)
    except ObjectDoesNotExist:
        customer_info = None

    context = {
        'order' : order,
        'details': details,
        'customer': customer_info,
    }

    return render(request, 'orderdetails.html', context)


@permission_required('themall.change_category', raise_exception=True)
def admin_manage_category(request):
    all_categories = Category.objects.all()
    if request.method == 'POST':
        form = ManageCategory(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Updated..')
            form = ManageCategory()

    else:
        form = ManageCategory()


    context = {
        'all_categories': all_categories,
        'form': form,

    }

    return render(request, 'viewcategories.html', context)


@permission_required('themall.change_category', raise_exception=True)
def admin_products(request, category):
    all_products = Product.objects.filter(category=category)
    all_categories = Category.objects.all()
    category = Category.objects.get(name=category)
    if request.method == 'POST':
        category = Category.objects.get(name=category)

        add_form = ManageProduct(request.POST)
        details_form = ManageProductDetail(request.POST, request.FILES)
        files = request.FILES.getlist('picture')

        
        if add_form.is_valid() and details_form.is_valid():
        

            # print(add_form['name'].value)
            # name = add_form.cleaned_data.get('name')

            # pow()
            create_or_update_product(add_form, details_form, category, files, edit=False)
            messages.info(request, '%s has been added to stock' %add_form.cleaned_data.get('name'))


            add_form = ManageProduct()
            details_form = ManageProductDetail()

        
    else:
        add_form = ManageProduct()
        details_form = ManageProductDetail()

    context = {
        'all_products' : all_products,
        'all_categories' : all_categories,
        'add_form' : add_form,	
        'details_form' : details_form,
        'category' : category
    }

    return render(request, 'viewproducts.html', context)


@permission_required('themall.change_category', raise_exception=True)
def admin_product_edit(request, category, product):

    product = Product.objects.get(url=product)
    category = product.category

    add_form = ManageProduct(instance=product)
    details_form = ManageProductDetail(instance=product.productdetail)

    if request.method =='POST':
        product = Product.objects.get(name=product)

        add_form = ManageProduct(request.POST, instance=product)
        details_form = ManageProductDetail(request.POST, request.FILES, instance=product.productdetail)
        files = request.FILES.getlist('picture')


        if add_form.is_valid() and details_form.is_valid():
            r = request.GET.get('1')
            # pow()
            create_or_update_product(add_form, details_form, category, files, product, edit=True)
            messages.info(request, '%s was successfully modified' %product)

            return redirect('manageproducts', category=category.name, permanent=True)
            

    context = {
            'product' : product,
            'add_form' : add_form,	
            'details_form' : details_form,
    }
    
    return render (request, 'viewproduct-edit.html', context)


@csrf_exempt
@permission_required('themall.change_category', raise_exception=True)
def admin_product_delete(request, product):
    product = Product.objects.get(name=product)
    product.delete()
    # all_product = Product.objects.filter(category=product.category)

    return render(request, 'viewproducts.html')		


@permission_required('themall.change_category', raise_exception=True)
def admin_products_details(request, product):
    try:
        product = Product.objects.get(url=product)
        details = ProductDetail.objects.get(product=product)

    except ObjectDoesNotExist:
        details = ''

    context ={
        'product': product,
        'details': details,

    }

    return render(request, 'viewproductdetails.html', context)


@permission_required('themall.change_category', raise_exception=True)
def admin_manage_customer(request):
    all_customers = Customer.objects.all()


    return render (request, 'customer.html', {'customers' : all_customers} )
