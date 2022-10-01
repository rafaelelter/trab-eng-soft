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
    path("search/", views.search_offerer, name="search_offerer"),
    path("profile/<int:pk>/", views.profile_view, name="profile"),
    path("ticket/<int:pk>/", views.ticket_view, name="ticket"),
    path("create_ticket/", views.create_ticket, name="create_ticket"),
    path("edit_ticket/<int:pk>/", views.edit_ticket, name="edit_ticket"),
    path("delete_ticket/<int:pk>/", views.delete_ticket, name="delete_ticket"),
    path("purchase_ticket/<int:pk>/", views.purchase_ticket, name="purchase_ticket"),
    path("approve_offerer/<int:pk>/", views.approve_offerer, name="approve_offerer"),
]