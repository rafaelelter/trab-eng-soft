from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signup/buyer', views.signup_buyer, name='signup-buyer'),
    path('signup/offerer', views.signup_offerer, name='signup-offerer'),
]