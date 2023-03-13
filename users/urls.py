from django.contrib import admin
from django.urls import path
from django.urls import include
from users import views
from django.contrib.auth.decorators import login_required

from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('home', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('<str:email>/<str:name>/add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('<str:email>/place-order', views.place_order, name='place_order'),
   # path('products/order', views.order_details),
    

]