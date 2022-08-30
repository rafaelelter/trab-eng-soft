from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='tickets-home'),
    path('signup/', views.signup, name='signup'),
    path('signup/offerer/', views.signup_offerer, name='signup_offerer'),
    path('signup/buyer/', views.signup_buyer, name='signup_buyer'),
    path("login/", auth_views.LoginView.as_view(template_name="tickets/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]