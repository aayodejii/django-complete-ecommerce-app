from django.urls import path, re_path
from . import views




urlpatterns = [


        
    # path('adef/', views.current_datetime, name='ajaxhom'),
    path('ajax/', views.ajax_home, name='ajaxhome'),
    path('test/', views.ajax_test, name='ajax_test'),

    path('ftestr', views.formtester),


    path('base/', views.base_template, name='base_template'),

    path('search/', views.search, name='search'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('customer-information/', views.customer_info, name='customer'),
    path('customer-information/edit', views.customer_info_edit, name='editinfo'),
    path('customer-information/orders', views.order_history, name='orderhistory'),
    path('remove-wish/<str:product>/<str:customer>/', views.remove_wish),


    path('', views.home, name = 'home'),
    # path('product/<slug:name>/', views.product,  name = 'product'),
    path('product/<str:url>/', views.product,  name = 'product'),
    path('product/wishlist/<str:product>/', views.wishlist, name='wishlist'),
    path('product/review/<str:product>/', views.review, name='review'),

    path('rating/<str:product>/<int:star>/', views.rating),
    path('category/<str:name>/', views.category,  name = 'category'),
    path('cart/', views.cart, name='cart' ),
    path('cart/<int:product>/<str:order_num>/delete/', views.cart_remove_item, name='delete-cart-item'),
    path('cart/<int:product>/<str:order_num>/update/', views.cart_update_quantity, name='update-cart-item'),

    path('admin/dashboard/', views.admin_dashboard,  name='dashboard' ),
    path('admin/orders/', views.admin_manage_order,  name='manageorders' ),
    path('admin/order-details/<str:order_num>/', views.admin_order_details,  name='manageorderdetails' ),
    path('admin/<str:category>/view-products/', views.admin_products,  name='manageproducts' ),
    path('admin/product/<str:product>/delete', views.admin_product_delete,  name='productdelete' ),
    path('admin/<str:category>/view_products/<str:product>/edit', views.admin_product_edit,  name='productupdate' ),
    path('admin/view-products-details/<str:product>/', views.admin_products_details,  name='manageproductdetails' ),
    path('admin/manage-category/', views.admin_manage_category,  name='managecategory' ),
    path('admin/manage-customer/', views.admin_manage_customer,  name='managecustomer' ),





]


 