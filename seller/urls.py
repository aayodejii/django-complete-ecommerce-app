from django.urls import path

from . import views


urlpatterns = [
    path('', views.store, name='store'),
    path('become-a-seller/', views.store_registration, name='become-a-seller'),
]